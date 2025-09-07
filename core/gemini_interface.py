"""
Gemini AI Interface Module
Professional AI integration for therapy system
Handles all interactions with Gemini 2.5 Pro for therapeutic conversations
"""

import os
import time
import json
import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import aiohttp
from pathlib import Path

# Note: In a real implementation, you would use the official Google AI SDK
# For demonstration, this shows the structure and integration patterns


class ConversationMode(Enum):
    """Different conversation modes for therapy"""
    ASSESSMENT = "assessment"
    THERAPY_SESSION = "therapy_session"
    CRISIS_INTERVENTION = "crisis_intervention"
    PSYCHOEDUCATION = "psychoeducation"
    SKILL_BUILDING = "skill_building"
    HOMEWORK_REVIEW = "homework_review"
    TERMINATION = "termination"


class ResponseType(Enum):
    """Types of AI responses"""
    THERAPEUTIC = "therapeutic"
    ASSESSMENT_QUESTION = "assessment_question"
    CRISIS_RESPONSE = "crisis_response"
    SKILL_INSTRUCTION = "skill_instruction"
    HOMEWORK_ASSIGNMENT = "homework_assignment"
    SUMMARY = "summary"
    REFERRAL = "referral"


class SafetyLevel(Enum):
    """Safety levels for content filtering"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ConversationContext:
    """Context for therapeutic conversation"""
    patient_id: str
    session_id: str
    therapy_modality: str
    session_number: int
    treatment_phase: str
    current_mood: Optional[str] = None
    risk_level: str = "low"
    active_goals: List[str] = field(default_factory=list)
    recent_assessments: Dict[str, Any] = field(default_factory=dict)
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    cultural_considerations: List[str] = field(default_factory=list)
    preferred_interventions: List[str] = field(default_factory=list)


@dataclass
class TherapeuticPrompt:
    """Structured therapeutic prompt for Gemini"""
    system_prompt: str
    context_prompt: str
    user_message: str
    mode: ConversationMode
    safety_instructions: str
    expected_response_type: ResponseType
    max_tokens: int = 1000
    temperature: float = 0.7


@dataclass
class AIResponse:
    """AI response with metadata"""
    content: str
    response_type: ResponseType
    confidence_score: float
    safety_flags: List[str] = field(default_factory=list)
    suggested_interventions: List[str] = field(default_factory=list)
    risk_indicators: List[str] = field(default_factory=list)
    follow_up_needed: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    tokens_used: int = 0


class GeminiTherapyInterface:
    """Professional AI interface for therapy sessions"""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        # Configuration
        self.config = config or {}
        self.model_name = self.config.get("model_name", "gemini-2.5-pro")
        self.max_tokens = self.config.get("max_tokens", 8192)
        self.temperature = self.config.get("temperature", 0.7)
        self.top_p = self.config.get("top_p", 0.9)
        self.top_k = self.config.get("top_k", 40)
        
        # Safety and compliance
        self.safety_settings = self._initialize_safety_settings()
        self.therapy_guidelines = self._initialize_therapy_guidelines()
        self.prompt_templates = self._initialize_prompt_templates()
        
        # Conversation management
        self.conversation_memory: Dict[str, List[Dict[str, Any]]] = {}
        self.safety_monitor = TherapySafetyMonitor()
        
        # Logging
        self.logger = logging.getLogger(__name__)
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # seconds
    
    def _initialize_safety_settings(self) -> Dict[str, str]:
        """Initialize safety settings for therapeutic context"""
        return {
            "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE", 
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_HIGH_ONLY",  # More permissive for therapy
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_MEDICAL": "BLOCK_NONE",  # Allow medical/mental health content
            "HARM_CATEGORY_DEROGATORY": "BLOCK_MEDIUM_AND_ABOVE"
        }
    
    def _initialize_therapy_guidelines(self) -> Dict[str, str]:
        """Initialize therapeutic practice guidelines"""
        return {
            "professional_boundaries": """
                Maintain professional therapeutic boundaries at all times.
                Do not engage in dual relationships or personal disclosure.
                Redirect inappropriate personal questions back to therapy focus.
            """,
            
            "crisis_protocols": """
                If patient expresses suicidal ideation, self-harm, or danger to others:
                1. Assess immediacy and severity of risk
                2. Validate feelings while promoting safety
                3. Explore protective factors and support systems
                4. Consider need for crisis intervention or emergency services
                5. Document all risk-related information thoroughly
                Never minimize or dismiss expressions of suicidal thoughts.
            """,
            
            "therapeutic_stance": """
                Maintain warm, empathetic, and non-judgmental stance.
                Use person-first language and avoid diagnostic labels in conversation.
                Validate patient emotions while promoting adaptive coping.
                Focus on patient strengths and resilience.
                Encourage patient autonomy and self-efficacy.
            """,
            
            "confidentiality": """
                Maintain strict confidentiality except for:
                - Imminent risk of harm to self or others
                - Suspected child or elder abuse
                - Court-ordered disclosure
                Explain limits of confidentiality clearly.
            """,
            
            "evidence_based_practice": """
                Use evidence-based interventions appropriate to patient's needs.
                Adapt interventions based on cultural considerations.
                Monitor treatment progress and adjust approaches as needed.
                Provide psychoeducation to enhance patient understanding.
            """
        }
    
    def _initialize_prompt_templates(self) -> Dict[ConversationMode, str]:
        """Initialize mode-specific prompt templates"""
        return {
            ConversationMode.THERAPY_SESSION: """
                You are a professional AI therapy assistant conducting a therapy session.
                
                THERAPEUTIC APPROACH: Use {therapy_modality} principles and techniques.
                TREATMENT PHASE: {treatment_phase}
                SESSION: {session_number} 
                PATIENT CONTEXT: {patient_context}
                
                GUIDELINES:
                - Maintain professional, warm, and empathetic tone
                - Use appropriate therapeutic interventions for the modality
                - Validate emotions while promoting adaptive thinking/behavior
                - Ask open-ended questions to facilitate exploration
                - Provide psychoeducation when appropriate
                - Monitor for risk factors and respond appropriately
                - Stay focused on therapeutic goals
                
                SAFETY PRIORITIES:
                - Assess and respond to any expressions of self-harm or suicide
                - Monitor for signs of psychosis or severe mental distress
                - Maintain professional boundaries
                - Encourage appropriate help-seeking behavior
                
                Respond as a skilled therapist would, providing therapeutic support while 
                maintaining professional standards and safety awareness.
            """,
            
            ConversationMode.ASSESSMENT: """
                You are conducting a clinical assessment interview.
                
                ASSESSMENT FOCUS: {assessment_type}
                PATIENT CONTEXT: {patient_context}
                
                GUIDELINES:
                - Ask clear, specific assessment questions
                - Gather relevant clinical information systematically
                - Assess for risk factors and safety concerns
                - Remain objective and non-judgmental
                - Explain the purpose of questions when helpful
                - Be sensitive to patient comfort level
                
                CRITICAL: Always assess for suicidal ideation, self-harm, and risk to others.
                Document any concerning responses for clinical review.
                
                Conduct this assessment professionally while building therapeutic rapport.
            """,
            
            ConversationMode.CRISIS_INTERVENTION: """
                You are providing crisis intervention support.
                
                CRISIS CONTEXT: {crisis_details}
                RISK LEVEL: {risk_level}
                
                IMMEDIATE PRIORITIES:
                1. Ensure immediate safety
                2. Assess severity and imminence of risk
                3. Validate distress while promoting hope
                4. Identify protective factors and support systems
                5. Develop safety plan if appropriate
                6. Consider need for emergency services
                
                APPROACH:
                - Remain calm and supportive
                - Use active listening and validation
                - Ask direct questions about safety
                - Avoid minimizing or dismissing concerns
                - Focus on immediate coping and safety
                - Provide crisis resources and contacts
                
                This is a crisis situation - prioritize safety above all other considerations.
            """,
            
            ConversationMode.SKILL_BUILDING: """
                You are teaching therapeutic skills and techniques.
                
                SKILL FOCUS: {skill_type}
                THERAPY MODALITY: {therapy_modality}
                PATIENT LEVEL: {difficulty_level}
                
                TEACHING APPROACH:
                - Explain skills clearly and simply
                - Provide concrete examples and applications
                - Use interactive practice when possible
                - Check for understanding frequently
                - Adapt explanations to patient's learning style
                - Connect skills to patient's specific situations
                - Assign appropriate homework/practice
                
                SKILLS FOCUS AREAS:
                - Cognitive restructuring techniques
                - Emotional regulation strategies
                - Behavioral activation methods
                - Mindfulness and grounding exercises
                - Interpersonal communication skills
                - Crisis coping strategies
                
                Make learning engaging and relevant to patient's daily life.
            """,
            
            ConversationMode.PSYCHOEDUCATION: """
                You are providing psychoeducation about mental health.
                
                TOPIC: {education_topic}
                PATIENT CONTEXT: {patient_context}
                
                EDUCATIONAL GOALS:
                - Increase understanding of mental health conditions
                - Normalize experiences and reduce stigma
                - Explain treatment rationale and options
                - Promote hope and self-efficacy
                - Encourage active participation in treatment
                
                APPROACH:
                - Use clear, accessible language
                - Avoid overwhelming with too much information
                - Check understanding and answer questions
                - Provide relevant examples and analogies
                - Connect information to patient's experience
                - Encourage questions and curiosity
                
                Make complex concepts understandable while maintaining accuracy.
            """
        }
    
    def create_therapeutic_prompt(self, context: ConversationContext, 
                                user_message: str, mode: ConversationMode) -> TherapeuticPrompt:
        """Create structured therapeutic prompt for Gemini"""
        
        # Get base template
        template = self.prompt_templates.get(mode, self.prompt_templates[ConversationMode.THERAPY_SESSION])
        
        # Format with context
        context_vars = {
            'therapy_modality': context.therapy_modality,
            'treatment_phase': context.treatment_phase,
            'session_number': context.session_number,
            'patient_context': self._format_patient_context(context),
            'risk_level': context.risk_level
        }
        
        system_prompt = template.format(**context_vars)
        
        # Add conversation history
        history_prompt = self._format_conversation_history(context.conversation_history)
        
        # Create context prompt
        context_prompt = f"""
        CURRENT SESSION CONTEXT:
        - Session #{context.session_number}
        - Therapy Modality: {context.therapy_modality}
        - Treatment Phase: {context.treatment_phase}
        - Current Risk Level: {context.risk_level}
        - Active Goals: {', '.join(context.active_goals) if context.active_goals else 'None set'}
        
        RECENT CONVERSATION:
        {history_prompt}
        
        PATIENT'S CURRENT MESSAGE:
        "{user_message}"
        """
        
        # Safety instructions
        safety_instructions = f"""
        SAFETY REQUIREMENTS:
        {self.therapy_guidelines['crisis_protocols']}
        {self.therapy_guidelines['professional_boundaries']}
        
        MONITOR FOR:
        - Suicidal or self-harm ideation
        - Threats to others
        - Psychotic symptoms
        - Severe distress requiring immediate attention
        
        If ANY safety concerns arise, prioritize safety response over other therapeutic goals.
        """
        
        return TherapeuticPrompt(
            system_prompt=system_prompt,
            context_prompt=context_prompt,
            user_message=user_message,
            mode=mode,
            safety_instructions=safety_instructions,
            expected_response_type=self._determine_response_type(mode, user_message),
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
    
    def _format_patient_context(self, context: ConversationContext) -> str:
        """Format patient context for prompt"""
        context_parts = []
        
        if context.current_mood:
            context_parts.append(f"Current mood: {context.current_mood}")
        
        if context.recent_assessments:
            context_parts.append("Recent assessments:")
            for assessment, results in context.recent_assessments.items():
                context_parts.append(f"  {assessment}: {results}")
        
        if context.cultural_considerations:
            context_parts.append(f"Cultural considerations: {', '.join(context.cultural_considerations)}")
        
        if context.preferred_interventions:
            context_parts.append(f"Preferred interventions: {', '.join(context.preferred_interventions)}")
        
        return '\n'.join(context_parts) if context_parts else "No specific context provided"
    
    def _format_conversation_history(self, history: List[Dict[str, str]]) -> str:
        """Format conversation history for context"""
        if not history:
            return "No previous conversation in this session."
        
        # Get last 5 exchanges to maintain context without overwhelming prompt
        recent_history = history[-10:]  # Last 5 back-and-forth exchanges
        
        formatted = []
        for exchange in recent_history:
            role = exchange.get('role', 'unknown')
            content = exchange.get('content', '')
            formatted.append(f"{role.upper()}: {content}")
        
        return '\n'.join(formatted)
    
    def _determine_response_type(self, mode: ConversationMode, user_message: str) -> ResponseType:
        """Determine expected response type based on mode and message"""
        
        # Check for crisis indicators
        crisis_keywords = ['suicide', 'kill myself', 'end it all', 'hurt myself', 'die', 'hopeless']
        if any(keyword in user_message.lower() for keyword in crisis_keywords):
            return ResponseType.CRISIS_RESPONSE
        
        # Mode-based response types
        mode_mapping = {
            ConversationMode.ASSESSMENT: ResponseType.ASSESSMENT_QUESTION,
            ConversationMode.CRISIS_INTERVENTION: ResponseType.CRISIS_RESPONSE,
            ConversationMode.SKILL_BUILDING: ResponseType.SKILL_INSTRUCTION,
            ConversationMode.HOMEWORK_REVIEW: ResponseType.HOMEWORK_ASSIGNMENT,
            ConversationMode.PSYCHOEDUCATION: ResponseType.THERAPEUTIC
        }
        
        return mode_mapping.get(mode, ResponseType.THERAPEUTIC)
    
    async def generate_therapeutic_response(self, context: ConversationContext,
                                          user_message: str, 
                                          mode: ConversationMode = ConversationMode.THERAPY_SESSION) -> AIResponse:
        """Generate therapeutic response using Gemini AI"""
        
        try:
            # Rate limiting
            await self._enforce_rate_limit()
            
            # Create therapeutic prompt
            prompt = self.create_therapeutic_prompt(context, user_message, mode)
            
            # Safety pre-screening
            safety_check = self.safety_monitor.screen_message(user_message)
            if safety_check.risk_level == SafetyLevel.CRITICAL:
                return self._create_crisis_response(user_message, safety_check)
            
            # Generate AI response
            ai_response = await self._call_gemini_api(prompt)
            
            # Post-process response
            processed_response = self._process_ai_response(ai_response, prompt, context)
            
            # Update conversation history
            self._update_conversation_history(context, user_message, processed_response.content)
            
            # Safety post-screening
            response_safety = self.safety_monitor.screen_response(processed_response.content)
            processed_response.safety_flags.extend(response_safety.flags)
            
            return processed_response
            
        except Exception as e:
            self.logger.error(f"Error generating therapeutic response: {e}")
            return self._create_error_response(str(e))
    
    async def _call_gemini_api(self, prompt: TherapeuticPrompt) -> Dict[str, Any]:
        """Call Gemini API with therapeutic prompt"""
        
        # This is a placeholder for the actual Gemini API call
        # In real implementation, you would use the official Google AI SDK
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': self.model_name,
            'messages': [
                {
                    'role': 'system',
                    'content': prompt.system_prompt + '\n\n' + prompt.safety_instructions
                },
                {
                    'role': 'user', 
                    'content': prompt.context_prompt
                }
            ],
            'max_tokens': prompt.max_tokens,
            'temperature': prompt.temperature,
            'top_p': self.top_p,
            'top_k': self.top_k,
            'safety_settings': self.safety_settings
        }
        
        # Simulate API call for demonstration
        # In real implementation, replace with actual Gemini API endpoint
        simulated_response = {
            'choices': [{
                'message': {
                    'content': self._generate_simulated_response(prompt)
                },
                'finish_reason': 'stop'
            }],
            'usage': {
                'total_tokens': 500,
                'prompt_tokens': 300,
                'completion_tokens': 200
            }
        }
        
        return simulated_response
    
    def _generate_simulated_response(self, prompt: TherapeuticPrompt) -> str:
        """Generate simulated therapeutic response for demonstration"""
        
        mode_responses = {
            ConversationMode.THERAPY_SESSION: """
                I hear that you're going through a difficult time right now. It takes courage to share what you're experiencing, and I want you to know that your feelings are valid and understandable given what you've been facing.

                Let's explore this a bit more together. When you mentioned feeling overwhelmed, can you help me understand what specifically feels most overwhelming right now? Sometimes breaking things down into smaller pieces can help us see where we might start addressing these challenges.

                I also want to check in with you about your safety and well-being. How are you taking care of yourself during this difficult period? Are you getting enough sleep, eating regularly, and staying connected with supportive people in your life?

                Remember that you don't have to go through this alone, and we're going to work together to help you develop strategies that can make things feel more manageable.
            """,
            
            ConversationMode.ASSESSMENT: """
                Thank you for sharing that information with me. I'd like to ask you a few more questions to better understand your experience so we can provide you with the most helpful support.

                Over the past two weeks, how often have you been bothered by feeling down, depressed, or hopeless? Has this been something you've experienced not at all, several days, more than half the days, or nearly every day?

                I'm also wondering about your energy levels and motivation. Have you noticed changes in your interest or pleasure in activities you usually enjoy?

                These questions help me understand what you're experiencing so we can work together on the most effective approaches for your situation.
            """,
            
            ConversationMode.CRISIS_INTERVENTION: """
                I'm really concerned about you right now, and I'm glad you're talking to me about these thoughts. When you're having thoughts about not wanting to be here anymore, that tells me you're in a lot of pain, and I want to help you through this.

                Right now, I need to ask you some important questions to make sure you're safe. Are you having thoughts about ending your life or hurting yourself? If so, do you have a plan for how you might do that?

                I want you to know that these feelings can change, even when it doesn't feel that way right now. You reached out for help, which shows incredible strength. Let's work together to get you through this crisis and connected with the support you need.

                Do you have someone you can stay with tonight, or someone you can call? I want to make sure you're not alone right now.
            """,
            
            ConversationMode.SKILL_BUILDING: """
                Let's work on learning a new coping skill that can help you when you're feeling anxious or overwhelmed. I'd like to teach you a technique called "grounding" that can help bring your attention to the present moment and reduce anxiety.

                Here's how the 5-4-3-2-1 technique works:
                - 5 things you can see around you
                - 4 things you can touch or feel
                - 3 things you can hear
                - 2 things you can smell
                - 1 thing you can taste

                This technique works by engaging your senses and bringing your mind back to the present moment instead of getting caught up in anxious thoughts about the future.

                Would you like to try this technique with me right now? We can practice it together, and then you can use it on your own when you notice anxiety building up.
            """
        }
        
        return mode_responses.get(prompt.mode, mode_responses[ConversationMode.THERAPY_SESSION]).strip()
    
    def _process_ai_response(self, ai_response: Dict[str, Any], 
                           prompt: TherapeuticPrompt, 
                           context: ConversationContext) -> AIResponse:
        """Process and validate AI response"""
        
        content = ai_response['choices'][0]['message']['content']
        tokens_used = ai_response.get('usage', {}).get('total_tokens', 0)
        
        # Analyze response content
        risk_indicators = self._analyze_risk_indicators(content)
        suggested_interventions = self._identify_interventions(content, context.therapy_modality)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(content, prompt.mode)
        
        # Determine if follow-up needed
        follow_up_needed = self._requires_follow_up(content, risk_indicators)
        
        return AIResponse(
            content=content,
            response_type=prompt.expected_response_type,
            confidence_score=confidence_score,
            suggested_interventions=suggested_interventions,
            risk_indicators=risk_indicators,
            follow_up_needed=follow_up_needed,
            tokens_used=tokens_used
        )
    
    def _analyze_risk_indicators(self, content: str) -> List[str]:
        """Analyze response for risk indicators"""
        risk_indicators = []
        
        content_lower = content.lower()
        
        # Check for crisis-related content
        if any(word in content_lower for word in ['suicide', 'self-harm', 'crisis', 'emergency']):
            risk_indicators.append('crisis_content_present')
        
        # Check for assessment needs
        if any(phrase in content_lower for phrase in ['need to assess', 'further evaluation', 'concerning']):
            risk_indicators.append('assessment_recommended')
        
        # Check for referral indicators
        if any(phrase in content_lower for phrase in ['refer to', 'consult with', 'emergency services']):
            risk_indicators.append('referral_indicated')
        
        return risk_indicators
    
    def _identify_interventions(self, content: str, therapy_modality: str) -> List[str]:
        """Identify therapeutic interventions mentioned in response"""
        interventions = []
        
        content_lower = content.lower()
        
        # CBT interventions
        if 'cognitive' in content_lower or 'thought' in content_lower:
            interventions.append('cognitive_restructuring')
        if 'behavior' in content_lower or 'activity' in content_lower:
            interventions.append('behavioral_activation')
        
        # DBT interventions  
        if 'mindfulness' in content_lower:
            interventions.append('mindfulness')
        if 'distress tolerance' in content_lower:
            interventions.append('distress_tolerance')
        
        # General interventions
        if 'grounding' in content_lower:
            interventions.append('grounding_techniques')
        if 'breathing' in content_lower:
            interventions.append('breathing_exercises')
        if 'relaxation' in content_lower:
            interventions.append('relaxation_training')
        
        return interventions
    
    def _calculate_confidence_score(self, content: str, mode: ConversationMode) -> float:
        """Calculate confidence score for response"""
        base_score = 0.8
        
        # Length appropriateness
        word_count = len(content.split())
        if 50 <= word_count <= 200:
            base_score += 0.1
        elif word_count < 20 or word_count > 300:
            base_score -= 0.2
        
        # Mode-appropriate content
        if mode == ConversationMode.CRISIS_INTERVENTION:
            if any(word in content.lower() for word in ['safety', 'support', 'help']):
                base_score += 0.1
        
        return min(max(base_score, 0.0), 1.0)
    
    def _requires_follow_up(self, content: str, risk_indicators: List[str]) -> bool:
        """Determine if response requires follow-up"""
        
        # Always follow up on crisis content
        if 'crisis_content_present' in risk_indicators:
            return True
        
        # Follow up on referral recommendations
        if 'referral_indicated' in risk_indicators:
            return True
        
        # Follow up on incomplete responses
        if len(content.split()) < 20:
            return True
        
        return False
    
    def _create_crisis_response(self, user_message: str, safety_check: Any) -> AIResponse:
        """Create immediate crisis response"""
        
        crisis_content = """
        I'm very concerned about what you've shared with me. Your safety is the most important thing right now, and I want to help you through this difficult time.

        If you are in immediate danger of hurting yourself or others, please:
        - Call 911 (emergency services)
        - Go to your nearest emergency room
        - Call the National Suicide Prevention Lifeline: 988

        You don't have to go through this alone. There are people who want to help you, and these feelings can change with the right support.

        Can you tell me if you're in a safe place right now? Is there someone who can be with you today?
        """
        
        return AIResponse(
            content=crisis_content.strip(),
            response_type=ResponseType.CRISIS_RESPONSE,
            confidence_score=1.0,
            safety_flags=['crisis_intervention_needed'],
            risk_indicators=['immediate_safety_concern'],
            follow_up_needed=True
        )
    
    def _create_error_response(self, error_message: str) -> AIResponse:
        """Create error response for system failures"""
        
        error_content = """
        I apologize, but I'm experiencing a technical difficulty right now. Your wellbeing is important to me, and I want to make sure you get the support you need.

        If this is an urgent situation, please don't hesitate to:
        - Contact your therapist or healthcare provider
        - Call a crisis helpline if you're in distress
        - Seek emergency help if you're in immediate danger

        Please try again in a few moments, or contact technical support if the problem continues.
        """
        
        return AIResponse(
            content=error_content.strip(),
            response_type=ResponseType.THERAPEUTIC,
            confidence_score=0.5,
            safety_flags=['system_error'],
            follow_up_needed=True
        )
    
    def _update_conversation_history(self, context: ConversationContext, 
                                   user_message: str, ai_response: str):
        """Update conversation history"""
        
        # Add to context history
        context.conversation_history.extend([
            {'role': 'user', 'content': user_message, 'timestamp': datetime.now().isoformat()},
            {'role': 'assistant', 'content': ai_response, 'timestamp': datetime.now().isoformat()}
        ])
        
        # Maintain memory limit
        max_history = 20  # 10 exchanges
        if len(context.conversation_history) > max_history:
            context.conversation_history = context.conversation_history[-max_history:]
        
        # Store in memory by session
        session_key = f"{context.patient_id}_{context.session_id}"
        self.conversation_memory[session_key] = context.conversation_history
    
    async def _enforce_rate_limit(self):
        """Enforce rate limiting for API calls"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last)
        
        self.last_request_time = time.time()
    
    def generate_session_summary(self, context: ConversationContext) -> str:
        """Generate session summary based on conversation"""
        
        if not context.conversation_history:
            return "No conversation occurred in this session."
        
        # Extract key themes and topics
        all_content = ' '.join([
            exchange['content'] for exchange in context.conversation_history 
            if exchange['role'] == 'user'
        ])
        
        # Simple keyword extraction for demonstration
        # In real implementation, this would use more sophisticated NLP
        themes = []
        if 'anxiety' in all_content.lower():
            themes.append('anxiety management')
        if 'depression' in all_content.lower():
            themes.append('depression symptoms')
        if 'stress' in all_content.lower():
            themes.append('stress coping')
        if 'relationship' in all_content.lower():
            themes.append('relationship issues')
        
        summary = f"""
        SESSION SUMMARY:
        Session #{context.session_number}
        Therapy Modality: {context.therapy_modality}
        Treatment Phase: {context.treatment_phase}
        
        Main Topics Discussed: {', '.join(themes) if themes else 'General support and check-in'}
        
        Session Notes:
        - Patient engaged in therapeutic conversation
        - Risk level maintained at: {context.risk_level}
        - Conversation exchanges: {len(context.conversation_history) // 2}
        
        Follow-up Recommendations:
        - Continue with current treatment approach
        - Monitor progress on active goals
        - Assess for any emerging concerns
        """
        
        return summary.strip()
    
    def get_conversation_insights(self, context: ConversationContext) -> Dict[str, Any]:
        """Extract insights from conversation for clinical documentation"""
        
        insights = {
            'session_metrics': {
                'total_exchanges': len(context.conversation_history) // 2,
                'session_duration_estimated': len(context.conversation_history) * 2,  # minutes
                'patient_engagement': 'active' if len(context.conversation_history) > 4 else 'limited'
            },
            'clinical_observations': [],
            'risk_factors': [],
            'therapeutic_progress': [],
            'recommendations': []
        }
        
        # Analyze conversation content
        user_messages = [
            exchange['content'] for exchange in context.conversation_history 
            if exchange['role'] == 'user'
        ]
        
        all_user_content = ' '.join(user_messages).lower()
        
        # Clinical observations
        if 'anxious' in all_user_content or 'worried' in all_user_content:
            insights['clinical_observations'].append('Patient reported anxiety symptoms')
        if 'sad' in all_user_content or 'depressed' in all_user_content:
            insights['clinical_observations'].append('Patient reported depressive symptoms')
        if 'better' in all_user_content or 'improved' in all_user_content:
            insights['therapeutic_progress'].append('Patient reported improvement')
        
        # Risk factors
        risk_keywords = ['suicide', 'hurt', 'hopeless', 'worthless', 'die']
        if any(keyword in all_user_content for keyword in risk_keywords):
            insights['risk_factors'].append('Risk indicators present - requires follow-up')
        
        # Recommendations
        if context.risk_level != 'low':
            insights['recommendations'].append('Continue safety monitoring')
        if len(user_messages) < 3:
            insights['recommendations'].append('Encourage more active participation')
        
        return insights


class TherapySafetyMonitor:
    """Safety monitoring for therapeutic conversations"""
    
    def __init__(self):
        self.risk_keywords = {
            'suicide': ['suicide', 'kill myself', 'end it all', 'better off dead', 'suicidal'],
            'self_harm': ['cut myself', 'hurt myself', 'self-harm', 'self harm'],
            'violence': ['hurt someone', 'kill them', 'violent', 'weapon'],
            'crisis': ['emergency', 'crisis', 'help me', 'desperate'],
            'psychosis': ['voices', 'hallucination', 'paranoid', 'conspiracy']
        }
    
    def screen_message(self, message: str) -> 'SafetyScreeningResult':
        """Screen user message for safety concerns"""
        
        message_lower = message.lower()
        risk_level = SafetyLevel.LOW
        flags = []
        recommendations = []
        
        # Check for high-risk keywords
        for category, keywords in self.risk_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                flags.append(f'{category}_indicators')
                
                if category in ['suicide', 'self_harm', 'violence']:
                    risk_level = SafetyLevel.CRITICAL
                    recommendations.append('Immediate safety assessment required')
                elif category in ['crisis', 'psychosis']:
                    risk_level = max(risk_level, SafetyLevel.HIGH)
                    recommendations.append('Enhanced monitoring needed')
        
        # Context-based risk assessment
        distress_indicators = ['overwhelming', 'can\'t cope', 'unbearable', 'hopeless']
        if any(indicator in message_lower for indicator in distress_indicators):
            risk_level = max(risk_level, SafetyLevel.MEDIUM)
            flags.append('high_distress')
        
        return SafetyScreeningResult(
            risk_level=risk_level,
            flags=flags,
            recommendations=recommendations
        )
    
    def screen_response(self, response: str) -> 'SafetyScreeningResult':
        """Screen AI response for appropriate content"""
        
        response_lower = response.lower()
        flags = []
        recommendations = []
        
        # Check for appropriate crisis response
        if any(word in response_lower for word in ['crisis', 'emergency', 'suicide']):
            if 'safety' not in response_lower or 'help' not in response_lower:
                flags.append('inadequate_crisis_response')
                recommendations.append('Enhance crisis intervention content')
        
        # Check for boundary violations
        inappropriate_phrases = ['personal experience', 'i feel', 'my life', 'i think you should']
        if any(phrase in response_lower for phrase in inappropriate_phrases):
            flags.append('boundary_concern')
            recommendations.append('Review professional boundaries')
        
        return SafetyScreeningResult(
            risk_level=SafetyLevel.LOW,
            flags=flags,
            recommendations=recommendations
        )


@dataclass
class SafetyScreeningResult:
    """Result of safety screening"""
    risk_level: SafetyLevel
    flags: List[str]
    recommendations: List[str]


# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    async def demonstrate_gemini_interface():
        print("=== GEMINI THERAPY INTERFACE DEMONSTRATION ===\n")
        
        # Initialize interface (using simulated responses for demo)
        config = {
            "model_name": "gemini-2.5-pro",
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        # Note: In real usage, you would provide actual API key
        interface = GeminiTherapyInterface(api_key="demo_key", config=config)
        
        # Create conversation context
        context = ConversationContext(
            patient_id="PATIENT_001",
            session_id="SESSION_003", 
            therapy_modality="CBT",
            session_number=3,
            treatment_phase="working",
            current_mood="anxious",
            risk_level="low",
            active_goals=["Manage anxiety", "Improve sleep"],
            recent_assessments={"GAD7": "moderate anxiety"},
            cultural_considerations=["English as second language"]
        )
        
        # Demonstrate different conversation modes
        test_scenarios = [
            {
                "mode": ConversationMode.THERAPY_SESSION,
                "message": "I've been feeling really anxious this week, especially about work. I can't seem to stop worrying about everything.",
                "description": "Regular therapy session"
            },
            {
                "mode": ConversationMode.SKILL_BUILDING,
                "message": "Can you teach me something to help when I get overwhelmed?",
                "description": "Skills training request"
            },
            {
                "mode": ConversationMode.CRISIS_INTERVENTION,
                "message": "I don't think I can handle this anymore. Sometimes I think everyone would be better off without me.",
                "description": "Crisis intervention needed"
            },
            {
                "mode": ConversationMode.ASSESSMENT,
                "message": "You asked about my sleep - it's been pretty bad lately.",
                "description": "Assessment conversation"
            }
        ]
        
        for scenario in test_scenarios:
            print(f"=== {scenario['description'].upper()} ===")
            print(f"User Message: \"{scenario['message']}\"")
            print()
            
            # Generate response
            response = await interface.generate_therapeutic_response(
                context, 
                scenario['message'], 
                scenario['mode']
            )
            
            print("AI Response:")
            print(response.content)
            print()
            print(f"Response Type: {response.response_type.value}")
            print(f"Confidence Score: {response.confidence_score:.2f}")
            print(f"Safety Flags: {response.safety_flags}")
            print(f"Risk Indicators: {response.risk_indicators}")
            print(f"Suggested Interventions: {response.suggested_interventions}")
            print(f"Follow-up Needed: {response.follow_up_needed}")
            print()
            print("-" * 60)
            print()
        
        # Demonstrate session summary
        print("=== SESSION SUMMARY ===")
        summary = interface.generate_session_summary(context)
        print(summary)
        print()
        
        # Demonstrate conversation insights
        print("=== CONVERSATION INSIGHTS ===")
        insights = interface.get_conversation_insights(context)
        print("Session Metrics:")
        for key, value in insights['session_metrics'].items():
            print(f"  {key}: {value}")
        
        print("\nClinical Observations:")
        for obs in insights['clinical_observations']:
            print(f"  • {obs}")
        
        print("\nRecommendations:")
        for rec in insights['recommendations']:
            print(f"  • {rec}")
        
        print("\n" + "="*60)
        
        # Demonstrate safety monitoring
        print("=== SAFETY MONITORING DEMONSTRATION ===")
        safety_monitor = TherapySafetyMonitor()
        
        test_messages = [
            "I'm feeling a bit sad today",
            "I can't take this anymore, I want to end it all",
            "I'm having thoughts about hurting myself",
            "Everything is going well, thanks for asking"
        ]
        
        for message in test_messages:
            result = safety_monitor.screen_message(message)
            print(f"Message: \"{message}\"")
            print(f"Risk Level: {result.risk_level.value}")
            print(f"Flags: {result.flags}")
            print(f"Recommendations: {result.recommendations}")
            print()
        
        print("="*60)
        print("Gemini interface ready for therapeutic conversations!")
        print("Features: Safety monitoring, context awareness, evidence-based responses")
    
    # Run demonstration
    asyncio.run(demonstrate_gemini_interface())
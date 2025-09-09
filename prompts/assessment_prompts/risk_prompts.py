"""
Risk Assessment Prompts Module
Professional risk assessment prompts for AI therapy system
Specialized prompts for evaluating suicide, self-harm, homicide, and other safety risks
"""

from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime
import uuid


class RiskType(Enum):
    """Types of risk assessments"""
    SUICIDE_RISK = "suicide_risk"
    SELF_HARM_RISK = "self_harm_risk"
    HOMICIDE_RISK = "homicide_risk"
    SUBSTANCE_ABUSE_RISK = "substance_abuse_risk"
    VIOLENCE_RISK = "violence_risk"
    CHILD_ABUSE_RISK = "child_abuse_risk"
    ELDER_ABUSE_RISK = "elder_abuse_risk"
    DOMESTIC_VIOLENCE_RISK = "domestic_violence_risk"
    PSYCHOSIS_RISK = "psychosis_risk"
    MANIA_RISK = "mania_risk"
    EATING_DISORDER_RISK = "eating_disorder_risk"
    DISSOCIATION_RISK = "dissociation_risk"


class RiskLevel(Enum):
    """Risk severity levels"""
    MINIMAL = "minimal"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    IMMINENT = "imminent"
    CRITICAL = "critical"


class AssessmentPhase(Enum):
    """Phases of risk assessment"""
    SCREENING = "screening"
    DETAILED_ASSESSMENT = "detailed_assessment"
    SAFETY_PLANNING = "safety_planning"
    INTERVENTION = "intervention"
    MONITORING = "monitoring"
    FOLLOW_UP = "follow_up"


class ProtectiveFactor(Enum):
    """Types of protective factors"""
    SOCIAL_SUPPORT = "social_support"
    RELIGIOUS_BELIEFS = "religious_beliefs"
    FUTURE_GOALS = "future_goals"
    CHILDREN_DEPENDENTS = "children_dependents"
    TREATMENT_ENGAGEMENT = "treatment_engagement"
    COPING_SKILLS = "coping_skills"
    PROBLEM_SOLVING = "problem_solving"
    IMPULSE_CONTROL = "impulse_control"


@dataclass
class RiskPromptTemplate:
    """Template for risk assessment prompts"""
    risk_type: RiskType
    phase: AssessmentPhase
    primary_prompt: str
    follow_up_questions: List[str]
    safety_considerations: List[str]
    immediate_actions: List[str]
    documentation_requirements: List[str]
    legal_considerations: List[str]
    protective_factors_to_assess: List[ProtectiveFactor]
    warning_signs: List[str]
    escalation_triggers: List[str]


@dataclass
class RiskAssessmentContext:
    """Context for risk assessment"""
    patient_id: str
    session_id: str
    current_risk_level: RiskLevel
    previous_risk_history: List[Dict[str, Any]]
    current_stressors: List[str]
    protective_factors: List[str]
    support_system: List[str]
    medication_compliance: bool = True
    substance_use_current: bool = False
    previous_attempts: int = 0
    access_to_means: bool = False


class RiskAssessmentPrompts:
    """Comprehensive risk assessment prompt system"""
    
    def __init__(self):
        self.prompt_templates = self._initialize_risk_prompts()
        self.safety_protocols = self._initialize_safety_protocols()
        self.crisis_interventions = self._initialize_crisis_interventions()
        self.documentation_standards = self._initialize_documentation_standards()
        self.legal_guidelines = self._initialize_legal_guidelines()
    
    def get_risk_assessment_prompt(
        self,
        risk_type: RiskType,
        phase: AssessmentPhase,
        context: RiskAssessmentContext,
        session_info: Dict[str, Any] = None
    ) -> str:
        """Generate contextual risk assessment prompt"""
        
        template = self.prompt_templates.get((risk_type, phase))
        if not template:
            return self._get_generic_risk_prompt(risk_type, phase)
        
        context_info = self._format_risk_context(context, session_info)
        safety_protocol = self.safety_protocols.get(risk_type, [])
        
        prompt = f"""
{template.primary_prompt}

PATIENT CONTEXT:
{context_info}

SAFETY PROTOCOL FOR {risk_type.value.upper()}:
{chr(10).join(f"• {protocol}" for protocol in safety_protocol)}

IMMEDIATE SAFETY CONSIDERATIONS:
{chr(10).join(f"• {consideration}" for consideration in template.safety_considerations)}

PROTECTIVE FACTORS TO ASSESS:
{chr(10).join(f"• {factor.value.replace('_', ' ').title()}" for factor in template.protective_factors_to_assess)}

WARNING SIGNS TO MONITOR:
{chr(10).join(f"• {sign}" for sign in template.warning_signs)}

DOCUMENTATION REQUIREMENTS:
{chr(10).join(f"• {req}" for req in template.documentation_requirements)}

APPROACH:
- Be direct and compassionate in your questioning
- Prioritize immediate safety over therapeutic goals
- Validate the patient's emotional pain while focusing on safety
- Assess both risk factors and protective factors
- Document all responses thoroughly
- Follow up with specific questions based on initial responses

Remember: Safety is the absolute priority. If imminent risk is identified, implement crisis intervention protocols immediately.
"""
        
        return prompt
    
    def _initialize_risk_prompts(self) -> Dict[Tuple[RiskType, AssessmentPhase], RiskPromptTemplate]:
        """Initialize comprehensive risk assessment prompts"""
        
        prompts = {}
        
        # SUICIDE RISK ASSESSMENT
        prompts[(RiskType.SUICIDE_RISK, AssessmentPhase.SCREENING)] = RiskPromptTemplate(
            risk_type=RiskType.SUICIDE_RISK,
            phase=AssessmentPhase.SCREENING,
            primary_prompt="""
You are conducting a suicide risk screening. This is a critical assessment that requires direct, compassionate questioning.

Start with: "I need to ask you some important questions about your safety. Sometimes when people are going through difficult times, they have thoughts of wanting to die or hurt themselves. Have you been having any thoughts like this recently?"

Continue with systematic assessment based on their response, always prioritizing safety.
""",
            follow_up_questions=[
                "How often have you been having these thoughts?",
                "When did these thoughts first start?",
                "How intense are these thoughts on a scale of 1-10?",
                "Have you thought about how you might do this?",
                "Do you have access to [means mentioned]?",
                "What has stopped you from acting on these thoughts?",
                "Have you made any preparations or taken any steps?",
                "Have you told anyone else about these thoughts?",
                "What would need to change for these thoughts to go away?"
            ],
            safety_considerations=[
                "Assess immediacy of risk",
                "Evaluate access to lethal means",
                "Determine level of planning and intent",
                "Assess impulse control",
                "Evaluate protective factors",
                "Consider need for emergency services",
                "Ensure patient is not left alone if high risk"
            ],
            immediate_actions=[
                "Complete safety assessment immediately",
                "Remove or secure lethal means if possible",
                "Contact emergency services if imminent danger",
                "Involve support system with consent",
                "Consider psychiatric hospitalization",
                "Create safety plan",
                "Schedule immediate follow-up"
            ],
            documentation_requirements=[
                "Document all responses verbatim",
                "Record risk level assessment",
                "Note protective factors identified",
                "Document safety plan created",
                "Record all interventions implemented",
                "Note follow-up plans"
            ],
            legal_considerations=[
                "Duty to protect patient safety",
                "Consider involuntary commitment if necessary",
                "Document decision-making process",
                "Consult with supervisor if available",
                "Follow state-specific reporting requirements"
            ],
            protective_factors_to_assess=[
                ProtectiveFactor.SOCIAL_SUPPORT,
                ProtectiveFactor.RELIGIOUS_BELIEFS,
                ProtectiveFactor.FUTURE_GOALS,
                ProtectiveFactor.CHILDREN_DEPENDENTS,
                ProtectiveFactor.TREATMENT_ENGAGEMENT
            ],
            warning_signs=[
                "Expressing hopelessness or worthlessness",
                "Talking about being a burden to others",
                "Withdrawal from family and friends",
                "Giving away possessions",
                "Sudden mood improvement after depression",
                "Increased substance use",
                "Reckless behavior"
            ],
            escalation_triggers=[
                "Loss of significant relationship",
                "Job loss or financial crisis",
                "Legal problems",
                "Serious medical diagnosis",
                "Anniversary dates of losses",
                "Substance use relapse"
            ]
        )
        
        # SELF-HARM RISK ASSESSMENT
        prompts[(RiskType.SELF_HARM_RISK, AssessmentPhase.SCREENING)] = RiskPromptTemplate(
            risk_type=RiskType.SELF_HARM_RISK,
            phase=AssessmentPhase.SCREENING,
            primary_prompt="""
You are assessing for self-harm behaviors. Self-harm is often used as a coping mechanism for emotional distress.

Ask: "Sometimes people cope with difficult emotions by hurting themselves in ways that aren't meant to be lethal, like cutting, burning, or hitting themselves. Have you ever done anything like this to cope with emotional pain?"

Assess the function, frequency, and severity of self-harm behaviors with empathy and without judgment.
""",
            follow_up_questions=[
                "What methods have you used to hurt yourself?",
                "How often do you engage in self-harm?",
                "When did you first start self-harming?",
                "What triggers these behaviors?",
                "How do you feel before, during, and after self-harming?",
                "Have you ever accidentally hurt yourself more than intended?",
                "What other ways have you found to cope with emotional pain?",
                "Have you received medical treatment for self-harm injuries?"
            ],
            safety_considerations=[
                "Assess for medical complications",
                "Evaluate infection risk",
                "Determine if behaviors are escalating",
                "Assess access to self-harm tools",
                "Evaluate suicide risk connection"
            ],
            immediate_actions=[
                "Assess current injuries needing medical attention",
                "Develop alternative coping strategies",
                "Remove or limit access to self-harm tools",
                "Create safety plan for urges",
                "Consider increased supervision",
                "Refer for medical evaluation if needed"
            ],
            documentation_requirements=[
                "Document methods and frequency",
                "Note triggers and functions",
                "Record current injury status",
                "Document safety plan elements",
                "Note alternative coping strategies taught"
            ],
            legal_considerations=[
                "Assess if self-harm indicates suicide risk",
                "Consider need for medical evaluation",
                "Document safety measures implemented"
            ],
            protective_factors_to_assess=[
                ProtectiveFactor.COPING_SKILLS,
                ProtectiveFactor.SOCIAL_SUPPORT,
                ProtectiveFactor.TREATMENT_ENGAGEMENT,
                ProtectiveFactor.IMPULSE_CONTROL
            ],
            warning_signs=[
                "Unexplained injuries or scars",
                "Wearing long sleeves in warm weather",
                "Possession of sharp objects",
                "Isolation and secrecy",
                "Emotional numbing"
            ],
            escalation_triggers=[
                "Increased emotional distress",
                "Relationship conflicts",
                "Academic or work stress",
                "Trauma anniversaries",
                "Feeling invalidated or misunderstood"
            ]
        )
        
        # HOMICIDE/VIOLENCE RISK ASSESSMENT
        prompts[(RiskType.HOMICIDE_RISK, AssessmentPhase.SCREENING)] = RiskPromptTemplate(
            risk_type=RiskType.HOMICIDE_RISK,
            phase=AssessmentPhase.SCREENING,
            primary_prompt="""
You are assessing for risk of violence toward others. This assessment is critical for public safety.

Ask: "When people feel very angry or upset, they sometimes have thoughts about hurting other people. Have you been having any thoughts about hurting someone else?"

Assess for specific targets, plans, and access to weapons. This assessment may trigger duty to warn obligations.
""",
            follow_up_questions=[
                "Who specifically have you thought about hurting?",
                "How would you hurt this person?",
                "Do you have access to weapons or means to harm them?",
                "How often do you have these thoughts?",
                "What triggers these thoughts about violence?",
                "Have you ever acted violently toward others before?",
                "Do you have contact with the person you're thinking of hurting?",
                "What stops you from acting on these thoughts?"
            ],
            safety_considerations=[
                "Assess immediacy of threat",
                "Identify specific intended victims",
                "Evaluate access to weapons",
                "Assess history of violence",
                "Consider duty to warn requirements"
            ],
            immediate_actions=[
                "Contact law enforcement if imminent threat",
                "Warn intended victims if legally required",
                "Consider psychiatric hospitalization",
                "Remove access to weapons",
                "Implement safety planning",
                "Consult with legal counsel"
            ],
            documentation_requirements=[
                "Document specific threats made",
                "Record intended victims identified",
                "Note access to weapons or means",
                "Document all safety measures taken",
                "Record consultations made"
            ],
            legal_considerations=[
                "Duty to warn intended victims",
                "Duty to protect public safety",
                "Tarasoff obligations",
                "Mandatory reporting requirements",
                "Documentation for legal proceedings"
            ],
            protective_factors_to_assess=[
                ProtectiveFactor.IMPULSE_CONTROL,
                ProtectiveFactor.SOCIAL_SUPPORT,
                ProtectiveFactor.TREATMENT_ENGAGEMENT,
                ProtectiveFactor.PROBLEM_SOLVING
            ],
            warning_signs=[
                "Specific threats against individuals",
                "Obsession with violent themes",
                "Acquisition of weapons",
                "Stalking behaviors",
                "History of violence"
            ],
            escalation_triggers=[
                "Relationship breakups",
                "Workplace conflicts",
                "Legal disputes",
                "Perceived humiliation",
                "Substance use"
            ]
        )
        
        # SUBSTANCE ABUSE RISK ASSESSMENT
        prompts[(RiskType.SUBSTANCE_ABUSE_RISK, AssessmentPhase.SCREENING)] = RiskPromptTemplate(
            risk_type=RiskType.SUBSTANCE_ABUSE_RISK,
            phase=AssessmentPhase.SCREENING,
            primary_prompt="""
You are assessing for substance abuse risk. Approach this sensitively and non-judgmentally.

Ask: "I'd like to ask about your use of alcohol and other substances. This information helps me understand your situation better and provide the best care. Can you tell me about your current use of alcohol, prescription medications, or any other substances?"

Focus on understanding patterns, consequences, and safety risks.
""",
            follow_up_questions=[
                "What substances do you currently use?",
                "How often do you use each substance?",
                "How much do you typically use?",
                "When did you last use?",
                "Have you noticed your tolerance increasing?",
                "Have you experienced withdrawal symptoms?",
                "How does substance use affect your daily life?",
                "Have you tried to cut down or stop using?",
                "Have you driven under the influence?",
                "Have others expressed concern about your use?"
            ],
            safety_considerations=[
                "Assess for withdrawal risks",
                "Evaluate overdose potential",
                "Check for dangerous combinations",
                "Assess driving safety",
                "Evaluate medication interactions"
            ],
            immediate_actions=[
                "Assess need for medical detox",
                "Check for withdrawal symptoms",
                "Review medication interactions",
                "Provide overdose prevention education",
                "Discuss harm reduction strategies",
                "Consider addiction treatment referral"
            ],
            documentation_requirements=[
                "Document substances used and amounts",
                "Record frequency and patterns",
                "Note consequences experienced",
                "Document withdrawal symptoms",
                "Record safety education provided"
            ],
            legal_considerations=[
                "Confidentiality protections",
                "Exceptions for imminent danger",
                "Reporting requirements for certain situations",
                "Documentation standards"
            ],
            protective_factors_to_assess=[
                ProtectiveFactor.SOCIAL_SUPPORT,
                ProtectiveFactor.TREATMENT_ENGAGEMENT,
                ProtectiveFactor.COPING_SKILLS,
                ProtectiveFactor.FUTURE_GOALS
            ],
            warning_signs=[
                "Increasing tolerance",
                "Withdrawal symptoms",
                "Neglecting responsibilities",
                "Relationship problems due to use",
                "Legal problems"
            ],
            escalation_triggers=[
                "Increased stress",
                "Relationship conflicts",
                "Financial problems",
                "Mental health symptoms",
                "Peer pressure"
            ]
        )
        
        # PSYCHOSIS RISK ASSESSMENT
        prompts[(RiskType.PSYCHOSIS_RISK, AssessmentPhase.SCREENING)] = RiskPromptTemplate(
            risk_type=RiskType.PSYCHOSIS_RISK,
            phase=AssessmentPhase.SCREENING,
            primary_prompt="""
You are assessing for psychotic symptoms and associated risks. Approach with sensitivity and avoid confirming or challenging delusions directly.

Ask: "Sometimes when people are under stress, they may have unusual experiences like hearing voices or seeing things others don't see, or having thoughts that others find hard to understand. Have you had any experiences like this?"

Focus on understanding the content and impact of psychotic symptoms on safety and functioning.
""",
            follow_up_questions=[
                "Can you describe these experiences for me?",
                "How often do these experiences occur?",
                "Do you hear voices talking to you or about you?",
                "What do the voices say?",
                "Do the voices tell you to do things?",
                "Do you see things that others don't see?",
                "Do you have beliefs that others find unusual?",
                "How do these experiences affect your daily life?",
                "Are you taking any medication for these experiences?"
            ],
            safety_considerations=[
                "Assess for command hallucinations",
                "Evaluate potential for violence",
                "Check reality testing ability",
                "Assess insight and judgment",
                "Evaluate medication compliance"
            ],
            immediate_actions=[
                "Assess command hallucination content",
                "Evaluate need for psychiatric evaluation",
                "Consider medication review",
                "Implement reality testing supports",
                "Ensure safe environment",
                "Consider hospitalization if severe"
            ],
            documentation_requirements=[
                "Document specific symptoms reported",
                "Record content of hallucinations/delusions",
                "Note level of insight",
                "Document safety assessment",
                "Record interventions provided"
            ],
            legal_considerations=[
                "Assess capacity for decision-making",
                "Consider need for psychiatric hold",
                "Evaluate competency issues",
                "Document safety measures"
            ],
            protective_factors_to_assess=[
                ProtectiveFactor.TREATMENT_ENGAGEMENT,
                ProtectiveFactor.SOCIAL_SUPPORT,
                ProtectiveFactor.COPING_SKILLS,
                ProtectiveFactor.IMPULSE_CONTROL
            ],
            warning_signs=[
                "Command hallucinations",
                "Paranoid delusions",
                "Disorganized thinking",
                "Bizarre behavior",
                "Poor insight"
            ],
            escalation_triggers=[
                "Medication non-compliance",
                "Increased stress",
                "Substance use",
                "Sleep deprivation",
                "Social isolation"
            ]
        )
        
        return prompts
    
    def _initialize_safety_protocols(self) -> Dict[RiskType, List[str]]:
        """Initialize safety protocols for each risk type"""
        
        return {
            RiskType.SUICIDE_RISK: [
                "Assess immediacy of risk using direct questions",
                "Evaluate access to lethal means",
                "Assess protective factors and social support",
                "Create detailed safety plan with patient",
                "Consider need for psychiatric hospitalization",
                "Involve support system with patient consent",
                "Schedule immediate follow-up contact",
                "Document all risk factors and protective factors",
                "Provide crisis contact numbers",
                "Consider 24/7 supervision if high risk"
            ],
            RiskType.HOMICIDE_RISK: [
                "Assess specific threats and intended victims",
                "Evaluate access to weapons or means",
                "Consider duty to warn obligations",
                "Contact law enforcement if imminent danger",
                "Consult with supervisor or legal counsel",
                "Document all threats and safety measures",
                "Consider psychiatric hospitalization",
                "Implement safety planning",
                "Remove access to weapons if possible",
                "Monitor patient closely"
            ],
            RiskType.SELF_HARM_RISK: [
                "Assess severity and medical risks",
                "Evaluate need for medical treatment",
                "Remove or limit access to self-harm tools",
                "Develop alternative coping strategies",
                "Create safety plan for urges",
                "Provide crisis intervention skills",
                "Consider increased supervision",
                "Schedule frequent check-ins",
                "Involve support system",
                "Monitor for escalation to suicide risk"
            ],
            RiskType.SUBSTANCE_ABUSE_RISK: [
                "Assess for withdrawal risks",
                "Evaluate need for medical detox",
                "Check for dangerous drug interactions",
                "Provide overdose prevention education",
                "Discuss harm reduction strategies",
                "Consider addiction treatment referral",
                "Monitor for safety risks",
                "Assess driving safety",
                "Involve support system if appropriate",
                "Schedule regular monitoring"
            ],
            RiskType.PSYCHOSIS_RISK: [
                "Assess command hallucination content",
                "Evaluate reality testing and insight",
                "Consider psychiatric evaluation",
                "Review medication compliance",
                "Ensure safe environment",
                "Monitor for agitation or unpredictability",
                "Assess decision-making capacity",
                "Consider hospitalization if severe",
                "Provide reality testing supports",
                "Involve mental health team"
            ]
        }
    
    def _initialize_crisis_interventions(self) -> Dict[RiskLevel, List[str]]:
        """Initialize crisis intervention protocols by risk level"""
        
        return {
            RiskLevel.MINIMAL: [
                "Continue routine monitoring",
                "Provide psychoeducation about warning signs",
                "Reinforce existing coping strategies",
                "Schedule regular follow-up",
                "Document baseline risk level"
            ],
            RiskLevel.LOW: [
                "Increase monitoring frequency",
                "Develop basic safety plan",
                "Strengthen coping strategies",
                "Involve support system",
                "Provide crisis contact information"
            ],
            RiskLevel.MODERATE: [
                "Create detailed safety plan",
                "Remove or secure means of harm",
                "Increase contact frequency",
                "Consider family involvement",
                "Provide intensive coping skills training",
                "Consider medication evaluation"
            ],
            RiskLevel.HIGH: [
                "Implement intensive safety measures",
                "Consider psychiatric hospitalization",
                "Remove all means of harm",
                "Arrange 24/7 supervision",
                "Contact emergency services if needed",
                "Involve psychiatrist immediately"
            ],
            RiskLevel.IMMINENT: [
                "Activate emergency protocols",
                "Contact emergency services immediately",
                "Do not leave patient alone",
                "Arrange immediate psychiatric evaluation",
                "Consider involuntary commitment",
                "Notify all relevant parties"
            ],
            RiskLevel.CRITICAL: [
                "Emergency services activation required",
                "Immediate hospitalization necessary",
                "Law enforcement involvement if needed",
                "Complete environmental safety measures",
                "Continuous supervision required",
                "Emergency psychiatric consultation"
            ]
        }
    
    def _initialize_documentation_standards(self) -> Dict[str, List[str]]:
        """Initialize documentation standards for risk assessments"""
        
        return {
            "assessment_documentation": [
                "Record all questions asked and responses given",
                "Document direct quotes when significant",
                "Note behavioral observations during assessment",
                "Record risk level determined and rationale",
                "Document all safety measures implemented",
                "Note protective factors identified"
            ],
            "safety_planning_documentation": [
                "Document safety plan components",
                "Record patient's commitment to safety",
                "Note support persons involved",
                "Document means restriction measures",
                "Record crisis contact information provided",
                "Note follow-up plans established"
            ],
            "intervention_documentation": [
                "Record all interventions implemented",
                "Document patient response to interventions",
                "Note any resistance or cooperation",
                "Record consultation with other professionals",
                "Document decision-making rationale",
                "Note outcomes of interventions"
            ]
        }
    
    def _initialize_legal_guidelines(self) -> Dict[str, List[str]]:
        """Initialize legal guidelines for risk assessment"""
        
        return {
            "duty_to_warn": [
                "Assess specificity of threat",
                "Identify intended victims",
                "Consider imminence of danger",
                "Consult with legal counsel if available",
                "Document decision-making process",
                "Follow state-specific requirements"
            ],
            "involuntary_commitment": [
                "Assess criteria for commitment",
                "Document danger to self or others",
                "Consider patient's decision-making capacity",
                "Follow legal procedures for jurisdiction",
                "Involve appropriate professionals",
                "Document all evidence supporting decision"
            ],
            "confidentiality_exceptions": [
                "Identify applicable exceptions",
                "Document rationale for disclosure",
                "Limit disclosure to necessary information",
                "Notify patient when possible",
                "Follow ethical guidelines",
                "Maintain detailed records"
            ]
        }
    
    def _format_risk_context(self, context: RiskAssessmentContext, session_info: Dict[str, Any] = None) -> str:
        """Format risk assessment context information"""
        
        context_lines = [
            f"Patient ID: {context.patient_id}",
            f"Current Risk Level: {context.current_risk_level.value}",
            f"Previous Attempts: {context.previous_attempts}",
            f"Access to Means: {'Yes' if context.access_to_means else 'No'}",
            f"Substance Use Current: {'Yes' if context.substance_use_current else 'No'}",
            f"Medication Compliant: {'Yes' if context.medication_compliance else 'No'}"
        ]
        
        if context.current_stressors:
            context_lines.append(f"Current Stressors: {', '.join(context.current_stressors)}")
        
        if context.protective_factors:
            context_lines.append(f"Protective Factors: {', '.join(context.protective_factors)}")
        
        if context.support_system:
            context_lines.append(f"Support System: {', '.join(context.support_system)}")
        
        return chr(10).join(context_lines)
    
    def _get_generic_risk_prompt(self, risk_type: RiskType, phase: AssessmentPhase) -> str:
        """Generate generic risk assessment prompt when specific template not found"""
        
        return f"""
You are conducting a {risk_type.value.replace('_', ' ')} assessment in the {phase.value.replace('_', ' ')} phase.

GENERAL APPROACH:
- Be direct but compassionate in your questioning
- Prioritize safety over all other considerations
- Use open-ended questions followed by specific follow-ups
- Assess both risk factors and protective factors
- Document all responses thoroughly
- Implement appropriate safety measures based on risk level

SAFETY PRIORITY:
The patient's immediate safety is the top priority. If you identify any imminent risk, implement crisis intervention protocols immediately.

Continue with systematic assessment appropriate for {risk_type.value.replace('_', ' ')}.
"""
    
    def get_safety_plan_prompt(self, risk_type: RiskType, risk_level: RiskLevel) -> str:
        """Generate safety planning prompt based on risk type and level"""
        
        base_prompt = f"""
You are now creating a safety plan for {risk_type.value.replace('_', ' ')} at {risk_level.value} risk level.

SAFETY PLAN COMPONENTS:
1. Warning signs recognition
2. Internal coping strategies
3. Social contacts for support
4. Professional contacts for crisis
5. Environmental safety measures
6. Reasons for living/protective factors

APPROACH:
- Collaborate with the patient in creating the plan
- Make it specific and actionable
- Include multiple levels of intervention
- Ensure patient understands and commits to the plan
- Provide written copy of the plan
- Schedule follow-up to review effectiveness

"""
        
        crisis_interventions = self.crisis_interventions.get(risk_level, [])
        if crisis_interventions:
            base_prompt += f"""
CRISIS INTERVENTION LEVEL FOR {risk_level.value.upper()} RISK:
{chr(10).join(f"• {intervention}" for intervention in crisis_interventions)}
"""
        
        return base_prompt
    
    def get_follow_up_risk_prompt(self, previous_assessment: Dict[str, Any]) -> str:
        """Generate follow-up risk assessment prompt"""
        
        return f"""
You are conducting a follow-up risk assessment.

PREVIOUS ASSESSMENT SUMMARY:
- Previous Risk Level: {previous_assessment.get('risk_level', 'Unknown')}
- Date of Last Assessment: {previous_assessment.get('assessment_date', 'Unknown')}
- Safety Plan Status: {previous_assessment.get('safety_plan_status', 'Unknown')}
- Protective Factors: {', '.join(previous_assessment.get('protective_factors', []))}

FOLLOW-UP FOCUS:
1. Changes in risk level since last assessment
2. Effectiveness of safety plan implementation
3. New stressors or protective factors
4. Compliance with treatment recommendations
5. Support system changes
6. Any new incidents or concerns

Ask: "Since our last meeting, how have you been doing with the safety plan we created? Have there been any changes in your thoughts about harming yourself or others?"

Continue with systematic reassessment based on previous findings and current presentation.
"""
    
    def generate_risk_assessment_summary(
        self,
        assessments: List[Dict[str, Any]],
        current_risk_level: RiskLevel,
        recommendations: List[str]
    ) -> str:
        """Generate comprehensive risk assessment summary"""
        
        summary = f"""
RISK ASSESSMENT SUMMARY
========================

CURRENT RISK LEVEL: {current_risk_level.value.upper()}
Assessment Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

RISK FACTORS IDENTIFIED:
"""
        
        risk_factors = []
        protective_factors = []
        
        for assessment in assessments:
            if assessment.get('risk_factors'):
                risk_factors.extend(assessment['risk_factors'])
            if assessment.get('protective_factors'):
                protective_factors.extend(assessment['protective_factors'])
        
        # Remove duplicates while preserving order
        risk_factors = list(dict.fromkeys(risk_factors))
        protective_factors = list(dict.fromkeys(protective_factors))
        
        for factor in risk_factors:
            summary += f"• {factor}\n"
        
        summary += f"""
PROTECTIVE FACTORS IDENTIFIED:
"""
        for factor in protective_factors:
            summary += f"• {factor}\n"
        
        summary += f"""
SAFETY INTERVENTIONS IMPLEMENTED:
"""
        for rec in recommendations:
            summary += f"• {rec}\n"
        
        summary += f"""
FOLLOW-UP REQUIREMENTS:
• Risk reassessment within [timeframe based on risk level]
• Safety plan review and updates as needed
• Coordination with treatment team
• Emergency contact protocols established

DOCUMENTATION COMPLETED:
• Detailed risk assessment recorded
• Safety plan created and reviewed with patient
• Crisis intervention protocols established
• Treatment team notifications made
"""
        
        return summary


class RiskAssessmentValidator:
    """Validates risk assessment responses and ensures safety protocols"""
    
    def __init__(self):
        self.critical_keywords = self._initialize_critical_keywords()
        self.validation_rules = self._initialize_validation_rules()
    
    def _initialize_critical_keywords(self) -> Dict[RiskType, List[str]]:
        """Initialize keywords that trigger immediate safety concerns"""
        
        return {
            RiskType.SUICIDE_RISK: [
                "kill myself", "end my life", "suicide", "want to die",
                "better off dead", "no point living", "can't go on",
                "have a plan", "tonight", "today", "pills", "gun",
                "rope", "bridge", "overdose"
            ],
            RiskType.HOMICIDE_RISK: [
                "kill them", "hurt someone", "get revenge", "make them pay",
                "gun", "knife", "weapon", "tonight", "going to do it",
                "they deserve to die", "eliminate them"
            ],
            RiskType.SELF_HARM_RISK: [
                "cut myself", "burn myself", "hit myself", "punish myself",
                "deserve pain", "razor", "blade", "cutting",
                "burning", "hitting walls"
            ],
            RiskType.VIOLENCE_RISK: [
                "hurt someone", "get violent", "lose control", "anger management",
                "want to fight", "make them suffer", "physical violence"
            ]
        }
    
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize validation rules for risk assessment responses"""
        
        return {
            "immediate_danger_phrases": [
                "right now", "tonight", "today", "this morning",
                "after this session", "when I leave here",
                "have the means", "already planned"
            ],
            "high_risk_indicators": [
                "detailed plan", "access to means", "no hope",
                "no one cares", "better off without me",
                "settled affairs", "said goodbye"
            ],
            "protective_factor_indicators": [
                "family needs me", "religious beliefs", "future goals",
                "love my children", "want to get better",
                "hope things improve", "support system"
            ]
        }
    
    def validate_response(self, response: str, risk_type: RiskType) -> Dict[str, Any]:
        """Validate risk assessment response and determine urgency"""
        
        validation_result = {
            "immediate_danger": False,
            "high_risk": False,
            "critical_keywords_found": [],
            "protective_factors_mentioned": [],
            "recommended_actions": [],
            "urgency_level": "routine"
        }
        
        response_lower = response.lower()
        
        # Check for critical keywords
        critical_words = self.critical_keywords.get(risk_type, [])
        found_critical = [word for word in critical_words if word in response_lower]
        validation_result["critical_keywords_found"] = found_critical
        
        # Check for immediate danger indicators
        immediate_phrases = self.validation_rules["immediate_danger_phrases"]
        if any(phrase in response_lower for phrase in immediate_phrases):
            validation_result["immediate_danger"] = True
            validation_result["urgency_level"] = "emergency"
            validation_result["recommended_actions"].extend([
                "Activate emergency protocols immediately",
                "Do not leave patient alone",
                "Contact emergency services if necessary",
                "Implement crisis intervention"
            ])
        
        # Check for high risk indicators
        high_risk_phrases = self.validation_rules["high_risk_indicators"]
        if any(phrase in response_lower for phrase in high_risk_phrases):
            validation_result["high_risk"] = True
            validation_result["urgency_level"] = "urgent"
            validation_result["recommended_actions"].extend([
                "Conduct detailed safety assessment",
                "Create comprehensive safety plan",
                "Consider higher level of care",
                "Increase monitoring frequency"
            ])
        
        # Check for protective factors
        protective_phrases = self.validation_rules["protective_factor_indicators"]
        found_protective = [phrase for phrase in protective_phrases if phrase in response_lower]
        validation_result["protective_factors_mentioned"] = found_protective
        
        return validation_result


class SafetyPlanGenerator:
    """Generates comprehensive safety plans based on risk assessment"""
    
    def __init__(self):
        self.safety_plan_templates = self._initialize_safety_plan_templates()
        self.coping_strategies = self._initialize_coping_strategies()
    
    def _initialize_safety_plan_templates(self) -> Dict[RiskType, Dict[str, Any]]:
        """Initialize safety plan templates for different risk types"""
        
        return {
            RiskType.SUICIDE_RISK: {
                "warning_signs": [
                    "Feeling hopeless or worthless",
                    "Thinking 'I would be better off dead'",
                    "Feeling like a burden to others",
                    "Withdrawing from family and friends",
                    "Increasing alcohol or drug use",
                    "Giving away possessions"
                ],
                "internal_coping": [
                    "Deep breathing exercises",
                    "Progressive muscle relaxation",
                    "Mindfulness meditation",
                    "Listening to calming music",
                    "Taking a warm bath or shower",
                    "Writing in a journal"
                ],
                "social_contacts": [
                    "Family member: [Name and phone]",
                    "Close friend: [Name and phone]",
                    "Supportive colleague: [Name and phone]",
                    "Spiritual advisor: [Name and phone]"
                ],
                "professional_contacts": [
                    "Therapist: [Name and phone]",
                    "Crisis hotline: 988 (Suicide & Crisis Lifeline)",
                    "Emergency services: 911",
                    "Hospital emergency room: [Local ER]"
                ],
                "environmental_safety": [
                    "Remove or secure firearms",
                    "Remove or secure medications",
                    "Remove or secure sharp objects",
                    "Have someone stay with you",
                    "Go to a safe location"
                ]
            },
            RiskType.SELF_HARM_RISK: {
                "warning_signs": [
                    "Feeling overwhelmed by emotions",
                    "Urge to hurt myself",
                    "Feeling numb or empty",
                    "Anger or frustration building up",
                    "Feeling like I deserve pain"
                ],
                "internal_coping": [
                    "Hold ice cubes in hands",
                    "Draw on skin with red marker",
                    "Intense exercise",
                    "Punch a pillow",
                    "Scream into a pillow",
                    "Listen to loud music"
                ],
                "environmental_safety": [
                    "Remove sharp objects",
                    "Give cutting tools to trusted person",
                    "Stay in common areas of home",
                    "Keep hands busy with activities"
                ]
            },
            RiskType.VIOLENCE_RISK: {
                "warning_signs": [
                    "Feeling extremely angry",
                    "Thoughts of hurting someone",
                    "Feeling out of control",
                    "Wanting revenge",
                    "Feeling threatened"
                ],
                "internal_coping": [
                    "Count to ten slowly",
                    "Leave the situation",
                    "Do intense exercise",
                    "Call a timeout",
                    "Practice deep breathing"
                ],
                "environmental_safety": [
                    "Remove weapons from environment",
                    "Avoid the person you're angry with",
                    "Go to a public place",
                    "Ask someone to intervene"
                ]
            }
        }
    
    def _initialize_coping_strategies(self) -> Dict[str, List[str]]:
        """Initialize coping strategies by category"""
        
        return {
            "immediate_distraction": [
                "Count backwards from 100 by 7s",
                "Name 5 things you can see, 4 you can hear, 3 you can touch",
                "Hold ice cubes",
                "Take a cold shower",
                "Do jumping jacks",
                "Call someone immediately"
            ],
            "emotional_regulation": [
                "Practice box breathing (4-4-4-4)",
                "Progressive muscle relaxation",
                "Mindfulness meditation",
                "Emotional labeling and rating",
                "Self-compassion exercises",
                "Grounding techniques"
            ],
            "cognitive_strategies": [
                "Challenge negative thoughts",
                "Use positive self-talk",
                "Focus on reasons for living",
                "Remind yourself this feeling will pass",
                "Think of future goals",
                "Use coping statements"
            ],
            "behavioral_activation": [
                "Go for a walk",
                "Listen to music",
                "Take a shower",
                "Do a creative activity",
                "Exercise",
                "Engage in a hobby"
            ]
        }
    
    def generate_personalized_safety_plan(
        self,
        risk_type: RiskType,
        patient_context: RiskAssessmentContext,
        specific_triggers: List[str],
        available_supports: List[str],
        preferred_coping: List[str]
    ) -> str:
        """Generate personalized safety plan"""
        
        template = self.safety_plan_templates.get(risk_type)
        if not template:
            return self._generate_generic_safety_plan(risk_type)
        
        safety_plan = f"""
PERSONALIZED SAFETY PLAN
========================
Patient: {patient_context.patient_id}
Risk Type: {risk_type.value.replace('_', ' ').title()}
Date Created: {datetime.now().strftime('%Y-%m-%d')}

STEP 1: WARNING SIGNS
Recognize when I might be at risk:
"""
        
        # Add personalized warning signs
        for sign in template.get("warning_signs", []):
            safety_plan += f"□ {sign}\n"
        
        # Add specific triggers
        if specific_triggers:
            safety_plan += "\nPersonal Triggers:\n"
            for trigger in specific_triggers:
                safety_plan += f"□ {trigger}\n"
        
        safety_plan += f"""
STEP 2: INTERNAL COPING STRATEGIES
Things I can do on my own to feel better:
"""
        
        # Add internal coping strategies
        for strategy in template.get("internal_coping", []):
            safety_plan += f"□ {strategy}\n"
        
        # Add preferred coping strategies
        if preferred_coping:
            safety_plan += "\nMy Preferred Strategies:\n"
            for strategy in preferred_coping:
                safety_plan += f"□ {strategy}\n"
        
        safety_plan += f"""
STEP 3: PEOPLE I CAN CONTACT FOR SUPPORT
Social contacts who can help distract me and offer support:
"""
        
        # Add social contacts
        if available_supports:
            for support in available_supports:
                safety_plan += f"□ {support}\n"
        else:
            for contact in template.get("social_contacts", []):
                safety_plan += f"□ {contact}\n"
        
        safety_plan += f"""
STEP 4: PROFESSIONAL CONTACTS
Mental health professionals and crisis services:
"""
        
        for contact in template.get("professional_contacts", []):
            safety_plan += f"□ {contact}\n"
        
        safety_plan += f"""
STEP 5: MAKING THE ENVIRONMENT SAFE
Steps to reduce access to means of harm:
"""
        
        for step in template.get("environmental_safety", []):
            safety_plan += f"□ {step}\n"
        
        safety_plan += f"""
STEP 6: REASONS FOR LIVING
Things that are important to me and worth living for:
"""
        
        # Add protective factors
        for factor in patient_context.protective_factors:
            safety_plan += f"□ {factor}\n"
        
        safety_plan += f"""
EMERGENCY CONTACTS:
□ National Suicide Prevention Lifeline: 988
□ Crisis Text Line: Text HOME to 741741
□ Emergency Services: 911
□ Local Emergency Room: [To be filled in]

COMMITMENT STATEMENT:
I commit to using this safety plan when I am having thoughts of harming myself or others. I understand that these feelings will pass and that I have people who care about me and want to help.

Signature: _________________________ Date: _____________

Review Date: _____________
"""
        
        return safety_plan
    
    def _generate_generic_safety_plan(self, risk_type: RiskType) -> str:
        """Generate generic safety plan when specific template not available"""
        
        return f"""
GENERIC SAFETY PLAN
==================
Risk Type: {risk_type.value.replace('_', ' ').title()}

This is a basic safety plan template. Please customize based on individual assessment.

STEP 1: Recognize warning signs
STEP 2: Use internal coping strategies  
STEP 3: Contact social supports
STEP 4: Contact professionals
STEP 5: Make environment safe
STEP 6: Remember reasons for living

Emergency contacts:
- 988 (Suicide & Crisis Lifeline)
- 911 (Emergency Services)
- Crisis Text Line: Text HOME to 741741
"""


class RiskAssessmentWorkflow:
    """Manages the complete risk assessment workflow"""
    
    def __init__(self):
        self.prompts = RiskAssessmentPrompts()
        self.validator = RiskAssessmentValidator()
        self.safety_planner = SafetyPlanGenerator()
        self.workflow_states = self._initialize_workflow_states()
    
    def _initialize_workflow_states(self) -> Dict[str, List[str]]:
        """Initialize workflow states for risk assessment"""
        
        return {
            "initial_screening": [
                "Present initial risk screening questions",
                "Assess immediate safety",
                "Determine need for detailed assessment"
            ],
            "detailed_assessment": [
                "Conduct comprehensive risk evaluation",
                "Assess all relevant risk factors",
                "Evaluate protective factors",
                "Determine risk level"
            ],
            "safety_planning": [
                "Create personalized safety plan",
                "Review plan with patient",
                "Ensure patient understanding and commitment",
                "Provide emergency contacts"
            ],
            "intervention": [
                "Implement appropriate interventions",
                "Contact support systems",
                "Arrange follow-up care",
                "Document all actions"
            ],
            "monitoring": [
                "Schedule follow-up assessments",
                "Monitor safety plan effectiveness",
                "Adjust interventions as needed",
                "Track risk level changes"
            ]
        }
    
    def execute_risk_assessment_workflow(
        self,
        risk_type: RiskType,
        patient_context: RiskAssessmentContext,
        session_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute complete risk assessment workflow"""
        
        workflow_result = {
            "workflow_id": str(uuid.uuid4()),
            "risk_type": risk_type.value,
            "start_time": datetime.now(),
            "phases_completed": [],
            "current_risk_level": RiskLevel.MINIMAL,
            "safety_plan_created": False,
            "follow_up_required": False,
            "emergency_action_taken": False,
            "documentation": []
        }
        
        try:
            # Phase 1: Initial Screening
            screening_prompt = self.prompts.get_risk_assessment_prompt(
                risk_type, AssessmentPhase.SCREENING, patient_context, session_info
            )
            workflow_result["phases_completed"].append("initial_screening")
            workflow_result["documentation"].append({
                "phase": "screening",
                "prompt_used": screening_prompt,
                "timestamp": datetime.now()
            })
            
            # Phase 2: Risk Level Determination (would be based on responses)
            # This would be implemented with actual response processing
            current_risk = self._determine_risk_level(patient_context)
            workflow_result["current_risk_level"] = current_risk
            
            # Phase 3: Safety Planning
            if current_risk in [RiskLevel.MODERATE, RiskLevel.HIGH, RiskLevel.IMMINENT]:
                safety_plan_prompt = self.prompts.get_safety_plan_prompt(risk_type, current_risk)
                workflow_result["safety_plan_created"] = True
                workflow_result["phases_completed"].append("safety_planning")
                workflow_result["documentation"].append({
                    "phase": "safety_planning",
                    "prompt_used": safety_plan_prompt,
                    "timestamp": datetime.now()
                })
            
            # Phase 4: Crisis Intervention (if needed)
            if current_risk in [RiskLevel.IMMINENT, RiskLevel.CRITICAL]:
                crisis_prompt = self.prompts.get_crisis_intervention_prompt(risk_type.value)
                workflow_result["emergency_action_taken"] = True
                workflow_result["phases_completed"].append("crisis_intervention")
                workflow_result["documentation"].append({
                    "phase": "crisis_intervention",
                    "prompt_used": crisis_prompt,
                    "timestamp": datetime.now()
                })
            
            # Phase 5: Follow-up Planning
            workflow_result["follow_up_required"] = True
            workflow_result["phases_completed"].append("follow_up_planning")
            
            workflow_result["end_time"] = datetime.now()
            workflow_result["status"] = "completed"
            
        except Exception as e:
            workflow_result["status"] = "error"
            workflow_result["error_message"] = str(e)
            workflow_result["end_time"] = datetime.now()
        
        return workflow_result
    
    def _determine_risk_level(self, context: RiskAssessmentContext) -> RiskLevel:
        """Determine risk level based on context (simplified logic)"""
        
        # This would be more sophisticated in a real implementation
        if context.access_to_means and context.previous_attempts > 0:
            return RiskLevel.HIGH
        elif context.current_risk_level == RiskLevel.MODERATE:
            return RiskLevel.MODERATE
        elif context.substance_use_current:
            return RiskLevel.MODERATE
        else:
            return RiskLevel.LOW


# Example usage and testing functions
def example_usage():
    """Example of how to use the risk assessment prompt system"""
    
    # Initialize the risk assessment system
    risk_system = RiskAssessmentPrompts()
    
    # Create patient context
    context = RiskAssessmentContext(
        patient_id="PATIENT_001",
        session_id="SESSION_001",
        current_risk_level=RiskLevel.MODERATE,
        previous_risk_history=[],
        current_stressors=["job loss", "relationship problems"],
        protective_factors=["strong family support", "religious beliefs"],
        support_system=["spouse", "sister", "pastor"],
        previous_attempts=0,
        access_to_means=False
    )
    
    # Get suicide risk screening prompt
    suicide_prompt = risk_system.get_risk_assessment_prompt(
        RiskType.SUICIDE_RISK,
        AssessmentPhase.SCREENING,
        context
    )
    
    print("SUICIDE RISK SCREENING PROMPT:")
    print("=" * 50)
    print(suicide_prompt)
    print("\n")
    
    # Get safety planning prompt
    safety_prompt = risk_system.get_safety_plan_prompt(
        RiskType.SUICIDE_RISK,
        RiskLevel.MODERATE
    )
    
    print("SAFETY PLANNING PROMPT:")
    print("=" * 50)
    print(safety_prompt)
    print("\n")
    
    # Generate safety plan
    safety_planner = SafetyPlanGenerator()
    personalized_plan = safety_planner.generate_personalized_safety_plan(
        RiskType.SUICIDE_RISK,
        context,
        specific_triggers=["feeling overwhelmed at work", "arguments with spouse"],
        available_supports=["John (spouse): 555-1234", "Sarah (sister): 555-5678"],
        preferred_coping=["listening to music", "taking walks", "prayer"]
    )
    
    print("PERSONALIZED SAFETY PLAN:")
    print("=" * 50)
    print(personalized_plan)


if __name__ == "__main__":
    example_usage()
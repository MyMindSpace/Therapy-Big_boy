from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json


class DiagnosticCategory(Enum):
    MOOD_DISORDERS = "mood_disorders"
    ANXIETY_DISORDERS = "anxiety_disorders" 
    TRAUMA_DISORDERS = "trauma_disorders"
    PSYCHOTIC_DISORDERS = "psychotic_disorders"
    PERSONALITY_DISORDERS = "personality_disorders"
    SUBSTANCE_DISORDERS = "substance_disorders"
    EATING_DISORDERS = "eating_disorders"
    SLEEP_DISORDERS = "sleep_disorders"
    ADHD_DISORDERS = "adhd_disorders"
    DEVELOPMENTAL_DISORDERS = "developmental_disorders"


class InterviewPhase(Enum):
    OPENING = "opening"
    SYMPTOM_EXPLORATION = "symptom_exploration"
    HISTORY_GATHERING = "history_gathering"
    FUNCTIONAL_ASSESSMENT = "functional_assessment"
    RISK_ASSESSMENT = "risk_assessment"
    DIFFERENTIAL_DIAGNOSIS = "differential_diagnosis"
    TREATMENT_PLANNING = "treatment_planning"
    CLOSING = "closing"


@dataclass
class DiagnosticPromptTemplate:
    category: DiagnosticCategory
    phase: InterviewPhase
    primary_prompt: str
    follow_up_prompts: List[str]
    clinical_guidelines: List[str]
    safety_considerations: List[str]
    dsm5_criteria_focus: List[str]
    differential_considerations: List[str]


class DiagnosticPromptsSystem:
    
    def __init__(self):
        self.prompt_templates = self._initialize_diagnostic_prompts()
        self.safety_protocols = self._initialize_safety_protocols()
        self.clinical_guidelines = self._initialize_clinical_guidelines()
    
    def get_diagnostic_prompt(
        self,
        category: DiagnosticCategory,
        phase: InterviewPhase,
        patient_context: Dict[str, Any] = None,
        session_info: Dict[str, Any] = None
    ) -> str:
        
        template = self.prompt_templates.get((category, phase))
        if not template:
            return self._get_generic_diagnostic_prompt(phase)
        
        context_info = self._format_context_information(patient_context, session_info)
        
        prompt = f"""
{template.primary_prompt}

{context_info}

CLINICAL GUIDELINES:
{chr(10).join(f"• {guideline}" for guideline in template.clinical_guidelines)}

DSM-5 FOCUS AREAS:
{chr(10).join(f"• {criteria}" for criteria in template.dsm5_criteria_focus)}

SAFETY CONSIDERATIONS:
{chr(10).join(f"• {safety}" for safety in template.safety_considerations)}

DIFFERENTIAL DIAGNOSIS CONSIDERATIONS:
{chr(10).join(f"• {diff}" for diff in template.differential_considerations)}

Remember to:
- Maintain professional therapeutic rapport throughout
- Use empathetic, non-judgmental language
- Ask one question at a time and allow full responses
- Pay attention to both verbal and non-verbal cues mentioned
- Document any concerning responses for clinical review
- Follow up on positive screening responses appropriately
- Maintain clinical boundaries while building trust
"""
        return prompt.strip()
    
    def _initialize_diagnostic_prompts(self) -> Dict[tuple, DiagnosticPromptTemplate]:
        
        prompts = {}
        
        # MOOD DISORDERS - Major Depression
        prompts[(DiagnosticCategory.MOOD_DISORDERS, InterviewPhase.SYMPTOM_EXPLORATION)] = DiagnosticPromptTemplate(
            category=DiagnosticCategory.MOOD_DISORDERS,
            phase=InterviewPhase.SYMPTOM_EXPLORATION,
            primary_prompt="""
You are conducting a diagnostic interview focusing on mood disorders, specifically exploring symptoms of major depressive disorder. 

Begin by asking about the patient's mood over the past two weeks using empathetic, clear language. Explore the core symptoms systematically while maintaining a supportive therapeutic presence.

Start with: "I'd like to understand more about how you've been feeling lately. Over the past two weeks, have you been feeling down, depressed, or hopeless most of the day, nearly every day?"

Based on their response, follow up appropriately to gather detailed information about mood symptoms, their severity, duration, and impact on daily functioning.
""",
            follow_up_prompts=[
                "Can you tell me more about when these feelings are strongest during the day?",
                "How has this affected your energy levels and motivation?", 
                "Have you noticed changes in your appetite or sleep patterns?",
                "How has this impacted your ability to concentrate or make decisions?",
                "Have you lost interest in activities you used to enjoy?",
                "How are you managing these feelings day to day?"
            ],
            clinical_guidelines=[
                "Assess for duration of at least 2 weeks for major depressive episode",
                "Evaluate functional impairment in work, social, or other important areas",
                "Screen for manic/hypomanic episodes to rule out bipolar disorder",
                "Assess for psychotic features if depression is severe",
                "Evaluate for seasonal patterns or postpartum onset"
            ],
            safety_considerations=[
                "Always assess for suicidal ideation when depression symptoms are present",
                "Monitor for self-harm behaviors or thoughts",
                "Assess support systems and protective factors",
                "Evaluate need for immediate safety intervention",
                "Consider hospitalization risk factors"
            ],
            dsm5_criteria_focus=[
                "Depressed mood most of the day, nearly every day",
                "Markedly diminished interest or pleasure in activities",
                "Significant weight loss/gain or appetite changes",
                "Insomnia or hypersomnia nearly every day",
                "Psychomotor agitation or retardation",
                "Fatigue or loss of energy",
                "Feelings of worthlessness or excessive guilt",
                "Diminished concentration or indecisiveness",
                "Recurrent thoughts of death or suicidal ideation"
            ],
            differential_considerations=[
                "Rule out substance-induced mood disorder",
                "Consider medical conditions causing mood symptoms",
                "Differentiate from adjustment disorder with depressed mood",
                "Assess for bipolar disorder (history of mania/hypomania)",
                "Consider persistent depressive disorder vs. major depression"
            ]
        )
        
        # ANXIETY DISORDERS - Generalized Anxiety
        prompts[(DiagnosticCategory.ANXIETY_DISORDERS, InterviewPhase.SYMPTOM_EXPLORATION)] = DiagnosticPromptTemplate(
            category=DiagnosticCategory.ANXIETY_DISORDERS,
            phase=InterviewPhase.SYMPTOM_EXPLORATION,
            primary_prompt="""
You are conducting a diagnostic interview focusing on anxiety disorders, particularly generalized anxiety disorder. 

Explore the patient's experience with worry and anxiety in a gentle, understanding manner. Begin by normalizing their experience while gathering specific diagnostic information.

Start with: "Many people experience worry and anxiety. I'd like to understand your experience with this. Over the past 6 months, have you found yourself worrying excessively about various things in your life, more days than not?"

Follow up based on their response to gather details about the nature, frequency, and impact of their anxiety and worry patterns.
""",
            follow_up_prompts=[
                "What kinds of things do you find yourself worrying about most?",
                "How difficult is it for you to control or stop these worries?",
                "Do you experience physical symptoms along with the worry?",
                "How has this anxiety affected your daily activities or relationships?",
                "Are there specific situations that trigger more intense anxiety?",
                "What helps you manage these feelings when they occur?"
            ],
            clinical_guidelines=[
                "Assess for 6-month duration requirement for GAD diagnosis",
                "Evaluate excessive worry that is difficult to control",
                "Screen for other anxiety disorders (panic, social anxiety, specific phobias)",
                "Assess functional impairment and avoidance behaviors",
                "Rule out anxiety due to medical conditions or substances"
            ],
            safety_considerations=[
                "Monitor for panic attacks and their frequency/severity",
                "Assess for agoraphobic avoidance that might impact safety",
                "Evaluate for substance use as coping mechanism",
                "Check for self-medication with alcohol or drugs",
                "Consider impact on driving, work, or social functioning"
            ],
            dsm5_criteria_focus=[
                "Excessive anxiety and worry occurring more days than not",
                "Difficulty controlling worry",
                "Restlessness or feeling on edge",
                "Being easily fatigued",
                "Difficulty concentrating",
                "Irritability",
                "Muscle tension",
                "Sleep disturbance"
            ],
            differential_considerations=[
                "Differentiate from panic disorder",
                "Rule out social anxiety disorder",
                "Consider specific phobias vs. generalized worry",
                "Assess for anxiety due to medical conditions",
                "Differentiate from obsessive-compulsive disorder"
            ]
        )
        
        # TRAUMA DISORDERS - PTSD
        prompts[(DiagnosticCategory.TRAUMA_DISORDERS, InterviewPhase.SYMPTOM_EXPLORATION)] = DiagnosticPromptTemplate(
            category=DiagnosticCategory.TRAUMA_DISORDERS,
            phase=InterviewPhase.SYMPTOM_EXPLORATION,
            primary_prompt="""
You are conducting a trauma-informed diagnostic interview focusing on post-traumatic stress disorder. This requires particular sensitivity and care.

Approach trauma exploration gradually and with great sensitivity. Begin by establishing safety and letting the patient know they can pause or stop at any time.

Start with: "I want to ask about some experiences that might have been difficult or traumatic. Please know that you're in control of this conversation, and you can pause or stop at any time. Sometimes people experience or witness events that are very distressing or traumatic. Has anything like this happened to you?"

Proceed very carefully, allowing the patient to share at their own pace and comfort level.
""",
            follow_up_prompts=[
                "How long ago did this happen?",
                "Do you experience unwanted memories or dreams about it?",
                "Are there things that remind you of the event that you try to avoid?",
                "Have you noticed changes in your mood or thoughts since then?",
                "Do you feel more on guard or alert than before?",
                "How has this affected your sleep or concentration?"
            ],
            clinical_guidelines=[
                "Use trauma-informed approach with emphasis on safety and choice",
                "Assess for exposure to actual or threatened death, serious injury, or sexual violence",
                "Evaluate symptoms across all four PTSD symptom clusters",
                "Consider complex trauma and developmental trauma history",
                "Assess for dissociative symptoms and dissociative subtype"
            ],
            safety_considerations=[
                "Monitor for re-traumatization during assessment",
                "Assess current safety from ongoing trauma exposure",
                "Evaluate suicidal risk related to trauma symptoms",
                "Consider risk of self-harm or risky behaviors",
                "Assess for substance use as trauma coping mechanism"
            ],
            dsm5_criteria_focus=[
                "Intrusion symptoms (memories, dreams, flashbacks)",
                "Avoidance of trauma-related stimuli",
                "Negative alterations in cognition and mood",
                "Alterations in arousal and reactivity",
                "Duration of more than one month",
                "Functional impairment"
            ],
            differential_considerations=[
                "Differentiate from acute stress disorder",
                "Rule out adjustment disorder",
                "Consider complex PTSD presentations",
                "Assess for dissociative disorders",
                "Differentiate from other anxiety or mood disorders"
            ]
        )
        
        # RISK ASSESSMENT
        prompts[(DiagnosticCategory.MOOD_DISORDERS, InterviewPhase.RISK_ASSESSMENT)] = DiagnosticPromptTemplate(
            category=DiagnosticCategory.MOOD_DISORDERS,
            phase=InterviewPhase.RISK_ASSESSMENT,
            primary_prompt="""
You are conducting a crucial safety and risk assessment. This requires direct, clear questioning while maintaining therapeutic rapport and support.

Assess suicide risk systematically and thoroughly. Be direct but compassionate in your questioning.

Begin with: "I need to ask you some important questions about your safety. When people are going through difficult times like you've described, they sometimes have thoughts of hurting themselves or ending their life. Have you had any thoughts like this?"

Continue with systematic risk assessment based on their response, always prioritizing safety.
""",
            follow_up_prompts=[
                "How often have you been having these thoughts?",
                "Have you thought about how you might do this?",
                "Have you made any preparations or taken any steps?",
                "What stops you from acting on these thoughts?",
                "Who in your life would you feel comfortable talking to about this?",
                "Have you ever attempted to hurt yourself before?"
            ],
            clinical_guidelines=[
                "Use direct, clear language when asking about suicidal thoughts",
                "Assess frequency, intensity, and duration of suicidal ideation",
                "Evaluate specific plans, means, and intent",
                "Assess protective factors and reasons for living",
                "Document risk level and safety planning needs"
            ],
            safety_considerations=[
                "Immediate safety assessment takes priority over diagnosis",
                "Consider need for emergency services or hospitalization",
                "Ensure patient is not left alone if high risk",
                "Involve support systems with patient consent when appropriate",
                "Create safety plan before ending session"
            ],
            dsm5_criteria_focus=[
                "Recurrent thoughts of death",
                "Suicidal ideation with or without specific plan",
                "Suicide attempt or specific plan for committing suicide",
                "Assessment of lethality and means",
                "Functional impairment related to safety concerns"
            ],
            differential_considerations=[
                "Differentiate between passive and active suicidal ideation",
                "Assess for psychotic features influencing risk",
                "Consider impulsivity factors",
                "Evaluate substance use impact on risk",
                "Assess for command hallucinations if psychotic features present"
            ]
        )
        
        # Add more diagnostic categories and phases...
        
        return prompts
    
    def _initialize_safety_protocols(self) -> Dict[str, List[str]]:
        return {
            "suicide_risk": [
                "Ask directly about suicidal thoughts, plans, and intent",
                "Assess protective factors and social support",
                "Create safety plan with specific coping strategies",
                "Consider need for higher level of care",
                "Involve support system with patient consent",
                "Document risk assessment thoroughly"
            ],
            "homicide_risk": [
                "Ask directly about thoughts of harming others",
                "Assess specific targets and plans",
                "Consider duty to warn obligations",
                "Evaluate need for immediate intervention",
                "Contact emergency services if imminent danger",
                "Document all assessments and actions taken"
            ],
            "psychosis_risk": [
                "Assess reality testing and thought organization",
                "Evaluate for command hallucinations",
                "Consider safety implications of delusions",
                "Assess insight and judgment",
                "Consider need for psychiatric evaluation",
                "Monitor for agitation or unpredictable behavior"
            ],
            "child_abuse": [
                "Follow mandatory reporting requirements",
                "Assess immediate safety of child",
                "Document specific allegations or concerns",
                "Contact child protective services if required",
                "Provide support resources for family",
                "Consider need for emergency medical attention"
            ]
        }
    
    def _initialize_clinical_guidelines(self) -> Dict[str, List[str]]:
        return {
            "interviewing_principles": [
                "Start with open-ended questions, then become more specific",
                "Use patient's own words when possible",
                "Avoid leading or suggestive questions",
                "Allow silence for patient reflection",
                "Validate emotions while gathering information",
                "Maintain professional boundaries throughout"
            ],
            "diagnostic_accuracy": [
                "Gather sufficient information for each criterion",
                "Consider differential diagnoses systematically",
                "Assess functional impairment thoroughly",
                "Rule out medical causes when appropriate",
                "Document evidence for and against diagnoses",
                "Consider cultural factors in symptom presentation"
            ],
            "cultural_considerations": [
                "Ask about cultural background and beliefs",
                "Consider cultural expressions of distress",
                "Assess language barriers and communication style",
                "Understand family and community context",
                "Respect cultural values in treatment planning",
                "Use culturally appropriate assessment tools when available"
            ]
        }
    
    def get_follow_up_prompts(
        self,
        category: DiagnosticCategory,
        initial_response: str,
        context: Dict[str, Any] = None
    ) -> List[str]:
        
        base_template = self.prompt_templates.get((category, InterviewPhase.SYMPTOM_EXPLORATION))
        if not base_template:
            return self._get_generic_follow_ups()
        
        follow_ups = base_template.follow_up_prompts.copy()
        
        # Customize based on initial response content
        if "yes" in initial_response.lower() or "have" in initial_response.lower():
            follow_ups = self._prioritize_confirmation_questions(follow_ups)
        elif "no" in initial_response.lower() or "not really" in initial_response.lower():
            follow_ups = self._add_alternative_exploration(follow_ups)
        
        return follow_ups
    
    def get_crisis_intervention_prompt(self, risk_type: str = "suicide") -> str:
        safety_protocol = self.safety_protocols.get(risk_type, self.safety_protocols["suicide_risk"])
        
        return f"""
CRISIS INTERVENTION MODE ACTIVATED

You are now in crisis intervention mode. The patient has indicated potential {risk_type} risk.

IMMEDIATE PRIORITIES:
1. Ensure immediate safety
2. Assess level of risk
3. Engage support systems
4. Create safety plan
5. Consider need for emergency services

SAFETY PROTOCOL:
{chr(10).join(f"• {step}" for step in safety_protocol)}

APPROACH:
- Remain calm and supportive
- Ask direct questions about safety
- Do not leave patient alone if high risk
- Validate their pain while focusing on safety
- Involve emergency services if imminent danger
- Document all assessments and interventions

Your primary goal is safety. All other therapeutic objectives are secondary to ensuring the patient's immediate wellbeing.
"""
    
    def get_differential_diagnosis_prompt(
        self,
        primary_category: DiagnosticCategory,
        symptoms_presented: List[str],
        context: Dict[str, Any] = None
    ) -> str:
        
        differential_map = {
            DiagnosticCategory.MOOD_DISORDERS: [
                "Major Depressive Disorder vs. Persistent Depressive Disorder",
                "Bipolar Disorder (assess for manic/hypomanic episodes)",
                "Substance-Induced Mood Disorder",
                "Mood Disorder Due to Medical Condition",
                "Adjustment Disorder with Depressed Mood"
            ],
            DiagnosticCategory.ANXIETY_DISORDERS: [
                "Generalized Anxiety Disorder vs. Panic Disorder",
                "Social Anxiety Disorder vs. Specific Phobia",
                "Anxiety Due to Medical Condition",
                "Substance-Induced Anxiety Disorder",
                "Obsessive-Compulsive Disorder"
            ],
            DiagnosticCategory.TRAUMA_DISORDERS: [
                "PTSD vs. Acute Stress Disorder",
                "Complex PTSD vs. Borderline Personality Disorder",
                "Dissociative Disorders",
                "Adjustment Disorder",
                "Substance-Induced symptoms"
            ]
        }
        
        differentials = differential_map.get(primary_category, ["Consider alternative diagnoses"])
        
        return f"""
DIFFERENTIAL DIAGNOSIS EXPLORATION

You are now focusing on differential diagnosis for {primary_category.value}.

SYMPTOMS PRESENTED: {', '.join(symptoms_presented)}

KEY DIFFERENTIALS TO CONSIDER:
{chr(10).join(f"• {diff}" for diff in differentials)}

DIAGNOSTIC QUESTIONS TO EXPLORE:
• Onset and duration of symptoms
• Temporal relationships between symptoms
• Functional impairment patterns
• Response to previous treatments
• Family history of mental health conditions
• Medical history and current medications
• Substance use patterns
• Cultural and contextual factors

APPROACH:
- Ask specific questions to rule in/out each differential
- Look for pathognomonic symptoms
- Consider comorbidity possibilities
- Assess severity and functional impact
- Document evidence for each diagnostic consideration

Remember: It's better to gather more information than to rush to diagnostic closure.
"""
    
    def _format_context_information(
        self,
        patient_context: Dict[str, Any] = None,
        session_info: Dict[str, Any] = None
    ) -> str:
        
        if not patient_context and not session_info:
            return "CONTEXT: Initial diagnostic assessment"
        
        context_parts = []
        
        if patient_context:
            context_parts.append("PATIENT CONTEXT:")
            if patient_context.get("age"):
                context_parts.append(f"• Age: {patient_context['age']}")
            if patient_context.get("presenting_concerns"):
                context_parts.append(f"• Presenting concerns: {patient_context['presenting_concerns']}")
            if patient_context.get("previous_treatment"):
                context_parts.append(f"• Previous treatment: {patient_context['previous_treatment']}")
        
        if session_info:
            context_parts.append("SESSION CONTEXT:")
            if session_info.get("session_number"):
                context_parts.append(f"• Session: {session_info['session_number']}")
            if session_info.get("assessment_phase"):
                context_parts.append(f"• Assessment phase: {session_info['assessment_phase']}")
        
        return "\n".join(context_parts)
    
    def _get_generic_diagnostic_prompt(self, phase: InterviewPhase) -> str:
        generic_prompts = {
            InterviewPhase.OPENING: """
Begin the diagnostic interview with a warm, professional greeting. Establish rapport while explaining the assessment process.

Start with: "Thank you for being here today. I'd like to learn more about what's been concerning you and how I can help. Can you tell me what brought you here today?"
""",
            InterviewPhase.SYMPTOM_EXPLORATION: """
Explore the patient's symptoms systematically and empathetically. Ask about onset, duration, severity, and impact on functioning.

Focus on gathering specific, detailed information while maintaining therapeutic rapport.
""",
            InterviewPhase.RISK_ASSESSMENT: """
Conduct a thorough safety assessment. Ask direct questions about thoughts of self-harm or harm to others.

Prioritize safety while maintaining therapeutic relationship.
"""
        }
        
        return generic_prompts.get(phase, "Conduct professional diagnostic interview with empathy and clinical accuracy.")
    
    def _get_generic_follow_ups(self) -> List[str]:
        return [
            "Can you tell me more about that?",
            "When did you first notice this?",
            "How has this affected your daily life?",
            "What makes it better or worse?",
            "How are you coping with this?"
        ]
    
    def _prioritize_confirmation_questions(self, follow_ups: List[str]) -> List[str]:
        priority_questions = []
        remaining_questions = []
        
        for question in follow_ups:
            if any(word in question.lower() for word in ["when", "how long", "how often", "severity"]):
                priority_questions.append(question)
            else:
                remaining_questions.append(question)
        
        return priority_questions + remaining_questions
    
    def _add_alternative_exploration(self, follow_ups: List[str]) -> List[str]:
        alternative_questions = [
            "Have you experienced anything similar to what I described?",
            "Are there other concerns or symptoms you'd like to discuss?",
            "What other difficulties have you been experiencing?"
        ]
        
        return alternative_questions + follow_ups


# Specialized prompt generators for specific diagnostic scenarios

def generate_comorbidity_assessment_prompt(
    primary_diagnosis: str,
    secondary_concerns: List[str]
) -> str:
    return f"""
COMORBIDITY ASSESSMENT

Primary diagnostic focus: {primary_diagnosis}
Secondary concerns to explore: {', '.join(secondary_concerns)}

You are conducting an assessment for potential comorbid conditions. This requires careful evaluation of:

1. Symptom overlap vs. distinct disorders
2. Temporal relationships between conditions
3. Functional impact of each condition
4. Treatment implications of comorbidity

APPROACH:
- Ask about onset timing of different symptom clusters
- Explore periods when only one condition was present
- Assess whether symptoms occur independently
- Consider how conditions might influence each other
- Evaluate overall functional impairment

CLINICAL CONSIDERATIONS:
• Some symptoms may serve multiple diagnostic criteria
• Consider hierarchical diagnostic rules
• Assess if one condition better explains all symptoms
• Document evidence for each potential diagnosis
• Consider dimensional vs. categorical approaches
"""

def generate_cultural_assessment_prompt(
    cultural_background: str,
    presenting_concerns: List[str]
) -> str:
    return f"""
CULTURALLY-INFORMED DIAGNOSTIC ASSESSMENT

Patient cultural background: {cultural_background}
Presenting concerns: {', '.join(presenting_concerns)}

You are conducting a diagnostic assessment with careful attention to cultural factors.

CULTURAL CONSIDERATIONS:
- How symptoms are expressed and understood culturally
- Family and community context of mental health
- Religious or spiritual factors in symptom presentation
- Cultural stigma or acceptance of mental health treatment
- Language and communication patterns
- Cultural explanatory models for distress

APPROACH:
- Ask about cultural understanding of current difficulties
- Explore family and community perspectives
- Assess cultural strengths and resources
- Consider culture-bound syndromes
- Evaluate acculturation stressors if applicable
- Respectfully inquire about traditional healing practices

DIAGNOSTIC ACCURACY:
• Avoid cultural stereotyping
• Consider cultural variations in symptom expression
• Assess functional impairment within cultural context
• Use cultural formulation in diagnosis
• Consider cultural factors in treatment planning
"""


def generate_developmental_assessment_prompt(
    age_group: str,
    developmental_concerns: List[str]
) -> str:
    return f"""
DEVELOPMENTALLY-INFORMED DIAGNOSTIC ASSESSMENT

Age group: {age_group}
Developmental concerns: {', '.join(developmental_concerns)}

You are conducting a diagnostic assessment with careful attention to developmental factors.

DEVELOPMENTAL CONSIDERATIONS:
- Age-appropriate symptom expression
- Normal vs. pathological developmental variations
- Impact on developmental milestones
- Family and school functioning
- Peer relationships and social development

KEY AREAS TO ASSESS:
• Developmental history and milestones
• Academic or occupational functioning
• Social and emotional development
• Behavioral patterns across settings
• Family dynamics and parenting factors

APPROACH:
- Use developmentally appropriate language
- Consider multiple informants when appropriate
- Assess symptoms across different contexts
- Evaluate developmental trajectory
- Consider environmental and social factors
- Screen for neurodevelopmental conditions

Remember: Symptoms must be considered within normal developmental expectations for accurate diagnosis.
"""


# Main diagnostic prompts interface
class DiagnosticInterviewAI:
    
    def __init__(self):
        self.prompts_system = DiagnosticPromptsSystem()
    
    def start_diagnostic_interview(
        self,
        category: DiagnosticCategory,
        patient_context: Dict[str, Any] = None
    ) -> str:
        return self.prompts_system.get_diagnostic_prompt(
            category=category,
            phase=InterviewPhase.OPENING,
            patient_context=patient_context
        )
    
    def continue_symptom_exploration(
        self,
        category: DiagnosticCategory,
        patient_response: str,
        context: Dict[str, Any] = None
    ) -> str:
        return self.prompts_system.get_diagnostic_prompt(
            category=category,
            phase=InterviewPhase.SYMPTOM_EXPLORATION,
            patient_context=context
        )
    
    def assess_safety_risk(
        self,
        risk_type: str = "suicide"
    ) -> str:
        return self.prompts_system.get_crisis_intervention_prompt(risk_type)
    
    def explore_differential_diagnosis(
        self,
        primary_category: DiagnosticCategory,
        symptoms: List[str],
        context: Dict[str, Any] = None
    ) -> str:
        return self.prompts_system.get_differential_diagnosis_prompt(
            primary_category=primary_category,
            symptoms_presented=symptoms,
            context=context
        )


if __name__ == "__main__":
    # Example usage
    diagnostic_ai = DiagnosticInterviewAI()
    
    # Start depression assessment
    depression_prompt = diagnostic_ai.start_diagnostic_interview(
        category=DiagnosticCategory.MOOD_DISORDERS,
        patient_context={
            "age": 28,
            "presenting_concerns": "feeling down and unmotivated",
            "duration": "several weeks"
        }
    )
    
    print("=== DEPRESSION DIAGNOSTIC PROMPT ===")
    print(depression_prompt)
    
    # Safety assessment
    safety_prompt = diagnostic_ai.assess_safety_risk("suicide")
    
    print("\n=== SAFETY ASSESSMENT PROMPT ===")
    print(safety_prompt)
    
    # Differential diagnosis
    differential_prompt = diagnostic_ai.explore_differential_diagnosis(
        primary_category=DiagnosticCategory.MOOD_DISORDERS,
        symptoms=["depressed mood", "loss of interest", "fatigue", "sleep problems"]
    )
    
    print("\n=== DIFFERENTIAL DIAGNOSIS PROMPT ===")
    print(differential_prompt)
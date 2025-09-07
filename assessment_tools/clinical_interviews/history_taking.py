"""
Comprehensive History Taking Module
Structured clinical history collection for AI therapy system
Covers all essential areas of psychological assessment
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
import json


class HistorySection(Enum):
    """Types of history sections"""
    PRESENTING_PROBLEM = "presenting_problem"
    PSYCHIATRIC_HISTORY = "psychiatric_history"
    MEDICAL_HISTORY = "medical_history"
    FAMILY_HISTORY = "family_history"
    SOCIAL_HISTORY = "social_history"
    SUBSTANCE_USE = "substance_use"
    TRAUMA_HISTORY = "trauma_history"
    DEVELOPMENTAL_HISTORY = "developmental_history"
    EDUCATIONAL_OCCUPATIONAL = "educational_occupational"
    LEGAL_HISTORY = "legal_history"
    RELATIONSHIP_HISTORY = "relationship_history"
    CURRENT_FUNCTIONING = "current_functioning"


class RiskLevel(Enum):
    """Risk assessment levels"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class HistoryItem:
    """Individual history item"""
    section: HistorySection
    question: str
    answer: Optional[str] = None
    date_reported: Optional[datetime] = None
    follow_up_questions: List[str] = field(default_factory=list)
    clinical_significance: str = "routine"
    risk_indicators: List[str] = field(default_factory=list)


@dataclass
class ComprehensiveHistory:
    """Complete patient history"""
    patient_id: str
    collected_date: datetime
    sections: Dict[HistorySection, List[HistoryItem]] = field(default_factory=dict)
    risk_assessment: Dict[str, RiskLevel] = field(default_factory=dict)
    clinical_summary: str = ""
    red_flags: List[str] = field(default_factory=list)
    protective_factors: List[str] = field(default_factory=list)


class ClinicalHistoryTaking:
    """Comprehensive clinical history taking system"""
    
    def __init__(self):
        self.history_templates = self._initialize_history_templates()
        self.risk_indicators = self._initialize_risk_indicators()
        self.follow_up_protocols = self._initialize_follow_up_protocols()
    
    def _initialize_history_templates(self) -> Dict[HistorySection, List[Dict]]:
        """Initialize structured history taking templates"""
        return {
            HistorySection.PRESENTING_PROBLEM: [
                {
                    "question": "What brings you to therapy today?",
                    "type": "open_ended",
                    "follow_ups": [
                        "When did you first notice this problem?",
                        "What was happening in your life when it started?",
                        "How has it affected your daily functioning?",
                        "What have you tried to address this issue?",
                        "What made you decide to seek help now?"
                    ],
                    "risk_keywords": ["suicide", "self-harm", "hopeless", "worthless", "death"]
                },
                {
                    "question": "How would you rate your current distress level on a scale of 1-10?",
                    "type": "scale",
                    "scale_range": (1, 10),
                    "follow_ups": [
                        "What would make it a 10?",
                        "What would make it a 1?",
                        "When was the last time it was lower?"
                    ]
                },
                {
                    "question": "What are your main symptoms or concerns?",
                    "type": "checklist",
                    "options": [
                        "Depressed mood", "Anxiety", "Panic attacks", "Sleep problems",
                        "Appetite changes", "Concentration difficulties", "Memory problems",
                        "Mood swings", "Irritability", "Social withdrawal", "Fatigue",
                        "Guilt or shame", "Hopelessness", "Worthlessness"
                    ]
                }
            ],
            
            HistorySection.PSYCHIATRIC_HISTORY: [
                {
                    "question": "Have you ever received mental health treatment before?",
                    "type": "yes_no",
                    "follow_ups": [
                        "When and where did you receive treatment?",
                        "What type of treatment (therapy, medication, hospitalization)?",
                        "Who was your provider?",
                        "How long did treatment last?",
                        "What was helpful or unhelpful about previous treatment?",
                        "Why did treatment end?"
                    ]
                },
                {
                    "question": "Have you ever been diagnosed with a mental health condition?",
                    "type": "yes_no",
                    "follow_ups": [
                        "What diagnoses have you received?",
                        "Who gave you these diagnoses?",
                        "Do you agree with these diagnoses?",
                        "How did receiving the diagnosis affect you?"
                    ]
                },
                {
                    "question": "Have you ever been hospitalized for mental health reasons?",
                    "type": "yes_no",
                    "follow_ups": [
                        "When and where were you hospitalized?",
                        "What led to the hospitalization?",
                        "How long were you there?",
                        "Was it voluntary or involuntary?",
                        "What treatment did you receive during hospitalization?"
                    ],
                    "risk_keywords": ["involuntary", "suicide attempt", "psychosis", "danger"]
                },
                {
                    "question": "Are you currently taking any psychiatric medications?",
                    "type": "yes_no",
                    "follow_ups": [
                        "What medications are you taking?",
                        "What dosages?",
                        "Who prescribed them?",
                        "How long have you been taking them?",
                        "Are they helpful?",
                        "Any side effects?",
                        "Have you tried other medications in the past?"
                    ]
                }
            ],
            
            HistorySection.TRAUMA_HISTORY: [
                {
                    "question": "Have you experienced any traumatic or very stressful events?",
                    "type": "yes_no",
                    "follow_ups": [
                        "Can you tell me about what happened?",
                        "How old were you when this occurred?",
                        "How did this experience affect you?",
                        "Do you still think about it or have nightmares?",
                        "Do you avoid certain places, people, or situations because of it?",
                        "Have you received treatment specifically for this trauma?"
                    ],
                    "risk_keywords": ["abuse", "assault", "violence", "accident", "death", "war"],
                    "clinical_significance": "high"
                },
                {
                    "question": "As a child, did you experience any abuse, neglect, or other harmful experiences?",
                    "type": "yes_no",
                    "follow_ups": [
                        "What type of experiences did you have?",
                        "Who was involved?",
                        "How long did this continue?",
                        "Did anyone know or try to help?",
                        "How do you think this has affected you as an adult?"
                    ],
                    "risk_keywords": ["sexual abuse", "physical abuse", "emotional abuse", "neglect"],
                    "clinical_significance": "high"
                }
            ],
            
            HistorySection.FAMILY_HISTORY: [
                {
                    "question": "Does anyone in your family have a history of mental health problems?",
                    "type": "yes_no",
                    "follow_ups": [
                        "Which family members?",
                        "What conditions did they have?",
                        "Did they receive treatment?",
                        "How did their condition affect the family?",
                        "Are you concerned about genetic factors?"
                    ]
                },
                {
                    "question": "Is there any family history of suicide or suicide attempts?",
                    "type": "yes_no",
                    "follow_ups": [
                        "Which family member(s)?",
                        "When did this occur?",
                        "How did this affect you and your family?",
                        "Do you worry about this happening to you?"
                    ],
                    "risk_keywords": ["suicide", "completed suicide", "attempt"],
                    "clinical_significance": "high"
                },
                {
                    "question": "Tell me about your family relationships and dynamics.",
                    "type": "open_ended",
                    "follow_ups": [
                        "How would you describe your relationship with your parents?",
                        "Do you have siblings? How do you get along?",
                        "Who are you closest to in your family?",
                        "Are there any ongoing family conflicts or stressors?",
                        "How does your family handle emotions and problems?"
                    ]
                }
            ],
            
            HistorySection.SUBSTANCE_USE: [
                {
                    "question": "Do you use alcohol, drugs, or other substances?",
                    "type": "yes_no",
                    "follow_ups": [
                        "What substances do you use?",
                        "How often do you use them?",
                        "How much do you typically use?",
                        "When did you first start using?",
                        "Has your use increased over time?",
                        "Do you use substances to cope with emotions or problems?"
                    ]
                },
                {
                    "question": "Has substance use ever caused problems in your life?",
                    "type": "yes_no",
                    "follow_ups": [
                        "What kinds of problems has it caused?",
                        "Have others expressed concern about your use?",
                        "Have you ever tried to cut down or stop?",
                        "Have you experienced withdrawal symptoms?",
                        "Have you received treatment for substance use?"
                    ],
                    "risk_keywords": ["withdrawal", "DUI", "job loss", "relationship problems"]
                }
            ],
            
            HistorySection.SOCIAL_HISTORY: [
                {
                    "question": "Tell me about your current living situation.",
                    "type": "open_ended",
                    "follow_ups": [
                        "Who do you live with?",
                        "How stable is your housing?",
                        "Are you comfortable and safe where you live?",
                        "Any recent changes in living situation?"
                    ]
                },
                {
                    "question": "What is your relationship status?",
                    "type": "multiple_choice",
                    "options": ["Single", "Dating", "Married", "Divorced", "Separated", "Widowed"],
                    "follow_ups": [
                        "How would you describe your current relationship?",
                        "Any recent changes in relationship status?",
                        "History of significant relationships?",
                        "Any patterns in your relationships you've noticed?"
                    ]
                },
                {
                    "question": "Do you have children?",
                    "type": "yes_no",
                    "follow_ups": [
                        "How many children and what ages?",
                        "How is your relationship with your children?",
                        "Any concerns about parenting or custody?",
                        "How has having children affected your mental health?"
                    ]
                }
            ],
            
            HistorySection.MEDICAL_HISTORY: [
                {
                    "question": "Do you have any chronic medical conditions?",
                    "type": "yes_no",
                    "follow_ups": [
                        "What conditions do you have?",
                        "How are they managed?",
                        "How do they affect your daily life?",
                        "Do you think they affect your mental health?"
                    ]
                },
                {
                    "question": "Are you currently taking any medications?",
                    "type": "yes_no",
                    "follow_ups": [
                        "What medications are you taking?",
                        "What are they for?",
                        "Any side effects?",
                        "Do any of your medications affect your mood or thinking?"
                    ]
                },
                {
                    "question": "Have you had any recent major illnesses, surgeries, or injuries?",
                    "type": "yes_no",
                    "follow_ups": [
                        "What happened?",
                        "When did this occur?",
                        "How has your recovery been?",
                        "Has this affected your mental health?"
                    ]
                }
            ],
            
            HistorySection.CURRENT_FUNCTIONING: [
                {
                    "question": "How are you functioning at work or school?",
                    "type": "scale",
                    "scale_range": (1, 10),
                    "follow_ups": [
                        "What's your current work/school situation?",
                        "Any recent changes in performance?",
                        "How do you get along with colleagues/classmates?",
                        "Any accommodations needed for mental health?"
                    ]
                },
                {
                    "question": "How are your social relationships?",
                    "type": "scale",
                    "scale_range": (1, 10),
                    "follow_ups": [
                        "Do you have close friends or family you can talk to?",
                        "How often do you socialize?",
                        "Do you feel isolated or lonely?",
                        "Any recent changes in your social life?"
                    ]
                },
                {
                    "question": "How are you taking care of yourself?",
                    "type": "checklist",
                    "options": [
                        "Regular sleep schedule", "Healthy eating", "Exercise",
                        "Personal hygiene", "Medical appointments", "Hobbies/interests",
                        "Spiritual practices", "Relaxation/stress management"
                    ]
                }
            ]
        }
    
    def _initialize_risk_indicators(self) -> Dict[str, List[str]]:
        """Initialize risk indicator keywords and phrases"""
        return {
            "suicide_risk": [
                "suicide", "kill myself", "end it all", "better off dead",
                "suicidal thoughts", "want to die", "no point living",
                "hopeless", "worthless", "burden to others"
            ],
            "self_harm": [
                "cut myself", "self-harm", "self-injury", "burning",
                "scratching", "hitting myself", "self-mutilation"
            ],
            "violence_risk": [
                "hurt someone", "kill them", "homicidal", "violence",
                "revenge", "get back at", "make them pay", "weapon"
            ],
            "psychosis": [
                "hearing voices", "hallucinations", "paranoid", "conspiracy",
                "people following me", "delusions", "not real", "visions"
            ],
            "substance_abuse": [
                "drinking heavily", "using drugs", "can't stop", "withdrawal",
                "need to use", "tolerance", "blackouts", "overdose"
            ],
            "trauma_indicators": [
                "flashbacks", "nightmares", "can't forget", "keeps happening",
                "triggered", "avoidance", "hypervigilant", "jumpy"
            ]
        }
    
    def _initialize_follow_up_protocols(self) -> Dict[str, List[str]]:
        """Initialize follow-up question protocols"""
        return {
            "suicide_assessment": [
                "Are you having thoughts of hurting yourself?",
                "Have you thought about how you might do it?",
                "Do you have access to means (weapons, pills, etc.)?",
                "What has stopped you from acting on these thoughts?",
                "Have you made any preparations or written notes?",
                "When do you feel most suicidal?",
                "What helps when you have these thoughts?"
            ],
            "trauma_assessment": [
                "How often do you think about what happened?",
                "Do you have nightmares or flashbacks?",
                "Do you avoid certain places, people, or situations?",
                "Do you feel emotionally numb or disconnected?",
                "Are you easily startled or on edge?",
                "How has this affected your relationships?",
                "Do you blame yourself for what happened?"
            ],
            "substance_assessment": [
                "How much do you typically use?",
                "How often are you using?",
                "Have you tried to cut down or stop?",
                "Do you use more than you intend to?",
                "Do you need more to get the same effect?",
                "Do you have withdrawal symptoms?",
                "Has use caused problems in your life?"
            ]
        }
    
    def create_comprehensive_history(self, patient_id: str) -> ComprehensiveHistory:
        """Create a new comprehensive history assessment"""
        return ComprehensiveHistory(
            patient_id=patient_id,
            collected_date=datetime.now()
        )
    
    def get_section_questions(self, section: HistorySection) -> List[Dict]:
        """Get all questions for a specific history section"""
        return self.history_templates.get(section, [])
    
    def add_history_item(self, history: ComprehensiveHistory, 
                        section: HistorySection, question: str, 
                        answer: str) -> HistoryItem:
        """Add a history item and assess for risk indicators"""
        
        # Create history item
        history_item = HistoryItem(
            section=section,
            question=question,
            answer=answer,
            date_reported=datetime.now()
        )
        
        # Analyze answer for risk indicators
        risk_indicators = self._analyze_risk_indicators(answer)
        history_item.risk_indicators = risk_indicators
        
        # Set clinical significance
        history_item.clinical_significance = self._assess_clinical_significance(
            section, answer, risk_indicators
        )
        
        # Generate follow-up questions
        history_item.follow_up_questions = self._generate_follow_ups(
            section, answer, risk_indicators
        )
        
        # Add to history
        if section not in history.sections:
            history.sections[section] = []
        history.sections[section].append(history_item)
        
        # Update risk assessment
        self._update_risk_assessment(history, risk_indicators)
        
        return history_item
    
    def _analyze_risk_indicators(self, answer: str) -> List[str]:
        """Analyze answer text for risk indicators"""
        if not answer:
            return []
        
        answer_lower = answer.lower()
        found_indicators = []
        
        for risk_type, keywords in self.risk_indicators.items():
            for keyword in keywords:
                if keyword.lower() in answer_lower:
                    found_indicators.append(risk_type)
                    break
        
        return found_indicators
    
    def _assess_clinical_significance(self, section: HistorySection, 
                                   answer: str, risk_indicators: List[str]) -> str:
        """Assess clinical significance of the response"""
        
        if risk_indicators:
            return "high"
        
        # Section-specific significance
        if section in [HistorySection.TRAUMA_HISTORY, HistorySection.PSYCHIATRIC_HISTORY]:
            if answer and len(answer) > 50:  # Detailed response suggests significance
                return "moderate"
        
        if section == HistorySection.FAMILY_HISTORY:
            family_keywords = ["depression", "anxiety", "bipolar", "schizophrenia", "suicide"]
            if any(keyword in answer.lower() for keyword in family_keywords):
                return "moderate"
        
        return "routine"
    
    def _generate_follow_ups(self, section: HistorySection, answer: str, 
                           risk_indicators: List[str]) -> List[str]:
        """Generate appropriate follow-up questions"""
        follow_ups = []
        
        # Risk-based follow-ups
        if "suicide_risk" in risk_indicators:
            follow_ups.extend(self.follow_up_protocols["suicide_assessment"])
        
        if "trauma_indicators" in risk_indicators:
            follow_ups.extend(self.follow_up_protocols["trauma_assessment"])
        
        if "substance_abuse" in risk_indicators:
            follow_ups.extend(self.follow_up_protocols["substance_assessment"])
        
        # Section-specific follow-ups
        section_questions = self.history_templates.get(section, [])
        for question_template in section_questions:
            if any(keyword in answer.lower() for keyword in 
                   question_template.get("risk_keywords", [])):
                follow_ups.extend(question_template.get("follow_ups", []))
                break
        
        return follow_ups[:5]  # Limit to 5 most relevant follow-ups
    
    def _update_risk_assessment(self, history: ComprehensiveHistory, 
                              risk_indicators: List[str]):
        """Update overall risk assessment"""
        
        for indicator in risk_indicators:
            current_risk = history.risk_assessment.get(indicator, RiskLevel.LOW)
            
            # Escalate risk level
            if indicator == "suicide_risk":
                history.risk_assessment[indicator] = RiskLevel.HIGH
            elif indicator in ["violence_risk", "psychosis"]:
                history.risk_assessment[indicator] = RiskLevel.HIGH
            elif indicator in ["self_harm", "substance_abuse"]:
                history.risk_assessment[indicator] = max(current_risk, RiskLevel.MODERATE)
            else:
                history.risk_assessment[indicator] = max(current_risk, RiskLevel.MODERATE)
    
    def generate_clinical_summary(self, history: ComprehensiveHistory) -> str:
        """Generate clinical summary of history"""
        summary_parts = []
        
        # Presenting problem
        presenting_items = history.sections.get(HistorySection.PRESENTING_PROBLEM, [])
        if presenting_items:
            summary_parts.append(f"PRESENTING PROBLEM: {presenting_items[0].answer}")
        
        # Risk factors
        high_risk_items = []
        for section_items in history.sections.values():
            for item in section_items:
                if item.clinical_significance == "high":
                    high_risk_items.append(f"{item.section.value}: {item.question}")
        
        if high_risk_items:
            summary_parts.append(f"HIGH RISK FACTORS: {', '.join(high_risk_items)}")
        
        # Current risk assessment
        if history.risk_assessment:
            risk_summary = ", ".join([f"{risk}: {level.value}" 
                                    for risk, level in history.risk_assessment.items()])
            summary_parts.append(f"CURRENT RISK LEVELS: {risk_summary}")
        
        # Treatment history
        psych_items = history.sections.get(HistorySection.PSYCHIATRIC_HISTORY, [])
        if psych_items:
            treatment_history = [item.answer for item in psych_items if "treatment" in item.question.lower()]
            if treatment_history:
                summary_parts.append(f"TREATMENT HISTORY: {treatment_history[0]}")
        
        return "\n\n".join(summary_parts)
    
    def identify_protective_factors(self, history: ComprehensiveHistory) -> List[str]:
        """Identify protective factors from history"""
        protective_factors = []
        
        # Check social support
        social_items = history.sections.get(HistorySection.SOCIAL_HISTORY, [])
        for item in social_items:
            if "relationship" in item.question.lower() and item.answer:
                if any(word in item.answer.lower() for word in ["good", "supportive", "close", "strong"]):
                    protective_factors.append("Strong social support system")
        
        # Check coping strategies
        functioning_items = history.sections.get(HistorySection.CURRENT_FUNCTIONING, [])
        for item in functioning_items:
            if "taking care" in item.question.lower() and item.answer:
                if any(word in item.answer.lower() for word in ["exercise", "sleep", "eating", "hobbies"]):
                    protective_factors.append("Active self-care practices")
        
        # Check treatment engagement
        psych_items = history.sections.get(HistorySection.PSYCHIATRIC_HISTORY, [])
        for item in psych_items:
            if "treatment" in item.question.lower() and item.answer:
                if any(word in item.answer.lower() for word in ["helpful", "beneficial", "working"]):
                    protective_factors.append("Previous positive treatment response")
        
        return protective_factors
    
    def get_recommended_assessments(self, history: ComprehensiveHistory) -> List[str]:
        """Recommend specific assessments based on history"""
        recommendations = []
        
        # Risk-based recommendations
        if RiskLevel.HIGH in history.risk_assessment.values():
            recommendations.append("Immediate safety assessment required")
        
        if "suicide_risk" in history.risk_assessment:
            recommendations.append("Columbia Suicide Severity Rating Scale")
        
        if "trauma_indicators" in history.risk_assessment:
            recommendations.append("PCL-5 (PTSD Checklist)")
            recommendations.append("Trauma history questionnaire")
        
        if "substance_abuse" in history.risk_assessment:
            recommendations.append("AUDIT (Alcohol Use Disorders Identification Test)")
            recommendations.append("DAST (Drug Abuse Screening Test)")
        
        # Symptom-based recommendations
        presenting_items = history.sections.get(HistorySection.PRESENTING_PROBLEM, [])
        for item in presenting_items:
            if item.answer:
                answer_lower = item.answer.lower()
                if "depress" in answer_lower:
                    recommendations.append("PHQ-9 (Depression screening)")
                if "anxiety" in answer_lower:
                    recommendations.append("GAD-7 (Anxiety screening)")
                if "mood" in answer_lower:
                    recommendations.append("Mood disorder questionnaire")
        
        return list(set(recommendations))  # Remove duplicates


# Example usage and testing
if __name__ == "__main__":
    # Initialize history taking system
    history_system = ClinicalHistoryTaking()
    
    # Create new comprehensive history
    patient_history = history_system.create_comprehensive_history("PATIENT_001")
    
    # Add some example history items
    history_system.add_history_item(
        patient_history,
        HistorySection.PRESENTING_PROBLEM,
        "What brings you to therapy today?",
        "I've been feeling really depressed and sometimes think about suicide. I can't sleep and have no energy."
    )
    
    history_system.add_history_item(
        patient_history,
        HistorySection.FAMILY_HISTORY,
        "Does anyone in your family have a history of mental health problems?",
        "My mother had severe depression and my uncle completed suicide when I was 16."
    )
    
    history_system.add_history_item(
        patient_history,
        HistorySection.TRAUMA_HISTORY,
        "Have you experienced any traumatic or very stressful events?",
        "I was in a car accident last year and still have nightmares about it. I avoid driving now."
    )
    
    # Generate clinical summary
    clinical_summary = history_system.generate_clinical_summary(patient_history)
    print("CLINICAL SUMMARY:")
    print(clinical_summary)
    print("\n" + "="*50 + "\n")
    
    # Get protective factors
    protective_factors = history_system.identify_protective_factors(patient_history)
    print("PROTECTIVE FACTORS:")
    for factor in protective_factors:
        print(f"- {factor}")
    print("\n" + "="*50 + "\n")
    
    # Get recommended assessments
    recommendations = history_system.get_recommended_assessments(patient_history)
    print("RECOMMENDED ASSESSMENTS:")
    for rec in recommendations:
        print(f"- {rec}")
    print("\n" + "="*50 + "\n")
    
    # Show risk assessment
    print("RISK ASSESSMENT:")
    for risk_type, level in patient_history.risk_assessment.items():
        print(f"- {risk_type}: {level.value}")
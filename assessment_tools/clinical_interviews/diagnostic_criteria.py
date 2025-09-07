"""
Diagnostic Criteria Module
Based on DSM-5 criteria for mental health assessment
Provides structured diagnostic evaluation tools for AI therapy system
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json


class SeverityLevel(Enum):
    """Severity levels for diagnostic criteria"""
    NONE = 0
    MILD = 1
    MODERATE = 2
    SEVERE = 3
    EXTREME = 4


@dataclass
class DiagnosticCriterion:
    """Individual diagnostic criterion"""
    code: str
    description: str
    required: bool = False
    severity_levels: List[str] = None
    duration_required: str = None
    exclusions: List[str] = None


@dataclass
class DiagnosticAssessment:
    """Results of diagnostic assessment"""
    disorder_code: str
    criteria_met: Dict[str, bool]
    severity: SeverityLevel
    confidence_level: float
    notes: str
    recommendations: List[str]


class DSM5DiagnosticCriteria:
    """DSM-5 based diagnostic criteria for common mental health disorders"""
    
    def __init__(self):
        self.criteria_database = self._initialize_criteria_database()
    
    def _initialize_criteria_database(self) -> Dict[str, Dict]:
        """Initialize the diagnostic criteria database"""
        return {
            "F32.9": {  # Major Depressive Episode
                "name": "Major Depressive Episode",
                "category": "Depressive Disorders",
                "criteria": {
                    "A": DiagnosticCriterion(
                        code="A",
                        description="Five or more symptoms present during same 2-week period",
                        required=True,
                        duration_required="2 weeks",
                        severity_levels=["mild", "moderate", "severe"]
                    ),
                    "A1": DiagnosticCriterion(
                        code="A1",
                        description="Depressed mood most of the day, nearly every day",
                        required=False
                    ),
                    "A2": DiagnosticCriterion(
                        code="A2",
                        description="Diminished interest or pleasure in activities",
                        required=False
                    ),
                    "A3": DiagnosticCriterion(
                        code="A3",
                        description="Significant weight loss/gain or appetite changes",
                        required=False
                    ),
                    "A4": DiagnosticCriterion(
                        code="A4",
                        description="Insomnia or hypersomnia nearly every day",
                        required=False
                    ),
                    "A5": DiagnosticCriterion(
                        code="A5",
                        description="Psychomotor agitation or retardation",
                        required=False
                    ),
                    "A6": DiagnosticCriterion(
                        code="A6",
                        description="Fatigue or loss of energy nearly every day",
                        required=False
                    ),
                    "A7": DiagnosticCriterion(
                        code="A7",
                        description="Feelings of worthlessness or inappropriate guilt",
                        required=False
                    ),
                    "A8": DiagnosticCriterion(
                        code="A8",
                        description="Diminished concentration or indecisiveness",
                        required=False
                    ),
                    "A9": DiagnosticCriterion(
                        code="A9",
                        description="Recurrent thoughts of death or suicidal ideation",
                        required=False
                    ),
                    "B": DiagnosticCriterion(
                        code="B",
                        description="Symptoms cause significant distress or impairment",
                        required=True
                    ),
                    "C": DiagnosticCriterion(
                        code="C",
                        description="Episode not attributable to substance use or medical condition",
                        required=True
                    )
                },
                "required_minimum": 5,
                "required_core": ["A1", "A2"]  # At least one must be present
            },
            
            "F41.1": {  # Generalized Anxiety Disorder
                "name": "Generalized Anxiety Disorder",
                "category": "Anxiety Disorders",
                "criteria": {
                    "A": DiagnosticCriterion(
                        code="A",
                        description="Excessive anxiety and worry about multiple events",
                        required=True,
                        duration_required="6 months"
                    ),
                    "B": DiagnosticCriterion(
                        code="B",
                        description="Difficulty controlling the worry",
                        required=True
                    ),
                    "C": DiagnosticCriterion(
                        code="C",
                        description="Three or more associated symptoms",
                        required=True
                    ),
                    "C1": DiagnosticCriterion(
                        code="C1",
                        description="Restlessness or feeling keyed up or on edge",
                        required=False
                    ),
                    "C2": DiagnosticCriterion(
                        code="C2",
                        description="Being easily fatigued",
                        required=False
                    ),
                    "C3": DiagnosticCriterion(
                        code="C3",
                        description="Difficulty concentrating or mind going blank",
                        required=False
                    ),
                    "C4": DiagnosticCriterion(
                        code="C4",
                        description="Irritability",
                        required=False
                    ),
                    "C5": DiagnosticCriterion(
                        code="C5",
                        description="Muscle tension",
                        required=False
                    ),
                    "C6": DiagnosticCriterion(
                        code="C6",
                        description="Sleep disturbance",
                        required=False
                    ),
                    "D": DiagnosticCriterion(
                        code="D",
                        description="Symptoms cause significant distress or impairment",
                        required=True
                    ),
                    "E": DiagnosticCriterion(
                        code="E",
                        description="Not attributable to substance use or medical condition",
                        required=True
                    )
                },
                "required_minimum": 3,
                "c_criteria_needed": 3
            },
            
            "F43.10": {  # PTSD
                "name": "Post-Traumatic Stress Disorder",
                "category": "Trauma and Stressor-Related Disorders",
                "criteria": {
                    "A": DiagnosticCriterion(
                        code="A",
                        description="Exposure to actual or threatened death, serious injury, or sexual violence",
                        required=True
                    ),
                    "B": DiagnosticCriterion(
                        code="B",
                        description="Intrusion symptoms associated with traumatic event",
                        required=True
                    ),
                    "C": DiagnosticCriterion(
                        code="C",
                        description="Avoidance of trauma-related stimuli",
                        required=True
                    ),
                    "D": DiagnosticCriterion(
                        code="D",
                        description="Negative alterations in cognitions and mood",
                        required=True
                    ),
                    "E": DiagnosticCriterion(
                        code="E",
                        description="Alterations in arousal and reactivity",
                        required=True
                    ),
                    "F": DiagnosticCriterion(
                        code="F",
                        description="Duration more than 1 month",
                        required=True,
                        duration_required="1 month"
                    ),
                    "G": DiagnosticCriterion(
                        code="G",
                        description="Significant distress or functional impairment",
                        required=True
                    ),
                    "H": DiagnosticCriterion(
                        code="H",
                        description="Not attributable to substance use or medical condition",
                        required=True
                    )
                }
            },
            
            "F60.3": {  # Borderline Personality Disorder
                "name": "Borderline Personality Disorder",
                "category": "Personality Disorders",
                "criteria": {
                    "A": DiagnosticCriterion(
                        code="A",
                        description="Pervasive pattern of instability beginning by early adulthood",
                        required=True
                    ),
                    "A1": DiagnosticCriterion(
                        code="A1",
                        description="Frantic efforts to avoid real or imagined abandonment",
                        required=False
                    ),
                    "A2": DiagnosticCriterion(
                        code="A2",
                        description="Unstable and intense interpersonal relationships",
                        required=False
                    ),
                    "A3": DiagnosticCriterion(
                        code="A3",
                        description="Identity disturbance: unstable self-image",
                        required=False
                    ),
                    "A4": DiagnosticCriterion(
                        code="A4",
                        description="Impulsivity in potentially self-damaging areas",
                        required=False
                    ),
                    "A5": DiagnosticCriterion(
                        code="A5",
                        description="Recurrent suicidal behavior or self-mutilating behavior",
                        required=False
                    ),
                    "A6": DiagnosticCriterion(
                        code="A6",
                        description="Affective instability due to mood reactivity",
                        required=False
                    ),
                    "A7": DiagnosticCriterion(
                        code="A7",
                        description="Chronic feelings of emptiness",
                        required=False
                    ),
                    "A8": DiagnosticCriterion(
                        code="A8",
                        description="Inappropriate, intense anger or difficulty controlling anger",
                        required=False
                    ),
                    "A9": DiagnosticCriterion(
                        code="A9",
                        description="Transient, stress-related paranoid ideation or dissociation",
                        required=False
                    )
                },
                "required_minimum": 5
            }
        }
    
    def get_disorder_criteria(self, disorder_code: str) -> Dict:
        """Get diagnostic criteria for a specific disorder"""
        return self.criteria_database.get(disorder_code, {})
    
    def list_available_disorders(self) -> List[Tuple[str, str]]:
        """List all available disorders with codes and names"""
        return [(code, data["name"]) for code, data in self.criteria_database.items()]
    
    def assess_criteria(self, disorder_code: str, symptoms: Dict[str, bool], 
                       severity_ratings: Dict[str, int] = None) -> DiagnosticAssessment:
        """
        Assess whether diagnostic criteria are met for a disorder
        
        Args:
            disorder_code: ICD-10 disorder code
            symptoms: Dict mapping criterion codes to presence (True/False)
            severity_ratings: Dict mapping criterion codes to severity (0-4)
        
        Returns:
            DiagnosticAssessment object
        """
        disorder_data = self.criteria_database.get(disorder_code)
        if not disorder_data:
            raise ValueError(f"Unknown disorder code: {disorder_code}")
        
        criteria_met = {}
        total_symptoms = 0
        core_symptoms_met = 0
        
        # Check each criterion
        for criterion_code, criterion in disorder_data["criteria"].items():
            is_met = symptoms.get(criterion_code, False)
            criteria_met[criterion_code] = is_met
            
            if is_met:
                total_symptoms += 1
                
                # Check core symptoms for depression
                if disorder_code == "F32.9" and criterion_code in ["A1", "A2"]:
                    core_symptoms_met += 1
        
        # Determine if diagnosis is met
        diagnosis_met = self._evaluate_diagnosis(disorder_code, disorder_data, 
                                               criteria_met, total_symptoms, 
                                               core_symptoms_met)
        
        # Calculate severity
        severity = self._calculate_severity(severity_ratings or {})
        
        # Calculate confidence
        confidence = self._calculate_confidence(disorder_data, criteria_met, 
                                              total_symptoms)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(disorder_code, 
                                                       criteria_met, severity)
        
        return DiagnosticAssessment(
            disorder_code=disorder_code,
            criteria_met=criteria_met,
            severity=severity,
            confidence_level=confidence,
            notes=f"Assessment for {disorder_data['name']}",
            recommendations=recommendations
        )
    
    def _evaluate_diagnosis(self, disorder_code: str, disorder_data: Dict,
                          criteria_met: Dict[str, bool], total_symptoms: int,
                          core_symptoms_met: int) -> bool:
        """Evaluate whether diagnostic criteria are satisfied"""
        
        # Check required criteria
        for criterion_code, criterion in disorder_data["criteria"].items():
            if criterion.required and not criteria_met.get(criterion_code, False):
                return False
        
        # Special rules for specific disorders
        if disorder_code == "F32.9":  # Major Depression
            # Need at least 5 symptoms and at least one core symptom
            required_min = disorder_data.get("required_minimum", 5)
            return (total_symptoms >= required_min and core_symptoms_met >= 1)
        
        elif disorder_code == "F41.1":  # GAD
            # Need at least 3 C criteria
            c_criteria_met = sum(1 for code in ["C1", "C2", "C3", "C4", "C5", "C6"] 
                               if criteria_met.get(code, False))
            return c_criteria_met >= 3
        
        elif disorder_code == "F60.3":  # BPD
            # Need at least 5 of the 9 A criteria
            a_criteria_met = sum(1 for code in [f"A{i}" for i in range(1, 10)] 
                               if criteria_met.get(code, False))
            return a_criteria_met >= 5
        
        elif disorder_code == "F43.10":  # PTSD
            # All required criteria must be met
            return all(criteria_met.get(code, False) 
                      for code in ["A", "B", "C", "D", "E", "F", "G", "H"])
        
        return True
    
    def _calculate_severity(self, severity_ratings: Dict[str, int]) -> SeverityLevel:
        """Calculate overall severity based on individual ratings"""
        if not severity_ratings:
            return SeverityLevel.MILD
        
        avg_severity = sum(severity_ratings.values()) / len(severity_ratings)
        
        if avg_severity < 1:
            return SeverityLevel.NONE
        elif avg_severity < 2:
            return SeverityLevel.MILD
        elif avg_severity < 3:
            return SeverityLevel.MODERATE
        elif avg_severity < 4:
            return SeverityLevel.SEVERE
        else:
            return SeverityLevel.EXTREME
    
    def _calculate_confidence(self, disorder_data: Dict, criteria_met: Dict[str, bool],
                            total_symptoms: int) -> float:
        """Calculate confidence level of diagnosis"""
        total_criteria = len(disorder_data["criteria"])
        met_criteria = sum(criteria_met.values())
        
        # Base confidence on proportion of criteria met
        base_confidence = met_criteria / total_criteria
        
        # Adjust based on required criteria
        required_met = sum(1 for code, criterion in disorder_data["criteria"].items()
                          if criterion.required and criteria_met.get(code, False))
        required_total = sum(1 for criterion in disorder_data["criteria"].values()
                           if criterion.required)
        
        if required_total > 0:
            required_confidence = required_met / required_total
            confidence = (base_confidence + required_confidence) / 2
        else:
            confidence = base_confidence
        
        return min(confidence, 1.0)
    
    def _generate_recommendations(self, disorder_code: str, criteria_met: Dict[str, bool],
                                severity: SeverityLevel) -> List[str]:
        """Generate treatment recommendations based on diagnosis"""
        recommendations = []
        
        # General recommendations based on disorder
        if disorder_code == "F32.9":  # Depression
            recommendations.extend([
                "Consider cognitive-behavioral therapy (CBT)",
                "Evaluate need for medication consultation",
                "Implement behavioral activation strategies",
                "Monitor suicide risk regularly"
            ])
            
        elif disorder_code == "F41.1":  # GAD
            recommendations.extend([
                "Implement anxiety management techniques",
                "Consider relaxation training and mindfulness",
                "Cognitive restructuring for worry patterns",
                "Gradual exposure to anxiety triggers"
            ])
            
        elif disorder_code == "F43.10":  # PTSD
            recommendations.extend([
                "Trauma-focused therapy (CPT, EMDR, or PE)",
                "Safety and stabilization as first priority",
                "Address comorbid conditions",
                "Consider intensive outpatient programs"
            ])
            
        elif disorder_code == "F60.3":  # BPD
            recommendations.extend([
                "Dialectical Behavior Therapy (DBT) recommended",
                "Focus on emotion regulation skills",
                "Address self-harm behaviors immediately",
                "Long-term therapy commitment needed"
            ])
        
        # Severity-based recommendations
        if severity in [SeverityLevel.SEVERE, SeverityLevel.EXTREME]:
            recommendations.extend([
                "Consider intensive outpatient or inpatient treatment",
                "Frequent monitoring and safety planning",
                "Medication evaluation strongly recommended"
            ])
        
        return recommendations
    
    def generate_diagnostic_interview_questions(self, disorder_code: str) -> List[Dict]:
        """Generate structured interview questions for a specific disorder"""
        disorder_data = self.criteria_database.get(disorder_code)
        if not disorder_data:
            return []
        
        questions = []
        
        for criterion_code, criterion in disorder_data["criteria"].items():
            # Skip meta-criteria
            if criterion_code in ["A", "B", "C", "D", "E", "F", "G", "H"] and disorder_code != "F43.10":
                continue
                
            question = {
                "criterion_code": criterion_code,
                "question": self._generate_question_text(criterion.description),
                "type": "yes_no",
                "follow_up": self._generate_follow_up_questions(criterion),
                "severity_scale": criterion.severity_levels
            }
            questions.append(question)
        
        return questions
    
    def _generate_question_text(self, description: str) -> str:
        """Convert criterion description to interview question"""
        question_starters = {
            "Depressed mood": "Over the past two weeks, have you been feeling sad, empty, or depressed most of the day, nearly every day?",
            "Diminished interest": "Have you lost interest or pleasure in activities you usually enjoy?",
            "weight loss": "Have you experienced significant changes in your weight or appetite?",
            "Insomnia": "Have you been having trouble sleeping or sleeping too much?",
            "Psychomotor": "Have others noticed that you've been moving or speaking more slowly than usual, or have you felt restless?",
            "Fatigue": "Have you been feeling tired or lacking energy nearly every day?",
            "worthlessness": "Have you been feeling worthless or excessively guilty about things?",
            "concentration": "Have you had trouble concentrating or making decisions?",
            "thoughts of death": "Have you had thoughts about death or suicide?"
        }
        
        for key, question in question_starters.items():
            if key.lower() in description.lower():
                return question
        
        return f"Have you experienced: {description.lower()}?"
    
    def _generate_follow_up_questions(self, criterion: DiagnosticCriterion) -> List[str]:
        """Generate follow-up questions for deeper assessment"""
        follow_ups = []
        
        if criterion.duration_required:
            follow_ups.append(f"How long has this been going on? (Required: {criterion.duration_required})")
        
        if criterion.severity_levels:
            follow_ups.append("On a scale of 1-4, how severe would you rate this symptom?")
        
        follow_ups.append("Can you give me a specific example of when this happened?")
        follow_ups.append("How much does this interfere with your daily life?")
        
        return follow_ups


# Example usage and testing
if __name__ == "__main__":
    # Initialize diagnostic criteria
    diagnostic_tool = DSM5DiagnosticCriteria()
    
    # Example assessment for depression
    depression_symptoms = {
        "A1": True,   # Depressed mood
        "A2": True,   # Loss of interest
        "A3": False,  # Weight changes
        "A4": True,   # Sleep problems
        "A5": False,  # Psychomotor changes
        "A6": True,   # Fatigue
        "A7": True,   # Worthlessness
        "A8": True,   # Concentration problems
        "A9": False,  # Suicidal thoughts
        "B": True,    # Functional impairment
        "C": True     # Not due to substance
    }
    
    severity_ratings = {
        "A1": 3,  # Severe depressed mood
        "A2": 2,  # Moderate loss of interest
        "A4": 2,  # Moderate sleep problems
        "A6": 3,  # Severe fatigue
        "A7": 2,  # Moderate worthlessness
        "A8": 2   # Moderate concentration problems
    }
    
    # Assess depression
    assessment = diagnostic_tool.assess_criteria("F32.9", depression_symptoms, severity_ratings)
    
    print(f"Disorder: {assessment.disorder_code}")
    print(f"Severity: {assessment.severity.name}")
    print(f"Confidence: {assessment.confidence_level:.2%}")
    print(f"Recommendations: {assessment.recommendations}")
    
    # Generate interview questions
    questions = diagnostic_tool.generate_diagnostic_interview_questions("F32.9")
    print(f"\nGenerated {len(questions)} interview questions for depression assessment")
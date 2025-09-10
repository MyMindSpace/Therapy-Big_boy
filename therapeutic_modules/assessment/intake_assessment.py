from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import sqlite3
import json
import uuid
from datetime import datetime, date


class IntakePhase(Enum):
    WELCOME_ORIENTATION = "welcome_orientation"
    PRESENTING_CONCERNS = "presenting_concerns"
    HISTORY_GATHERING = "history_gathering"
    PSYCHOSOCIAL_ASSESSMENT = "psychosocial_assessment"
    MENTAL_STATUS_EXAM = "mental_status_exam"
    RISK_ASSESSMENT = "risk_assessment"
    TREATMENT_PLANNING = "treatment_planning"
    GOAL_SETTING = "goal_setting"
    WRAP_UP = "wrap_up"


class IntakeArea(Enum):
    DEMOGRAPHIC_INFO = "demographic_info"
    PRESENTING_PROBLEM = "presenting_problem"
    SYMPTOM_HISTORY = "symptom_history"
    MEDICAL_HISTORY = "medical_history"
    FAMILY_HISTORY = "family_history"
    SOCIAL_HISTORY = "social_history"
    EDUCATIONAL_OCCUPATIONAL = "educational_occupational"
    RELATIONSHIPS = "relationships"
    SUBSTANCE_USE = "substance_use"
    TRAUMA_HISTORY = "trauma_history"
    PREVIOUS_TREATMENT = "previous_treatment"
    STRENGTHS_RESOURCES = "strengths_resources"
    CULTURAL_FACTORS = "cultural_factors"
    FUNCTIONAL_ASSESSMENT = "functional_assessment"


class AssessmentStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    INTERRUPTED = "interrupted"
    REQUIRES_FOLLOW_UP = "requires_follow_up"


class RiskLevel(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    IMMINENT = "imminent"
    UNKNOWN = "unknown"


class SeverityLevel(Enum):
    MINIMAL = "minimal"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    EXTREME = "extreme"


@dataclass
class DemographicInfo:
    age: Optional[int] = None
    gender: str = ""
    pronouns: str = ""
    race_ethnicity: List[str] = field(default_factory=list)
    primary_language: str = ""
    education_level: str = ""
    employment_status: str = ""
    marital_status: str = ""
    living_situation: str = ""
    insurance_type: str = ""
    emergency_contact: Dict[str, str] = field(default_factory=dict)


@dataclass
class PresentingProblem:
    chief_complaint: str = ""
    problem_description: str = ""
    onset_timeline: str = ""
    severity_rating: int = 0
    frequency: str = ""
    duration: str = ""
    precipitating_factors: List[str] = field(default_factory=list)
    current_stressors: List[str] = field(default_factory=list)
    impact_on_functioning: Dict[str, str] = field(default_factory=dict)
    previous_episodes: bool = False
    what_brings_them_now: str = ""


@dataclass
class MedicalHistory:
    current_medications: List[Dict[str, str]] = field(default_factory=list)
    medical_conditions: List[str] = field(default_factory=list)
    hospitalizations: List[Dict[str, str]] = field(default_factory=list)
    surgeries: List[Dict[str, str]] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    substance_use: Dict[str, Any] = field(default_factory=dict)
    sleep_patterns: Dict[str, str] = field(default_factory=dict)
    appetite_changes: str = ""
    pain_issues: str = ""


@dataclass
class FamilyHistory:
    mental_health_history: List[Dict[str, str]] = field(default_factory=list)
    substance_abuse_history: List[Dict[str, str]] = field(default_factory=list)
    suicide_attempts: List[Dict[str, str]] = field(default_factory=list)
    medical_conditions: List[Dict[str, str]] = field(default_factory=list)
    family_dynamics: str = ""
    childhood_environment: str = ""
    parenting_style: str = ""
    family_stressors: List[str] = field(default_factory=list)


@dataclass
class TraumaHistory:
    childhood_trauma: List[Dict[str, Any]] = field(default_factory=list)
    adult_trauma: List[Dict[str, Any]] = field(default_factory=list)
    domestic_violence: Dict[str, Any] = field(default_factory=dict)
    sexual_assault: Dict[str, Any] = field(default_factory=dict)
    combat_exposure: Dict[str, Any] = field(default_factory=dict)
    medical_trauma: Dict[str, Any] = field(default_factory=dict)
    traumatic_loss: List[Dict[str, Any]] = field(default_factory=list)
    ptsd_symptoms: List[str] = field(default_factory=list)
    trauma_impact: str = ""


@dataclass
class SocialHistory:
    family_relationships: Dict[str, str] = field(default_factory=dict)
    intimate_relationships: Dict[str, str] = field(default_factory=dict)
    friendships: str = ""
    social_support: List[str] = field(default_factory=list)
    cultural_background: str = ""
    religious_spiritual: str = ""
    hobbies_interests: List[str] = field(default_factory=list)
    financial_status: str = ""
    legal_issues: str = ""
    housing_stability: str = ""


@dataclass
class TreatmentHistory:
    previous_therapy: List[Dict[str, str]] = field(default_factory=list)
    previous_medications: List[Dict[str, str]] = field(default_factory=list)
    hospitalizations: List[Dict[str, str]] = field(default_factory=list)
    what_helped: List[str] = field(default_factory=list)
    what_didnt_help: List[str] = field(default_factory=list)
    therapy_expectations: str = ""
    treatment_goals: List[str] = field(default_factory=list)


@dataclass
class MentalStatusExam:
    appearance: str = ""
    behavior: str = ""
    speech: str = ""
    mood: str = ""
    affect: str = ""
    thought_process: str = ""
    thought_content: str = ""
    perceptual_disturbances: str = ""
    cognition: Dict[str, str] = field(default_factory=dict)
    insight: str = ""
    judgment: str = ""


@dataclass
class RiskAssessment:
    suicide_risk: RiskLevel = RiskLevel.UNKNOWN
    self_harm_risk: RiskLevel = RiskLevel.UNKNOWN
    violence_risk: RiskLevel = RiskLevel.UNKNOWN
    substance_abuse_risk: RiskLevel = RiskLevel.UNKNOWN
    risk_factors: List[str] = field(default_factory=list)
    protective_factors: List[str] = field(default_factory=list)
    previous_attempts: List[Dict[str, str]] = field(default_factory=list)
    current_ideation: Dict[str, Any] = field(default_factory=dict)
    safety_plan_needed: bool = False
    immediate_interventions: List[str] = field(default_factory=list)


@dataclass
class IntakeAssessmentResult:
    assessment_id: str
    patient_id: str
    assessment_date: datetime
    status: AssessmentStatus
    demographic_info: DemographicInfo
    presenting_problem: PresentingProblem
    medical_history: MedicalHistory
    family_history: FamilyHistory
    trauma_history: TraumaHistory
    social_history: SocialHistory
    treatment_history: TreatmentHistory
    mental_status_exam: MentalStatusExam
    risk_assessment: RiskAssessment
    clinical_impressions: List[str] = field(default_factory=list)
    differential_diagnoses: List[str] = field(default_factory=list)
    treatment_recommendations: List[str] = field(default_factory=list)
    session_notes: str = ""
    clinician_observations: str = ""
    next_steps: List[str] = field(default_factory=list)


@dataclass
class IntakeSession:
    session_id: str
    patient_id: str
    start_time: datetime
    end_time: Optional[datetime]
    current_phase: IntakePhase
    completed_phases: List[IntakePhase]
    session_notes: Dict[str, str] = field(default_factory=dict)
    clinician_observations: str = ""
    patient_engagement: int = 0
    rapport_quality: int = 0
    crisis_indicators: List[str] = field(default_factory=list)
    immediate_concerns: List[str] = field(default_factory=list)
    session_status: AssessmentStatus = AssessmentStatus.IN_PROGRESS


class IntakeAssessmentModule:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.assessment_templates = self._initialize_assessment_templates()
        self.screening_questions = self._initialize_screening_questions()
        self.risk_indicators = self._initialize_risk_indicators()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS intake_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    assessment_date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    demographic_info TEXT,
                    presenting_problem TEXT,
                    medical_history TEXT,
                    family_history TEXT,
                    trauma_history TEXT,
                    social_history TEXT,
                    treatment_history TEXT,
                    mental_status_exam TEXT,
                    risk_assessment TEXT,
                    clinical_impressions TEXT,
                    differential_diagnoses TEXT,
                    treatment_recommendations TEXT,
                    session_notes TEXT,
                    clinician_observations TEXT,
                    next_steps TEXT,
                    created_date TEXT,
                    last_updated TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS intake_sessions (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    assessment_id TEXT,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    current_phase TEXT,
                    completed_phases TEXT,
                    session_notes TEXT,
                    clinician_observations TEXT,
                    patient_engagement INTEGER,
                    rapport_quality INTEGER,
                    crisis_indicators TEXT,
                    immediate_concerns TEXT,
                    session_status TEXT,
                    FOREIGN KEY (assessment_id) REFERENCES intake_assessments (assessment_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS intake_responses (
                    response_id TEXT PRIMARY KEY,
                    assessment_id TEXT NOT NULL,
                    question_id TEXT NOT NULL,
                    response_text TEXT,
                    response_value TEXT,
                    response_time TEXT,
                    notes TEXT,
                    FOREIGN KEY (assessment_id) REFERENCES intake_assessments (assessment_id)
                )
            """)
    
    def _initialize_assessment_templates(self) -> Dict[IntakeArea, Dict[str, Any]]:
        templates = {}
        
        templates[IntakeArea.DEMOGRAPHIC_INFO] = {
            "questions": [
                {"id": "age", "text": "What is your age?", "type": "numeric"},
                {"id": "gender", "text": "What is your gender identity?", "type": "open_text"},
                {"id": "pronouns", "text": "What pronouns do you use?", "type": "open_text"},
                {"id": "race_ethnicity", "text": "How do you identify racially/ethnically?", "type": "multiple_choice"},
                {"id": "primary_language", "text": "What is your primary language?", "type": "open_text"},
                {"id": "education", "text": "What is your highest level of education?", "type": "multiple_choice"},
                {"id": "employment", "text": "What is your current employment status?", "type": "multiple_choice"},
                {"id": "marital_status", "text": "What is your relationship status?", "type": "multiple_choice"},
                {"id": "living_situation", "text": "What is your current living situation?", "type": "open_text"}
            ],
            "clinical_focus": ["Basic demographics", "Cultural considerations", "Social determinants"]
        }
        
        templates[IntakeArea.PRESENTING_PROBLEM] = {
            "questions": [
                {"id": "chief_complaint", "text": "What brings you to therapy today?", "type": "open_text"},
                {"id": "problem_onset", "text": "When did you first notice these difficulties?", "type": "open_text"},
                {"id": "severity", "text": "On a scale of 1-10, how severe are these problems?", "type": "scale_1_10"},
                {"id": "frequency", "text": "How often do you experience these difficulties?", "type": "frequency"},
                {"id": "precipitating_factors", "text": "What do you think might have triggered these problems?", "type": "open_text"},
                {"id": "impact_functioning", "text": "How are these problems affecting your daily life?", "type": "open_text"},
                {"id": "previous_episodes", "text": "Have you experienced similar problems before?", "type": "yes_no"},
                {"id": "what_brings_now", "text": "What made you decide to seek help now?", "type": "open_text"}
            ],
            "clinical_focus": ["Symptom presentation", "Functional impairment", "Timeline", "Severity assessment"]
        }
        
        templates[IntakeArea.MEDICAL_HISTORY] = {
            "questions": [
                {"id": "current_medications", "text": "What medications are you currently taking?", "type": "open_text"},
                {"id": "medical_conditions", "text": "Do you have any current medical conditions?", "type": "open_text"},
                {"id": "hospitalizations", "text": "Have you been hospitalized recently?", "type": "open_text"},
                {"id": "allergies", "text": "Do you have any allergies?", "type": "open_text"},
                {"id": "sleep_patterns", "text": "How are you sleeping?", "type": "open_text"},
                {"id": "appetite", "text": "Have you noticed changes in appetite or weight?", "type": "open_text"},
                {"id": "pain_issues", "text": "Are you experiencing any pain?", "type": "open_text"}
            ],
            "clinical_focus": ["Medical comorbidities", "Medication effects", "Physical symptoms"]
        }
        
        return templates
    
    def _initialize_screening_questions(self) -> Dict[str, List[Dict[str, Any]]]:
        return {
            "depression_screening": [
                {"question": "Over the past 2 weeks, how often have you felt down, depressed, or hopeless?", "scale": "frequency"},
                {"question": "Over the past 2 weeks, how often have you had little interest or pleasure in activities?", "scale": "frequency"},
                {"question": "Have you had thoughts that you would be better off dead?", "scale": "yes_no"}
            ],
            "anxiety_screening": [
                {"question": "Over the past 2 weeks, how often have you felt nervous, anxious, or on edge?", "scale": "frequency"},
                {"question": "Over the past 2 weeks, how often have you been unable to stop or control worrying?", "scale": "frequency"},
                {"question": "Do you avoid situations that make you anxious?", "scale": "yes_no"}
            ],
            "trauma_screening": [
                {"question": "Have you ever experienced or witnessed a traumatic event?", "scale": "yes_no"},
                {"question": "Do you have unwanted memories or nightmares about difficult experiences?", "scale": "frequency"},
                {"question": "Do you avoid reminders of difficult experiences?", "scale": "yes_no"}
            ]
        }
    
    def _initialize_risk_indicators(self) -> Dict[str, List[str]]:
        return {
            "suicide_risk_factors": [
                "Previous suicide attempts",
                "Current suicidal ideation",
                "Detailed suicide plan",
                "Access to means",
                "Social isolation",
                "Recent losses",
                "Substance abuse",
                "Chronic illness",
                "History of mental illness"
            ],
            "protective_factors": [
                "Strong social support",
                "Religious/spiritual beliefs",
                "Sense of responsibility to family",
                "Therapeutic relationship",
                "Access to mental health care",
                "Coping skills",
                "Hope for future",
                "Problem-solving skills"
            ],
            "crisis_indicators": [
                "Acute suicidal ideation",
                "Psychotic symptoms",
                "Severe depression",
                "Substance intoxication",
                "Domestic violence",
                "Child abuse concerns",
                "Homicidal ideation",
                "Severe agitation"
            ]
        }
    
    def start_intake_assessment(self, patient_id: str) -> IntakeSession:
        session_id = str(uuid.uuid4())
        assessment_id = str(uuid.uuid4())
        
        session = IntakeSession(
            session_id=session_id,
            patient_id=patient_id,
            start_time=datetime.now(),
            end_time=None,
            current_phase=IntakePhase.WELCOME_ORIENTATION,
            completed_phases=[],
            session_notes={},
            clinician_observations="",
            patient_engagement=0,
            rapport_quality=0,
            crisis_indicators=[],
            immediate_concerns=[],
            session_status=AssessmentStatus.IN_PROGRESS
        )
        
        assessment = IntakeAssessmentResult(
            assessment_id=assessment_id,
            patient_id=patient_id,
            assessment_date=datetime.now(),
            status=AssessmentStatus.IN_PROGRESS,
            demographic_info=DemographicInfo(),
            presenting_problem=PresentingProblem(),
            medical_history=MedicalHistory(),
            family_history=FamilyHistory(),
            trauma_history=TraumaHistory(),
            social_history=SocialHistory(),
            treatment_history=TreatmentHistory(),
            mental_status_exam=MentalStatusExam(),
            risk_assessment=RiskAssessment(),
            clinical_impressions=[],
            differential_diagnoses=[],
            treatment_recommendations=[],
            session_notes="",
            clinician_observations="",
            next_steps=[]
        )
        
        self._save_intake_session(session)
        self._save_intake_assessment(assessment)
        return session
    
    def update_assessment_data(self, assessment_id: str, area: IntakeArea, data: Dict[str, Any]) -> bool:
        assessment = self._get_assessment(assessment_id)
        if not assessment:
            return False
        
        if area == IntakeArea.DEMOGRAPHIC_INFO:
            for key, value in data.items():
                if hasattr(assessment.demographic_info, key):
                    setattr(assessment.demographic_info, key, value)
        
        elif area == IntakeArea.PRESENTING_PROBLEM:
            for key, value in data.items():
                if hasattr(assessment.presenting_problem, key):
                    setattr(assessment.presenting_problem, key, value)
        
        elif area == IntakeArea.MEDICAL_HISTORY:
            for key, value in data.items():
                if hasattr(assessment.medical_history, key):
                    setattr(assessment.medical_history, key, value)
        
        elif area == IntakeArea.FAMILY_HISTORY:
            for key, value in data.items():
                if hasattr(assessment.family_history, key):
                    setattr(assessment.family_history, key, value)
        
        elif area == IntakeArea.TRAUMA_HISTORY:
            for key, value in data.items():
                if hasattr(assessment.trauma_history, key):
                    setattr(assessment.trauma_history, key, value)
        
        elif area == IntakeArea.SOCIAL_HISTORY:
            for key, value in data.items():
                if hasattr(assessment.social_history, key):
                    setattr(assessment.social_history, key, value)
        
        self._save_intake_assessment(assessment)
        return True
    
    def conduct_risk_assessment(self, assessment_id: str, risk_data: Dict[str, Any]) -> RiskAssessment:
        assessment = self._get_assessment(assessment_id)
        if not assessment:
            return RiskAssessment()
        
        risk_assessment = assessment.risk_assessment
        
        risk_assessment.suicide_risk = self._assess_suicide_risk(risk_data)
        risk_assessment.self_harm_risk = self._assess_self_harm_risk(risk_data)
        risk_assessment.violence_risk = self._assess_violence_risk(risk_data)
        risk_assessment.substance_abuse_risk = self._assess_substance_risk(risk_data)
        
        risk_assessment.risk_factors = self._identify_risk_factors(risk_data)
        risk_assessment.protective_factors = self._identify_protective_factors(risk_data)
        
        if risk_data.get('current_ideation'):
            risk_assessment.current_ideation = risk_data['current_ideation']
        
        if risk_data.get('previous_attempts'):
            risk_assessment.previous_attempts = risk_data['previous_attempts']
        
        risk_assessment.safety_plan_needed = self._determine_safety_plan_need(risk_assessment)
        risk_assessment.immediate_interventions = self._determine_immediate_interventions(risk_assessment)
        
        assessment.risk_assessment = risk_assessment
        self._save_intake_assessment(assessment)
        return risk_assessment
    
    def complete_mental_status_exam(self, assessment_id: str, mse_data: Dict[str, str]) -> MentalStatusExam:
        assessment = self._get_assessment(assessment_id)
        if not assessment:
            return MentalStatusExam()
        
        mse = MentalStatusExam()
        for key, value in mse_data.items():
            if hasattr(mse, key):
                setattr(mse, key, value)
        
        assessment.mental_status_exam = mse
        self._save_intake_assessment(assessment)
        return mse
    
    def generate_clinical_summary(self, assessment_id: str) -> Dict[str, Any]:
        assessment = self._get_assessment(assessment_id)
        if not assessment:
            return {}
        
        summary = {
            "presenting_concerns": assessment.presenting_problem.chief_complaint,
            "risk_level": assessment.risk_assessment.suicide_risk.value,
            "functional_impairment": assessment.presenting_problem.impact_on_functioning,
            "strengths_resources": self._extract_strengths(assessment),
            "treatment_priorities": self._identify_treatment_priorities(assessment),
            "recommended_interventions": self._recommend_interventions(assessment),
            "diagnostic_considerations": self._generate_diagnostic_considerations(assessment),
            "treatment_modality_recommendations": self._recommend_treatment_modalities(assessment)
        }
        
        return summary
    
    def get_assessment_questions(self, area: IntakeArea) -> List[Dict[str, Any]]:
        template = self.assessment_templates.get(area, {})
        return template.get("questions", [])
    
    def assess_crisis_indicators(self, patient_responses: Dict[str, Any]) -> List[str]:
        crisis_indicators = []
        
        if patient_responses.get('suicidal_ideation') == 'yes':
            crisis_indicators.append("Active suicidal ideation")
        
        if patient_responses.get('homicidal_ideation') == 'yes':
            crisis_indicators.append("Homicidal ideation")
        
        if patient_responses.get('psychotic_symptoms') == 'yes':
            crisis_indicators.append("Psychotic symptoms")
        
        if patient_responses.get('substance_intoxication') == 'yes':
            crisis_indicators.append("Substance intoxication")
        
        severity_rating = patient_responses.get('severity_rating', 0)
        if severity_rating >= 8:
            crisis_indicators.append("High severity symptoms")
        
        return crisis_indicators
    
    def _assess_suicide_risk(self, risk_data: Dict[str, Any]) -> RiskLevel:
        risk_score = 0
        
        if risk_data.get('current_ideation'):
            risk_score += 3
        if risk_data.get('previous_attempts'):
            risk_score += 2
        if risk_data.get('detailed_plan'):
            risk_score += 3
        if risk_data.get('access_to_means'):
            risk_score += 2
        if risk_data.get('social_isolation'):
            risk_score += 1
        if risk_data.get('substance_abuse'):
            risk_score += 1
        if risk_data.get('recent_losses'):
            risk_score += 1
        
        if risk_score >= 8:
            return RiskLevel.IMMINENT
        elif risk_score >= 5:
            return RiskLevel.HIGH
        elif risk_score >= 3:
            return RiskLevel.MODERATE
        elif risk_score >= 1:
            return RiskLevel.LOW
        else:
            return RiskLevel.LOW
    
    def _assess_self_harm_risk(self, risk_data: Dict[str, Any]) -> RiskLevel:
        if risk_data.get('self_harm_history') or risk_data.get('current_self_harm_urges'):
            return RiskLevel.MODERATE
        return RiskLevel.LOW
    
    def _assess_violence_risk(self, risk_data: Dict[str, Any]) -> RiskLevel:
        if risk_data.get('violence_history') or risk_data.get('homicidal_ideation'):
            return RiskLevel.HIGH
        return RiskLevel.LOW
    
    def _assess_substance_risk(self, risk_data: Dict[str, Any]) -> RiskLevel:
        substance_use = risk_data.get('substance_use', {})
        if substance_use.get('daily_use') or substance_use.get('impairment'):
            return RiskLevel.HIGH
        elif substance_use.get('regular_use'):
            return RiskLevel.MODERATE
        return RiskLevel.LOW
    
    def _identify_risk_factors(self, risk_data: Dict[str, Any]) -> List[str]:
        factors = []
        risk_indicators = self.risk_indicators['suicide_risk_factors']
        
        for indicator in risk_indicators:
            key = indicator.lower().replace(' ', '_')
            if risk_data.get(key):
                factors.append(indicator)
        
        return factors
    
    def _identify_protective_factors(self, risk_data: Dict[str, Any]) -> List[str]:
        factors = []
        protective_indicators = self.risk_indicators['protective_factors']
        
        for indicator in protective_indicators:
            key = indicator.lower().replace(' ', '_')
            if risk_data.get(key):
                factors.append(indicator)
        
        return factors
    
    def _determine_safety_plan_need(self, risk_assessment: RiskAssessment) -> bool:
        return risk_assessment.suicide_risk in [RiskLevel.MODERATE, RiskLevel.HIGH, RiskLevel.IMMINENT]
    
    def _determine_immediate_interventions(self, risk_assessment: RiskAssessment) -> List[str]:
        interventions = []
        
        if risk_assessment.suicide_risk == RiskLevel.IMMINENT:
            interventions.extend([
                "Emergency psychiatric evaluation",
                "24/7 supervision",
                "Remove access to means",
                "Crisis hotline contact"
            ])
        elif risk_assessment.suicide_risk == RiskLevel.HIGH:
            interventions.extend([
                "Safety planning",
                "Frequent check-ins",
                "Crisis resources",
                "Emergency contacts"
            ])
        elif risk_assessment.suicide_risk == RiskLevel.MODERATE:
            interventions.extend([
                "Safety planning",
                "Crisis resources",
                "Support system activation"
            ])
        
        return interventions
    
    def _extract_strengths(self, assessment: IntakeAssessmentResult) -> List[str]:
        strengths = []
        
        if assessment.social_history.social_support:
            strengths.append("Strong social support system")
        
        if assessment.treatment_history.what_helped:
            strengths.append("Previous positive treatment response")
        
        if assessment.social_history.hobbies_interests:
            strengths.append("Engaged in meaningful activities")
        
        if "stable" in assessment.social_history.housing_stability.lower():
            strengths.append("Housing stability")
        
        return strengths
    
    def _identify_treatment_priorities(self, assessment: IntakeAssessmentResult) -> List[str]:
        priorities = []
        
        if assessment.risk_assessment.suicide_risk != RiskLevel.LOW:
            priorities.append("Safety and risk management")
        
        if assessment.presenting_problem.severity_rating >= 7:
            priorities.append("Symptom stabilization")
        
        if "severe" in assessment.presenting_problem.impact_on_functioning.get("work", "").lower():
            priorities.append("Functional improvement")
        
        if assessment.trauma_history.childhood_trauma or assessment.trauma_history.adult_trauma:
            priorities.append("Trauma processing")
        
        return priorities
    
    def _recommend_interventions(self, assessment: IntakeAssessmentResult) -> List[str]:
        interventions = []
        
        if "depression" in assessment.presenting_problem.chief_complaint.lower():
            interventions.extend(["CBT for depression", "Behavioral activation"])
        
        if "anxiety" in assessment.presenting_problem.chief_complaint.lower():
            interventions.extend(["CBT for anxiety", "Exposure therapy"])
        
        if assessment.trauma_history.ptsd_symptoms:
            interventions.extend(["Trauma-focused therapy", "EMDR"])
        
        if assessment.medical_history.substance_use:
            interventions.append("Substance abuse treatment")
        
        return interventions
    
    def _generate_diagnostic_considerations(self, assessment: IntakeAssessmentResult) -> List[str]:
        considerations = []
        
        presenting_problem = assessment.presenting_problem.chief_complaint.lower()
        symptoms = assessment.presenting_problem.problem_description.lower()
        
        if any(word in presenting_problem for word in ["depressed", "sad", "hopeless", "empty"]):
            considerations.append("Major Depressive Disorder")
            if assessment.presenting_problem.previous_episodes:
                considerations.append("Recurrent Major Depressive Disorder")
        
        if any(word in presenting_problem for word in ["anxious", "worry", "nervous", "panic"]):
            considerations.append("Generalized Anxiety Disorder")
            if "panic" in symptoms:
                considerations.append("Panic Disorder")
        
        if assessment.trauma_history.ptsd_symptoms:
            considerations.append("Post-Traumatic Stress Disorder")
            considerations.append("Acute Stress Disorder")
        
        if assessment.medical_history.substance_use:
            considerations.append("Substance Use Disorder")
            considerations.append("Substance-Induced Mood Disorder")
        
        if "mood swings" in symptoms or "manic" in symptoms:
            considerations.append("Bipolar Disorder")
        
        if assessment.presenting_problem.onset_timeline == "chronic" or "years" in assessment.presenting_problem.onset_timeline:
            considerations.append("Persistent Depressive Disorder (Dysthymia)")
        
        if assessment.family_history.mental_health_history:
            considerations.append("Consider genetic predisposition factors")
        
        return considerations
    
    def _recommend_treatment_modalities(self, assessment: IntakeAssessmentResult) -> List[str]:
        modalities = []
        
        presenting_problem = assessment.presenting_problem.chief_complaint.lower()
        severity = assessment.presenting_problem.severity_rating
        
        if severity >= 7:
            modalities.append("Individual therapy (weekly)")
        elif severity >= 4:
            modalities.append("Individual therapy (bi-weekly)")
        else:
            modalities.append("Individual therapy (monthly)")
        
        if "depression" in presenting_problem:
            modalities.extend(["Cognitive Behavioral Therapy (CBT)", "Interpersonal Therapy (IPT)"])
        
        if "anxiety" in presenting_problem:
            modalities.extend(["Cognitive Behavioral Therapy (CBT)", "Acceptance and Commitment Therapy (ACT)"])
        
        if assessment.trauma_history.ptsd_symptoms:
            modalities.extend(["Trauma-Focused CBT", "EMDR", "Prolonged Exposure Therapy"])
        
        if assessment.social_history.family_relationships and "conflict" in str(assessment.social_history.family_relationships):
            modalities.append("Family therapy")
        
        if assessment.social_history.intimate_relationships and "problems" in str(assessment.social_history.intimate_relationships):
            modalities.append("Couples therapy")
        
        if assessment.medical_history.substance_use:
            modalities.extend(["Substance abuse counseling", "12-step programs", "Motivational interviewing"])
        
        if severity >= 8 or assessment.risk_assessment.suicide_risk == RiskLevel.HIGH:
            modalities.append("Intensive outpatient program (IOP)")
        
        if assessment.risk_assessment.suicide_risk == RiskLevel.IMMINENT:
            modalities.append("Inpatient psychiatric treatment")
        
        return modalities
    
    def _save_intake_assessment(self, assessment: IntakeAssessmentResult):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO intake_assessments (
                    assessment_id, patient_id, assessment_date, status,
                    demographic_info, presenting_problem, medical_history,
                    family_history, trauma_history, social_history,
                    treatment_history, mental_status_exam, risk_assessment,
                    clinical_impressions, differential_diagnoses, treatment_recommendations,
                    session_notes, clinician_observations, next_steps,
                    created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id,
                assessment.patient_id,
                assessment.assessment_date.isoformat(),
                assessment.status.value,
                json.dumps(assessment.demographic_info.__dict__),
                json.dumps(assessment.presenting_problem.__dict__),
                json.dumps(assessment.medical_history.__dict__),
                json.dumps(assessment.family_history.__dict__),
                json.dumps(assessment.trauma_history.__dict__),
                json.dumps(assessment.social_history.__dict__),
                json.dumps(assessment.treatment_history.__dict__),
                json.dumps(assessment.mental_status_exam.__dict__),
                json.dumps(assessment.risk_assessment.__dict__),
                json.dumps(assessment.clinical_impressions),
                json.dumps(assessment.differential_diagnoses),
                json.dumps(assessment.treatment_recommendations),
                assessment.session_notes,
                assessment.clinician_observations,
                json.dumps(assessment.next_steps),
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
    
    def _save_intake_session(self, session: IntakeSession):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO intake_sessions (
                    session_id, patient_id, assessment_id, start_time, end_time,
                    current_phase, completed_phases, session_notes,
                    clinician_observations, patient_engagement, rapport_quality,
                    crisis_indicators, immediate_concerns, session_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id,
                session.patient_id,
                None,  # assessment_id will be linked separately
                session.start_time.isoformat(),
                session.end_time.isoformat() if session.end_time else None,
                session.current_phase.value,
                json.dumps([phase.value for phase in session.completed_phases]),
                json.dumps(session.session_notes),
                session.clinician_observations,
                session.patient_engagement,
                session.rapport_quality,
                json.dumps(session.crisis_indicators),
                json.dumps(session.immediate_concerns),
                session.session_status.value
            ))
    
    def _get_assessment(self, assessment_id: str) -> Optional[IntakeAssessmentResult]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM intake_assessments WHERE assessment_id = ?
            """, (assessment_id,))
            row = cursor.fetchone()
            
            if row:
                return IntakeAssessmentResult(
                    assessment_id=row[0],
                    patient_id=row[1],
                    assessment_date=datetime.fromisoformat(row[2]),
                    status=AssessmentStatus(row[3]),
                    demographic_info=DemographicInfo(**json.loads(row[4]) if row[4] else {}),
                    presenting_problem=PresentingProblem(**json.loads(row[5]) if row[5] else {}),
                    medical_history=MedicalHistory(**json.loads(row[6]) if row[6] else {}),
                    family_history=FamilyHistory(**json.loads(row[7]) if row[7] else {}),
                    trauma_history=TraumaHistory(**json.loads(row[8]) if row[8] else {}),
                    social_history=SocialHistory(**json.loads(row[9]) if row[9] else {}),
                    treatment_history=TreatmentHistory(**json.loads(row[10]) if row[10] else {}),
                    mental_status_exam=MentalStatusExam(**json.loads(row[11]) if row[11] else {}),
                    risk_assessment=RiskAssessment(**json.loads(row[12]) if row[12] else {}),
                    clinical_impressions=json.loads(row[13]) if row[13] else [],
                    differential_diagnoses=json.loads(row[14]) if row[14] else [],
                    treatment_recommendations=json.loads(row[15]) if row[15] else [],
                    session_notes=row[16] or "",
                    clinician_observations=row[17] or "",
                    next_steps=json.loads(row[18]) if row[18] else []
                )
            return None
    
    def get_patient_assessments(self, patient_id: str) -> List[IntakeAssessmentResult]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT assessment_id FROM intake_assessments 
                WHERE patient_id = ? 
                ORDER BY assessment_date DESC
            """, (patient_id,))
            rows = cursor.fetchall()
            
            assessments = []
            for row in rows:
                assessment = self._get_assessment(row[0])
                if assessment:
                    assessments.append(assessment)
            
            return assessments
    
    def update_session_status(self, session_id: str, status: AssessmentStatus, notes: str = "") -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE intake_sessions 
                SET session_status = ?, clinician_observations = ?
                WHERE session_id = ?
            """, (status.value, notes, session_id))
            return cursor.rowcount > 0
    
    def complete_intake_assessment(self, assessment_id: str, clinical_summary: Dict[str, Any]) -> IntakeAssessmentResult:
        assessment = self._get_assessment(assessment_id)
        if not assessment:
            return None
        
        assessment.status = AssessmentStatus.COMPLETED
        assessment.clinical_impressions = clinical_summary.get('clinical_impressions', [])
        assessment.differential_diagnoses = clinical_summary.get('differential_diagnoses', [])
        assessment.treatment_recommendations = clinical_summary.get('treatment_recommendations', [])
        assessment.next_steps = clinical_summary.get('next_steps', [])
        
        self._save_intake_assessment(assessment)
        return assessment
    
    def get_crisis_indicators(self, assessment_id: str) -> List[str]:
        assessment = self._get_assessment(assessment_id)
        if not assessment:
            return []
        
        indicators = []
        
        if assessment.risk_assessment.suicide_risk in [RiskLevel.HIGH, RiskLevel.IMMINENT]:
            indicators.append("High suicide risk")
        
        if assessment.risk_assessment.violence_risk == RiskLevel.HIGH:
            indicators.append("Violence risk")
        
        if assessment.presenting_problem.severity_rating >= 9:
            indicators.append("Severe symptom presentation")
        
        if "psychotic" in assessment.mental_status_exam.thought_content.lower():
            indicators.append("Psychotic symptoms")
        
        if assessment.medical_history.substance_use:
            substance_data = assessment.medical_history.substance_use
            if substance_data.get('current_intoxication'):
                indicators.append("Substance intoxication")
        
        return indicators
    
    def generate_intake_report(self, assessment_id: str) -> Dict[str, Any]:
        assessment = self._get_assessment(assessment_id)
        if not assessment:
            return {}
        
        report = {
            "patient_id": assessment.patient_id,
            "assessment_date": assessment.assessment_date.strftime("%Y-%m-%d"),
            "assessment_status": assessment.status.value,
            
            "demographics": {
                "age": assessment.demographic_info.age,
                "gender": assessment.demographic_info.gender,
                "race_ethnicity": assessment.demographic_info.race_ethnicity,
                "education": assessment.demographic_info.education_level,
                "employment": assessment.demographic_info.employment_status
            },
            
            "presenting_concerns": {
                "chief_complaint": assessment.presenting_problem.chief_complaint,
                "severity": assessment.presenting_problem.severity_rating,
                "onset": assessment.presenting_problem.onset_timeline,
                "functional_impact": assessment.presenting_problem.impact_on_functioning
            },
            
            "risk_assessment": {
                "suicide_risk": assessment.risk_assessment.suicide_risk.value,
                "self_harm_risk": assessment.risk_assessment.self_harm_risk.value,
                "violence_risk": assessment.risk_assessment.violence_risk.value,
                "risk_factors": assessment.risk_assessment.risk_factors,
                "protective_factors": assessment.risk_assessment.protective_factors,
                "safety_plan_needed": assessment.risk_assessment.safety_plan_needed
            },
            
            "mental_status": {
                "appearance": assessment.mental_status_exam.appearance,
                "mood": assessment.mental_status_exam.mood,
                "affect": assessment.mental_status_exam.affect,
                "thought_process": assessment.mental_status_exam.thought_process,
                "insight": assessment.mental_status_exam.insight,
                "judgment": assessment.mental_status_exam.judgment
            },
            
            "clinical_summary": {
                "impressions": assessment.clinical_impressions,
                "diagnostic_considerations": assessment.differential_diagnoses,
                "treatment_recommendations": assessment.treatment_recommendations,
                "next_steps": assessment.next_steps
            },
            
            "strengths_resources": self._extract_strengths(assessment),
            "treatment_priorities": self._identify_treatment_priorities(assessment),
            "recommended_modalities": self._recommend_treatment_modalities(assessment)
        }
        
        return report
    
    def validate_assessment_completeness(self, assessment_id: str) -> Dict[str, Any]:
        assessment = self._get_assessment(assessment_id)
        if not assessment:
            return {"valid": False, "errors": ["Assessment not found"]}
        
        required_fields = {
            "presenting_problem": ["chief_complaint", "severity_rating"],
            "demographic_info": ["age", "gender"],
            "risk_assessment": ["suicide_risk", "self_harm_risk"],
            "mental_status_exam": ["mood", "affect", "thought_process"]
        }
        
        missing_fields = []
        
        for section, fields in required_fields.items():
            section_obj = getattr(assessment, section)
            for field in fields:
                value = getattr(section_obj, field, None)
                if not value or (isinstance(value, str) and not value.strip()):
                    missing_fields.append(f"{section}.{field}")
        
        validation_result = {
            "valid": len(missing_fields) == 0,
            "missing_fields": missing_fields,
            "completion_percentage": self._calculate_completion_percentage(assessment),
            "critical_sections_complete": self._check_critical_sections(assessment)
        }
        
        return validation_result
    
    def _calculate_completion_percentage(self, assessment: IntakeAssessmentResult) -> float:
        total_fields = 0
        completed_fields = 0
        
        sections = [
            assessment.demographic_info,
            assessment.presenting_problem,
            assessment.medical_history,
            assessment.family_history,
            assessment.social_history,
            assessment.treatment_history,
            assessment.mental_status_exam,
            assessment.risk_assessment
        ]
        
        for section in sections:
            for field_name, field_value in section.__dict__.items():
                total_fields += 1
                if field_value:
                    if isinstance(field_value, str) and field_value.strip():
                        completed_fields += 1
                    elif isinstance(field_value, (list, dict)) and field_value:
                        completed_fields += 1
                    elif isinstance(field_value, (int, float)) and field_value > 0:
                        completed_fields += 1
                    elif not isinstance(field_value, (str, list, dict, int, float)):
                        completed_fields += 1
        
        return (completed_fields / total_fields) * 100 if total_fields > 0 else 0
    
    def _check_critical_sections(self, assessment: IntakeAssessmentResult) -> Dict[str, bool]:
        return {
            "presenting_problem": bool(assessment.presenting_problem.chief_complaint),
            "risk_assessment": assessment.risk_assessment.suicide_risk != RiskLevel.UNKNOWN,
            "mental_status": bool(assessment.mental_status_exam.mood),
            "demographics": bool(assessment.demographic_info.age and assessment.demographic_info.gender)
        }
    
    def export_assessment_data(self, assessment_id: str, format_type: str = "json") -> Union[str, Dict[str, Any]]:
        assessment = self._get_assessment(assessment_id)
        if not assessment:
            return None
        
        if format_type == "json":
            return self.generate_intake_report(assessment_id)
        
        elif format_type == "clinical_summary":
            return self._generate_clinical_narrative(assessment)
        
        elif format_type == "treatment_plan":
            return self._generate_treatment_plan_template(assessment)
        
        return None
    
    def _generate_clinical_narrative(self, assessment: IntakeAssessmentResult) -> str:
        narrative_parts = []
        
        narrative_parts.append(f"CLINICAL INTAKE SUMMARY")
        narrative_parts.append(f"Date: {assessment.assessment_date.strftime('%Y-%m-%d')}")
        narrative_parts.append(f"Patient ID: {assessment.patient_id}")
        narrative_parts.append("")
        
        narrative_parts.append("PRESENTING CONCERNS:")
        narrative_parts.append(f"{assessment.presenting_problem.chief_complaint}")
        narrative_parts.append(f"Severity: {assessment.presenting_problem.severity_rating}/10")
        narrative_parts.append(f"Onset: {assessment.presenting_problem.onset_timeline}")
        narrative_parts.append("")
        
        narrative_parts.append("RISK ASSESSMENT:")
        narrative_parts.append(f"Suicide Risk: {assessment.risk_assessment.suicide_risk.value}")
        narrative_parts.append(f"Self-Harm Risk: {assessment.risk_assessment.self_harm_risk.value}")
        if assessment.risk_assessment.risk_factors:
            narrative_parts.append(f"Risk Factors: {', '.join(assessment.risk_assessment.risk_factors)}")
        if assessment.risk_assessment.protective_factors:
            narrative_parts.append(f"Protective Factors: {', '.join(assessment.risk_assessment.protective_factors)}")
        narrative_parts.append("")
        
        narrative_parts.append("MENTAL STATUS EXAMINATION:")
        narrative_parts.append(f"Mood: {assessment.mental_status_exam.mood}")
        narrative_parts.append(f"Affect: {assessment.mental_status_exam.affect}")
        narrative_parts.append(f"Thought Process: {assessment.mental_status_exam.thought_process}")
        narrative_parts.append(f"Insight: {assessment.mental_status_exam.insight}")
        narrative_parts.append(f"Judgment: {assessment.mental_status_exam.judgment}")
        narrative_parts.append("")
        
        if assessment.clinical_impressions:
            narrative_parts.append("CLINICAL IMPRESSIONS:")
            for impression in assessment.clinical_impressions:
                narrative_parts.append(f"• {impression}")
            narrative_parts.append("")
        
        if assessment.differential_diagnoses:
            narrative_parts.append("DIAGNOSTIC CONSIDERATIONS:")
            for diagnosis in assessment.differential_diagnoses:
                narrative_parts.append(f"• {diagnosis}")
            narrative_parts.append("")
        
        if assessment.treatment_recommendations:
            narrative_parts.append("TREATMENT RECOMMENDATIONS:")
            for recommendation in assessment.treatment_recommendations:
                narrative_parts.append(f"• {recommendation}")
        
        return "\n".join(narrative_parts)
    
    def _generate_treatment_plan_template(self, assessment: IntakeAssessmentResult) -> Dict[str, Any]:
        return {
            "patient_id": assessment.patient_id,
            "assessment_date": assessment.assessment_date.isoformat(),
            "treatment_goals": [
                {
                    "goal": "Safety and stabilization",
                    "priority": "High" if assessment.risk_assessment.suicide_risk in [RiskLevel.HIGH, RiskLevel.IMMINENT] else "Medium",
                    "target_date": "2 weeks",
                    "interventions": assessment.risk_assessment.immediate_interventions
                },
                {
                    "goal": "Symptom reduction",
                    "priority": "High" if assessment.presenting_problem.severity_rating >= 7 else "Medium",
                    "target_date": "8 weeks",
                    "interventions": self._recommend_interventions(assessment)
                },
                {
                    "goal": "Functional improvement",
                    "priority": "Medium",
                    "target_date": "12 weeks",
                    "interventions": ["Behavioral activation", "Skills training"]
                }
            ],
            "recommended_modalities": self._recommend_treatment_modalities(assessment),
            "session_frequency": "Weekly" if assessment.presenting_problem.severity_rating >= 6 else "Bi-weekly",
            "treatment_duration": "12-16 weeks initial phase",
            "crisis_plan": {
                "needed": assessment.risk_assessment.safety_plan_needed,
                "components": assessment.risk_assessment.immediate_interventions
            }
        }


class IntakeAssessmentWorkflow:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.intake_module = IntakeAssessmentModule(db_path)
        self.current_session = None
        self.current_assessment = None
    
    def initiate_intake(self, patient_id: str) -> Dict[str, Any]:
        self.current_session = self.intake_module.start_intake_assessment(patient_id)
        
        return {
            "session_id": self.current_session.session_id,
            "current_phase": self.current_session.current_phase.value,
            "next_steps": "Begin with demographic information and presenting concerns",
            "estimated_duration": "60-90 minutes",
            "crisis_protocol_active": False
        }
    
    def process_phase_responses(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        if not self.current_session:
            return {"error": "No active intake session"}
        
        crisis_indicators = self.intake_module.assess_crisis_indicators(responses)
        
        if crisis_indicators:
            return {
                "crisis_detected": True,
                "indicators": crisis_indicators,
                "immediate_actions": [
                    "Conduct immediate risk assessment",
                    "Ensure patient safety",
                    "Contact emergency services if needed",
                    "Document crisis indicators"
                ],
                "next_phase": IntakePhase.RISK_ASSESSMENT.value
            }
        
        current_phase = self.current_session.current_phase
        completed_phases = self.current_session.completed_phases.copy()
        
        if current_phase not in completed_phases:
            completed_phases.append(current_phase)
        
        next_phase = self._determine_next_phase(current_phase, completed_phases)
        
        return {
            "crisis_detected": False,
            "current_phase_complete": True,
            "next_phase": next_phase.value if next_phase else "COMPLETE",
            "completion_percentage": len(completed_phases) / len(IntakePhase) * 100,
            "remaining_phases": [phase.value for phase in IntakePhase if phase not in completed_phases]
        }
    
    def _determine_next_phase(self, current_phase: IntakePhase, completed_phases: List[IntakePhase]) -> Optional[IntakePhase]:
        phase_order = [
            IntakePhase.WELCOME_ORIENTATION,
            IntakePhase.PRESENTING_CONCERNS,
            IntakePhase.HISTORY_GATHERING,
            IntakePhase.PSYCHOSOCIAL_ASSESSMENT,
            IntakePhase.MENTAL_STATUS_EXAM,
            IntakePhase.RISK_ASSESSMENT,
            IntakePhase.TREATMENT_PLANNING,
            IntakePhase.WRAP_UP
        ]
        
        try:
            current_index = phase_order.index(current_phase)
            if current_index + 1 < len(phase_order):
                return phase_order[current_index + 1]
        except ValueError:
            pass
        
        return None
    
    def finalize_intake(self, final_notes: str = "") -> Dict[str, Any]:
        if not self.current_session:
            return {"error": "No active intake session"}
        
        assessment_id = f"assessment_{self.current_session.session_id}"
        
        clinical_summary = self.intake_module.generate_clinical_summary(assessment_id)
        completed_assessment = self.intake_module.complete_intake_assessment(assessment_id, clinical_summary)
        
        intake_report = self.intake_module.generate_intake_report(assessment_id)
        validation_result = self.intake_module.validate_assessment_completeness(assessment_id)
        
        self.current_session = None
        self.current_assessment = None
        
        return {
            "intake_complete": True,
            "assessment_id": assessment_id,
            "clinical_summary": clinical_summary,
            "validation": validation_result,
            "intake_report": intake_report,
            "next_steps": completed_assessment.next_steps if completed_assessment else []
        }
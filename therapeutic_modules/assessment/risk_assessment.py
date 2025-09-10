from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import sqlite3
import json
import uuid
from datetime import datetime, timedelta


class RiskType(Enum):
    SUICIDE_RISK = "suicide_risk"
    SELF_HARM_RISK = "self_harm_risk"
    HOMICIDE_RISK = "homicide_risk"
    VIOLENCE_RISK = "violence_risk"
    SUBSTANCE_ABUSE_RISK = "substance_abuse_risk"
    CHILD_ABUSE_RISK = "child_abuse_risk"
    ELDER_ABUSE_RISK = "elder_abuse_risk"
    DOMESTIC_VIOLENCE_RISK = "domestic_violence_risk"
    PSYCHOSIS_RISK = "psychosis_risk"
    MANIA_RISK = "mania_risk"
    EATING_DISORDER_RISK = "eating_disorder_risk"
    DISSOCIATION_RISK = "dissociation_risk"


class RiskLevel(Enum):
    MINIMAL = "minimal"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    IMMINENT = "imminent"
    CRITICAL = "critical"


class AssessmentPhase(Enum):
    SCREENING = "screening"
    DETAILED_ASSESSMENT = "detailed_assessment"
    SAFETY_PLANNING = "safety_planning"
    INTERVENTION = "intervention"
    MONITORING = "monitoring"
    FOLLOW_UP = "follow_up"


class ProtectiveFactor(Enum):
    SOCIAL_SUPPORT = "social_support"
    RELIGIOUS_BELIEFS = "religious_beliefs"
    FUTURE_GOALS = "future_goals"
    CHILDREN_DEPENDENTS = "children_dependents"
    THERAPEUTIC_RELATIONSHIP = "therapeutic_relationship"
    COPING_SKILLS = "coping_skills"
    TREATMENT_ENGAGEMENT = "treatment_engagement"
    HOPE_OPTIMISM = "hope_optimism"
    IMPULSE_CONTROL = "impulse_control"
    PROBLEM_SOLVING = "problem_solving"
    RESPONSIBILITY_OTHERS = "responsibility_others"
    MORAL_OBJECTIONS = "moral_objections"


class InterventionLevel(Enum):
    OUTPATIENT = "outpatient"
    INTENSIVE_OUTPATIENT = "intensive_outpatient"
    PARTIAL_HOSPITALIZATION = "partial_hospitalization"
    INPATIENT = "inpatient"
    CRISIS_INTERVENTION = "crisis_intervention"
    EMERGENCY_SERVICES = "emergency_services"


@dataclass
class RiskFactor:
    factor_id: str
    risk_type: RiskType
    factor_name: str
    description: str
    weight: int
    clinical_significance: str
    assessment_questions: List[str]
    evidence_indicators: List[str]


@dataclass
class SuicideRiskAssessment:
    assessment_id: str
    patient_id: str
    session_id: str
    assessment_date: datetime
    assessor: str
    ideation_present: bool = False
    ideation_frequency: str = ""
    ideation_intensity: int = 0
    plan_present: bool = False
    plan_specificity: str = ""
    plan_lethality: str = ""
    intent_present: bool = False
    intent_level: str = ""
    means_access: bool = False
    means_description: str = ""
    previous_attempts: List[Dict[str, Any]] = field(default_factory=list)
    rehearsal_behaviors: bool = False
    precipitating_factors: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    protective_factors: List[str] = field(default_factory=list)
    overall_risk_level: RiskLevel = RiskLevel.LOW
    confidence_level: int = 0
    clinical_notes: str = ""
    immediate_interventions: List[str] = field(default_factory=list)
    safety_plan_created: bool = False


@dataclass
class SelfHarmAssessment:
    assessment_id: str
    patient_id: str
    session_id: str
    assessment_date: datetime
    assessor: str
    current_urges: bool = False
    urge_intensity: int = 0
    methods_used: List[str] = field(default_factory=list)
    frequency: str = ""
    onset_age: Optional[int] = None
    triggers: List[str] = field(default_factory=list)
    functions_served: List[str] = field(default_factory=list)
    medical_complications: List[str] = field(default_factory=list)
    concealment_behaviors: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    protective_factors: List[str] = field(default_factory=list)
    overall_risk_level: RiskLevel = RiskLevel.LOW
    suicide_risk_connection: bool = False
    immediate_interventions: List[str] = field(default_factory=list)
    safety_strategies: List[str] = field(default_factory=list)


@dataclass
class ViolenceRiskAssessment:
    assessment_id: str
    patient_id: str
    session_id: str
    assessment_date: datetime
    assessor: str
    homicidal_ideation: bool = False
    specific_targets: List[str] = field(default_factory=list)
    threat_specificity: str = ""
    violence_history: List[Dict[str, Any]] = field(default_factory=list)
    weapon_access: bool = False
    weapon_types: List[str] = field(default_factory=list)
    impulse_control: str = ""
    substance_use_factor: bool = False
    paranoid_ideation: bool = False
    command_hallucinations: bool = False
    risk_factors: List[str] = field(default_factory=list)
    protective_factors: List[str] = field(default_factory=list)
    overall_risk_level: RiskLevel = RiskLevel.LOW
    duty_to_warn_triggered: bool = False
    law_enforcement_contacted: bool = False
    immediate_interventions: List[str] = field(default_factory=list)


@dataclass
class ComprehensiveRiskAssessment:
    assessment_id: str
    patient_id: str
    session_id: str
    assessment_date: datetime
    assessor: str
    suicide_assessment: Optional[SuicideRiskAssessment] = None
    self_harm_assessment: Optional[SelfHarmAssessment] = None
    violence_assessment: Optional[ViolenceRiskAssessment] = None
    substance_risk_level: RiskLevel = RiskLevel.LOW
    psychosis_risk_level: RiskLevel = RiskLevel.LOW
    overall_risk_profile: Dict[RiskType, RiskLevel] = field(default_factory=dict)
    global_risk_level: RiskLevel = RiskLevel.LOW
    intervention_level: InterventionLevel = InterventionLevel.OUTPATIENT
    safety_plan_elements: List[str] = field(default_factory=list)
    follow_up_schedule: str = ""
    crisis_contacts: List[Dict[str, str]] = field(default_factory=list)
    clinical_summary: str = ""
    recommendations: List[str] = field(default_factory=list)


@dataclass
class SafetyPlan:
    plan_id: str
    patient_id: str
    created_date: datetime
    created_by: str
    risk_types_addressed: List[RiskType]
    warning_signs: List[str] = field(default_factory=list)
    internal_coping_strategies: List[str] = field(default_factory=list)
    social_contacts: List[Dict[str, str]] = field(default_factory=list)
    professional_contacts: List[Dict[str, str]] = field(default_factory=list)
    environmental_safety_steps: List[str] = field(default_factory=list)
    reasons_for_living: List[str] = field(default_factory=list)
    patient_commitment: str = ""
    review_date: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=30))
    plan_status: str = "active"
    effectiveness_rating: Optional[int] = None


class RiskAssessmentModule:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.risk_factors = self._initialize_risk_factors()
        self.protective_factors = self._initialize_protective_factors()
        self.assessment_protocols = self._initialize_assessment_protocols()
        self.intervention_guidelines = self._initialize_intervention_guidelines()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS suicide_risk_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    assessment_date TEXT NOT NULL,
                    assessor TEXT NOT NULL,
                    ideation_present BOOLEAN,
                    ideation_frequency TEXT,
                    ideation_intensity INTEGER,
                    plan_present BOOLEAN,
                    plan_specificity TEXT,
                    plan_lethality TEXT,
                    intent_present BOOLEAN,
                    intent_level TEXT,
                    means_access BOOLEAN,
                    means_description TEXT,
                    previous_attempts TEXT,
                    rehearsal_behaviors BOOLEAN,
                    precipitating_factors TEXT,
                    risk_factors TEXT,
                    protective_factors TEXT,
                    overall_risk_level TEXT,
                    confidence_level INTEGER,
                    clinical_notes TEXT,
                    immediate_interventions TEXT,
                    safety_plan_created BOOLEAN,
                    created_date TEXT,
                    last_updated TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS self_harm_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    assessment_date TEXT NOT NULL,
                    assessor TEXT NOT NULL,
                    current_urges BOOLEAN,
                    urge_intensity INTEGER,
                    methods_used TEXT,
                    frequency TEXT,
                    onset_age INTEGER,
                    triggers TEXT,
                    functions_served TEXT,
                    medical_complications TEXT,
                    concealment_behaviors TEXT,
                    risk_factors TEXT,
                    protective_factors TEXT,
                    overall_risk_level TEXT,
                    suicide_risk_connection BOOLEAN,
                    immediate_interventions TEXT,
                    safety_strategies TEXT,
                    created_date TEXT,
                    last_updated TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS violence_risk_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    assessment_date TEXT NOT NULL,
                    assessor TEXT NOT NULL,
                    homicidal_ideation BOOLEAN,
                    specific_targets TEXT,
                    threat_specificity TEXT,
                    violence_history TEXT,
                    weapon_access BOOLEAN,
                    weapon_types TEXT,
                    impulse_control TEXT,
                    substance_use_factor BOOLEAN,
                    paranoid_ideation BOOLEAN,
                    command_hallucinations BOOLEAN,
                    risk_factors TEXT,
                    protective_factors TEXT,
                    overall_risk_level TEXT,
                    duty_to_warn_triggered BOOLEAN,
                    law_enforcement_contacted BOOLEAN,
                    immediate_interventions TEXT,
                    created_date TEXT,
                    last_updated TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS comprehensive_risk_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    assessment_date TEXT NOT NULL,
                    assessor TEXT NOT NULL,
                    suicide_assessment_id TEXT,
                    self_harm_assessment_id TEXT,
                    violence_assessment_id TEXT,
                    substance_risk_level TEXT,
                    psychosis_risk_level TEXT,
                    overall_risk_profile TEXT,
                    global_risk_level TEXT,
                    intervention_level TEXT,
                    safety_plan_elements TEXT,
                    follow_up_schedule TEXT,
                    crisis_contacts TEXT,
                    clinical_summary TEXT,
                    recommendations TEXT,
                    created_date TEXT,
                    last_updated TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS safety_plans (
                    plan_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    created_by TEXT NOT NULL,
                    risk_types_addressed TEXT,
                    warning_signs TEXT,
                    internal_coping_strategies TEXT,
                    social_contacts TEXT,
                    professional_contacts TEXT,
                    environmental_safety_steps TEXT,
                    reasons_for_living TEXT,
                    patient_commitment TEXT,
                    review_date TEXT,
                    plan_status TEXT,
                    effectiveness_rating INTEGER,
                    last_updated TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS risk_incidents (
                    incident_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    incident_date TEXT NOT NULL,
                    incident_type TEXT NOT NULL,
                    severity_level TEXT,
                    description TEXT,
                    precipitating_factors TEXT,
                    interventions_used TEXT,
                    outcome TEXT,
                    lessons_learned TEXT,
                    safety_plan_updated BOOLEAN,
                    reported_to_authorities BOOLEAN,
                    follow_up_actions TEXT,
                    documented_by TEXT,
                    created_date TEXT
                )
            """)
    
    def _initialize_risk_factors(self) -> Dict[RiskType, List[RiskFactor]]:
        factors = {}
        
        factors[RiskType.SUICIDE_RISK] = [
            RiskFactor(
                factor_id="suicide_previous_attempt",
                risk_type=RiskType.SUICIDE_RISK,
                factor_name="Previous Suicide Attempt",
                description="History of previous suicide attempts",
                weight=5,
                clinical_significance="critical",
                assessment_questions=[
                    "Have you ever tried to hurt yourself or end your life before?",
                    "When was your most recent attempt?",
                    "What method did you use?",
                    "What stopped you or led to your survival?"
                ],
                evidence_indicators=["Scars", "Medical records", "Hospital admissions", "Patient report"]
            ),
            RiskFactor(
                factor_id="suicide_current_ideation",
                risk_type=RiskType.SUICIDE_RISK,
                factor_name="Current Suicidal Ideation",
                description="Active thoughts of suicide",
                weight=4,
                clinical_significance="critical",
                assessment_questions=[
                    "Are you having thoughts of hurting yourself or ending your life?",
                    "How often do these thoughts occur?",
                    "How intense are these thoughts on a scale of 1-10?",
                    "What triggers these thoughts?"
                ],
                evidence_indicators=["Patient verbal report", "Behavioral indicators", "Written materials"]
            ),
            RiskFactor(
                factor_id="suicide_plan_method",
                risk_type=RiskType.SUICIDE_RISK,
                factor_name="Specific Plan and Method",
                description="Detailed plan for suicide with specific method",
                weight=5,
                clinical_significance="critical",
                assessment_questions=[
                    "Have you thought about how you would hurt yourself?",
                    "Do you have a specific plan?",
                    "How detailed is your plan?",
                    "When would you carry out this plan?"
                ],
                evidence_indicators=["Detailed planning", "Method specification", "Timeline", "Preparation behaviors"]
            ),
            RiskFactor(
                factor_id="suicide_means_access",
                risk_type=RiskType.SUICIDE_RISK,
                factor_name="Access to Means",
                description="Access to lethal means for suicide",
                weight=4,
                clinical_significance="critical",
                assessment_questions=[
                    "Do you have access to the means to hurt yourself?",
                    "Are there firearms in your home?",
                    "Do you have access to medications?",
                    "Are there other dangerous items available to you?"
                ],
                evidence_indicators=["Weapon ownership", "Medication stockpiling", "Environmental hazards"]
            )
        ]
        
        factors[RiskType.SELF_HARM_RISK] = [
            RiskFactor(
                factor_id="self_harm_current_urges",
                risk_type=RiskType.SELF_HARM_RISK,
                factor_name="Current Self-Harm Urges",
                description="Active urges to engage in self-harm",
                weight=3,
                clinical_significance="high",
                assessment_questions=[
                    "Are you having urges to hurt yourself right now?",
                    "How strong are these urges?",
                    "What makes the urges stronger or weaker?",
                    "How do you usually cope with these urges?"
                ],
                evidence_indicators=["Patient report", "Behavioral agitation", "Physical signs"]
            ),
            RiskFactor(
                factor_id="self_harm_history",
                risk_type=RiskType.SELF_HARM_RISK,
                factor_name="History of Self-Harm",
                description="Previous episodes of deliberate self-harm",
                weight=3,
                clinical_significance="high",
                assessment_questions=[
                    "Have you hurt yourself on purpose before?",
                    "What methods have you used?",
                    "When did you first start hurting yourself?",
                    "How often do you engage in self-harm?"
                ],
                evidence_indicators=["Scars", "Medical records", "Patient disclosure"]
            )
        ]
        
        factors[RiskType.VIOLENCE_RISK] = [
            RiskFactor(
                factor_id="violence_homicidal_ideation",
                risk_type=RiskType.VIOLENCE_RISK,
                factor_name="Homicidal Ideation",
                description="Thoughts of harming or killing others",
                weight=5,
                clinical_significance="critical",
                assessment_questions=[
                    "Are you having thoughts of hurting someone else?",
                    "Who are you thinking of hurting?",
                    "How specific are these thoughts?",
                    "Have you made any threats?"
                ],
                evidence_indicators=["Patient report", "Threats made", "Behavioral indicators"]
            ),
            RiskFactor(
                factor_id="violence_history",
                risk_type=RiskType.VIOLENCE_RISK,
                factor_name="History of Violence",
                description="Previous acts of violence or aggression",
                weight=4,
                clinical_significance="critical",
                assessment_questions=[
                    "Have you ever hurt someone else physically?",
                    "Have you been in physical fights?",
                    "Have you ever threatened someone?",
                    "Have you been arrested for violent behavior?"
                ],
                evidence_indicators=["Criminal record", "Medical reports", "Witness accounts"]
            )
        ]
        
        return factors
    
    def _initialize_protective_factors(self) -> Dict[ProtectiveFactor, Dict[str, Any]]:
        return {
            ProtectiveFactor.SOCIAL_SUPPORT: {
                "name": "Strong Social Support",
                "description": "Meaningful relationships and social connections",
                "assessment_questions": [
                    "Who are the important people in your life?",
                    "Who can you talk to when you're struggling?",
                    "Do you feel supported by family and friends?",
                    "Who would you reach out to in a crisis?"
                ],
                "indicators": ["Regular social contact", "Emotional support", "Practical assistance"],
                "strength_weight": 3
            },
            ProtectiveFactor.RELIGIOUS_BELIEFS: {
                "name": "Religious or Spiritual Beliefs",
                "description": "Strong religious or spiritual convictions",
                "assessment_questions": [
                    "Do you have religious or spiritual beliefs?",
                    "How important are these beliefs to you?",
                    "Do your beliefs provide comfort during difficult times?",
                    "Are you connected to a religious community?"
                ],
                "indicators": ["Regular worship", "Prayer/meditation", "Religious community"],
                "strength_weight": 2
            },
            ProtectiveFactor.FUTURE_GOALS: {
                "name": "Future Goals and Plans",
                "description": "Meaningful future goals and aspirations",
                "assessment_questions": [
                    "What are your goals for the future?",
                    "What are you looking forward to?",
                    "What gives your life meaning and purpose?",
                    "What would you like to accomplish?"
                ],
                "indicators": ["Specific goals", "Motivation", "Sense of purpose"],
                "strength_weight": 2
            },
            ProtectiveFactor.CHILDREN_DEPENDENTS: {
                "name": "Responsibility for Others",
                "description": "Responsibility for children or dependents",
                "assessment_questions": [
                    "Do you have children or others who depend on you?",
                    "How important is your role as a caregiver?",
                    "Who would take care of them if something happened to you?",
                    "How does this responsibility affect your thoughts?"
                ],
                "indicators": ["Active caregiving", "Strong bonds", "Sense of responsibility"],
                "strength_weight": 4
            }
        }
    
    def _initialize_assessment_protocols(self) -> Dict[RiskType, Dict[str, Any]]:
        return {
            RiskType.SUICIDE_RISK: {
                "screening_questions": [
                    "Are you having thoughts of hurting yourself or ending your life?",
                    "Have you had thoughts that you would be better off dead?",
                    "Have you ever tried to hurt yourself before?"
                ],
                "detailed_questions": [
                    "How often do you have these thoughts?",
                    "How intense are these thoughts?",
                    "Do you have a plan for how you would hurt yourself?",
                    "Do you have access to means to carry out a plan?",
                    "What has stopped you from acting on these thoughts?",
                    "What makes these thoughts better or worse?"
                ],
                "risk_calculation": {
                    "ideation": 2,
                    "plan": 3,
                    "means": 2,
                    "intent": 3,
                    "previous_attempt": 4,
                    "protective_factors": -2
                }
            },
            RiskType.SELF_HARM_RISK: {
                "screening_questions": [
                    "Have you ever hurt yourself on purpose?",
                    "Are you having urges to hurt yourself now?",
                    "Do you have scars or marks from hurting yourself?"
                ],
                "detailed_questions": [
                    "What methods have you used to hurt yourself?",
                    "How often do you engage in self-harm?",
                    "What triggers these behaviors?",
                    "How do you feel before, during, and after?",
                    "What purpose does self-harm serve for you?",
                    "Have you ever accidentally hurt yourself more than intended?"
                ]
            },
            RiskType.VIOLENCE_RISK: {
                "screening_questions": [
                    "Are you having thoughts of hurting someone else?",
                    "Have you threatened anyone recently?",
                    "Have you been in fights or violent situations?"
                ],
                "detailed_questions": [
                    "Who are you thinking of hurting?",
                    "How specific are these thoughts?",
                    "Do you have access to weapons?",
                    "What would trigger you to act on these thoughts?",
                    "Have you hurt others in the past?",
                    "Are you using substances that affect your judgment?"
                ]
            }
        }
    
    def _initialize_intervention_guidelines(self) -> Dict[RiskLevel, Dict[str, Any]]:
        return {
            RiskLevel.LOW: {
                "monitoring_frequency": "routine",
                "intervention_level": InterventionLevel.OUTPATIENT,
                "safety_planning": "basic",
                "immediate_actions": [
                    "Document assessment",
                    "Provide crisis resources",
                    "Schedule follow-up"
                ],
                "follow_up_timeframe": "1-2 weeks"
            },
            RiskLevel.MODERATE: {
                "monitoring_frequency": "increased",
                "intervention_level": InterventionLevel.INTENSIVE_OUTPATIENT,
                "safety_planning": "detailed",
                "immediate_actions": [
                    "Create safety plan",
                    "Remove means if possible",
                    "Increase session frequency",
                    "Involve support system",
                    "Provide crisis contacts"
                ],
                "follow_up_timeframe": "2-3 days"
            },
            RiskLevel.HIGH: {
                "monitoring_frequency": "intensive",
                "intervention_level": InterventionLevel.PARTIAL_HOSPITALIZATION,
                "safety_planning": "comprehensive",
                "immediate_actions": [
                    "Comprehensive safety plan",
                    "Remove all means",
                    "24/7 supervision consideration",
                    "Crisis team involvement",
                    "Possible hospitalization",
                    "Daily contact"
                ],
                "follow_up_timeframe": "24 hours"
            },
            RiskLevel.IMMINENT: {
                "monitoring_frequency": "continuous",
                "intervention_level": InterventionLevel.INPATIENT,
                "safety_planning": "crisis_intervention",
                "immediate_actions": [
                    "Immediate psychiatric evaluation",
                    "Involuntary hold if necessary",
                    "Emergency services activation",
                    "Continuous supervision",
                    "Family notification",
                    "Legal consultation"
                ],
                "follow_up_timeframe": "immediate"
            }
        }
    
    def conduct_suicide_risk_assessment(self, patient_id: str, session_id: str, 
                                      assessor: str, responses: Dict[str, Any]) -> SuicideRiskAssessment:
        assessment_id = str(uuid.uuid4())
        
        assessment = SuicideRiskAssessment(
            assessment_id=assessment_id,
            patient_id=patient_id,
            session_id=session_id,
            assessment_date=datetime.now(),
            assessor=assessor
        )
        
        # Process responses
        assessment.ideation_present = responses.get("ideation_present", False)
        assessment.ideation_frequency = responses.get("ideation_frequency", "")
        assessment.ideation_intensity = responses.get("ideation_intensity", 0)
        assessment.plan_present = responses.get("plan_present", False)
        assessment.plan_specificity = responses.get("plan_specificity", "")
        assessment.plan_lethality = responses.get("plan_lethality", "")
        assessment.intent_present = responses.get("intent_present", False)
        assessment.intent_level = responses.get("intent_level", "")
        assessment.means_access = responses.get("means_access", False)
        assessment.means_description = responses.get("means_description", "")
        assessment.previous_attempts = responses.get("previous_attempts", [])
        assessment.rehearsal_behaviors = responses.get("rehearsal_behaviors", False)
        assessment.precipitating_factors = responses.get("precipitating_factors", [])
        assessment.risk_factors = responses.get("risk_factors", [])
        assessment.protective_factors = responses.get("protective_factors", [])
        
        # Calculate risk level
        assessment.overall_risk_level = self._calculate_suicide_risk_level(assessment)
        assessment.confidence_level = responses.get("confidence_level", 8)
        assessment.clinical_notes = responses.get("clinical_notes", "")
        
        # Determine interventions
        assessment.immediate_interventions = self._determine_suicide_interventions(assessment)
        assessment.safety_plan_created = assessment.overall_risk_level in [RiskLevel.MODERATE, RiskLevel.HIGH, RiskLevel.IMMINENT]
        
        self._save_suicide_assessment(assessment)
        return assessment
    
    def conduct_self_harm_assessment(self, patient_id: str, session_id: str,
                                   assessor: str, responses: Dict[str, Any]) -> SelfHarmAssessment:
        assessment_id = str(uuid.uuid4())
        
        assessment = SelfHarmAssessment(
            assessment_id=assessment_id,
            patient_id=patient_id,
            session_id=session_id,
            assessment_date=datetime.now(),
            assessor=assessor
        )
        
        # Process responses
        assessment.current_urges = responses.get("current_urges", False)
        assessment.urge_intensity = responses.get("urge_intensity", 0)
        assessment.methods_used = responses.get("methods_used", [])
        assessment.frequency = responses.get("frequency", "")
        assessment.onset_age = responses.get("onset_age")
        assessment.triggers = responses.get("triggers", [])
        assessment.functions_served = responses.get("functions_served", [])
        assessment.medical_complications = responses.get("medical_complications", [])
        assessment.concealment_behaviors = responses.get("concealment_behaviors", [])
        assessment.risk_factors = responses.get("risk_factors", [])
        assessment.protective_factors = responses.get("protective_factors", [])
        assessment.suicide_risk_connection = responses.get("suicide_risk_connection", False)
        
        # Calculate risk level
        assessment.overall_risk_level = self._calculate_self_harm_risk_level(assessment)
        
        # Determine interventions
        assessment.immediate_interventions = self._determine_self_harm_interventions(assessment)
        assessment.safety_strategies = self._generate_self_harm_safety_strategies(assessment)
        
        self._save_self_harm_assessment(assessment)
        return assessment
    
    def conduct_violence_risk_assessment(self, patient_id: str, session_id: str,
                                        assessor: str, responses: Dict[str, Any]) -> ViolenceRiskAssessment:
        assessment_id = str(uuid.uuid4())
        
        assessment = ViolenceRiskAssessment(
            assessment_id=assessment_id,
            patient_id=patient_id,
            session_id=session_id,
            assessment_date=datetime.now(),
            assessor=assessor
        )
        
        # Process responses
        assessment.homicidal_ideation = responses.get("homicidal_ideation", False)
        assessment.specific_targets = responses.get("specific_targets", [])
        assessment.threat_specificity = responses.get("threat_specificity", "")
        assessment.violence_history = responses.get("violence_history", [])
        assessment.weapon_access = responses.get("weapon_access", False)
        assessment.weapon_types = responses.get("weapon_types", [])
        assessment.impulse_control = responses.get("impulse_control", "")
        assessment.substance_use_factor = responses.get("substance_use_factor", False)
        assessment.paranoid_ideation = responses.get("paranoid_ideation", False)
        assessment.command_hallucinations = responses.get("command_hallucinations", False)
        assessment.risk_factors = responses.get("risk_factors", [])
        assessment.protective_factors = responses.get("protective_factors", [])
        
        # Calculate risk level
        assessment.overall_risk_level = self._calculate_violence_risk_level(assessment)
        
        # Determine duty to warn
        assessment.duty_to_warn_triggered = self._assess_duty_to_warn(assessment)
        
        # Determine interventions
        assessment.immediate_interventions = self._determine_violence_interventions(assessment)
        
        self._save_violence_assessment(assessment)
        return assessment
    
    def conduct_comprehensive_risk_assessment(self, patient_id: str, session_id: str,
                                            assessor: str, assessment_data: Dict[str, Any]) -> ComprehensiveRiskAssessment:
        assessment_id = str(uuid.uuid4())
        
        comprehensive = ComprehensiveRiskAssessment(
            assessment_id=assessment_id,
            patient_id=patient_id,
            session_id=session_id,
            assessment_date=datetime.now(),
            assessor=assessor
        )
        
        # Conduct individual assessments if data provided
        if assessment_data.get("suicide_data"):
            comprehensive.suicide_assessment = self.conduct_suicide_risk_assessment(
                patient_id, session_id, assessor, assessment_data["suicide_data"]
            )
        
        if assessment_data.get("self_harm_data"):
            comprehensive.self_harm_assessment = self.conduct_self_harm_assessment(
                patient_id, session_id, assessor, assessment_data["self_harm_data"]
            )
        
        if assessment_data.get("violence_data"):
            comprehensive.violence_assessment = self.conduct_violence_risk_assessment(
                patient_id, session_id, assessor, assessment_data["violence_data"]
            )
        
        # Assess other risk types
        comprehensive.substance_risk_level = self._assess_substance_risk(assessment_data.get("substance_data", {}))
        comprehensive.psychosis_risk_level = self._assess_psychosis_risk(assessment_data.get("psychosis_data", {}))
        
        # Create overall risk profile
        comprehensive.overall_risk_profile = self._create_risk_profile(comprehensive)
        comprehensive.global_risk_level = self._determine_global_risk_level(comprehensive)
        comprehensive.intervention_level = self._determine_intervention_level(comprehensive)
        
        # Generate recommendations
        comprehensive.recommendations = self._generate_risk_recommendations(comprehensive)
        comprehensive.clinical_summary = self._generate_clinical_summary(comprehensive)
        comprehensive.follow_up_schedule = self._determine_follow_up_schedule(comprehensive)
        
        # Set up crisis contacts
        comprehensive.crisis_contacts = self._setup_crisis_contacts(assessment_data.get("contacts", []))
        
        self._save_comprehensive_assessment(comprehensive)
        return comprehensive
    
    def create_safety_plan(self, patient_id: str, created_by: str, 
                          risk_types: List[RiskType], plan_data: Dict[str, Any]) -> SafetyPlan:
        plan_id = str(uuid.uuid4())
        
        safety_plan = SafetyPlan(
            plan_id=plan_id,
            patient_id=patient_id,
            created_date=datetime.now(),
            created_by=created_by,
            risk_types_addressed=risk_types
        )
        
        # Populate plan elements
        safety_plan.warning_signs = plan_data.get("warning_signs", [])
        safety_plan.internal_coping_strategies = plan_data.get("internal_coping", [])
        safety_plan.social_contacts = plan_data.get("social_contacts", [])
        safety_plan.professional_contacts = plan_data.get("professional_contacts", [])
        safety_plan.environmental_safety_steps = plan_data.get("environmental_safety", [])
        safety_plan.reasons_for_living = plan_data.get("reasons_for_living", [])
        safety_plan.patient_commitment = plan_data.get("patient_commitment", "")
        
        # Set review date
        review_days = 30 if any(rt in [RiskType.SUICIDE_RISK, RiskType.VIOLENCE_RISK] for rt in risk_types) else 90
        safety_plan.review_date = datetime.now() + timedelta(days=review_days)
        
        self._save_safety_plan(safety_plan)
        return safety_plan
    
    def _calculate_suicide_risk_level(self, assessment: SuicideRiskAssessment) -> RiskLevel:
        risk_score = 0
        
        # Core risk factors
        if assessment.ideation_present:
            risk_score += 2
            if assessment.ideation_intensity >= 7:
                risk_score += 2
        
        if assessment.plan_present:
            risk_score += 3
            if assessment.plan_specificity in ["detailed", "specific"]:
                risk_score += 2
            if assessment.plan_lethality in ["high", "lethal"]:
                risk_score += 2
        
        if assessment.intent_present:
            risk_score += 3
            if assessment.intent_level in ["strong", "definite"]:
                risk_score += 2
        
        if assessment.means_access:
            risk_score += 2
        
        if assessment.previous_attempts:
            risk_score += 3
            if len(assessment.previous_attempts) > 1:
                risk_score += 1
        
        if assessment.rehearsal_behaviors:
            risk_score += 2
        
        # Adjust for protective factors
        protective_adjustment = max(0, len(assessment.protective_factors) - 2)
        risk_score = max(0, risk_score - protective_adjustment)
        
        # Determine risk level
        if risk_score >= 12:
            return RiskLevel.IMMINENT
        elif risk_score >= 9:
            return RiskLevel.HIGH
        elif risk_score >= 6:
            return RiskLevel.MODERATE
        elif risk_score >= 3:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL
    
    def _calculate_self_harm_risk_level(self, assessment: SelfHarmAssessment) -> RiskLevel:
        risk_score = 0
        
        if assessment.current_urges:
            risk_score += 2
            if assessment.urge_intensity >= 7:
                risk_score += 2
        
        if assessment.methods_used:
            risk_score += 1
            if any(method in ["cutting", "burning", "hitting"] for method in assessment.methods_used):
                risk_score += 1
        
        if assessment.frequency in ["daily", "multiple_times_daily"]:
            risk_score += 2
        elif assessment.frequency in ["weekly", "multiple_times_weekly"]:
            risk_score += 1
        
        if assessment.medical_complications:
            risk_score += 2
        
        if assessment.suicide_risk_connection:
            risk_score += 3
        
        # Protective factors adjustment
        protective_adjustment = len(assessment.protective_factors)
        risk_score = max(0, risk_score - protective_adjustment)
        
        if risk_score >= 8:
            return RiskLevel.HIGH
        elif risk_score >= 5:
            return RiskLevel.MODERATE
        elif risk_score >= 2:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL
    
    def _calculate_violence_risk_level(self, assessment: ViolenceRiskAssessment) -> RiskLevel:
        risk_score = 0
        
        if assessment.homicidal_ideation:
            risk_score += 3
            if assessment.specific_targets:
                risk_score += 2
            if assessment.threat_specificity in ["detailed", "specific"]:
                risk_score += 2
        
        if assessment.violence_history:
            risk_score += 2
            recent_violence = any(
                incident.get("date", "") and 
                (datetime.now() - datetime.fromisoformat(incident["date"])).days < 365
                for incident in assessment.violence_history
            )
            if recent_violence:
                risk_score += 2
        
        if assessment.weapon_access:
            risk_score += 2
            if "firearm" in assessment.weapon_types:
                risk_score += 1
        
        if assessment.impulse_control in ["poor", "very_poor"]:
            risk_score += 2
        
        if assessment.substance_use_factor:
            risk_score += 1
        
        if assessment.paranoid_ideation:
            risk_score += 2
        
        if assessment.command_hallucinations:
            risk_score += 3
        
        # Protective factors adjustment
        protective_adjustment = len(assessment.protective_factors)
        risk_score = max(0, risk_score - protective_adjustment)
        
        if risk_score >= 12:
            return RiskLevel.IMMINENT
        elif risk_score >= 9:
            return RiskLevel.HIGH
        elif risk_score >= 6:
            return RiskLevel.MODERATE
        elif risk_score >= 3:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL
    
    def _assess_duty_to_warn(self, assessment: ViolenceRiskAssessment) -> bool:
        # Tarasoff criteria: specific threat to identifiable victim
        return (
            assessment.homicidal_ideation and
            assessment.specific_targets and
            assessment.threat_specificity in ["detailed", "specific"] and
            assessment.overall_risk_level in [RiskLevel.HIGH, RiskLevel.IMMINENT]
        )
    
    def _determine_suicide_interventions(self, assessment: SuicideRiskAssessment) -> List[str]:
        interventions = []
        
        if assessment.overall_risk_level == RiskLevel.IMMINENT:
            interventions.extend([
                "Immediate psychiatric evaluation",
                "Consider involuntary hold",
                "Continuous supervision",
                "Remove all means of self-harm",
                "Emergency services consultation",
                "Family/support system notification"
            ])
        elif assessment.overall_risk_level == RiskLevel.HIGH:
            interventions.extend([
                "Comprehensive safety planning",
                "Increased session frequency",
                "Remove means of self-harm",
                "24/7 crisis support",
                "Consider hospitalization",
                "Daily safety check-ins"
            ])
        elif assessment.overall_risk_level == RiskLevel.MODERATE:
            interventions.extend([
                "Create safety plan",
                "Increase monitoring",
                "Crisis resources provided",
                "Support system involvement",
                "Weekly safety assessments"
            ])
        else:
            interventions.extend([
                "Standard safety planning",
                "Crisis resources",
                "Regular monitoring",
                "Protective factor enhancement"
            ])
        
        return interventions
    
    def _determine_self_harm_interventions(self, assessment: SelfHarmAssessment) -> List[str]:
        interventions = []
        
        if assessment.overall_risk_level == RiskLevel.HIGH:
            interventions.extend([
                "Remove self-harm tools",
                "Intensive coping skills training",
                "Frequent check-ins",
                "Medical evaluation for complications",
                "Crisis intervention plan"
            ])
        elif assessment.overall_risk_level == RiskLevel.MODERATE:
            interventions.extend([
                "Safety planning for urges",
                "Alternative coping strategies",
                "Regular monitoring",
                "Address underlying triggers"
            ])
        else:
            interventions.extend([
                "Psychoeducation about self-harm",
                "Coping skills development",
                "Regular assessment"
            ])
        
        return interventions
    
    def _determine_violence_interventions(self, assessment: ViolenceRiskAssessment) -> List[str]:
        interventions = []
        
        if assessment.duty_to_warn_triggered:
            interventions.extend([
                "Duty to warn procedures",
                "Contact potential victims",
                "Law enforcement notification",
                "Legal consultation"
            ])
        
        if assessment.overall_risk_level == RiskLevel.IMMINENT:
            interventions.extend([
                "Immediate psychiatric evaluation",
                "Consider involuntary hold",
                "Remove weapon access",
                "Law enforcement involvement",
                "Victim protection measures"
            ])
        elif assessment.overall_risk_level == RiskLevel.HIGH:
            interventions.extend([
                "Intensive monitoring",
                "Anger management referral",
                "Substance abuse treatment if needed",
                "Remove weapon access",
                "Safety planning"
            ])
        
        return interventions
    
    def _generate_self_harm_safety_strategies(self, assessment: SelfHarmAssessment) -> List[str]:
        strategies = [
            "Hold ice cubes instead of cutting",
            "Draw on skin with red marker",
            "Exercise vigorously",
            "Squeeze a stress ball",
            "Listen to loud music",
            "Take a cold shower",
            "Call crisis hotline",
            "Practice deep breathing"
        ]
        
        # Customize based on methods used
        if "cutting" in assessment.methods_used:
            strategies.extend([
                "Use rubber band snapping",
                "Draw cutting motions without tool"
            ])
        
        if "burning" in assessment.methods_used:
            strategies.extend([
                "Hold ice instead of heat source",
                "Use mentholated rub for sensation"
            ])
        
        return strategies[:8]  # Return top 8 strategies
    
    def _assess_substance_risk(self, substance_data: Dict[str, Any]) -> RiskLevel:
        if not substance_data:
            return RiskLevel.LOW
        
        risk_indicators = 0
        
        if substance_data.get("daily_use"):
            risk_indicators += 2
        if substance_data.get("withdrawal_symptoms"):
            risk_indicators += 2
        if substance_data.get("impaired_judgment"):
            risk_indicators += 1
        if substance_data.get("dangerous_combinations"):
            risk_indicators += 2
        if substance_data.get("overdose_history"):
            risk_indicators += 3
        
        if risk_indicators >= 6:
            return RiskLevel.HIGH
        elif risk_indicators >= 4:
            return RiskLevel.MODERATE
        elif risk_indicators >= 2:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL
    
    def _assess_psychosis_risk(self, psychosis_data: Dict[str, Any]) -> RiskLevel:
        if not psychosis_data:
            return RiskLevel.LOW
        
        risk_indicators = 0
        
        if psychosis_data.get("active_hallucinations"):
            risk_indicators += 2
        if psychosis_data.get("command_hallucinations"):
            risk_indicators += 3
        if psychosis_data.get("paranoid_delusions"):
            risk_indicators += 2
        if psychosis_data.get("disorganized_thinking"):
            risk_indicators += 1
        if psychosis_data.get("poor_reality_testing"):
            risk_indicators += 2
        
        if risk_indicators >= 6:
            return RiskLevel.HIGH
        elif risk_indicators >= 4:
            return RiskLevel.MODERATE
        elif risk_indicators >= 2:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL
    
    def _create_risk_profile(self, comprehensive: ComprehensiveRiskAssessment) -> Dict[RiskType, RiskLevel]:
        profile = {}
        
        if comprehensive.suicide_assessment:
            profile[RiskType.SUICIDE_RISK] = comprehensive.suicide_assessment.overall_risk_level
        
        if comprehensive.self_harm_assessment:
            profile[RiskType.SELF_HARM_RISK] = comprehensive.self_harm_assessment.overall_risk_level
        
        if comprehensive.violence_assessment:
            profile[RiskType.VIOLENCE_RISK] = comprehensive.violence_assessment.overall_risk_level
        
        profile[RiskType.SUBSTANCE_ABUSE_RISK] = comprehensive.substance_risk_level
        profile[RiskType.PSYCHOSIS_RISK] = comprehensive.psychosis_risk_level
        
        return profile
    
    def _determine_global_risk_level(self, comprehensive: ComprehensiveRiskAssessment) -> RiskLevel:
        risk_levels = list(comprehensive.overall_risk_profile.values())
        
        if RiskLevel.IMMINENT in risk_levels:
            return RiskLevel.IMMINENT
        elif RiskLevel.HIGH in risk_levels:
            return RiskLevel.HIGH
        elif RiskLevel.MODERATE in risk_levels:
            return RiskLevel.MODERATE
        elif RiskLevel.LOW in risk_levels:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL
    
    def _determine_intervention_level(self, comprehensive: ComprehensiveRiskAssessment) -> InterventionLevel:
        global_risk = comprehensive.global_risk_level
        
        if global_risk == RiskLevel.IMMINENT:
            return InterventionLevel.INPATIENT
        elif global_risk == RiskLevel.HIGH:
            return InterventionLevel.PARTIAL_HOSPITALIZATION
        elif global_risk == RiskLevel.MODERATE:
            return InterventionLevel.INTENSIVE_OUTPATIENT
        else:
            return InterventionLevel.OUTPATIENT
    
    def _generate_risk_recommendations(self, comprehensive: ComprehensiveRiskAssessment) -> List[str]:
        recommendations = []
        
        # Global recommendations based on overall risk
        if comprehensive.global_risk_level == RiskLevel.IMMINENT:
            recommendations.extend([
                "Immediate psychiatric hospitalization",
                "Continuous supervision required",
                "Emergency intervention protocol"
            ])
        elif comprehensive.global_risk_level == RiskLevel.HIGH:
            recommendations.extend([
                "Intensive treatment recommended",
                "Frequent monitoring required",
                "Safety planning essential"
            ])
        
        # Specific recommendations based on risk types
        if RiskType.SUICIDE_RISK in comprehensive.overall_risk_profile:
            recommendations.append("Suicide-specific safety planning")
        
        if RiskType.VIOLENCE_RISK in comprehensive.overall_risk_profile:
            if comprehensive.violence_assessment and comprehensive.violence_assessment.duty_to_warn_triggered:
                recommendations.append("Duty to warn procedures required")
        
        if RiskType.SUBSTANCE_ABUSE_RISK in comprehensive.overall_risk_profile:
            if comprehensive.substance_risk_level in [RiskLevel.MODERATE, RiskLevel.HIGH]:
                recommendations.append("Substance abuse treatment referral")
        
        return recommendations
    
    def _generate_clinical_summary(self, comprehensive: ComprehensiveRiskAssessment) -> str:
        summary_parts = []
        
        summary_parts.append(f"Comprehensive risk assessment conducted on {comprehensive.assessment_date.strftime('%Y-%m-%d')}.")
        summary_parts.append(f"Global risk level assessed as {comprehensive.global_risk_level.value}.")
        
        # Summarize individual risk assessments
        if comprehensive.suicide_assessment:
            suicide_level = comprehensive.suicide_assessment.overall_risk_level.value
            summary_parts.append(f"Suicide risk: {suicide_level}.")
            if comprehensive.suicide_assessment.ideation_present:
                summary_parts.append("Active suicidal ideation identified.")
        
        if comprehensive.violence_assessment:
            violence_level = comprehensive.violence_assessment.overall_risk_level.value
            summary_parts.append(f"Violence risk: {violence_level}.")
            if comprehensive.violence_assessment.duty_to_warn_triggered:
                summary_parts.append("Duty to warn criteria met.")
        
        if comprehensive.self_harm_assessment:
            self_harm_level = comprehensive.self_harm_assessment.overall_risk_level.value
            summary_parts.append(f"Self-harm risk: {self_harm_level}.")
        
        # Intervention recommendations
        summary_parts.append(f"Recommended intervention level: {comprehensive.intervention_level.value}.")
        
        return " ".join(summary_parts)
    
    def _determine_follow_up_schedule(self, comprehensive: ComprehensiveRiskAssessment) -> str:
        if comprehensive.global_risk_level == RiskLevel.IMMINENT:
            return "Immediate and continuous monitoring"
        elif comprehensive.global_risk_level == RiskLevel.HIGH:
            return "Daily contact for first week, then every 2-3 days"
        elif comprehensive.global_risk_level == RiskLevel.MODERATE:
            return "Every 2-3 days for first week, then weekly"
        else:
            return "Weekly initially, then bi-weekly as appropriate"
    
    def _setup_crisis_contacts(self, contact_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        crisis_contacts = [
            {"name": "National Suicide Prevention Lifeline", "phone": "988", "available": "24/7"},
            {"name": "Crisis Text Line", "phone": "741741", "available": "24/7", "text": "HOME"},
            {"name": "Emergency Services", "phone": "911", "available": "24/7"}
        ]
        
        # Add custom contacts
        crisis_contacts.extend(contact_data)
        
        return crisis_contacts
    
    def update_safety_plan(self, plan_id: str, updates: Dict[str, Any]) -> bool:
        plan = self._get_safety_plan(plan_id)
        if not plan:
            return False
        
        # Update specified fields
        for field, value in updates.items():
            if hasattr(plan, field):
                setattr(plan, field, value)
        
        # Update review date if plan was modified
        plan.review_date = datetime.now() + timedelta(days=30)
        
        self._save_safety_plan(plan)
        return True
    
    def get_risk_history(self, patient_id: str, risk_type: Optional[RiskType] = None) -> List[Dict[str, Any]]:
        history = []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if not risk_type or risk_type == RiskType.SUICIDE_RISK:
                cursor.execute("""
                    SELECT assessment_date, overall_risk_level, 'suicide' as type
                    FROM suicide_risk_assessments 
                    WHERE patient_id = ?
                    ORDER BY assessment_date DESC
                """, (patient_id,))
                history.extend([{"date": row[0], "risk_level": row[1], "type": row[2]} for row in cursor.fetchall()])
            
            if not risk_type or risk_type == RiskType.VIOLENCE_RISK:
                cursor.execute("""
                    SELECT assessment_date, overall_risk_level, 'violence' as type
                    FROM violence_risk_assessments 
                    WHERE patient_id = ?
                    ORDER BY assessment_date DESC
                """, (patient_id,))
                history.extend([{"date": row[0], "risk_level": row[1], "type": row[2]} for row in cursor.fetchall()])
        
        return sorted(history, key=lambda x: x["date"], reverse=True)
    
    def generate_risk_report(self, assessment_id: str) -> str:
        assessment = self._get_comprehensive_assessment(assessment_id)
        if not assessment:
            return "Assessment not found"
        
        report_parts = []
        
        report_parts.append("COMPREHENSIVE RISK ASSESSMENT REPORT")
        report_parts.append("=" * 50)
        report_parts.append(f"Patient ID: {assessment.patient_id}")
        report_parts.append(f"Assessment Date: {assessment.assessment_date.strftime('%Y-%m-%d %H:%M')}")
        report_parts.append(f"Assessor: {assessment.assessor}")
        report_parts.append(f"Global Risk Level: {assessment.global_risk_level.value.upper()}")
        report_parts.append("")
        
        report_parts.append("RISK PROFILE:")
        for risk_type, risk_level in assessment.overall_risk_profile.items():
            report_parts.append(f"• {risk_type.value.replace('_', ' ').title()}: {risk_level.value}")
        report_parts.append("")
        
        if assessment.suicide_assessment:
            report_parts.append("SUICIDE RISK DETAILS:")
            suicide = assessment.suicide_assessment
            report_parts.append(f"• Ideation Present: {'Yes' if suicide.ideation_present else 'No'}")
            report_parts.append(f"• Plan Present: {'Yes' if suicide.plan_present else 'No'}")
            report_parts.append(f"• Intent Present: {'Yes' if suicide.intent_present else 'No'}")
            report_parts.append(f"• Means Access: {'Yes' if suicide.means_access else 'No'}")
            if suicide.protective_factors:
                report_parts.append(f"• Protective Factors: {', '.join(suicide.protective_factors)}")
            report_parts.append("")
        
        if assessment.violence_assessment:
            report_parts.append("VIOLENCE RISK DETAILS:")
            violence = assessment.violence_assessment
            report_parts.append(f"• Homicidal Ideation: {'Yes' if violence.homicidal_ideation else 'No'}")
            report_parts.append(f"• Specific Targets: {'Yes' if violence.specific_targets else 'No'}")
            report_parts.append(f"• Weapon Access: {'Yes' if violence.weapon_access else 'No'}")
            report_parts.append(f"• Duty to Warn: {'Yes' if violence.duty_to_warn_triggered else 'No'}")
            report_parts.append("")
        
        report_parts.append("RECOMMENDED INTERVENTIONS:")
        for rec in assessment.recommendations:
            report_parts.append(f"• {rec}")
        report_parts.append("")
        
        report_parts.append(f"INTERVENTION LEVEL: {assessment.intervention_level.value.replace('_', ' ').title()}")
        report_parts.append(f"FOLLOW-UP SCHEDULE: {assessment.follow_up_schedule}")
        report_parts.append("")
        
        if assessment.clinical_summary:
            report_parts.append("CLINICAL SUMMARY:")
            report_parts.append(assessment.clinical_summary)
        
        return "\n".join(report_parts)
    
    # Database operations
    def _save_suicide_assessment(self, assessment: SuicideRiskAssessment):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO suicide_risk_assessments (
                    assessment_id, patient_id, session_id, assessment_date, assessor,
                    ideation_present, ideation_frequency, ideation_intensity,
                    plan_present, plan_specificity, plan_lethality,
                    intent_present, intent_level, means_access, means_description,
                    previous_attempts, rehearsal_behaviors, precipitating_factors,
                    risk_factors, protective_factors, overall_risk_level,
                    confidence_level, clinical_notes, immediate_interventions,
                    safety_plan_created, created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id, assessment.patient_id, assessment.session_id,
                assessment.assessment_date.isoformat(), assessment.assessor,
                assessment.ideation_present, assessment.ideation_frequency, assessment.ideation_intensity,
                assessment.plan_present, assessment.plan_specificity, assessment.plan_lethality,
                assessment.intent_present, assessment.intent_level, assessment.means_access, assessment.means_description,
                json.dumps(assessment.previous_attempts), assessment.rehearsal_behaviors,
                json.dumps(assessment.precipitating_factors), json.dumps(assessment.risk_factors),
                json.dumps(assessment.protective_factors), assessment.overall_risk_level.value,
                assessment.confidence_level, assessment.clinical_notes,
                json.dumps(assessment.immediate_interventions), assessment.safety_plan_created,
                datetime.now().isoformat(), datetime.now().isoformat()
            ))
    
    def _save_self_harm_assessment(self, assessment: SelfHarmAssessment):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO self_harm_assessments (
                    assessment_id, patient_id, session_id, assessment_date, assessor,
                    current_urges, urge_intensity, methods_used, frequency, onset_age,
                    triggers, functions_served, medical_complications, concealment_behaviors,
                    risk_factors, protective_factors, overall_risk_level, suicide_risk_connection,
                    immediate_interventions, safety_strategies, created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id, assessment.patient_id, assessment.session_id,
                assessment.assessment_date.isoformat(), assessment.assessor,
                assessment.current_urges, assessment.urge_intensity, json.dumps(assessment.methods_used),
                assessment.frequency, assessment.onset_age, json.dumps(assessment.triggers),
                json.dumps(assessment.functions_served), json.dumps(assessment.medical_complications),
                json.dumps(assessment.concealment_behaviors), json.dumps(assessment.risk_factors),
                json.dumps(assessment.protective_factors), assessment.overall_risk_level.value,
                assessment.suicide_risk_connection, json.dumps(assessment.immediate_interventions),
                json.dumps(assessment.safety_strategies),
                datetime.now().isoformat(), datetime.now().isoformat()
            ))
    
    def _save_violence_assessment(self, assessment: ViolenceRiskAssessment):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO violence_risk_assessments (
                    assessment_id, patient_id, session_id, assessment_date, assessor,
                    homicidal_ideation, specific_targets, threat_specificity, violence_history,
                    weapon_access, weapon_types, impulse_control, substance_use_factor,
                    paranoid_ideation, command_hallucinations, risk_factors, protective_factors,
                    overall_risk_level, duty_to_warn_triggered, law_enforcement_contacted,
                    immediate_interventions, created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id, assessment.patient_id, assessment.session_id,
                assessment.assessment_date.isoformat(), assessment.assessor,
                assessment.homicidal_ideation, json.dumps(assessment.specific_targets),
                assessment.threat_specificity, json.dumps(assessment.violence_history),
                assessment.weapon_access, json.dumps(assessment.weapon_types),
                assessment.impulse_control, assessment.substance_use_factor,
                assessment.paranoid_ideation, assessment.command_hallucinations,
                json.dumps(assessment.risk_factors), json.dumps(assessment.protective_factors),
                assessment.overall_risk_level.value, assessment.duty_to_warn_triggered,
                assessment.law_enforcement_contacted, json.dumps(assessment.immediate_interventions),
                datetime.now().isoformat(), datetime.now().isoformat()
            ))
    
    def _save_comprehensive_assessment(self, assessment: ComprehensiveRiskAssessment):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO comprehensive_risk_assessments (
                    assessment_id, patient_id, session_id, assessment_date, assessor,
                    suicide_assessment_id, self_harm_assessment_id, violence_assessment_id,
                    substance_risk_level, psychosis_risk_level, overall_risk_profile,
                    global_risk_level, intervention_level, safety_plan_elements,
                    follow_up_schedule, crisis_contacts, clinical_summary,
                    recommendations, created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id, assessment.patient_id, assessment.session_id,
                assessment.assessment_date.isoformat(), assessment.assessor,
                assessment.suicide_assessment.assessment_id if assessment.suicide_assessment else None,
                assessment.self_harm_assessment.assessment_id if assessment.self_harm_assessment else None,
                assessment.violence_assessment.assessment_id if assessment.violence_assessment else None,
                assessment.substance_risk_level.value, assessment.psychosis_risk_level.value,
                json.dumps({k.value: v.value for k, v in assessment.overall_risk_profile.items()}),
                assessment.global_risk_level.value, assessment.intervention_level.value,
                json.dumps(assessment.safety_plan_elements), assessment.follow_up_schedule,
                json.dumps(assessment.crisis_contacts), assessment.clinical_summary,
                json.dumps(assessment.recommendations),
                datetime.now().isoformat(), datetime.now().isoformat()
            ))
    
    def _save_safety_plan(self, plan: SafetyPlan):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO safety_plans (
                    plan_id, patient_id, created_date, created_by, risk_types_addressed,
                    warning_signs, internal_coping_strategies, social_contacts,
                    professional_contacts, environmental_safety_steps, reasons_for_living,
                    patient_commitment, review_date, plan_status, effectiveness_rating, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plan.plan_id, plan.patient_id, plan.created_date.isoformat(), plan.created_by,
                json.dumps([rt.value for rt in plan.risk_types_addressed]),
                json.dumps(plan.warning_signs), json.dumps(plan.internal_coping_strategies),
                json.dumps(plan.social_contacts), json.dumps(plan.professional_contacts),
                json.dumps(plan.environmental_safety_steps), json.dumps(plan.reasons_for_living),
                plan.patient_commitment, plan.review_date.isoformat(), plan.plan_status,
                plan.effectiveness_rating, datetime.now().isoformat()
            ))
    
    def _get_safety_plan(self, plan_id: str) -> Optional[SafetyPlan]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM safety_plans WHERE plan_id = ?", (plan_id,))
            row = cursor.fetchone()
            
            if row:
                return SafetyPlan(
                    plan_id=row[0],
                    patient_id=row[1],
                    created_date=datetime.fromisoformat(row[2]),
                    created_by=row[3],
                    risk_types_addressed=[RiskType(rt) for rt in json.loads(row[4])],
                    warning_signs=json.loads(row[5]) if row[5] else [],
                    internal_coping_strategies=json.loads(row[6]) if row[6] else [],
                    social_contacts=json.loads(row[7]) if row[7] else [],
                    professional_contacts=json.loads(row[8]) if row[8] else [],
                    environmental_safety_steps=json.loads(row[9]) if row[9] else [],
                    reasons_for_living=json.loads(row[10]) if row[10] else [],
                    patient_commitment=row[11] or "",
                    review_date=datetime.fromisoformat(row[12]),
                    plan_status=row[13],
                    effectiveness_rating=row[14]
                )
            return None
    
    def _get_comprehensive_assessment(self, assessment_id: str) -> Optional[ComprehensiveRiskAssessment]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM comprehensive_risk_assessments WHERE assessment_id = ?", (assessment_id,))
            row = cursor.fetchone()
            
            if row:
                risk_profile = {}
                if row[10]:  # overall_risk_profile
                    profile_data = json.loads(row[10])
                    risk_profile = {RiskType(k): RiskLevel(v) for k, v in profile_data.items()}
                
                return ComprehensiveRiskAssessment(
                    assessment_id=row[0],
                    patient_id=row[1],
                    session_id=row[2],
                    assessment_date=datetime.fromisoformat(row[3]),
                    assessor=row[4],
                    suicide_assessment=None,  # Would need separate queries to load
                    self_harm_assessment=None,
                    violence_assessment=None,
                    substance_risk_level=RiskLevel(row[8]),
                    psychosis_risk_level=RiskLevel(row[9]),
                    overall_risk_profile=risk_profile,
                    global_risk_level=RiskLevel(row[11]),
                    intervention_level=InterventionLevel(row[12]),
                    safety_plan_elements=json.loads(row[13]) if row[13] else [],
                    follow_up_schedule=row[14] or "",
                    crisis_contacts=json.loads(row[15]) if row[15] else [],
                    clinical_summary=row[16] or "",
                    recommendations=json.loads(row[17]) if row[17] else []
                )
            return None


class RiskAssessmentWorkflow:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.risk_module = RiskAssessmentModule(db_path)
        self.current_assessment_id = None
        self.assessment_phase = AssessmentPhase.SCREENING
    
    def initiate_risk_assessment(self, patient_id: str, session_id: str, 
                               assessor: str, initial_concerns: List[str]) -> Dict[str, Any]:
        
        # Determine which risk types to assess based on concerns
        risk_types_to_assess = self._identify_risk_types_from_concerns(initial_concerns)
        
        # Start comprehensive assessment
        assessment_data = {"identified_risks": risk_types_to_assess}
        self.current_assessment_id = str(uuid.uuid4())
        
        return {
            "assessment_id": self.current_assessment_id,
            "risk_types_identified": [rt.value for rt in risk_types_to_assess],
            "assessment_phase": self.assessment_phase.value,
            "immediate_safety_check_needed": self._check_immediate_safety_concerns(initial_concerns),
            "next_steps": self._determine_next_assessment_steps(risk_types_to_assess)
        }
    
    def conduct_risk_screening(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        screening_results = {}
        follow_up_needed = []
        
        # Screen for suicide risk
        if any(keyword in str(responses).lower() for keyword in ["suicide", "kill myself", "end it all", "better off dead"]):
            screening_results[RiskType.SUICIDE_RISK] = RiskLevel.MODERATE
            follow_up_needed.append(RiskType.SUICIDE_RISK)
        
        # Screen for violence risk
        if any(keyword in str(responses).lower() for keyword in ["hurt someone", "kill them", "revenge", "weapon"]):
            screening_results[RiskType.VIOLENCE_RISK] = RiskLevel.MODERATE
            follow_up_needed.append(RiskType.VIOLENCE_RISK)
        
        # Screen for self-harm
        if any(keyword in str(responses).lower() for keyword in ["cut myself", "hurt myself", "self-harm", "burning"]):
            screening_results[RiskType.SELF_HARM_RISK] = RiskLevel.MODERATE
            follow_up_needed.append(RiskType.SELF_HARM_RISK)
        
        return {
            "screening_results": {k.value: v.value for k, v in screening_results.items()},
            "detailed_assessment_needed": follow_up_needed,
            "immediate_intervention_required": any(level in [RiskLevel.HIGH, RiskLevel.IMMINENT] for level in screening_results.values())
        }
    
    def conduct_detailed_assessment(self, risk_type: RiskType, responses: Dict[str, Any]) -> Dict[str, Any]:
        if not self.current_assessment_id:
            return {"error": "No active assessment session"}
        
        # Extract patient and session info from current assessment
        patient_id = responses.get("patient_id", "")
        session_id = responses.get("session_id", "")
        assessor = responses.get("assessor", "")
        
        assessment_result = None
        
        if risk_type == RiskType.SUICIDE_RISK:
            assessment_result = self.risk_module.conduct_suicide_risk_assessment(
                patient_id, session_id, assessor, responses
            )
        elif risk_type == RiskType.SELF_HARM_RISK:
            assessment_result = self.risk_module.conduct_self_harm_assessment(
                patient_id, session_id, assessor, responses
            )
        elif risk_type == RiskType.VIOLENCE_RISK:
            assessment_result = self.risk_module.conduct_violence_risk_assessment(
                patient_id, session_id, assessor, responses
            )
        
        if assessment_result:
            return {
                "assessment_completed": True,
                "risk_level": assessment_result.overall_risk_level.value,
                "immediate_interventions": getattr(assessment_result, 'immediate_interventions', []),
                "safety_plan_needed": getattr(assessment_result, 'safety_plan_created', False),
                "crisis_intervention_required": assessment_result.overall_risk_level in [RiskLevel.HIGH, RiskLevel.IMMINENT]
            }
        
        return {"assessment_completed": False, "error": "Assessment failed"}
    
    def create_safety_plan_from_assessment(self, patient_id: str, created_by: str, 
                                         assessment_results: Dict[str, Any]) -> Dict[str, Any]:
        
        # Determine risk types from assessment results
        risk_types = []
        if assessment_results.get("suicide_assessment"):
            risk_types.append(RiskType.SUICIDE_RISK)
        if assessment_results.get("violence_assessment"):
            risk_types.append(RiskType.VIOLENCE_RISK)
        if assessment_results.get("self_harm_assessment"):
            risk_types.append(RiskType.SELF_HARM_RISK)
        
        # Generate safety plan data
        plan_data = self._generate_safety_plan_data(assessment_results, risk_types)
        
        # Create safety plan
        safety_plan = self.risk_module.create_safety_plan(patient_id, created_by, risk_types, plan_data)
        
        return {
            "safety_plan_created": True,
            "plan_id": safety_plan.plan_id,
            "risk_types_addressed": [rt.value for rt in safety_plan.risk_types_addressed],
            "review_date": safety_plan.review_date.isoformat(),
            "plan_elements": len(safety_plan.warning_signs) + len(safety_plan.internal_coping_strategies)
        }
    
    def _identify_risk_types_from_concerns(self, concerns: List[str]) -> List[RiskType]:
        risk_types = []
        concerns_text = " ".join(concerns).lower()
        
        suicide_keywords = ["suicide", "kill myself", "end life", "better off dead", "hopeless", "worthless"]
        violence_keywords = ["hurt someone", "kill them", "revenge", "angry", "weapon", "fight"]
        self_harm_keywords = ["cut myself", "self-harm", "hurt myself", "burning", "punish myself"]
        
        if any(keyword in concerns_text for keyword in suicide_keywords):
            risk_types.append(RiskType.SUICIDE_RISK)
        
        if any(keyword in concerns_text for keyword in violence_keywords):
            risk_types.append(RiskType.VIOLENCE_RISK)
        
        if any(keyword in concerns_text for keyword in self_harm_keywords):
            risk_types.append(RiskType.SELF_HARM_RISK)
        
        # Default to suicide screening if no specific indicators
        if not risk_types:
            risk_types.append(RiskType.SUICIDE_RISK)
        
        return risk_types
    
    def _check_immediate_safety_concerns(self, concerns: List[str]) -> bool:
        immediate_keywords = [
            "right now", "tonight", "today", "going to do it", "have the means",
            "can't take it", "tonight's the night", "goodbye"
        ]
        
        concerns_text = " ".join(concerns).lower()
        return any(keyword in concerns_text for keyword in immediate_keywords)
    
    def _determine_next_assessment_steps(self, risk_types: List[RiskType]) -> List[str]:
        steps = []
        
        for risk_type in risk_types:
            if risk_type == RiskType.SUICIDE_RISK:
                steps.append("Conduct detailed suicide risk assessment")
            elif risk_type == RiskType.VIOLENCE_RISK:
                steps.append("Conduct violence risk assessment with duty to warn considerations")
            elif risk_type == RiskType.SELF_HARM_RISK:
                steps.append("Assess self-harm behaviors and triggers")
        
        steps.append("Create comprehensive safety plan")
        steps.append("Determine appropriate intervention level")
        
        return steps
    
    def _generate_safety_plan_data(self, assessment_results: Dict[str, Any], 
                                 risk_types: List[RiskType]) -> Dict[str, Any]:
        plan_data = {
            "warning_signs": [],
            "internal_coping": [],
            "social_contacts": [],
            "professional_contacts": [
                {"name": "National Suicide Prevention Lifeline", "phone": "988"},
                {"name": "Crisis Text Line", "phone": "741741", "instructions": "Text HOME"},
                {"name": "Emergency Services", "phone": "911"}
            ],
            "environmental_safety": [],
            "reasons_for_living": []
        }
        
        # Add risk-specific elements
        if RiskType.SUICIDE_RISK in risk_types:
            plan_data["warning_signs"].extend([
                "Feeling hopeless or trapped",
                "Thoughts of death or dying",
                "Feeling like a burden to others",
                "Extreme emotional pain"
            ])
            plan_data["environmental_safety"].extend([
                "Remove or secure firearms",
                "Remove access to large quantities of medication",
                "Remove other potential means of harm"
            ])
        
        if RiskType.SELF_HARM_RISK in risk_types:
            plan_data["warning_signs"].extend([
                "Strong urges to hurt myself",
                "Feeling emotionally overwhelmed",
                "Feeling numb or empty"
            ])
            plan_data["internal_coping"].extend([
                "Hold ice cubes",
                "Draw on skin with red marker",
                "Exercise vigorously",
                "Listen to loud music"
            ])
        
        if RiskType.VIOLENCE_RISK in risk_types:
            plan_data["warning_signs"].extend([
                "Anger escalating beyond control",
                "Thoughts of hurting others",
                "Feeling paranoid or persecuted"
            ])
            plan_data["environmental_safety"].extend([
                "Remove weapons from environment",
                "Avoid alcohol and substances",
                "Remove self from triggering situations"
            ])
        
        # Add common coping strategies
        plan_data["internal_coping"].extend([
            "Deep breathing exercises",
            "Progressive muscle relaxation",
            "Call a trusted friend or family member",
            "Engage in a distracting activity",
            "Write in a journal",
            "Take a warm bath or shower"
        ])
        
        return plan_data


class CrisisInterventionModule:
    
    def __init__(self, risk_module: RiskAssessmentModule):
        self.risk_module = risk_module
        self.crisis_protocols = self._initialize_crisis_protocols()
    
    def _initialize_crisis_protocols(self) -> Dict[RiskLevel, Dict[str, Any]]:
        return {
            RiskLevel.IMMINENT: {
                "immediate_actions": [
                    "Do not leave patient alone",
                    "Contact emergency services if necessary",
                    "Initiate psychiatric hold procedures",
                    "Remove all means of harm",
                    "Contact crisis team",
                    "Notify family/emergency contacts",
                    "Document all actions taken"
                ],
                "timeframe": "Immediate (within minutes)",
                "authorization_required": "Emergency procedures",
                "follow_up": "Continuous monitoring until stabilized"
            },
            RiskLevel.HIGH: {
                "immediate_actions": [
                    "Increase supervision level",
                    "Remove means of harm",
                    "Create detailed safety plan",
                    "Contact crisis team",
                    "Schedule immediate follow-up",
                    "Involve support system",
                    "Consider hospitalization"
                ],
                "timeframe": "Within 2 hours",
                "authorization_required": "Clinical supervisor notification",
                "follow_up": "Daily contact for one week"
            }
        }
    
    def activate_crisis_intervention(self, assessment_id: str, crisis_level: RiskLevel) -> Dict[str, Any]:
        protocol = self.crisis_protocols.get(crisis_level, {})
        
        if not protocol:
            return {"error": "No crisis protocol for this risk level"}
        
        intervention_id = str(uuid.uuid4())
        
        return {
            "intervention_id": intervention_id,
            "crisis_level": crisis_level.value,
            "immediate_actions": protocol["immediate_actions"],
            "timeframe": protocol["timeframe"],
            "authorization_required": protocol["authorization_required"],
            "follow_up_requirements": protocol["follow_up"],
            "documentation_needed": [
                "Crisis assessment details",
                "Actions taken and rationale",
                "Patient response to interventions",
                "Safety measures implemented",
                "Follow-up plan established"
            ]
        }
    
    def document_crisis_incident(self, patient_id: str, incident_data: Dict[str, Any]) -> str:
        incident_id = str(uuid.uuid4())
        
        with sqlite3.connect(self.risk_module.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO risk_incidents (
                    incident_id, patient_id, incident_date, incident_type,
                    severity_level, description, precipitating_factors,
                    interventions_used, outcome, lessons_learned,
                    safety_plan_updated, reported_to_authorities,
                    follow_up_actions, documented_by, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                incident_id, patient_id, datetime.now().isoformat(),
                incident_data.get("incident_type", ""), incident_data.get("severity_level", ""),
                incident_data.get("description", ""), json.dumps(incident_data.get("precipitating_factors", [])),
                json.dumps(incident_data.get("interventions_used", [])), incident_data.get("outcome", ""),
                incident_data.get("lessons_learned", ""), incident_data.get("safety_plan_updated", False),
                incident_data.get("reported_to_authorities", False),
                json.dumps(incident_data.get("follow_up_actions", [])),
                incident_data.get("documented_by", ""), datetime.now().isoformat()
            ))
        
        return incident_id
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import sqlite3
import json
import uuid
from datetime import datetime


class MSEDomain(Enum):
    APPEARANCE = "appearance"
    BEHAVIOR = "behavior"
    SPEECH = "speech"
    MOOD = "mood"
    AFFECT = "affect"
    THOUGHT_PROCESS = "thought_process"
    THOUGHT_CONTENT = "thought_content"
    PERCEPTION = "perception"
    COGNITION = "cognition"
    INSIGHT = "insight"
    JUDGMENT = "judgment"


class AppearanceDescriptor(Enum):
    WELL_GROOMED = "well_groomed"
    POORLY_GROOMED = "poorly_groomed"
    DISHEVELED = "disheveled"
    BIZARRE_DRESS = "bizarre_dress"
    AGE_APPROPRIATE = "age_appropriate"
    YOUNGER_THAN_AGE = "younger_than_age"
    OLDER_THAN_AGE = "older_than_age"
    THIN = "thin"
    AVERAGE_BUILD = "average_build"
    OVERWEIGHT = "overweight"
    TATTOOS_PIERCINGS = "tattoos_piercings"
    UNUSUAL_FEATURES = "unusual_features"


class BehaviorDescriptor(Enum):
    COOPERATIVE = "cooperative"
    UNCOOPERATIVE = "uncooperative"
    AGITATED = "agitated"
    RESTLESS = "restless"
    CALM = "calm"
    WITHDRAWN = "withdrawn"
    SUSPICIOUS = "suspicious"
    HOSTILE = "hostile"
    GUARDED = "guarded"
    OVERLY_FAMILIAR = "overly_familiar"
    SEDUCTIVE = "seductive"
    BIZARRE = "bizarre"
    CATATONIC = "catatonic"
    HYPERVIGILANT = "hypervigilant"


class SpeechCharacteristic(Enum):
    NORMAL_RATE = "normal_rate"
    SLOW = "slow"
    RAPID = "rapid"
    PRESSURED = "pressured"
    NORMAL_VOLUME = "normal_volume"
    LOUD = "loud"
    SOFT = "soft"
    MUMBLED = "mumbled"
    CLEAR = "clear"
    SLURRED = "slurred"
    ACCENTED = "accented"
    MONOTONE = "monotone"
    NORMAL_TONE = "normal_tone"
    HESITANT = "hesitant"
    FLUENT = "fluent"
    POVERTY_OF_SPEECH = "poverty_of_speech"


class MoodDescriptor(Enum):
    EUTHYMIC = "euthymic"
    DEPRESSED = "depressed"
    ELEVATED = "elevated"
    EUPHORIC = "euphoric"
    IRRITABLE = "irritable"
    ANXIOUS = "anxious"
    ANGRY = "angry"
    DYSPHORIC = "dysphoric"
    LABILE = "labile"
    EXPANSIVE = "expansive"


class AffectDescriptor(Enum):
    EUTHYMIC = "euthymic"
    CONSTRICTED = "constricted"
    BLUNTED = "blunted"
    FLAT = "flat"
    LABILE = "labile"
    INAPPROPRIATE = "inappropriate"
    CONGRUENT = "congruent"
    INCONGRUENT = "incongruent"
    ANXIOUS = "anxious"
    TEARFUL = "tearful"
    ANGRY = "angry"
    EUPHORIC = "euphoric"


class ThoughtProcessDescriptor(Enum):
    LINEAR = "linear"
    LOGICAL = "logical"
    GOAL_DIRECTED = "goal_directed"
    CIRCUMSTANTIAL = "circumstantial"
    TANGENTIAL = "tangential"
    LOOSE_ASSOCIATIONS = "loose_associations"
    FLIGHT_OF_IDEAS = "flight_of_ideas"
    WORD_SALAD = "word_salad"
    PERSEVERATION = "perseveration"
    BLOCKING = "blocking"
    RACING_THOUGHTS = "racing_thoughts"
    POVERTY_OF_THOUGHT = "poverty_of_thought"


class ThoughtContentDescriptor(Enum):
    NORMAL = "normal"
    OBSESSIONS = "obsessions"
    COMPULSIONS = "compulsions"
    PHOBIAS = "phobias"
    SUICIDAL_IDEATION = "suicidal_ideation"
    HOMICIDAL_IDEATION = "homicidal_ideation"
    DELUSIONS = "delusions"
    PARANOID_IDEATION = "paranoid_ideation"
    IDEAS_OF_REFERENCE = "ideas_of_reference"
    MAGICAL_THINKING = "magical_thinking"
    RUMINATIONS = "ruminations"
    WORTHLESSNESS = "worthlessness"
    GUILT = "guilt"
    HOPELESSNESS = "hopelessness"


class PerceptionDescriptor(Enum):
    NORMAL = "normal"
    AUDITORY_HALLUCINATIONS = "auditory_hallucinations"
    VISUAL_HALLUCINATIONS = "visual_hallucinations"
    TACTILE_HALLUCINATIONS = "tactile_hallucinations"
    OLFACTORY_HALLUCINATIONS = "olfactory_hallucinations"
    GUSTATORY_HALLUCINATIONS = "gustatory_hallucinations"
    DEPERSONALIZATION = "depersonalization"
    DEREALIZATION = "derealization"
    ILLUSIONS = "illusions"


class CognitionLevel(Enum):
    INTACT = "intact"
    MILDLY_IMPAIRED = "mildly_impaired"
    MODERATELY_IMPAIRED = "moderately_impaired"
    SEVERELY_IMPAIRED = "severely_impaired"


class InsightLevel(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    ABSENT = "absent"


class JudgmentLevel(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    SEVERELY_IMPAIRED = "severely_impaired"


@dataclass
class AppearanceObservation:
    overall_appearance: str = ""
    grooming: AppearanceDescriptor = AppearanceDescriptor.WELL_GROOMED
    dress: str = ""
    hygiene: str = ""
    physical_build: str = ""
    apparent_age: str = ""
    distinguishing_features: List[str] = field(default_factory=list)
    eye_contact: str = ""
    posture: str = ""


@dataclass
class BehaviorObservation:
    attitude: BehaviorDescriptor = BehaviorDescriptor.COOPERATIVE
    motor_activity: str = ""
    psychomotor_agitation: bool = False
    psychomotor_retardation: bool = False
    abnormal_movements: List[str] = field(default_factory=list)
    rapport: str = ""
    cooperation_level: str = ""
    impulse_control: str = ""
    social_appropriateness: str = ""


@dataclass
class SpeechObservation:
    rate: SpeechCharacteristic = SpeechCharacteristic.NORMAL_RATE
    volume: SpeechCharacteristic = SpeechCharacteristic.NORMAL_VOLUME
    tone: SpeechCharacteristic = SpeechCharacteristic.NORMAL_TONE
    articulation: SpeechCharacteristic = SpeechCharacteristic.CLEAR
    fluency: SpeechCharacteristic = SpeechCharacteristic.FLUENT
    quantity: str = ""
    spontaneity: str = ""
    latency: str = ""
    additional_notes: str = ""


@dataclass
class MoodAffectObservation:
    stated_mood: str = ""
    observed_mood: MoodDescriptor = MoodDescriptor.EUTHYMIC
    affect_type: AffectDescriptor = AffectDescriptor.EUTHYMIC
    mood_congruence: str = ""
    range: str = ""
    intensity: str = ""
    stability: str = ""
    reactivity: str = ""
    additional_observations: str = ""


@dataclass
class ThoughtObservation:
    process: ThoughtProcessDescriptor = ThoughtProcessDescriptor.LINEAR
    content_normal: bool = True
    content_descriptors: List[ThoughtContentDescriptor] = field(default_factory=list)
    delusion_types: List[str] = field(default_factory=list)
    obsessions_compulsions: List[str] = field(default_factory=list)
    suicidal_thoughts: Dict[str, Any] = field(default_factory=dict)
    homicidal_thoughts: Dict[str, Any] = field(default_factory=dict)
    preoccupations: List[str] = field(default_factory=list)
    abstract_thinking: str = ""


@dataclass
class PerceptionObservation:
    hallucinations_present: bool = False
    hallucination_types: List[PerceptionDescriptor] = field(default_factory=list)
    hallucination_details: Dict[str, str] = field(default_factory=dict)
    dissociative_symptoms: List[str] = field(default_factory=list)
    reality_testing: str = ""
    perceptual_distortions: List[str] = field(default_factory=list)


@dataclass
class CognitionObservation:
    orientation_person: bool = True
    orientation_place: bool = True
    orientation_time: bool = True
    orientation_situation: bool = True
    attention_concentration: CognitionLevel = CognitionLevel.INTACT
    memory_immediate: CognitionLevel = CognitionLevel.INTACT
    memory_recent: CognitionLevel = CognitionLevel.INTACT
    memory_remote: CognitionLevel = CognitionLevel.INTACT
    fund_of_knowledge: CognitionLevel = CognitionLevel.INTACT
    calculation: CognitionLevel = CognitionLevel.INTACT
    abstract_reasoning: CognitionLevel = CognitionLevel.INTACT
    proverb_interpretation: str = ""
    similarities_interpretation: str = ""
    cognitive_screening_score: Optional[int] = None
    cognitive_screening_test: str = ""


@dataclass
class InsightJudgmentObservation:
    illness_awareness: InsightLevel = InsightLevel.GOOD
    need_for_treatment: InsightLevel = InsightLevel.GOOD
    insight_description: str = ""
    practical_judgment: JudgmentLevel = JudgmentLevel.GOOD
    social_judgment: JudgmentLevel = JudgmentLevel.GOOD
    judgment_examples: List[str] = field(default_factory=list)
    decision_making_capacity: str = ""


@dataclass
class MentalStatusExamination:
    exam_id: str
    patient_id: str
    session_id: str
    exam_date: datetime
    examiner: str
    appearance: AppearanceObservation
    behavior: BehaviorObservation
    speech: SpeechObservation
    mood_affect: MoodAffectObservation
    thought: ThoughtObservation
    perception: PerceptionObservation
    cognition: CognitionObservation
    insight_judgment: InsightJudgmentObservation
    overall_impression: str = ""
    clinical_significance: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class MSETemplate:
    template_id: str
    template_name: str
    description: str
    domains_included: List[MSEDomain]
    questions: Dict[MSEDomain, List[str]]
    observation_prompts: Dict[MSEDomain, List[str]]
    scoring_criteria: Dict[str, Any]
    clinical_considerations: List[str]


class MentalStatusExamModule:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.mse_templates = self._initialize_mse_templates()
        self.cognitive_tests = self._initialize_cognitive_tests()
        self.clinical_indicators = self._initialize_clinical_indicators()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mental_status_exams (
                    exam_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    exam_date TEXT NOT NULL,
                    examiner TEXT NOT NULL,
                    appearance_data TEXT,
                    behavior_data TEXT,
                    speech_data TEXT,
                    mood_affect_data TEXT,
                    thought_data TEXT,
                    perception_data TEXT,
                    cognition_data TEXT,
                    insight_judgment_data TEXT,
                    overall_impression TEXT,
                    clinical_significance TEXT,
                    recommendations TEXT,
                    notes TEXT,
                    created_date TEXT,
                    last_updated TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mse_observations (
                    observation_id TEXT PRIMARY KEY,
                    exam_id TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    observation_type TEXT NOT NULL,
                    observation_value TEXT NOT NULL,
                    severity TEXT,
                    clinical_significance TEXT,
                    notes TEXT,
                    timestamp TEXT,
                    FOREIGN KEY (exam_id) REFERENCES mental_status_exams (exam_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cognitive_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    exam_id TEXT NOT NULL,
                    test_name TEXT NOT NULL,
                    raw_score INTEGER,
                    standardized_score INTEGER,
                    percentile_rank INTEGER,
                    interpretation TEXT,
                    areas_of_concern TEXT,
                    recommendations TEXT,
                    test_date TEXT,
                    FOREIGN KEY (exam_id) REFERENCES mental_status_exams (exam_id)
                )
            """)
    
    def _initialize_mse_templates(self) -> Dict[str, MSETemplate]:
        templates = {}
        
        templates["comprehensive"] = MSETemplate(
            template_id="comprehensive_mse",
            template_name="Comprehensive Mental Status Examination",
            description="Full MSE covering all domains for initial assessment",
            domains_included=list(MSEDomain),
            questions={
                MSEDomain.APPEARANCE: [
                    "How would you describe your appearance today?",
                    "How has your self-care been lately?",
                    "Are you comfortable with how you look?"
                ],
                MSEDomain.MOOD: [
                    "How would you describe your mood today?",
                    "How has your mood been over the past week?",
                    "What emotions have you been experiencing most?"
                ],
                MSEDomain.COGNITION: [
                    "What year is it? What month? What day?",
                    "Where are we right now?",
                    "I'm going to say three words and ask you to repeat them back",
                    "Can you count backward from 100 by 7s?"
                ]
            },
            observation_prompts={
                MSEDomain.APPEARANCE: [
                    "Note grooming and hygiene",
                    "Observe dress appropriateness",
                    "Assess apparent age vs chronological age"
                ],
                MSEDomain.BEHAVIOR: [
                    "Observe cooperation level",
                    "Note any unusual movements",
                    "Assess impulse control"
                ]
            },
            scoring_criteria={
                "orientation": {"fully_oriented": 4, "mild_impairment": 3, "moderate_impairment": 2, "severe_impairment": 1},
                "memory": {"intact": 3, "mild_impairment": 2, "moderate_impairment": 1, "severe_impairment": 0}
            },
            clinical_considerations=[
                "Note any signs requiring immediate intervention",
                "Assess for psychosis or severe mood symptoms",
                "Evaluate cognitive capacity for treatment decisions"
            ]
        )
        
        templates["brief"] = MSETemplate(
            template_id="brief_mse",
            template_name="Brief Mental Status Screen",
            description="Abbreviated MSE for routine follow-up sessions",
            domains_included=[MSEDomain.APPEARANCE, MSEDomain.MOOD, MSEDomain.THOUGHT_CONTENT, MSEDomain.COGNITION],
            questions={
                MSEDomain.MOOD: [
                    "How has your mood been since our last session?",
                    "Any significant changes in how you're feeling?"
                ],
                MSEDomain.THOUGHT_CONTENT: [
                    "Any thoughts of hurting yourself?",
                    "Any unusual or concerning thoughts?"
                ]
            },
            observation_prompts={
                MSEDomain.APPEARANCE: ["Quick grooming/presentation check"],
                MSEDomain.BEHAVIOR: ["Note any obvious behavioral changes"]
            },
            scoring_criteria={},
            clinical_considerations=[
                "Focus on safety and significant changes",
                "Compare to baseline from previous sessions"
            ]
        )
        
        return templates
    
    def _initialize_cognitive_tests(self) -> Dict[str, Dict[str, Any]]:
        return {
            "mini_mental_state": {
                "name": "Mini-Mental State Examination (MMSE)",
                "domains": ["orientation", "registration", "attention", "recall", "language"],
                "max_score": 30,
                "cutoffs": {"normal": 24, "mild_impairment": 18, "severe_impairment": 0},
                "questions": {
                    "orientation": [
                        "What year is it?", "What season?", "What month?", "What date?", "What day?",
                        "What country?", "What state?", "What city?", "What building?", "What floor?"
                    ],
                    "registration": ["Repeat these three words: apple, penny, table"],
                    "attention": ["Spell WORLD backwards or count backward from 100 by 7s"],
                    "recall": ["What were those three words I asked you to remember?"],
                    "language": ["Name this object (pen, watch)", "Repeat: No ifs, ands, or buts"]
                }
            },
            
            "montreal_cognitive": {
                "name": "Montreal Cognitive Assessment (MoCA)",
                "domains": ["visuospatial", "naming", "memory", "attention", "language", "abstraction", "orientation"],
                "max_score": 30,
                "cutoffs": {"normal": 26, "mild_impairment": 18, "severe_impairment": 0},
                "questions": {
                    "visuospatial": ["Copy this cube", "Draw a clock showing 10 past 11"],
                    "naming": ["Name these animals: lion, rhinoceros, camel"],
                    "attention": ["Repeat these numbers forward, then backward"]
                }
            },
            
            "clock_drawing": {
                "name": "Clock Drawing Test",
                "domains": ["visuospatial", "executive", "memory"],
                "max_score": 4,
                "cutoffs": {"normal": 3, "mild_impairment": 2, "severe_impairment": 0},
                "instructions": "Draw a clock face showing the time 10 past 11"
            }
        }
    
    def _initialize_clinical_indicators(self) -> Dict[str, List[str]]:
        return {
            "psychosis_indicators": [
                "Delusions present",
                "Hallucinations present",
                "Disorganized thought process",
                "Grossly disorganized behavior",
                "Bizarre appearance"
            ],
            "mood_disorder_indicators": [
                "Depressed or elevated mood",
                "Mood incongruent affect",
                "Psychomotor changes",
                "Suicidal or homicidal ideation",
                "Mood lability"
            ],
            "cognitive_impairment_indicators": [
                "Disorientation",
                "Memory impairment",
                "Attention deficits",
                "Language difficulties",
                "Executive dysfunction"
            ],
            "crisis_indicators": [
                "Active suicidal ideation",
                "Homicidal ideation",
                "Severe psychosis",
                "Severe agitation",
                "Substance intoxication"
            ]
        }
    
    def conduct_mental_status_exam(self, patient_id: str, session_id: str, 
                                  examiner: str, template_type: str = "comprehensive") -> str:
        exam_id = str(uuid.uuid4())
        template = self.mse_templates.get(template_type, self.mse_templates["comprehensive"])
        
        exam = MentalStatusExamination(
            exam_id=exam_id,
            patient_id=patient_id,
            session_id=session_id,
            exam_date=datetime.now(),
            examiner=examiner,
            appearance=AppearanceObservation(),
            behavior=BehaviorObservation(),
            speech=SpeechObservation(),
            mood_affect=MoodAffectObservation(),
            thought=ThoughtObservation(),
            perception=PerceptionObservation(),
            cognition=CognitionObservation(),
            insight_judgment=InsightJudgmentObservation(),
            overall_impression="",
            clinical_significance=[],
            recommendations=[],
            notes=""
        )
        
        self._save_mental_status_exam(exam)
        return exam_id
    
    def update_appearance_observations(self, exam_id: str, observations: Dict[str, Any]) -> bool:
        exam = self._get_mental_status_exam(exam_id)
        if not exam:
            return False
        
        appearance = exam.appearance
        for key, value in observations.items():
            if hasattr(appearance, key):
                setattr(appearance, key, value)
        
        exam.appearance = appearance
        self._save_mental_status_exam(exam)
        return True
    
    def update_behavior_observations(self, exam_id: str, observations: Dict[str, Any]) -> bool:
        exam = self._get_mental_status_exam(exam_id)
        if not exam:
            return False
        
        behavior = exam.behavior
        for key, value in observations.items():
            if hasattr(behavior, key):
                setattr(behavior, key, value)
        
        exam.behavior = behavior
        self._save_mental_status_exam(exam)
        return True
    
    def update_speech_observations(self, exam_id: str, observations: Dict[str, Any]) -> bool:
        exam = self._get_mental_status_exam(exam_id)
        if not exam:
            return False
        
        speech = exam.speech
        for key, value in observations.items():
            if hasattr(speech, key):
                setattr(speech, key, value)
        
        exam.speech = speech
        self._save_mental_status_exam(exam)
        return True
    
    def update_mood_affect_observations(self, exam_id: str, observations: Dict[str, Any]) -> bool:
        exam = self._get_mental_status_exam(exam_id)
        if not exam:
            return False
        
        mood_affect = exam.mood_affect
        for key, value in observations.items():
            if hasattr(mood_affect, key):
                setattr(mood_affect, key, value)
        
        exam.mood_affect = mood_affect
        self._save_mental_status_exam(exam)
        return True
    
    def update_thought_observations(self, exam_id: str, observations: Dict[str, Any]) -> bool:
        exam = self._get_mental_status_exam(exam_id)
        if not exam:
            return False
        
        thought = exam.thought
        for key, value in observations.items():
            if hasattr(thought, key):
                setattr(thought, key, value)
        
        exam.thought = thought
        self._save_mental_status_exam(exam)
        return True
    
    def update_perception_observations(self, exam_id: str, observations: Dict[str, Any]) -> bool:
        exam = self._get_mental_status_exam(exam_id)
        if not exam:
            return False
        
        perception = exam.perception
        for key, value in observations.items():
            if hasattr(perception, key):
                setattr(perception, key, value)
        
        exam.perception = perception
        self._save_mental_status_exam(exam)
        return True
    
    def update_cognition_observations(self, exam_id: str, observations: Dict[str, Any]) -> bool:
        exam = self._get_mental_status_exam(exam_id)
        if not exam:
            return False
        
        cognition = exam.cognition
        for key, value in observations.items():
            if hasattr(cognition, key):
                setattr(cognition, key, value)
        
        exam.cognition = cognition
        self._save_mental_status_exam(exam)
        return True
    
    def update_insight_judgment_observations(self, exam_id: str, observations: Dict[str, Any]) -> bool:
        exam = self._get_mental_status_exam(exam_id)
        if not exam:
            return False
        
        insight_judgment = exam.insight_judgment
        for key, value in observations.items():
            if hasattr(insight_judgment, key):
                setattr(insight_judgment, key, value)
        
        exam.insight_judgment = insight_judgment
        self._save_mental_status_exam(exam)
        return True
    
    def conduct_cognitive_screening(self, exam_id: str, test_name: str, responses: Dict[str, Any]) -> Dict[str, Any]:
        test_config = self.cognitive_tests.get(test_name)
        if not test_config:
            return {"error": "Test not found"}
        
        assessment_id = str(uuid.uuid4())
        raw_score = self._calculate_cognitive_score(test_name, responses)
        interpretation = self._interpret_cognitive_score(test_name, raw_score)
        
        cognitive_assessment = {
            "assessment_id": assessment_id,
            "exam_id": exam_id,
            "test_name": test_config["name"],
            "raw_score": raw_score,
            "max_score": test_config["max_score"],
            "interpretation": interpretation,
            "areas_of_concern": self._identify_cognitive_concerns(test_name, responses),
            "recommendations": self._generate_cognitive_recommendations(interpretation)
        }
        
        self._save_cognitive_assessment(cognitive_assessment)
        return cognitive_assessment
    
    def generate_mse_summary(self, exam_id: str) -> Dict[str, Any]:
        exam = self._get_mental_status_exam(exam_id)
        if not exam:
            return {}
        
        summary = {
            "exam_id": exam_id,
            "patient_id": exam.patient_id,
            "exam_date": exam.exam_date.isoformat(),
            "examiner": exam.examiner,
            
            "appearance_summary": self._summarize_appearance(exam.appearance),
            "behavior_summary": self._summarize_behavior(exam.behavior),
            "speech_summary": self._summarize_speech(exam.speech),
            "mood_affect_summary": self._summarize_mood_affect(exam.mood_affect),
            "thought_summary": self._summarize_thought(exam.thought),
            "perception_summary": self._summarize_perception(exam.perception),
            "cognition_summary": self._summarize_cognition(exam.cognition),
            "insight_judgment_summary": self._summarize_insight_judgment(exam.insight_judgment),
            
            "clinical_significance": exam.clinical_significance,
            "crisis_indicators": self._identify_crisis_indicators(exam),
            "diagnostic_indicators": self._identify_diagnostic_indicators(exam),
            "recommendations": exam.recommendations,
            "overall_impression": exam.overall_impression
        }
        
        return summary
    
    def _calculate_cognitive_score(self, test_name: str, responses: Dict[str, Any]) -> int:
        test_config = self.cognitive_tests[test_name]
        total_score = 0
        
        if test_name == "mini_mental_state":
            orientation_score = sum(1 for q in responses.get("orientation", []) if q.get("correct"))
            registration_score = sum(1 for q in responses.get("registration", []) if q.get("correct"))
            attention_score = responses.get("attention_score", 0)
            recall_score = sum(1 for q in responses.get("recall", []) if q.get("correct"))
            language_score = sum(1 for q in responses.get("language", []) if q.get("correct"))
            
            total_score = orientation_score + registration_score + attention_score + recall_score + language_score
        
        elif test_name == "clock_drawing":
            clock_features = responses.get("clock_features", {})
            score = 0
            if clock_features.get("circle_drawn"): score += 1
            if clock_features.get("numbers_correct"): score += 1
            if clock_features.get("hands_present"): score += 1
            if clock_features.get("time_correct"): score += 1
            total_score = score
        
        return min(total_score, test_config["max_score"])
    
    def _interpret_cognitive_score(self, test_name: str, raw_score: int) -> str:
        test_config = self.cognitive_tests[test_name]
        cutoffs = test_config["cutoffs"]
        
        if raw_score >= cutoffs["normal"]:
            return "Normal cognitive function"
        elif raw_score >= cutoffs["mild_impairment"]:
            return "Mild cognitive impairment"
        else:
            return "Significant cognitive impairment"
    
    def _identify_cognitive_concerns(self, test_name: str, responses: Dict[str, Any]) -> List[str]:
        concerns = []
        
        if test_name == "mini_mental_state":
            if not all(q.get("correct") for q in responses.get("orientation", [])):
                concerns.append("Orientation difficulties")
            if responses.get("attention_score", 0) < 3:
                concerns.append("Attention and concentration problems")
            if not all(q.get("correct") for q in responses.get("recall", [])):
                concerns.append("Memory impairment")
        
        return concerns
    
    def _generate_cognitive_recommendations(self, interpretation: str) -> List[str]:
        recommendations = []
        
        if "impairment" in interpretation.lower():
            recommendations.extend([
                "Consider neuropsychological testing",
                "Evaluate for medical causes of cognitive impairment",
                "Assess functional capacity",
                "Consider cognitive rehabilitation"
            ])
        
        if "significant" in interpretation.lower():
            recommendations.extend([
                "Urgent neurological consultation",
                "Brain imaging recommended",
                "Assess decision-making capacity",
                "Involve family/caregivers in treatment planning"
            ])
        
        return recommendations
    
    def _summarize_appearance(self, appearance: AppearanceObservation) -> str:
        descriptors = []
        
        if appearance.grooming != AppearanceDescriptor.WELL_GROOMED:
            descriptors.append(f"grooming: {appearance.grooming.value}")
        
        if appearance.dress:
            descriptors.append(f"dress: {appearance.dress}")
        
        if appearance.eye_contact:
            descriptors.append(f"eye contact: {appearance.eye_contact}")
        
        if appearance.distinguishing_features:
            descriptors.append(f"notable features: {', '.join(appearance.distinguishing_features)}")
        
        return "; ".join(descriptors) if descriptors else "Unremarkable appearance"
    
    def _summarize_behavior(self, behavior: BehaviorObservation) -> str:
        descriptors = []
        
        if behavior.attitude != BehaviorDescriptor.COOPERATIVE:
            descriptors.append(f"attitude: {behavior.attitude.value}")
        
        if behavior.psychomotor_agitation:
            descriptors.append("psychomotor agitation")
        
        if behavior.psychomotor_retardation:
            descriptors.append("psychomotor retardation")
        
        if behavior.abnormal_movements:
            descriptors.append(f"abnormal movements: {', '.join(behavior.abnormal_movements)}")
        
        if behavior.impulse_control and "poor" in behavior.impulse_control.lower():
            descriptors.append("poor impulse control")
        
        return "; ".join(descriptors) if descriptors else "Cooperative, no behavioral concerns"
    
    def _summarize_speech(self, speech: SpeechObservation) -> str:
        descriptors = []
        
        if speech.rate != SpeechCharacteristic.NORMAL_RATE:
            descriptors.append(f"rate: {speech.rate.value}")
        
        if speech.volume != SpeechCharacteristic.NORMAL_VOLUME:
            descriptors.append(f"volume: {speech.volume.value}")
        
        if speech.articulation != SpeechCharacteristic.CLEAR:
            descriptors.append(f"articulation: {speech.articulation.value}")
        
        if speech.fluency != SpeechCharacteristic.FLUENT:
            descriptors.append(f"fluency: {speech.fluency.value}")
        
        if speech.quantity and "reduced" in speech.quantity.lower():
            descriptors.append("reduced quantity")
        
        return "; ".join(descriptors) if descriptors else "Normal speech characteristics"
    
    def _summarize_mood_affect(self, mood_affect: MoodAffectObservation) -> str:
        descriptors = []
        
        if mood_affect.stated_mood:
            descriptors.append(f"stated mood: {mood_affect.stated_mood}")
        
        if mood_affect.observed_mood != MoodDescriptor.EUTHYMIC:
            descriptors.append(f"observed mood: {mood_affect.observed_mood.value}")
        
        if mood_affect.affect_type != AffectDescriptor.EUTHYMIC:
            descriptors.append(f"affect: {mood_affect.affect_type.value}")
        
        if mood_affect.mood_congruence and "incongruent" in mood_affect.mood_congruence.lower():
            descriptors.append("mood-affect incongruence")
        
        if mood_affect.stability and "labile" in mood_affect.stability.lower():
            descriptors.append("mood lability")
        
        return "; ".join(descriptors) if descriptors else "Euthymic mood, appropriate affect"
    
    def _summarize_thought(self, thought: ThoughtObservation) -> str:
        descriptors = []
        
        if thought.process != ThoughtProcessDescriptor.LINEAR:
            descriptors.append(f"process: {thought.process.value}")
        
        if not thought.content_normal:
            content_issues = [desc.value for desc in thought.content_descriptors]
            descriptors.append(f"content: {', '.join(content_issues)}")
        
        if thought.suicidal_thoughts.get("present"):
            descriptors.append("suicidal ideation present")
        
        if thought.homicidal_thoughts.get("present"):
            descriptors.append("homicidal ideation present")
        
        if thought.delusion_types:
            descriptors.append(f"delusions: {', '.join(thought.delusion_types)}")
        
        return "; ".join(descriptors) if descriptors else "Linear thought process, normal content"
    
    def _summarize_perception(self, perception: PerceptionObservation) -> str:
        descriptors = []
        
        if perception.hallucinations_present:
            hallucination_types = [desc.value for desc in perception.hallucination_types]
            descriptors.append(f"hallucinations: {', '.join(hallucination_types)}")
        
        if perception.dissociative_symptoms:
            descriptors.append(f"dissociative symptoms: {', '.join(perception.dissociative_symptoms)}")
        
        if perception.reality_testing and "impaired" in perception.reality_testing.lower():
            descriptors.append("impaired reality testing")
        
        return "; ".join(descriptors) if descriptors else "No perceptual disturbances"
    
    def _summarize_cognition(self, cognition: CognitionObservation) -> str:
        descriptors = []
        
        orientation_items = []
        if not cognition.orientation_person:
            orientation_items.append("person")
        if not cognition.orientation_place:
            orientation_items.append("place")
        if not cognition.orientation_time:
            orientation_items.append("time")
        if not cognition.orientation_situation:
            orientation_items.append("situation")
        
        if orientation_items:
            descriptors.append(f"disoriented to: {', '.join(orientation_items)}")
        
        if cognition.attention_concentration != CognitionLevel.INTACT:
            descriptors.append(f"attention: {cognition.attention_concentration.value}")
        
        memory_issues = []
        if cognition.memory_immediate != CognitionLevel.INTACT:
            memory_issues.append(f"immediate: {cognition.memory_immediate.value}")
        if cognition.memory_recent != CognitionLevel.INTACT:
            memory_issues.append(f"recent: {cognition.memory_recent.value}")
        if cognition.memory_remote != CognitionLevel.INTACT:
            memory_issues.append(f"remote: {cognition.memory_remote.value}")
        
        if memory_issues:
            descriptors.append(f"memory - {', '.join(memory_issues)}")
        
        if cognition.cognitive_screening_score is not None:
            descriptors.append(f"{cognition.cognitive_screening_test}: {cognition.cognitive_screening_score}")
        
        return "; ".join(descriptors) if descriptors else "Cognitively intact"
    
    def _summarize_insight_judgment(self, insight_judgment: InsightJudgmentObservation) -> str:
        descriptors = []
        
        if insight_judgment.illness_awareness != InsightLevel.GOOD:
            descriptors.append(f"illness awareness: {insight_judgment.illness_awareness.value}")
        
        if insight_judgment.need_for_treatment != InsightLevel.GOOD:
            descriptors.append(f"treatment awareness: {insight_judgment.need_for_treatment.value}")
        
        if insight_judgment.practical_judgment != JudgmentLevel.GOOD:
            descriptors.append(f"practical judgment: {insight_judgment.practical_judgment.value}")
        
        if insight_judgment.social_judgment != JudgmentLevel.GOOD:
            descriptors.append(f"social judgment: {insight_judgment.social_judgment.value}")
        
        return "; ".join(descriptors) if descriptors else "Good insight and judgment"
    
    def _identify_crisis_indicators(self, exam: MentalStatusExamination) -> List[str]:
        indicators = []
        
        if exam.thought.suicidal_thoughts.get("present"):
            indicators.append("Active suicidal ideation")
        
        if exam.thought.homicidal_thoughts.get("present"):
            indicators.append("Homicidal ideation")
        
        if exam.perception.hallucinations_present:
            indicators.append("Active hallucinations")
        
        if exam.behavior.psychomotor_agitation:
            indicators.append("Severe agitation")
        
        if exam.behavior.attitude in [BehaviorDescriptor.HOSTILE, BehaviorDescriptor.AGITATED]:
            indicators.append("Behavioral dyscontrol")
        
        if not exam.cognition.orientation_person or not exam.cognition.orientation_place:
            indicators.append("Severe disorientation")
        
        return indicators
    
    def _identify_diagnostic_indicators(self, exam: MentalStatusExamination) -> Dict[str, List[str]]:
        indicators = {
            "mood_disorders": [],
            "psychotic_disorders": [],
            "anxiety_disorders": [],
            "cognitive_disorders": [],
            "substance_related": []
        }
        
        if exam.mood_affect.observed_mood in [MoodDescriptor.DEPRESSED, MoodDescriptor.ELEVATED, MoodDescriptor.EUPHORIC]:
            indicators["mood_disorders"].append(f"Mood: {exam.mood_affect.observed_mood.value}")
        
        if exam.behavior.psychomotor_agitation or exam.behavior.psychomotor_retardation:
            indicators["mood_disorders"].append("Psychomotor changes")
        
        if exam.thought.delusion_types or exam.perception.hallucinations_present:
            indicators["psychotic_disorders"].append("Psychotic symptoms present")
        
        if exam.thought.process in [ThoughtProcessDescriptor.LOOSE_ASSOCIATIONS, ThoughtProcessDescriptor.FLIGHT_OF_IDEAS]:
            indicators["psychotic_disorders"].append(f"Thought process: {exam.thought.process.value}")
        
        if exam.mood_affect.observed_mood == MoodDescriptor.ANXIOUS:
            indicators["anxiety_disorders"].append("Anxious mood")
        
        orientation_deficits = sum([
            not exam.cognition.orientation_person,
            not exam.cognition.orientation_place,
            not exam.cognition.orientation_time,
            not exam.cognition.orientation_situation
        ])
        
        if orientation_deficits >= 2:
            indicators["cognitive_disorders"].append("Orientation deficits")
        
        if exam.cognition.memory_recent != CognitionLevel.INTACT:
            indicators["cognitive_disorders"].append("Memory impairment")
        
        if exam.speech.articulation == SpeechCharacteristic.SLURRED:
            indicators["substance_related"].append("Speech changes suggestive of intoxication")
        
        return {k: v for k, v in indicators.items() if v}
    
    def _save_mental_status_exam(self, exam: MentalStatusExamination):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO mental_status_exams (
                    exam_id, patient_id, session_id, exam_date, examiner,
                    appearance_data, behavior_data, speech_data, mood_affect_data,
                    thought_data, perception_data, cognition_data, insight_judgment_data,
                    overall_impression, clinical_significance, recommendations, notes,
                    created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                exam.exam_id,
                exam.patient_id,
                exam.session_id,
                exam.exam_date.isoformat(),
                exam.examiner,
                json.dumps(exam.appearance.__dict__),
                json.dumps(exam.behavior.__dict__),
                json.dumps(exam.speech.__dict__),
                json.dumps(exam.mood_affect.__dict__),
                json.dumps(exam.thought.__dict__),
                json.dumps(exam.perception.__dict__),
                json.dumps(exam.cognition.__dict__),
                json.dumps(exam.insight_judgment.__dict__),
                exam.overall_impression,
                json.dumps(exam.clinical_significance),
                json.dumps(exam.recommendations),
                exam.notes,
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
    
    def _save_cognitive_assessment(self, assessment: Dict[str, Any]):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO cognitive_assessments (
                    assessment_id, exam_id, test_name, raw_score, standardized_score,
                    percentile_rank, interpretation, areas_of_concern, recommendations, test_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment["assessment_id"],
                assessment["exam_id"],
                assessment["test_name"],
                assessment["raw_score"],
                assessment.get("standardized_score"),
                assessment.get("percentile_rank"),
                assessment["interpretation"],
                json.dumps(assessment.get("areas_of_concern", [])),
                json.dumps(assessment.get("recommendations", [])),
                datetime.now().isoformat()
            ))
    
    def _get_mental_status_exam(self, exam_id: str) -> Optional[MentalStatusExamination]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM mental_status_exams WHERE exam_id = ?
            """, (exam_id,))
            row = cursor.fetchone()
            
            if row:
                return MentalStatusExamination(
                    exam_id=row[0],
                    patient_id=row[1],
                    session_id=row[2],
                    exam_date=datetime.fromisoformat(row[3]),
                    examiner=row[4],
                    appearance=AppearanceObservation(**json.loads(row[5]) if row[5] else {}),
                    behavior=BehaviorObservation(**json.loads(row[6]) if row[6] else {}),
                    speech=SpeechObservation(**json.loads(row[7]) if row[7] else {}),
                    mood_affect=MoodAffectObservation(**json.loads(row[8]) if row[8] else {}),
                    thought=ThoughtObservation(**json.loads(row[9]) if row[9] else {}),
                    perception=PerceptionObservation(**json.loads(row[10]) if row[10] else {}),
                    cognition=CognitionObservation(**json.loads(row[11]) if row[11] else {}),
                    insight_judgment=InsightJudgmentObservation(**json.loads(row[12]) if row[12] else {}),
                    overall_impression=row[13] or "",
                    clinical_significance=json.loads(row[14]) if row[14] else [],
                    recommendations=json.loads(row[15]) if row[15] else [],
                    notes=row[16] or ""
                )
            return None
    
    def get_patient_mse_history(self, patient_id: str) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT exam_id, exam_date, examiner, overall_impression 
                FROM mental_status_exams 
                WHERE patient_id = ? 
                ORDER BY exam_date DESC
            """, (patient_id,))
            rows = cursor.fetchall()
            
            history = []
            for row in rows:
                history.append({
                    "exam_id": row[0],
                    "exam_date": row[1],
                    "examiner": row[2],
                    "overall_impression": row[3]
                })
            
            return history
    
    def compare_mse_findings(self, exam_id_1: str, exam_id_2: str) -> Dict[str, Any]:
        exam1 = self._get_mental_status_exam(exam_id_1)
        exam2 = self._get_mental_status_exam(exam_id_2)
        
        if not exam1 or not exam2:
            return {"error": "One or both exams not found"}
        
        comparison = {
            "exam_dates": {
                "earlier": exam1.exam_date.isoformat(),
                "later": exam2.exam_date.isoformat()
            },
            "changes_noted": {
                "mood": self._compare_mood_changes(exam1.mood_affect, exam2.mood_affect),
                "cognition": self._compare_cognitive_changes(exam1.cognition, exam2.cognition),
                "thought": self._compare_thought_changes(exam1.thought, exam2.thought),
                "behavior": self._compare_behavior_changes(exam1.behavior, exam2.behavior)
            },
            "clinical_significance": self._assess_change_significance(exam1, exam2)
        }
        
        return comparison
    
    def _compare_mood_changes(self, mood1: MoodAffectObservation, mood2: MoodAffectObservation) -> Dict[str, str]:
        changes = {}
        
        if mood1.observed_mood != mood2.observed_mood:
            changes["mood"] = f"Changed from {mood1.observed_mood.value} to {mood2.observed_mood.value}"
        
        if mood1.affect_type != mood2.affect_type:
            changes["affect"] = f"Changed from {mood1.affect_type.value} to {mood2.affect_type.value}"
        
        return changes
    
    def _compare_cognitive_changes(self, cog1: CognitionObservation, cog2: CognitionObservation) -> Dict[str, str]:
        changes = {}
        
        orientation1 = sum([cog1.orientation_person, cog1.orientation_place, cog1.orientation_time, cog1.orientation_situation])
        orientation2 = sum([cog2.orientation_person, cog2.orientation_place, cog2.orientation_time, cog2.orientation_situation])
        
        if orientation1 != orientation2:
            changes["orientation"] = f"Orientation changed from {orientation1}/4 to {orientation2}/4"
        
        if cog1.attention_concentration != cog2.attention_concentration:
            changes["attention"] = f"Attention changed from {cog1.attention_concentration.value} to {cog2.attention_concentration.value}"
        
        if cog1.memory_recent != cog2.memory_recent:
            changes["memory"] = f"Recent memory changed from {cog1.memory_recent.value} to {cog2.memory_recent.value}"
        
        return changes
    
    def _compare_thought_changes(self, thought1: ThoughtObservation, thought2: ThoughtObservation) -> Dict[str, str]:
        changes = {}
        
        if thought1.process != thought2.process:
            changes["process"] = f"Thought process changed from {thought1.process.value} to {thought2.process.value}"
        
        if thought1.content_normal != thought2.content_normal:
            changes["content"] = "Thought content abnormalities changed"
        
        suicidal1 = thought1.suicidal_thoughts.get("present", False)
        suicidal2 = thought2.suicidal_thoughts.get("present", False)
        
        if suicidal1 != suicidal2:
            if suicidal2:
                changes["suicidal_ideation"] = "Suicidal ideation emerged"
            else:
                changes["suicidal_ideation"] = "Suicidal ideation resolved"
        
        return changes
    
    def _compare_behavior_changes(self, behavior1: BehaviorObservation, behavior2: BehaviorObservation) -> Dict[str, str]:
        changes = {}
        
        if behavior1.attitude != behavior2.attitude:
            changes["attitude"] = f"Attitude changed from {behavior1.attitude.value} to {behavior2.attitude.value}"
        
        if behavior1.psychomotor_agitation != behavior2.psychomotor_agitation:
            if behavior2.psychomotor_agitation:
                changes["psychomotor"] = "Psychomotor agitation developed"
            else:
                changes["psychomotor"] = "Psychomotor agitation resolved"
        
        return changes
    
    def _assess_change_significance(self, exam1: MentalStatusExamination, exam2: MentalStatusExamination) -> str:
        significant_changes = []
        
        if exam1.mood_affect.observed_mood != exam2.mood_affect.observed_mood:
            significant_changes.append("mood change")
        
        suicidal1 = exam1.thought.suicidal_thoughts.get("present", False)
        suicidal2 = exam2.thought.suicidal_thoughts.get("present", False)
        if suicidal1 != suicidal2:
            significant_changes.append("suicidal ideation change")
        
        if exam1.perception.hallucinations_present != exam2.perception.hallucinations_present:
            significant_changes.append("perceptual change")
        
        orientation1 = sum([exam1.cognition.orientation_person, exam1.cognition.orientation_place, exam1.cognition.orientation_time, exam1.cognition.orientation_situation])
        orientation2 = sum([exam2.cognition.orientation_person, exam2.cognition.orientation_place, exam2.cognition.orientation_time, exam2.cognition.orientation_situation])
        
        if abs(orientation1 - orientation2) >= 2:
            significant_changes.append("cognitive change")
        
        if len(significant_changes) >= 3:
            return "Significant clinical changes noted"
        elif len(significant_changes) >= 1:
            return "Some clinical changes noted"
        else:
            return "Stable presentation"
    
    def generate_mse_report(self, exam_id: str, report_type: str = "comprehensive") -> str:
        exam = self._get_mental_status_exam(exam_id)
        if not exam:
            return "Exam not found"
        
        if report_type == "comprehensive":
            return self._generate_comprehensive_report(exam)
        elif report_type == "brief":
            return self._generate_brief_report(exam)
        elif report_type == "clinical":
            return self._generate_clinical_narrative(exam)
        
        return "Unknown report type"
    
    def _generate_comprehensive_report(self, exam: MentalStatusExamination) -> str:
        report_sections = []
        
        report_sections.append("MENTAL STATUS EXAMINATION")
        report_sections.append(f"Date: {exam.exam_date.strftime('%Y-%m-%d')}")
        report_sections.append(f"Patient ID: {exam.patient_id}")
        report_sections.append(f"Examiner: {exam.examiner}")
        report_sections.append("")
        
        report_sections.append("APPEARANCE:")
        report_sections.append(self._summarize_appearance(exam.appearance))
        report_sections.append("")
        
        report_sections.append("BEHAVIOR:")
        report_sections.append(self._summarize_behavior(exam.behavior))
        report_sections.append("")
        
        report_sections.append("SPEECH:")
        report_sections.append(self._summarize_speech(exam.speech))
        report_sections.append("")
        
        report_sections.append("MOOD AND AFFECT:")
        report_sections.append(self._summarize_mood_affect(exam.mood_affect))
        report_sections.append("")
        
        report_sections.append("THOUGHT:")
        report_sections.append(self._summarize_thought(exam.thought))
        report_sections.append("")
        
        report_sections.append("PERCEPTION:")
        report_sections.append(self._summarize_perception(exam.perception))
        report_sections.append("")
        
        report_sections.append("COGNITION:")
        report_sections.append(self._summarize_cognition(exam.cognition))
        report_sections.append("")
        
        report_sections.append("INSIGHT AND JUDGMENT:")
        report_sections.append(self._summarize_insight_judgment(exam.insight_judgment))
        report_sections.append("")
        
        if exam.overall_impression:
            report_sections.append("OVERALL IMPRESSION:")
            report_sections.append(exam.overall_impression)
            report_sections.append("")
        
        if exam.clinical_significance:
            report_sections.append("CLINICAL SIGNIFICANCE:")
            for item in exam.clinical_significance:
                report_sections.append(f"• {item}")
            report_sections.append("")
        
        if exam.recommendations:
            report_sections.append("RECOMMENDATIONS:")
            for item in exam.recommendations:
                report_sections.append(f"• {item}")
        
        return "\n".join(report_sections)
    
    def _generate_brief_report(self, exam: MentalStatusExamination) -> str:
        crisis_indicators = self._identify_crisis_indicators(exam)
        diagnostic_indicators = self._identify_diagnostic_indicators(exam)
        
        brief_report = []
        brief_report.append(f"MSE Brief Summary - {exam.exam_date.strftime('%Y-%m-%d')}")
        brief_report.append("")
        
        if crisis_indicators:
            brief_report.append("CRISIS INDICATORS:")
            for indicator in crisis_indicators:
                brief_report.append(f"• {indicator}")
            brief_report.append("")
        
        brief_report.append("KEY FINDINGS:")
        brief_report.append(f"Mood: {self._summarize_mood_affect(exam.mood_affect)}")
        brief_report.append(f"Thought: {self._summarize_thought(exam.thought)}")
        brief_report.append(f"Cognition: {self._summarize_cognition(exam.cognition)}")
        brief_report.append("")
        
        if any(diagnostic_indicators.values()):
            brief_report.append("DIAGNOSTIC CONSIDERATIONS:")
            for category, indicators in diagnostic_indicators.items():
                if indicators:
                    brief_report.append(f"{category.replace('_', ' ').title()}: {', '.join(indicators)}")
        
        return "\n".join(brief_report)
    
    def _generate_clinical_narrative(self, exam: MentalStatusExamination) -> str:
        narrative = []
        
        narrative.append(f"Patient presented for mental status examination on {exam.exam_date.strftime('%B %d, %Y')}.")
        
        appearance_summary = self._summarize_appearance(exam.appearance)
        if appearance_summary != "Unremarkable appearance":
            narrative.append(f"Appearance was notable for {appearance_summary.lower()}.")
        
        behavior_summary = self._summarize_behavior(exam.behavior)
        if behavior_summary != "Cooperative, no behavioral concerns":
            narrative.append(f"Behaviorally, patient demonstrated {behavior_summary.lower()}.")
        
        mood_summary = self._summarize_mood_affect(exam.mood_affect)
        narrative.append(f"Mood and affect were characterized by {mood_summary.lower()}.")
        
        thought_summary = self._summarize_thought(exam.thought)
        if thought_summary != "Linear thought process, normal content":
            narrative.append(f"Thought processes revealed {thought_summary.lower()}.")
        
        cognition_summary = self._summarize_cognition(exam.cognition)
        if cognition_summary != "Cognitively intact":
            narrative.append(f"Cognitive assessment showed {cognition_summary.lower()}.")
        
        crisis_indicators = self._identify_crisis_indicators(exam)
        if crisis_indicators:
            narrative.append(f"Significant safety concerns were identified including {', '.join(crisis_indicators).lower()}.")
        
        if exam.overall_impression:
            narrative.append(f"Overall clinical impression: {exam.overall_impression}")
        
        return " ".join(narrative)


class MSEWorkflow:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.mse_module = MentalStatusExamModule(db_path)
        self.current_exam_id = None
        self.current_domain = None
    
    def start_mse(self, patient_id: str, session_id: str, examiner: str, template_type: str = "comprehensive") -> Dict[str, Any]:
        self.current_exam_id = self.mse_module.conduct_mental_status_exam(
            patient_id, session_id, examiner, template_type
        )
        
        template = self.mse_module.mse_templates[template_type]
        
        return {
            "exam_id": self.current_exam_id,
            "template_used": template_type,
            "domains_to_assess": [domain.value for domain in template.domains_included],
            "estimated_duration": "30-45 minutes" if template_type == "comprehensive" else "10-15 minutes",
            "next_domain": template.domains_included[0].value,
            "instructions": f"Beginning {template.template_name}"
        }
    
    def assess_domain(self, domain: MSEDomain, observations: Dict[str, Any]) -> Dict[str, Any]:
        if not self.current_exam_id:
            return {"error": "No active MSE session"}
        
        success = False
        
        if domain == MSEDomain.APPEARANCE:
            success = self.mse_module.update_appearance_observations(self.current_exam_id, observations)
        elif domain == MSEDomain.BEHAVIOR:
            success = self.mse_module.update_behavior_observations(self.current_exam_id, observations)
        elif domain == MSEDomain.SPEECH:
            success = self.mse_module.update_speech_observations(self.current_exam_id, observations)
        elif domain == MSEDomain.MOOD:
            success = self.mse_module.update_mood_affect_observations(self.current_exam_id, observations)
        elif domain == MSEDomain.THOUGHT_PROCESS or domain == MSEDomain.THOUGHT_CONTENT:
            success = self.mse_module.update_thought_observations(self.current_exam_id, observations)
        elif domain == MSEDomain.PERCEPTION:
            success = self.mse_module.update_perception_observations(self.current_exam_id, observations)
        elif domain == MSEDomain.COGNITION:
            success = self.mse_module.update_cognition_observations(self.current_exam_id, observations)
        elif domain == MSEDomain.INSIGHT or domain == MSEDomain.JUDGMENT:
            success = self.mse_module.update_insight_judgment_observations(self.current_exam_id, observations)
        
        if success:
            self.current_domain = domain
            return {
                "domain_completed": True,
                "domain": domain.value,
                "observations_recorded": len(observations),
                "next_steps": self._determine_next_steps(domain)
            }
        else:
            return {
                "domain_completed": False,
                "error": "Failed to record observations"
            }
    
    def conduct_cognitive_test(self, test_name: str, responses: Dict[str, Any]) -> Dict[str, Any]:
        if not self.current_exam_id:
            return {"error": "No active MSE session"}
        
        result = self.mse_module.conduct_cognitive_screening(self.current_exam_id, test_name, responses)
        
        if "error" not in result:
            return {
                "test_completed": True,
                "test_name": test_name,
                "raw_score": result["raw_score"],
                "max_score": result["max_score"],
                "interpretation": result["interpretation"],
                "areas_of_concern": result.get("areas_of_concern", []),
                "recommendations": result.get("recommendations", [])
            }
        else:
            return result
    
    def finalize_mse(self, overall_impression: str, clinical_significance: List[str], 
                    recommendations: List[str]) -> Dict[str, Any]:
        if not self.current_exam_id:
            return {"error": "No active MSE session"}
        
        exam = self.mse_module._get_mental_status_exam(self.current_exam_id)
        if exam:
            exam.overall_impression = overall_impression
            exam.clinical_significance = clinical_significance
            exam.recommendations = recommendations
            self.mse_module._save_mental_status_exam(exam)
        
        summary = self.mse_module.generate_mse_summary(self.current_exam_id)
        crisis_indicators = summary.get("crisis_indicators", [])
        
        self.current_exam_id = None
        self.current_domain = None
        
        return {
            "mse_completed": True,
            "summary": summary,
            "crisis_indicators": crisis_indicators,
            "requires_immediate_attention": len(crisis_indicators) > 0,
            "recommendations": recommendations
        }
    
    def _determine_next_steps(self, completed_domain: MSEDomain) -> List[str]:
        domain_order = [
            MSEDomain.APPEARANCE,
            MSEDomain.BEHAVIOR,
            MSEDomain.SPEECH,
            MSEDomain.MOOD,
            MSEDomain.AFFECT,
            MSEDomain.THOUGHT_PROCESS,
            MSEDomain.THOUGHT_CONTENT,
            MSEDomain.PERCEPTION,
            MSEDomain.COGNITION,
            MSEDomain.INSIGHT,
            MSEDomain.JUDGMENT
        ]
        
        try:
            current_index = domain_order.index(completed_domain)
            if current_index + 1 < len(domain_order):
                next_domain = domain_order[current_index + 1]
                return [f"Proceed to assess {next_domain.value}"]
            else:
                return ["Complete MSE with overall impression and recommendations"]
        except ValueError:
            return ["Continue with remaining MSE domains"]
    
    def get_mse_progress(self) -> Dict[str, Any]:
        if not self.current_exam_id:
            return {"error": "No active MSE session"}
        
        exam = self.mse_module._get_mental_status_exam(self.current_exam_id)
        if not exam:
            return {"error": "MSE session not found"}
        
        completed_domains = []
        if exam.appearance.overall_appearance:
            completed_domains.append("appearance")
        if exam.behavior.attitude:
            completed_domains.append("behavior")
        if exam.speech.rate:
            completed_domains.append("speech")
        if exam.mood_affect.stated_mood:
            completed_domains.append("mood_affect")
        if exam.thought.process:
            completed_domains.append("thought")
        if exam.perception.hallucinations_present is not None:
            completed_domains.append("perception")
        if exam.cognition.orientation_person is not None:
            completed_domains.append("cognition")
        if exam.insight_judgment.illness_awareness:
            completed_domains.append("insight_judgment")
        
        total_domains = 8
        completion_percentage = (len(completed_domains) / total_domains) * 100
        
        return {
            "exam_id": self.current_exam_id,
            "completed_domains": completed_domains,
            "completion_percentage": completion_percentage,
            "remaining_domains": [domain for domain in [
                "appearance", "behavior", "speech", "mood_affect", 
                "thought", "perception", "cognition", "insight_judgment"
            ] if domain not in completed_domains]
        }


class MSEAnalytics:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.mse_module = MentalStatusExamModule(db_path)
    
    def analyze_patient_mse_trends(self, patient_id: str) -> Dict[str, Any]:
        history = self.mse_module.get_patient_mse_history(patient_id)
        
        if len(history) < 2:
            return {"error": "Insufficient data for trend analysis"}
        
        trends = {
            "mood_trends": self._analyze_mood_trends(patient_id),
            "cognitive_trends": self._analyze_cognitive_trends(patient_id),
            "crisis_pattern": self._analyze_crisis_patterns(patient_id),
            "improvement_indicators": self._identify_improvement_indicators(patient_id),
            "concerning_patterns": self._identify_concerning_patterns(patient_id)
        }
        
        return trends
    
    def _analyze_mood_trends(self, patient_id: str) -> Dict[str, Any]:
        with sqlite3.connect(self.mse_module.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT exam_date, mood_affect_data 
                FROM mental_status_exams 
                WHERE patient_id = ? 
                ORDER BY exam_date
            """, (patient_id,))
            rows = cursor.fetchall()
        
        mood_data = []
        for row in rows:
            mood_affect = json.loads(row[1]) if row[1] else {}
            mood_data.append({
                "date": row[0],
                "observed_mood": mood_affect.get("observed_mood", "euthymic"),
                "affect_type": mood_affect.get("affect_type", "euthymic")
            })
        
        return {
            "mood_progression": mood_data,
            "stability": self._assess_mood_stability(mood_data),
            "predominant_mood": self._find_predominant_mood(mood_data)
        }
    
    def _analyze_cognitive_trends(self, patient_id: str) -> Dict[str, Any]:
        with sqlite3.connect(self.mse_module.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT mse.exam_date, mse.cognition_data, cog.raw_score, cog.test_name
                FROM mental_status_exams mse
                LEFT JOIN cognitive_assessments cog ON mse.exam_id = cog.exam_id
                WHERE mse.patient_id = ? 
                ORDER BY mse.exam_date
            """, (patient_id,))
            rows = cursor.fetchall()
        
        cognitive_data = []
        for row in rows:
            cognition = json.loads(row[1]) if row[1] else {}
            cognitive_data.append({
                "date": row[0],
                "orientation_score": sum([
                    cognition.get("orientation_person", True),
                    cognition.get("orientation_place", True),
                    cognition.get("orientation_time", True),
                    cognition.get("orientation_situation", True)
                ]),
                "attention_level": cognition.get("attention_concentration", "intact"),
                "memory_level": cognition.get("memory_recent", "intact"),
                "test_score": row[2],
                "test_name": row[3]
            })
        
        return {
            "cognitive_progression": cognitive_data,
            "decline_indicators": self._assess_cognitive_decline(cognitive_data),
            "areas_of_concern": self._identify_cognitive_concerns(cognitive_data)
        }
    
    def _analyze_crisis_patterns(self, patient_id: str) -> Dict[str, Any]:
        with sqlite3.connect(self.mse_module.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT exam_date, thought_data, clinical_significance
                FROM mental_status_exams 
                WHERE patient_id = ? 
                ORDER BY exam_date
            """, (patient_id,))
            rows = cursor.fetchall()
        
        crisis_episodes = []
        for row in rows:
            thought_data = json.loads(row[1]) if row[1] else {}
            clinical_sig = json.loads(row[2]) if row[2] else []
            
            has_crisis = (
                thought_data.get("suicidal_thoughts", {}).get("present", False) or
                thought_data.get("homicidal_thoughts", {}).get("present", False) or
                any("crisis" in sig.lower() for sig in clinical_sig)
            )
            
            if has_crisis:
                crisis_episodes.append({
                    "date": row[0],
                    "suicidal_ideation": thought_data.get("suicidal_thoughts", {}).get("present", False),
                    "homicidal_ideation": thought_data.get("homicidal_thoughts", {}).get("present", False),
                    "crisis_indicators": clinical_sig
                })
        
        return {
            "crisis_episodes": crisis_episodes,
            "frequency": len(crisis_episodes),
            "pattern_analysis": self._identify_crisis_patterns(crisis_episodes)
        }
    
    def _assess_mood_stability(self, mood_data: List[Dict[str, Any]]) -> str:
        if len(mood_data) < 3:
            return "insufficient_data"
        
        mood_changes = 0
        for i in range(1, len(mood_data)):
            if mood_data[i]["observed_mood"] != mood_data[i-1]["observed_mood"]:
                mood_changes += 1
        
        change_rate = mood_changes / (len(mood_data) - 1)
        
        if change_rate > 0.7:
            return "highly_unstable"
        elif change_rate > 0.4:
            return "moderately_unstable"
        elif change_rate > 0.2:
            return "mildly_unstable"
        else:
            return "stable"
    
    def _find_predominant_mood(self, mood_data: List[Dict[str, Any]]) -> str:
        mood_counts = {}
        for data in mood_data:
            mood = data["observed_mood"]
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        return max(mood_counts, key=mood_counts.get) if mood_counts else "unknown"
    
    def _assess_cognitive_decline(self, cognitive_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        if len(cognitive_data) < 2:
            return {"decline_detected": False}
        
        orientation_scores = [data["orientation_score"] for data in cognitive_data]
        test_scores = [data["test_score"] for data in cognitive_data if data["test_score"] is not None]
        
        decline_indicators = []
        
        if len(orientation_scores) >= 2:
            if orientation_scores[-1] < orientation_scores[0]:
                decline_indicators.append("orientation_decline")
        
        if len(test_scores) >= 2:
            if test_scores[-1] < test_scores[0] - 2:  # 2-point decline threshold
                decline_indicators.append("test_score_decline")
        
        return {
            "decline_detected": len(decline_indicators) > 0,
            "decline_indicators": decline_indicators,
            "severity": "mild" if len(decline_indicators) == 1 else "moderate" if len(decline_indicators) == 2 else "severe"
        }
    
    def _identify_cognitive_concerns(self, cognitive_data: List[Dict[str, Any]]) -> List[str]:
        concerns = []
        
        if cognitive_data:
            latest = cognitive_data[-1]
            
            if latest["orientation_score"] < 4:
                concerns.append("orientation_impairment")
            
            if latest["attention_level"] in ["mildly_impaired", "moderately_impaired", "severely_impaired"]:
                concerns.append("attention_deficits")
            
            if latest["memory_level"] in ["mildly_impaired", "moderately_impaired", "severely_impaired"]:
                concerns.append("memory_impairment")
        
        return concerns
    
    def _identify_crisis_patterns(self, crisis_episodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        if len(crisis_episodes) < 2:
            return {"pattern": "insufficient_data"}
        
        intervals = []
        for i in range(1, len(crisis_episodes)):
            date1 = datetime.fromisoformat(crisis_episodes[i-1]["date"])
            date2 = datetime.fromisoformat(crisis_episodes[i]["date"])
            intervals.append((date2 - date1).days)
        
        avg_interval = sum(intervals) / len(intervals) if intervals else 0
        
        if avg_interval < 30:
            pattern = "frequent_episodes"
        elif avg_interval < 90:
            pattern = "moderate_frequency"
        else:
            pattern = "sporadic_episodes"
        
        return {
            "pattern": pattern,
            "average_interval_days": avg_interval,
            "escalation_trend": self._assess_crisis_escalation(crisis_episodes)
        }
    
    def _assess_crisis_escalation(self, crisis_episodes: List[Dict[str, Any]]) -> str:
        if len(crisis_episodes) < 3:
            return "insufficient_data"
        
        recent_episodes = crisis_episodes[-3:]
        severity_scores = []
        
        for episode in recent_episodes:
            score = 0
            if episode["suicidal_ideation"]:
                score += 3
            if episode["homicidal_ideation"]:
                score += 3
            score += len(episode.get("crisis_indicators", []))
            severity_scores.append(score)
        
        if severity_scores[-1] > severity_scores[0]:
            return "escalating"
        elif severity_scores[-1] < severity_scores[0]:
            return "de_escalating"
        else:
            return "stable"
    
    def _identify_improvement_indicators(self, patient_id: str) -> List[str]:
        improvements = []
        
        mood_trends = self._analyze_mood_trends(patient_id)
        if mood_trends["stability"] in ["stable", "mildly_unstable"]:
            improvements.append("mood_stabilization")
        
        cognitive_trends = self._analyze_cognitive_trends(patient_id)
        if not cognitive_trends["decline_indicators"]["decline_detected"]:
            improvements.append("cognitive_stability")
        
        crisis_patterns = self._analyze_crisis_patterns(patient_id)
        if crisis_patterns["frequency"] == 0:
            improvements.append("crisis_resolution")
        elif len(crisis_patterns["crisis_episodes"]) > 0:
            if crisis_patterns["pattern_analysis"]["escalation_trend"] == "de_escalating":
                improvements.append("crisis_de_escalation")
        
        return improvements
    
    def _identify_concerning_patterns(self, patient_id: str) -> List[str]:
        concerns = []
        
        mood_trends = self._analyze_mood_trends(patient_id)
        if mood_trends["stability"] == "highly_unstable":
            concerns.append("mood_instability")
        
        cognitive_trends = self._analyze_cognitive_trends(patient_id)
        if cognitive_trends["decline_indicators"]["decline_detected"]:
            concerns.append("cognitive_decline")
        
        crisis_patterns = self._analyze_crisis_patterns(patient_id)
        if crisis_patterns["frequency"] > 0:
            if crisis_patterns["pattern_analysis"]["escalation_trend"] == "escalating":
                concerns.append("escalating_crisis_risk")
            if crisis_patterns["pattern_analysis"]["pattern"] == "frequent_episodes":
                concerns.append("frequent_crisis_episodes")
        
        return concerns
    
    def generate_longitudinal_report(self, patient_id: str) -> str:
        trends = self.analyze_patient_mse_trends(patient_id)
        
        if "error" in trends:
            return trends["error"]
        
        report_sections = []
        
        report_sections.append("LONGITUDINAL MENTAL STATUS ANALYSIS")
        report_sections.append(f"Patient ID: {patient_id}")
        report_sections.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d')}")
        report_sections.append("")
        
        report_sections.append("MOOD TRENDS:")
        mood_trends = trends["mood_trends"]
        report_sections.append(f"Mood Stability: {mood_trends['stability'].replace('_', ' ').title()}")
        report_sections.append(f"Predominant Mood: {mood_trends['predominant_mood'].replace('_', ' ').title()}")
        report_sections.append("")
        
        report_sections.append("COGNITIVE TRENDS:")
        cognitive_trends = trends["cognitive_trends"]
        if cognitive_trends["decline_indicators"]["decline_detected"]:
            report_sections.append(f"Cognitive Decline Detected: {cognitive_trends['decline_indicators']['severity']}")
            report_sections.append(f"Areas of Concern: {', '.join(cognitive_trends['areas_of_concern'])}")
        else:
            report_sections.append("No significant cognitive decline detected")
        report_sections.append("")
        
        report_sections.append("CRISIS PATTERNS:")
        crisis_patterns = trends["crisis_pattern"]
        if crisis_patterns["frequency"] > 0:
            report_sections.append(f"Crisis Episodes: {crisis_patterns['frequency']}")
            report_sections.append(f"Pattern: {crisis_patterns['pattern_analysis']['pattern'].replace('_', ' ').title()}")
            report_sections.append(f"Trend: {crisis_patterns['pattern_analysis']['escalation_trend'].replace('_', ' ').title()}")
        else:
            report_sections.append("No crisis episodes identified")
        report_sections.append("")
        
        improvements = trends["improvement_indicators"]
        if improvements:
            report_sections.append("IMPROVEMENT INDICATORS:")
            for improvement in improvements:
                report_sections.append(f"• {improvement.replace('_', ' ').title()}")
            report_sections.append("")
        
        concerns = trends["concerning_patterns"]
        if concerns:
            report_sections.append("CONCERNING PATTERNS:")
            for concern in concerns:
                report_sections.append(f"• {concern.replace('_', ' ').title()}")
            report_sections.append("")
        
        report_sections.append("CLINICAL RECOMMENDATIONS:")
        if concerns:
            if "mood_instability" in concerns:
                report_sections.append("• Consider mood stabilizing interventions")
            if "cognitive_decline" in concerns:
                report_sections.append("• Neuropsychological evaluation recommended")
            if "escalating_crisis_risk" in concerns:
                report_sections.append("• Intensive safety planning and monitoring required")
        else:
            report_sections.append("• Continue current treatment approach")
            report_sections.append("• Regular monitoring with standard MSE intervals")
        
        return "\n".join(report_sections)
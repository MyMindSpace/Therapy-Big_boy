from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import sqlite3
import json
import uuid
from datetime import datetime, date


class AssessmentType(Enum):
    SCREENING = "screening"
    DIAGNOSTIC = "diagnostic"
    PROGRESS = "progress"
    OUTCOME = "outcome"
    RISK = "risk"


class ResponseFormat(Enum):
    LIKERT_4 = "likert_4_point"
    LIKERT_5 = "likert_5_point"
    LIKERT_7 = "likert_7_point"
    YES_NO = "yes_no"
    MULTIPLE_CHOICE = "multiple_choice"
    OPEN_TEXT = "open_text"
    NUMERIC = "numeric"
    SCALE_0_10 = "scale_0_10"


class SeverityLevel(Enum):
    MINIMAL = "minimal"
    MILD = "mild"
    MODERATE = "moderate"
    MODERATELY_SEVERE = "moderately_severe"
    SEVERE = "severe"


@dataclass
class AssessmentItem:
    item_id: str
    text: str
    response_format: ResponseFormat
    options: List[str] = field(default_factory=list)
    reverse_scored: bool = False
    subscale: Optional[str] = None
    clinical_significance: str = "routine"
    required: bool = True


@dataclass
class AssessmentScale:
    scale_name: str
    items: List[str]
    scoring_method: str
    clinical_cutoffs: Dict[str, float] = field(default_factory=dict)
    reliability: Optional[float] = None
    validity_info: str = ""


@dataclass
class AssessmentResponse:
    item_id: str
    response: Union[str, int, float, bool]
    response_time: Optional[float] = None
    confidence: Optional[int] = None
    notes: str = ""


@dataclass
class AssessmentResult:
    assessment_id: str
    template_id: str
    patient_id: str
    administered_date: datetime
    responses: Dict[str, AssessmentResponse] = field(default_factory=dict)
    scale_scores: Dict[str, float] = field(default_factory=dict)
    percentile_scores: Dict[str, float] = field(default_factory=dict)
    severity_levels: Dict[str, str] = field(default_factory=dict)
    clinical_interpretation: str = ""
    recommendations: List[str] = field(default_factory=list)
    risk_flags: List[str] = field(default_factory=list)
    completed: bool = False
    total_score: float = 0.0
    administration_time: Optional[int] = None


@dataclass
class StandardizedTest:
    test_id: str
    name: str
    version: str
    assessment_type: AssessmentType
    items: List[AssessmentItem]
    scales: List[AssessmentScale]
    administration_time: int
    target_population: str
    purpose: str
    instructions: str
    scoring_instructions: str
    interpretation_guidelines: Dict[str, str]
    references: List[str] = field(default_factory=list)


class StandardizedTestsModule:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.tests = self._initialize_standardized_tests()
        self.scoring_algorithms = self._initialize_scoring_algorithms()
        self.interpretation_rules = self._initialize_interpretation_rules()
        self.clinical_cutoffs = self._initialize_clinical_cutoffs()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS assessment_results (
                    assessment_id TEXT PRIMARY KEY,
                    template_id TEXT NOT NULL,
                    patient_id TEXT NOT NULL,
                    administered_date TEXT NOT NULL,
                    responses TEXT,
                    scale_scores TEXT,
                    percentile_scores TEXT,
                    severity_levels TEXT,
                    clinical_interpretation TEXT,
                    recommendations TEXT,
                    risk_flags TEXT,
                    completed BOOLEAN,
                    total_score REAL,
                    administration_time INTEGER,
                    created_date TEXT,
                    last_updated TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS assessment_sessions (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    assessment_date TEXT NOT NULL,
                    assessments_completed TEXT,
                    session_duration INTEGER,
                    completion_status TEXT,
                    clinical_notes TEXT,
                    administered_by TEXT,
                    created_date TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS progress_tracking (
                    tracking_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    test_type TEXT NOT NULL,
                    assessment_dates TEXT,
                    scores TEXT,
                    trend_analysis TEXT,
                    clinical_significance TEXT,
                    last_updated TEXT
                )
            """)
    
    def _initialize_standardized_tests(self) -> Dict[str, StandardizedTest]:
        tests = {}
        
        # PHQ-9 (Patient Health Questionnaire-9)
        tests["PHQ9"] = StandardizedTest(
            test_id="PHQ9",
            name="Patient Health Questionnaire-9",
            version="1.0",
            assessment_type=AssessmentType.SCREENING,
            items=[
                AssessmentItem(
                    item_id="PHQ9_1",
                    text="Little interest or pleasure in doing things",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="depression_severity"
                ),
                AssessmentItem(
                    item_id="PHQ9_2",
                    text="Feeling down, depressed, or hopeless",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="depression_severity",
                    clinical_significance="high"
                ),
                AssessmentItem(
                    item_id="PHQ9_3",
                    text="Trouble falling or staying asleep, or sleeping too much",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="depression_severity"
                ),
                AssessmentItem(
                    item_id="PHQ9_4",
                    text="Feeling tired or having little energy",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="depression_severity"
                ),
                AssessmentItem(
                    item_id="PHQ9_5",
                    text="Poor appetite or overeating",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="depression_severity"
                ),
                AssessmentItem(
                    item_id="PHQ9_6",
                    text="Feeling bad about yourself - or that you are a failure or have let yourself or your family down",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="depression_severity"
                ),
                AssessmentItem(
                    item_id="PHQ9_7",
                    text="Trouble concentrating on things, such as reading the newspaper or watching television",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="depression_severity"
                ),
                AssessmentItem(
                    item_id="PHQ9_8",
                    text="Moving or speaking so slowly that other people could have noticed. Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="depression_severity"
                ),
                AssessmentItem(
                    item_id="PHQ9_9",
                    text="Thoughts that you would be better off dead, or of hurting yourself in some way",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="depression_severity",
                    clinical_significance="critical"
                ),
                AssessmentItem(
                    item_id="PHQ9_10",
                    text="If you checked off any problems, how difficult have these problems made it for you to do your work, take care of things at home, or get along with other people?",
                    response_format=ResponseFormat.MULTIPLE_CHOICE,
                    options=["Not difficult at all", "Somewhat difficult", "Very difficult", "Extremely difficult"],
                    subscale="functional_impairment"
                )
            ],
            scales=[
                AssessmentScale(
                    scale_name="Depression Severity",
                    items=["PHQ9_1", "PHQ9_2", "PHQ9_3", "PHQ9_4", "PHQ9_5", "PHQ9_6", "PHQ9_7", "PHQ9_8", "PHQ9_9"],
                    scoring_method="sum",
                    clinical_cutoffs={
                        "minimal": 4.0,
                        "mild": 9.0,
                        "moderate": 14.0,
                        "moderately_severe": 19.0,
                        "severe": 27.0
                    },
                    reliability=0.89
                )
            ],
            administration_time=5,
            target_population="Adults",
            purpose="Depression screening and severity assessment",
            instructions="Over the last 2 weeks, how often have you been bothered by any of the following problems?",
            scoring_instructions="Sum scores for items 1-9. Item 10 assesses functional impairment.",
            interpretation_guidelines={
                "0-4": "Minimal depression",
                "5-9": "Mild depression",
                "10-14": "Moderate depression",
                "15-19": "Moderately severe depression",
                "20-27": "Severe depression"
            },
            references=["Kroenke, K., Spitzer, R. L., & Williams, J. B. (2001). The PHQ-9."]
        )
        
        # GAD-7 (Generalized Anxiety Disorder-7)
        tests["GAD7"] = StandardizedTest(
            test_id="GAD7",
            name="Generalized Anxiety Disorder-7",
            version="1.0",
            assessment_type=AssessmentType.SCREENING,
            items=[
                AssessmentItem(
                    item_id="GAD7_1",
                    text="Feeling nervous, anxious, or on edge",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="anxiety_severity"
                ),
                AssessmentItem(
                    item_id="GAD7_2",
                    text="Not being able to stop or control worrying",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="anxiety_severity",
                    clinical_significance="high"
                ),
                AssessmentItem(
                    item_id="GAD7_3",
                    text="Worrying too much about different things",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="anxiety_severity"
                ),
                AssessmentItem(
                    item_id="GAD7_4",
                    text="Trouble relaxing",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="anxiety_severity"
                ),
                AssessmentItem(
                    item_id="GAD7_5",
                    text="Being so restless that it is hard to sit still",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="anxiety_severity"
                ),
                AssessmentItem(
                    item_id="GAD7_6",
                    text="Becoming easily annoyed or irritable",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="anxiety_severity"
                ),
                AssessmentItem(
                    item_id="GAD7_7",
                    text="Feeling afraid, as if something awful might happen",
                    response_format=ResponseFormat.LIKERT_4,
                    options=["Not at all", "Several days", "More than half the days", "Nearly every day"],
                    subscale="anxiety_severity",
                    clinical_significance="high"
                )
            ],
            scales=[
                AssessmentScale(
                    scale_name="Anxiety Severity",
                    items=["GAD7_1", "GAD7_2", "GAD7_3", "GAD7_4", "GAD7_5", "GAD7_6", "GAD7_7"],
                    scoring_method="sum",
                    clinical_cutoffs={
                        "minimal": 4.0,
                        "mild": 9.0,
                        "moderate": 14.0,
                        "severe": 21.0
                    },
                    reliability=0.92
                )
            ],
            administration_time=3,
            target_population="Adults",
            purpose="Anxiety screening and severity assessment",
            instructions="Over the last 2 weeks, how often have you been bothered by any of the following problems?",
            scoring_instructions="Sum scores for all 7 items.",
            interpretation_guidelines={
                "0-4": "Minimal anxiety",
                "5-9": "Mild anxiety",
                "10-14": "Moderate anxiety",
                "15-21": "Severe anxiety"
            },
            references=["Spitzer, R. L., Kroenke, K., Williams, J. B., & Löwe, B. (2006). GAD-7."]
        )
        
        # PCL-5 (PTSD Checklist for DSM-5)
        tests["PCL5"] = StandardizedTest(
            test_id="PCL5",
            name="PTSD Checklist for DSM-5",
            version="1.0",
            assessment_type=AssessmentType.DIAGNOSTIC,
            items=[
                AssessmentItem(
                    item_id="PCL5_1",
                    text="Repeated, disturbing, and unwanted memories of the stressful experience",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="intrusion"
                ),
                AssessmentItem(
                    item_id="PCL5_2",
                    text="Repeated, disturbing dreams of the stressful experience",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="intrusion"
                ),
                AssessmentItem(
                    item_id="PCL5_3",
                    text="Suddenly feeling or acting as if the stressful experience were actually happening again",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="intrusion",
                    clinical_significance="high"
                ),
                AssessmentItem(
                    item_id="PCL5_4",
                    text="Feeling very upset when something reminded you of the stressful experience",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="intrusion"
                ),
                AssessmentItem(
                    item_id="PCL5_5",
                    text="Having strong physical reactions when something reminded you of the stressful experience",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="intrusion"
                ),
                AssessmentItem(
                    item_id="PCL5_6",
                    text="Avoiding memories, thoughts, or feelings related to the stressful experience",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="avoidance"
                ),
                AssessmentItem(
                    item_id="PCL5_7",
                    text="Avoiding external reminders of the stressful experience",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="avoidance"
                ),
                AssessmentItem(
                    item_id="PCL5_8",
                    text="Trouble remembering important parts of the stressful experience",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="negative_cognition"
                ),
                AssessmentItem(
                    item_id="PCL5_9",
                    text="Having strong negative beliefs about yourself, other people, or the world",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="negative_cognition"
                ),
                AssessmentItem(
                    item_id="PCL5_10",
                    text="Blaming yourself or someone else for the stressful experience or what happened after it",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="negative_cognition"
                ),
                AssessmentItem(
                    item_id="PCL5_11",
                    text="Having strong negative feelings such as fear, horror, anger, guilt, or shame",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="negative_cognition"
                ),
                AssessmentItem(
                    item_id="PCL5_12",
                    text="Loss of interest in activities that you used to enjoy",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="negative_cognition"
                ),
                AssessmentItem(
                    item_id="PCL5_13",
                    text="Feeling distant or cut off from other people",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="negative_cognition"
                ),
                AssessmentItem(
                    item_id="PCL5_14",
                    text="Trouble experiencing positive feelings",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="negative_cognition"
                ),
                AssessmentItem(
                    item_id="PCL5_15",
                    text="Irritable behavior, angry outbursts, or acting aggressively",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="arousal"
                ),
                AssessmentItem(
                    item_id="PCL5_16",
                    text="Taking too many risks or doing things that could cause you harm",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="arousal"
                ),
                AssessmentItem(
                    item_id="PCL5_17",
                    text="Being super alert or watchful or on guard",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="arousal"
                ),
                AssessmentItem(
                    item_id="PCL5_18",
                    text="Feeling jumpy or easily startled",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="arousal"
                ),
                AssessmentItem(
                    item_id="PCL5_19",
                    text="Having difficulty concentrating",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="arousal"
                ),
                AssessmentItem(
                    item_id="PCL5_20",
                    text="Trouble falling or staying asleep",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="arousal"
                )
            ],
            scales=[
                AssessmentScale(
                    scale_name="PTSD Total",
                    items=[f"PCL5_{i}" for i in range(1, 21)],
                    scoring_method="sum",
                    clinical_cutoffs={
                        "probable_ptsd": 33.0,
                        "severe_ptsd": 50.0
                    },
                    reliability=0.97
                ),
                AssessmentScale(
                    scale_name="Intrusion",
                    items=["PCL5_1", "PCL5_2", "PCL5_3", "PCL5_4", "PCL5_5"],
                    scoring_method="sum",
                    clinical_cutoffs={"moderate": 8.0}
                ),
                AssessmentScale(
                    scale_name="Avoidance",
                    items=["PCL5_6", "PCL5_7"],
                    scoring_method="sum",
                    clinical_cutoffs={"moderate": 3.0}
                ),
                AssessmentScale(
                    scale_name="Negative Cognition",
                    items=[f"PCL5_{i}" for i in range(8, 15)],
                    scoring_method="sum",
                    clinical_cutoffs={"moderate": 12.0}
                ),
                AssessmentScale(
                    scale_name="Arousal",
                    items=[f"PCL5_{i}" for i in range(15, 21)],
                    scoring_method="sum",
                    clinical_cutoffs={"moderate": 10.0}
                )
            ],
            administration_time=10,
            target_population="Adults with trauma exposure",
            purpose="PTSD screening and severity assessment",
            instructions="Below is a list of problems that people sometimes have in response to a very stressful experience. Please read each problem carefully and then circle one of the numbers to the right to indicate how much you have been bothered by that problem in the past month.",
            scoring_instructions="Sum all items for total score. Subscale scores calculated separately.",
            interpretation_guidelines={
                "0-32": "Below PTSD threshold",
                "33-49": "Probable PTSD",
                "50+": "Severe PTSD symptoms"
            },
            references=["Weathers, F. W., et al. (2013). The PTSD Checklist for DSM-5 (PCL-5)."]
        )
        
        return tests
    
    def _initialize_scoring_algorithms(self) -> Dict[str, Dict[str, Any]]:
        return {
            "PHQ9": {
                "total_score": {"method": "sum", "items": [f"PHQ9_{i}" for i in range(1, 10)]},
                "severity_levels": {
                    (0, 4): "minimal",
                    (5, 9): "mild",
                    (10, 14): "moderate",
                    (15, 19): "moderately_severe",
                    (20, 27): "severe"
                }
            },
            "GAD7": {
                "total_score": {"method": "sum", "items": [f"GAD7_{i}" for i in range(1, 8)]},
                "severity_levels": {
                    (0, 4): "minimal",
                    (5, 9): "mild",
                    (10, 14): "moderate",
                    (15, 21): "severe"
                }
            },
            "PCL5": {
                "total_score": {"method": "sum", "items": [f"PCL5_{i}" for i in range(1, 21)]},
                "severity_levels": {
                    (0, 32): "below_threshold",
                    (33, 49): "probable_ptsd",
                    (50, 80): "severe_ptsd"
                }
            }
        }
    
    def _initialize_interpretation_rules(self) -> Dict[str, Dict[str, Any]]:
        return {
            "PHQ9": {
                "minimal": {
                    "description": "Minimal depression",
                    "recommendations": ["Monitor symptoms", "Psychoeducation about depression"],
                    "follow_up": "3-6 months"
                },
                "mild": {
                    "description": "Mild depression",
                    "recommendations": ["Psychotherapy", "Lifestyle interventions", "Monitor closely"],
                    "follow_up": "4-6 weeks"
                },
                "moderate": {
                    "description": "Moderate depression",
                    "recommendations": ["Psychotherapy", "Consider medication", "Regular monitoring"],
                    "follow_up": "2-4 weeks"
                },
                "moderately_severe": {
                    "description": "Moderately severe depression",
                    "recommendations": ["Psychotherapy", "Medication evaluation", "Close monitoring"],
                    "follow_up": "1-2 weeks"
                },
                "severe": {
                    "description": "Severe depression",
                    "recommendations": ["Immediate treatment", "Medication", "Safety assessment", "Intensive therapy"],
                    "follow_up": "Weekly or more frequent"
                }
            },
            "GAD7": {
                "minimal": {
                    "description": "Minimal anxiety",
                    "recommendations": ["Monitor symptoms", "Stress management education"],
                    "follow_up": "3-6 months"
                },
                "mild": {
                    "description": "Mild anxiety",
                    "recommendations": ["Psychotherapy", "Relaxation techniques", "Lifestyle modifications"],
                    "follow_up": "4-6 weeks"
                },
                "moderate": {
                    "description": "Moderate anxiety",
                    "recommendations": ["Psychotherapy", "Consider medication", "Regular monitoring"],
                    "follow_up": "2-4 weeks"
                },
                "severe": {
                    "description": "Severe anxiety",
                    "recommendations": ["Immediate treatment", "Medication evaluation", "Intensive therapy"],
                    "follow_up": "Weekly"
                }
            },
            "PCL5": {
                "below_threshold": {
                    "description": "Below PTSD threshold",
                    "recommendations": ["Monitor symptoms", "Trauma-informed care"],
                    "follow_up": "3-6 months"
                },
                "probable_ptsd": {
                    "description": "Probable PTSD",
                    "recommendations": ["Trauma-focused therapy", "Comprehensive assessment", "Safety planning"],
                    "follow_up": "2-4 weeks"
                },
                "severe_ptsd": {
                    "description": "Severe PTSD symptoms",
                    "recommendations": ["Intensive trauma therapy", "Medication evaluation", "Safety assessment", "Crisis planning"],
                    "follow_up": "Weekly"
                }
            }
        }
    
    def _initialize_clinical_cutoffs(self) -> Dict[str, Dict[str, float]]:
        return {
            "PHQ9": {
                "minimal": 4.0,
                "mild": 9.0,
                "moderate": 14.0,
                "moderately_severe": 19.0,
                "severe": 27.0
            },
            "GAD7": {
                "minimal": 4.0,
                "mild": 9.0,
                "moderate": 14.0,
                "severe": 21.0
            },
            "PCL5": {
                "below_threshold": 32.0,
                "probable_ptsd": 49.0,
                "severe_ptsd": 80.0
            }
        }
    
    def create_assessment_instance(self, test_id: str, patient_id: str) -> AssessmentResult:
        if test_id not in self.tests:
            raise ValueError(f"Test {test_id} not found")
        
        assessment_id = str(uuid.uuid4())
        
        return AssessmentResult(
            assessment_id=assessment_id,
            template_id=test_id,
            patient_id=patient_id,
            administered_date=datetime.now()
        )
    
    def record_response(self, assessment: AssessmentResult, item_id: str, 
                       response: Union[str, int, float, bool], notes: str = "") -> bool:
        if item_id not in [item.item_id for item in self.tests[assessment.template_id].items]:
            return False
        
        assessment.responses[item_id] = AssessmentResponse(
            item_id=item_id,
            response=response,
            notes=notes
        )
        return True
    
    def score_assessment(self, assessment: AssessmentResult) -> AssessmentResult:
        test = self.tests[assessment.template_id]
        scoring_algorithm = self.scoring_algorithms[assessment.template_id]
        
        # Calculate scale scores
        for scale in test.scales:
            score = self._calculate_scale_score(scale, assessment.responses)
            assessment.scale_scores[scale.scale_name] = score
        
        # Calculate total score
        if "total_score" in scoring_algorithm:
            total_items = scoring_algorithm["total_score"]["items"]
            total_score = sum(
                assessment.responses[item_id].response 
                for item_id in total_items 
                if item_id in assessment.responses and isinstance(assessment.responses[item_id].response, (int, float))
            )
            assessment.total_score = total_score
        
        # Determine severity levels
        assessment.severity_levels = self._determine_severity_levels(assessment)
        
        # Generate interpretation
        assessment.clinical_interpretation = self._generate_interpretation(assessment)
        
        # Generate recommendations
        assessment.recommendations = self._generate_recommendations(assessment)
        
        # Check for risk flags
        assessment.risk_flags = self._check_risk_flags(assessment)
        
        # Mark as completed
        assessment.completed = True
        
        # Save to database
        self._save_assessment_result(assessment)
        
        return assessment
    
    def _calculate_scale_score(self, scale: AssessmentScale, 
                              responses: Dict[str, AssessmentResponse]) -> float:
        scale_responses = []
        for item_id in scale.items:
            if item_id in responses:
                response = responses[item_id].response
                if isinstance(response, (int, float)):
                    scale_responses.append(response)
                elif isinstance(response, str) and response.isdigit():
                    scale_responses.append(float(response))
        
        if not scale_responses:
            return 0.0
        
        if scale.scoring_method == "sum":
            return sum(scale_responses)
        elif scale.scoring_method == "mean":
            return sum(scale_responses) / len(scale_responses)
        elif scale.scoring_method == "max":
            return max(scale_responses)
        else:
            return sum(scale_responses)
    
    def _determine_severity_levels(self, assessment: AssessmentResult) -> Dict[str, str]:
        severity_levels = {}
        algorithm = self.scoring_algorithms[assessment.template_id]
        
        if "severity_levels" in algorithm:
            total_score = assessment.total_score
            for score_range, level in algorithm["severity_levels"].items():
                min_score, max_score = score_range
                if min_score <= total_score <= max_score:
                    severity_levels["overall"] = level
                    break
        
        return severity_levels
    
    def _generate_interpretation(self, assessment: AssessmentResult) -> str:
        template_id = assessment.template_id
        severity = assessment.severity_levels.get("overall", "unknown")
        
        if template_id in self.interpretation_rules and severity in self.interpretation_rules[template_id]:
            rule = self.interpretation_rules[template_id][severity]
            return rule["description"]
        
        return f"Score: {assessment.total_score}"
    
    def _generate_recommendations(self, assessment: AssessmentResult) -> List[str]:
        template_id = assessment.template_id
        severity = assessment.severity_levels.get("overall", "unknown")
        
        if template_id in self.interpretation_rules and severity in self.interpretation_rules[template_id]:
            rule = self.interpretation_rules[template_id][severity]
            return rule.get("recommendations", [])
        
        return []
    
    def _check_risk_flags(self, assessment: AssessmentResult) -> List[str]:
        risk_flags = []
        test = self.tests[assessment.template_id]
        
        # Check for critical item responses
        for item in test.items:
            if item.clinical_significance == "critical" and item.item_id in assessment.responses:
                response = assessment.responses[item.item_id].response
                if isinstance(response, (int, float)) and response > 0:
                    if item.item_id == "PHQ9_9":
                        risk_flags.append("Suicidal ideation reported")
                    elif "PCL5" in item.item_id and response >= 2:
                        risk_flags.append("Significant PTSD symptoms")
        
        # Check severity-based flags
        severity = assessment.severity_levels.get("overall", "unknown")
        if severity in ["severe", "moderately_severe", "severe_ptsd"]:
            risk_flags.append(f"Severe symptoms requiring immediate attention")
        
        return risk_flags
    
    def administer_test_battery(self, patient_id: str, test_ids: List[str]) -> Dict[str, AssessmentResult]:
        session_id = str(uuid.uuid4())
        results = {}
        
        for test_id in test_ids:
            if test_id in self.tests:
                assessment = self.create_assessment_instance(test_id, patient_id)
                results[test_id] = assessment
        
        # Save session info
        self._save_assessment_session(session_id, patient_id, test_ids)
        
        return results
    
    def get_assessment_history(self, patient_id: str, test_id: Optional[str] = None) -> List[AssessmentResult]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if test_id:
                cursor.execute("""
                    SELECT * FROM assessment_results 
                    WHERE patient_id = ? AND template_id = ?
                    ORDER BY administered_date DESC
                """, (patient_id, test_id))
            else:
                cursor.execute("""
                    SELECT * FROM assessment_results 
                    WHERE patient_id = ?
                    ORDER BY administered_date DESC
                """, (patient_id,))
            
            rows = cursor.fetchall()
            assessments = []
            
            for row in rows:
                assessment = AssessmentResult(
                    assessment_id=row[0],
                    template_id=row[1],
                    patient_id=row[2],
                    administered_date=datetime.fromisoformat(row[3]),
                    responses={},
                    scale_scores=json.loads(row[5]) if row[5] else {},
                    severity_levels=json.loads(row[7]) if row[7] else {},
                    clinical_interpretation=row[8] or "",
                    recommendations=json.loads(row[9]) if row[9] else [],
                    risk_flags=json.loads(row[10]) if row[10] else [],
                    completed=row[11],
                    total_score=row[12] or 0.0
                )
                
                if row[4]:  # responses
                    response_data = json.loads(row[4])
                    for item_id, resp_data in response_data.items():
                        assessment.responses[item_id] = AssessmentResponse(
                            item_id=item_id,
                            response=resp_data.get("response"),
                            notes=resp_data.get("notes", "")
                        )
                
                assessments.append(assessment)
            
            return assessments
    
    def analyze_progress(self, patient_id: str, test_id: str) -> Dict[str, Any]:
        history = self.get_assessment_history(patient_id, test_id)
        
        if len(history) < 2:
            return {"error": "Insufficient data for progress analysis"}
        
        # Sort by date
        history.sort(key=lambda x: x.administered_date)
        
        scores = [assessment.total_score for assessment in history]
        dates = [assessment.administered_date for assessment in history]
        
        # Calculate trend
        trend = self._calculate_trend(scores)
        
        # Determine clinical significance of change
        change_significance = self._assess_change_significance(test_id, scores[0], scores[-1])
        
        return {
            "assessment_count": len(history),
            "date_range": {
                "first": dates[0].isoformat(),
                "last": dates[-1].isoformat()
            },
            "scores": {
                "first": scores[0],
                "last": scores[-1],
                "change": scores[-1] - scores[0],
                "percent_change": ((scores[-1] - scores[0]) / scores[0] * 100) if scores[0] > 0 else 0
            },
            "trend": trend,
            "clinical_significance": change_significance,
            "severity_progression": [
                assessment.severity_levels.get("overall", "unknown") 
                for assessment in history
            ]
        }
    
    def _calculate_trend(self, scores: List[float]) -> str:
        if len(scores) < 2:
            return "insufficient_data"
        
        # Simple linear trend calculation
        n = len(scores)
        x = list(range(n))
        
        # Calculate slope
        x_mean = sum(x) / n
        y_mean = sum(scores) / n
        
        numerator = sum((x[i] - x_mean) * (scores[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return "stable"
        
        slope = numerator / denominator
        
        if slope > 0.5:
            return "worsening"
        elif slope < -0.5:
            return "improving"
        else:
            return "stable"
    
    def _assess_change_significance(self, test_id: str, first_score: float, last_score: float) -> str:
        # Reliable change thresholds (simplified)
        reliable_change_thresholds = {
            "PHQ9": 3.0,
            "GAD7": 2.0,
            "PCL5": 5.0
        }
        
        threshold = reliable_change_thresholds.get(test_id, 2.0)
        change = abs(last_score - first_score)
        
        if change >= threshold:
            if last_score < first_score:
                return "clinically_significant_improvement"
            else:
                return "clinically_significant_deterioration"
        else:
            return "no_significant_change"
    
    def generate_assessment_report(self, assessment: AssessmentResult) -> str:
        test = self.tests[assessment.template_id]
        
        report_parts = []
        
        # Header
        report_parts.append(f"{test.name} - Assessment Report")
        report_parts.append("=" * 50)
        report_parts.append(f"Patient ID: {assessment.patient_id}")
        report_parts.append(f"Assessment Date: {assessment.administered_date.strftime('%Y-%m-%d %H:%M')}")
        report_parts.append(f"Total Score: {assessment.total_score}")
        report_parts.append("")
        
        # Severity and interpretation
        severity = assessment.severity_levels.get("overall", "unknown")
        report_parts.append(f"Severity Level: {severity.replace('_', ' ').title()}")
        report_parts.append(f"Clinical Interpretation: {assessment.clinical_interpretation}")
        report_parts.append("")
        
        # Scale scores
        if assessment.scale_scores:
            report_parts.append("Scale Scores:")
            for scale_name, score in assessment.scale_scores.items():
                report_parts.append(f"• {scale_name}: {score}")
            report_parts.append("")
        
        # Risk flags
        if assessment.risk_flags:
            report_parts.append("RISK FLAGS:")
            for flag in assessment.risk_flags:
                report_parts.append(f"⚠ {flag}")
            report_parts.append("")
        
        # Recommendations
        if assessment.recommendations:
            report_parts.append("Clinical Recommendations:")
            for i, rec in enumerate(assessment.recommendations, 1):
                report_parts.append(f"{i}. {rec}")
            report_parts.append("")
        
        # Item-level responses (for clinical review)
        report_parts.append("Item-Level Responses:")
        for item in test.items:
            if item.item_id in assessment.responses:
                response = assessment.responses[item.item_id]
                response_text = response.response
                if isinstance(response.response, int) and item.options:
                    if response.response < len(item.options):
                        response_text = f"{response.response} ({item.options[response.response]})"
                
                report_parts.append(f"{item.item_id}: {response_text}")
                if response.notes:
                    report_parts.append(f"  Notes: {response.notes}")
        
        return "\n".join(report_parts)
    
    def get_test_norms(self, test_id: str, demographic_filters: Dict[str, Any] = None) -> Dict[str, Any]:
        # Simplified normative data - in production, this would query actual norm databases
        norms = {
            "PHQ9": {
                "general_population": {"mean": 2.9, "std": 3.1},
                "clinical_sample": {"mean": 13.2, "std": 6.4},
                "percentiles": {
                    10: 0, 25: 1, 50: 3, 75: 7, 90: 12, 95: 16
                }
            },
            "GAD7": {
                "general_population": {"mean": 2.5, "std": 2.8},
                "clinical_sample": {"mean": 11.8, "std": 5.9},
                "percentiles": {
                    10: 0, 25: 0, 50: 2, 75: 5, 90: 10, 95: 14
                }
            },
            "PCL5": {
                "general_population": {"mean": 8.5, "std": 12.3},
                "clinical_sample": {"mean": 45.2, "std": 18.7},
                "percentiles": {
                    10: 0, 25: 2, 50: 8, 75: 18, 90: 32, 95: 44
                }
            }
        }
        
        return norms.get(test_id, {})
    
    def calculate_percentile_score(self, test_id: str, raw_score: float) -> Optional[float]:
        norms = self.get_test_norms(test_id)
        if "percentiles" not in norms:
            return None
        
        percentiles = norms["percentiles"]
        
        # Find closest percentile
        for percentile in sorted(percentiles.keys(), reverse=True):
            if raw_score >= percentiles[percentile]:
                return float(percentile)
        
        return 0.0
    
    def validate_assessment(self, assessment: AssessmentResult) -> Dict[str, Any]:
        test = self.tests[assessment.template_id]
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "completion_rate": 0.0
        }
        
        # Check completion
        total_items = len(test.items)
        completed_items = len(assessment.responses)
        validation_result["completion_rate"] = (completed_items / total_items) * 100
        
        if completed_items < total_items:
            missing_items = [
                item.item_id for item in test.items 
                if item.item_id not in assessment.responses and item.required
            ]
            if missing_items:
                validation_result["errors"].append(f"Missing required items: {', '.join(missing_items)}")
                validation_result["valid"] = False
        
        # Check response validity
        for item_id, response in assessment.responses.items():
            item = next((item for item in test.items if item.item_id == item_id), None)
            if item:
                if item.response_format in [ResponseFormat.LIKERT_4, ResponseFormat.LIKERT_5]:
                    max_value = 4 if item.response_format == ResponseFormat.LIKERT_4 else 5
                    if not isinstance(response.response, int) or response.response < 0 or response.response >= max_value:
                        validation_result["errors"].append(f"Invalid response for {item_id}: {response.response}")
                        validation_result["valid"] = False
        
        # Check for concerning patterns
        if assessment.template_id == "PHQ9" and "PHQ9_9" in assessment.responses:
            if assessment.responses["PHQ9_9"].response > 0:
                validation_result["warnings"].append("Suicidal ideation reported - requires immediate attention")
        
        return validation_result
    
    def export_assessment_data(self, patient_id: str, format_type: str = "json") -> Union[Dict[str, Any], str]:
        assessments = self.get_assessment_history(patient_id)
        
        if format_type == "json":
            return {
                "patient_id": patient_id,
                "export_date": datetime.now().isoformat(),
                "total_assessments": len(assessments),
                "assessments": [
                    {
                        "assessment_id": a.assessment_id,
                        "test_type": a.template_id,
                        "date": a.administered_date.isoformat(),
                        "total_score": a.total_score,
                        "severity": a.severity_levels.get("overall"),
                        "completed": a.completed
                    } for a in assessments
                ]
            }
        
        elif format_type == "csv":
            csv_lines = ["Assessment_ID,Test_Type,Date,Total_Score,Severity,Completed"]
            for a in assessments:
                csv_lines.append(
                    f"{a.assessment_id},{a.template_id},{a.administered_date.isoformat()},"
                    f"{a.total_score},{a.severity_levels.get('overall', '')},{a.completed}"
                )
            return "\n".join(csv_lines)
        
        return {}
    
    def _save_assessment_result(self, assessment: AssessmentResult):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Prepare responses data
            responses_data = {}
            for item_id, response in assessment.responses.items():
                responses_data[item_id] = {
                    "response": response.response,
                    "notes": response.notes
                }
            
            cursor.execute("""
                INSERT OR REPLACE INTO assessment_results (
                    assessment_id, template_id, patient_id, administered_date,
                    responses, scale_scores, percentile_scores, severity_levels,
                    clinical_interpretation, recommendations, risk_flags,
                    completed, total_score, administration_time,
                    created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id, assessment.template_id, assessment.patient_id,
                assessment.administered_date.isoformat(),
                json.dumps(responses_data), json.dumps(assessment.scale_scores),
                json.dumps(assessment.percentile_scores), json.dumps(assessment.severity_levels),
                assessment.clinical_interpretation, json.dumps(assessment.recommendations),
                json.dumps(assessment.risk_flags), assessment.completed, assessment.total_score,
                assessment.administration_time, datetime.now().isoformat(), datetime.now().isoformat()
            ))
    
    def _save_assessment_session(self, session_id: str, patient_id: str, test_ids: List[str]):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO assessment_sessions (
                    session_id, patient_id, assessment_date, assessments_completed,
                    completion_status, administered_by, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id, patient_id, datetime.now().isoformat(),
                json.dumps(test_ids), "in_progress", "system", datetime.now().isoformat()
            ))


class AssessmentBattery:
    
    def __init__(self, tests_module: StandardizedTestsModule):
        self.tests_module = tests_module
        self.standard_batteries = self._initialize_standard_batteries()
    
    def _initialize_standard_batteries(self) -> Dict[str, Dict[str, Any]]:
        return {
            "depression_screening": {
                "name": "Depression Screening Battery",
                "tests": ["PHQ9"],
                "estimated_time": 5,
                "purpose": "Initial depression screening"
            },
            "anxiety_screening": {
                "name": "Anxiety Screening Battery",
                "tests": ["GAD7"],
                "estimated_time": 3,
                "purpose": "Initial anxiety screening"
            },
            "trauma_screening": {
                "name": "Trauma Screening Battery",
                "tests": ["PCL5"],
                "estimated_time": 10,
                "purpose": "PTSD and trauma-related symptoms screening"
            },
            "comprehensive_screening": {
                "name": "Comprehensive Mental Health Screening",
                "tests": ["PHQ9", "GAD7", "PCL5"],
                "estimated_time": 18,
                "purpose": "Comprehensive assessment of common mental health conditions"
            },
            "progress_monitoring": {
                "name": "Progress Monitoring Battery",
                "tests": ["PHQ9", "GAD7"],
                "estimated_time": 8,
                "purpose": "Monitor treatment progress for depression and anxiety"
            }
        }
    
    def administer_battery(self, battery_name: str, patient_id: str) -> Dict[str, Any]:
        if battery_name not in self.standard_batteries:
            return {"error": f"Battery '{battery_name}' not found"}
        
        battery = self.standard_batteries[battery_name]
        results = self.tests_module.administer_test_battery(patient_id, battery["tests"])
        
        return {
            "battery_name": battery["name"],
            "patient_id": patient_id,
            "tests_administered": battery["tests"],
            "estimated_time": battery["estimated_time"],
            "results": results,
            "administration_date": datetime.now().isoformat()
        }
    
    def get_battery_recommendations(self, presenting_concerns: List[str]) -> List[str]:
        recommendations = []
        concerns_text = " ".join(presenting_concerns).lower()
        
        if any(word in concerns_text for word in ["depressed", "sad", "hopeless", "mood"]):
            recommendations.append("depression_screening")
        
        if any(word in concerns_text for word in ["anxious", "worry", "nervous", "panic"]):
            recommendations.append("anxiety_screening")
        
        if any(word in concerns_text for word in ["trauma", "ptsd", "flashback", "nightmare"]):
            recommendations.append("trauma_screening")
        
        if len(recommendations) == 0:
            recommendations.append("comprehensive_screening")
        elif len(recommendations) > 1:
            recommendations = ["comprehensive_screening"]
        
        return recommendations


class ProgressTracker:
    
    def __init__(self, tests_module: StandardizedTestsModule):
        self.tests_module = tests_module
    
    def track_patient_progress(self, patient_id: str) -> Dict[str, Any]:
        all_assessments = self.tests_module.get_assessment_history(patient_id)
        
        if not all_assessments:
            return {"error": "No assessment data found for patient"}
        
        # Group by test type
        assessments_by_test = {}
        for assessment in all_assessments:
            test_id = assessment.template_id
            if test_id not in assessments_by_test:
                assessments_by_test[test_id] = []
            assessments_by_test[test_id].append(assessment)
        
        # Analyze progress for each test type
        progress_analysis = {}
        for test_id, assessments in assessments_by_test.items():
            if len(assessments) > 1:
                progress_analysis[test_id] = self.tests_module.analyze_progress(patient_id, test_id)
        
        return {
            "patient_id": patient_id,
            "total_assessments": len(all_assessments),
            "test_types": list(assessments_by_test.keys()),
            "progress_analysis": progress_analysis,
            "latest_scores": {
                test_id: assessments[0].total_score
                for test_id, assessments in assessments_by_test.items()
            }
        }
    
    def generate_progress_report(self, patient_id: str) -> str:
        progress_data = self.track_patient_progress(patient_id)
        
        if "error" in progress_data:
            return progress_data["error"]
        
        report_lines = []
        report_lines.append("PATIENT PROGRESS REPORT")
        report_lines.append("=" * 40)
        report_lines.append(f"Patient ID: {patient_id}")
        report_lines.append(f"Report Date: {datetime.now().strftime('%Y-%m-%d')}")
        report_lines.append(f"Total Assessments: {progress_data['total_assessments']}")
        report_lines.append("")
        
        for test_id, analysis in progress_data.get("progress_analysis", {}).items():
            test_name = self.tests_module.tests[test_id].name
            report_lines.append(f"{test_name.upper()}:")
            report_lines.append(f"  Assessments: {analysis['assessment_count']}")
            report_lines.append(f"  Score Change: {analysis['scores']['change']:.1f} ({analysis['scores']['percent_change']:.1f}%)")
            report_lines.append(f"  Trend: {analysis['trend'].replace('_', ' ').title()}")
            report_lines.append(f"  Clinical Significance: {analysis['clinical_significance'].replace('_', ' ').title()}")
            report_lines.append("")
        
        return "\n".join(report_lines)
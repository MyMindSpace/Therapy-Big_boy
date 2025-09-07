"""
Assessment Templates Module
Comprehensive templates for clinical assessments in AI therapy system
Provides standardized assessment formats and scoring protocols
"""

from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
import json


class AssessmentType(Enum):
    """Types of clinical assessments"""
    INTAKE = "intake_assessment"
    SCREENING = "screening_assessment"
    DIAGNOSTIC = "diagnostic_assessment"
    PROGRESS = "progress_assessment"
    OUTCOME = "outcome_assessment"
    RISK = "risk_assessment"
    FUNCTIONAL = "functional_assessment"
    COGNITIVE = "cognitive_assessment"
    PERSONALITY = "personality_assessment"
    TRAUMA = "trauma_assessment"


class ResponseFormat(Enum):
    """Assessment response formats"""
    LIKERT_4 = "likert_4_point"
    LIKERT_5 = "likert_5_point"
    LIKERT_7 = "likert_7_point"
    YES_NO = "yes_no"
    MULTIPLE_CHOICE = "multiple_choice"
    OPEN_TEXT = "open_text"
    NUMERIC = "numeric"
    DATE = "date"
    SCALE_0_10 = "scale_0_10"
    FREQUENCY = "frequency"
    SEVERITY = "severity"


class ScoreType(Enum):
    """Types of assessment scores"""
    RAW_SCORE = "raw_score"
    STANDARDIZED = "standardized_score"
    PERCENTILE = "percentile"
    T_SCORE = "t_score"
    CLINICAL_CUTOFF = "clinical_cutoff"
    SEVERITY_LEVEL = "severity_level"


@dataclass
class AssessmentItem:
    """Individual assessment item/question"""
    item_id: str
    text: str
    response_format: ResponseFormat
    options: List[str] = field(default_factory=list)
    reverse_scored: bool = False
    subscale: Optional[str] = None
    clinical_significance: str = "routine"
    required: bool = True
    validation_rules: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AssessmentScale:
    """Assessment scale/subscale definition"""
    scale_name: str
    items: List[str]  # Item IDs
    scoring_method: str
    clinical_cutoffs: Dict[str, float] = field(default_factory=dict)
    normative_data: Dict[str, Any] = field(default_factory=dict)
    reliability: Optional[float] = None
    validity_info: str = ""


@dataclass
class AssessmentTemplate:
    """Complete assessment template"""
    template_id: str
    name: str
    assessment_type: AssessmentType
    version: str
    items: List[AssessmentItem]
    scales: List[AssessmentScale]
    administration_time: int  # minutes
    target_population: str
    purpose: str
    instructions: str
    scoring_instructions: str
    interpretation_guidelines: Dict[str, str]
    references: List[str] = field(default_factory=list)


@dataclass
class AssessmentResponse:
    """Response to assessment item"""
    item_id: str
    response: Union[str, int, float, bool]
    response_time: Optional[float] = None
    confidence: Optional[int] = None
    notes: str = ""


@dataclass
class AssessmentResult:
    """Complete assessment results"""
    assessment_id: str
    template_id: str
    patient_id: str
    administered_date: datetime
    responses: Dict[str, AssessmentResponse]
    scale_scores: Dict[str, float]
    clinical_interpretation: str
    recommendations: List[str]
    risk_flags: List[str] = field(default_factory=list)
    completed: bool = False


class AssessmentTemplateManager:
    """Manages assessment templates and scoring"""
    
    def __init__(self):
        self.templates = self._initialize_assessment_templates()
        self.scoring_algorithms = self._initialize_scoring_algorithms()
        self.interpretation_rules = self._initialize_interpretation_rules()
    
    def _initialize_assessment_templates(self) -> Dict[str, AssessmentTemplate]:
        """Initialize standardized assessment templates"""
        
        templates = {}
        
        # PHQ-9 (Patient Health Questionnaire-9)
        templates["PHQ9"] = AssessmentTemplate(
            template_id="PHQ9",
            name="Patient Health Questionnaire-9",
            assessment_type=AssessmentType.SCREENING,
            version="1.0",
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
        templates["GAD7"] = AssessmentTemplate(
            template_id="GAD7",
            name="Generalized Anxiety Disorder-7",
            assessment_type=AssessmentType.SCREENING,
            version="1.0",
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
            instructions="Over the last 2 weeks, how often have you been bothered by the following problems?",
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
        templates["PCL5"] = AssessmentTemplate(
            template_id="PCL5",
            name="PTSD Checklist for DSM-5",
            assessment_type=AssessmentType.DIAGNOSTIC,
            version="1.0",
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
                    item_id="PCL5_11",
                    text="Having trouble remembering important parts of the stressful experience",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="negative_cognition"
                ),
                AssessmentItem(
                    item_id="PCL5_15",
                    text="Trouble concentrating",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="arousal"
                ),
                AssessmentItem(
                    item_id="PCL5_16",
                    text="Being super alert or watchful or on guard",
                    response_format=ResponseFormat.LIKERT_5,
                    options=["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"],
                    subscale="arousal"
                )
            ],
            scales=[
                AssessmentScale(
                    scale_name="PTSD Total",
                    items=["PCL5_1", "PCL5_2", "PCL5_3", "PCL5_4", "PCL5_5", "PCL5_6", "PCL5_7", "PCL5_11", "PCL5_15", "PCL5_16"],
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
        
        # Columbia Suicide Severity Rating Scale (C-SSRS) - Screening Version
        templates["CSSRS"] = AssessmentTemplate(
            template_id="CSSRS",
            name="Columbia Suicide Severity Rating Scale - Screening Version",
            assessment_type=AssessmentType.RISK,
            version="1.0",
            items=[
                AssessmentItem(
                    item_id="CSSRS_1",
                    text="Have you wished you were dead or wished you could go to sleep and not wake up?",
                    response_format=ResponseFormat.YES_NO,
                    subscale="suicidal_ideation",
                    clinical_significance="critical",
                    required=True
                ),
                AssessmentItem(
                    item_id="CSSRS_2",
                    text="Have you actually had any thoughts of killing yourself?",
                    response_format=ResponseFormat.YES_NO,
                    subscale="suicidal_ideation",
                    clinical_significance="critical",
                    required=True
                ),
                AssessmentItem(
                    item_id="CSSRS_3",
                    text="Have you been thinking about how you might do this?",
                    response_format=ResponseFormat.YES_NO,
                    subscale="suicidal_ideation",
                    clinical_significance="critical"
                ),
                AssessmentItem(
                    item_id="CSSRS_4",
                    text="Have you had these thoughts and had some intention of acting on them?",
                    response_format=ResponseFormat.YES_NO,
                    subscale="suicidal_ideation",
                    clinical_significance="critical"
                ),
                AssessmentItem(
                    item_id="CSSRS_5",
                    text="Have you started to work out or worked out the details of how to kill yourself? Do you intend to carry out this plan?",
                    response_format=ResponseFormat.YES_NO,
                    subscale="suicidal_ideation",
                    clinical_significance="critical"
                ),
                AssessmentItem(
                    item_id="CSSRS_6",
                    text="Have you ever done anything, started to do anything, or prepared to do anything to end your life?",
                    response_format=ResponseFormat.YES_NO,
                    subscale="suicidal_behavior",
                    clinical_significance="critical"
                )
            ],
            scales=[
                AssessmentScale(
                    scale_name="Suicide Risk Level",
                    items=["CSSRS_1", "CSSRS_2", "CSSRS_3", "CSSRS_4", "CSSRS_5", "CSSRS_6"],
                    scoring_method="categorical",
                    clinical_cutoffs={
                        "low_risk": 1.0,
                        "moderate_risk": 2.0,
                        "high_risk": 4.0,
                        "imminent_risk": 6.0
                    }
                )
            ],
            administration_time=5,
            target_population="All ages",
            purpose="Suicide risk assessment and screening",
            instructions="I'm going to ask you some questions about thoughts and feelings you may have had about death and suicide.",
            scoring_instructions="Categorical scoring based on highest endorsed item. Any 'Yes' to behavior questions = high risk.",
            interpretation_guidelines={
                "Category 1": "Death wishes - Low risk, monitor",
                "Category 2": "Suicidal thoughts - Moderate risk, safety planning",
                "Category 3": "Methods - High risk, immediate intervention",
                "Category 4": "Intent - High risk, crisis intervention", 
                "Category 5": "Plan - Imminent risk, emergency response",
                "Category 6": "Behavior - Critical risk, immediate safety"
            },
            references=["Posner, K., et al. (2011). The Columbia Suicide Severity Rating Scale."]
        )
        
        # Outcome Rating Scale (ORS)
        templates["ORS"] = AssessmentTemplate(
            template_id="ORS",
            name="Outcome Rating Scale",
            assessment_type=AssessmentType.OUTCOME,
            version="1.0",
            items=[
                AssessmentItem(
                    item_id="ORS_1",
                    text="Individually (personal well-being)",
                    response_format=ResponseFormat.SCALE_0_10,
                    subscale="individual_wellbeing"
                ),
                AssessmentItem(
                    item_id="ORS_2", 
                    text="Interpersonally (family, close relationships)",
                    response_format=ResponseFormat.SCALE_0_10,
                    subscale="interpersonal"
                ),
                AssessmentItem(
                    item_id="ORS_3",
                    text="Socially (work, school, friendships)",
                    response_format=ResponseFormat.SCALE_0_10,
                    subscale="social"
                ),
                AssessmentItem(
                    item_id="ORS_4",
                    text="Overall (general sense of well-being)",
                    response_format=ResponseFormat.SCALE_0_10,
                    subscale="overall"
                )
            ],
            scales=[
                AssessmentScale(
                    scale_name="Total Well-being",
                    items=["ORS_1", "ORS_2", "ORS_3", "ORS_4"],
                    scoring_method="sum",
                    clinical_cutoffs={
                        "clinical_distress": 25.0,
                        "reliable_change": 5.0
                    }
                )
            ],
            administration_time=2,
            target_population="All ages",
            purpose="Brief outcome measurement for therapy progress",
            instructions="Looking back over the last week, including today, help us understand how you have been feeling by rating how well you have been doing in the following areas of your life.",
            scoring_instructions="Mark visual analog scale from 0-10 for each domain. Sum for total score.",
            interpretation_guidelines={
                "0-24": "Clinical range - significant distress",
                "25-40": "Non-clinical range - normal functioning"
            },
            references=["Miller, S. D., Duncan, B. L., Brown, J., Sparks, J., & Claud, D. (2003). The Outcome Rating Scale."]
        )
        
        return templates
    
    def _initialize_scoring_algorithms(self) -> Dict[str, Any]:
        """Initialize scoring algorithms for different assessments"""
        return {
            "sum_scoring": {
                "method": "sum",
                "description": "Sum all item scores",
                "reverse_items": True
            },
            "mean_scoring": {
                "method": "mean", 
                "description": "Calculate mean of item scores",
                "handle_missing": "exclude"
            },
            "categorical_scoring": {
                "method": "categorical",
                "description": "Highest endorsed category determines score"
            },
            "weighted_scoring": {
                "method": "weighted",
                "description": "Apply item weights before summing"
            },
            "cutoff_scoring": {
                "method": "cutoff",
                "description": "Compare to established cutoff scores"
            }
        }
    
    def _initialize_interpretation_rules(self) -> Dict[str, Any]:
        """Initialize interpretation rules for assessment results"""
        return {
            "depression_severity": {
                "minimal": "No significant depressive symptoms",
                "mild": "Mild depression - monitor and consider psychosocial interventions",
                "moderate": "Moderate depression - therapy recommended, consider medication evaluation",
                "moderately_severe": "Moderately severe depression - therapy and medication recommended",
                "severe": "Severe depression - intensive treatment, safety assessment required"
            },
            "anxiety_severity": {
                "minimal": "No significant anxiety symptoms", 
                "mild": "Mild anxiety - coping strategies and stress management",
                "moderate": "Moderate anxiety - therapy recommended, anxiety management techniques",
                "severe": "Severe anxiety - intensive therapy, consider medication evaluation"
            },
            "ptsd_severity": {
                "below_threshold": "PTSD symptoms below clinical threshold",
                "probable_ptsd": "Probable PTSD - trauma-focused therapy recommended",
                "severe_ptsd": "Severe PTSD symptoms - intensive trauma treatment needed"
            },
            "suicide_risk": {
                "low_risk": "Low suicide risk - routine monitoring",
                "moderate_risk": "Moderate suicide risk - safety planning, increased contact",
                "high_risk": "High suicide risk - immediate intervention, safety measures",
                "imminent_risk": "Imminent suicide risk - emergency response required"
            }
        }
    
    def get_template(self, template_id: str) -> Optional[AssessmentTemplate]:
        """Get assessment template by ID"""
        return self.templates.get(template_id)
    
    def list_templates(self, assessment_type: Optional[AssessmentType] = None) -> List[str]:
        """List available assessment templates"""
        if assessment_type:
            return [tid for tid, template in self.templates.items() 
                   if template.assessment_type == assessment_type]
        return list(self.templates.keys())
    
    def create_assessment_instance(self, template_id: str, patient_id: str) -> Optional[AssessmentResult]:
        """Create new assessment instance from template"""
        template = self.get_template(template_id)
        if not template:
            return None
        
        assessment_id = f"{patient_id}_{template_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return AssessmentResult(
            assessment_id=assessment_id,
            template_id=template_id,
            patient_id=patient_id,
            administered_date=datetime.now(),
            responses={},
            scale_scores={},
            clinical_interpretation="",
            recommendations=[]
        )
    
    def score_assessment(self, assessment_result: AssessmentResult) -> AssessmentResult:
        """Score completed assessment"""
        template = self.get_template(assessment_result.template_id)
        if not template:
            return assessment_result
        
        # Calculate scale scores
        for scale in template.scales:
            score = self._calculate_scale_score(scale, assessment_result.responses)
            assessment_result.scale_scores[scale.scale_name] = score
        
        # Generate interpretation
        assessment_result.clinical_interpretation = self._generate_interpretation(
            template, assessment_result.scale_scores
        )
        
        # Generate recommendations
        assessment_result.recommendations = self._generate_recommendations(
            template, assessment_result.scale_scores, assessment_result.responses
        )
        
        # Check for risk flags
        assessment_result.risk_flags = self._check_risk_flags(
            template, assessment_result.responses
        )
        
        assessment_result.completed = True
        return assessment_result
    
    def _calculate_scale_score(self, scale: AssessmentScale, 
                              responses: Dict[str, AssessmentResponse]) -> float:
        """Calculate score for an assessment scale"""
        
        # Get responses for scale items
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
        
        # Apply scoring method
        if scale.scoring_method == "sum":
            return sum(scale_responses)
        elif scale.scoring_method == "mean":
            return sum(scale_responses) / len(scale_responses)
        elif scale.scoring_method == "categorical":
            return max(scale_responses)
        else:
            return sum(scale_responses)  # Default to sum
    
    def _generate_interpretation(self, template: AssessmentTemplate, 
                                scale_scores: Dict[str, float]) -> str:
        """Generate clinical interpretation of assessment results"""
        
        interpretations = []
        
        for scale_name, score in scale_scores.items():
            scale = next((s for s in template.scales if s.scale_name == scale_name), None)
            if not scale:
                continue
            
            # Determine severity level based on cutoffs
            severity = self._determine_severity_level(score, scale.clinical_cutoffs)
            
            # Get interpretation text
            if template.template_id == "PHQ9" and scale_name == "Depression Severity":
                interpretation_key = "depression_severity"
            elif template.template_id == "GAD7" and scale_name == "Anxiety Severity":
                interpretation_key = "anxiety_severity"
            elif template.template_id == "PCL5" and scale_name == "PTSD Total":
                interpretation_key = "ptsd_severity"
            elif template.template_id == "CSSRS":
                interpretation_key = "suicide_risk"
            else:
                interpretation_key = "general"
            
            severity_descriptions = self.interpretation_rules.get(interpretation_key, {})
            description = severity_descriptions.get(severity, f"Score: {score}")
            
            interpretations.append(f"{scale_name}: {description} (Score: {score})")
        
        return "\n".join(interpretations)
    
    def _determine_severity_level(self, score: float, cutoffs: Dict[str, float]) -> str:
        """Determine severity level based on cutoff scores"""
        
        if not cutoffs:
            return "unspecified"
        
        # Sort cutoffs by value
        sorted_cutoffs = sorted(cutoffs.items(), key=lambda x: x[1])
        
        # Find appropriate level
        for level, cutoff in sorted_cutoffs:
            if score < cutoff:
                return level
        
        # If score exceeds all cutoffs, return highest level
        return sorted_cutoffs[-1][0]
    
    def _generate_recommendations(self, template: AssessmentTemplate,
                                 scale_scores: Dict[str, float],
                                 responses: Dict[str, AssessmentResponse]) -> List[str]:
        """Generate treatment recommendations based on assessment results"""
        
        recommendations = []
        
        # Template-specific recommendations
        if template.template_id == "PHQ9":
            depression_score = scale_scores.get("Depression Severity", 0)
            
            if depression_score >= 20:
                recommendations.extend([
                    "Severe depression identified - immediate clinical attention recommended",
                    "Consider psychiatric evaluation for medication",
                    "Intensive therapy (2-3 sessions per week initially)",
                    "Safety assessment and monitoring required"
                ])
            elif depression_score >= 15:
                recommendations.extend([
                    "Moderately severe depression - therapy and medication evaluation recommended",
                    "Weekly therapy sessions",
                    "Consider cognitive-behavioral therapy (CBT)"
                ])
            elif depression_score >= 10:
                recommendations.extend([
                    "Moderate depression - therapy recommended",
                    "Consider cognitive-behavioral therapy or interpersonal therapy",
                    "Monitor progress with regular assessments"
                ])
            elif depression_score >= 5:
                recommendations.extend([
                    "Mild depression - psychosocial interventions recommended",
                    "Consider therapy, self-help resources, lifestyle changes",
                    "Monitor for progression"
                ])
            
            # Check item 9 (suicidal ideation)
            suicide_response = responses.get("PHQ9_9")
            if suicide_response and suicide_response.response > 0:
                recommendations.insert(0, "PRIORITY: Suicidal ideation present - immediate risk assessment required")
        
        elif template.template_id == "GAD7":
            anxiety_score = scale_scores.get("Anxiety Severity", 0)
            
            if anxiety_score >= 15:
                recommendations.extend([
                    "Severe anxiety - intensive treatment recommended",
                    "Consider cognitive-behavioral therapy for anxiety",
                    "Evaluate for medication consultation",
                    "Anxiety management and relaxation training"
                ])
            elif anxiety_score >= 10:
                recommendations.extend([
                    "Moderate anxiety - therapy recommended",
                    "Cognitive-behavioral therapy for anxiety disorders",
                    "Mindfulness and stress reduction techniques"
                ])
            elif anxiety_score >= 5:
                recommendations.extend([
                    "Mild anxiety - coping strategies and monitoring",
                    "Consider therapy if symptoms persist or worsen",
                    "Stress management and relaxation techniques"
                ])
        
        elif template.template_id == "PCL5":
            ptsd_score = scale_scores.get("PTSD Total", 0)
            
            if ptsd_score >= 50:
                recommendations.extend([
                    "Severe PTSD symptoms - intensive trauma-focused therapy required",
                    "Consider specialized trauma treatment (CPT, EMDR, PE)",
                    "Evaluate for comorbid conditions",
                    "Consider intensive outpatient or residential treatment"
                ])
            elif ptsd_score >= 33:
                recommendations.extend([
                    "Probable PTSD - trauma-focused therapy recommended",
                    "Evidence-based trauma treatments (CPT, EMDR, Prolonged Exposure)",
                    "Address safety and stabilization first",
                    "Monitor for comorbid depression and anxiety"
                ])
        
        elif template.template_id == "CSSRS":
            # Check highest endorsed item
            highest_risk = 0
            for item_id, response in responses.items():
                if response.response in [True, "yes", "Yes"]:
                    item_num = int(item_id.split("_")[1])
                    highest_risk = max(highest_risk, item_num)
            
            if highest_risk >= 6:
                recommendations.extend([
                    "EMERGENCY: Suicide attempt or preparatory behavior - immediate intervention required",
                    "Crisis intervention and safety planning",
                    "Consider emergency department evaluation",
                    "Remove means of self-harm",
                    "Continuous monitoring until safe"
                ])
            elif highest_risk >= 4:
                recommendations.extend([
                    "HIGH RISK: Suicidal intent present - immediate safety measures required",
                    "Comprehensive safety planning",
                    "Increase frequency of contact",
                    "Consider higher level of care",
                    "Remove access to lethal means"
                ])
            elif highest_risk >= 2:
                recommendations.extend([
                    "MODERATE RISK: Suicidal ideation present - safety assessment and planning",
                    "Develop safety plan with patient",
                    "Increase monitoring and support",
                    "Address underlying mental health conditions"
                ])
            elif highest_risk >= 1:
                recommendations.extend([
                    "LOW RISK: Death wishes present - monitor and support",
                    "Explore underlying concerns",
                    "Provide hope and coping strategies",
                    "Regular check-ins on mood and ideation"
                ])
        
        elif template.template_id == "ORS":
            total_score = scale_scores.get("Total Well-being", 0)
            
            if total_score < 25:
                recommendations.extend([
                    "Significant distress identified across multiple life domains",
                    "Comprehensive therapy recommended",
                    "Address areas of lowest functioning first",
                    "Regular progress monitoring with ORS"
                ])
            else:
                recommendations.extend([
                    "Functioning within normal range",
                    "Continue current interventions if in therapy",
                    "Focus on maintenance and prevention"
                ])
        
        return recommendations
    
    def _check_risk_flags(self, template: AssessmentTemplate,
                         responses: Dict[str, AssessmentResponse]) -> List[str]:
        """Check for risk flags in assessment responses"""
        
        risk_flags = []
        
        # Check items marked as critical significance
        for item in template.items:
            if item.clinical_significance == "critical":
                response = responses.get(item.item_id)
                if response and response.response not in [0, "Not at all", False, "no", "No"]:
                    risk_flags.append(f"Critical item endorsed: {item.text}")
        
        # Template-specific risk checks
        if template.template_id == "PHQ9":
            suicide_item = responses.get("PHQ9_9")
            if suicide_item and suicide_item.response > 0:
                risk_flags.append("Suicidal ideation present")
        
        elif template.template_id == "CSSRS":
            for item_id, response in responses.items():
                if response.response in [True, "yes", "Yes"]:
                    if item_id in ["CSSRS_4", "CSSRS_5", "CSSRS_6"]:
                        risk_flags.append("High suicide risk - immediate intervention required")
                    elif item_id in ["CSSRS_2", "CSSRS_3"]:
                        risk_flags.append("Moderate suicide risk - safety planning needed")
        
        elif template.template_id == "PCL5":
            flashback_item = responses.get("PCL5_3")
            if flashback_item and flashback_item.response >= 3:
                risk_flags.append("Severe dissociative symptoms present")
        
        return risk_flags
    
    def generate_assessment_report(self, assessment_result: AssessmentResult) -> str:
        """Generate comprehensive assessment report"""
        
        template = self.get_template(assessment_result.template_id)
        if not template:
            return "Template not found"
        
        report_sections = []
        
        # Header
        report_sections.append(f"ASSESSMENT REPORT: {template.name}")
        report_sections.append(f"Patient ID: {assessment_result.patient_id}")
        report_sections.append(f"Assessment Date: {assessment_result.administered_date.strftime('%Y-%m-%d %H:%M')}")
        report_sections.append(f"Assessment ID: {assessment_result.assessment_id}")
        report_sections.append("")
        
        # Assessment Information
        report_sections.append("ASSESSMENT INFORMATION:")
        report_sections.append(f"Purpose: {template.purpose}")
        report_sections.append(f"Target Population: {template.target_population}")
        report_sections.append(f"Administration Time: {template.administration_time} minutes")
        report_sections.append("")
        
        # Risk Flags (if any)
        if assessment_result.risk_flags:
            report_sections.append("⚠️  RISK ALERTS:")
            for flag in assessment_result.risk_flags:
                report_sections.append(f"  • {flag}")
            report_sections.append("")
        
        # Scale Scores
        report_sections.append("SCALE SCORES:")
        for scale_name, score in assessment_result.scale_scores.items():
            scale = next((s for s in template.scales if s.scale_name == scale_name), None)
            if scale and scale.clinical_cutoffs:
                severity = self._determine_severity_level(score, scale.clinical_cutoffs)
                report_sections.append(f"  {scale_name}: {score} ({severity})")
            else:
                report_sections.append(f"  {scale_name}: {score}")
        report_sections.append("")
        
        # Clinical Interpretation
        report_sections.append("CLINICAL INTERPRETATION:")
        report_sections.append(assessment_result.clinical_interpretation)
        report_sections.append("")
        
        # Recommendations
        if assessment_result.recommendations:
            report_sections.append("RECOMMENDATIONS:")
            for i, rec in enumerate(assessment_result.recommendations, 1):
                report_sections.append(f"  {i}. {rec}")
            report_sections.append("")
        
        # Item-by-Item Responses (for critical items)
        critical_responses = []
        for item in template.items:
            if item.clinical_significance in ["high", "critical"]:
                response = assessment_result.responses.get(item.item_id)
                if response:
                    critical_responses.append(f"  {item.item_id}: {response.response}")
                    if response.notes:
                        critical_responses.append(f"    Notes: {response.notes}")
        
        if critical_responses:
            report_sections.append("CRITICAL ITEM RESPONSES:")
            report_sections.extend(critical_responses)
            report_sections.append("")
        
        # Footer
        report_sections.append("RELIABILITY AND VALIDITY:")
        for scale in template.scales:
            if scale.reliability:
                report_sections.append(f"  {scale.scale_name}: Cronbach's α = {scale.reliability}")
        
        if template.references:
            report_sections.append("")
            report_sections.append("REFERENCES:")
            for ref in template.references:
                report_sections.append(f"  • {ref}")
        
        return "\n".join(report_sections)
    
    def validate_assessment_response(self, template_id: str, item_id: str, 
                                   response: Any) -> Tuple[bool, str]:
        """Validate individual assessment response"""
        
        template = self.get_template(template_id)
        if not template:
            return False, "Template not found"
        
        item = next((i for i in template.items if i.item_id == item_id), None)
        if not item:
            return False, "Item not found"
        
        # Check response format
        if item.response_format == ResponseFormat.YES_NO:
            if response not in [True, False, "yes", "no", "Yes", "No"]:
                return False, "Response must be yes/no"
        
        elif item.response_format in [ResponseFormat.LIKERT_4, ResponseFormat.LIKERT_5, ResponseFormat.LIKERT_7]:
            scale_max = int(item.response_format.value.split("_")[1])
            if not isinstance(response, int) or response < 0 or response >= scale_max:
                return False, f"Response must be integer 0-{scale_max-1}"
        
        elif item.response_format == ResponseFormat.SCALE_0_10:
            if not isinstance(response, (int, float)) or response < 0 or response > 10:
                return False, "Response must be number 0-10"
        
        elif item.response_format == ResponseFormat.MULTIPLE_CHOICE:
            if response not in range(len(item.options)) and response not in item.options:
                return False, f"Response must be one of: {item.options}"
        
        # Check validation rules
        for rule, value in item.validation_rules.items():
            if rule == "min_value" and response < value:
                return False, f"Response must be at least {value}"
            elif rule == "max_value" and response > value:
                return False, f"Response must be no more than {value}"
            elif rule == "required" and value and not response:
                return False, "Response is required for this item"
        
        return True, "Valid response"


# Example usage and testing
if __name__ == "__main__":
    # Initialize assessment template manager
    template_manager = AssessmentTemplateManager()
    
    print("=== ASSESSMENT TEMPLATE SYSTEM DEMONSTRATION ===\n")
    
    # List available templates
    print("Available Assessment Templates:")
    for template_id in template_manager.list_templates():
        template = template_manager.get_template(template_id)
        print(f"  • {template_id}: {template.name} ({template.assessment_type.value})")
    print()
    
    # Demonstrate PHQ-9 assessment
    print("=== PHQ-9 DEPRESSION SCREENING DEMONSTRATION ===")
    
    # Create assessment instance
    phq9_assessment = template_manager.create_assessment_instance("PHQ9", "PATIENT_001")
    print(f"Created assessment: {phq9_assessment.assessment_id}")
    
    # Simulate responses (moderate depression)
    phq9_responses = {
        "PHQ9_1": 2,  # Several days
        "PHQ9_2": 3,  # Nearly every day
        "PHQ9_3": 2,  # Several days
        "PHQ9_4": 3,  # Nearly every day
        "PHQ9_5": 1,  # Several days
        "PHQ9_6": 2,  # More than half the days
        "PHQ9_7": 2,  # More than half the days
        "PHQ9_8": 1,  # Several days
        "PHQ9_9": 1,  # Several days - RISK FLAG
        "PHQ9_10": 2  # Very difficult
    }
    
    # Record responses
    for item_id, response_value in phq9_responses.items():
        phq9_assessment.responses[item_id] = AssessmentResponse(
            item_id=item_id,
            response=response_value,
            notes="Simulated response" if item_id == "PHQ9_9" else ""
        )
    
    # Score the assessment
    phq9_assessment = template_manager.score_assessment(phq9_assessment)
    
    print(f"Depression Severity Score: {phq9_assessment.scale_scores.get('Depression Severity', 0)}")
    print(f"Risk Flags: {phq9_assessment.risk_flags}")
    print()
    
    # Generate report
    print("=== COMPLETE PHQ-9 ASSESSMENT REPORT ===")
    report = template_manager.generate_assessment_report(phq9_assessment)
    print(report)
    print("\n" + "="*60 + "\n")
    
    # Demonstrate C-SSRS (Suicide Risk Assessment)
    print("=== C-SSRS SUICIDE RISK ASSESSMENT DEMONSTRATION ===")
    
    cssrs_assessment = template_manager.create_assessment_instance("CSSRS", "PATIENT_001")
    
    # High risk scenario
    cssrs_responses = {
        "CSSRS_1": True,   # Death wishes
        "CSSRS_2": True,   # Suicidal thoughts
        "CSSRS_3": True,   # Methods
        "CSSRS_4": False,  # Intent
        "CSSRS_5": False,  # Plan
        "CSSRS_6": False   # Behavior
    }
    
    for item_id, response_value in cssrs_responses.items():
        cssrs_assessment.responses[item_id] = AssessmentResponse(
            item_id=item_id,
            response=response_value
        )
    
    cssrs_assessment = template_manager.score_assessment(cssrs_assessment)
    
    print("C-SSRS Results:")
    print(f"Risk Level: {cssrs_assessment.scale_scores}")
    print(f"Risk Flags: {cssrs_assessment.risk_flags}")
    print("\nRecommendations:")
    for rec in cssrs_assessment.recommendations:
        print(f"  • {rec}")
    print()
    
    # Demonstrate validation
    print("=== RESPONSE VALIDATION DEMONSTRATION ===")
    
    # Test valid response
    valid, message = template_manager.validate_assessment_response("PHQ9", "PHQ9_1", 2)
    print(f"Valid PHQ9 response (2): {valid} - {message}")
    
    # Test invalid response
    valid, message = template_manager.validate_assessment_response("PHQ9", "PHQ9_1", 5)
    print(f"Invalid PHQ9 response (5): {valid} - {message}")
    
    # Test C-SSRS validation
    valid, message = template_manager.validate_assessment_response("CSSRS", "CSSRS_1", True)
    print(f"Valid C-SSRS response (True): {valid} - {message}")
    
    print("\n" + "="*60)
    print("Assessment template system demonstration complete!")
    print("Templates ready for integration with AI therapy system and database storage.")
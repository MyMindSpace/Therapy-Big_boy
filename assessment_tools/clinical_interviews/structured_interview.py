"""
Structured Clinical Interview Module
Professional structured interviews for mental health assessment
Based on SCID-5 (Structured Clinical Interview for DSM-5) protocols
"""

from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import re


class InterviewType(Enum):
    """Types of structured interviews"""
    SCID_5_RV = "scid_5_research_version"
    SCID_5_CV = "scid_5_clinician_version"
    MINI = "mini_international_neuropsychiatric_interview"
    CIDI = "composite_international_diagnostic_interview"
    DIAGNOSTIC_SCREENING = "diagnostic_screening"
    RISK_ASSESSMENT = "risk_assessment"


class ResponseType(Enum):
    """Types of interview responses"""
    YES_NO = "yes_no"
    SCALE = "scale"
    MULTIPLE_CHOICE = "multiple_choice"
    OPEN_ENDED = "open_ended"
    DATETIME = "datetime"
    DURATION = "duration"


class ClinicalJudgment(Enum):
    """Clinical judgment ratings"""
    ABSENT = 0
    SUBTHRESHOLD = 1
    THRESHOLD = 2
    SEVERE = 3
    INADEQUATE_INFO = 9


class InterviewSection(Enum):
    """Structured interview sections"""
    OVERVIEW = "overview"
    MOOD_EPISODES = "mood_episodes"
    PSYCHOTIC_SYMPTOMS = "psychotic_symptoms"
    SUBSTANCE_USE_DISORDERS = "substance_use_disorders"
    ANXIETY_DISORDERS = "anxiety_disorders"
    OBSESSIVE_COMPULSIVE = "obsessive_compulsive"
    TRAUMA_STRESSOR = "trauma_stressor"
    EATING_DISORDERS = "eating_disorders"
    SOMATIC_SYMPTOMS = "somatic_symptoms"
    SLEEP_WAKE_DISORDERS = "sleep_wake_disorders"
    PERSONALITY_DISORDERS = "personality_disorders"
    RISK_ASSESSMENT = "risk_assessment"


@dataclass
class InterviewQuestion:
    """Individual interview question"""
    id: str
    section: InterviewSection
    question_text: str
    response_type: ResponseType
    skip_logic: Dict[str, str] = field(default_factory=dict)
    probe_questions: List[str] = field(default_factory=list)
    clinical_significance: str = "routine"
    dsm5_criteria: Optional[str] = None
    scoring_guidelines: Dict[str, Any] = field(default_factory=dict)
    required: bool = False


@dataclass
class InterviewResponse:
    """Response to interview question"""
    question_id: str
    response: Union[str, int, float, bool]
    clinical_rating: Optional[ClinicalJudgment] = None
    confidence_level: float = 1.0
    notes: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    follow_up_needed: bool = False


@dataclass
class InterviewSession:
    """Complete interview session"""
    session_id: str
    patient_id: str
    interview_type: InterviewType
    interviewer: str
    start_time: datetime
    end_time: Optional[datetime] = None
    responses: Dict[str, InterviewResponse] = field(default_factory=dict)
    clinical_impressions: List[str] = field(default_factory=list)
    diagnostic_conclusions: Dict[str, Any] = field(default_factory=dict)
    risk_assessment: Dict[str, str] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


class StructuredClinicalInterview:
    """Comprehensive structured clinical interview system"""
    
    def __init__(self):
        self.interview_protocols = self._initialize_interview_protocols()
        self.skip_logic_engine = self._initialize_skip_logic()
        self.scoring_algorithms = self._initialize_scoring_algorithms()
        self.diagnostic_algorithms = self._initialize_diagnostic_algorithms()
    
    def _initialize_interview_protocols(self) -> Dict[InterviewType, Dict[InterviewSection, List[InterviewQuestion]]]:
        """Initialize structured interview protocols"""
        
        protocols = {}
        
        # SCID-5 Research Version Protocol
        protocols[InterviewType.SCID_5_RV] = {
            InterviewSection.OVERVIEW: [
                InterviewQuestion(
                    id="A.1",
                    section=InterviewSection.OVERVIEW,
                    question_text="How old are you?",
                    response_type=ResponseType.OPEN_ENDED,
                    clinical_significance="demographic"
                ),
                InterviewQuestion(
                    id="A.2",
                    section=InterviewSection.OVERVIEW,
                    question_text="What is the highest level of education you completed?",
                    response_type=ResponseType.MULTIPLE_CHOICE,
                    scoring_guidelines={
                        "options": ["Less than high school", "High school", "Some college", 
                                  "Bachelor's degree", "Graduate degree"]
                    }
                ),
                InterviewQuestion(
                    id="A.3",
                    section=InterviewSection.OVERVIEW,
                    question_text="Are you currently working?",
                    response_type=ResponseType.YES_NO,
                    probe_questions=[
                        "What kind of work do you do?",
                        "How long have you been at your current job?",
                        "Any problems at work related to your mental health?"
                    ]
                )
            ],
            
            InterviewSection.MOOD_EPISODES: [
                InterviewQuestion(
                    id="A.1",
                    section=InterviewSection.MOOD_EPISODES,
                    question_text="Have you ever had a period of time when you were feeling depressed, sad, or down most of the day nearly every day?",
                    response_type=ResponseType.YES_NO,
                    skip_logic={"no": "A.15"},
                    probe_questions=[
                        "What was that like?",
                        "How long did it last?",
                        "When did this happen?"
                    ],
                    dsm5_criteria="Major Depressive Episode - Criterion A1",
                    clinical_significance="high",
                    required=True
                ),
                InterviewQuestion(
                    id="A.2",
                    section=InterviewSection.MOOD_EPISODES,
                    question_text="What about a period of time when you were much less interested in most things or unable to enjoy things you used to enjoy?",
                    response_type=ResponseType.YES_NO,
                    probe_questions=[
                        "Did you lose interest in things you usually enjoyed?",
                        "How long did this last?",
                        "Was this different from your usual self?"
                    ],
                    dsm5_criteria="Major Depressive Episode - Criterion A2",
                    clinical_significance="high"
                ),
                InterviewQuestion(
                    id="A.3",
                    section=InterviewSection.MOOD_EPISODES,
                    question_text="During this time, did you lose or gain weight? Did your appetite change?",
                    response_type=ResponseType.OPEN_ENDED,
                    probe_questions=[
                        "How much weight did you lose/gain?",
                        "Was this intentional?",
                        "How was your appetite different?"
                    ],
                    dsm5_criteria="Major Depressive Episode - Criterion A3"
                ),
                InterviewQuestion(
                    id="A.4",
                    section=InterviewSection.MOOD_EPISODES,
                    question_text="How was your sleep?",
                    response_type=ResponseType.OPEN_ENDED,
                    probe_questions=[
                        "Trouble falling asleep?",
                        "Waking up in the middle of the night?",
                        "Waking up too early?",
                        "Sleeping too much?"
                    ],
                    dsm5_criteria="Major Depressive Episode - Criterion A4"
                ),
                InterviewQuestion(
                    id="A.5",
                    section=InterviewSection.MOOD_EPISODES,
                    question_text="Were you so fidgety or restless that you were moving around a lot more than usual? Or the opposite - talking or moving more slowly than normal?",
                    response_type=ResponseType.MULTIPLE_CHOICE,
                    scoring_guidelines={
                        "options": ["No change", "Psychomotor agitation", "Psychomotor retardation", "Both at different times"]
                    },
                    probe_questions=[
                        "Did other people notice this?",
                        "Was this every day?"
                    ],
                    dsm5_criteria="Major Depressive Episode - Criterion A5"
                ),
                InterviewQuestion(
                    id="A.6",
                    section=InterviewSection.MOOD_EPISODES,
                    question_text="What was your energy like?",
                    response_type=ResponseType.OPEN_ENDED,
                    probe_questions=[
                        "Did you feel tired all the time?",
                        "Even when you hadn't been doing anything?",
                        "Was this nearly every day?"
                    ],
                    dsm5_criteria="Major Depressive Episode - Criterion A6"
                ),
                InterviewQuestion(
                    id="A.7",
                    section=InterviewSection.MOOD_EPISODES,
                    question_text="How did you feel about yourself?",
                    response_type=ResponseType.OPEN_ENDED,
                    probe_questions=[
                        "Did you feel worthless?",
                        "Did you feel guilty about things?",
                        "Were these feelings excessive or inappropriate?"
                    ],
                    dsm5_criteria="Major Depressive Episode - Criterion A7"
                ),
                InterviewQuestion(
                    id="A.8",
                    section=InterviewSection.MOOD_EPISODES,
                    question_text="Did you have trouble thinking or concentrating?",
                    response_type=ResponseType.YES_NO,
                    probe_questions=[
                        "What kinds of things were hard to concentrate on?",
                        "Trouble making decisions?",
                        "Did other people notice?"
                    ],
                    dsm5_criteria="Major Depressive Episode - Criterion A8"
                ),
                InterviewQuestion(
                    id="A.9",
                    section=InterviewSection.MOOD_EPISODES,
                    question_text="Were things so bad that you were thinking a lot about death or that you would be better off dead? What about thinking of hurting yourself?",
                    response_type=ResponseType.OPEN_ENDED,
                    probe_questions=[
                        "Did you think about suicide?",
                        "Did you have a plan?",
                        "Did you do anything to hurt yourself?",
                        "How often did you have these thoughts?"
                    ],
                    dsm5_criteria="Major Depressive Episode - Criterion A9",
                    clinical_significance="critical"
                )
            ],
            
            InterviewSection.ANXIETY_DISORDERS: [
                InterviewQuestion(
                    id="F.1",
                    section=InterviewSection.ANXIETY_DISORDERS,
                    question_text="Have you ever had a panic attack, when all of a sudden you felt frightened, anxious, or extremely uncomfortable?",
                    response_type=ResponseType.YES_NO,
                    skip_logic={"no": "F.32"},
                    probe_questions=[
                        "What was that like?",
                        "How long did it last?",
                        "What brought it on?"
                    ],
                    dsm5_criteria="Panic Attack Specifier",
                    clinical_significance="high"
                ),
                InterviewQuestion(
                    id="F.2",
                    section=InterviewSection.ANXIETY_DISORDERS,
                    question_text="During the attack, did you have a racing or pounding heart?",
                    response_type=ResponseType.YES_NO,
                    dsm5_criteria="Panic Attack - Criterion A1"
                ),
                InterviewQuestion(
                    id="F.3",
                    section=InterviewSection.ANXIETY_DISORDERS,
                    question_text="Were you sweating?",
                    response_type=ResponseType.YES_NO,
                    dsm5_criteria="Panic Attack - Criterion A2"
                ),
                InterviewQuestion(
                    id="F.4",
                    section=InterviewSection.ANXIETY_DISORDERS,
                    question_text="Were you trembling or shaking?",
                    response_type=ResponseType.YES_NO,
                    dsm5_criteria="Panic Attack - Criterion A3"
                ),
                InterviewQuestion(
                    id="F.32",
                    section=InterviewSection.ANXIETY_DISORDERS,
                    question_text="Have you ever been bothered by excessive anxiety and worry about a number of events or activities?",
                    response_type=ResponseType.YES_NO,
                    skip_logic={"no": "F.50"},
                    probe_questions=[
                        "What kinds of things do you worry about?",
                        "How long has this been going on?",
                        "Is it hard to control the worry?"
                    ],
                    dsm5_criteria="Generalized Anxiety Disorder - Criterion A",
                    clinical_significance="high"
                )
            ],
            
            InterviewSection.RISK_ASSESSMENT: [
                InterviewQuestion(
                    id="R.1",
                    section=InterviewSection.RISK_ASSESSMENT,
                    question_text="In the past month, have you wished you were dead or wished you could go to sleep and not wake up?",
                    response_type=ResponseType.YES_NO,
                    probe_questions=[
                        "How often have you had these thoughts?",
                        "What triggers these thoughts?",
                        "How long do these feelings last?"
                    ],
                    clinical_significance="critical",
                    required=True
                ),
                InterviewQuestion(
                    id="R.2",
                    section=InterviewSection.RISK_ASSESSMENT,
                    question_text="In the past month, have you actually had any thoughts about killing yourself?",
                    response_type=ResponseType.YES_NO,
                    skip_logic={"no": "R.5"},
                    probe_questions=[
                        "When did you first have these thoughts?",
                        "How often do you have them?",
                        "What do you think about doing?"
                    ],
                    clinical_significance="critical",
                    required=True
                ),
                InterviewQuestion(
                    id="R.3",
                    section=InterviewSection.RISK_ASSESSMENT,
                    question_text="Have you been thinking about how you might kill yourself?",
                    response_type=ResponseType.YES_NO,
                    probe_questions=[
                        "What method have you thought about?",
                        "How detailed is this plan?",
                        "Do you have access to this method?"
                    ],
                    clinical_significance="critical"
                ),
                InterviewQuestion(
                    id="R.4",
                    section=InterviewSection.RISK_ASSESSMENT,
                    question_text="Have you had these thoughts and had some intention of acting on them?",
                    response_type=ResponseType.YES_NO,
                    probe_questions=[
                        "How strong is this intention?",
                        "What has stopped you so far?",
                        "When do you feel most likely to act?"
                    ],
                    clinical_significance="critical"
                ),
                InterviewQuestion(
                    id="R.5",
                    section=InterviewSection.RISK_ASSESSMENT,
                    question_text="Have you ever done anything, started to do anything, or prepared to do anything to end your life?",
                    response_type=ResponseType.YES_NO,
                    probe_questions=[
                        "What did you do?",
                        "When did this happen?",
                        "What was going on in your life then?",
                        "Did you receive medical attention?"
                    ],
                    clinical_significance="critical"
                )
            ]
        }
        
        return protocols
    
    def _initialize_skip_logic(self) -> Dict[str, Any]:
        """Initialize skip logic rules for efficient interviews"""
        return {
            "depression_screening": {
                "A.1": {"no": "anxiety_module"},
                "A.2": {"no": "check_depression_history"}
            },
            "anxiety_screening": {
                "F.1": {"no": "trauma_module"},
                "F.32": {"no": "substance_module"}
            }
        }
    
    def _initialize_scoring_algorithms(self) -> Dict[str, Any]:
        """Initialize scoring algorithms for different assessments"""
        return {
            "major_depression": {
                "required_criteria": ["A.1", "A.2"],
                "minimum_symptoms": 5,
                "duration_requirement": "2_weeks",
                "exclusions": ["manic_episode", "substance_induced"]
            },
            "panic_disorder": {
                "required_criteria": ["F.1"],
                "minimum_symptoms": 4,
                "duration_requirement": "peak_within_minutes",
                "additional_requirements": ["persistent_concern", "behavioral_change"]
            },
            "generalized_anxiety": {
                "required_criteria": ["F.32"],
                "duration_requirement": "6_months",
                "associated_symptoms": 3,
                "functional_impairment": True
            }
        }
    
    def _initialize_diagnostic_algorithms(self) -> Dict[str, Any]:
        """Initialize diagnostic decision algorithms"""
        return {
            "mood_disorders": {
                "major_depression": ["A.1", "A.2", "A.3", "A.4", "A.5", "A.6", "A.7", "A.8", "A.9"],
                "dysthymia": ["chronic_depression", "duration_2_years"],
                "bipolar_i": ["manic_episode"],
                "bipolar_ii": ["hypomanic_episode", "major_depression"]
            },
            "anxiety_disorders": {
                "panic_disorder": ["F.1", "F.2", "F.3", "F.4"],
                "generalized_anxiety": ["F.32", "worry_control", "associated_symptoms"],
                "social_anxiety": ["social_fear", "avoidance", "impairment"]
            }
        }
    
    def create_interview_session(self, patient_id: str, interview_type: InterviewType,
                               interviewer: str = "AI_Therapist") -> InterviewSession:
        """Create a new structured interview session"""
        session_id = f"{patient_id}_{interview_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return InterviewSession(
            session_id=session_id,
            patient_id=patient_id,
            interview_type=interview_type,
            interviewer=interviewer,
            start_time=datetime.now()
        )
    
    def get_next_question(self, session: InterviewSession) -> Optional[InterviewQuestion]:
        """Get the next question in the interview sequence"""
        protocol = self.interview_protocols.get(session.interview_type, {})
        
        # Determine current section and position
        current_section = self._determine_current_section(session)
        section_questions = protocol.get(current_section, [])
        
        # Find next unanswered question
        for question in section_questions:
            if question.id not in session.responses:
                return question
        
        # Move to next section if current section complete
        next_section = self._get_next_section(session, current_section)
        if next_section:
            next_section_questions = protocol.get(next_section, [])
            if next_section_questions:
                return next_section_questions[0]
        
        return None  # Interview complete
    
    def record_response(self, session: InterviewSession, question_id: str,
                       response: Union[str, int, float, bool],
                       clinical_rating: Optional[ClinicalJudgment] = None,
                       notes: str = "") -> InterviewResponse:
        """Record response to interview question"""
        
        interview_response = InterviewResponse(
            question_id=question_id,
            response=response,
            clinical_rating=clinical_rating,
            notes=notes,
            timestamp=datetime.now()
        )
        
        # Assess clinical significance and follow-up needs
        interview_response.follow_up_needed = self._assess_follow_up_need(
            session, question_id, response
        )
        
        # Store response
        session.responses[question_id] = interview_response
        
        # Update risk assessment if needed
        self._update_risk_assessment(session, question_id, response)
        
        return interview_response
    
    def _determine_current_section(self, session: InterviewSession) -> InterviewSection:
        """Determine which section the interview is currently in"""
        if not session.responses:
            return InterviewSection.OVERVIEW
        
        # Check latest response section
        latest_response = max(session.responses.values(), key=lambda x: x.timestamp)
        question_id = latest_response.question_id
        
        # Find section for this question
        protocol = self.interview_protocols.get(session.interview_type, {})
        for section, questions in protocol.items():
            for question in questions:
                if question.id == question_id:
                    return section
        
        return InterviewSection.OVERVIEW
    
    def _get_next_section(self, session: InterviewSession, 
                         current_section: InterviewSection) -> Optional[InterviewSection]:
        """Determine next section based on skip logic and responses"""
        
        # Standard section progression
        section_order = [
            InterviewSection.OVERVIEW,
            InterviewSection.MOOD_EPISODES,
            InterviewSection.PSYCHOTIC_SYMPTOMS,
            InterviewSection.ANXIETY_DISORDERS,
            InterviewSection.SUBSTANCE_USE_DISORDERS,
            InterviewSection.TRAUMA_STRESSOR,
            InterviewSection.RISK_ASSESSMENT
        ]
        
        try:
            current_index = section_order.index(current_section)
            if current_index + 1 < len(section_order):
                return section_order[current_index + 1]
        except ValueError:
            pass
        
        return None
    
    def _assess_follow_up_need(self, session: InterviewSession, 
                              question_id: str, response: Any) -> bool:
        """Assess if follow-up questions are needed"""
        
        # Risk-related questions always need follow-up if positive
        if question_id.startswith("R.") and response in [True, "yes", "Yes"]:
            return True
        
        # Symptom questions need follow-up if endorsed
        if question_id.startswith("A.") and response in [True, "yes", "Yes"]:
            return True
        
        # Complex or concerning responses need follow-up
        if isinstance(response, str) and len(response) > 100:
            concerning_keywords = ["suicide", "death", "hurt", "harm", "hopeless", "worthless"]
            if any(keyword in response.lower() for keyword in concerning_keywords):
                return True
        
        return False
    
    def _update_risk_assessment(self, session: InterviewSession, 
                               question_id: str, response: Any):
        """Update risk assessment based on responses"""
        
        # Suicide risk assessment
        if question_id in ["R.1", "R.2", "R.3", "R.4", "R.5"]:
            if response in [True, "yes", "Yes"]:
                current_risk = session.risk_assessment.get("suicide_risk", "low")
                if question_id == "R.1":
                    session.risk_assessment["suicide_risk"] = "moderate"
                elif question_id in ["R.2", "R.3"]:
                    session.risk_assessment["suicide_risk"] = "high"
                elif question_id in ["R.4", "R.5"]:
                    session.risk_assessment["suicide_risk"] = "critical"
        
        # Depression severity
        if question_id in ["A.1", "A.2", "A.9"]:
            if response in [True, "yes", "Yes"]:
                session.risk_assessment["depression_risk"] = "moderate"
        
        # Anxiety severity
        if question_id in ["F.1", "F.32"]:
            if response in [True, "yes", "Yes"]:
                session.risk_assessment["anxiety_risk"] = "moderate"
    
    def generate_diagnostic_impression(self, session: InterviewSession) -> Dict[str, Any]:
        """Generate diagnostic impression based on interview responses"""
        
        impressions = {
            "probable_diagnoses": [],
            "rule_out_diagnoses": [],
            "severity_ratings": {},
            "confidence_levels": {},
            "supporting_evidence": {}
        }
        
        # Analyze mood disorders
        mood_analysis = self._analyze_mood_disorders(session)
        impressions.update(mood_analysis)
        
        # Analyze anxiety disorders
        anxiety_analysis = self._analyze_anxiety_disorders(session)
        impressions.update(anxiety_analysis)
        
        # Risk assessment summary
        risk_summary = self._generate_risk_summary(session)
        impressions["risk_assessment"] = risk_summary
        
        return impressions
    
    def _analyze_mood_disorders(self, session: InterviewSession) -> Dict[str, Any]:
        """Analyze responses for mood disorder diagnoses"""
        analysis = {
            "mood_symptoms_present": [],
            "mood_severity": "none"
        }
        
        # Check major depression criteria
        depression_symptoms = []
        for q_id in ["A.1", "A.2", "A.3", "A.4", "A.5", "A.6", "A.7", "A.8", "A.9"]:
            response = session.responses.get(q_id)
            if response and response.response in [True, "yes", "Yes"]:
                depression_symptoms.append(q_id)
        
        # Core symptoms check
        core_symptoms = sum(1 for q_id in ["A.1", "A.2"] 
                           if q_id in depression_symptoms)
        
        if len(depression_symptoms) >= 5 and core_symptoms >= 1:
            analysis["probable_diagnoses"] = ["Major Depressive Episode"]
            analysis["mood_severity"] = "severe" if len(depression_symptoms) >= 7 else "moderate"
        elif len(depression_symptoms) >= 3:
            analysis["rule_out_diagnoses"] = ["Major Depressive Episode"]
            analysis["mood_severity"] = "mild"
        
        return analysis
    
    def _analyze_anxiety_disorders(self, session: InterviewSession) -> Dict[str, Any]:
        """Analyze responses for anxiety disorder diagnoses"""
        analysis = {
            "anxiety_symptoms_present": [],
            "anxiety_severity": "none"
        }
        
        # Check panic disorder
        panic_response = session.responses.get("F.1")
        if panic_response and panic_response.response in [True, "yes", "Yes"]:
            analysis["anxiety_symptoms_present"].append("panic_attacks")
            analysis["rule_out_diagnoses"] = analysis.get("rule_out_diagnoses", []) + ["Panic Disorder"]
        
        # Check generalized anxiety
        gad_response = session.responses.get("F.32")
        if gad_response and gad_response.response in [True, "yes", "Yes"]:
            analysis["anxiety_symptoms_present"].append("generalized_worry")
            analysis["rule_out_diagnoses"] = analysis.get("rule_out_diagnoses", []) + ["Generalized Anxiety Disorder"]
        
        return analysis
    
    def _generate_risk_summary(self, session: InterviewSession) -> Dict[str, str]:
        """Generate comprehensive risk assessment summary"""
        risk_summary = {
            "overall_risk": "low",
            "suicide_risk": "low",
            "self_harm_risk": "low",
            "recommendations": []
        }
        
        # Update based on recorded risk assessments
        risk_summary.update(session.risk_assessment)
        
        # Generate recommendations
        if session.risk_assessment.get("suicide_risk") in ["high", "critical"]:
            risk_summary["recommendations"].extend([
                "Immediate safety assessment required",
                "Consider crisis intervention",
                "Assess need for higher level of care",
                "Develop safety plan"
            ])
        elif session.risk_assessment.get("suicide_risk") == "moderate":
            risk_summary["recommendations"].extend([
                "Regular risk monitoring",
                "Safety planning",
                "Increase contact frequency"
            ])
        
        return risk_summary
    
    def generate_interview_report(self, session: InterviewSession) -> str:
        """Generate comprehensive interview report"""
        
        # Complete the session
        session.end_time = datetime.now()
        duration = session.end_time - session.start_time
        
        # Generate diagnostic impressions
        diagnostic_impressions = self.generate_diagnostic_impression(session)
        
        report_sections = []
        
        # Header
        report_sections.append(f"STRUCTURED CLINICAL INTERVIEW REPORT")
        report_sections.append(f"Session ID: {session.session_id}")
        report_sections.append(f"Patient ID: {session.patient_id}")
        report_sections.append(f"Date: {session.start_time.strftime('%Y-%m-%d')}")
        report_sections.append(f"Duration: {duration}")
        report_sections.append(f"Interview Type: {session.interview_type.value}")
        report_sections.append("")
        
        # Risk Assessment
        report_sections.append("RISK ASSESSMENT:")
        risk_summary = diagnostic_impressions.get("risk_assessment", {})
        for risk_type, level in risk_summary.items():
            if risk_type != "recommendations":
                report_sections.append(f"  {risk_type.replace('_', ' ').title()}: {level}")
        
        if risk_summary.get("recommendations"):
            report_sections.append("  Recommendations:")
            for rec in risk_summary["recommendations"]:
                report_sections.append(f"    - {rec}")
        report_sections.append("")
        
        # Diagnostic Impressions
        report_sections.append("DIAGNOSTIC IMPRESSIONS:")
        
        probable_dx = diagnostic_impressions.get("probable_diagnoses", [])
        if probable_dx:
            report_sections.append("  Probable Diagnoses:")
            for dx in probable_dx:
                report_sections.append(f"    - {dx}")
        
        rule_out_dx = diagnostic_impressions.get("rule_out_diagnoses", [])
        if rule_out_dx:
            report_sections.append("  Rule Out:")
            for dx in rule_out_dx:
                report_sections.append(f"    - {dx}")
        
        report_sections.append("")
        
        # Key Responses
        report_sections.append("KEY CLINICAL RESPONSES:")
        for question_id, response in session.responses.items():
            if response.clinical_rating and response.clinical_rating != ClinicalJudgment.ABSENT:
                report_sections.append(f"  {question_id}: {response.response}")
                if response.notes:
                    report_sections.append(f"    Notes: {response.notes}")
        
        return "\n".join(report_sections)


# Example usage and testing
if __name__ == "__main__":
    # Initialize structured interview system
    interview_system = StructuredClinicalInterview()
    
    # Create interview session
    session = interview_system.create_interview_session(
        patient_id="PATIENT_001",
        interview_type=InterviewType.SCID_5_RV,
        interviewer="Dr. AI_Therapist"
    )
    
    # Simulate interview responses
    print("=== STRUCTURED CLINICAL INTERVIEW SIMULATION ===\n")
    
    # Record some example responses
    interview_system.record_response(
        session, "A.1", True, 
        clinical_rating=ClinicalJudgment.THRESHOLD,
        notes="Patient reports 3 weeks of persistent depressed mood"
    )
    
    interview_system.record_response(
        session, "A.2", True,
        clinical_rating=ClinicalJudgment.THRESHOLD,
        notes="Complete loss of interest in previously enjoyed activities"
    )
    
    interview_system.record_response(
        session, "A.3", "Lost 15 pounds without trying",
        clinical_rating=ClinicalJudgment.THRESHOLD
    )
    
    interview_system.record_response(
        session, "A.4", "Waking up at 3 AM every night, can't get back to sleep",
        clinical_rating=ClinicalJudgment.THRESHOLD
    )
    
    interview_system.record_response(
        session, "A.6", "Exhausted all the time, can barely get out of bed",
        clinical_rating=ClinicalJudgment.SEVERE
    )
    
    interview_system.record_response(
        session, "A.7", "I feel completely worthless and guilty about everything",
        clinical_rating=ClinicalJudgment.THRESHOLD
    )
    
    interview_system.record_response(
        session, "A.8", True,
        clinical_rating=ClinicalJudgment.THRESHOLD,
        notes="Significant concentration problems at work"
    )
    
    interview_system.record_response(
        session, "A.9", "I think about death a lot and sometimes wish I wouldn't wake up",
        clinical_rating=ClinicalJudgment.THRESHOLD,
        notes="Passive suicidal ideation, no active plan"
    )
    
    # Risk assessment responses
    interview_system.record_response(
        session, "R.1", True,
        clinical_rating=ClinicalJudgment.THRESHOLD,
        notes="Wishes to not wake up, occurring daily"
    )
    
    interview_system.record_response(
        session, "R.2", False,
        clinical_rating=ClinicalJudgment.ABSENT,
        notes="Denies active suicidal thoughts"
    )
    
    # Get next question
    next_question = interview_system.get_next_question(session)
    if next_question:
        print(f"Next Question: {next_question.id}")
        print(f"Question: {next_question.question_text}")
        print(f"Response Type: {next_question.response_type.value}")
        if next_question.probe_questions:
            print("Probe Questions:")
            for probe in next_question.probe_questions:
                print(f"  - {probe}")
        print()
    
    # Generate diagnostic impressions
    print("=== DIAGNOSTIC ANALYSIS ===")
    impressions = interview_system.generate_diagnostic_impression(session)
    
    print("Probable Diagnoses:")
    for dx in impressions.get("probable_diagnoses", []):
        print(f"  - {dx}")
    
    print("\nRule Out Diagnoses:")
    for dx in impressions.get("rule_out_diagnoses", []):
        print(f"  - {dx}")
    
    print("\nRisk Assessment:")
    risk_info = impressions.get("risk_assessment", {})
    for risk_type, level in risk_info.items():
        if risk_type != "recommendations":
            print(f"  {risk_type}: {level}")
    
    print("\nRecommendations:")
    for rec in risk_info.get("recommendations", []):
        print(f"  - {rec}")
    
    print("\n" + "="*60)
    
    # Generate full interview report
    print("\n=== COMPLETE INTERVIEW REPORT ===")
    report = interview_system.generate_interview_report(session)
    print(report)
    
    print("\n" + "="*60)
    
    # Demonstrate skip logic
    print("\n=== SKIP LOGIC DEMONSTRATION ===")
    new_session = interview_system.create_interview_session(
        patient_id="PATIENT_002",
        interview_type=InterviewType.SCID_5_RV
    )
    
    # Record negative response to depression screening
    interview_system.record_response(new_session, "A.1", False)
    interview_system.record_response(new_session, "A.2", False)
    
    next_q = interview_system.get_next_question(new_session)
    if next_q:
        print(f"After negative depression screening, next question: {next_q.id}")
        print(f"Question: {next_q.question_text}")
    
    print("\n=== SESSION STATISTICS ===")
    print(f"Total responses recorded: {len(session.responses)}")
    print(f"Questions requiring follow-up: {sum(1 for r in session.responses.values() if r.follow_up_needed)}")
    print(f"High significance responses: {sum(1 for r in session.responses.values() if r.clinical_rating in [ClinicalJudgment.THRESHOLD, ClinicalJudgment.SEVERE])}")
    print(f"Session duration: {session.end_time - session.start_time if session.end_time else 'In progress'}")


def create_mini_interview_protocol() -> Dict[InterviewSection, List[InterviewQuestion]]:
    """Create a simplified MINI-style interview protocol for quick screening"""
    
    mini_protocol = {
        InterviewSection.MOOD_EPISODES: [
            InterviewQuestion(
                id="MINI_A.1",
                section=InterviewSection.MOOD_EPISODES,
                question_text="Have you been consistently depressed or down, most of the day, nearly every day, for the past 2 weeks?",
                response_type=ResponseType.YES_NO,
                skip_logic={"no": "MINI_B.1"},
                dsm5_criteria="Major Depression - Quick Screen",
                clinical_significance="high"
            ),
            InterviewQuestion(
                id="MINI_A.2",
                section=InterviewSection.MOOD_EPISODES,
                question_text="In the past 2 weeks, have you been much less interested in most things or much less able to enjoy things?",
                response_type=ResponseType.YES_NO,
                dsm5_criteria="Major Depression - Quick Screen",
                clinical_significance="high"
            )
        ],
        
        InterviewSection.ANXIETY_DISORDERS: [
            InterviewQuestion(
                id="MINI_B.1",
                section=InterviewSection.ANXIETY_DISORDERS,
                question_text="In the last month, have you had an anxiety attack - suddenly feeling fear or panic?",
                response_type=ResponseType.YES_NO,
                skip_logic={"no": "MINI_C.1"},
                probe_questions=[
                    "Did it reach a peak within 10 minutes?",
                    "During the attack, did you have physical symptoms like racing heart, sweating, or trembling?"
                ],
                clinical_significance="high"
            )
        ],
        
        InterviewSection.RISK_ASSESSMENT: [
            InterviewQuestion(
                id="MINI_S.1",
                section=InterviewSection.RISK_ASSESSMENT,
                question_text="Have you thought that you would be better off dead, or of hurting yourself in some way?",
                response_type=ResponseType.YES_NO,
                probe_questions=[
                    "In the past month?",
                    "Have you made plans?",
                    "Have you attempted to hurt yourself?"
                ],
                clinical_significance="critical",
                required=True
            )
        ]
    }
    
    return mini_protocol


def generate_ai_interview_prompts(interview_question: InterviewQuestion) -> Dict[str, str]:
    """Generate AI prompts for conducting structured interviews with Gemini"""
    
    prompts = {
        "question_prompt": f"""
You are conducting a professional structured clinical interview. Ask the following question in a warm, empathetic manner:

Question: {interview_question.question_text}

Guidelines:
- Be professional but warm and empathetic
- Allow the patient to respond fully before follow-up
- Pay attention to non-verbal cues if mentioned
- Note any concerning responses for follow-up
- Maintain appropriate clinical boundaries

If the patient seems distressed by the question, provide appropriate support while gathering necessary clinical information.
""",
        
        "follow_up_prompt": f"""
Based on the patient's response, you may need to ask follow-up questions. Here are suggested probes:

{chr(10).join(f'- {probe}' for probe in interview_question.probe_questions)}

Use your clinical judgment to determine which follow-ups are most appropriate based on:
- The patient's initial response
- Level of detail provided
- Any concerning content mentioned
- Clinical significance of the response

Ask follow-ups naturally in conversation, not as a checklist.
""",
        
        "risk_assessment_prompt": f"""
CRITICAL: This question assesses for potential risk factors. 

If the patient endorses {interview_question.question_text.lower()}, you must:

1. Assess severity and frequency
2. Explore triggers and context
3. Evaluate safety and risk level
4. Consider immediate interventions if high risk
5. Document all risk-related information thoroughly

Risk Level Guidelines:
- Low: Mild symptoms, good coping, no immediate risk
- Moderate: Significant symptoms, some impairment, monitoring needed
- High: Severe symptoms, functional impairment, active risk factors
- Critical: Immediate risk, safety concerns, urgent intervention needed

Always err on the side of caution with risk assessment.
""",
        
        "scoring_prompt": f"""
Rate the clinical significance of the patient's response:

0 - Absent: No evidence of the symptom/criterion
1 - Subthreshold: Some features present but below clinical threshold  
2 - Threshold: Meets clinical criteria for the symptom/diagnosis
3 - Severe: Meets criteria with significant severity or impairment
9 - Inadequate Information: Unable to determine due to insufficient information

Consider:
- Frequency and duration of symptoms
- Severity and intensity
- Functional impairment
- Patient's subjective distress
- Objective clinical observations

Base your rating on DSM-5 criteria when applicable: {interview_question.dsm5_criteria or 'General clinical judgment'}
"""
    }
    
    return prompts
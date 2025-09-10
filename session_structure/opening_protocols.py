from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import sqlite3
import json


class SessionType(Enum):
    INITIAL_INTAKE = "initial_intake"
    FOLLOW_UP = "follow_up"
    CRISIS_SESSION = "crisis_session"
    ASSESSMENT = "assessment"
    TERMINATION = "termination"
    MEDICATION_CHECK = "medication_check"


class RiskLevel(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    SEVERE = "severe"


class MoodState(Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    NEUTRAL = "neutral"
    GOOD = "good"
    VERY_GOOD = "very_good"
    MIXED = "mixed"
    ELEVATED = "elevated"


@dataclass
class SessionOpening:
    session_id: str
    patient_id: str
    session_type: SessionType
    opening_time: datetime
    therapist_id: str
    current_mood: str
    mood_rating: int
    sleep_quality: str
    medication_compliance: str
    crisis_indicators: List[str]
    risk_assessment: RiskLevel
    presenting_concerns: List[str]
    session_goals: List[str]
    homework_completion: str
    significant_events: List[str]
    therapeutic_alliance: int
    motivation_level: int
    notes: str = ""


@dataclass
class SafetyAssessment:
    patient_id: str
    session_id: str
    assessment_date: datetime
    suicidal_ideation: bool
    suicidal_plan: bool
    suicidal_intent: bool
    self_harm_urges: bool
    homicidal_ideation: bool
    substance_use: bool
    psychotic_symptoms: bool
    risk_factors: List[str]
    protective_factors: List[str]
    safety_plan_active: bool
    intervention_needed: bool
    risk_level: RiskLevel
    assessor_notes: str


@dataclass
class CheckInResponse:
    question: str
    response: str
    follow_up_needed: bool
    concern_level: int
    notes: str = ""


class SessionOpeningProtocols:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.check_in_protocols = self._initialize_check_in_protocols()
        self.safety_protocols = self._initialize_safety_protocols()
        self.opening_templates = self._initialize_opening_templates()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_openings (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    session_type TEXT NOT NULL,
                    opening_time TEXT NOT NULL,
                    therapist_id TEXT NOT NULL,
                    current_mood TEXT,
                    mood_rating INTEGER,
                    sleep_quality TEXT,
                    medication_compliance TEXT,
                    crisis_indicators TEXT,
                    risk_assessment TEXT,
                    presenting_concerns TEXT,
                    session_goals TEXT,
                    homework_completion TEXT,
                    significant_events TEXT,
                    therapeutic_alliance INTEGER,
                    motivation_level INTEGER,
                    notes TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS safety_assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    assessment_date TEXT NOT NULL,
                    suicidal_ideation BOOLEAN,
                    suicidal_plan BOOLEAN,
                    suicidal_intent BOOLEAN,
                    self_harm_urges BOOLEAN,
                    homicidal_ideation BOOLEAN,
                    substance_use BOOLEAN,
                    psychotic_symptoms BOOLEAN,
                    risk_factors TEXT,
                    protective_factors TEXT,
                    safety_plan_active BOOLEAN,
                    intervention_needed BOOLEAN,
                    risk_level TEXT,
                    assessor_notes TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS check_in_responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    patient_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    response TEXT NOT NULL,
                    follow_up_needed BOOLEAN,
                    concern_level INTEGER,
                    notes TEXT,
                    response_time TEXT
                )
            """)
    
    def _initialize_check_in_protocols(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "standard_check_in": {
                "mood_assessment": [
                    "How are you feeling today on a scale of 1-10?",
                    "What's your overall mood been like since our last session?",
                    "Have you noticed any significant mood changes this week?"
                ],
                "functioning_check": [
                    "How has your sleep been?",
                    "How's your appetite been?",
                    "How has your energy level been?",
                    "Have you been able to keep up with daily activities?"
                ],
                "symptom_monitoring": [
                    "Have you noticed any return or worsening of symptoms?",
                    "Are you experiencing any new concerns?",
                    "How have you been coping with stress this week?"
                ],
                "medication_check": [
                    "How has medication compliance been?",
                    "Any side effects or concerns with medications?",
                    "Have you missed any doses this week?"
                ]
            },
            
            "crisis_check_in": {
                "immediate_safety": [
                    "Are you having any thoughts of hurting yourself right now?",
                    "Do you feel safe at this moment?",
                    "What brought you in for this emergency session?"
                ],
                "crisis_timeline": [
                    "When did this crisis begin?",
                    "What happened leading up to this?",
                    "Have things gotten better or worse since then?"
                ],
                "support_systems": [
                    "Who knows about what you're going through?",
                    "Is there anyone available to support you today?",
                    "Have you been alone during this difficult time?"
                ]
            },
            
            "follow_up_check_in": {
                "homework_review": [
                    "How did the homework assignment go?",
                    "Were you able to practice the skills we discussed?",
                    "What worked well and what was challenging?"
                ],
                "skill_application": [
                    "Did you have opportunities to use the coping skills?",
                    "How effective were the strategies we practiced?",
                    "What situations came up that were difficult to handle?"
                ],
                "progress_review": [
                    "How do you feel you're progressing toward your goals?",
                    "What changes have you noticed in yourself?",
                    "What areas do you want to focus on today?"
                ]
            },
            
            "assessment_check_in": {
                "symptom_inquiry": [
                    "Can you describe the main concerns bringing you here?",
                    "How long have you been experiencing these difficulties?",
                    "How are these problems affecting your daily life?"
                ],
                "history_gathering": [
                    "Have you experienced anything like this before?",
                    "What treatments have you tried in the past?",
                    "What has been most helpful for you previously?"
                ],
                "goals_exploration": [
                    "What are you hoping to get out of therapy?",
                    "What would need to change for you to feel better?",
                    "What does success look like to you?"
                ]
            }
        }
    
    def _initialize_safety_protocols(self) -> Dict[str, Any]:
        
        return {
            "suicide_assessment": {
                "ideation_questions": [
                    "Have you been having thoughts that life isn't worth living?",
                    "Have you been thinking about death or dying?",
                    "Have you had thoughts about hurting yourself?",
                    "Have you thought about suicide?"
                ],
                "plan_questions": [
                    "Have you thought about how you might hurt yourself?",
                    "Do you have a specific plan for ending your life?",
                    "Have you thought about when you might do this?",
                    "Do you have access to means to hurt yourself?"
                ],
                "intent_questions": [
                    "How likely is it that you would act on these thoughts?",
                    "What has stopped you from acting on these thoughts?",
                    "Are you planning to hurt yourself today?",
                    "Do you want to die or do you want the pain to stop?"
                ]
            },
            
            "risk_factors": [
                "Previous suicide attempts",
                "Family history of suicide",
                "Mental health conditions",
                "Substance abuse",
                "Recent losses or trauma",
                "Social isolation",
                "Access to lethal means",
                "Impulsivity",
                "Hopelessness",
                "Recent discharge from hospital"
            ],
            
            "protective_factors": [
                "Strong social support",
                "Religious or spiritual beliefs",
                "Responsibility to family/pets",
                "Future goals and plans",
                "Positive coping skills",
                "Treatment engagement",
                "Problem-solving skills",
                "Reasons for living",
                "Fear of death/dying",
                "Restricted access to means"
            ],
            
            "intervention_thresholds": {
                "low_risk": "Continue session with safety planning",
                "moderate_risk": "Develop comprehensive safety plan, increase monitoring",
                "high_risk": "Consider hospitalization, remove means, constant supervision",
                "severe_risk": "Immediate hospitalization or emergency intervention"
            }
        }
    
    def _initialize_opening_templates(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "initial_session": {
                "greeting": "Thank you for coming in today. How are you feeling about being here?",
                "orientation": "Let me explain how our sessions will work and what you can expect.",
                "goal_setting": "What are you hoping to accomplish through therapy?",
                "expectation_setting": "What questions do you have about the therapy process?"
            },
            
            "follow_up_session": {
                "greeting": "Good to see you again. How have things been since our last session?",
                "homework_check": "Let's start by reviewing how the homework went.",
                "mood_check": "How has your mood been overall this week?",
                "agenda_setting": "What would you like to focus on in today's session?"
            },
            
            "crisis_session": {
                "immediate_assessment": "I'm glad you reached out. Let's start by making sure you're safe right now.",
                "crisis_exploration": "Can you tell me what's been happening that brought you in today?",
                "safety_planning": "Let's work together to make sure you have a plan to stay safe.",
                "support_activation": "Who can we involve to support you through this difficult time?"
            }
        }
    
    def conduct_session_opening(self, session_id: str, patient_id: str, 
                              session_type: SessionType, therapist_id: str) -> SessionOpening:
        
        opening_template = self.opening_templates.get(f"{session_type.value}_session", 
                                                    self.opening_templates["follow_up_session"])
        
        check_in_protocol = self.check_in_protocols.get(f"{session_type.value}_check_in",
                                                       self.check_in_protocols["standard_check_in"])
        
        session_opening = SessionOpening(
            session_id=session_id,
            patient_id=patient_id,
            session_type=session_type,
            opening_time=datetime.now(),
            therapist_id=therapist_id,
            current_mood="",
            mood_rating=0,
            sleep_quality="",
            medication_compliance="",
            crisis_indicators=[],
            risk_assessment=RiskLevel.LOW,
            presenting_concerns=[],
            session_goals=[],
            homework_completion="",
            significant_events=[],
            therapeutic_alliance=0,
            motivation_level=0
        )
        
        return session_opening
    
    def conduct_mood_check_in(self, session_id: str, patient_id: str) -> List[CheckInResponse]:
        
        mood_questions = [
            "How are you feeling today on a scale of 1-10?",
            "What's your overall mood been like since our last session?",
            "Have you noticed any significant mood changes this week?",
            "What emotions have been most present for you lately?"
        ]
        
        responses = []
        
        for question in mood_questions:
            response = CheckInResponse(
                question=question,
                response="",
                follow_up_needed=False,
                concern_level=0
            )
            responses.append(response)
        
        return responses
    
    def conduct_safety_assessment(self, session_id: str, patient_id: str, 
                                 presenting_concerns: List[str]) -> SafetyAssessment:
        
        requires_full_assessment = any(
            concern.lower() in ["suicide", "self-harm", "hopeless", "death", "crisis"]
            for concern in presenting_concerns
        )
        
        assessment = SafetyAssessment(
            patient_id=patient_id,
            session_id=session_id,
            assessment_date=datetime.now(),
            suicidal_ideation=False,
            suicidal_plan=False,
            suicidal_intent=False,
            self_harm_urges=False,
            homicidal_ideation=False,
            substance_use=False,
            psychotic_symptoms=False,
            risk_factors=[],
            protective_factors=[],
            safety_plan_active=False,
            intervention_needed=False,
            risk_level=RiskLevel.LOW,
            assessor_notes=""
        )
        
        if requires_full_assessment:
            assessment.assessor_notes = "Full safety assessment indicated based on presenting concerns"
        
        self._save_safety_assessment(assessment)
        return assessment
    
    def assess_suicide_risk(self, patient_responses: Dict[str, Any]) -> Tuple[RiskLevel, List[str]]:
        
        risk_score = 0
        risk_factors_present = []
        
        if patient_responses.get("suicidal_ideation"):
            risk_score += 2
            risk_factors_present.append("Active suicidal ideation")
        
        if patient_responses.get("suicidal_plan"):
            risk_score += 3
            risk_factors_present.append("Specific suicide plan")
        
        if patient_responses.get("suicidal_intent"):
            risk_score += 4
            risk_factors_present.append("Intent to act on plan")
        
        if patient_responses.get("previous_attempts"):
            risk_score += 2
            risk_factors_present.append("Previous suicide attempts")
        
        if patient_responses.get("substance_use"):
            risk_score += 1
            risk_factors_present.append("Current substance use")
        
        if patient_responses.get("social_isolation"):
            risk_score += 1
            risk_factors_present.append("Social isolation")
        
        if patient_responses.get("hopelessness"):
            risk_score += 2
            risk_factors_present.append("Feelings of hopelessness")
        
        protective_factors = patient_responses.get("protective_factors", [])
        if len(protective_factors) >= 3:
            risk_score -= 1
        
        if risk_score >= 6:
            risk_level = RiskLevel.SEVERE
        elif risk_score >= 4:
            risk_level = RiskLevel.HIGH
        elif risk_score >= 2:
            risk_level = RiskLevel.MODERATE
        else:
            risk_level = RiskLevel.LOW
        
        return risk_level, risk_factors_present
    
    def create_session_agenda(self, session_opening: SessionOpening, 
                            time_available: int) -> Dict[str, Any]:
        
        agenda = {
            "session_id": session_opening.session_id,
            "total_time": time_available,
            "agenda_items": [],
            "time_allocation": {},
            "priorities": []
        }
        
        if session_opening.risk_assessment in [RiskLevel.HIGH, RiskLevel.SEVERE]:
            agenda["agenda_items"] = [
                "Safety stabilization",
                "Crisis intervention",
                "Safety planning",
                "Support system activation"
            ]
            agenda["time_allocation"] = {
                "safety_work": time_available * 0.8,
                "planning": time_available * 0.2
            }
            agenda["priorities"] = ["immediate_safety", "crisis_management"]
        
        elif session_opening.homework_completion == "not_completed":
            agenda["agenda_items"] = [
                "Homework review and problem-solving",
                "Barrier identification",
                "Skill practice",
                "Modified homework assignment"
            ]
            agenda["time_allocation"] = {
                "homework_review": time_available * 0.3,
                "skill_work": time_available * 0.5,
                "assignment": time_available * 0.2
            }
        
        else:
            agenda["agenda_items"] = [
                "Homework review",
                "Current concerns exploration",
                "Skill building/practice",
                "Session summary and homework"
            ]
            agenda["time_allocation"] = {
                "homework_review": time_available * 0.2,
                "main_work": time_available * 0.6,
                "wrap_up": time_available * 0.2
            }
        
        if session_opening.presenting_concerns:
            agenda["priorities"].extend(session_opening.presenting_concerns[:2])
        
        return agenda
    
    def monitor_therapeutic_alliance(self, session_id: str, patient_id: str,
                                   alliance_indicators: Dict[str, Any]) -> int:
        
        alliance_score = 0
        
        engagement_level = alliance_indicators.get("engagement", "low")
        if engagement_level == "high":
            alliance_score += 3
        elif engagement_level == "medium":
            alliance_score += 2
        elif engagement_level == "low":
            alliance_score += 1
        
        collaboration = alliance_indicators.get("collaboration", "poor")
        if collaboration == "excellent":
            alliance_score += 3
        elif collaboration == "good":
            alliance_score += 2
        elif collaboration == "fair":
            alliance_score += 1
        
        trust_level = alliance_indicators.get("trust", "low")
        if trust_level == "high":
            alliance_score += 2
        elif trust_level == "medium":
            alliance_score += 1
        
        communication = alliance_indicators.get("communication", "poor")
        if communication == "open":
            alliance_score += 2
        elif communication == "guarded":
            alliance_score += 1
        
        return min(alliance_score, 10)
    
    def identify_session_priorities(self, session_opening: SessionOpening) -> List[str]:
        
        priorities = []
        
        if session_opening.risk_assessment in [RiskLevel.HIGH, RiskLevel.SEVERE]:
            priorities.append("immediate_safety_assessment")
            priorities.append("crisis_intervention")
            return priorities
        
        if session_opening.crisis_indicators:
            priorities.append("crisis_stabilization")
        
        if session_opening.mood_rating <= 3:
            priorities.append("mood_stabilization")
        
        if session_opening.homework_completion == "not_completed":
            priorities.append("homework_barrier_resolution")
        
        if session_opening.medication_compliance == "poor":
            priorities.append("medication_adherence")
        
        if session_opening.presenting_concerns:
            priorities.extend([f"address_{concern.lower().replace(' ', '_')}" 
                             for concern in session_opening.presenting_concerns[:2]])
        
        if session_opening.therapeutic_alliance < 6:
            priorities.append("alliance_building")
        
        return priorities[:4]
    
    def generate_opening_summary(self, session_opening: SessionOpening) -> Dict[str, Any]:
        
        summary = {
            "session_id": session_opening.session_id,
            "patient_status": "stable",
            "risk_level": session_opening.risk_assessment.value,
            "mood_status": self._interpret_mood_rating(session_opening.mood_rating),
            "session_readiness": "ready",
            "immediate_concerns": [],
            "recommended_focus": []
        }
        
        if session_opening.risk_assessment in [RiskLevel.HIGH, RiskLevel.SEVERE]:
            summary["patient_status"] = "crisis"
            summary["session_readiness"] = "crisis_intervention_needed"
            summary["immediate_concerns"].append("Safety risk identified")
        
        if session_opening.mood_rating <= 3:
            summary["immediate_concerns"].append("Significantly low mood")
        
        if session_opening.crisis_indicators:
            summary["immediate_concerns"].extend(session_opening.crisis_indicators)
        
        if session_opening.homework_completion == "not_completed":
            summary["recommended_focus"].append("Homework compliance barriers")
        
        if session_opening.presenting_concerns:
            summary["recommended_focus"].extend(session_opening.presenting_concerns)
        
        if session_opening.therapeutic_alliance < 6:
            summary["recommended_focus"].append("Therapeutic relationship building")
        
        return summary
    
    def _interpret_mood_rating(self, rating: int) -> str:
        
        if rating <= 2:
            return "severely_low"
        elif rating <= 4:
            return "low"
        elif rating <= 6:
            return "fair"
        elif rating <= 8:
            return "good"
        else:
            return "very_good"
    
    def _save_session_opening(self, opening: SessionOpening):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO session_openings
                (session_id, patient_id, session_type, opening_time, therapist_id,
                 current_mood, mood_rating, sleep_quality, medication_compliance,
                 crisis_indicators, risk_assessment, presenting_concerns, session_goals,
                 homework_completion, significant_events, therapeutic_alliance,
                 motivation_level, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                opening.session_id, opening.patient_id, opening.session_type.value,
                opening.opening_time.isoformat(), opening.therapist_id,
                opening.current_mood, opening.mood_rating, opening.sleep_quality,
                opening.medication_compliance, json.dumps(opening.crisis_indicators),
                opening.risk_assessment.value, json.dumps(opening.presenting_concerns),
                json.dumps(opening.session_goals), opening.homework_completion,
                json.dumps(opening.significant_events), opening.therapeutic_alliance,
                opening.motivation_level, opening.notes
            ))
    
    def _save_safety_assessment(self, assessment: SafetyAssessment):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO safety_assessments
                (patient_id, session_id, assessment_date, suicidal_ideation,
                 suicidal_plan, suicidal_intent, self_harm_urges, homicidal_ideation,
                 substance_use, psychotic_symptoms, risk_factors, protective_factors,
                 safety_plan_active, intervention_needed, risk_level, assessor_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.patient_id, assessment.session_id, assessment.assessment_date.isoformat(),
                assessment.suicidal_ideation, assessment.suicidal_plan, assessment.suicidal_intent,
                assessment.self_harm_urges, assessment.homicidal_ideation, assessment.substance_use,
                assessment.psychotic_symptoms, json.dumps(assessment.risk_factors),
                json.dumps(assessment.protective_factors), assessment.safety_plan_active,
                assessment.intervention_needed, assessment.risk_level.value, assessment.assessor_notes
            ))
    
    def _save_check_in_response(self, session_id: str, patient_id: str, response: CheckInResponse):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO check_in_responses
                (session_id, patient_id, question, response, follow_up_needed,
                 concern_level, notes, response_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id, patient_id, response.question, response.response,
                response.follow_up_needed, response.concern_level, response.notes,
                datetime.now().isoformat()
            ))


if __name__ == "__main__":
    opening_protocols = SessionOpeningProtocols()
    
    session_opening = opening_protocols.conduct_session_opening(
        session_id="session_001",
        patient_id="patient_123", 
        session_type=SessionType.FOLLOW_UP,
        therapist_id="therapist_001"
    )
    
    print("=== SESSION OPENING ===")
    print(f"Session ID: {session_opening.session_id}")
    print(f"Session Type: {session_opening.session_type.value}")
    print(f"Opening Time: {session_opening.opening_time}")
    
    patient_responses = {
        "suicidal_ideation": False,
        "suicidal_plan": False,
        "suicidal_intent": False,
        "previous_attempts": False,
        "substance_use": False,
        "social_isolation": False,
        "hopelessness": False,
        "protective_factors": ["family support", "future goals", "treatment engagement"]
    }
    
    risk_level, risk_factors = opening_protocols.assess_suicide_risk(patient_responses)
    print(f"\n=== RISK ASSESSMENT ===")
    print(f"Risk Level: {risk_level.value}")
    print(f"Risk Factors: {risk_factors}")
    
    session_opening.risk_assessment = risk_level
    session_opening.mood_rating = 6
    session_opening.homework_completion = "completed"
    session_opening.presenting_concerns = ["anxiety", "work stress"]
    
    agenda = opening_protocols.create_session_agenda(session_opening, 50)
    print(f"\n=== SESSION AGENDA ===")
    print(f"Total Time: {agenda['total_time']} minutes")
    print(f"Agenda Items: {agenda['agenda_items']}")
    print(f"Time Allocation: {agenda['time_allocation']}")
    
    priorities = opening_protocols.identify_session_priorities(session_opening)
    print(f"\n=== SESSION PRIORITIES ===")
    for i, priority in enumerate(priorities, 1):
        print(f"{i}. {priority}")
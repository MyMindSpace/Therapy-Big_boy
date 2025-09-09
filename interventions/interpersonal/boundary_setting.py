import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid
from pathlib import Path


class BoundaryType(Enum):
    PHYSICAL = "physical"
    EMOTIONAL = "emotional"
    TIME = "time"
    MENTAL = "mental"
    DIGITAL = "digital"
    FINANCIAL = "financial"
    SEXUAL = "sexual"
    PROFESSIONAL = "professional"
    FAMILY = "family"
    SOCIAL = "social"


class BoundaryStyle(Enum):
    RIGID = "rigid"
    HEALTHY = "healthy"
    LOOSE = "loose"
    INCONSISTENT = "inconsistent"
    NONEXISTENT = "nonexistent"


class RelationshipContext(Enum):
    ROMANTIC_PARTNER = "romantic_partner"
    FAMILY_MEMBER = "family_member"
    FRIEND = "friend"
    COWORKER = "coworker"
    BOSS_SUPERVISOR = "boss_supervisor"
    ACQUAINTANCE = "acquaintance"
    STRANGER = "stranger"
    AUTHORITY_FIGURE = "authority_figure"
    SERVICE_PROVIDER = "service_provider"
    ONLINE_CONTACT = "online_contact"


class BoundaryViolationSeverity(Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    SEVERE = "severe"


class CommunicationApproach(Enum):
    DIRECT_ASSERTIVE = "direct_assertive"
    GENTLE_FIRM = "gentle_firm"
    COLLABORATIVE = "collaborative"
    PROTECTIVE = "protective"
    PROFESSIONAL = "professional"
    COMPASSIONATE = "compassionate"


@dataclass
class BoundaryRule:
    rule_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    
    boundary_type: BoundaryType = BoundaryType.EMOTIONAL
    relationship_context: RelationshipContext = RelationshipContext.FRIEND
    
    rule_statement: str = ""
    specific_behaviors_allowed: List[str] = field(default_factory=list)
    specific_behaviors_not_allowed: List[str] = field(default_factory=list)
    
    communication_script: str = ""
    enforcement_strategies: List[str] = field(default_factory=list)
    consequences: List[str] = field(default_factory=list)
    
    flexibility_level: int = 5
    importance_rating: int = 8
    
    triggers_that_activate: List[str] = field(default_factory=list)
    warning_signs: List[str] = field(default_factory=list)
    
    support_needed: List[str] = field(default_factory=list)
    practice_scenarios: List[str] = field(default_factory=list)
    
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    active: bool = True


@dataclass 
class BoundaryViolation:
    violation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    boundary_rule_id: Optional[str] = None
    
    date_occurred: datetime = field(default_factory=datetime.now)
    relationship_context: RelationshipContext = RelationshipContext.FRIEND
    violator_description: str = ""
    
    boundary_type: BoundaryType = BoundaryType.EMOTIONAL
    severity: BoundaryViolationSeverity = BoundaryViolationSeverity.MODERATE
    
    description: str = ""
    specific_behaviors: List[str] = field(default_factory=list)
    impact_on_patient: List[str] = field(default_factory=list)
    
    patient_response: str = ""
    response_effectiveness: Optional[int] = None
    
    lessons_learned: List[str] = field(default_factory=list)
    needs_follow_up: bool = False
    follow_up_plan: str = ""
    
    created_date: datetime = field(default_factory=datetime.now)
    resolved: bool = False


@dataclass
class BoundaryPracticeSession:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    boundary_rule_id: str = ""
    
    practice_date: datetime = field(default_factory=datetime.now)
    practice_type: str = "role_play"
    
    scenario_description: str = ""
    communication_approach: CommunicationApproach = CommunicationApproach.DIRECT_ASSERTIVE
    
    script_used: str = ""
    modifications_made: List[str] = field(default_factory=list)
    
    comfort_level_before: int = 1
    comfort_level_after: int = 1
    confidence_rating: int = 1
    
    challenges_encountered: List[str] = field(default_factory=list)
    successes_noted: List[str] = field(default_factory=list)
    
    therapist_feedback: str = ""
    next_practice_goals: List[str] = field(default_factory=list)
    
    created_date: datetime = field(default_factory=datetime.now)


@dataclass
class BoundaryAssessment:
    assessment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    
    assessment_date: datetime = field(default_factory=datetime.now)
    
    boundary_styles_by_context: Dict[str, BoundaryStyle] = field(default_factory=dict)
    boundary_strengths: List[str] = field(default_factory=list)
    boundary_challenges: List[str] = field(default_factory=list)
    
    family_boundary_patterns: List[str] = field(default_factory=list)
    cultural_considerations: List[str] = field(default_factory=list)
    
    violation_history: List[str] = field(default_factory=list)
    current_stressors: List[str] = field(default_factory=list)
    
    support_systems: List[str] = field(default_factory=list)
    motivation_for_change: int = 5
    
    priority_boundary_areas: List[BoundaryType] = field(default_factory=list)
    treatment_goals: List[str] = field(default_factory=list)
    
    created_date: datetime = field(default_factory=datetime.now)


class BoundarySettingSystem:
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self._initialize_database()
        self._populate_default_templates()
    
    def _initialize_database(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS boundary_rules (
                    rule_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    boundary_type TEXT NOT NULL,
                    relationship_context TEXT NOT NULL,
                    rule_statement TEXT NOT NULL,
                    specific_behaviors_allowed TEXT,
                    specific_behaviors_not_allowed TEXT,
                    communication_script TEXT,
                    enforcement_strategies TEXT,
                    consequences TEXT,
                    flexibility_level INTEGER,
                    importance_rating INTEGER,
                    triggers_that_activate TEXT,
                    warning_signs TEXT,
                    support_needed TEXT,
                    practice_scenarios TEXT,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS boundary_violations (
                    violation_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    boundary_rule_id TEXT,
                    date_occurred TEXT NOT NULL,
                    relationship_context TEXT NOT NULL,
                    violator_description TEXT,
                    boundary_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    description TEXT,
                    specific_behaviors TEXT,
                    impact_on_patient TEXT,
                    patient_response TEXT,
                    response_effectiveness INTEGER,
                    lessons_learned TEXT,
                    needs_follow_up BOOLEAN,
                    follow_up_plan TEXT,
                    created_date TEXT NOT NULL,
                    resolved BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                    FOREIGN KEY (boundary_rule_id) REFERENCES boundary_rules (rule_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS boundary_practice_sessions (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    boundary_rule_id TEXT NOT NULL,
                    practice_date TEXT NOT NULL,
                    practice_type TEXT,
                    scenario_description TEXT,
                    communication_approach TEXT,
                    script_used TEXT,
                    modifications_made TEXT,
                    comfort_level_before INTEGER,
                    comfort_level_after INTEGER,
                    confidence_rating INTEGER,
                    challenges_encountered TEXT,
                    successes_noted TEXT,
                    therapist_feedback TEXT,
                    next_practice_goals TEXT,
                    created_date TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                    FOREIGN KEY (boundary_rule_id) REFERENCES boundary_rules (rule_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS boundary_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    assessment_date TEXT NOT NULL,
                    boundary_styles_by_context TEXT,
                    boundary_strengths TEXT,
                    boundary_challenges TEXT,
                    family_boundary_patterns TEXT,
                    cultural_considerations TEXT,
                    violation_history TEXT,
                    current_stressors TEXT,
                    support_systems TEXT,
                    motivation_for_change INTEGER,
                    priority_boundary_areas TEXT,
                    treatment_goals TEXT,
                    created_date TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            conn.commit()
    
    def _populate_default_templates(self):
        pass
    
    def create_boundary_rule(
        self,
        patient_id: str,
        boundary_type: BoundaryType,
        relationship_context: RelationshipContext,
        rule_statement: str,
        importance_rating: int = 8
    ) -> str:
        
        rule = BoundaryRule(
            patient_id=patient_id,
            boundary_type=boundary_type,
            relationship_context=relationship_context,
            rule_statement=rule_statement,
            importance_rating=importance_rating
        )
        
        template_data = self._get_boundary_template(boundary_type, relationship_context)
        rule.communication_script = template_data.get("communication_script", "")
        rule.enforcement_strategies = template_data.get("enforcement_strategies", [])
        rule.consequences = template_data.get("consequences", [])
        rule.practice_scenarios = template_data.get("practice_scenarios", [])
        
        self._save_boundary_rule(rule)
        return rule.rule_id
    
    def _get_boundary_template(self, boundary_type: BoundaryType, context: RelationshipContext) -> Dict[str, Any]:
        templates = {
            (BoundaryType.EMOTIONAL, RelationshipContext.FAMILY_MEMBER): {
                "communication_script": "I understand you care about me, but when you [specific behavior], I feel [emotion]. I need you to [specific request]. Can we agree on this?",
                "enforcement_strategies": [
                    "Calmly restate the boundary",
                    "Leave the conversation if necessary",
                    "Limit contact temporarily if violations continue",
                    "Seek support from other family members"
                ],
                "consequences": [
                    "First violation: verbal reminder",
                    "Second violation: time-out from interaction",
                    "Continued violations: reduced contact"
                ],
                "practice_scenarios": [
                    "Family member gives unsolicited advice about your life choices",
                    "Relative makes critical comments about your appearance",
                    "Family member tries to guilt you into attending events"
                ]
            },
            
            (BoundaryType.TIME, RelationshipContext.COWORKER): {
                "communication_script": "I want to be helpful, but I'm not available to work on this outside of my scheduled hours. Let's discuss how to handle this during work time.",
                "enforcement_strategies": [
                    "Don't respond to non-urgent messages after hours",
                    "Set clear expectations about availability",
                    "Use out-of-office messages consistently",
                    "Involve supervisor if necessary"
                ],
                "consequences": [
                    "Delayed responses to after-hours requests",
                    "Formal discussion with supervisor",
                    "HR involvement if harassment occurs"
                ],
                "practice_scenarios": [
                    "Coworker texts work requests late at night",
                    "Colleague expects immediate responses to emails",
                    "Team member asks you to cover their work repeatedly"
                ]
            },
            
            (BoundaryType.PHYSICAL, RelationshipContext.ACQUAINTANCE): {
                "communication_script": "I'm not comfortable with [physical contact]. Please respect my personal space.",
                "enforcement_strategies": [
                    "Step back physically",
                    "Use clear body language",
                    "State boundary firmly",
                    "Remove yourself from situation if needed"
                ],
                "consequences": [
                    "Immediate physical distancing",
                    "End interaction if necessary",
                    "Avoid future contact if violations continue"
                ],
                "practice_scenarios": [
                    "Someone stands too close in conversation",
                    "Acquaintance tries to hug without permission",
                    "Person touches your arm while talking"
                ]
            },
            
            (BoundaryType.DIGITAL, RelationshipContext.FRIEND): {
                "communication_script": "I value our friendship, but I need some boundaries around social media and texting. I'd prefer if you [specific request].",
                "enforcement_strategies": [
                    "Use privacy settings effectively",
                    "Set specific times for responding",
                    "Be consistent with digital boundaries",
                    "Have direct conversation about expectations"
                ],
                "consequences": [
                    "Mute or unfollow if necessary",
                    "Delayed responses to excessive messages",
                    "Block if harassment occurs"
                ],
                "practice_scenarios": [
                    "Friend posts embarrassing photos of you",
                    "Constant texting throughout the day",
                    "Sharing your personal information online"
                ]
            }
        }
        
        return templates.get((boundary_type, context), {
            "communication_script": "I need to set a boundary about [specific issue]. This is important to me, and I hope you can respect it.",
            "enforcement_strategies": ["State boundary clearly", "Be consistent", "Follow through with consequences"],
            "consequences": ["Reduced interaction", "Seek support", "End relationship if necessary"],
            "practice_scenarios": ["Practice stating the boundary in different situations"]
        })
    
    def _save_boundary_rule(self, rule: BoundaryRule):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO boundary_rules (
                    rule_id, patient_id, boundary_type, relationship_context,
                    rule_statement, specific_behaviors_allowed, specific_behaviors_not_allowed,
                    communication_script, enforcement_strategies, consequences,
                    flexibility_level, importance_rating, triggers_that_activate,
                    warning_signs, support_needed, practice_scenarios,
                    created_date, last_updated, active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                rule.rule_id, rule.patient_id, rule.boundary_type.value,
                rule.relationship_context.value, rule.rule_statement,
                json.dumps(rule.specific_behaviors_allowed),
                json.dumps(rule.specific_behaviors_not_allowed),
                rule.communication_script, json.dumps(rule.enforcement_strategies),
                json.dumps(rule.consequences), rule.flexibility_level,
                rule.importance_rating, json.dumps(rule.triggers_that_activate),
                json.dumps(rule.warning_signs), json.dumps(rule.support_needed),
                json.dumps(rule.practice_scenarios), rule.created_date.isoformat(),
                rule.last_updated.isoformat(), rule.active
            ))
            
            conn.commit()
    
    def get_boundary_rule(self, rule_id: str) -> Optional[BoundaryRule]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM boundary_rules WHERE rule_id = ?
            """, (rule_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return BoundaryRule(
                rule_id=row[0],
                patient_id=row[1],
                boundary_type=BoundaryType(row[2]),
                relationship_context=RelationshipContext(row[3]),
                rule_statement=row[4],
                specific_behaviors_allowed=json.loads(row[5] or '[]'),
                specific_behaviors_not_allowed=json.loads(row[6] or '[]'),
                communication_script=row[7] or "",
                enforcement_strategies=json.loads(row[8] or '[]'),
                consequences=json.loads(row[9] or '[]'),
                flexibility_level=row[10] or 5,
                importance_rating=row[11] or 8,
                triggers_that_activate=json.loads(row[12] or '[]'),
                warning_signs=json.loads(row[13] or '[]'),
                support_needed=json.loads(row[14] or '[]'),
                practice_scenarios=json.loads(row[15] or '[]'),
                created_date=datetime.fromisoformat(row[16]),
                last_updated=datetime.fromisoformat(row[17]),
                active=bool(row[18])
            )
    
    def get_patient_boundary_rules(self, patient_id: str, active_only: bool = True) -> List[BoundaryRule]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM boundary_rules WHERE patient_id = ?"
            params = [patient_id]
            
            if active_only:
                query += " AND active = TRUE"
            
            query += " ORDER BY importance_rating DESC, created_date DESC"
            
            cursor.execute(query, params)
            
            rules = []
            for row in cursor.fetchall():
                rule = BoundaryRule(
                    rule_id=row[0],
                    patient_id=row[1],
                    boundary_type=BoundaryType(row[2]),
                    relationship_context=RelationshipContext(row[3]),
                    rule_statement=row[4],
                    specific_behaviors_allowed=json.loads(row[5] or '[]'),
                    specific_behaviors_not_allowed=json.loads(row[6] or '[]'),
                    communication_script=row[7] or "",
                    enforcement_strategies=json.loads(row[8] or '[]'),
                    consequences=json.loads(row[9] or '[]'),
                    flexibility_level=row[10] or 5,
                    importance_rating=row[11] or 8,
                    triggers_that_activate=json.loads(row[12] or '[]'),
                    warning_signs=json.loads(row[13] or '[]'),
                    support_needed=json.loads(row[14] or '[]'),
                    practice_scenarios=json.loads(row[15] or '[]'),
                    created_date=datetime.fromisoformat(row[16]),
                    last_updated=datetime.fromisoformat(row[17]),
                    active=bool(row[18])
                )
                rules.append(rule)
            
            return rules
    
    def log_boundary_violation(
        self,
        patient_id: str,
        boundary_type: BoundaryType,
        relationship_context: RelationshipContext,
        description: str,
        severity: BoundaryViolationSeverity = BoundaryViolationSeverity.MODERATE,
        boundary_rule_id: Optional[str] = None
    ) -> str:
        
        violation = BoundaryViolation(
            patient_id=patient_id,
            boundary_rule_id=boundary_rule_id,
            boundary_type=boundary_type,
            relationship_context=relationship_context,
            description=description,
            severity=severity
        )
        
        self._save_boundary_violation(violation)
        return violation.violation_id
    
    def _save_boundary_violation(self, violation: BoundaryViolation):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO boundary_violations (
                    violation_id, patient_id, boundary_rule_id, date_occurred,
                    relationship_context, violator_description, boundary_type,
                    severity, description, specific_behaviors, impact_on_patient,
                    patient_response, response_effectiveness, lessons_learned,
                    needs_follow_up, follow_up_plan, created_date, resolved
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                violation.violation_id, violation.patient_id, violation.boundary_rule_id,
                violation.date_occurred.isoformat(), violation.relationship_context.value,
                violation.violator_description, violation.boundary_type.value,
                violation.severity.value, violation.description,
                json.dumps(violation.specific_behaviors),
                json.dumps(violation.impact_on_patient), violation.patient_response,
                violation.response_effectiveness, json.dumps(violation.lessons_learned),
                violation.needs_follow_up, violation.follow_up_plan,
                violation.created_date.isoformat(), violation.resolved
            ))
            
            conn.commit()
    
    def conduct_boundary_practice(
        self,
        patient_id: str,
        boundary_rule_id: str,
        scenario_description: str,
        communication_approach: CommunicationApproach = CommunicationApproach.DIRECT_ASSERTIVE
    ) -> str:
        
        rule = self.get_boundary_rule(boundary_rule_id)
        if not rule:
            return ""
        
        session = BoundaryPracticeSession(
            patient_id=patient_id,
            boundary_rule_id=boundary_rule_id,
            scenario_description=scenario_description,
            communication_approach=communication_approach,
            script_used=rule.communication_script
        )
        
        self._save_practice_session(session)
        return session.session_id
    
    def _save_practice_session(self, session: BoundaryPracticeSession):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO boundary_practice_sessions (
                    session_id, patient_id, boundary_rule_id, practice_date,
                    practice_type, scenario_description, communication_approach,
                    script_used, modifications_made, comfort_level_before,
                    comfort_level_after, confidence_rating, challenges_encountered,
                    successes_noted, therapist_feedback, next_practice_goals,
                    created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id, session.patient_id, session.boundary_rule_id,
                session.practice_date.isoformat(), session.practice_type,
                session.scenario_description, session.communication_approach.value,
                session.script_used, json.dumps(session.modifications_made),
                session.comfort_level_before, session.comfort_level_after,
                session.confidence_rating, json.dumps(session.challenges_encountered),
                json.dumps(session.successes_noted), session.therapist_feedback,
                json.dumps(session.next_practice_goals), session.created_date.isoformat()
            ))
            
            conn.commit()
    
    def update_practice_session_feedback(
        self,
        session_id: str,
        comfort_after: int,
        confidence_rating: int,
        challenges: List[str] = None,
        successes: List[str] = None,
        therapist_feedback: str = ""
    ) -> bool:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE boundary_practice_sessions SET
                    comfort_level_after = ?,
                    confidence_rating = ?,
                    challenges_encountered = ?,
                    successes_noted = ?,
                    therapist_feedback = ?
                WHERE session_id = ?
            """, (
                comfort_after, confidence_rating,
                json.dumps(challenges or []), json.dumps(successes or []),
                therapist_feedback, session_id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def conduct_boundary_assessment(self, patient_id: str) -> str:
        assessment_questions = self._get_assessment_questions()
        
        assessment = BoundaryAssessment(
            patient_id=patient_id,
            boundary_styles_by_context={
                context.value: BoundaryStyle.HEALTHY.value 
                for context in RelationshipContext
            },
            treatment_goals=[
                "Identify current boundary patterns",
                "Develop healthy boundary setting skills",
                "Practice assertive communication",
                "Build confidence in maintaining boundaries"
            ]
        )
        
        self._save_boundary_assessment(assessment)
        return assessment.assessment_id
    
    def _get_assessment_questions(self) -> List[Dict[str, Any]]:
        return [
            {
                "category": "family_boundaries",
                "questions": [
                    "How comfortable are you saying 'no' to family members?",
                    "Do family members respect your privacy and personal choices?",
                    "How do you handle criticism or unwanted advice from family?",
                    "Are you able to limit contact with family when needed?"
                ]
            },
            {
                "category": "work_boundaries", 
                "questions": [
                    "Do you work outside of scheduled hours regularly?",
                    "How comfortable are you declining additional work requests?",
                    "Do you respond to work communications during personal time?",
                    "Are you able to take breaks and vacation time without guilt?"
                ]
            },
            {
                "category": "friendship_boundaries",
                "questions": [
                    "Do you feel obligated to always be available for friends?",
                    "How do you handle friends who drain your energy?",
                    "Are you comfortable expressing disagreement with friends?",
                    "Do you maintain friendships that don't feel reciprocal?"
                ]
            },
            {
                "category": "physical_boundaries",
                "questions": [
                    "Are you comfortable with your personal space being respected?",
                    "How do you respond when someone touches you without permission?",
                    "Do you feel safe setting limits on physical contact?",
                    "Are you able to leave situations where you feel physically uncomfortable?"
                ]
            }
        ]
    
    def _save_boundary_assessment(self, assessment: BoundaryAssessment):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO boundary_assessments (
                    assessment_id, patient_id, assessment_date,
                    boundary_styles_by_context, boundary_strengths, boundary_challenges,
                    family_boundary_patterns, cultural_considerations, violation_history,
                    current_stressors, support_systems, motivation_for_change,
                    priority_boundary_areas, treatment_goals, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id, assessment.patient_id,
                assessment.assessment_date.isoformat(),
                json.dumps(assessment.boundary_styles_by_context),
                json.dumps(assessment.boundary_strengths),
                json.dumps(assessment.boundary_challenges),
                json.dumps(assessment.family_boundary_patterns),
                json.dumps(assessment.cultural_considerations),
                json.dumps(assessment.violation_history),
                json.dumps(assessment.current_stressors),
                json.dumps(assessment.support_systems),
                assessment.motivation_for_change,
                json.dumps([area.value for area in assessment.priority_boundary_areas]),
                json.dumps(assessment.treatment_goals),
                assessment.created_date.isoformat()
            ))
            
            conn.commit()
    
    def get_boundary_violations(
        self,
        patient_id: str,
        days_back: int = 30,
        severity_filter: Optional[BoundaryViolationSeverity] = None
    ) -> List[BoundaryViolation]:
        
        start_date = datetime.now() - timedelta(days=days_back)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM boundary_violations 
                WHERE patient_id = ? AND date_occurred >= ?
            """
            params = [patient_id, start_date.isoformat()]
            
            if severity_filter:
                query += " AND severity = ?"
                params.append(severity_filter.value)
            
            query += " ORDER BY date_occurred DESC"
            
            cursor.execute(query, params)
            
            violations = []
            for row in cursor.fetchall():
                violation = BoundaryViolation(
                    violation_id=row[0],
                    patient_id=row[1],
                    boundary_rule_id=row[2],
                    date_occurred=datetime.fromisoformat(row[3]),
                    relationship_context=RelationshipContext(row[4]),
                    violator_description=row[5] or "",
                    boundary_type=BoundaryType(row[6]),
                    severity=BoundaryViolationSeverity(row[7]),
                    description=row[8] or "",
                    specific_behaviors=json.loads(row[9] or '[]'),
                    impact_on_patient=json.loads(row[10] or '[]'),
                    patient_response=row[11] or "",
                    response_effectiveness=row[12],
                    lessons_learned=json.loads(row[13] or '[]'),
                    needs_follow_up=bool(row[14]),
                    follow_up_plan=row[15] or "",
                    created_date=datetime.fromisoformat(row[16]),
                    resolved=bool(row[17])
                )
                violations.append(violation)
            
            return violations
    
    def generate_boundary_scripts(
        self,
        boundary_type: BoundaryType,
        relationship_context: RelationshipContext,
        specific_situation: str = "",
        communication_style: str = "assertive"
    ) -> Dict[str, str]:
        
        base_scripts = {
            "direct": "I need to set a boundary about {situation}. {specific_request}. I hope you can respect this.",
            "gentle": "I've been thinking about our {relationship}, and I'd like to discuss {situation}. Would it be okay if {specific_request}?",
            "firm": "I'm not comfortable with {situation}. I need {specific_request}, and this isn't negotiable.",
            "collaborative": "I'd like us to figure out a way to handle {situation} that works for both of us. What if {specific_request}?"
        }
        
        situation_templates = {
            BoundaryType.TIME: {
                "situation": "time boundaries",
                "specific_request": "we respect each other's schedules and don't expect immediate responses outside of agreed hours"
            },
            BoundaryType.EMOTIONAL: {
                "situation": "emotional boundaries", 
                "specific_request": "we avoid topics that feel too personal or overwhelming"
            },
            BoundaryType.PHYSICAL: {
                "situation": "physical space",
                "specific_request": "we ask before hugging or touching, and respect personal space"
            },
            BoundaryType.DIGITAL: {
                "situation": "digital communication",
                "specific_request": "we set limits on sharing personal information online"
            }
        }
        
        context_adjustments = {
            RelationshipContext.FAMILY_MEMBER: "our family relationship",
            RelationshipContext.COWORKER: "our work relationship",
            RelationshipContext.FRIEND: "our friendship",
            RelationshipContext.ROMANTIC_PARTNER: "our relationship"
        }
        
        template = situation_templates.get(boundary_type, {
            "situation": "this issue",
            "specific_request": "we handle this differently"
        })
        
        relationship = context_adjustments.get(relationship_context, "our interaction")
        
        scripts = {}
        for style, script_template in base_scripts.items():
            scripts[style] = script_template.format(
                situation=specific_situation or template["situation"],
                specific_request=template["specific_request"],
                relationship=relationship
            )
        
        return scripts
    
    def get_boundary_enforcement_strategies(
        self,
        boundary_type: BoundaryType,
        relationship_context: RelationshipContext,
        severity: BoundaryViolationSeverity = BoundaryViolationSeverity.MODERATE
    ) -> List[str]:
        
        base_strategies = {
            "gentle_reminder": "Calmly restate the boundary",
            "clear_communication": "Use 'I' statements to express impact", 
            "natural_consequences": "Allow natural consequences to occur",
            "time_limits": "Set time limits on interactions",
            "physical_distance": "Create physical distance when needed",
            "support_system": "Involve trusted friends or family for support",
            "professional_help": "Seek professional mediation if needed",
            "documentation": "Keep records of violations if necessary",
            "legal_action": "Consider legal options for severe violations"
        }
        
        severity_appropriate = {
            BoundaryViolationSeverity.MINOR: [
                "gentle_reminder", "clear_communication", "time_limits"
            ],
            BoundaryViolationSeverity.MODERATE: [
                "gentle_reminder", "clear_communication", "natural_consequences", 
                "time_limits", "physical_distance", "support_system"
            ],
            BoundaryViolationSeverity.MAJOR: [
                "clear_communication", "natural_consequences", "physical_distance", 
                "support_system", "professional_help", "documentation"
            ],
            BoundaryViolationSeverity.SEVERE: [
                "physical_distance", "support_system", "professional_help", 
                "documentation", "legal_action"
            ]
        }
        
        context_specific = {
            RelationshipContext.FAMILY_MEMBER: [
                "Set visiting limits", "Use neutral meeting places", 
                "Have conversations with witnesses present"
            ],
            RelationshipContext.COWORKER: [
                "Involve supervisor", "Document interactions", 
                "Use official communication channels"
            ],
            RelationshipContext.ROMANTIC_PARTNER: [
                "Couple's counseling", "Individual therapy", 
                "Safety planning if needed"
            ],
            RelationshipContext.FRIEND: [
                "Reduce frequency of contact", "Group settings only", 
                "Clear communication of expectations"
            ]
        }
        
        strategies = []
        for strategy_key in severity_appropriate.get(severity, []):
            strategies.append(base_strategies[strategy_key])
        
        if relationship_context in context_specific:
            strategies.extend(context_specific[relationship_context])
        
        return strategies
    
    def create_boundary_action_plan(
        self,
        patient_id: str,
        boundary_rule_id: str,
        target_relationship: str = "",
        timeline_weeks: int = 4
    ) -> Dict[str, Any]:
        
        rule = self.get_boundary_rule(boundary_rule_id)
        if not rule:
            return {}
        
        violations = self.get_boundary_violations(patient_id, days_back=90)
        related_violations = [v for v in violations if v.boundary_rule_id == boundary_rule_id]
        
        action_plan = {
            "patient_id": patient_id,
            "boundary_rule_id": boundary_rule_id,
            "rule_statement": rule.rule_statement,
            "target_relationship": target_relationship,
            "timeline_weeks": timeline_weeks,
            "created_date": datetime.now().isoformat(),
            
            "preparation_phase": {
                "week": 1,
                "activities": [
                    "Review and refine boundary statement",
                    "Practice communication scripts in therapy",
                    "Identify support system",
                    "Plan timing and setting for conversation"
                ],
                "homework": [
                    "Write out boundary statement in your own words",
                    "Role-play with trusted friend or therapist",
                    "Identify 3 people who can support you"
                ]
            },
            
            "implementation_phase": {
                "week": 2,
                "activities": [
                    "Have initial boundary conversation",
                    "Use prepared scripts and stay calm",
                    "Document the interaction",
                    "Debrief with therapist or support person"
                ],
                "homework": [
                    "Set the boundary in real life",
                    "Keep a journal of responses and feelings",
                    "Practice self-care after difficult conversations"
                ]
            },
            
            "reinforcement_phase": {
                "weeks": [3, 4],
                "activities": [
                    "Consistently enforce the boundary",
                    "Use consequences when needed",
                    "Continue to communicate clearly",
                    "Seek support when challenged"
                ],
                "homework": [
                    "Track boundary violations and responses",
                    "Celebrate small successes",
                    "Adjust strategies based on what works"
                ]
            },
            
            "potential_challenges": [
                "Guilt or anxiety about setting boundaries",
                "Pushback or anger from others",
                "Temptation to give in to maintain peace",
                "Fear of relationship damage"
            ],
            
            "coping_strategies": [
                "Remember your right to have boundaries",
                "Use grounding techniques during difficult conversations",
                "Have support person on standby",
                "Practice self-compassion"
            ],
            
            "success_indicators": [
                "Able to state boundary clearly and calmly",
                "Reduced anxiety about the relationship",
                "Other person begins respecting the boundary",
                "Increased sense of self-respect and empowerment"
            ]
        }
        
        if related_violations:
            recent_patterns = {}
            for violation in related_violations:
                for behavior in violation.specific_behaviors:
                    recent_patterns[behavior] = recent_patterns.get(behavior, 0) + 1
            
            action_plan["common_violation_patterns"] = sorted(
                recent_patterns.items(), key=lambda x: x[1], reverse=True
            )[:3]
        
        return action_plan
    
    def generate_progress_report(self, patient_id: str, days_back: int = 90) -> Dict[str, Any]:
        rules = self.get_patient_boundary_rules(patient_id)
        violations = self.get_boundary_violations(patient_id, days_back)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM boundary_practice_sessions 
                WHERE patient_id = ? AND practice_date >= ?
                ORDER BY practice_date DESC
            """, (patient_id, (datetime.now() - timedelta(days=days_back)).isoformat()))
            
            practice_sessions = cursor.fetchall()
        
        total_rules = len(rules)
        active_rules = len([r for r in rules if r.active])
        
        violation_summary = {
            "total_violations": len(violations),
            "by_severity": {},
            "by_type": {},
            "by_context": {}
        }
        
        for violation in violations:
            severity = violation.severity.value
            boundary_type = violation.boundary_type.value
            context = violation.relationship_context.value
            
            violation_summary["by_severity"][severity] = violation_summary["by_severity"].get(severity, 0) + 1
            violation_summary["by_type"][boundary_type] = violation_summary["by_type"].get(boundary_type, 0) + 1
            violation_summary["by_context"][context] = violation_summary["by_context"].get(context, 0) + 1
        
        practice_summary = {
            "total_sessions": len(practice_sessions),
            "avg_confidence_improvement": 0,
            "avg_comfort_improvement": 0
        }
        
        if practice_sessions:
            confidence_improvements = []
            comfort_improvements = []
            
            for session in practice_sessions:
                if session[10] is not None and session[9] is not None:  # comfort_before and after
                    comfort_improvements.append(session[10] - session[9])
                if session[11] is not None:  # confidence_rating
                    confidence_improvements.append(session[11])
            
            if comfort_improvements:
                practice_summary["avg_comfort_improvement"] = sum(comfort_improvements) / len(comfort_improvements)
            if confidence_improvements:
                practice_summary["avg_confidence_improvement"] = sum(confidence_improvements) / len(confidence_improvements)
        
        weekly_violation_trend = {}
        for violation in violations:
            week = violation.date_occurred.isocalendar()[1]
            weekly_violation_trend[week] = weekly_violation_trend.get(week, 0) + 1
        
        trend_direction = "stable"
        if len(weekly_violation_trend) >= 4:
            weeks = sorted(weekly_violation_trend.keys())
            early_avg = sum(weekly_violation_trend[w] for w in weeks[:len(weeks)//2]) / (len(weeks)//2)
            late_avg = sum(weekly_violation_trend[w] for w in weeks[len(weeks)//2:]) / (len(weeks) - len(weeks)//2)
            
            if late_avg < early_avg * 0.7:
                trend_direction = "improving"
            elif late_avg > early_avg * 1.3:
                trend_direction = "worsening"
        
        insights = []
        
        if violation_summary["total_violations"] == 0:
            insights.append("No boundary violations recorded - excellent boundary maintenance")
        elif violation_summary["total_violations"] < 5:
            insights.append("Low violation count indicates good boundary awareness")
        elif violation_summary["total_violations"] > 15:
            insights.append("High violation count suggests need for stronger enforcement strategies")
        
        if practice_summary["total_sessions"] >= 4:
            insights.append("Consistent practice shows commitment to boundary skill development")
        elif practice_summary["total_sessions"] < 2:
            insights.append("Increase boundary practice sessions for better skill consolidation")
        
        if practice_summary["avg_confidence_improvement"] >= 7:
            insights.append("High confidence scores indicate good progress in boundary setting")
        
        most_common_violation_type = max(violation_summary["by_type"], key=violation_summary["by_type"].get) if violation_summary["by_type"] else None
        if most_common_violation_type:
            insights.append(f"Focus on {most_common_violation_type} boundaries - most frequent violation type")
        
        return {
            "patient_id": patient_id,
            "report_period_days": days_back,
            "boundary_rules_summary": {
                "total_rules": total_rules,
                "active_rules": active_rules,
                "most_important_areas": [r.boundary_type.value for r in sorted(rules, key=lambda x: x.importance_rating, reverse=True)[:3]]
            },
            "violation_summary": violation_summary,
            "practice_summary": practice_summary,
            "weekly_trend": {
                "direction": trend_direction,
                "weekly_violations": dict(weekly_violation_trend)
            },
            "insights": insights,
            "recommendations": self._generate_boundary_recommendations(rules, violations, practice_sessions),
            "generated_date": datetime.now().isoformat()
        }
    
    def _generate_boundary_recommendations(self, rules, violations, practice_sessions) -> List[str]:
        recommendations = []
        
        if not rules:
            recommendations.extend([
                "Begin with boundary assessment to identify priority areas",
                "Start with one clear, important boundary in a safe relationship",
                "Practice boundary scripts in therapy before real-world use"
            ])
            return recommendations
        
        if len(violations) > len(rules) * 2:
            recommendations.append("Focus on enforcement strategies - violations exceeding established boundaries")
        
        if len(practice_sessions) < len(rules):
            recommendations.append("Increase practice sessions for each boundary rule")
        
        violation_contexts = {}
        for violation in violations:
            context = violation.relationship_context.value
            violation_contexts[context] = violation_contexts.get(context, 0) + 1
        
        if violation_contexts:
            most_problematic = max(violation_contexts, key=violation_contexts.get)
            recommendations.append(f"Prioritize boundary work in {most_problematic} relationships")
        
        low_confidence_areas = []
        for session in practice_sessions:
            if session[11] is not None and session[11] < 5:  # confidence_rating
                low_confidence_areas.append(session[2])  # boundary_rule_id
        
        if low_confidence_areas:
            recommendations.append("Additional practice needed for rules with low confidence ratings")
        
        unresolved_violations = [v for v in violations if not v.resolved]
        if unresolved_violations:
            recommendations.append("Address unresolved boundary violations with specific action plans")
        
        high_importance_rules = [r for r in rules if r.importance_rating >= 8]
        if high_importance_rules and len(practice_sessions) < len(high_importance_rules) * 2:
            recommendations.append("Increase practice frequency for high-importance boundaries")
        
        return recommendations
    
    def get_boundary_reminders(self, patient_id: str) -> List[Dict[str, str]]:
        rules = self.get_patient_boundary_rules(patient_id)
        violations = self.get_boundary_violations(patient_id, days_back=7)
        
        reminders = []
        
        recent_violation_rules = {v.boundary_rule_id for v in violations if v.boundary_rule_id}
        
        for rule in rules:
            if rule.rule_id in recent_violation_rules:
                reminders.append({
                    "type": "violation_follow_up",
                    "message": f"Remember: {rule.rule_statement}",
                    "action": "Practice your communication script for this boundary",
                    "boundary_type": rule.boundary_type.value
                })
        
        high_priority_rules = [r for r in rules if r.importance_rating >= 8][:3]
        for rule in high_priority_rules:
            if rule.rule_id not in recent_violation_rules:
                reminders.append({
                    "type": "maintenance",
                    "message": f"Keep maintaining: {rule.rule_statement}",
                    "action": "Notice if this boundary feels strong or needs reinforcement",
                    "boundary_type": rule.boundary_type.value
                })
        
        if not reminders:
            reminders.append({
                "type": "general",
                "message": "Your boundaries are your responsibility and your right",
                "action": "Check in with yourself about how your boundaries are feeling today",
                "boundary_type": "general"
            })
        
        return reminders
    
    def export_boundary_data(self, patient_id: str) -> Dict[str, Any]:
        rules = self.get_patient_boundary_rules(patient_id, active_only=False)
        violations = self.get_boundary_violations(patient_id, days_back=365)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM boundary_practice_sessions 
                WHERE patient_id = ?
                ORDER BY practice_date DESC
            """, (patient_id,))
            
            practice_sessions = cursor.fetchall()
            
            cursor.execute("""
                SELECT * FROM boundary_assessments 
                WHERE patient_id = ?
                ORDER BY assessment_date DESC
                LIMIT 1
            """, (patient_id,))
            
            assessment = cursor.fetchone()
        
        export_data = {
            "patient_id": patient_id,
            "export_date": datetime.now().isoformat(),
            "boundary_rules": [
                {
                    "rule_id": rule.rule_id,
                    "boundary_type": rule.boundary_type.value,
                    "relationship_context": rule.relationship_context.value,
                    "rule_statement": rule.rule_statement,
                    "importance_rating": rule.importance_rating,
                    "communication_script": rule.communication_script,
                    "enforcement_strategies": rule.enforcement_strategies,
                    "active": rule.active,
                    "created_date": rule.created_date.isoformat()
                }
                for rule in rules
            ],
            "violations": [
                {
                    "date": violation.date_occurred.isoformat(),
                    "boundary_type": violation.boundary_type.value,
                    "relationship_context": violation.relationship_context.value,
                    "severity": violation.severity.value,
                    "description": violation.description,
                    "patient_response": violation.patient_response,
                    "resolved": violation.resolved
                }
                for violation in violations
            ],
            "practice_sessions_count": len(practice_sessions),
            "latest_assessment": {
                "date": datetime.fromisoformat(assessment[2]).isoformat() if assessment else None,
                "boundary_strengths": json.loads(assessment[4]) if assessment else [],
                "boundary_challenges": json.loads(assessment[5]) if assessment else [],
                "treatment_goals": json.loads(assessment[13]) if assessment else []
            } if assessment else None
        }
        
        return export_data


def create_boundary_worksheet(boundary_type: BoundaryType, relationship_context: RelationshipContext) -> Dict[str, Any]:
    return {
        "boundary_type": boundary_type.value,
        "relationship_context": relationship_context.value,
        "reflection_questions": [
            "What specific behaviors make me uncomfortable in this relationship?",
            "What am I willing to accept, and what am I not willing to accept?",
            "How have I communicated my needs in the past?",
            "What fears do I have about setting this boundary?",
            "What support do I need to maintain this boundary?"
        ],
        "boundary_statement_template": "When [specific behavior occurs], I feel [emotion]. I need [specific request]. If this continues, I will [consequence].",
        "practice_scenarios": [
            "The person respects your boundary immediately",
            "The person asks questions about your boundary", 
            "The person pushes back or argues",
            "The person ignores your boundary",
            "The person tries to guilt or manipulate you"
        ],
        "self_care_reminders": [
            "Setting boundaries is not selfish - it's necessary",
            "You cannot control others' reactions, only your own responses",
            "Boundaries may feel uncomfortable at first, but get easier with practice",
            "It's okay to start small and build up to bigger boundaries",
            "You deserve relationships where your boundaries are respected"
        ]
    }


if __name__ == "__main__":
    boundary_system = BoundarySettingSystem()
    
    patient_id = "test_patient_001"
    
    rule_id = boundary_system.create_boundary_rule(
        patient_id=patient_id,
        boundary_type=BoundaryType.TIME,
        relationship_context=RelationshipContext.COWORKER,
        rule_statement="I will not respond to work emails after 7 PM or on weekends",
        importance_rating=9
    )
    
    violation_id = boundary_system.log_boundary_violation(
        patient_id=patient_id,
        boundary_type=BoundaryType.TIME,
        relationship_context=RelationshipContext.COWORKER,
        description="Coworker sent urgent email at 10 PM expecting immediate response",
        severity=BoundaryViolationSeverity.MODERATE,
        boundary_rule_id=rule_id
    )
    
    practice_id = boundary_system.conduct_boundary_practice(
        patient_id=patient_id,
        boundary_rule_id=rule_id,
        scenario_description="Practicing response to after-hours work requests"
    )
    
    boundary_system.update_practice_session_feedback(
        session_id=practice_id,
        comfort_after=7,
        confidence_rating=8,
        successes=["Used clear, professional language", "Felt more confident"],
        therapist_feedback="Excellent progress on assertive communication"
    )
    
    action_plan = boundary_system.create_boundary_action_plan(
        patient_id=patient_id,
        boundary_rule_id=rule_id,
        target_relationship="Work colleague",
        timeline_weeks=4
    )
    
    report = boundary_system.generate_progress_report(patient_id, 30)
    
    print(f"Boundary rule created: {rule_id}")
    print(f"Violation logged: {violation_id}")
    print(f"Practice session: {practice_id}")
    print(f"Action plan created for {action_plan['timeline_weeks']} weeks")
    print(f"Progress report shows {report['boundary_rules_summary']['total_rules']} active boundaries")
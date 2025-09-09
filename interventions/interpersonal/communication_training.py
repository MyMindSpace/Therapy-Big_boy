import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid
from pathlib import Path


class CommunicationSkill(Enum):
    ACTIVE_LISTENING = "active_listening"
    ASSERTIVENESS = "assertiveness"
    EMPATHY = "empathy"
    CONFLICT_RESOLUTION = "conflict_resolution"
    NONVERBAL_COMMUNICATION = "nonverbal_communication"
    EMOTIONAL_EXPRESSION = "emotional_expression"
    FEEDBACK_GIVING = "feedback_giving"
    FEEDBACK_RECEIVING = "feedback_receiving"
    NEGOTIATION = "negotiation"
    SMALL_TALK = "small_talk"
    PUBLIC_SPEAKING = "public_speaking"
    DIFFICULT_CONVERSATIONS = "difficult_conversations"


class CommunicationStyle(Enum):
    PASSIVE = "passive"
    AGGRESSIVE = "aggressive"
    PASSIVE_AGGRESSIVE = "passive_aggressive"
    ASSERTIVE = "assertive"
    MANIPULATIVE = "manipulative"


class ConversationType(Enum):
    CASUAL_SOCIAL = "casual_social"
    PROFESSIONAL = "professional"
    INTIMATE_PERSONAL = "intimate_personal"
    CONFLICT_DISCUSSION = "conflict_discussion"
    FEEDBACK_SESSION = "feedback_session"
    NEGOTIATION = "negotiation"
    GROUP_DISCUSSION = "group_discussion"
    PRESENTATION = "presentation"
    JOB_INTERVIEW = "job_interview"
    DIFFICULT_NEWS = "difficult_news"


class PracticeFormat(Enum):
    ROLE_PLAY = "role_play"
    MIRROR_PRACTICE = "mirror_practice"
    RECORDING_REVIEW = "recording_review"
    WRITTEN_SCRIPTS = "written_scripts"
    REAL_WORLD_HOMEWORK = "real_world_homework"
    GROUP_PRACTICE = "group_practice"
    THERAPIST_MODELING = "therapist_modeling"


class NonverbalElement(Enum):
    EYE_CONTACT = "eye_contact"
    FACIAL_EXPRESSION = "facial_expression"
    BODY_POSTURE = "body_posture"
    HAND_GESTURES = "hand_gestures"
    VOICE_TONE = "voice_tone"
    SPEAKING_PACE = "speaking_pace"
    PERSONAL_SPACE = "personal_space"
    ACTIVE_LISTENING_CUES = "active_listening_cues"


@dataclass
class CommunicationSkillModule:
    module_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    skill: CommunicationSkill = CommunicationSkill.ACTIVE_LISTENING
    module_name: str = ""
    
    learning_objectives: List[str] = field(default_factory=list)
    key_concepts: List[str] = field(default_factory=list)
    techniques: List[str] = field(default_factory=list)
    
    practice_exercises: List[str] = field(default_factory=list)
    role_play_scenarios: List[str] = field(default_factory=list)
    homework_assignments: List[str] = field(default_factory=list)
    
    common_mistakes: List[str] = field(default_factory=list)
    troubleshooting_tips: List[str] = field(default_factory=list)
    
    difficulty_level: int = 1
    estimated_sessions: int = 3
    prerequisite_skills: List[CommunicationSkill] = field(default_factory=list)
    
    assessment_criteria: List[str] = field(default_factory=list)
    success_indicators: List[str] = field(default_factory=list)
    
    created_date: datetime = field(default_factory=datetime.now)


@dataclass
class CommunicationPracticeSession:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    skill_focus: CommunicationSkill = CommunicationSkill.ACTIVE_LISTENING
    
    session_date: datetime = field(default_factory=datetime.now)
    duration_minutes: int = 45
    
    conversation_type: ConversationType = ConversationType.CASUAL_SOCIAL
    practice_format: PracticeFormat = PracticeFormat.ROLE_PLAY
    
    scenario_description: str = ""
    learning_goals: List[str] = field(default_factory=list)
    
    pre_session_confidence: int = 1
    post_session_confidence: int = 1
    pre_session_anxiety: int = 10
    post_session_anxiety: int = 10
    
    techniques_practiced: List[str] = field(default_factory=list)
    challenges_encountered: List[str] = field(default_factory=list)
    breakthroughs_achieved: List[str] = field(default_factory=list)
    
    nonverbal_skills_rating: Dict[str, int] = field(default_factory=dict)
    verbal_skills_rating: Dict[str, int] = field(default_factory=dict)
    
    therapist_observations: str = ""
    patient_self_reflection: str = ""
    
    homework_assigned: List[str] = field(default_factory=list)
    next_session_goals: List[str] = field(default_factory=list)
    
    overall_effectiveness: int = 5
    created_date: datetime = field(default_factory=datetime.now)


@dataclass
class CommunicationAssessment:
    assessment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    
    assessment_date: datetime = field(default_factory=datetime.now)
    assessment_type: str = "comprehensive"
    
    dominant_communication_style: CommunicationStyle = CommunicationStyle.PASSIVE
    style_flexibility: int = 5
    
    skill_ratings: Dict[str, int] = field(default_factory=dict)
    strength_areas: List[str] = field(default_factory=list)
    challenge_areas: List[str] = field(default_factory=list)
    
    nonverbal_communication_rating: int = 5
    emotional_intelligence_rating: int = 5
    conflict_comfort_level: int = 3
    
    social_anxiety_factors: List[str] = field(default_factory=list)
    cultural_communication_patterns: List[str] = field(default_factory=list)
    
    relationship_impact_areas: List[str] = field(default_factory=list)
    professional_impact_areas: List[str] = field(default_factory=list)
    
    motivation_level: int = 7
    preferred_learning_style: str = "interactive"
    
    priority_skill_goals: List[CommunicationSkill] = field(default_factory=list)
    treatment_recommendations: List[str] = field(default_factory=list)
    
    created_date: datetime = field(default_factory=datetime.now)


@dataclass
class ConversationScript:
    script_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    
    skill_focus: CommunicationSkill = CommunicationSkill.ASSERTIVENESS
    conversation_type: ConversationType = ConversationType.PROFESSIONAL
    
    scenario_title: str = ""
    scenario_description: str = ""
    
    participant_roles: List[str] = field(default_factory=list)
    conversation_context: str = ""
    
    script_phases: List[Dict[str, str]] = field(default_factory=list)
    key_phrases: List[str] = field(default_factory=list)
    nonverbal_cues: List[str] = field(default_factory=list)
    
    difficulty_level: int = 3
    estimated_duration: int = 10
    
    learning_points: List[str] = field(default_factory=list)
    common_variations: List[str] = field(default_factory=list)
    
    practice_count: int = 0
    effectiveness_ratings: List[int] = field(default_factory=list)
    
    created_date: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None


@dataclass
class CommunicationChallenge:
    challenge_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    
    challenge_date: datetime = field(default_factory=datetime.now)
    situation_description: str = ""
    
    people_involved: List[str] = field(default_factory=list)
    relationship_context: str = ""
    conversation_type: ConversationType = ConversationType.CASUAL_SOCIAL
    
    communication_goals: List[str] = field(default_factory=list)
    approach_planned: str = ""
    skills_to_use: List[CommunicationSkill] = field(default_factory=list)
    
    anticipated_challenges: List[str] = field(default_factory=list)
    backup_strategies: List[str] = field(default_factory=list)
    
    outcome_description: str = ""
    success_rating: Optional[int] = None
    lessons_learned: List[str] = field(default_factory=list)
    
    skills_used_effectively: List[str] = field(default_factory=list)
    areas_for_improvement: List[str] = field(default_factory=list)
    
    follow_up_needed: bool = False
    next_steps: List[str] = field(default_factory=list)
    
    created_date: datetime = field(default_factory=datetime.now)
    completed: bool = False


class CommunicationTrainingSystem:
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self._initialize_database()
        self._populate_skill_modules()
    
    def _initialize_database(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS communication_skill_modules (
                    module_id TEXT PRIMARY KEY,
                    skill TEXT NOT NULL,
                    module_name TEXT NOT NULL,
                    learning_objectives TEXT,
                    key_concepts TEXT,
                    techniques TEXT,
                    practice_exercises TEXT,
                    role_play_scenarios TEXT,
                    homework_assignments TEXT,
                    common_mistakes TEXT,
                    troubleshooting_tips TEXT,
                    difficulty_level INTEGER,
                    estimated_sessions INTEGER,
                    prerequisite_skills TEXT,
                    assessment_criteria TEXT,
                    success_indicators TEXT,
                    created_date TEXT NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS communication_practice_sessions (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    skill_focus TEXT NOT NULL,
                    session_date TEXT NOT NULL,
                    duration_minutes INTEGER,
                    conversation_type TEXT,
                    practice_format TEXT,
                    scenario_description TEXT,
                    learning_goals TEXT,
                    pre_session_confidence INTEGER,
                    post_session_confidence INTEGER,
                    pre_session_anxiety INTEGER,
                    post_session_anxiety INTEGER,
                    techniques_practiced TEXT,
                    challenges_encountered TEXT,
                    breakthroughs_achieved TEXT,
                    nonverbal_skills_rating TEXT,
                    verbal_skills_rating TEXT,
                    therapist_observations TEXT,
                    patient_self_reflection TEXT,
                    homework_assigned TEXT,
                    next_session_goals TEXT,
                    overall_effectiveness INTEGER,
                    created_date TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS communication_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    assessment_date TEXT NOT NULL,
                    assessment_type TEXT,
                    dominant_communication_style TEXT,
                    style_flexibility INTEGER,
                    skill_ratings TEXT,
                    strength_areas TEXT,
                    challenge_areas TEXT,
                    nonverbal_communication_rating INTEGER,
                    emotional_intelligence_rating INTEGER,
                    conflict_comfort_level INTEGER,
                    social_anxiety_factors TEXT,
                    cultural_communication_patterns TEXT,
                    relationship_impact_areas TEXT,
                    professional_impact_areas TEXT,
                    motivation_level INTEGER,
                    preferred_learning_style TEXT,
                    priority_skill_goals TEXT,
                    treatment_recommendations TEXT,
                    created_date TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_scripts (
                    script_id TEXT PRIMARY KEY,
                    patient_id TEXT,
                    skill_focus TEXT NOT NULL,
                    conversation_type TEXT NOT NULL,
                    scenario_title TEXT,
                    scenario_description TEXT,
                    participant_roles TEXT,
                    conversation_context TEXT,
                    script_phases TEXT,
                    key_phrases TEXT,
                    nonverbal_cues TEXT,
                    difficulty_level INTEGER,
                    estimated_duration INTEGER,
                    learning_points TEXT,
                    common_variations TEXT,
                    practice_count INTEGER DEFAULT 0,
                    effectiveness_ratings TEXT,
                    created_date TEXT NOT NULL,
                    last_used TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS communication_challenges (
                    challenge_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    challenge_date TEXT NOT NULL,
                    situation_description TEXT,
                    people_involved TEXT,
                    relationship_context TEXT,
                    conversation_type TEXT,
                    communication_goals TEXT,
                    approach_planned TEXT,
                    skills_to_use TEXT,
                    anticipated_challenges TEXT,
                    backup_strategies TEXT,
                    outcome_description TEXT,
                    success_rating INTEGER,
                    lessons_learned TEXT,
                    skills_used_effectively TEXT,
                    areas_for_improvement TEXT,
                    follow_up_needed BOOLEAN,
                    next_steps TEXT,
                    created_date TEXT NOT NULL,
                    completed BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            conn.commit()
    
    def _populate_skill_modules(self):
        modules = self._get_default_skill_modules()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for module in modules:
                cursor.execute("""
                    INSERT OR IGNORE INTO communication_skill_modules (
                        module_id, skill, module_name, learning_objectives,
                        key_concepts, techniques, practice_exercises,
                        role_play_scenarios, homework_assignments, common_mistakes,
                        troubleshooting_tips, difficulty_level, estimated_sessions,
                        prerequisite_skills, assessment_criteria, success_indicators,
                        created_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    module.module_id, module.skill.value, module.module_name,
                    json.dumps(module.learning_objectives),
                    json.dumps(module.key_concepts),
                    json.dumps(module.techniques),
                    json.dumps(module.practice_exercises),
                    json.dumps(module.role_play_scenarios),
                    json.dumps(module.homework_assignments),
                    json.dumps(module.common_mistakes),
                    json.dumps(module.troubleshooting_tips),
                    module.difficulty_level, module.estimated_sessions,
                    json.dumps([s.value for s in module.prerequisite_skills]),
                    json.dumps(module.assessment_criteria),
                    json.dumps(module.success_indicators),
                    module.created_date.isoformat()
                ))
            
            conn.commit()
    
    def _get_default_skill_modules(self) -> List[CommunicationSkillModule]:
        return [
            CommunicationSkillModule(
                module_id="active_listening_fundamentals",
                skill=CommunicationSkill.ACTIVE_LISTENING,
                module_name="Active Listening Fundamentals",
                learning_objectives=[
                    "Understand the components of active listening",
                    "Practice reflective listening techniques",
                    "Develop empathetic responding skills",
                    "Learn to ask clarifying questions effectively"
                ],
                key_concepts=[
                    "Full attention and presence",
                    "Reflective listening",
                    "Empathetic responses",
                    "Nonverbal listening cues",
                    "Avoiding interruptions and judgment"
                ],
                techniques=[
                    "Paraphrasing and summarizing",
                    "Reflecting emotions",
                    "Asking open-ended questions",
                    "Using minimal encouragers",
                    "Maintaining appropriate eye contact"
                ],
                practice_exercises=[
                    "Listen to 5-minute audio clip and summarize key points",
                    "Practice paraphrasing partner's statements",
                    "Emotion reflection role-play",
                    "Active listening in group discussion"
                ],
                role_play_scenarios=[
                    "Friend sharing relationship problems",
                    "Coworker explaining project challenges",
                    "Family member expressing frustrations",
                    "Partner discussing future plans"
                ],
                homework_assignments=[
                    "Practice active listening with one person daily",
                    "Keep listening journal for one week",
                    "Identify personal listening barriers"
                ],
                common_mistakes=[
                    "Thinking about your response while others speak",
                    "Offering unsolicited advice",
                    "Making assumptions about meaning",
                    "Getting distracted by technology"
                ],
                difficulty_level=2,
                estimated_sessions=4
            ),
            
            CommunicationSkillModule(
                module_id="assertiveness_training",
                skill=CommunicationSkill.ASSERTIVENESS,
                module_name="Assertiveness Training",
                learning_objectives=[
                    "Distinguish between passive, aggressive, and assertive communication",
                    "Learn to express needs and wants clearly",
                    "Practice saying no effectively",
                    "Develop confidence in self-advocacy"
                ],
                key_concepts=[
                    "Assertive vs aggressive vs passive communication",
                    "Personal rights and responsibilities",
                    "I-statements and clear requests",
                    "Boundary setting in communication",
                    "Handling pushback and negotiation"
                ],
                techniques=[
                    "I-statement formula",
                    "Broken record technique",
                    "Fogging and negative assertion",
                    "Workable compromise",
                    "DESC script (Describe, Express, Specify, Consequences)"
                ],
                practice_exercises=[
                    "Convert passive statements to assertive ones",
                    "Practice saying no in various scenarios",
                    "Role-play requesting behavior changes",
                    "Assertive body language practice"
                ],
                role_play_scenarios=[
                    "Asking for a raise or promotion",
                    "Declining social invitations",
                    "Addressing inappropriate behavior",
                    "Negotiating household responsibilities",
                    "Setting boundaries with family members"
                ],
                homework_assignments=[
                    "Practice one assertive request daily",
                    "Identify situations where assertiveness is needed",
                    "Keep assertiveness practice log"
                ],
                common_mistakes=[
                    "Apologizing excessively when being assertive",
                    "Using aggressive tone with assertive words",
                    "Giving too many explanations or justifications",
                    "Backing down at first sign of resistance"
                ],
                difficulty_level=4,
                estimated_sessions=6,
                prerequisite_skills=[CommunicationSkill.ACTIVE_LISTENING]
            ),
            
            CommunicationSkillModule(
                module_id="empathy_development",
                skill=CommunicationSkill.EMPATHY,
                module_name="Developing Empathetic Communication",
                learning_objectives=[
                    "Understand emotional intelligence in communication",
                    "Practice perspective-taking skills",
                    "Learn to validate others' emotions",
                    "Develop compassionate responding"
                ],
                key_concepts=[
                    "Cognitive vs emotional empathy",
                    "Perspective-taking techniques",
                    "Emotional validation",
                    "Nonviolent communication principles",
                    "Cultural sensitivity in empathy"
                ],
                techniques=[
                    "Emotion labeling and reflection",
                    "Perspective-taking exercises",
                    "Validation statements",
                    "Nonviolent communication framework",
                    "Empathetic inquiry questions"
                ],
                practice_exercises=[
                    "Emotion identification in facial expressions",
                    "Practice validating different viewpoints",
                    "Empathetic response to conflict scenarios",
                    "Cross-cultural empathy practice"
                ],
                role_play_scenarios=[
                    "Comforting someone experiencing loss",
                    "Understanding different political viewpoints",
                    "Supporting friend making difficult decision",
                    "Responding to workplace frustrations"
                ],
                homework_assignments=[
                    "Practice daily empathetic responses",
                    "Observe and reflect on others' emotional states",
                    "Keep empathy practice journal"
                ],
                common_mistakes=[
                    "Trying to fix instead of understand",
                    "Making assumptions about others' feelings",
                    "Overwhelming others with emotional intensity",
                    "Taking on others' emotions as your own"
                ],
                difficulty_level=3,
                estimated_sessions=5,
                prerequisite_skills=[CommunicationSkill.ACTIVE_LISTENING]
            ),
            
            CommunicationSkillModule(
                module_id="conflict_resolution",
                skill=CommunicationSkill.CONFLICT_RESOLUTION,
                module_name="Conflict Resolution Skills",
                learning_objectives=[
                    "Learn to approach conflict constructively",
                    "Practice de-escalation techniques",
                    "Develop problem-solving communication",
                    "Build skills for difficult conversations"
                ],
                key_concepts=[
                    "Conflict as opportunity for growth",
                    "De-escalation strategies",
                    "Win-win problem solving",
                    "Managing emotional intensity",
                    "Finding common ground"
                ],
                techniques=[
                    "PEACE model for conflict resolution",
                    "De-escalation phrases and tone",
                    "Active problem-solving steps",
                    "Emotional regulation during conflict",
                    "Compromise and collaboration strategies"
                ],
                practice_exercises=[
                    "De-escalation phrase practice",
                    "Conflict scenario problem-solving",
                    "Emotional regulation techniques",
                    "Finding common ground exercises"
                ],
                role_play_scenarios=[
                    "Disagreement with romantic partner",
                    "Workplace conflict with colleague",
                    "Family dispute resolution",
                    "Neighbor boundary issues",
                    "Service complaint handling"
                ],
                homework_assignments=[
                    "Practice conflict resolution in low-stakes situations",
                    "Identify personal conflict triggers",
                    "Keep conflict resolution journal"
                ],
                common_mistakes=[
                    "Avoiding conflict entirely",
                    "Escalating instead of de-escalating",
                    "Focusing on being right vs. finding solutions",
                    "Bringing up past grievances"
                ],
                difficulty_level=5,
                estimated_sessions=7,
                prerequisite_skills=[CommunicationSkill.ASSERTIVENESS, CommunicationSkill.EMPATHY]
            ),
            
            CommunicationSkillModule(
                module_id="nonverbal_communication",
                skill=CommunicationSkill.NONVERBAL_COMMUNICATION,
                module_name="Mastering Nonverbal Communication",
                learning_objectives=[
                    "Understand impact of body language on communication",
                    "Practice congruent verbal and nonverbal messages",
                    "Learn to read others' nonverbal cues",
                    "Develop confident body language"
                ],
                key_concepts=[
                    "Components of nonverbal communication",
                    "Cultural differences in body language",
                    "Congruence between verbal and nonverbal",
                    "Reading social and emotional cues",
                    "Professional vs casual body language"
                ],
                techniques=[
                    "Confident posture and stance",
                    "Appropriate eye contact patterns",
                    "Facial expression awareness",
                    "Voice tone and pace modulation",
                    "Personal space management"
                ],
                practice_exercises=[
                    "Mirror practice for body language",
                    "Video analysis of nonverbal communication",
                    "Nonverbal cue identification exercises",
                    "Congruence practice between verbal and nonverbal"
                ],
                role_play_scenarios=[
                    "Job interview presentation",
                    "First date conversation",
                    "Professional networking event",
                    "Giving presentation to group",
                    "Difficult conversation with authority figure"
                ],
                homework_assignments=[
                    "Observe nonverbal communication in public spaces",
                    "Practice confident body language daily",
                    "Keep nonverbal awareness journal"
                ],
                common_mistakes=[
                    "Incongruent verbal and nonverbal messages",
                    "Too much or too little eye contact",
                    "Closed-off body posture",
                    "Ignoring others' nonverbal cues"
                ],
                difficulty_level=3,
                estimated_sessions=4
            ),
            
            CommunicationSkillModule(
                module_id="emotional_expression",
                skill=CommunicationSkill.EMOTIONAL_EXPRESSION,
                module_name="Healthy Emotional Expression",
                learning_objectives=[
                    "Learn to identify and name emotions accurately",
                    "Practice expressing emotions appropriately",
                    "Develop emotional vocabulary",
                    "Build skills for vulnerable communication"
                ],
                key_concepts=[
                    "Emotional awareness and literacy",
                    "Appropriate emotional expression",
                    "Vulnerability vs oversharing",
                    "Cultural norms for emotional expression",
                    "Timing and context for emotional sharing"
                ],
                techniques=[
                    "Emotion wheel and vocabulary building",
                    "I-feel statements",
                    "Graduated emotional disclosure",
                    "Emotional regulation before expression",
                    "Nonviolent expression of difficult emotions"
                ],
                practice_exercises=[
                    "Daily emotion identification and naming",
                    "Practice expressing emotions at different intensities",
                    "Vulnerable sharing in safe contexts",
                    "Emotional expression through multiple channels"
                ],
                role_play_scenarios=[
                    "Sharing disappointment with friend",
                    "Expressing appreciation to partner",
                    "Communicating frustration at work",
                    "Sharing fears about future",
                    "Expressing needs in relationship"
                ],
                homework_assignments=[
                    "Keep daily emotion journal",
                    "Practice expressing one emotion daily",
                    "Identify emotional expression patterns"
                ],
                common_mistakes=[
                    "Suppressing all emotions",
                    "Emotional dumping on others",
                    "Using emotions to manipulate",
                    "Expressing emotions at inappropriate times or places"
                ],
                difficulty_level=4,
                estimated_sessions=5,
                prerequisite_skills=[CommunicationSkill.EMPATHY]
            )
        ]
    
    def conduct_communication_assessment(self, patient_id: str) -> str:
        assessment = CommunicationAssessment(
            patient_id=patient_id,
            skill_ratings={
                skill.value: 5 for skill in CommunicationSkill
            }
        )
        
        self._save_communication_assessment(assessment)
        return assessment.assessment_id
    
    def _save_communication_assessment(self, assessment: CommunicationAssessment):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO communication_assessments (
                    assessment_id, patient_id, assessment_date, assessment_type,
                    dominant_communication_style, style_flexibility, skill_ratings,
                    strength_areas, challenge_areas, nonverbal_communication_rating,
                    emotional_intelligence_rating, conflict_comfort_level,
                    social_anxiety_factors, cultural_communication_patterns,
                    relationship_impact_areas, professional_impact_areas,
                    motivation_level, preferred_learning_style, priority_skill_goals,
                    treatment_recommendations, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id, assessment.patient_id,
                assessment.assessment_date.isoformat(), assessment.assessment_type,
                assessment.dominant_communication_style.value, assessment.style_flexibility,
                json.dumps(assessment.skill_ratings),
                json.dumps(assessment.strength_areas),
                json.dumps(assessment.challenge_areas),
                assessment.nonverbal_communication_rating,
                assessment.emotional_intelligence_rating,
                assessment.conflict_comfort_level,
                json.dumps(assessment.social_anxiety_factors),
                json.dumps(assessment.cultural_communication_patterns),
                json.dumps(assessment.relationship_impact_areas),
                json.dumps(assessment.professional_impact_areas),
                assessment.motivation_level, assessment.preferred_learning_style,
                json.dumps([g.value for g in assessment.priority_skill_goals]),
                json.dumps(assessment.treatment_recommendations),
                assessment.created_date.isoformat()
            ))
            
            conn.commit()
    
    def create_practice_session(
        self,
        patient_id: str,
        skill_focus: CommunicationSkill,
        conversation_type: ConversationType = ConversationType.CASUAL_SOCIAL,
        scenario_description: str = ""
    ) -> str:
        
        session = CommunicationPracticeSession(
            patient_id=patient_id,
            skill_focus=skill_focus,
            conversation_type=conversation_type,
            scenario_description=scenario_description
        )
        
        module = self._get_skill_module(skill_focus)
        if module:
            session.learning_goals = module.learning_objectives[:3]
            session.techniques_practiced = module.techniques[:3]
        
        self._save_practice_session(session)
        return session.session_id
    
    def _get_skill_module(self, skill: CommunicationSkill) -> Optional[CommunicationSkillModule]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM communication_skill_modules WHERE skill = ?
            """, (skill.value,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return CommunicationSkillModule(
                module_id=row[0],
                skill=CommunicationSkill(row[1]),
                module_name=row[2],
                learning_objectives=json.loads(row[3] or '[]'),
                key_concepts=json.loads(row[4] or '[]'),
                techniques=json.loads(row[5] or '[]'),
                practice_exercises=json.loads(row[6] or '[]'),
                role_play_scenarios=json.loads(row[7] or '[]'),
                homework_assignments=json.loads(row[8] or '[]'),
                common_mistakes=json.loads(row[9] or '[]'),
                troubleshooting_tips=json.loads(row[10] or '[]'),
                difficulty_level=row[11] or 1,
                estimated_sessions=row[12] or 3,
                prerequisite_skills=[CommunicationSkill(s) for s in json.loads(row[13] or '[]')],
                assessment_criteria=json.loads(row[14] or '[]'),
                success_indicators=json.loads(row[15] or '[]'),
                created_date=datetime.fromisoformat(row[16])
            )
    
    def _save_practice_session(self, session: CommunicationPracticeSession):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO communication_practice_sessions (
                    session_id, patient_id, skill_focus, session_date,
                    duration_minutes, conversation_type, practice_format,
                    scenario_description, learning_goals, pre_session_confidence,
                    post_session_confidence, pre_session_anxiety, post_session_anxiety,
                    techniques_practiced, challenges_encountered, breakthroughs_achieved,
                    nonverbal_skills_rating, verbal_skills_rating, therapist_observations,
                    patient_self_reflection, homework_assigned, next_session_goals,
                    overall_effectiveness, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id, session.patient_id, session.skill_focus.value,
                session.session_date.isoformat(), session.duration_minutes,
                session.conversation_type.value, session.practice_format.value,
                session.scenario_description, json.dumps(session.learning_goals),
                session.pre_session_confidence, session.post_session_confidence,
                session.pre_session_anxiety, session.post_session_anxiety,
                json.dumps(session.techniques_practiced),
                json.dumps(session.challenges_encountered),
                json.dumps(session.breakthroughs_achieved),
                json.dumps(session.nonverbal_skills_rating),
                json.dumps(session.verbal_skills_rating),
                session.therapist_observations, session.patient_self_reflection,
                json.dumps(session.homework_assigned),
                json.dumps(session.next_session_goals),
                session.overall_effectiveness, session.created_date.isoformat()
            ))
            
            conn.commit()
    
    def update_practice_session_results(
        self,
        session_id: str,
        post_confidence: int,
        post_anxiety: int,
        challenges: List[str] = None,
        breakthroughs: List[str] = None,
        nonverbal_ratings: Dict[str, int] = None,
        verbal_ratings: Dict[str, int] = None,
        effectiveness: int = 5,
        patient_reflection: str = "",
        therapist_observations: str = ""
    ) -> bool:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE communication_practice_sessions SET
                    post_session_confidence = ?,
                    post_session_anxiety = ?,
                    challenges_encountered = ?,
                    breakthroughs_achieved = ?,
                    nonverbal_skills_rating = ?,
                    verbal_skills_rating = ?,
                    overall_effectiveness = ?,
                    patient_self_reflection = ?,
                    therapist_observations = ?
                WHERE session_id = ?
            """, (
                post_confidence, post_anxiety,
                json.dumps(challenges or []),
                json.dumps(breakthroughs or []),
                json.dumps(nonverbal_ratings or {}),
                json.dumps(verbal_ratings or {}),
                effectiveness, patient_reflection, therapist_observations,
                session_id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def create_conversation_script(
        self,
        skill_focus: CommunicationSkill,
        conversation_type: ConversationType,
        scenario_title: str,
        patient_id: Optional[str] = None
    ) -> str:
        
        script = ConversationScript(
            patient_id=patient_id or "",
            skill_focus=skill_focus,
            conversation_type=conversation_type,
            scenario_title=scenario_title
        )
        
        template_data = self._get_script_template(skill_focus, conversation_type)
        script.scenario_description = template_data.get("description", "")
        script.participant_roles = template_data.get("roles", ["Person A", "Person B"])
        script.script_phases = template_data.get("phases", [])
        script.key_phrases = template_data.get("key_phrases", [])
        script.nonverbal_cues = template_data.get("nonverbal_cues", [])
        script.learning_points = template_data.get("learning_points", [])
        
        self._save_conversation_script(script)
        return script.script_id
    
    def _get_script_template(self, skill: CommunicationSkill, conv_type: ConversationType) -> Dict[str, Any]:
        templates = {
            (CommunicationSkill.ASSERTIVENESS, ConversationType.PROFESSIONAL): {
                "description": "Practice assertive communication in professional setting",
                "roles": ["Employee", "Supervisor"],
                "phases": [
                    {"phase": "opening", "employee": "Thank you for making time to meet with me.", "supervisor": "Of course, what did you want to discuss?"},
                    {"phase": "issue_presentation", "employee": "I'd like to discuss my current workload and some concerns I have.", "supervisor": "I'm listening, please go ahead."},
                    {"phase": "assertive_request", "employee": "I've been working 60+ hours weekly for the past month. I need to discuss redistributing some responsibilities.", "supervisor": "That does sound like a lot. What are you thinking?"},
                    {"phase": "negotiation", "employee": "I'd like to either hire temporary help or reassign the Johnson project to someone else.", "supervisor": "Let me consider the options and get back to you."},
                    {"phase": "closing", "employee": "I appreciate you listening. When can we follow up on this?", "supervisor": "Let's meet again Friday to discuss solutions."}
                ],
                "key_phrases": [
                    "I need to discuss...",
                    "I'd like to request...",
                    "This is important to me because...",
                    "I'm hoping we can find a solution that works for both of us"
                ],
                "nonverbal_cues": [
                    "Maintain steady eye contact",
                    "Sit up straight with open posture",
                    "Use calm, steady voice tone",
                    "Keep hands visible and relaxed"
                ],
                "learning_points": [
                    "State needs clearly without apologizing",
                    "Provide specific examples and data",
                    "Stay calm when faced with pushback",
                    "Be willing to negotiate and find compromise"
                ]
            },
            
            (CommunicationSkill.ACTIVE_LISTENING, ConversationType.INTIMATE_PERSONAL): {
                "description": "Practice active listening with close friend or partner",
                "roles": ["Listener", "Sharer"],
                "phases": [
                    {"phase": "opening", "sharer": "I've been having a really hard time lately and could use someone to talk to.", "listener": "I'm here for you. What's been going on?"},
                    {"phase": "sharing", "sharer": "Work has been incredibly stressful, and I feel like I'm failing at everything.", "listener": "That sounds really overwhelming. Tell me more about what's making work so stressful."},
                    {"phase": "reflection", "sharer": "My boss keeps adding projects, and I can't keep up. I feel like I'm disappointing everyone.", "listener": "So you're feeling overwhelmed with the workload and worried about letting people down. That must be exhausting."},
                    {"phase": "deeper_sharing", "sharer": "Exactly. And I don't know how to say no without seeming incompetent.", "listener": "It sounds like you're caught between wanting to do well and feeling like you can't manage everything. What would feel most helpful right now?"},
                    {"phase": "support", "sharer": "Just knowing someone understands helps. I think I need to have a conversation with my boss.", "listener": "I'm glad talking helped. You're not failing - you're dealing with a difficult situation. How can I support you?"}
                ],
                "key_phrases": [
                    "Tell me more about...",
                    "That sounds really...",
                    "It seems like you're feeling...",
                    "What I'm hearing is...",
                    "How can I support you?"
                ],
                "nonverbal_cues": [
                    "Face the person and lean in slightly",
                    "Maintain gentle, caring eye contact",
                    "Use nodding and minimal encouragers",
                    "Mirror emotions appropriately in facial expressions"
                ],
                "learning_points": [
                    "Focus completely on understanding, not on giving advice",
                    "Reflect both content and emotions",
                    "Ask questions to deepen understanding",
                    "Avoid judgment and immediate problem-solving"
                ]
            },
            
            (CommunicationSkill.CONFLICT_RESOLUTION, ConversationType.CONFLICT_DISCUSSION): {
                "description": "Practice resolving disagreement constructively",
                "roles": ["Person A", "Person B"],
                "phases": [
                    {"phase": "problem_acknowledgment", "person_a": "I think we need to talk about what happened yesterday. I felt upset about the way our conversation ended.", "person_b": "I noticed things got tense too. I'm willing to talk about it."},
                    {"phase": "perspective_sharing", "person_a": "When you said my idea wouldn't work, I felt dismissed and frustrated.", "person_b": "I can understand why you felt that way. I was stressed about the deadline and probably came across too harshly."},
                    {"phase": "understanding", "person_a": "I appreciate you acknowledging that. I know you were under pressure.", "person_b": "And I should have recognized that you were trying to help. Your ideas deserve consideration."},
                    {"phase": "solution_focus", "person_a": "How can we handle disagreements better in the future?", "person_b": "Maybe we could take a pause when things get heated and come back to it?"},
                    {"phase": "agreement", "person_a": "That sounds good. And I'll try to be more understanding when you're stressed.", "person_b": "And I'll work on expressing disagreement more respectfully."}
                ],
                "key_phrases": [
                    "I'd like to understand your perspective...",
                    "When [behavior], I felt [emotion]...",
                    "How can we handle this differently?",
                    "What would work better for both of us?",
                    "I appreciate you working on this with me"
                ],
                "nonverbal_cues": [
                    "Stay physically relaxed and open",
                    "Maintain calm, steady voice",
                    "Use appropriate eye contact without staring",
                    "Keep gestures open and non-threatening"
                ],
                "learning_points": [
                    "Focus on the issue, not attacking the person",
                    "Use I-statements to express feelings",
                    "Look for win-win solutions",
                    "Acknowledge the other person's perspective"
                ]
            }
        }
        
        return templates.get((skill, conv_type), {
            "description": f"Practice {skill.value} in {conv_type.value} setting",
            "roles": ["Person A", "Person B"],
            "phases": [{"phase": "practice", "person_a": "Practice the communication skill", "person_b": "Respond appropriately"}],
            "key_phrases": ["Practice clear communication"],
            "nonverbal_cues": ["Use appropriate body language"],
            "learning_points": ["Focus on skill development"]
        })
    
    def _save_conversation_script(self, script: ConversationScript):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO conversation_scripts (
                    script_id, patient_id, skill_focus, conversation_type,
                    scenario_title, scenario_description, participant_roles,
                    conversation_context, script_phases, key_phrases,
                    nonverbal_cues, difficulty_level, estimated_duration,
                    learning_points, common_variations, practice_count,
                    effectiveness_ratings, created_date, last_used
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                script.script_id, script.patient_id, script.skill_focus.value,
                script.conversation_type.value, script.scenario_title,
                script.scenario_description, json.dumps(script.participant_roles),
                script.conversation_context, json.dumps(script.script_phases),
                json.dumps(script.key_phrases), json.dumps(script.nonverbal_cues),
                script.difficulty_level, script.estimated_duration,
                json.dumps(script.learning_points), json.dumps(script.common_variations),
                script.practice_count, json.dumps(script.effectiveness_ratings),
                script.created_date.isoformat(),
                script.last_used.isoformat() if script.last_used else None
            ))
            
            conn.commit()
    
    def create_communication_challenge(
        self,
        patient_id: str,
        situation_description: str,
        conversation_type: ConversationType,
        communication_goals: List[str] = None
    ) -> str:
        
        challenge = CommunicationChallenge(
            patient_id=patient_id,
            situation_description=situation_description,
            conversation_type=conversation_type,
            communication_goals=communication_goals or []
        )
        
        self._save_communication_challenge(challenge)
        return challenge.challenge_id
    
    def _save_communication_challenge(self, challenge: CommunicationChallenge):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO communication_challenges (
                    challenge_id, patient_id, challenge_date, situation_description,
                    people_involved, relationship_context, conversation_type,
                    communication_goals, approach_planned, skills_to_use,
                    anticipated_challenges, backup_strategies, outcome_description,
                    success_rating, lessons_learned, skills_used_effectively,
                    areas_for_improvement, follow_up_needed, next_steps,
                    created_date, completed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                challenge.challenge_id, challenge.patient_id,
                challenge.challenge_date.isoformat(), challenge.situation_description,
                json.dumps(challenge.people_involved), challenge.relationship_context,
                challenge.conversation_type.value,
                json.dumps(challenge.communication_goals), challenge.approach_planned,
                json.dumps([s.value for s in challenge.skills_to_use]),
                json.dumps(challenge.anticipated_challenges),
                json.dumps(challenge.backup_strategies), challenge.outcome_description,
                challenge.success_rating, json.dumps(challenge.lessons_learned),
                json.dumps(challenge.skills_used_effectively),
                json.dumps(challenge.areas_for_improvement),
                challenge.follow_up_needed, json.dumps(challenge.next_steps),
                challenge.created_date.isoformat(), challenge.completed
            ))
            
            conn.commit()
    
    def update_communication_challenge_outcome(
        self,
        challenge_id: str,
        outcome_description: str,
        success_rating: int,
        lessons_learned: List[str] = None,
        skills_used_effectively: List[str] = None,
        areas_for_improvement: List[str] = None,
        follow_up_needed: bool = False,
        next_steps: List[str] = None
    ) -> bool:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE communication_challenges SET
                    outcome_description = ?,
                    success_rating = ?,
                    lessons_learned = ?,
                    skills_used_effectively = ?,
                    areas_for_improvement = ?,
                    follow_up_needed = ?,
                    next_steps = ?,
                    completed = TRUE
                WHERE challenge_id = ?
            """, (
                outcome_description, success_rating,
                json.dumps(lessons_learned or []),
                json.dumps(skills_used_effectively or []),
                json.dumps(areas_for_improvement or []),
                follow_up_needed, json.dumps(next_steps or []),
                challenge_id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def get_patient_practice_history(
        self,
        patient_id: str,
        days_back: int = 30,
        skill_filter: Optional[CommunicationSkill] = None
    ) -> List[CommunicationPracticeSession]:
        
        start_date = datetime.now() - timedelta(days=days_back)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM communication_practice_sessions 
                WHERE patient_id = ? AND session_date >= ?
            """
            params = [patient_id, start_date.isoformat()]
            
            if skill_filter:
                query += " AND skill_focus = ?"
                params.append(skill_filter.value)
            
            query += " ORDER BY session_date DESC"
            
            cursor.execute(query, params)
            
            sessions = []
            for row in cursor.fetchall():
                session = CommunicationPracticeSession(
                    session_id=row[0],
                    patient_id=row[1],
                    skill_focus=CommunicationSkill(row[2]),
                    session_date=datetime.fromisoformat(row[3]),
                    duration_minutes=row[4] or 45,
                    conversation_type=ConversationType(row[5]) if row[5] else ConversationType.CASUAL_SOCIAL,
                    practice_format=PracticeFormat(row[6]) if row[6] else PracticeFormat.ROLE_PLAY,
                    scenario_description=row[7] or "",
                    learning_goals=json.loads(row[8] or '[]'),
                    pre_session_confidence=row[9] or 1,
                    post_session_confidence=row[10] or 1,
                    pre_session_anxiety=row[11] or 10,
                    post_session_anxiety=row[12] or 10,
                    techniques_practiced=json.loads(row[13] or '[]'),
                    challenges_encountered=json.loads(row[14] or '[]'),
                    breakthroughs_achieved=json.loads(row[15] or '[]'),
                    nonverbal_skills_rating=json.loads(row[16] or '{}'),
                    verbal_skills_rating=json.loads(row[17] or '{}'),
                    therapist_observations=row[18] or "",
                    patient_self_reflection=row[19] or "",
                    homework_assigned=json.loads(row[20] or '[]'),
                    next_session_goals=json.loads(row[21] or '[]'),
                    overall_effectiveness=row[22] or 5,
                    created_date=datetime.fromisoformat(row[23])
                )
                sessions.append(session)
            
            return sessions
    
    def get_recommended_skills(self, patient_id: str) -> List[CommunicationSkill]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM communication_assessments 
                WHERE patient_id = ? 
                ORDER BY assessment_date DESC 
                LIMIT 1
            """, (patient_id,))
            
            assessment_row = cursor.fetchone()
            if not assessment_row:
                return [CommunicationSkill.ACTIVE_LISTENING, CommunicationSkill.ASSERTIVENESS]
            
            priority_skills = json.loads(assessment_row[18] or '[]')
            if priority_skills:
                return [CommunicationSkill(skill) for skill in priority_skills]
            
            challenge_areas = json.loads(assessment_row[8] or '[]')
            skill_mapping = {
                "listening": CommunicationSkill.ACTIVE_LISTENING,
                "assertiveness": CommunicationSkill.ASSERTIVENESS,
                "conflict": CommunicationSkill.CONFLICT_RESOLUTION,
                "empathy": CommunicationSkill.EMPATHY,
                "emotions": CommunicationSkill.EMOTIONAL_EXPRESSION,
                "nonverbal": CommunicationSkill.NONVERBAL_COMMUNICATION
            }
            
            recommended = []
            for area in challenge_areas:
                for key, skill in skill_mapping.items():
                    if key in area.lower():
                        recommended.append(skill)
                        break
            
            return recommended[:3] if recommended else [CommunicationSkill.ACTIVE_LISTENING]
    
    def generate_progress_report(self, patient_id: str, days_back: int = 90) -> Dict[str, Any]:
        sessions = self.get_patient_practice_history(patient_id, days_back)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM communication_challenges 
                WHERE patient_id = ? AND challenge_date >= ?
                ORDER BY challenge_date DESC
            """, (patient_id, (datetime.now() - timedelta(days=days_back)).isoformat()))
            
            challenges = cursor.fetchall()
        
        if not sessions:
            return {
                "patient_id": patient_id,
                "report_period_days": days_back,
                "total_sessions": 0,
                "message": "No communication practice sessions recorded"
            }
        
        skill_progress = {}
        for session in sessions:
            skill = session.skill_focus.value
            if skill not in skill_progress:
                skill_progress[skill] = {
                    "sessions": 0,
                    "avg_confidence_gain": 0,
                    "avg_anxiety_reduction": 0,
                    "avg_effectiveness": 0,
                    "confidence_gains": [],
                    "anxiety_reductions": [],
                    "effectiveness_scores": []
                }
            
            skill_progress[skill]["sessions"] += 1
            
            if session.post_session_confidence and session.pre_session_confidence:
                confidence_gain = session.post_session_confidence - session.pre_session_confidence
                skill_progress[skill]["confidence_gains"].append(confidence_gain)
            
            if session.pre_session_anxiety and session.post_session_anxiety:
                anxiety_reduction = session.pre_session_anxiety - session.post_session_anxiety
                skill_progress[skill]["anxiety_reductions"].append(anxiety_reduction)
            
            skill_progress[skill]["effectiveness_scores"].append(session.overall_effectiveness)
        
        for skill_data in skill_progress.values():
            if skill_data["confidence_gains"]:
                skill_data["avg_confidence_gain"] = sum(skill_data["confidence_gains"]) / len(skill_data["confidence_gains"])
            if skill_data["anxiety_reductions"]:
                skill_data["avg_anxiety_reduction"] = sum(skill_data["anxiety_reductions"]) / len(skill_data["anxiety_reductions"])
            if skill_data["effectiveness_scores"]:
                skill_data["avg_effectiveness"] = sum(skill_data["effectiveness_scores"]) / len(skill_data["effectiveness_scores"])
        
        completed_challenges = len([c for c in challenges if c[20]])  # completed field
        successful_challenges = len([c for c in challenges if c[20] and c[13] and c[13] >= 7])  # success_rating >= 7
        
        most_practiced_skills = sorted(skill_progress.items(), key=lambda x: x[1]["sessions"], reverse=True)[:3]
        highest_confidence_gains = sorted(skill_progress.items(), key=lambda x: x[1]["avg_confidence_gain"], reverse=True)[:3]
        
        recent_trends = self._analyze_recent_trends(sessions[-10:] if len(sessions) >= 10 else sessions)
        
        insights = self._generate_communication_insights(sessions, challenges, skill_progress)
        
        return {
            "patient_id": patient_id,
            "report_period_days": days_back,
            "session_summary": {
                "total_sessions": len(sessions),
                "skills_practiced": len(skill_progress),
                "avg_session_duration": sum(s.duration_minutes for s in sessions) / len(sessions),
                "most_practiced_skills": [{"skill": skill, "sessions": data["sessions"]} for skill, data in most_practiced_skills]
            },
            "skill_progress": {
                skill: {
                    "sessions": data["sessions"],
                    "avg_confidence_gain": round(data["avg_confidence_gain"], 2),
                    "avg_anxiety_reduction": round(data["avg_anxiety_reduction"], 2),
                    "avg_effectiveness": round(data["avg_effectiveness"], 2)
                }
                for skill, data in skill_progress.items()
            },
            "real_world_application": {
                "total_challenges": len(challenges),
                "completed_challenges": completed_challenges,
                "successful_challenges": successful_challenges,
                "success_rate": round(successful_challenges / completed_challenges, 2) if completed_challenges > 0 else 0
            },
            "confidence_development": [
                {"skill": skill, "avg_gain": round(data["avg_confidence_gain"], 2)}
                for skill, data in highest_confidence_gains
            ],
            "recent_trends": recent_trends,
            "insights": insights,
            "recommendations": self._generate_communication_recommendations(sessions, skill_progress),
            "generated_date": datetime.now().isoformat()
        }
    
    def _analyze_recent_trends(self, recent_sessions: List[CommunicationPracticeSession]) -> Dict[str, Any]:
        if len(recent_sessions) < 3:
            return {"trend": "insufficient_data", "message": "Need more sessions for trend analysis"}
        
        confidence_trend = []
        effectiveness_trend = []
        
        for session in recent_sessions:
            if session.post_session_confidence:
                confidence_trend.append(session.post_session_confidence)
            effectiveness_trend.append(session.overall_effectiveness)
        
        confidence_direction = "stable"
        if len(confidence_trend) >= 3:
            if confidence_trend[-1] > confidence_trend[0] + 1:
                confidence_direction = "improving"
            elif confidence_trend[-1] < confidence_trend[0] - 1:
                confidence_direction = "declining"
        
        effectiveness_direction = "stable"
        if len(effectiveness_trend) >= 3:
            if effectiveness_trend[-1] > effectiveness_trend[0] + 1:
                effectiveness_direction = "improving"
            elif effectiveness_trend[-1] < effectiveness_trend[0] - 1:
                effectiveness_direction = "declining"
        
        return {
            "confidence_trend": confidence_direction,
            "effectiveness_trend": effectiveness_direction,
            "recent_avg_confidence": round(sum(confidence_trend) / len(confidence_trend), 2) if confidence_trend else 0,
            "recent_avg_effectiveness": round(sum(effectiveness_trend) / len(effectiveness_trend), 2)
        }
    
    def _generate_communication_insights(
        self,
        sessions: List[CommunicationPracticeSession],
        challenges: List,
        skill_progress: Dict[str, Any]
    ) -> List[str]:
        
        insights = []
        
        if not sessions:
            insights.append("Begin regular communication practice to develop skills")
            return insights
        
        total_sessions = len(sessions)
        
        if total_sessions >= 10:
            insights.append(f"Consistent practice with {total_sessions} sessions shows strong commitment to skill development")
        
        high_effectiveness_skills = [
            skill for skill, data in skill_progress.items()
            if data["avg_effectiveness"] >= 7
        ]
        
        if high_effectiveness_skills:
            insights.append(f"Strong performance in {len(high_effectiveness_skills)} skill areas: {', '.join(high_effectiveness_skills)}")
        
        high_confidence_gains = [
            skill for skill, data in skill_progress.items()
            if data["avg_confidence_gain"] >= 2
        ]
        
        if high_confidence_gains:
            insights.append(f"Significant confidence improvement in: {', '.join(high_confidence_gains)}")
        
        low_confidence_areas = [
            skill for skill, data in skill_progress.items()
            if data["avg_confidence_gain"] < 1 and data["sessions"] >= 3
        ]
        
        if low_confidence_areas:
            insights.append(f"Areas needing additional focus: {', '.join(low_confidence_areas)}")
        
        completed_challenges = len([c for c in challenges if c[20]])
        if completed_challenges >= 5:
            insights.append("Strong real-world application - actively using skills outside of practice")
        
        avg_anxiety_reduction = 0
        anxiety_reductions = []
        for data in skill_progress.values():
            anxiety_reductions.extend(data["anxiety_reductions"])
        
        if anxiety_reductions:
            avg_anxiety_reduction = sum(anxiety_reductions) / len(anxiety_reductions)
            if avg_anxiety_reduction >= 2:
                insights.append("Communication practice significantly reducing social anxiety")
        
        return insights
    
    def _generate_communication_recommendations(
        self,
        sessions: List[CommunicationPracticeSession],
        skill_progress: Dict[str, Any]
    ) -> List[str]:
        
        recommendations = []
        
        if not sessions:
            recommendations.extend([
                "Start with communication assessment to identify priority skills",
                "Begin with active listening practice - foundation for all communication",
                "Practice in low-stakes situations before high-pressure conversations"
            ])
            return recommendations
        
        underused_skills = []
        for skill in CommunicationSkill:
            if skill.value not in skill_progress:
                underused_skills.append(skill.value)
        
        if underused_skills:
            recommendations.append(f"Explore new skill areas: {', '.join(underused_skills[:3])}")
        
        low_effectiveness_skills = [
            skill for skill, data in skill_progress.items()
            if data["avg_effectiveness"] < 5 and data["sessions"] >= 3
        ]
        
        if low_effectiveness_skills:
            recommendations.append(f"Focus on improving effectiveness in: {', '.join(low_effectiveness_skills)}")
        
        practice_frequency = len(sessions) / 12 if len(sessions) > 0 else 0  # sessions per week over 3 months
        if practice_frequency < 1:
            recommendations.append("Increase practice frequency to at least once per week")
        
        skills_with_high_anxiety = [
            skill for skill, data in skill_progress.items()
            if data["avg_anxiety_reduction"] < 1 and data["sessions"] >= 3
        ]
        
        if skills_with_high_anxiety:
            recommendations.append(f"Use anxiety management techniques when practicing: {', '.join(skills_with_high_anxiety)}")
        
        skills_needing_real_world_practice = [
            skill for skill, data in skill_progress.items()
            if data["sessions"] >= 4 and data["avg_effectiveness"] >= 6
        ]
        
        if skills_needing_real_world_practice:
            recommendations.append(f"Ready for real-world challenges in: {', '.join(skills_needing_real_world_practice[:2])}")
        
        return recommendations
    
    def get_personalized_practice_suggestions(self, patient_id: str) -> List[Dict[str, Any]]:
        recent_sessions = self.get_patient_practice_history(patient_id, days_back=30)
        recommended_skills = self.get_recommended_skills(patient_id)
        
        suggestions = []
        
        for skill in recommended_skills[:3]:
            module = self._get_skill_module(skill)
            if not module:
                continue
            
            recent_practice = [s for s in recent_sessions if s.skill_focus == skill]
            
            if not recent_practice:
                difficulty = 1
                focus = "introduction and basic concepts"
            elif len(recent_practice) < 3:
                difficulty = 2
                focus = "fundamental techniques and practice"
            else:
                avg_effectiveness = sum(s.overall_effectiveness for s in recent_practice) / len(recent_practice)
                if avg_effectiveness < 6:
                    difficulty = max(1, min(3, len(recent_practice)))
                    focus = "skill refinement and troubleshooting"
                else:
                    difficulty = min(5, len(recent_practice))
                    focus = "advanced application and real-world challenges"
            
            suggestion = {
                "skill": skill.value,
                "skill_name": module.module_name,
                "difficulty_level": difficulty,
                "focus_area": focus,
                "suggested_exercises": module.practice_exercises[:3],
                "role_play_scenarios": module.role_play_scenarios[:2],
                "next_steps": module.techniques[:3] if not recent_practice else module.homework_assignments[:2],
                "estimated_sessions_needed": max(1, module.estimated_sessions - len(recent_practice))
            }
            
            suggestions.append(suggestion)
        
        return suggestions
    
    def create_communication_homework(
        self,
        patient_id: str,
        skill_focus: CommunicationSkill,
        difficulty_level: int = 3
    ) -> Dict[str, Any]:
        
        module = self._get_skill_module(skill_focus)
        if not module:
            return {}
        
        base_homework = module.homework_assignments
        scenarios = module.role_play_scenarios
        
        homework_options = {
            1: {  # Beginner
                "daily_practice": f"Practice basic {skill_focus.value} techniques for 10 minutes daily",
                "observation_task": f"Observe others using {skill_focus.value} skills in daily interactions",
                "self_reflection": f"Keep a daily journal noting opportunities to use {skill_focus.value}",
                "low_risk_practice": f"Practice {skill_focus.value} in one low-stakes situation this week"
            },
            2: {  # Beginner-Intermediate
                "structured_practice": f"Complete 3 structured {skill_focus.value} exercises this week",
                "conversation_practice": f"Have one focused conversation using {skill_focus.value} techniques",
                "skill_logging": f"Log successes and challenges with {skill_focus.value} practice",
                "feedback_seeking": f"Ask trusted friend for feedback on your {skill_focus.value} skills"
            },
            3: {  # Intermediate
                "real_world_application": f"Apply {skill_focus.value} skills in 2-3 different contexts this week",
                "challenging_situation": f"Use {skill_focus.value} in one moderately challenging conversation",
                "skill_integration": f"Combine {skill_focus.value} with other communication skills",
                "progress_evaluation": f"Evaluate your {skill_focus.value} progress and identify next steps"
            },
            4: {  # Advanced
                "complex_scenarios": f"Practice {skill_focus.value} in complex or emotionally charged situations",
                "teaching_others": f"Explain or demonstrate {skill_focus.value} principles to someone else",
                "skill_refinement": f"Focus on nuanced aspects of {skill_focus.value}",
                "mentoring_practice": f"Help someone else develop their {skill_focus.value} skills"
            },
            5: {  # Expert
                "innovation_practice": f"Develop your own approaches to {skill_focus.value}",
                "difficult_relationships": f"Apply {skill_focus.value} skills to your most challenging relationships",
                "skill_mastery": f"Achieve consistent excellence in {skill_focus.value}",
                "leadership_application": f"Use {skill_focus.value} skills in leadership or mentoring roles"
            }
        }
        
        selected_homework = homework_options.get(difficulty_level, homework_options[3])
        
        return {
            "skill_focus": skill_focus.value,
            "difficulty_level": difficulty_level,
            "homework_assignments": selected_homework,
            "practice_scenarios": scenarios[:3] if scenarios else [],
            "success_criteria": module.success_indicators[:3] if module else [],
            "common_challenges": module.common_mistakes[:3] if module else [],
            "troubleshooting_tips": module.troubleshooting_tips[:3] if module else [],
            "estimated_time_commitment": f"{10 + (difficulty_level * 5)} minutes per day",
            "week_goals": [
                f"Practice {skill_focus.value} techniques daily",
                f"Apply skills in {difficulty_level} real situations",
                f"Reflect on progress and challenges"
            ]
        }
    
    def get_communication_tips_for_context(
        self,
        conversation_type: ConversationType,
        skill_focus: CommunicationSkill
    ) -> Dict[str, List[str]]:
        
        tips_database = {
            (ConversationType.JOB_INTERVIEW, CommunicationSkill.ASSERTIVENESS): {
                "preparation": [
                    "Research the company and role thoroughly",
                    "Prepare specific examples of your achievements",
                    "Practice discussing salary and benefits confidently",
                    "Prepare thoughtful questions about the role and company"
                ],
                "during_conversation": [
                    "Maintain confident posture and eye contact",
                    "Use specific examples when answering questions",
                    "Ask for clarification if questions are unclear",
                    "Express enthusiasm for the role and company"
                ],
                "key_phrases": [
                    "I have experience in... which resulted in...",
                    "I'm particularly interested in this role because...",
                    "Could you tell me more about...?",
                    "I would bring [specific skill/experience] to this position"
                ],
                "avoid": [
                    "Speaking negatively about previous employers",
                    "Appearing desperate or overly eager",
                    "Being vague about your accomplishments",
                    "Failing to ask questions about the role"
                ]
            },
            
            (ConversationType.CONFLICT_DISCUSSION, CommunicationSkill.EMPATHY): {
                "preparation": [
                    "Take time to calm down before the conversation",
                    "Consider the other person's perspective beforehand",
                    "Identify your main concerns and desired outcomes",
                    "Choose an appropriate time and private location"
                ],
                "during_conversation": [
                    "Listen to understand, not to defend",
                    "Acknowledge the other person's feelings",
                    "Use 'I' statements to express your experience",
                    "Look for common ground and shared values"
                ],
                "key_phrases": [
                    "I can see that you're feeling...",
                    "Help me understand your perspective on...",
                    "It sounds like what's important to you is...",
                    "I appreciate you sharing that with me"
                ],
                "avoid": [
                    "Dismissing or minimizing their concerns",
                    "Making assumptions about their intentions",
                    "Bringing up past grievances",
                    "Using accusatory language"
                ]
            },
            
            (ConversationType.PROFESSIONAL, CommunicationSkill.FEEDBACK_GIVING): {
                "preparation": [
                    "Focus on specific, observable behaviors",
                    "Prepare concrete examples and evidence",
                    "Consider timing and setting for the conversation",
                    "Think about desired outcomes and next steps"
                ],
                "during_conversation": [
                    "Start with positive observations",
                    "Be specific about behaviors and impacts",
                    "Ask for their perspective and input",
                    "Collaborate on solutions and next steps"
                ],
                "key_phrases": [
                    "I've noticed that when you..., the impact is...",
                    "What's your take on this situation?",
                    "How do you think we could approach this differently?",
                    "I'd like to see more of... because..."
                ],
                "avoid": [
                    "Making personal attacks or character judgments",
                    "Using vague or general criticism",
                    "Overwhelming with too much feedback at once",
                    "Failing to follow up on agreed actions"
                ]
            }
        }
        
        default_tips = {
            "preparation": ["Prepare mentally for the conversation", "Consider your goals"],
            "during_conversation": ["Stay calm and focused", "Listen actively"],
            "key_phrases": ["Use clear, respectful language"],
            "avoid": ["Don't interrupt", "Avoid inflammatory language"]
        }
        
        return tips_database.get((conversation_type, skill_focus), default_tips)
    
    def export_communication_data(self, patient_id: str) -> Dict[str, Any]:
        sessions = self.get_patient_practice_history(patient_id, days_back=365)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM communication_assessments 
                WHERE patient_id = ?
                ORDER BY assessment_date DESC
            """, (patient_id,))
            
            assessments = cursor.fetchall()
            
            cursor.execute("""
                SELECT * FROM communication_challenges 
                WHERE patient_id = ?
                ORDER BY challenge_date DESC
            """, (patient_id,))
            
            challenges = cursor.fetchall()
        
        export_data = {
            "patient_id": patient_id,
            "export_date": datetime.now().isoformat(),
            "practice_sessions": [
                {
                    "session_date": session.session_date.isoformat(),
                    "skill_focus": session.skill_focus.value,
                    "conversation_type": session.conversation_type.value,
                    "duration_minutes": session.duration_minutes,
                    "confidence_improvement": (session.post_session_confidence - session.pre_session_confidence) if session.post_session_confidence and session.pre_session_confidence else None,
                    "anxiety_reduction": (session.pre_session_anxiety - session.post_session_anxiety) if session.pre_session_anxiety and session.post_session_anxiety else None,
                    "overall_effectiveness": session.overall_effectiveness,
                    "techniques_practiced": session.techniques_practiced,
                    "breakthroughs": session.breakthroughs_achieved
                }
                for session in sessions
            ],
            "assessments_count": len(assessments),
            "latest_assessment": {
                "date": datetime.fromisoformat(assessments[0][2]).isoformat() if assessments else None,
                "dominant_style": assessments[0][4] if assessments else None,
                "strength_areas": json.loads(assessments[0][7]) if assessments else [],
                "challenge_areas": json.loads(assessments[0][8]) if assessments else [],
                "priority_goals": json.loads(assessments[0][18]) if assessments else []
            } if assessments else None,
            "real_world_challenges": [
                {
                    "date": datetime.fromisoformat(challenge[2]).isoformat(),
                    "situation": challenge[3],
                    "conversation_type": challenge[6],
                    "success_rating": challenge[13],
                    "completed": bool(challenge[20])
                }
                for challenge in challenges
            ],
            "summary_statistics": {
                "total_practice_sessions": len(sessions),
                "skills_practiced": len(set(session.skill_focus.value for session in sessions)),
                "avg_effectiveness": sum(session.overall_effectiveness for session in sessions) / len(sessions) if sessions else 0,
                "completed_challenges": len([c for c in challenges if c[20]]),
                "successful_challenges": len([c for c in challenges if c[20] and c[13] and c[13] >= 7])
            }
        }
        
        return export_data


def get_communication_style_description(style: CommunicationStyle) -> str:
    descriptions = {
        CommunicationStyle.PASSIVE: "Tends to avoid expressing needs, difficulty saying no, may suppress own feelings to avoid conflict",
        CommunicationStyle.AGGRESSIVE: "Direct but often harsh, may interrupt others, focuses on own needs at expense of others",
        CommunicationStyle.PASSIVE_AGGRESSIVE: "Indirect expression of negative feelings, may use sarcasm or silent treatment",
        CommunicationStyle.ASSERTIVE: "Direct and honest while respecting others, expresses needs clearly, good boundary setting",
        CommunicationStyle.MANIPULATIVE: "Uses indirect tactics to get needs met, may use guilt or emotional pressure"
    }
    return descriptions.get(style, "Communication style not recognized")


def create_communication_skill_tracker() -> Dict[str, Dict[str, Any]]:
    return {
        skill.value: {
            "current_level": 1,
            "target_level": 5,
            "practice_sessions": 0,
            "last_practiced": None,
            "confidence_rating": 1,
            "real_world_applications": 0,
            "areas_for_improvement": [],
            "recent_breakthroughs": [],
            "next_practice_goals": []
        }
        for skill in CommunicationSkill
    }


if __name__ == "__main__":
    comm_system = CommunicationTrainingSystem()
    
    patient_id = "test_patient_001"
    
    assessment_id = comm_system.conduct_communication_assessment(patient_id)
    
    session_id = comm_system.create_practice_session(
        patient_id=patient_id,
        skill_focus=CommunicationSkill.ASSERTIVENESS,
        conversation_type=ConversationType.PROFESSIONAL,
        scenario_description="Practicing asking for a raise"
    )
    
    comm_system.update_practice_session_results(
        session_id=session_id,
        post_confidence=7,
        post_anxiety=4,
        challenges=["Felt nervous initially", "Struggled with maintaining eye contact"],
        breakthroughs=["Successfully stated salary request clearly", "Remained calm when supervisor asked questions"],
        effectiveness=8,
        patient_reflection="Felt much more confident by the end. The practice really helped.",
        therapist_observations="Good progress on assertive language. Continue working on nonverbal confidence."
    )
    
    script_id = comm_system.create_conversation_script(
        skill_focus=CommunicationSkill.ACTIVE_LISTENING,
        conversation_type=ConversationType.INTIMATE_PERSONAL,
        scenario_title="Supporting a friend through difficult time"
    )
    
    challenge_id = comm_system.create_communication_challenge(
        patient_id=patient_id,
        situation_description="Need to have difficult conversation with roommate about cleanliness",
        conversation_type=ConversationType.CONFLICT_DISCUSSION,
        communication_goals=["Express concerns clearly", "Find mutually acceptable solution", "Maintain relationship"]
    )
    
    comm_system.update_communication_challenge_outcome(
        challenge_id=challenge_id,
        outcome_description="Had the conversation and reached agreement on cleaning schedule",
        success_rating=8,
        lessons_learned=["Starting with empathy helped", "Being specific about issues was important"],
        skills_used_effectively=["Active listening", "I-statements", "Collaborative problem-solving"],
        areas_for_improvement=["Could have been more confident initially"],
        next_steps=["Follow up in two weeks", "Continue practicing assertive communication"]
    )
    
    homework = comm_system.create_communication_homework(
        patient_id=patient_id,
        skill_focus=CommunicationSkill.EMPATHY,
        difficulty_level=3
    )
    
    progress_report = comm_system.generate_progress_report(patient_id, 90)
    
    suggestions = comm_system.get_personalized_practice_suggestions(patient_id)
    
    tips = comm_system.get_communication_tips_for_context(
        ConversationType.JOB_INTERVIEW,
        CommunicationSkill.ASSERTIVENESS
    )
    
    print(f"Communication assessment completed: {assessment_id}")
    print(f"Practice session created: {session_id}")
    print(f"Conversation script generated: {script_id}")
    print(f"Real-world challenge tracked: {challenge_id}")
    print(f"Progress report shows {progress_report['session_summary']['total_sessions']} total sessions")
    print(f"Generated {len(suggestions)} personalized practice suggestions")
    print(f"Context-specific tips provided for job interview assertiveness")
    print(f"Homework assignment created with {len(homework['homework_assignments'])} tasks")
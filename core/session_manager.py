"""
Session Manager Module
Comprehensive therapy session management for AI therapy system
Handles session scheduling, structure, flow, and documentation
"""

import sqlite3
import json
import uuid
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, date, timedelta
from enum import Enum
import logging
from pathlib import Path


class SessionType(Enum):
    """Types of therapy sessions"""
    INTAKE = "intake"
    THERAPY = "therapy"
    ASSESSMENT = "assessment"
    CRISIS = "crisis"
    CONSULTATION = "consultation"
    FOLLOW_UP = "follow_up"
    TERMINATION = "termination"


class SessionStatus(Enum):
    """Session status options"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"


class SessionPhase(Enum):
    """Phases within a therapy session"""
    OPENING = "opening"
    CHECK_IN = "check_in"
    HOMEWORK_REVIEW = "homework_review"
    AGENDA_SETTING = "agenda_setting"
    MAIN_WORK = "main_work"
    SKILL_PRACTICE = "skill_practice"
    HOMEWORK_ASSIGNMENT = "homework_assignment"
    SUMMARY = "summary"
    CLOSING = "closing"


class InterventionType(Enum):
    """Types of therapeutic interventions"""
    PSYCHOEDUCATION = "psychoeducation"
    COGNITIVE_RESTRUCTURING = "cognitive_restructuring"
    BEHAVIORAL_ACTIVATION = "behavioral_activation"
    EXPOSURE_THERAPY = "exposure_therapy"
    MINDFULNESS = "mindfulness"
    SKILLS_TRAINING = "skills_training"
    EMOTIONAL_REGULATION = "emotional_regulation"
    INTERPERSONAL_SKILLS = "interpersonal_skills"
    TRAUMA_PROCESSING = "trauma_processing"
    CRISIS_INTERVENTION = "crisis_intervention"


@dataclass
class SessionGoal:
    """Individual session goal"""
    goal_id: str
    description: str
    priority: int  # 1-5, 1 being highest
    target_phase: SessionPhase
    success_criteria: List[str]
    achieved: bool = False
    notes: str = ""


@dataclass
class HomeworkAssignment:
    """Homework assignment for patient"""
    assignment_id: str
    title: str
    description: str
    instructions: List[str]
    due_date: Optional[date] = None
    estimated_time_minutes: int = 30
    difficulty_level: str = "moderate"
    therapeutic_rationale: str = ""


@dataclass
class SessionNote:
    """Clinical session note"""
    note_id: str
    note_type: str  # progress, observation, intervention, risk
    content: str
    timestamp: datetime
    phase: Optional[SessionPhase] = None
    risk_indicators: List[str] = field(default_factory=list)
    follow_up_needed: bool = False


@dataclass
class SessionMetrics:
    """Session performance metrics"""
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    patient_engagement_score: Optional[int] = None  # 1-10
    mood_pre_session: Optional[int] = None  # 1-10
    mood_post_session: Optional[int] = None  # 1-10
    anxiety_pre_session: Optional[int] = None  # 1-10
    anxiety_post_session: Optional[int] = None  # 1-10
    homework_completion_rate: Optional[float] = None  # 0-1
    goals_achieved: int = 0
    total_goals: int = 0


@dataclass
class TherapySession:
    """Complete therapy session object"""
    session_id: str
    patient_id: str
    session_type: SessionType
    session_number: int
    scheduled_date: datetime
    therapy_modality: str
    treatment_phase: str
    status: SessionStatus = SessionStatus.SCHEDULED
    current_phase: Optional[SessionPhase] = None
    completed_phases: List[SessionPhase] = field(default_factory=list)
    session_goals: List[SessionGoal] = field(default_factory=list)
    interventions_used: List[InterventionType] = field(default_factory=list)
    session_notes: List[SessionNote] = field(default_factory=list)
    homework_assignments: List[HomeworkAssignment] = field(default_factory=list)
    session_metrics: Optional[SessionMetrics] = None
    risk_assessment: Dict[str, Any] = field(default_factory=dict)
    next_session_recommendations: List[str] = field(default_factory=list)
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


class SessionManager:
    """Comprehensive session management system"""
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._ensure_database_exists()
        self._create_tables()
        
        # Initialize templates and resources
        self.session_templates = self._initialize_session_templates()
        self.homework_templates = self._initialize_homework_templates()
    
    def _ensure_database_exists(self):
        """Ensure database directory and file exist"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def _create_tables(self):
        """Create database tables for session management"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Main sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS therapy_sessions (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    session_type TEXT NOT NULL,
                    session_number INTEGER NOT NULL,
                    scheduled_date TEXT NOT NULL,
                    therapy_modality TEXT NOT NULL,
                    treatment_phase TEXT NOT NULL,
                    status TEXT NOT NULL,
                    current_phase TEXT,
                    completed_phases TEXT,
                    interventions_used TEXT,
                    risk_assessment TEXT,
                    next_session_recommendations TEXT,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patient_profiles (patient_id)
                )
            """)
            
            # Session goals table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_goals (
                    goal_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    description TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    target_phase TEXT NOT NULL,
                    success_criteria TEXT,
                    achieved BOOLEAN DEFAULT 0,
                    notes TEXT,
                    FOREIGN KEY (session_id) REFERENCES therapy_sessions (session_id)
                )
            """)
            
            # Session notes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_notes (
                    note_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    note_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    phase TEXT,
                    risk_indicators TEXT,
                    follow_up_needed BOOLEAN DEFAULT 0,
                    FOREIGN KEY (session_id) REFERENCES therapy_sessions (session_id)
                )
            """)
            
            # Homework assignments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS homework_assignments (
                    assignment_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    instructions TEXT,
                    due_date TEXT,
                    estimated_time_minutes INTEGER,
                    difficulty_level TEXT,
                    therapeutic_rationale TEXT,
                    completed BOOLEAN DEFAULT 0,
                    completion_date TEXT,
                    completion_notes TEXT,
                    FOREIGN KEY (session_id) REFERENCES therapy_sessions (session_id)
                )
            """)
            
            # Session metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_metrics (
                    session_id TEXT PRIMARY KEY,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    duration_minutes INTEGER,
                    patient_engagement_score INTEGER,
                    mood_pre_session INTEGER,
                    mood_post_session INTEGER,
                    anxiety_pre_session INTEGER,
                    anxiety_post_session INTEGER,
                    homework_completion_rate REAL,
                    goals_achieved INTEGER DEFAULT 0,
                    total_goals INTEGER DEFAULT 0,
                    FOREIGN KEY (session_id) REFERENCES therapy_sessions (session_id)
                )
            """)
            
            conn.commit()
    
    def _initialize_session_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize session structure templates"""
        
        return {
            "CBT_STANDARD": {
                "name": "CBT Standard Session",
                "phases": [
                    {
                        "phase": SessionPhase.OPENING,
                        "duration_minutes": 5,
                        "objectives": ["Establish rapport", "Brief mood check"],
                        "interventions": [InterventionType.PSYCHOEDUCATION],
                        "prompts": [
                            "How are you feeling today?",
                            "What has been on your mind since our last session?"
                        ]
                    },
                    {
                        "phase": SessionPhase.CHECK_IN,
                        "duration_minutes": 10,
                        "objectives": ["Assess current mood", "Review week's events", "Safety check"],
                        "interventions": [InterventionType.PSYCHOEDUCATION],
                        "prompts": [
                            "Tell me about your week",
                            "How has your mood been?",
                            "Any significant events or stressors?"
                        ]
                    },
                    {
                        "phase": SessionPhase.HOMEWORK_REVIEW,
                        "duration_minutes": 10,
                        "objectives": ["Review homework completion", "Process learning"],
                        "interventions": [InterventionType.COGNITIVE_RESTRUCTURING],
                        "prompts": [
                            "How did the homework go this week?",
                            "What did you learn from the exercises?",
                            "What challenges did you encounter?"
                        ]
                    },
                    {
                        "phase": SessionPhase.AGENDA_SETTING,
                        "duration_minutes": 5,
                        "objectives": ["Collaborate on session agenda", "Prioritize topics"],
                        "interventions": [InterventionType.PSYCHOEDUCATION],
                        "prompts": [
                            "What would you like to focus on today?",
                            "What feels most important to address?"
                        ]
                    },
                    {
                        "phase": SessionPhase.MAIN_WORK,
                        "duration_minutes": 20,
                        "objectives": ["Address session agenda", "Practice core skills"],
                        "interventions": [InterventionType.COGNITIVE_RESTRUCTURING, InterventionType.BEHAVIORAL_ACTIVATION],
                        "prompts": [
                            "Let's explore that thought/feeling more deeply",
                            "What evidence supports or contradicts that belief?",
                            "What would be a more balanced way to think about this?"
                        ]
                    },
                    {
                        "phase": SessionPhase.HOMEWORK_ASSIGNMENT,
                        "duration_minutes": 5,
                        "objectives": ["Assign relevant homework", "Ensure understanding"],
                        "interventions": [InterventionType.BEHAVIORAL_ACTIVATION],
                        "prompts": [
                            "Based on today's work, what practice would be most helpful?",
                            "When will you have time to work on this?"
                        ]
                    },
                    {
                        "phase": SessionPhase.SUMMARY,
                        "duration_minutes": 5,
                        "objectives": ["Summarize key points", "Get feedback"],
                        "interventions": [InterventionType.PSYCHOEDUCATION],
                        "prompts": [
                            "What are the main takeaways from today?",
                            "What felt most helpful?"
                        ]
                    }
                ]
            },
            
            "DBT_SKILLS": {
                "name": "DBT Skills Session",
                "phases": [
                    {
                        "phase": SessionPhase.CHECK_IN,
                        "duration_minutes": 10,
                        "objectives": ["Review diary card", "Assess distress level"],
                        "interventions": [InterventionType.EMOTIONAL_REGULATION],
                        "prompts": [
                            "How has your distress level been this week?",
                            "How did you use your skills?"
                        ]
                    },
                    {
                        "phase": SessionPhase.HOMEWORK_REVIEW,
                        "duration_minutes": 15,
                        "objectives": ["Review skills practice", "Troubleshoot problems"],
                        "interventions": [InterventionType.SKILLS_TRAINING],
                        "prompts": [
                            "Which skills did you practice this week?",
                            "What situations did you use them in?"
                        ]
                    },
                    {
                        "phase": SessionPhase.MAIN_WORK,
                        "duration_minutes": 20,
                        "objectives": ["Teach new skill", "Practice skill"],
                        "interventions": [InterventionType.MINDFULNESS, InterventionType.EMOTIONAL_REGULATION],
                        "prompts": [
                            "Today we're learning about [specific skill]",
                            "Let's practice this together"
                        ]
                    },
                    {
                        "phase": SessionPhase.HOMEWORK_ASSIGNMENT,
                        "duration_minutes": 5,
                        "objectives": ["Assign skills practice", "Plan implementation"],
                        "interventions": [InterventionType.SKILLS_TRAINING],
                        "prompts": [
                            "This week, practice [specific skill] daily",
                            "What specific situations will you practice in?"
                        ]
                    }
                ]
            },
            
            "CRISIS_INTERVENTION": {
                "name": "Crisis Intervention Session",
                "phases": [
                    {
                        "phase": SessionPhase.OPENING,
                        "duration_minutes": 5,
                        "objectives": ["Assess immediate safety", "Establish calm presence"],
                        "interventions": [InterventionType.CRISIS_INTERVENTION],
                        "prompts": [
                            "I'm here to help you through this",
                            "You're safe right now"
                        ]
                    },
                    {
                        "phase": SessionPhase.CHECK_IN,
                        "duration_minutes": 15,
                        "objectives": ["Assess crisis severity", "Evaluate immediate risk"],
                        "interventions": [InterventionType.CRISIS_INTERVENTION],
                        "prompts": [
                            "Tell me what's happening right now",
                            "Are you having thoughts of hurting yourself?"
                        ]
                    },
                    {
                        "phase": SessionPhase.MAIN_WORK,
                        "duration_minutes": 25,
                        "objectives": ["Stabilize emotions", "Develop safety plan"],
                        "interventions": [InterventionType.CRISIS_INTERVENTION, InterventionType.EMOTIONAL_REGULATION],
                        "prompts": [
                            "Let's focus on getting you through the next few hours",
                            "What has helped you cope before?"
                        ]
                    },
                    {
                        "phase": SessionPhase.CLOSING,
                        "duration_minutes": 5,
                        "objectives": ["Finalize safety plan", "Schedule follow-up"],
                        "interventions": [InterventionType.CRISIS_INTERVENTION],
                        "prompts": [
                            "Let's review your safety plan",
                            "When will we talk again?"
                        ]
                    }
                ]
            }
        }
    
    def _initialize_homework_templates(self) -> Dict[str, HomeworkAssignment]:
        """Initialize homework assignment templates"""
        
        templates = {}
        
        templates["thought_record"] = HomeworkAssignment(
            assignment_id="HW_THOUGHT_RECORD",
            title="Daily Thought Record",
            description="Track negative thoughts and practice challenging them",
            instructions=[
                "Complete one thought record entry daily",
                "Focus on situations that triggered strong emotions",
                "Rate your belief in the thought before and after challenging it"
            ],
            estimated_time_minutes=15,
            difficulty_level="moderate",
            therapeutic_rationale="Builds awareness of thought patterns and develops cognitive flexibility"
        )
        
        templates["activity_scheduling"] = HomeworkAssignment(
            assignment_id="HW_ACTIVITY_SCHEDULE",
            title="Activity Scheduling",
            description="Plan and engage in pleasant and meaningful activities",
            instructions=[
                "Schedule one pleasant activity each day",
                "Rate your mood before and after each activity",
                "Include a mix of achievement and pleasure activities"
            ],
            estimated_time_minutes=30,
            difficulty_level="easy",
            therapeutic_rationale="Increases positive reinforcement and behavioral activation"
        )
        
        templates["mindfulness_practice"] = HomeworkAssignment(
            assignment_id="HW_MINDFULNESS",
            title="Daily Mindfulness Practice",
            description="Practice mindfulness meditation and exercises",
            instructions=[
                "Practice mindfulness meditation for 10 minutes daily",
                "Use the guided audio provided",
                "Record your experience in the practice log"
            ],
            estimated_time_minutes=15,
            difficulty_level="moderate",
            therapeutic_rationale="Develops present-moment awareness and emotional regulation"
        )
        
        return templates
    
    def create_session(self, patient_id: str, session_type: SessionType, 
                      session_number: int, scheduled_date: datetime,
                      therapy_modality: str, treatment_phase: str) -> TherapySession:
        """Create new therapy session"""
        
        session_id = f"{patient_id}_SESSION_{session_number:03d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate session goals
        session_goals = self._generate_session_goals(therapy_modality, treatment_phase, session_number)
        
        session = TherapySession(
            session_id=session_id,
            patient_id=patient_id,
            session_type=session_type,
            session_number=session_number,
            scheduled_date=scheduled_date,
            therapy_modality=therapy_modality,
            treatment_phase=treatment_phase,
            session_goals=session_goals
        )
        
        # Save to database
        self._save_session_to_db(session)
        
        self.logger.info(f"Created session: {session_id}")
        return session
    
    def _generate_session_goals(self, therapy_modality: str, treatment_phase: str, session_number: int) -> List[SessionGoal]:
        """Generate session goals based on context"""
        
        goals = []
        
        # Phase-specific goals
        if treatment_phase == "assessment":
            goals.append(SessionGoal(
                goal_id=f"GOAL_ASSESS_{uuid.uuid4().hex[:8]}",
                description="Complete comprehensive assessment",
                priority=1,
                target_phase=SessionPhase.MAIN_WORK,
                success_criteria=["Gather clinical information", "Assess risk factors", "Identify treatment targets"]
            ))
        elif treatment_phase == "stabilization":
            goals.append(SessionGoal(
                goal_id=f"GOAL_STAB_{uuid.uuid4().hex[:8]}",
                description="Establish safety and stability",
                priority=1,
                target_phase=SessionPhase.MAIN_WORK,
                success_criteria=["Address safety concerns", "Develop coping strategies", "Build rapport"]
            ))
        elif treatment_phase == "working":
            goals.append(SessionGoal(
                goal_id=f"GOAL_WORK_{uuid.uuid4().hex[:8]}",
                description="Practice core therapeutic skills",
                priority=1,
                target_phase=SessionPhase.MAIN_WORK,
                success_criteria=["Apply therapeutic techniques", "Process difficulties", "Develop insights"]
            ))
        
        # Session number specific goals
        if session_number == 1:
            goals.append(SessionGoal(
                goal_id=f"GOAL_INTRO_{uuid.uuid4().hex[:8]}",
                description="Establish therapeutic relationship",
                priority=2,
                target_phase=SessionPhase.OPENING,
                success_criteria=["Build rapport", "Explain therapy process", "Set expectations"]
            ))
        
        return goals
    
    def start_session(self, session_id: str) -> bool:
        """Start therapy session"""
        
        try:
            session = self.get_session(session_id)
            if not session:
                return False
            
            session.status = SessionStatus.IN_PROGRESS
            session.current_phase = SessionPhase.OPENING
            
            # Initialize session metrics
            session.session_metrics = SessionMetrics(start_time=datetime.now())
            
            # Add session start note
            start_note = SessionNote(
                note_id=f"NOTE_{session_id}_START_{datetime.now().strftime('%H%M%S')}",
                note_type="session_start",
                content="Session started",
                timestamp=datetime.now()
            )
            session.session_notes.append(start_note)
            
            self._update_session_in_db(session)
            
            self.logger.info(f"Started session: {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start session: {e}")
            return False
    
    def advance_session_phase(self, session_id: str, next_phase: SessionPhase, phase_notes: str = "") -> bool:
        """Advance session to next phase"""
        
        try:
            session = self.get_session(session_id)
            if not session:
                return False
            
            # Mark current phase as completed
            if session.current_phase:
                session.completed_phases.append(session.current_phase)
                
                # Add phase completion note
                phase_note = SessionNote(
                    note_id=f"NOTE_{session_id}_{session.current_phase.value}_{datetime.now().strftime('%H%M%S')}",
                    note_type="phase_completion",
                    content=f"Completed {session.current_phase.value} phase. {phase_notes}",
                    timestamp=datetime.now(),
                    phase=session.current_phase
                )
                session.session_notes.append(phase_note)
            
            # Advance to next phase
            session.current_phase = next_phase
            session.last_updated = datetime.now()
            
            self._update_session_in_db(session)
            
            self.logger.info(f"Advanced session {session_id} to phase: {next_phase.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to advance session phase: {e}")
            return False
    
    def add_intervention(self, session_id: str, intervention_type: InterventionType,
                        notes: str = "", phase: Optional[SessionPhase] = None) -> bool:
        """Add intervention to session"""
        
        try:
            session = self.get_session(session_id)
            if not session:
                return False
            
            # Add intervention to session
            if intervention_type not in session.interventions_used:
                session.interventions_used.append(intervention_type)
            
            # Add intervention note
            intervention_note = SessionNote(
                note_id=f"NOTE_{session_id}_INT_{datetime.now().strftime('%H%M%S')}",
                note_type="intervention",
                content=f"Applied {intervention_type.value}: {notes}",
                timestamp=datetime.now(),
                phase=phase or session.current_phase
            )
            session.session_notes.append(intervention_note)
            
            session.last_updated = datetime.now()
            self._update_session_in_db(session)
            
            self.logger.info(f"Added intervention {intervention_type.value} to session {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add intervention: {e}")
            return False
    
    def add_session_note(self, session_id: str, note_type: str, content: str,
                        risk_indicators: Optional[List[str]] = None,
                        follow_up_needed: bool = False) -> bool:
        """Add clinical note to session"""
        
        try:
            session = self.get_session(session_id)
            if not session:
                return False
            
            note = SessionNote(
                note_id=f"NOTE_{session_id}_{note_type}_{datetime.now().strftime('%H%M%S')}",
                note_type=note_type,
                content=content,
                timestamp=datetime.now(),
                phase=session.current_phase,
                risk_indicators=risk_indicators or [],
                follow_up_needed=follow_up_needed
            )
            
            session.session_notes.append(note)
            
            # Update risk assessment if risk indicators present
            if risk_indicators:
                session.risk_assessment.update({
                    "indicators_present": risk_indicators,
                    "last_assessment": datetime.now().isoformat(),
                    "follow_up_required": follow_up_needed
                })
            
            session.last_updated = datetime.now()
            self._update_session_in_db(session)
            
            self.logger.info(f"Added session note: {note_type} to session {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add session note: {e}")
            return False
    
    def assign_homework(self, session_id: str, homework_template_id: str,
                       custom_instructions: Optional[List[str]] = None,
                       due_date: Optional[date] = None) -> bool:
        """Assign homework to patient"""
        
        try:
            session = self.get_session(session_id)
            if not session:
                return False
            
            # Get homework template
            template = self.homework_templates.get(homework_template_id)
            if not template:
                return False
            
            # Create homework assignment
            assignment = HomeworkAssignment(
                assignment_id=f"HW_{session_id}_{homework_template_id}_{datetime.now().strftime('%H%M%S')}",
                title=template.title,
                description=template.description,
                instructions=custom_instructions or template.instructions,
                due_date=due_date or (date.today() + timedelta(days=7)),
                estimated_time_minutes=template.estimated_time_minutes,
                difficulty_level=template.difficulty_level,
                therapeutic_rationale=template.therapeutic_rationale
            )
            
            session.homework_assignments.append(assignment)
            
            # Add homework assignment note
            hw_note = SessionNote(
                note_id=f"NOTE_{session_id}_HW_{datetime.now().strftime('%H%M%S')}",
                note_type="homework_assigned",
                content=f"Assigned homework: {assignment.title}. Due: {assignment.due_date}",
                timestamp=datetime.now(),
                phase=session.current_phase
            )
            session.session_notes.append(hw_note)
            
            session.last_updated = datetime.now()
            self._update_session_in_db(session)
            
            self.logger.info(f"Assigned homework {assignment.title} in session {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to assign homework: {e}")
            return False
    
    def update_session_metrics(self, session_id: str, metrics: Dict[str, Any]) -> bool:
        """Update session performance metrics"""
        
        try:
            session = self.get_session(session_id)
            if not session or not session.session_metrics:
                return False
            
            # Update metrics
            for key, value in metrics.items():
                if hasattr(session.session_metrics, key):
                    setattr(session.session_metrics, key, value)
            
            session.last_updated = datetime.now()
            self._update_session_in_db(session)
            
            self.logger.info(f"Updated session metrics for {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update session metrics: {e}")
            return False
    
    def complete_session(self, session_id: str, session_summary: str = "",
                        next_session_recommendations: Optional[List[str]] = None) -> bool:
        """Complete therapy session"""
        
        try:
            session = self.get_session(session_id)
            if not session:
                return False
            
            session.status = SessionStatus.COMPLETED
            
            # Update session metrics
            if session.session_metrics:
                session.session_metrics.end_time = datetime.now()
                if session.session_metrics.start_time:
                    duration = (session.session_metrics.end_time - session.session_metrics.start_time).total_seconds() / 60
                    session.session_metrics.duration_minutes = int(duration)
                
                # Calculate goal achievement
                session.session_metrics.total_goals = len(session.session_goals)
                session.session_metrics.goals_achieved = sum(1 for goal in session.session_goals if goal.achieved)
            
            # Add session completion note
            completion_note = SessionNote(
                note_id=f"NOTE_{session_id}_COMPLETE_{datetime.now().strftime('%H%M%S')}",
                note_type="session_completion",
                content=f"Session completed. Summary: {session_summary}",
                timestamp=datetime.now()
            )
            session.session_notes.append(completion_note)
            
            # Set next session recommendations
            if next_session_recommendations:
                session.next_session_recommendations = next_session_recommendations
            
            session.last_updated = datetime.now()
            self._update_session_in_db(session)
            
            self.logger.info(f"Completed session: {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to complete session: {e}")
            return False
    
    def get_session(self, session_id: str) -> Optional[TherapySession]:
        """Retrieve session by ID"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get main session data
                cursor.execute("SELECT * FROM therapy_sessions WHERE session_id = ?", (session_id,))
                session_row = cursor.fetchone()
                
                if not session_row:
                    return None
                
                # Parse session data
                session = self._row_to_session(session_row)
                
                # Get session goals
                cursor.execute("SELECT * FROM session_goals WHERE session_id = ?", (session_id,))
                for goal_row in cursor.fetchall():
                    goal = SessionGoal(
                        goal_id=goal_row[0],
                        description=goal_row[2],
                        priority=goal_row[3],
                        target_phase=SessionPhase(goal_row[4]),
                        success_criteria=json.loads(goal_row[5]) if goal_row[5] else [],
                        achieved=bool(goal_row[6]),
                        notes=goal_row[7] or ""
                    )
                    session.session_goals.append(goal)
                
                # Get session notes
                cursor.execute("SELECT * FROM session_notes WHERE session_id = ?", (session_id,))
                for note_row in cursor.fetchall():
                    note = SessionNote(
                        note_id=note_row[0],
                        note_type=note_row[2],
                        content=note_row[3],
                        timestamp=datetime.fromisoformat(note_row[4]),
                        phase=SessionPhase(note_row[5]) if note_row[5] else None,
                        risk_indicators=json.loads(note_row[6]) if note_row[6] else [],
                        follow_up_needed=bool(note_row[7])
                    )
                    session.session_notes.append(note)
                
                # Get homework assignments
                cursor.execute("SELECT * FROM homework_assignments WHERE session_id = ?", (session_id,))
                for hw_row in cursor.fetchall():
                    assignment = HomeworkAssignment(
                        assignment_id=hw_row[0],
                        title=hw_row[2],
                        description=hw_row[3],
                        instructions=json.loads(hw_row[4]) if hw_row[4] else [],
                        due_date=datetime.fromisoformat(hw_row[5]).date() if hw_row[5] else None,
                        estimated_time_minutes=hw_row[6] or 30,
                        difficulty_level=hw_row[7] or "moderate",
                        therapeutic_rationale=hw_row[8] or ""
                    )
                    session.homework_assignments.append(assignment)
                
                # Get session metrics
                cursor.execute("SELECT * FROM session_metrics WHERE session_id = ?", (session_id,))
                metrics_row = cursor.fetchone()
                if metrics_row:
                    session.session_metrics = SessionMetrics(
                        start_time=datetime.fromisoformat(metrics_row[1]),
                        end_time=datetime.fromisoformat(metrics_row[2]) if metrics_row[2] else None,
                        duration_minutes=metrics_row[3],
                        patient_engagement_score=metrics_row[4],
                        mood_pre_session=metrics_row[5],
                        mood_post_session=metrics_row[6],
                        anxiety_pre_session=metrics_row[7],
                        anxiety_post_session=metrics_row[8],
                        homework_completion_rate=metrics_row[9],
                        goals_achieved=metrics_row[10] or 0,
                        total_goals=metrics_row[11] or 0
                    )
                
                return session
                
        except Exception as e:
            self.logger.error(f"Failed to retrieve session: {e}")
            return None
    
    def _row_to_session(self, row: Tuple) -> TherapySession:
        """Convert database row to TherapySession object"""
        
        session = TherapySession(
            session_id=row[0],
            patient_id=row[1],
            session_type=SessionType(row[2]),
            session_number=row[3],
            scheduled_date=datetime.fromisoformat(row[4]),
            therapy_modality=row[5],
            treatment_phase=row[6],
            status=SessionStatus(row[7]),
            session_goals=[]  # Will be populated separately
        )
        
        # Optional fields
        if row[8]:
            session.current_phase = SessionPhase(row[8])
        if row[9]:
            session.completed_phases = [SessionPhase(phase) for phase in json.loads(row[9])]
        if row[10]:
            session.interventions_used = [InterventionType(i) for i in json.loads(row[10])]
        if row[11]:
            session.risk_assessment = json.loads(row[11])
        if row[12]:
            session.next_session_recommendations = json.loads(row[12])
        
        session.created_date = datetime.fromisoformat(row[13])
        session.last_updated = datetime.fromisoformat(row[14])
        
        return session
    
    def _save_session_to_db(self, session: TherapySession):
        """Save session to database"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Save main session
            cursor.execute("""
                INSERT OR REPLACE INTO therapy_sessions (
                    session_id, patient_id, session_type, session_number, scheduled_date,
                    therapy_modality, treatment_phase, status, current_phase, completed_phases,
                    interventions_used, risk_assessment, next_session_recommendations,
                    created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id,
                session.patient_id,
                session.session_type.value,
                session.session_number,
                session.scheduled_date.isoformat(),
                session.therapy_modality,
                session.treatment_phase,
                session.status.value,
                session.current_phase.value if session.current_phase else None,
                json.dumps([phase.value for phase in session.completed_phases]),
                json.dumps([intervention.value for intervention in session.interventions_used]),
                json.dumps(session.risk_assessment),
                json.dumps(session.next_session_recommendations),
                session.created_date.isoformat(),
                session.last_updated.isoformat()
            ))
            
            conn.commit()
    
    def _update_session_in_db(self, session: TherapySession):
        """Update existing session in database"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Update main session
            cursor.execute("""
                UPDATE therapy_sessions SET
                    status = ?, current_phase = ?, completed_phases = ?, interventions_used = ?,
                    risk_assessment = ?, next_session_recommendations = ?, last_updated = ?
                WHERE session_id = ?
            """, (
                session.status.value,
                session.current_phase.value if session.current_phase else None,
                json.dumps([phase.value for phase in session.completed_phases]),
                json.dumps([intervention.value for intervention in session.interventions_used]),
                json.dumps(session.risk_assessment),
                json.dumps(session.next_session_recommendations),
                session.last_updated.isoformat(),
                session.session_id
            ))
            
            # Update or insert session goals
            for goal in session.session_goals:
                cursor.execute("""
                    INSERT OR REPLACE INTO session_goals (
                        goal_id, session_id, description, priority, target_phase,
                        success_criteria, achieved, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    goal.goal_id,
                    session.session_id,
                    goal.description,
                    goal.priority,
                    goal.target_phase.value,
                    json.dumps(goal.success_criteria),
                    goal.achieved,
                    goal.notes
                ))
            
            # Update or insert session notes
            for note in session.session_notes:
                cursor.execute("""
                    INSERT OR REPLACE INTO session_notes (
                        note_id, session_id, note_type, content, timestamp,
                        phase, risk_indicators, follow_up_needed
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    note.note_id,
                    session.session_id,
                    note.note_type,
                    note.content,
                    note.timestamp.isoformat(),
                    note.phase.value if note.phase else None,
                    json.dumps(note.risk_indicators),
                    note.follow_up_needed
                ))
            
            # Update or insert homework assignments
            for assignment in session.homework_assignments:
                cursor.execute("""
                    INSERT OR REPLACE INTO homework_assignments (
                        assignment_id, session_id, title, description, instructions,
                        due_date, estimated_time_minutes, difficulty_level, therapeutic_rationale
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    assignment.assignment_id,
                    session.session_id,
                    assignment.title,
                    assignment.description,
                    json.dumps(assignment.instructions),
                    assignment.due_date.isoformat() if assignment.due_date else None,
                    assignment.estimated_time_minutes,
                    assignment.difficulty_level,
                    assignment.therapeutic_rationale
                ))
            
            # Update session metrics
            if session.session_metrics:
                cursor.execute("""
                    INSERT OR REPLACE INTO session_metrics (
                        session_id, start_time, end_time, duration_minutes,
                        patient_engagement_score, mood_pre_session, mood_post_session,
                        anxiety_pre_session, anxiety_post_session, homework_completion_rate,
                        goals_achieved, total_goals
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session.session_id,
                    session.session_metrics.start_time.isoformat(),
                    session.session_metrics.end_time.isoformat() if session.session_metrics.end_time else None,
                    session.session_metrics.duration_minutes,
                    session.session_metrics.patient_engagement_score,
                    session.session_metrics.mood_pre_session,
                    session.session_metrics.mood_post_session,
                    session.session_metrics.anxiety_pre_session,
                    session.session_metrics.anxiety_post_session,
                    session.session_metrics.homework_completion_rate,
                    session.session_metrics.goals_achieved,
                    session.session_metrics.total_goals
                ))
            
            conn.commit()
    
    def get_patient_sessions(self, patient_id: str, limit: Optional[int] = None) -> List[TherapySession]:
        """Get all sessions for a patient"""
        
        sessions = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT session_id FROM therapy_sessions 
                    WHERE patient_id = ? 
                    ORDER BY session_number DESC
                """
                
                if limit:
                    query += f" LIMIT {limit}"
                
                cursor.execute(query, (patient_id,))
                
                for row in cursor.fetchall():
                    session = self.get_session(row[0])
                    if session:
                        sessions.append(session)
                
            return sessions
            
        except Exception as e:
            self.logger.error(f"Failed to get patient sessions: {e}")
            return []
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        
        session = self.get_session(session_id)
        if not session:
            return {}
        
        # Calculate session statistics
        duration = None
        if session.session_metrics and session.session_metrics.duration_minutes:
            duration = session.session_metrics.duration_minutes
        
        goals_achieved = sum(1 for goal in session.session_goals if goal.achieved)
        total_goals = len(session.session_goals)
        goal_achievement_rate = (goals_achieved / total_goals * 100) if total_goals > 0 else 0
        
        # Risk indicators
        risk_notes = [note for note in session.session_notes if note.risk_indicators]
        high_risk_present = bool(risk_notes)
        
        summary = {
            "session_info": {
                "session_id": session.session_id,
                "session_number": session.session_number,
                "session_type": session.session_type.value,
                "status": session.status.value,
                "scheduled_date": session.scheduled_date.isoformat(),
                "therapy_modality": session.therapy_modality,
                "treatment_phase": session.treatment_phase
            },
            "session_metrics": {
                "duration_minutes": duration,
                "goals_achieved": goals_achieved,
                "total_goals": total_goals,
                "goal_achievement_rate": goal_achievement_rate
            },
            "interventions_used": [i.value for i in session.interventions_used],
            "homework_assigned": len(session.homework_assignments),
            "clinical_notes": len(session.session_notes),
            "risk_assessment": {
                "high_risk_present": high_risk_present,
                "risk_indicators": list(set(indicator for note in risk_notes for indicator in note.risk_indicators)),
                "follow_up_needed": any(note.follow_up_needed for note in session.session_notes)
            },
            "next_session_recommendations": session.next_session_recommendations
        }
        
        # Add detailed metrics if available
        if session.session_metrics:
            summary["detailed_metrics"] = {
                "patient_engagement": session.session_metrics.patient_engagement_score,
                "mood_change": (
                    session.session_metrics.mood_post_session - session.session_metrics.mood_pre_session
                    if session.session_metrics.mood_pre_session and session.session_metrics.mood_post_session
                    else None
                ),
                "anxiety_change": (
                    session.session_metrics.anxiety_post_session - session.session_metrics.anxiety_pre_session
                    if session.session_metrics.anxiety_pre_session and session.session_metrics.anxiety_post_session
                    else None
                ),
                "homework_completion_rate": session.session_metrics.homework_completion_rate
            }
        
        return summary
    
    def generate_session_report(self, session_id: str) -> str:
        """Generate comprehensive session report"""
        
        summary = self.get_session_summary(session_id)
        session = self.get_session(session_id)
        
        if not summary or not session:
            return "Session not found or incomplete data"
        
        report_sections = []
        
        # Header
        report_sections.append("THERAPY SESSION REPORT")
        report_sections.append("=" * 50)
        report_sections.append(f"Session ID: {summary['session_info']['session_id']}")
        report_sections.append(f"Session #{summary['session_info']['session_number']}")
        report_sections.append(f"Date: {summary['session_info']['scheduled_date'][:10]}")
        report_sections.append(f"Type: {summary['session_info']['session_type'].title()}")
        report_sections.append(f"Modality: {summary['session_info']['therapy_modality']}")
        report_sections.append(f"Treatment Phase: {summary['session_info']['treatment_phase'].title()}")
        report_sections.append(f"Status: {summary['session_info']['status'].title()}")
        report_sections.append("")
        
        # Session Metrics
        report_sections.append("SESSION METRICS:")
        metrics = summary['session_metrics']
        if metrics['duration_minutes']:
            report_sections.append(f"  Duration: {metrics['duration_minutes']} minutes")
        report_sections.append(f"  Goals Achieved: {metrics['goals_achieved']}/{metrics['total_goals']} ({metrics['goal_achievement_rate']:.1f}%)")
        report_sections.append(f"  Interventions Used: {len(summary['interventions_used'])}")
        report_sections.append(f"  Homework Assigned: {summary['homework_assigned']} items")
        report_sections.append("")
        
        # Detailed Metrics
        if "detailed_metrics" in summary:
            detailed = summary["detailed_metrics"]
            report_sections.append("DETAILED METRICS:")
            if detailed["patient_engagement"]:
                report_sections.append(f"  Patient Engagement: {detailed['patient_engagement']}/10")
            if detailed["mood_change"] is not None:
                change_desc = "improved" if detailed["mood_change"] > 0 else "declined" if detailed["mood_change"] < 0 else "stable"
                report_sections.append(f"  Mood Change: {detailed['mood_change']:+.1f} ({change_desc})")
            if detailed["anxiety_change"] is not None:
                change_desc = "reduced" if detailed["anxiety_change"] < 0 else "increased" if detailed["anxiety_change"] > 0 else "stable"
                report_sections.append(f"  Anxiety Change: {detailed['anxiety_change']:+.1f} ({change_desc})")
            report_sections.append("")
        
        # Interventions Used
        if summary['interventions_used']:
            report_sections.append("INTERVENTIONS APPLIED:")
            for intervention in summary['interventions_used']:
                report_sections.append(f"  • {intervention.replace('_', ' ').title()}")
            report_sections.append("")
        
        # Risk Assessment
        risk = summary['risk_assessment']
        if risk['high_risk_present'] or risk['follow_up_needed']:
            report_sections.append("⚠️  RISK ASSESSMENT:")
            if risk['high_risk_present']:
                report_sections.append("  High Risk Indicators Present:")
                for indicator in risk['risk_indicators']:
                    report_sections.append(f"    • {indicator}")
            if risk['follow_up_needed']:
                report_sections.append("  Follow-up Required: Yes")
            report_sections.append("")
        
        # Session Goals
        if session.session_goals:
            report_sections.append("SESSION GOALS:")
            for goal in session.session_goals:
                status_icon = "✓" if goal.achieved else "○"
                report_sections.append(f"  {status_icon} {goal.description}")
                if goal.notes:
                    report_sections.append(f"    Notes: {goal.notes}")
            report_sections.append("")
        
        # Homework Assignments
        if session.homework_assignments:
            report_sections.append("HOMEWORK ASSIGNED:")
            for assignment in session.homework_assignments:
                report_sections.append(f"  • {assignment.title}")
                report_sections.append(f"    Due: {assignment.due_date}")
                report_sections.append(f"    Estimated Time: {assignment.estimated_time_minutes} minutes")
                if assignment.therapeutic_rationale:
                    report_sections.append(f"    Rationale: {assignment.therapeutic_rationale}")
            report_sections.append("")
        
        # Next Session Recommendations
        if summary['next_session_recommendations']:
            report_sections.append("NEXT SESSION RECOMMENDATIONS:")
            for rec in summary['next_session_recommendations']:
                report_sections.append(f"  • {rec}")
            report_sections.append("")
        
        return "\n".join(report_sections)


# Example usage and testing
if __name__ == "__main__":
    print("=== SESSION MANAGER SYSTEM DEMONSTRATION ===\n")
    
    # Initialize session manager
    session_manager = SessionManager()
    
    # Create sample session
    print("Creating therapy session...")
    session = session_manager.create_session(
        patient_id="PT_20240101_ABC123",
        session_type=SessionType.THERAPY,
        session_number=5,
        scheduled_date=datetime.now(),
        therapy_modality="CBT",
        treatment_phase="working"
    )
    
    print(f"Created session: {session.session_id}")
    print(f"Session goals: {len(session.session_goals)}")
    print()
    
    # Start session
    print("Starting session...")
    session_manager.start_session(session.session_id)
    
    # Advance through phases
    print("Advancing through session phases...")
    session_manager.advance_session_phase(
        session.session_id, 
        SessionPhase.CHECK_IN,
        "Patient reports moderate mood, some work anxiety"
    )
    
    # Add interventions
    print("Adding interventions...")
    session_manager.add_intervention(
        session.session_id,
        InterventionType.COGNITIVE_RESTRUCTURING,
        "Worked on catastrophic thinking about work presentation",
        SessionPhase.MAIN_WORK
    )
    
    # Add session notes
    print("Adding clinical notes...")
    session_manager.add_session_note(
        session.session_id,
        "observation",
        "Patient demonstrated good insight into thought patterns. Engaged actively in cognitive restructuring exercise."
    )
    
    # Assign homework
    print("Assigning homework...")
    session_manager.assign_homework(
        session.session_id,
        "thought_record",
        custom_instructions=[
            "Focus specifically on work-related anxiety thoughts",
            "Complete one entry each morning and evening"
        ],
        due_date=date.today() + timedelta(days=7)
    )
    
    # Update session metrics
    print("Updating session metrics...")
    session_manager.update_session_metrics(session.session_id, {
        "patient_engagement_score": 9,
        "mood_pre_session": 5,
        "mood_post_session": 7,
        "anxiety_pre_session": 8,
        "anxiety_post_session": 6,
        "homework_completion_rate": 0.8
    })
    
    # Complete session
    print("Completing session...")
    session_manager.complete_session(
        session.session_id,
        "Productive session. Patient showed excellent engagement and insight.",
        ["Continue cognitive restructuring practice", "Monitor anxiety levels"]
    )
    
    # Get session summary
    print("\n=== SESSION SUMMARY ===")
    summary = session_manager.get_session_summary(session.session_id)
    
    print(f"Session #{summary['session_info']['session_number']}")
    print(f"Status: {summary['session_info']['status']}")
    print(f"Duration: {summary['session_metrics']['duration_minutes']} minutes")
    print(f"Goals Achieved: {summary['session_metrics']['goals_achieved']}/{summary['session_metrics']['total_goals']}")
    print(f"Interventions Used: {len(summary['interventions_used'])}")
    print(f"Homework Assigned: {summary['homework_assigned']} items")
    
    # Generate session report
    print("\n=== SESSION REPORT ===")
    report = session_manager.generate_session_report(session.session_id)
    print(report)
    
    print("\n" + "="*60)
    print("Session manager system demonstration complete!")
    print("Professional session management with structured protocols and documentation.")
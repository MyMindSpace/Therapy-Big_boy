from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import sqlite3
import json


class SessionPhase(Enum):
    OPENING = "opening"
    HOMEWORK_REVIEW = "homework_review"
    MAIN_WORK = "main_work"
    SKILL_PRACTICE = "skill_practice"
    HOMEWORK_ASSIGNMENT = "homework_assignment"
    CLOSING = "closing"
    CRISIS_INTERVENTION = "crisis_intervention"


class SessionStatus(Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"


class TherapyModality(Enum):
    CBT = "cbt"
    DBT = "dbt"
    ACT = "act"
    PSYCHODYNAMIC = "psychodynamic"
    HUMANISTIC = "humanistic"
    EMDR = "emdr"
    INTEGRATIVE = "integrative"


class SessionIntensity(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    INTENSIVE = "intensive"


@dataclass
class SessionPhaseStructure:
    phase: SessionPhase
    duration_minutes: int
    objectives: List[str]
    activities: List[str]
    required: bool = True
    flexibility_level: int = 1
    crisis_adaptable: bool = False


@dataclass
class SessionStructure:
    session_id: str
    patient_id: str
    therapist_id: str
    therapy_modality: TherapyModality
    session_number: int
    total_duration: int
    session_date: datetime
    session_status: SessionStatus
    phases: List[SessionPhaseStructure]
    session_goals: List[str]
    adaptations_made: List[str] = field(default_factory=list)
    intensity_level: SessionIntensity = SessionIntensity.MODERATE
    notes: str = ""


@dataclass
class SessionTracking:
    session_id: str
    current_phase: SessionPhase
    phase_start_time: datetime
    time_remaining: int
    completed_objectives: List[str]
    pending_objectives: List[str]
    adaptations_needed: List[str]
    effectiveness_rating: int = 0


@dataclass
class SessionOutcome:
    session_id: str
    completion_status: str
    objectives_achieved: List[str]
    goals_progress: Dict[str, int]
    homework_assigned: bool
    crisis_addressed: bool
    follow_up_needed: bool
    session_effectiveness: int
    patient_feedback: str
    therapist_observations: str
    next_session_focus: List[str]


class SessionFramework:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.modality_structures = self._initialize_modality_structures()
        self.phase_templates = self._initialize_phase_templates()
        self.adaptation_strategies = self._initialize_adaptation_strategies()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_structures (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    therapist_id TEXT NOT NULL,
                    therapy_modality TEXT NOT NULL,
                    session_number INTEGER,
                    total_duration INTEGER,
                    session_date TEXT,
                    session_status TEXT,
                    phases TEXT,
                    session_goals TEXT,
                    adaptations_made TEXT,
                    intensity_level TEXT,
                    notes TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    current_phase TEXT,
                    phase_start_time TEXT,
                    time_remaining INTEGER,
                    completed_objectives TEXT,
                    pending_objectives TEXT,
                    adaptations_needed TEXT,
                    effectiveness_rating INTEGER,
                    tracking_time TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_outcomes (
                    session_id TEXT PRIMARY KEY,
                    completion_status TEXT,
                    objectives_achieved TEXT,
                    goals_progress TEXT,
                    homework_assigned BOOLEAN,
                    crisis_addressed BOOLEAN,
                    follow_up_needed BOOLEAN,
                    session_effectiveness INTEGER,
                    patient_feedback TEXT,
                    therapist_observations TEXT,
                    next_session_focus TEXT,
                    outcome_date TEXT
                )
            """)
    
    def _initialize_modality_structures(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "cbt": {
                "standard_duration": 50,
                "typical_phases": [
                    SessionPhaseStructure(
                        phase=SessionPhase.OPENING,
                        duration_minutes=5,
                        objectives=["Check-in", "Agenda setting", "Mood assessment"],
                        activities=["Greeting", "Brief mood check", "Session planning"],
                        required=True
                    ),
                    SessionPhaseStructure(
                        phase=SessionPhase.HOMEWORK_REVIEW,
                        duration_minutes=10,
                        objectives=["Review homework completion", "Process learning", "Problem-solve barriers"],
                        activities=["Homework discussion", "Skill reinforcement", "Obstacle identification"],
                        required=True
                    ),
                    SessionPhaseStructure(
                        phase=SessionPhase.MAIN_WORK,
                        duration_minutes=25,
                        objectives=["Address session agenda", "Practice core CBT skills", "Work on goals"],
                        activities=["Cognitive restructuring", "Behavioral experiments", "Skill building"],
                        required=True,
                        flexibility_level=3
                    ),
                    SessionPhaseStructure(
                        phase=SessionPhase.HOMEWORK_ASSIGNMENT,
                        duration_minutes=5,
                        objectives=["Assign relevant homework", "Ensure understanding", "Plan practice"],
                        activities=["Homework planning", "Instruction clarification", "Barrier anticipation"],
                        required=True
                    ),
                    SessionPhaseStructure(
                        phase=SessionPhase.CLOSING,
                        duration_minutes=5,
                        objectives=["Summarize session", "Plan next steps", "Check understanding"],
                        activities=["Session summary", "Next session planning", "Question addressing"],
                        required=True
                    )
                ],
                "crisis_adaptations": {
                    "priority_phases": [SessionPhase.OPENING, SessionPhase.CRISIS_INTERVENTION, SessionPhase.CLOSING],
                    "flexible_phases": [SessionPhase.HOMEWORK_REVIEW, SessionPhase.MAIN_WORK]
                }
            },
            
            "dbt": {
                "standard_duration": 50,
                "typical_phases": [
                    SessionPhaseStructure(
                        phase=SessionPhase.OPENING,
                        duration_minutes=10,
                        objectives=["Assess current distress", "Review diary card", "Safety check"],
                        activities=["Distress scale", "Diary card review", "Crisis assessment"],
                        required=True
                    ),
                    SessionPhaseStructure(
                        phase=SessionPhase.MAIN_WORK,
                        duration_minutes=35,
                        objectives=["Skills training", "Crisis management", "Behavioral analysis"],
                        activities=["Skills practice", "Chain analysis", "Problem solving"],
                        required=True,
                        flexibility_level=4,
                        crisis_adaptable=True
                    ),
                    SessionPhaseStructure(
                        phase=SessionPhase.CLOSING,
                        duration_minutes=5,
                        objectives=["Summarize skills learned", "Plan skill practice", "Check commitment"],
                        activities=["Skills summary", "Practice planning", "Commitment assessment"],
                        required=True
                    )
                ],
                "crisis_adaptations": {
                    "priority_phases": [SessionPhase.OPENING, SessionPhase.CRISIS_INTERVENTION],
                    "distress_tolerance_focus": True
                }
            },
            
            "psychodynamic": {
                "standard_duration": 50,
                "typical_phases": [
                    SessionPhaseStructure(
                        phase=SessionPhase.OPENING,
                        duration_minutes=5,
                        objectives=["Begin with patient's immediate experience", "Notice transference"],
                        activities=["Free association beginning", "Transference observation"],
                        required=True,
                        flexibility_level=5
                    ),
                    SessionPhaseStructure(
                        phase=SessionPhase.MAIN_WORK,
                        duration_minutes=40,
                        objectives=["Explore unconscious material", "Work with transference", "Develop insight"],
                        activities=["Free association", "Dream work", "Interpretation", "Pattern exploration"],
                        required=True,
                        flexibility_level=5,
                        crisis_adaptable=False
                    ),
                    SessionPhaseStructure(
                        phase=SessionPhase.CLOSING,
                        duration_minutes=5,
                        objectives=["Process session material", "Prepare for ending"],
                        activities=["Integration", "Ending preparation"],
                        required=True
                    )
                ],
                "crisis_adaptations": {
                    "priority_phases": [SessionPhase.OPENING, SessionPhase.CRISIS_INTERVENTION],
                    "insight_work_pause": True
                }
            },
            
            "act": {
                "standard_duration": 50,
                "typical_phases": [
                    SessionPhaseStructure(
                        phase=SessionPhase.OPENING,
                        duration_minutes=5,
                        objectives=["Present moment awareness", "Connect with values"],
                        activities=["Mindfulness moment", "Values check-in"],
                        required=True
                    ),
                    SessionPhaseStructure(
                        phase=SessionPhase.MAIN_WORK,
                        duration_minutes=35,
                        objectives=["Practice psychological flexibility", "Values clarification", "Committed action"],
                        activities=["Defusion exercises", "Values work", "Behavioral commitments"],
                        required=True,
                        flexibility_level=3
                    ),
                    SessionPhaseStructure(
                        phase=SessionPhase.CLOSING,
                        duration_minutes=10,
                        objectives=["Summarize insights", "Plan values-based actions"],
                        activities=["Insight integration", "Action planning"],
                        required=True
                    )
                ]
            }
        }
    
    def _initialize_phase_templates(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "opening": {
                "standard_activities": [
                    "Greeting and initial rapport",
                    "Mood and functioning check-in",
                    "Session agenda collaboration",
                    "Safety assessment if indicated"
                ],
                "time_range": (3, 10),
                "adaptations": {
                    "crisis": "Immediate safety assessment and stabilization",
                    "low_motivation": "Enhanced engagement and motivation building",
                    "high_distress": "Distress management and grounding"
                }
            },
            
            "homework_review": {
                "standard_activities": [
                    "Homework completion assessment",
                    "Learning extraction and reinforcement",
                    "Barrier identification and problem-solving",
                    "Skill generalization discussion"
                ],
                "time_range": (5, 15),
                "adaptations": {
                    "non_compliance": "Barrier exploration and motivation enhancement",
                    "partial_completion": "Success reinforcement and obstacle addressing",
                    "high_success": "Skill building and complexity increase"
                }
            },
            
            "main_work": {
                "standard_activities": [
                    "Primary therapeutic intervention",
                    "Skill building and practice",
                    "Goal-focused work",
                    "Problem-solving and insight development"
                ],
                "time_range": (20, 40),
                "adaptations": {
                    "crisis": "Crisis intervention and safety planning",
                    "resistance": "Resistance exploration and alliance building",
                    "breakthrough": "Insight consolidation and integration"
                }
            },
            
            "closing": {
                "standard_activities": [
                    "Session summary and integration",
                    "Homework assignment and planning",
                    "Next session preparation",
                    "Final check-in and support"
                ],
                "time_range": (5, 10),
                "adaptations": {
                    "crisis": "Safety planning and resource connection",
                    "overwhelming_content": "Grounding and stabilization",
                    "high_insight": "Integration support and application planning"
                }
            }
        }
    
    def _initialize_adaptation_strategies(self) -> Dict[str, List[str]]:
        
        return {
            "crisis_adaptations": [
                "Prioritize safety assessment and intervention",
                "Extend opening phase for thorough crisis evaluation",
                "Modify main work to focus on crisis resolution",
                "Ensure robust safety planning in closing",
                "Consider session extension if needed"
            ],
            
            "low_engagement": [
                "Enhance rapport building in opening",
                "Increase collaborative agenda setting",
                "Use motivational interviewing techniques",
                "Adjust intervention intensity and pace",
                "Focus on patient strengths and successes"
            ],
            
            "high_distress": [
                "Begin with grounding and stabilization",
                "Use distress tolerance skills",
                "Slow pace and provide more support",
                "Focus on immediate coping strategies",
                "Ensure patient feels contained and safe"
            ],
            
            "resistance_patterns": [
                "Explore resistance as meaningful communication",
                "Increase patient choice and collaboration",
                "Address therapeutic relationship issues",
                "Modify approach based on patient feedback",
                "Consider pacing and readiness factors"
            ],
            
            "breakthrough_moments": [
                "Allow additional time for processing",
                "Support insight integration",
                "Plan application to real-life situations",
                "Reinforce progress and growth",
                "Prepare for potential temporary regression"
            ]
        }
    
    def create_session_structure(self, patient_id: str, therapist_id: str, 
                               therapy_modality: TherapyModality, session_number: int,
                               duration: int = 50) -> SessionStructure:
        
        session_id = f"{patient_id}_{session_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        modality_template = self.modality_structures.get(therapy_modality.value, 
                                                        self.modality_structures["cbt"])
        
        phases = []
        for phase_template in modality_template["typical_phases"]:
            phases.append(SessionPhaseStructure(
                phase=phase_template.phase,
                duration_minutes=phase_template.duration_minutes,
                objectives=phase_template.objectives.copy(),
                activities=phase_template.activities.copy(),
                required=phase_template.required,
                flexibility_level=phase_template.flexibility_level,
                crisis_adaptable=getattr(phase_template, 'crisis_adaptable', False)
            ))
        
        session_structure = SessionStructure(
            session_id=session_id,
            patient_id=patient_id,
            therapist_id=therapist_id,
            therapy_modality=therapy_modality,
            session_number=session_number,
            total_duration=duration,
            session_date=datetime.now(),
            session_status=SessionStatus.SCHEDULED,
            phases=phases,
            session_goals=[]
        )
        
        self._adjust_phase_timing(session_structure)
        self._save_session_structure(session_structure)
        
        return session_structure
    
    def _adjust_phase_timing(self, session_structure: SessionStructure):
        
        total_planned = sum(phase.duration_minutes for phase in session_structure.phases)
        
        if total_planned != session_structure.total_duration:
            adjustment_factor = session_structure.total_duration / total_planned
            
            for phase in session_structure.phases:
                if phase.flexibility_level > 1:
                    phase.duration_minutes = int(phase.duration_minutes * adjustment_factor)
        
        remaining_time = session_structure.total_duration - sum(phase.duration_minutes for phase in session_structure.phases)
        
        if remaining_time > 0:
            main_work_phase = next((p for p in session_structure.phases if p.phase == SessionPhase.MAIN_WORK), None)
            if main_work_phase:
                main_work_phase.duration_minutes += remaining_time
    
    def adapt_session_for_crisis(self, session_id: str, crisis_level: str) -> SessionStructure:
        
        session_structure = self._get_session_structure(session_id)
        if not session_structure:
            raise ValueError(f"Session {session_id} not found")
        
        modality_adaptations = self.modality_structures[session_structure.therapy_modality.value].get("crisis_adaptations", {})
        
        crisis_phase = SessionPhaseStructure(
            phase=SessionPhase.CRISIS_INTERVENTION,
            duration_minutes=30,
            objectives=["Assess immediate safety", "Provide crisis intervention", "Develop safety plan"],
            activities=["Safety assessment", "Crisis counseling", "Safety planning", "Resource connection"],
            required=True,
            crisis_adaptable=True
        )
        
        if crisis_level in ["high", "severe"]:
            new_phases = [
                next(p for p in session_structure.phases if p.phase == SessionPhase.OPENING),
                crisis_phase,
                next(p for p in session_structure.phases if p.phase == SessionPhase.CLOSING)
            ]
            
            new_phases[0].duration_minutes = 10
            new_phases[2].duration_minutes = 10
            
        else:
            session_structure.phases.insert(1, crisis_phase)
            self._adjust_phase_timing(session_structure)
        
        session_structure.phases = new_phases if crisis_level in ["high", "severe"] else session_structure.phases
        session_structure.adaptations_made.append(f"Crisis adaptation for {crisis_level} level crisis")
        session_structure.intensity_level = SessionIntensity.INTENSIVE
        
        self._save_session_structure(session_structure)
        return session_structure
    
    def track_session_progress(self, session_id: str, current_phase: SessionPhase,
                             completed_objectives: List[str]) -> SessionTracking:
        
        session_structure = self._get_session_structure(session_id)
        if not session_structure:
            raise ValueError(f"Session {session_id} not found")
        
        current_phase_structure = next((p for p in session_structure.phases if p.phase == current_phase), None)
        if not current_phase_structure:
            raise ValueError(f"Phase {current_phase.value} not found in session structure")
        
        phases_completed = []
        time_used = 0
        
        for phase in session_structure.phases:
            if phase.phase.value <= current_phase.value:
                if phase.phase != current_phase:
                    phases_completed.append(phase)
                    time_used += phase.duration_minutes
        
        time_remaining = session_structure.total_duration - time_used
        
        pending_objectives = [obj for obj in current_phase_structure.objectives 
                            if obj not in completed_objectives]
        
        tracking = SessionTracking(
            session_id=session_id,
            current_phase=current_phase,
            phase_start_time=datetime.now(),
            time_remaining=time_remaining,
            completed_objectives=completed_objectives,
            pending_objectives=pending_objectives,
            adaptations_needed=[]
        )
        
        if len(pending_objectives) > len(completed_objectives) and time_remaining < current_phase_structure.duration_minutes:
            tracking.adaptations_needed.append("Time management needed - many objectives remaining")
        
        if not completed_objectives and time_remaining < session_structure.total_duration * 0.3:
            tracking.adaptations_needed.append("Low productivity - consider engagement strategies")
        
        self._save_session_tracking(tracking)
        return tracking
    
    def complete_session(self, session_id: str, completion_data: Dict[str, Any]) -> SessionOutcome:
        
        session_structure = self._get_session_structure(session_id)
        if not session_structure:
            raise ValueError(f"Session {session_id} not found")
        
        session_structure.session_status = SessionStatus.COMPLETED
        
        outcome = SessionOutcome(
            session_id=session_id,
            completion_status=completion_data.get("status", "completed"),
            objectives_achieved=completion_data.get("objectives_achieved", []),
            goals_progress=completion_data.get("goals_progress", {}),
            homework_assigned=completion_data.get("homework_assigned", False),
            crisis_addressed=completion_data.get("crisis_addressed", False),
            follow_up_needed=completion_data.get("follow_up_needed", False),
            session_effectiveness=completion_data.get("effectiveness", 0),
            patient_feedback=completion_data.get("patient_feedback", ""),
            therapist_observations=completion_data.get("therapist_observations", ""),
            next_session_focus=completion_data.get("next_focus", [])
        )
        
        self._save_session_structure(session_structure)
        self._save_session_outcome(outcome)
        
        return outcome
    
    def analyze_session_efficiency(self, session_id: str) -> Dict[str, Any]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT current_phase, phase_start_time, completed_objectives, effectiveness_rating
                FROM session_tracking
                WHERE session_id = ?
                ORDER BY tracking_time
            """, (session_id,))
            
            tracking_data = cursor.fetchall()
        
        if not tracking_data:
            return {"error": "No tracking data found for session"}
        
        analysis = {
            "session_id": session_id,
            "total_phase_transitions": len(tracking_data),
            "objective_completion_rate": 0,
            "effectiveness_progression": [],
            "time_management": "unknown",
            "recommendations": []
        }
        
        total_objectives = 0
        completed_objectives = 0
        
        for phase, start_time, objectives_json, effectiveness in tracking_data:
            objectives = json.loads(objectives_json) if objectives_json else []
            completed_objectives += len(objectives)
            
            if effectiveness:
                analysis["effectiveness_progression"].append(effectiveness)
        
        session_structure = self._get_session_structure(session_id)
        if session_structure:
            for phase in session_structure.phases:
                total_objectives += len(phase.objectives)
        
        if total_objectives > 0:
            analysis["objective_completion_rate"] = round((completed_objectives / total_objectives) * 100, 1)
        
        if analysis["objective_completion_rate"] >= 80:
            analysis["time_management"] = "excellent"
        elif analysis["objective_completion_rate"] >= 60:
            analysis["time_management"] = "good"
        elif analysis["objective_completion_rate"] >= 40:
            analysis["time_management"] = "fair"
        else:
            analysis["time_management"] = "poor"
        
        if analysis["objective_completion_rate"] < 60:
            analysis["recommendations"].append("Consider adjusting session pacing or objective complexity")
        
        if len(analysis["effectiveness_progression"]) > 1:
            if analysis["effectiveness_progression"][-1] > analysis["effectiveness_progression"][0]:
                analysis["recommendations"].append("Positive effectiveness trend - continue current approach")
            else:
                analysis["recommendations"].append("Consider modifying intervention approach")
        
        return analysis
    
    def generate_session_report(self, session_id: str) -> Dict[str, Any]:
        
        session_structure = self._get_session_structure(session_id)
        outcome = self._get_session_outcome(session_id)
        efficiency = self.analyze_session_efficiency(session_id)
        
        if not session_structure:
            return {"error": "Session not found"}
        
        report = {
            "session_id": session_id,
            "session_info": {
                "modality": session_structure.therapy_modality.value,
                "session_number": session_structure.session_number,
                "duration": session_structure.total_duration,
                "status": session_structure.session_status.value,
                "adaptations": session_structure.adaptations_made
            },
            "structure_analysis": {
                "phases_planned": len(session_structure.phases),
                "total_objectives": sum(len(p.objectives) for p in session_structure.phases),
                "intensity_level": session_structure.intensity_level.value
            },
            "outcome_summary": {},
            "efficiency_metrics": efficiency,
            "recommendations": []
        }
        
        if outcome:
            report["outcome_summary"] = {
                "completion_status": outcome.completion_status,
                "objectives_achieved": len(outcome.objectives_achieved),
                "homework_assigned": outcome.homework_assigned,
                "crisis_addressed": outcome.crisis_addressed,
                "effectiveness_rating": outcome.session_effectiveness,
                "follow_up_needed": outcome.follow_up_needed
            }
        
        if efficiency.get("time_management") == "poor":
            report["recommendations"].append("Review session pacing and objective setting")
        
        if outcome and outcome.session_effectiveness < 6:
            report["recommendations"].append("Explore factors affecting session effectiveness")
        
        if session_structure.adaptations_made:
            report["recommendations"].append("Continue monitoring need for adaptations")
        
        return report
    
    def _get_session_structure(self, session_id: str) -> Optional[SessionStructure]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT session_id, patient_id, therapist_id, therapy_modality,
                       session_number, total_duration, session_date, session_status,
                       phases, session_goals, adaptations_made, intensity_level, notes
                FROM session_structures
                WHERE session_id = ?
            """, (session_id,))
            
            result = cursor.fetchone()
        
        if not result:
            return None
        
        phases_data = json.loads(result[8]) if result[8] else []
        phases = []
        
        for phase_data in phases_data:
            phases.append(SessionPhaseStructure(
                phase=SessionPhase(phase_data["phase"]),
                duration_minutes=phase_data["duration_minutes"],
                objectives=phase_data["objectives"],
                activities=phase_data["activities"],
                required=phase_data.get("required", True),
                flexibility_level=phase_data.get("flexibility_level", 1),
                crisis_adaptable=phase_data.get("crisis_adaptable", False)
            ))
        
        return SessionStructure(
            session_id=result[0],
            patient_id=result[1],
            therapist_id=result[2],
            therapy_modality=TherapyModality(result[3]),
            session_number=result[4],
            total_duration=result[5],
            session_date=datetime.fromisoformat(result[6]),
            session_status=SessionStatus(result[7]),
            phases=phases,
            session_goals=json.loads(result[9]) if result[9] else [],
            adaptations_made=json.loads(result[10]) if result[10] else [],
            intensity_level=SessionIntensity(result[11]) if result[11] else SessionIntensity.MODERATE,
            notes=result[12] or ""
        )
    
    def _get_session_outcome(self, session_id: str) -> Optional[SessionOutcome]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT session_id, completion_status, objectives_achieved, goals_progress,
                       homework_assigned, crisis_addressed, follow_up_needed,
                       session_effectiveness, patient_feedback, therapist_observations,
                       next_session_focus
                FROM session_outcomes
                WHERE session_id = ?
            """, (session_id,))
            
            result = cursor.fetchone()
        
        if not result:
            return None
        
        return SessionOutcome(
            session_id=result[0],
            completion_status=result[1],
            objectives_achieved=json.loads(result[2]) if result[2] else [],
            goals_progress=json.loads(result[3]) if result[3] else {},
            homework_assigned=result[4],
            crisis_addressed=result[5],
            follow_up_needed=result[6],
            session_effectiveness=result[7],
            patient_feedback=result[8],
            therapist_observations=result[9],
            next_session_focus=json.loads(result[10]) if result[10] else []
        )
    
    def _save_session_structure(self, session_structure: SessionStructure):
        
        phases_data = []
        for phase in session_structure.phases:
            phases_data.append({
                "phase": phase.phase.value,
                "duration_minutes": phase.duration_minutes,
                "objectives": phase.objectives,
                "activities": phase.activities,
                "required": phase.required,
                "flexibility_level": phase.flexibility_level,
                "crisis_adaptable": phase.crisis_adaptable
            })
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO session_structures
                (session_id, patient_id, therapist_id, therapy_modality, session_number,
                 total_duration, session_date, session_status, phases, session_goals,
                 adaptations_made, intensity_level, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_structure.session_id, session_structure.patient_id,
                session_structure.therapist_id, session_structure.therapy_modality.value,
                session_structure.session_number, session_structure.total_duration,
                session_structure.session_date.isoformat(), session_structure.session_status.value,
                json.dumps(phases_data), json.dumps(session_structure.session_goals),
                json.dumps(session_structure.adaptations_made),
                session_structure.intensity_level.value, session_structure.notes
            ))
    
    def _save_session_tracking(self, tracking: SessionTracking):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO session_tracking
                (session_id, current_phase, phase_start_time, time_remaining,
                 completed_objectives, pending_objectives, adaptations_needed,
                 effectiveness_rating, tracking_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tracking.session_id, tracking.current_phase.value,
                tracking.phase_start_time.isoformat(), tracking.time_remaining,
                json.dumps(tracking.completed_objectives),
                json.dumps(tracking.pending_objectives),
                json.dumps(tracking.adaptations_needed),
                tracking.effectiveness_rating, datetime.now().isoformat()
            ))
    
    def _save_session_outcome(self, outcome: SessionOutcome):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO session_outcomes
                (session_id, completion_status, objectives_achieved, goals_progress,
                 homework_assigned, crisis_addressed, follow_up_needed,
                 session_effectiveness, patient_feedback, therapist_observations,
                 next_session_focus, outcome_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                outcome.session_id, outcome.completion_status,
                json.dumps(outcome.objectives_achieved),
                json.dumps(outcome.goals_progress),
                outcome.homework_assigned, outcome.crisis_addressed,
                outcome.follow_up_needed, outcome.session_effectiveness,
                outcome.patient_feedback, outcome.therapist_observations,
                json.dumps(outcome.next_session_focus),
                datetime.now().isoformat()
            ))
    
    def modify_session_structure(self, session_id: str, modifications: Dict[str, Any]) -> SessionStructure:
        
        session_structure = self._get_session_structure(session_id)
        if not session_structure:
            raise ValueError(f"Session {session_id} not found")
        
        if "duration_change" in modifications:
            new_duration = modifications["duration_change"]
            old_duration = session_structure.total_duration
            session_structure.total_duration = new_duration
            
            adjustment_factor = new_duration / old_duration
            for phase in session_structure.phases:
                if phase.flexibility_level > 1:
                    phase.duration_minutes = max(1, int(phase.duration_minutes * adjustment_factor))
            
            session_structure.adaptations_made.append(f"Duration changed from {old_duration} to {new_duration} minutes")
        
        if "add_phase" in modifications:
            new_phase_data = modifications["add_phase"]
            new_phase = SessionPhaseStructure(
                phase=SessionPhase(new_phase_data["phase"]),
                duration_minutes=new_phase_data["duration"],
                objectives=new_phase_data["objectives"],
                activities=new_phase_data["activities"],
                required=new_phase_data.get("required", False),
                flexibility_level=new_phase_data.get("flexibility", 2)
            )
            
            insert_position = new_phase_data.get("position", len(session_structure.phases))
            session_structure.phases.insert(insert_position, new_phase)
            
            session_structure.adaptations_made.append(f"Added {new_phase.phase.value} phase")
        
        if "remove_phase" in modifications:
            phase_to_remove = SessionPhase(modifications["remove_phase"])
            session_structure.phases = [p for p in session_structure.phases 
                                      if p.phase != phase_to_remove or p.required]
            
            if any(p.phase == phase_to_remove and not p.required for p in session_structure.phases):
                session_structure.adaptations_made.append(f"Removed {phase_to_remove.value} phase")
        
        if "modify_objectives" in modifications:
            phase_name = modifications["modify_objectives"]["phase"]
            new_objectives = modifications["modify_objectives"]["objectives"]
            
            for phase in session_structure.phases:
                if phase.phase.value == phase_name:
                    phase.objectives = new_objectives
                    session_structure.adaptations_made.append(f"Modified objectives for {phase_name} phase")
                    break
        
        if "intensity_change" in modifications:
            old_intensity = session_structure.intensity_level
            session_structure.intensity_level = SessionIntensity(modifications["intensity_change"])
            session_structure.adaptations_made.append(f"Intensity changed from {old_intensity.value} to {session_structure.intensity_level.value}")
        
        self._adjust_phase_timing(session_structure)
        self._save_session_structure(session_structure)
        
        return session_structure
    
    def get_session_templates(self, therapy_modality: TherapyModality) -> Dict[str, Any]:
        
        modality_structure = self.modality_structures.get(therapy_modality.value)
        if not modality_structure:
            return {"error": f"No template found for {therapy_modality.value}"}
        
        template = {
            "modality": therapy_modality.value,
            "standard_duration": modality_structure["standard_duration"],
            "phases": [],
            "total_objectives": 0,
            "adaptations_available": []
        }
        
        for phase in modality_structure["typical_phases"]:
            phase_info = {
                "phase": phase.phase.value,
                "duration": phase.duration_minutes,
                "objectives": phase.objectives,
                "activities": phase.activities,
                "required": phase.required,
                "flexibility": phase.flexibility_level
            }
            template["phases"].append(phase_info)
            template["total_objectives"] += len(phase.objectives)
        
        if "crisis_adaptations" in modality_structure:
            template["adaptations_available"].extend(["Crisis intervention", "Safety prioritization"])
        
        template["adaptations_available"].extend([
            "Duration modification",
            "Objective adjustment",
            "Intensity modification",
            "Phase reordering"
        ])
        
        return template
    
    def assess_session_feasibility(self, patient_factors: Dict[str, Any], 
                                 planned_structure: SessionStructure) -> Dict[str, Any]:
        
        assessment = {
            "feasibility_score": 0,
            "concerns": [],
            "recommendations": [],
            "modifications_needed": []
        }
        
        attention_span = patient_factors.get("attention_span", "normal")
        current_distress = patient_factors.get("distress_level", "moderate")
        motivation_level = patient_factors.get("motivation", "moderate")
        crisis_indicators = patient_factors.get("crisis_indicators", [])
        
        base_score = 70
        
        if attention_span == "short":
            base_score -= 20
            assessment["concerns"].append("Short attention span may limit session engagement")
            assessment["modifications_needed"].append("Reduce phase durations and increase breaks")
        elif attention_span == "very_short":
            base_score -= 30
            assessment["concerns"].append("Very short attention span requires significant adaptations")
            assessment["modifications_needed"].append("Consider shorter session or modified structure")
        
        if current_distress == "high":
            base_score -= 15
            assessment["concerns"].append("High distress may interfere with learning objectives")
            assessment["modifications_needed"].append("Prioritize stabilization over skill building")
        elif current_distress == "severe":
            base_score -= 25
            assessment["concerns"].append("Severe distress requires crisis intervention approach")
            assessment["modifications_needed"].append("Switch to crisis intervention structure")
        
        if motivation_level == "low":
            base_score -= 10
            assessment["concerns"].append("Low motivation may affect homework completion")
            assessment["recommendations"].append("Focus on engagement and motivation building")
        elif motivation_level == "very_low":
            base_score -= 20
            assessment["concerns"].append("Very low motivation requires modified approach")
            assessment["modifications_needed"].append("Simplify objectives and increase collaboration")
        
        if crisis_indicators:
            base_score -= 30
            assessment["concerns"].append("Crisis indicators present require immediate attention")
            assessment["modifications_needed"].append("Implement crisis adaptation protocol")
        
        total_objectives = sum(len(phase.objectives) for phase in planned_structure.phases)
        if total_objectives > 15:
            base_score -= 10
            assessment["concerns"].append("High number of objectives may be overwhelming")
            assessment["recommendations"].append("Reduce or prioritize objectives")
        
        if planned_structure.total_duration > 60 and attention_span in ["short", "very_short"]:
            base_score -= 15
            assessment["concerns"].append("Session duration may exceed attention capacity")
            assessment["modifications_needed"].append("Consider reducing session duration")
        
        assessment["feasibility_score"] = max(0, min(100, base_score))
        
        if assessment["feasibility_score"] >= 80:
            assessment["overall_assessment"] = "Highly feasible - proceed as planned"
        elif assessment["feasibility_score"] >= 60:
            assessment["overall_assessment"] = "Feasible with minor modifications"
        elif assessment["feasibility_score"] >= 40:
            assessment["overall_assessment"] = "Challenging - significant modifications needed"
        else:
            assessment["overall_assessment"] = "Not feasible without major restructuring"
        
        return assessment
    
    def generate_session_timeline(self, session_id: str) -> Dict[str, Any]:
        
        session_structure = self._get_session_structure(session_id)
        if not session_structure:
            return {"error": "Session not found"}
        
        timeline = {
            "session_id": session_id,
            "total_duration": session_structure.total_duration,
            "phases": [],
            "key_transitions": [],
            "buffer_time": 0
        }
        
        current_time = 0
        
        for i, phase in enumerate(session_structure.phases):
            phase_timeline = {
                "phase": phase.phase.value,
                "start_time": current_time,
                "end_time": current_time + phase.duration_minutes,
                "duration": phase.duration_minutes,
                "objectives": phase.objectives,
                "activities": phase.activities,
                "flexibility_level": phase.flexibility_level
            }
            
            timeline["phases"].append(phase_timeline)
            
            if i < len(session_structure.phases) - 1:
                timeline["key_transitions"].append({
                    "from_phase": phase.phase.value,
                    "to_phase": session_structure.phases[i + 1].phase.value,
                    "transition_time": current_time + phase.duration_minutes,
                    "transition_notes": f"Transition from {phase.phase.value} to {session_structure.phases[i + 1].phase.value}"
                })
            
            current_time += phase.duration_minutes
        
        timeline["buffer_time"] = session_structure.total_duration - current_time
        
        if timeline["buffer_time"] < 0:
            timeline["timing_warning"] = f"Session overallocated by {abs(timeline['buffer_time'])} minutes"
        elif timeline["buffer_time"] > 5:
            timeline["timing_note"] = f"{timeline['buffer_time']} minutes of unallocated time available"
        
        return timeline
    
    def optimize_session_flow(self, session_id: str, optimization_goals: List[str]) -> SessionStructure:
        
        session_structure = self._get_session_structure(session_id)
        if not session_structure:
            raise ValueError(f"Session {session_id} not found")
        
        original_phases = session_structure.phases.copy()
        
        for goal in optimization_goals:
            if goal == "maximize_therapeutic_work":
                main_work_phase = next((p for p in session_structure.phases 
                                      if p.phase == SessionPhase.MAIN_WORK), None)
                if main_work_phase and main_work_phase.flexibility_level > 2:
                    
                    flexible_phases = [p for p in session_structure.phases 
                                     if p.flexibility_level > 1 and p != main_work_phase]
                    
                    time_to_redistribute = sum(max(0, p.duration_minutes - 3) for p in flexible_phases)
                    
                    for phase in flexible_phases:
                        reduction = max(0, phase.duration_minutes - 3)
                        phase.duration_minutes -= reduction
                    
                    main_work_phase.duration_minutes += time_to_redistribute
                    
                    session_structure.adaptations_made.append("Optimized for maximum therapeutic work time")
            
            elif goal == "improve_engagement":
                opening_phase = next((p for p in session_structure.phases 
                                    if p.phase == SessionPhase.OPENING), None)
                if opening_phase:
                    opening_phase.duration_minutes = min(opening_phase.duration_minutes + 3, 15)
                    opening_phase.objectives.append("Enhanced engagement and rapport building")
                    
                    session_structure.adaptations_made.append("Optimized for improved patient engagement")
            
            elif goal == "crisis_preparedness":
                if not any(p.phase == SessionPhase.CRISIS_INTERVENTION for p in session_structure.phases):
                    crisis_buffer = SessionPhaseStructure(
                        phase=SessionPhase.CRISIS_INTERVENTION,
                        duration_minutes=0,
                        objectives=["Available for crisis intervention if needed"],
                        activities=["Crisis assessment", "Safety planning"],
                        required=False,
                        flexibility_level=5,
                        crisis_adaptable=True
                    )
                    session_structure.phases.append(crisis_buffer)
                    
                    session_structure.adaptations_made.append("Added crisis intervention preparedness")
            
            elif goal == "homework_focus":
                homework_phase = next((p for p in session_structure.phases 
                                     if p.phase == SessionPhase.HOMEWORK_REVIEW), None)
                if homework_phase and homework_phase.duration_minutes < 15:
                    additional_time = min(5, 15 - homework_phase.duration_minutes)
                    homework_phase.duration_minutes += additional_time
                    
                    assignment_phase = next((p for p in session_structure.phases 
                                           if p.phase == SessionPhase.HOMEWORK_ASSIGNMENT), None)
                    if assignment_phase:
                        assignment_phase.duration_minutes += 3
                    
                    session_structure.adaptations_made.append("Optimized for homework focus")
        
        self._adjust_phase_timing(session_structure)
        
        if session_structure.phases != original_phases:
            self._save_session_structure(session_structure)
        
        return session_structure
    
    def create_session_checklist(self, session_id: str) -> Dict[str, Any]:
        
        session_structure = self._get_session_structure(session_id)
        if not session_structure:
            return {"error": "Session not found"}
        
        checklist = {
            "session_id": session_id,
            "pre_session": [],
            "during_session": {},
            "post_session": [],
            "emergency_procedures": []
        }
        
        checklist["pre_session"] = [
            "Review patient file and previous session notes",
            "Prepare materials for planned interventions",
            "Review homework assignments and outcomes",
            "Check for any crisis alerts or safety concerns",
            "Ensure session space is prepared and private"
        ]
        
        for phase in session_structure.phases:
            phase_checklist = []
            
            if phase.phase == SessionPhase.OPENING:
                phase_checklist.extend([
                    "Greet patient warmly and assess immediate presentation",
                    "Conduct mood and safety check-in",
                    "Review agenda and adjust based on patient needs",
                    "Address any immediate concerns or crises"
                ])
            
            elif phase.phase == SessionPhase.HOMEWORK_REVIEW:
                phase_checklist.extend([
                    "Review homework completion and challenges",
                    "Reinforce successes and problem-solve obstacles",
                    "Extract learning and generalize skills",
                    "Document compliance and effectiveness"
                ])
            
            elif phase.phase == SessionPhase.MAIN_WORK:
                phase_checklist.extend([
                    "Implement primary therapeutic interventions",
                    "Monitor patient engagement and understanding",
                    "Practice skills and provide feedback",
                    "Address resistance or difficulties as they arise"
                ])
            
            elif phase.phase == SessionPhase.HOMEWORK_ASSIGNMENT:
                phase_checklist.extend([
                    "Assign relevant and appropriate homework",
                    "Ensure patient understands instructions",
                    "Anticipate and plan for potential barriers",
                    "Confirm patient commitment to completion"
                ])
            
            elif phase.phase == SessionPhase.CLOSING:
                phase_checklist.extend([
                    "Summarize key session points and insights",
                    "Check patient's emotional state before leaving",
                    "Confirm next appointment and homework plans",
                    "Address any final questions or concerns"
                ])
            
            elif phase.phase == SessionPhase.CRISIS_INTERVENTION:
                phase_checklist.extend([
                    "Assess immediate safety and risk level",
                    "Implement appropriate crisis intervention",
                    "Develop or update safety plan",
                    "Connect with support systems and resources"
                ])
            
            checklist["during_session"][phase.phase.value] = phase_checklist
        
        checklist["post_session"] = [
            "Complete session notes and documentation",
            "Update treatment plan if necessary",
            "Note any homework assignments given",
            "Plan for next session based on progress",
            "Complete any required safety documentation"
        ]
        
        checklist["emergency_procedures"] = [
            "If crisis emerges: stop current activity and assess safety",
            "If patient becomes suicidal: implement safety protocol",
            "If patient becomes aggressive: ensure safety and seek help",
            "If patient dissociates: use grounding techniques",
            "Emergency contacts: [to be filled with actual contacts]"
        ]
        
        return checklist


if __name__ == "__main__":
    framework = SessionFramework()
    
    session_structure = framework.create_session_structure(
        patient_id="patient_123",
        therapist_id="therapist_001",
        therapy_modality=TherapyModality.CBT,
        session_number=5,
        duration=50
    )
    
    print("=== SESSION STRUCTURE ===")
    print(f"Session ID: {session_structure.session_id}")
    print(f"Modality: {session_structure.therapy_modality.value}")
    print(f"Duration: {session_structure.total_duration} minutes")
    print(f"Number of phases: {len(session_structure.phases)}")
    
    print("\n=== PHASES ===")
    for phase in session_structure.phases:
        print(f"Phase: {phase.phase.value}")
        print(f"Duration: {phase.duration_minutes} minutes")
        print(f"Objectives: {phase.objectives}")
        print(f"Required: {phase.required}")
        print()
    
    crisis_adapted = framework.adapt_session_for_crisis(session_structure.session_id, "high")
    print("=== CRISIS ADAPTATION ===")
    print(f"Adaptations made: {crisis_adapted.adaptations_made}")
    print(f"New intensity level: {crisis_adapted.intensity_level.value}")
    
    patient_factors = {
        "attention_span": "short",
        "distress_level": "moderate",
        "motivation": "low",
        "crisis_indicators": []
    }
    
    feasibility = framework.assess_session_feasibility(patient_factors, session_structure)
    print(f"\n=== FEASIBILITY ASSESSMENT ===")
    print(f"Feasibility Score: {feasibility['feasibility_score']}")
    print(f"Assessment: {feasibility['overall_assessment']}")
    print(f"Concerns: {feasibility['concerns']}")
    
    timeline = framework.generate_session_timeline(session_structure.session_id)
    print(f"\n=== SESSION TIMELINE ===")
    for phase_timeline in timeline["phases"]:
        print(f"{phase_timeline['start_time']}-{phase_timeline['end_time']} min: {phase_timeline['phase']}")
    
    checklist = framework.create_session_checklist(session_structure.session_id)
    print(f"\n=== PRE-SESSION CHECKLIST ===")
    for item in checklist["pre_session"]:
        print(f"- {item}")
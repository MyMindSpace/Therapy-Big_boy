from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import sqlite3
import json


class GoalType(Enum):
    SESSION_GOAL = "session_goal"
    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"
    TREATMENT_GOAL = "treatment_goal"
    BEHAVIORAL = "behavioral"
    EMOTIONAL = "emotional"
    COGNITIVE = "cognitive"
    INTERPERSONAL = "interpersonal"
    FUNCTIONAL = "functional"


class GoalStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PARTIALLY_ACHIEVED = "partially_achieved"
    ACHIEVED = "achieved"
    REVISED = "revised"
    DISCONTINUED = "discontinued"


class PriorityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class TherapeuticGoal:
    goal_id: str
    patient_id: str
    goal_type: GoalType
    title: str
    description: str
    specific_behaviors: List[str]
    measurement_criteria: List[str]
    target_date: Optional[datetime] = None
    priority_level: PriorityLevel = PriorityLevel.MEDIUM
    status: GoalStatus = GoalStatus.NOT_STARTED
    progress_percentage: int = 0
    barriers: List[str] = field(default_factory=list)
    resources_needed: List[str] = field(default_factory=list)
    intervention_strategies: List[str] = field(default_factory=list)
    milestone_markers: List[str] = field(default_factory=list)
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    notes: str = ""


@dataclass
class SessionGoal:
    session_id: str
    patient_id: str
    goal_description: str
    success_criteria: List[str]
    time_allocation: int
    related_treatment_goals: List[str] = field(default_factory=list)
    priority: PriorityLevel = PriorityLevel.MEDIUM
    achieved: bool = False
    progress_notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class GoalProgress:
    goal_id: str
    session_date: datetime
    progress_rating: int
    progress_description: str
    obstacles_encountered: List[str]
    strategies_used: List[str]
    next_steps: List[str]
    therapist_observations: str
    patient_feedback: str


class SessionGoalSetting:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.goal_templates = self._initialize_goal_templates()
        self.measurement_frameworks = self._initialize_measurement_frameworks()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS therapeutic_goals (
                    goal_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    goal_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    specific_behaviors TEXT,
                    measurement_criteria TEXT,
                    target_date TEXT,
                    priority_level TEXT,
                    status TEXT,
                    progress_percentage INTEGER,
                    barriers TEXT,
                    resources_needed TEXT,
                    intervention_strategies TEXT,
                    milestone_markers TEXT,
                    created_date TEXT,
                    last_updated TEXT,
                    notes TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_goals (
                    session_id TEXT,
                    patient_id TEXT,
                    goal_description TEXT,
                    success_criteria TEXT,
                    time_allocation INTEGER,
                    related_treatment_goals TEXT,
                    priority TEXT,
                    achieved BOOLEAN,
                    progress_notes TEXT,
                    created_at TEXT,
                    PRIMARY KEY (session_id, goal_description)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS goal_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    goal_id TEXT,
                    session_date TEXT,
                    progress_rating INTEGER,
                    progress_description TEXT,
                    obstacles_encountered TEXT,
                    strategies_used TEXT,
                    next_steps TEXT,
                    therapist_observations TEXT,
                    patient_feedback TEXT
                )
            """)
    
    def _initialize_goal_templates(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "depression_goals": {
                "mood_improvement": {
                    "title": "Improve Daily Mood",
                    "description": "Increase overall mood stability and reduce depressive symptoms",
                    "behaviors": ["Daily mood tracking", "Engage in pleasant activities", "Challenge negative thoughts"],
                    "measurements": ["PHQ-9 score reduction", "Mood ratings 1-10", "Activity completion rate"],
                    "timeline": "8 weeks"
                },
                "behavioral_activation": {
                    "title": "Increase Activity Level",
                    "description": "Re-engage in meaningful and enjoyable activities",
                    "behaviors": ["Schedule 3 pleasant activities weekly", "Complete daily activities", "Social engagement"],
                    "measurements": ["Activity completion percentage", "Energy level ratings", "Social contact frequency"],
                    "timeline": "6 weeks"
                },
                "cognitive_restructuring": {
                    "title": "Challenge Negative Thinking",
                    "description": "Develop balanced, realistic thinking patterns",
                    "behaviors": ["Daily thought records", "Challenge automatic thoughts", "Practice balanced thinking"],
                    "measurements": ["Thought record completion", "Cognitive flexibility scores", "Belief conviction ratings"],
                    "timeline": "10 weeks"
                }
            },
            
            "anxiety_goals": {
                "exposure_progression": {
                    "title": "Reduce Avoidance Behaviors",
                    "description": "Gradually face feared situations to reduce anxiety",
                    "behaviors": ["Complete exposure exercises", "Reduce safety behaviors", "Practice coping skills"],
                    "measurements": ["Anxiety ratings during exposure", "Avoidance frequency", "Confidence levels"],
                    "timeline": "12 weeks"
                },
                "anxiety_management": {
                    "title": "Develop Anxiety Coping Skills",
                    "description": "Learn and practice effective anxiety management techniques",
                    "behaviors": ["Practice relaxation techniques", "Use grounding skills", "Apply coping strategies"],
                    "measurements": ["Anxiety episode frequency", "Coping skill usage", "Recovery time"],
                    "timeline": "8 weeks"
                }
            },
            
            "relationship_goals": {
                "communication_skills": {
                    "title": "Improve Communication",
                    "description": "Develop effective interpersonal communication skills",
                    "behaviors": ["Practice assertive communication", "Active listening", "Express needs clearly"],
                    "measurements": ["Communication effectiveness ratings", "Conflict resolution success", "Relationship satisfaction"],
                    "timeline": "10 weeks"
                },
                "boundary_setting": {
                    "title": "Establish Healthy Boundaries",
                    "description": "Learn to set and maintain appropriate personal boundaries",
                    "behaviors": ["Identify boundary violations", "Practice saying no", "Communicate limits clearly"],
                    "measurements": ["Boundary maintenance frequency", "Comfort level ratings", "Relationship quality"],
                    "timeline": "8 weeks"
                }
            }
        }
    
    def _initialize_measurement_frameworks(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "behavioral_tracking": {
                "frequency_count": "Count number of times behavior occurs",
                "duration_tracking": "Measure how long behavior lasts",
                "intensity_rating": "Rate intensity of behavior 1-10",
                "completion_percentage": "Percentage of planned behaviors completed"
            },
            
            "emotional_tracking": {
                "mood_ratings": "Daily mood ratings 1-10 scale",
                "emotion_frequency": "How often specific emotions occur",
                "emotional_intensity": "Strength of emotional experiences 1-10",
                "emotional_duration": "How long emotions last"
            },
            
            "cognitive_tracking": {
                "thought_frequency": "Number of negative thoughts per day",
                "belief_conviction": "How strongly patient believes thoughts 0-100%",
                "cognitive_flexibility": "Ability to generate alternative thoughts",
                "insight_level": "Understanding of thought patterns 1-10"
            },
            
            "functional_tracking": {
                "activity_completion": "Percentage of planned activities completed",
                "social_engagement": "Frequency of social interactions",
                "work_performance": "Job or school performance ratings",
                "self_care_behaviors": "Completion of self-care activities"
            }
        }
    
    def create_session_goals(self, session_id: str, patient_id: str, 
                           session_focus: str, time_available: int) -> List[SessionGoal]:
        
        session_goals = []
        
        focus_mappings = {
            "cognitive_restructuring": [
                {
                    "description": "Identify and challenge automatic negative thoughts",
                    "criteria": ["Complete thought record", "Generate balanced alternative", "Practice new thinking"],
                    "time": 20
                },
                {
                    "description": "Practice cognitive restructuring technique",
                    "criteria": ["Apply technique to current situation", "Demonstrate understanding", "Plan homework"],
                    "time": 15
                }
            ],
            
            "behavioral_activation": [
                {
                    "description": "Schedule pleasant and meaningful activities",
                    "criteria": ["Identify 3 pleasant activities", "Schedule specific times", "Address barriers"],
                    "time": 20
                },
                {
                    "description": "Review activity completion and mood connection",
                    "criteria": ["Discuss completed activities", "Identify mood changes", "Plan next week"],
                    "time": 15
                }
            ],
            
            "exposure_therapy": [
                {
                    "description": "Complete exposure exercise",
                    "criteria": ["Face feared situation", "Stay until anxiety decreases", "Process experience"],
                    "time": 25
                },
                {
                    "description": "Plan next exposure step",
                    "criteria": ["Identify next hierarchy item", "Prepare coping strategies", "Set timeline"],
                    "time": 10
                }
            ],
            
            "interpersonal_skills": [
                {
                    "description": "Practice assertive communication skills",
                    "criteria": ["Role-play difficult conversation", "Use assertiveness techniques", "Plan real-world application"],
                    "time": 20
                },
                {
                    "description": "Address relationship conflict",
                    "criteria": ["Identify communication patterns", "Practice new responses", "Develop action plan"],
                    "time": 20
                }
            ]
        }
        
        goal_templates = focus_mappings.get(session_focus, [])
        
        for template in goal_templates:
            if time_available >= template["time"]:
                goal = SessionGoal(
                    session_id=session_id,
                    patient_id=patient_id,
                    goal_description=template["description"],
                    success_criteria=template["criteria"],
                    time_allocation=template["time"]
                )
                session_goals.append(goal)
                time_available -= template["time"]
        
        return session_goals
    
    def create_treatment_goal(self, patient_id: str, goal_category: str, 
                            specific_focus: str, patient_input: Dict[str, Any]) -> TherapeuticGoal:
        
        goal_id = f"{patient_id}_{goal_category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        template = self.goal_templates.get(goal_category, {}).get(specific_focus, {})
        
        if not template:
            template = {
                "title": f"Custom {goal_category} Goal",
                "description": "Patient-specific therapeutic goal",
                "behaviors": ["To be determined with patient"],
                "measurements": ["Progress ratings", "Patient self-report"],
                "timeline": "12 weeks"
            }
        
        goal = TherapeuticGoal(
            goal_id=goal_id,
            patient_id=patient_id,
            goal_type=GoalType.TREATMENT_GOAL,
            title=patient_input.get("title", template["title"]),
            description=patient_input.get("description", template["description"]),
            specific_behaviors=patient_input.get("behaviors", template["behaviors"]),
            measurement_criteria=patient_input.get("measurements", template["measurements"]),
            target_date=self._calculate_target_date(template.get("timeline", "12 weeks")),
            priority_level=PriorityLevel(patient_input.get("priority", "medium")),
            intervention_strategies=patient_input.get("strategies", []),
            milestone_markers=self._create_milestones(template["timeline"])
        )
        
        self._save_therapeutic_goal(goal)
        return goal
    
    def _calculate_target_date(self, timeline_str: str) -> datetime:
        
        if "week" in timeline_str:
            weeks = int(timeline_str.split()[0])
            return datetime.now() + timedelta(weeks=weeks)
        elif "month" in timeline_str:
            months = int(timeline_str.split()[0])
            return datetime.now() + timedelta(days=months * 30)
        else:
            return datetime.now() + timedelta(weeks=12)
    
    def _create_milestones(self, timeline: str) -> List[str]:
        
        if "week" in timeline:
            weeks = int(timeline.split()[0])
            milestones = []
            
            if weeks >= 4:
                milestones.append(f"25% progress by week {weeks//4}")
            if weeks >= 8:
                milestones.append(f"50% progress by week {weeks//2}")
            if weeks >= 12:
                milestones.append(f"75% progress by week {3*weeks//4}")
            
            milestones.append(f"Goal completion by week {weeks}")
            return milestones
        
        return ["Regular progress review", "Goal completion"]
    
    def set_smart_goals(self, patient_id: str, goal_area: str, patient_preferences: Dict[str, Any]) -> TherapeuticGoal:
        
        smart_framework = {
            "specific": patient_preferences.get("specific_target", ""),
            "measurable": patient_preferences.get("measurement_method", ""),
            "achievable": patient_preferences.get("realistic_steps", ""),
            "relevant": patient_preferences.get("personal_importance", ""),
            "time_bound": patient_preferences.get("target_timeline", "")
        }
        
        goal_id = f"{patient_id}_smart_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        goal = TherapeuticGoal(
            goal_id=goal_id,
            patient_id=patient_id,
            goal_type=GoalType.TREATMENT_GOAL,
            title=f"SMART Goal: {smart_framework['specific']}",
            description=f"Achieve {smart_framework['specific']} within {smart_framework['time_bound']}",
            specific_behaviors=[smart_framework["achievable"]],
            measurement_criteria=[smart_framework["measurable"]],
            target_date=self._parse_timeline(smart_framework["time_bound"]),
            notes=f"Relevance: {smart_framework['relevant']}"
        )
        
        self._save_therapeutic_goal(goal)
        return goal
    
    def _parse_timeline(self, timeline_str: str) -> datetime:
        
        timeline_lower = timeline_str.lower()
        
        if "week" in timeline_lower:
            weeks = 1
            for word in timeline_lower.split():
                if word.isdigit():
                    weeks = int(word)
                    break
            return datetime.now() + timedelta(weeks=weeks)
        
        elif "month" in timeline_lower:
            months = 1
            for word in timeline_lower.split():
                if word.isdigit():
                    months = int(word)
                    break
            return datetime.now() + timedelta(days=months * 30)
        
        else:
            return datetime.now() + timedelta(weeks=8)
    
    def track_goal_progress(self, goal_id: str, session_date: datetime, 
                          progress_data: Dict[str, Any]) -> GoalProgress:
        
        progress = GoalProgress(
            goal_id=goal_id,
            session_date=session_date,
            progress_rating=progress_data.get("rating", 0),
            progress_description=progress_data.get("description", ""),
            obstacles_encountered=progress_data.get("obstacles", []),
            strategies_used=progress_data.get("strategies", []),
            next_steps=progress_data.get("next_steps", []),
            therapist_observations=progress_data.get("therapist_notes", ""),
            patient_feedback=progress_data.get("patient_feedback", "")
        )
        
        self._save_goal_progress(progress)
        self._update_goal_progress_percentage(goal_id, progress_data.get("rating", 0))
        
        return progress
    
    def _update_goal_progress_percentage(self, goal_id: str, latest_rating: int):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT progress_rating FROM goal_progress 
                WHERE goal_id = ? 
                ORDER BY session_date DESC 
                LIMIT 5
            """, (goal_id,))
            
            recent_ratings = [row[0] for row in cursor.fetchall()]
            
            if recent_ratings:
                avg_progress = sum(recent_ratings) / len(recent_ratings)
                progress_percentage = min(int(avg_progress * 10), 100)
                
                cursor.execute("""
                    UPDATE therapeutic_goals 
                    SET progress_percentage = ?, last_updated = ?
                    WHERE goal_id = ?
                """, (progress_percentage, datetime.now().isoformat(), goal_id))
    
    def review_session_goal_achievement(self, session_id: str, patient_id: str) -> Dict[str, Any]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT goal_description, success_criteria, achieved, progress_notes
                FROM session_goals
                WHERE session_id = ? AND patient_id = ?
            """, (session_id, patient_id))
            
            goals = cursor.fetchall()
        
        review_summary = {
            "total_goals": len(goals),
            "achieved_goals": 0,
            "partially_achieved": 0,
            "not_achieved": 0,
            "goal_details": [],
            "overall_success_rate": 0
        }
        
        for goal_desc, criteria_json, achieved, notes in goals:
            criteria = json.loads(criteria_json) if criteria_json else []
            
            goal_detail = {
                "description": goal_desc,
                "success_criteria": criteria,
                "achieved": achieved,
                "notes": notes
            }
            
            review_summary["goal_details"].append(goal_detail)
            
            if achieved:
                review_summary["achieved_goals"] += 1
            elif notes and "partial" in notes.lower():
                review_summary["partially_achieved"] += 1
            else:
                review_summary["not_achieved"] += 1
        
        if review_summary["total_goals"] > 0:
            review_summary["overall_success_rate"] = round(
                (review_summary["achieved_goals"] / review_summary["total_goals"]) * 100, 1
            )
        
        return review_summary
    
    def generate_goal_recommendations(self, patient_id: str, current_concerns: List[str], 
                                    therapy_modality: str) -> List[Dict[str, Any]]:
        
        recommendations = []
        
        concern_mappings = {
            "depression": ["mood_improvement", "behavioral_activation", "cognitive_restructuring"],
            "anxiety": ["exposure_progression", "anxiety_management", "relaxation_skills"],
            "relationships": ["communication_skills", "boundary_setting", "conflict_resolution"],
            "trauma": ["safety_stabilization", "trauma_processing", "integration_work"],
            "anger": ["anger_management", "trigger_identification", "coping_strategies"]
        }
        
        modality_priorities = {
            "CBT": ["cognitive_restructuring", "behavioral_activation", "exposure_progression"],
            "DBT": ["emotion_regulation", "distress_tolerance", "interpersonal_effectiveness"],
            "Psychodynamic": ["pattern_recognition", "insight_development", "relationship_exploration"]
        }
        
        for concern in current_concerns:
            goal_types = concern_mappings.get(concern.lower(), [])
            
            for goal_type in goal_types:
                if goal_type in modality_priorities.get(therapy_modality, []):
                    priority = PriorityLevel.HIGH
                else:
                    priority = PriorityLevel.MEDIUM
                
                recommendation = {
                    "goal_area": concern,
                    "goal_type": goal_type,
                    "priority": priority.value,
                    "rationale": f"Addresses {concern} using {therapy_modality} approach",
                    "estimated_timeline": "8-12 weeks"
                }
                
                recommendations.append(recommendation)
        
        return recommendations[:5]
    
    def prioritize_goals(self, patient_id: str, safety_concerns: List[str], 
                        functional_impairment: str) -> List[str]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT goal_id, title, priority_level, goal_type, status
                FROM therapeutic_goals
                WHERE patient_id = ? AND status != 'achieved'
                ORDER BY created_date
            """, (patient_id,))
            
            goals = cursor.fetchall()
        
        priority_order = []
        
        for goal_id, title, priority, goal_type, status in goals:
            priority_score = 0
            
            if any(concern in title.lower() for concern in safety_concerns):
                priority_score += 100
            
            if functional_impairment == "severe" and "functional" in goal_type:
                priority_score += 50
            
            if priority == "urgent":
                priority_score += 40
            elif priority == "high":
                priority_score += 30
            elif priority == "medium":
                priority_score += 20
            
            if status == "in_progress":
                priority_score += 15
            
            priority_order.append((goal_id, priority_score))
        
        priority_order.sort(key=lambda x: x[1], reverse=True)
        
        return [goal_id for goal_id, score in priority_order]
    
    def _save_therapeutic_goal(self, goal: TherapeuticGoal):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO therapeutic_goals
                (goal_id, patient_id, goal_type, title, description, specific_behaviors,
                 measurement_criteria, target_date, priority_level, status, progress_percentage,
                 barriers, resources_needed, intervention_strategies, milestone_markers,
                 created_date, last_updated, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                goal.goal_id, goal.patient_id, goal.goal_type.value, goal.title,
                goal.description, json.dumps(goal.specific_behaviors),
                json.dumps(goal.measurement_criteria),
                goal.target_date.isoformat() if goal.target_date else None,
                goal.priority_level.value, goal.status.value, goal.progress_percentage,
                json.dumps(goal.barriers), json.dumps(goal.resources_needed),
                json.dumps(goal.intervention_strategies), json.dumps(goal.milestone_markers),
                goal.created_date.isoformat(), goal.last_updated.isoformat(), goal.notes
            ))
    
    def _save_session_goal(self, goal: SessionGoal):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO session_goals
                (session_id, patient_id, goal_description, success_criteria, time_allocation,
                 related_treatment_goals, priority, achieved, progress_notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                goal.session_id, goal.patient_id, goal.goal_description,
                json.dumps(goal.success_criteria), goal.time_allocation,
                json.dumps(goal.related_treatment_goals), goal.priority.value,
                goal.achieved, goal.progress_notes, goal.created_at.isoformat()
            ))
    
    def _save_goal_progress(self, progress: GoalProgress):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO goal_progress
                (goal_id, session_date, progress_rating, progress_description,
                 obstacles_encountered, strategies_used, next_steps,
                 therapist_observations, patient_feedback)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                progress.goal_id, progress.session_date.isoformat(),
                progress.progress_rating, progress.progress_description,
                json.dumps(progress.obstacles_encountered),
                json.dumps(progress.strategies_used),
                json.dumps(progress.next_steps),
                progress.therapist_observations, progress.patient_feedback
            ))


if __name__ == "__main__":
    goal_setter = SessionGoalSetting()
    
    session_goals = goal_setter.create_session_goals(
        session_id="session_001",
        patient_id="patient_123",
        session_focus="cognitive_restructuring",
        time_available=45
    )
    
    print("=== SESSION GOALS ===")
    for goal in session_goals:
        print(f"Goal: {goal.goal_description}")
        print(f"Time: {goal.time_allocation} minutes")
        print(f"Success criteria: {goal.success_criteria}")
        print()
    
    patient_input = {
        "title": "Reduce Social Anxiety",
        "description": "Feel more comfortable in social situations",
        "behaviors": ["Practice small talk", "Attend social events", "Use coping skills"],
        "measurements": ["Anxiety ratings 1-10", "Social events attended", "Confidence levels"],
        "priority": "high"
    }
    
    treatment_goal = goal_setter.create_treatment_goal(
        patient_id="patient_123",
        goal_category="anxiety_goals",
        specific_focus="exposure_progression",
        patient_input=patient_input
    )
    
    print("=== TREATMENT GOAL ===")
    print(f"Title: {treatment_goal.title}")
    print(f"Target Date: {treatment_goal.target_date}")
    print(f"Behaviors: {treatment_goal.specific_behaviors}")
    print(f"Measurements: {treatment_goal.measurement_criteria}")
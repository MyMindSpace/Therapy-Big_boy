"""
Activity Scheduling Module

Implements behavioral activation techniques for depression treatment.
Provides tools for activity planning, mood monitoring, and behavioral change.
"""

import sqlite3
from datetime import datetime, timedelta, time
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, asdict
import json

from config.therapy_protocols import TherapyModality, InterventionType


class ActivityType(Enum):
    """Types of activities for scheduling"""
    PLEASANT = "pleasant"  # Activities for enjoyment/pleasure
    MASTERY = "mastery"    # Activities for accomplishment/competence
    ROUTINE = "routine"    # Daily living activities
    SOCIAL = "social"      # Social connection activities
    PHYSICAL = "physical"  # Exercise and movement
    CREATIVE = "creative"  # Creative expression
    SELF_CARE = "self_care" # Personal care activities
    SPIRITUAL = "spiritual" # Meaning/spiritual activities


class MoodRating(Enum):
    """Mood rating scale (1-10)"""
    VERY_LOW = 1
    LOW = 2
    BELOW_AVERAGE = 3
    SLIGHTLY_LOW = 4
    NEUTRAL = 5
    SLIGHTLY_GOOD = 6
    GOOD = 7
    VERY_GOOD = 8
    EXCELLENT = 9
    EXCEPTIONAL = 10


class ActivityStatus(Enum):
    """Status of scheduled activities"""
    PLANNED = "planned"
    COMPLETED = "completed"
    PARTIALLY_COMPLETED = "partially_completed"
    SKIPPED = "skipped"
    RESCHEDULED = "rescheduled"


@dataclass
class Activity:
    """Individual activity definition"""
    activity_id: str
    name: str
    description: str
    activity_type: ActivityType
    estimated_duration: int  # minutes
    difficulty_level: int  # 1-5 scale
    pleasure_rating: Optional[int] = None  # 1-10 scale
    mastery_rating: Optional[int] = None  # 1-10 scale
    required_materials: List[str] = None
    location: str = ""
    notes: str = ""
    
    def __post_init__(self):
        if self.required_materials is None:
            self.required_materials = []


@dataclass
class ScheduledActivity:
    """Scheduled instance of an activity"""
    schedule_id: str
    activity_id: str
    patient_id: str
    scheduled_date: datetime
    scheduled_time: time
    duration_minutes: int
    
    status: ActivityStatus
    actual_start_time: Optional[datetime] = None
    actual_duration: Optional[int] = None
    
    # Mood ratings
    mood_before: Optional[int] = None  # 1-10 scale
    mood_after: Optional[int] = None   # 1-10 scale
    
    # Experience ratings
    pleasure_experienced: Optional[int] = None  # 1-10 scale
    mastery_experienced: Optional[int] = None   # 1-10 scale
    energy_level: Optional[int] = None          # 1-10 scale
    
    completion_notes: str = ""
    barriers_encountered: List[str] = None
    created_date: datetime = None
    
    def __post_init__(self):
        if self.barriers_encountered is None:
            self.barriers_encountered = []
        if self.created_date is None:
            self.created_date = datetime.now()


@dataclass
class ActivityPlan:
    """Weekly activity plan"""
    plan_id: str
    patient_id: str
    week_start_date: datetime
    treatment_goals: List[str]
    scheduled_activities: List[ScheduledActivity]
    weekly_targets: Dict[str, int]  # activity_type: target_count
    
    created_date: datetime
    last_updated: datetime
    notes: str = ""


class ActivityScheduler:
    """
    Manages activity scheduling and behavioral activation interventions.
    """
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self._initialize_database()
        self._load_default_activities()
    
    def _initialize_database(self):
        """Initialize activity scheduling tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Activity library table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_library (
                    activity_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    activity_type TEXT NOT NULL,
                    estimated_duration INTEGER,
                    difficulty_level INTEGER,
                    pleasure_rating INTEGER,
                    mastery_rating INTEGER,
                    required_materials TEXT,
                    location TEXT,
                    notes TEXT,
                    is_default BOOLEAN DEFAULT FALSE
                )
            """)
            
            # Scheduled activities table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scheduled_activities (
                    schedule_id TEXT PRIMARY KEY,
                    activity_id TEXT NOT NULL,
                    patient_id TEXT NOT NULL,
                    scheduled_date DATE NOT NULL,
                    scheduled_time TIME NOT NULL,
                    duration_minutes INTEGER,
                    status TEXT NOT NULL,
                    actual_start_time TIMESTAMP,
                    actual_duration INTEGER,
                    mood_before INTEGER,
                    mood_after INTEGER,
                    pleasure_experienced INTEGER,
                    mastery_experienced INTEGER,
                    energy_level INTEGER,
                    completion_notes TEXT,
                    barriers_encountered TEXT,
                    created_date TIMESTAMP,
                    FOREIGN KEY (activity_id) REFERENCES activity_library (activity_id),
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            # Activity plans table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_plans (
                    plan_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    week_start_date DATE NOT NULL,
                    treatment_goals TEXT,
                    weekly_targets TEXT,
                    created_date TIMESTAMP,
                    last_updated TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            # Activity completion tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_tracking (
                    tracking_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    tracking_date DATE NOT NULL,
                    total_activities_planned INTEGER DEFAULT 0,
                    total_activities_completed INTEGER DEFAULT 0,
                    average_mood_before REAL,
                    average_mood_after REAL,
                    average_pleasure REAL,
                    average_mastery REAL,
                    daily_notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            conn.commit()
    
    def _load_default_activities(self):
        """Load default activity library"""
        default_activities = [
            # Pleasant Activities
            Activity("act_001", "Take a warm bath", "Relaxing bath with favorite products", 
                    ActivityType.PLEASANT, 30, 1, 7, 3, ["bath products", "towel"]),
            Activity("act_002", "Listen to favorite music", "Play uplifting or calming music", 
                    ActivityType.PLEASANT, 20, 1, 8, 2, ["music player/app"]),
            Activity("act_003", "Watch a favorite movie", "Enjoyable movie or TV show", 
                    ActivityType.PLEASANT, 120, 1, 7, 2, ["TV/device"]),
            Activity("act_004", "Call a friend", "Social connection with supportive friend", 
                    ActivityType.SOCIAL, 30, 2, 6, 4, ["phone"]),
            Activity("act_005", "Read a book", "Engaging book or magazine", 
                    ActivityType.PLEASANT, 45, 2, 6, 5, ["book/e-reader"]),
            
            # Mastery Activities
            Activity("act_006", "Organize a room", "Clean and organize living space", 
                    ActivityType.MASTERY, 60, 3, 4, 8, ["cleaning supplies"]),
            Activity("act_007", "Learn something new", "Online course, tutorial, or skill practice", 
                    ActivityType.MASTERY, 45, 4, 5, 8, ["computer/materials"]),
            Activity("act_008", "Cook a healthy meal", "Prepare nutritious meal from scratch", 
                    ActivityType.MASTERY, 60, 3, 6, 7, ["ingredients", "cooking utensils"]),
            Activity("act_009", "Exercise routine", "Planned physical exercise", 
                    ActivityType.PHYSICAL, 30, 3, 5, 8, ["workout clothes", "equipment"]),
            Activity("act_010", "Complete work project", "Make progress on important task", 
                    ActivityType.MASTERY, 90, 4, 3, 9, ["work materials"]),
            
            # Routine Activities
            Activity("act_011", "Morning routine", "Consistent morning self-care", 
                    ActivityType.ROUTINE, 45, 2, 5, 6, ["toiletries"]),
            Activity("act_012", "Grocery shopping", "Plan and shop for weekly groceries", 
                    ActivityType.ROUTINE, 60, 2, 3, 6, ["shopping list", "money/card"]),
            Activity("act_013", "Household maintenance", "Basic home upkeep tasks", 
                    ActivityType.ROUTINE, 30, 2, 3, 6, ["tools", "supplies"]),
            
            # Social Activities
            Activity("act_014", "Meet friend for coffee", "Social connection over coffee/tea", 
                    ActivityType.SOCIAL, 90, 3, 7, 5, ["money"]),
            Activity("act_015", "Join group activity", "Participate in hobby or interest group", 
                    ActivityType.SOCIAL, 120, 4, 6, 6, ["materials for activity"]),
            Activity("act_016", "Family time", "Quality time with family members", 
                    ActivityType.SOCIAL, 60, 2, 7, 4, []),
            
            # Creative Activities
            Activity("act_017", "Art/Drawing", "Creative expression through visual art", 
                    ActivityType.CREATIVE, 60, 3, 8, 6, ["art supplies"]),
            Activity("act_018", "Write in journal", "Reflective writing or creative writing", 
                    ActivityType.CREATIVE, 30, 2, 6, 7, ["journal", "pen"]),
            Activity("act_019", "Photography", "Take photos of interesting subjects", 
                    ActivityType.CREATIVE, 45, 2, 7, 5, ["camera/phone"]),
            
            # Self-Care Activities
            Activity("act_020", "Meditation/Mindfulness", "Mindfulness or meditation practice", 
                    ActivityType.SELF_CARE, 20, 2, 6, 7, ["quiet space"]),
            Activity("act_021", "Skincare routine", "Self-care focused on appearance", 
                    ActivityType.SELF_CARE, 15, 1, 6, 5, ["skincare products"]),
            Activity("act_022", "Yoga/Stretching", "Gentle movement and flexibility", 
                    ActivityType.PHYSICAL, 30, 2, 6, 6, ["yoga mat", "comfortable clothes"]),
        ]
        
        # Check if default activities already exist
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM activity_library WHERE is_default = TRUE")
            count = cursor.fetchone()[0]
            
            if count == 0:  # Load defaults if not already present
                for activity in default_activities:
                    self._save_activity(activity, is_default=True)
    
    def _save_activity(self, activity: Activity, is_default: bool = False):
        """Save activity to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO activity_library (
                    activity_id, name, description, activity_type,
                    estimated_duration, difficulty_level, pleasure_rating,
                    mastery_rating, required_materials, location, notes, is_default
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                activity.activity_id, activity.name, activity.description,
                activity.activity_type.value, activity.estimated_duration,
                activity.difficulty_level, activity.pleasure_rating,
                activity.mastery_rating, json.dumps(activity.required_materials),
                activity.location, activity.notes, is_default
            ))
            conn.commit()
    
    def get_activity_suggestions(
        self, 
        patient_id: str,
        activity_types: List[ActivityType] = None,
        max_difficulty: int = 5,
        max_duration: int = 120
    ) -> List[Activity]:
        """Get personalized activity suggestions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Build query based on filters
            query = """
                SELECT * FROM activity_library 
                WHERE difficulty_level <= ? AND estimated_duration <= ?
            """
            params = [max_difficulty, max_duration]
            
            if activity_types:
                type_placeholders = ','.join(['?' for _ in activity_types])
                query += f" AND activity_type IN ({type_placeholders})"
                params.extend([t.value for t in activity_types])
            
            query += " ORDER BY pleasure_rating DESC, mastery_rating DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            activities = []
            for row in rows:
                activity = Activity(
                    activity_id=row[0],
                    name=row[1],
                    description=row[2],
                    activity_type=ActivityType(row[3]),
                    estimated_duration=row[4],
                    difficulty_level=row[5],
                    pleasure_rating=row[6],
                    mastery_rating=row[7],
                    required_materials=json.loads(row[8] or '[]'),
                    location=row[9] or "",
                    notes=row[10] or ""
                )
                activities.append(activity)
            
            return activities
    
    def create_weekly_plan(
        self, 
        patient_id: str,
        week_start_date: datetime,
        treatment_goals: List[str],
        preferences: Dict[str, Any] = None
    ) -> ActivityPlan:
        """Create a weekly activity plan"""
        plan_id = f"plan_{patient_id}_{week_start_date.strftime('%Y%m%d')}"
        
        # Set default preferences if not provided
        if preferences is None:
            preferences = {
                'pleasant_activities_per_day': 2,
                'mastery_activities_per_day': 1,
                'preferred_activity_types': [ActivityType.PLEASANT, ActivityType.MASTERY],
                'max_difficulty': 3,
                'max_duration_per_activity': 90,
                'preferred_times': ['morning', 'afternoon', 'evening']
            }
        
        # Calculate weekly targets
        weekly_targets = {
            ActivityType.PLEASANT.value: preferences.get('pleasant_activities_per_day', 2) * 7,
            ActivityType.MASTERY.value: preferences.get('mastery_activities_per_day', 1) * 7,
            ActivityType.SOCIAL.value: 3,
            ActivityType.PHYSICAL.value: 4,
            ActivityType.ROUTINE.value: 7
        }
        
        # Get suggested activities
        suggested_activities = self.get_activity_suggestions(
            patient_id=patient_id,
            activity_types=preferences.get('preferred_activity_types'),
            max_difficulty=preferences.get('max_difficulty', 5),
            max_duration=preferences.get('max_duration_per_activity', 120)
        )
        
        # Create scheduled activities for the week
        scheduled_activities = self._generate_weekly_schedule(
            patient_id=patient_id,
            week_start_date=week_start_date,
            activities=suggested_activities,
            weekly_targets=weekly_targets,
            preferences=preferences
        )
        
        plan = ActivityPlan(
            plan_id=plan_id,
            patient_id=patient_id,
            week_start_date=week_start_date,
            treatment_goals=treatment_goals,
            scheduled_activities=scheduled_activities,
            weekly_targets=weekly_targets,
            created_date=datetime.now(),
            last_updated=datetime.now()
        )
        
        self._save_activity_plan(plan)
        return plan
    
    def _generate_weekly_schedule(
        self,
        patient_id: str,
        week_start_date: datetime,
        activities: List[Activity],
        weekly_targets: Dict[str, int],
        preferences: Dict[str, Any]
    ) -> List[ScheduledActivity]:
        """Generate scheduled activities for a week"""
        scheduled_activities = []
        
        # Time slots for scheduling
        time_slots = {
            'morning': time(9, 0),
            'afternoon': time(14, 0),
            'evening': time(18, 0)
        }
        
        # Distribute activities across the week
        for day_offset in range(7):
            current_date = week_start_date + timedelta(days=day_offset)
            
            # Schedule pleasant activities
            pleasant_count = preferences.get('pleasant_activities_per_day', 2)
            pleasant_activities = [a for a in activities if a.activity_type == ActivityType.PLEASANT]
            
            for i in range(min(pleasant_count, len(pleasant_activities))):
                activity = pleasant_activities[i % len(pleasant_activities)]
                
                schedule_id = f"sched_{patient_id}_{current_date.strftime('%Y%m%d')}_{i}_pleasant"
                scheduled_time = time_slots['afternoon']  # Default to afternoon
                
                scheduled_activity = ScheduledActivity(
                    schedule_id=schedule_id,
                    activity_id=activity.activity_id,
                    patient_id=patient_id,
                    scheduled_date=current_date,
                    scheduled_time=scheduled_time,
                    duration_minutes=activity.estimated_duration,
                    status=ActivityStatus.PLANNED
                )
                scheduled_activities.append(scheduled_activity)
            
            # Schedule mastery activities
            mastery_count = preferences.get('mastery_activities_per_day', 1)
            mastery_activities = [a for a in activities if a.activity_type == ActivityType.MASTERY]
            
            for i in range(min(mastery_count, len(mastery_activities))):
                activity = mastery_activities[i % len(mastery_activities)]
                
                schedule_id = f"sched_{patient_id}_{current_date.strftime('%Y%m%d')}_{i}_mastery"
                scheduled_time = time_slots['morning']  # Default to morning
                
                scheduled_activity = ScheduledActivity(
                    schedule_id=schedule_id,
                    activity_id=activity.activity_id,
                    patient_id=patient_id,
                    scheduled_date=current_date,
                    scheduled_time=scheduled_time,
                    duration_minutes=activity.estimated_duration,
                    status=ActivityStatus.PLANNED
                )
                scheduled_activities.append(scheduled_activity)
        
        return scheduled_activities
    
    def _save_activity_plan(self, plan: ActivityPlan):
        """Save activity plan to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Save plan
            cursor.execute("""
                INSERT OR REPLACE INTO activity_plans (
                    plan_id, patient_id, week_start_date, treatment_goals,
                    weekly_targets, created_date, last_updated, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plan.plan_id, plan.patient_id, plan.week_start_date.date(),
                json.dumps(plan.treatment_goals), json.dumps(plan.weekly_targets),
                plan.created_date, plan.last_updated, plan.notes
            ))
            
            # Save scheduled activities
            for activity in plan.scheduled_activities:
                self._save_scheduled_activity(activity)
            
            conn.commit()
    
    def _save_scheduled_activity(self, scheduled_activity: ScheduledActivity):
        """Save scheduled activity to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO scheduled_activities (
                    schedule_id, activity_id, patient_id, scheduled_date,
                    scheduled_time, duration_minutes, status, actual_start_time,
                    actual_duration, mood_before, mood_after, pleasure_experienced,
                    mastery_experienced, energy_level, completion_notes,
                    barriers_encountered, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                scheduled_activity.schedule_id, scheduled_activity.activity_id,
                scheduled_activity.patient_id, scheduled_activity.scheduled_date.date(),
                scheduled_activity.scheduled_time, scheduled_activity.duration_minutes,
                scheduled_activity.status.value, scheduled_activity.actual_start_time,
                scheduled_activity.actual_duration, scheduled_activity.mood_before,
                scheduled_activity.mood_after, scheduled_activity.pleasure_experienced,
                scheduled_activity.mastery_experienced, scheduled_activity.energy_level,
                scheduled_activity.completion_notes, json.dumps(scheduled_activity.barriers_encountered),
                scheduled_activity.created_date
            ))
            conn.commit()
    
    def record_activity_completion(
        self,
        schedule_id: str,
        status: ActivityStatus,
        mood_before: int,
        mood_after: int,
        pleasure_experienced: int,
        mastery_experienced: int,
        energy_level: int,
        actual_duration: int = None,
        notes: str = "",
        barriers: List[str] = None
    ) -> bool:
        """Record completion of scheduled activity"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Update scheduled activity
            cursor.execute("""
                UPDATE scheduled_activities 
                SET status = ?, actual_start_time = ?, actual_duration = ?,
                    mood_before = ?, mood_after = ?, pleasure_experienced = ?,
                    mastery_experienced = ?, energy_level = ?, completion_notes = ?,
                    barriers_encountered = ?
                WHERE schedule_id = ?
            """, (
                status.value, datetime.now(), actual_duration,
                mood_before, mood_after, pleasure_experienced,
                mastery_experienced, energy_level, notes,
                json.dumps(barriers or []), schedule_id
            ))
            
            if cursor.rowcount > 0:
                conn.commit()
                
                # Update daily tracking
                cursor.execute("""
                    SELECT patient_id, scheduled_date FROM scheduled_activities 
                    WHERE schedule_id = ?
                """, (schedule_id,))
                result = cursor.fetchone()
                
                if result:
                    patient_id, scheduled_date = result
                    self._update_daily_tracking(patient_id, scheduled_date)
                
                return True
            return False
    
    def _update_daily_tracking(self, patient_id: str, tracking_date: str):
        """Update daily activity tracking summary"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Calculate daily statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_planned,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as total_completed,
                    AVG(CASE WHEN mood_before IS NOT NULL THEN mood_before END) as avg_mood_before,
                    AVG(CASE WHEN mood_after IS NOT NULL THEN mood_after END) as avg_mood_after,
                    AVG(CASE WHEN pleasure_experienced IS NOT NULL THEN pleasure_experienced END) as avg_pleasure,
                    AVG(CASE WHEN mastery_experienced IS NOT NULL THEN mastery_experienced END) as avg_mastery
                FROM scheduled_activities 
                WHERE patient_id = ? AND scheduled_date = ?
            """, (patient_id, tracking_date))
            
            stats = cursor.fetchone()
            
            tracking_id = f"track_{patient_id}_{tracking_date}"
            
            cursor.execute("""
                INSERT OR REPLACE INTO activity_tracking (
                    tracking_id, patient_id, tracking_date, total_activities_planned,
                    total_activities_completed, average_mood_before, average_mood_after,
                    average_pleasure, average_mastery
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tracking_id, patient_id, tracking_date, stats[0], stats[1],
                stats[2], stats[3], stats[4], stats[5]
            ))
            
            conn.commit()
    
    def get_weekly_plan(self, patient_id: str, week_start_date: datetime) -> Optional[ActivityPlan]:
        """Retrieve weekly activity plan"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM activity_plans 
                WHERE patient_id = ? AND week_start_date = ?
            """, (patient_id, week_start_date.date()))
            
            plan_data = cursor.fetchone()
            if not plan_data:
                return None
            
            # Get scheduled activities
            cursor.execute("""
                SELECT * FROM scheduled_activities 
                WHERE patient_id = ? AND scheduled_date >= ? AND scheduled_date < ?
                ORDER BY scheduled_date, scheduled_time
            """, (patient_id, week_start_date.date(), 
                  (week_start_date + timedelta(days=7)).date()))
            
            activities_data = cursor.fetchall()
            
            return self._reconstruct_activity_plan(plan_data, activities_data)
    
    def _reconstruct_activity_plan(self, plan_data, activities_data) -> ActivityPlan:
        """Reconstruct ActivityPlan from database data"""
        scheduled_activities = []
        for row in activities_data:
            scheduled_activity = ScheduledActivity(
                schedule_id=row[0],
                activity_id=row[1],
                patient_id=row[2],
                scheduled_date=datetime.strptime(row[3], '%Y-%m-%d'),
                scheduled_time=datetime.strptime(row[4], '%H:%M:%S').time(),
                duration_minutes=row[5],
                status=ActivityStatus(row[6]),
                actual_start_time=datetime.fromisoformat(row[7]) if row[7] else None,
                actual_duration=row[8],
                mood_before=row[9],
                mood_after=row[10],
                pleasure_experienced=row[11],
                mastery_experienced=row[12],
                energy_level=row[13],
                completion_notes=row[14] or "",
                barriers_encountered=json.loads(row[15] or '[]'),
                created_date=datetime.fromisoformat(row[16])
            )
            scheduled_activities.append(scheduled_activity)
        
        return ActivityPlan(
            plan_id=plan_data[0],
            patient_id=plan_data[1],
            week_start_date=datetime.strptime(plan_data[2], '%Y-%m-%d'),
            treatment_goals=json.loads(plan_data[3] or '[]'),
            scheduled_activities=scheduled_activities,
            weekly_targets=json.loads(plan_data[4] or '{}'),
            created_date=datetime.fromisoformat(plan_data[5]),
            last_updated=datetime.fromisoformat(plan_data[6]),
            notes=plan_data[7] or ""
        )
    
    def generate_activity_report(
        self, 
        patient_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        """Generate activity completion and mood tracking report"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get activity completion statistics
            cursor.execute("""
                SELECT 
                    activity_type,
                    COUNT(*) as total_planned,
                    COUNT(CASE WHEN sa.status = 'completed' THEN 1 END) as completed,
                    AVG(CASE WHEN sa.mood_before IS NOT NULL THEN sa.mood_before END) as avg_mood_before,
                    AVG(CASE WHEN sa.mood_after IS NOT NULL THEN sa.mood_after END) as avg_mood_after,
                    AVG(CASE WHEN sa.pleasure_experienced IS NOT NULL THEN sa.pleasure_experienced END) as avg_pleasure,
                    AVG(CASE WHEN sa.mastery_experienced IS NOT NULL THEN sa.mastery_experienced END) as avg_mastery
                FROM scheduled_activities sa
                JOIN activity_library al ON sa.activity_id = al.activity_id
                WHERE sa.patient_id = ? AND sa.scheduled_date BETWEEN ? AND ?
                GROUP BY activity_type
            """, (patient_id, start_date.date(), end_date.date()))
            
            activity_stats = cursor.fetchall()
            
            # Get daily tracking data
            cursor.execute("""
                SELECT 
                    tracking_date,
                    total_activities_planned,
                    total_activities_completed,
                    average_mood_before,
                    average_mood_after,
                    average_pleasure,
                    average_mastery
                FROM activity_tracking
                WHERE patient_id = ? AND tracking_date BETWEEN ? AND ?
                ORDER BY tracking_date
            """, (patient_id, start_date.date(), end_date.date()))
            
            daily_tracking = cursor.fetchall()
            
            # Calculate overall statistics
            total_planned = sum(stat[1] for stat in activity_stats)
            total_completed = sum(stat[2] for stat in activity_stats)
            completion_rate = (total_completed / total_planned * 100) if total_planned > 0 else 0
            
            # Calculate mood improvement
            mood_improvements = []
            for day in daily_tracking:
                if day[3] and day[4]:  # Both before and after mood ratings exist
                    improvement = day[4] - day[3]
                    mood_improvements.append(improvement)
            
            avg_mood_improvement = sum(mood_improvements) / len(mood_improvements) if mood_improvements else 0
            
            # Identify most effective activities
            cursor.execute("""
                SELECT 
                    al.name,
                    al.activity_type,
                    COUNT(CASE WHEN sa.status = 'completed' THEN 1 END) as times_completed,
                    AVG(CASE WHEN sa.mood_after - sa.mood_before IS NOT NULL 
                        THEN sa.mood_after - sa.mood_before END) as avg_mood_change,
                    AVG(CASE WHEN sa.pleasure_experienced IS NOT NULL 
                        THEN sa.pleasure_experienced END) as avg_pleasure,
                    AVG(CASE WHEN sa.mastery_experienced IS NOT NULL 
                        THEN sa.mastery_experienced END) as avg_mastery
                FROM scheduled_activities sa
                JOIN activity_library al ON sa.activity_id = al.activity_id
                WHERE sa.patient_id = ? AND sa.scheduled_date BETWEEN ? AND ?
                    AND sa.status = 'completed' AND sa.mood_before IS NOT NULL 
                    AND sa.mood_after IS NOT NULL
                GROUP BY al.activity_id, al.name, al.activity_type
                HAVING COUNT(CASE WHEN sa.status = 'completed' THEN 1 END) >= 2
                ORDER BY avg_mood_change DESC
                LIMIT 5
            """, (patient_id, start_date.date(), end_date.date()))
            
            effective_activities = cursor.fetchall()
            
            # Identify patterns and barriers
            cursor.execute("""
                SELECT barriers_encountered
                FROM scheduled_activities
                WHERE patient_id = ? AND scheduled_date BETWEEN ? AND ?
                    AND barriers_encountered IS NOT NULL 
                    AND barriers_encountered != '[]'
            """, (patient_id, start_date.date(), end_date.date()))
            
            barrier_data = cursor.fetchall()
            all_barriers = []
            for row in barrier_data:
                barriers = json.loads(row[0])
                all_barriers.extend(barriers)
            
            # Count barrier frequency
            barrier_counts = {}
            for barrier in all_barriers:
                barrier_counts[barrier] = barrier_counts.get(barrier, 0) + 1
            
            most_common_barriers = sorted(barrier_counts.items(), 
                                        key=lambda x: x[1], reverse=True)[:5]
            
            report = {
                "report_period": {
                    "start_date": start_date.strftime('%Y-%m-%d'),
                    "end_date": end_date.strftime('%Y-%m-%d'),
                    "days_tracked": len(daily_tracking)
                },
                "overall_statistics": {
                    "total_activities_planned": total_planned,
                    "total_activities_completed": total_completed,
                    "completion_rate_percent": round(completion_rate, 1),
                    "average_mood_improvement": round(avg_mood_improvement, 2)
                },
                "activity_type_breakdown": [
                    {
                        "activity_type": stat[0],
                        "planned": stat[1],
                        "completed": stat[2],
                        "completion_rate": round((stat[2] / stat[1] * 100) if stat[1] > 0 else 0, 1),
                        "avg_mood_before": round(stat[3], 1) if stat[3] else None,
                        "avg_mood_after": round(stat[4], 1) if stat[4] else None,
                        "avg_pleasure_rating": round(stat[5], 1) if stat[5] else None,
                        "avg_mastery_rating": round(stat[6], 1) if stat[6] else None
                    }
                    for stat in activity_stats
                ],
                "daily_tracking": [
                    {
                        "date": day[0],
                        "activities_planned": day[1],
                        "activities_completed": day[2],
                        "completion_rate": round((day[2] / day[1] * 100) if day[1] > 0 else 0, 1),
                        "mood_before": round(day[3], 1) if day[3] else None,
                        "mood_after": round(day[4], 1) if day[4] else None,
                        "mood_change": round(day[4] - day[3], 1) if (day[3] and day[4]) else None,
                        "avg_pleasure": round(day[5], 1) if day[5] else None,
                        "avg_mastery": round(day[6], 1) if day[6] else None
                    }
                    for day in daily_tracking
                ],
                "most_effective_activities": [
                    {
                        "activity_name": activity[0],
                        "activity_type": activity[1],
                        "times_completed": activity[2],
                        "avg_mood_improvement": round(activity[3], 2),
                        "avg_pleasure_rating": round(activity[4], 1),
                        "avg_mastery_rating": round(activity[5], 1)
                    }
                    for activity in effective_activities
                ],
                "common_barriers": [
                    {"barrier": barrier[0], "frequency": barrier[1]}
                    for barrier in most_common_barriers
                ],
                "recommendations": self._generate_activity_recommendations(
                    activity_stats, effective_activities, most_common_barriers, avg_mood_improvement
                )
            }
            
            return report
    
    def _generate_activity_recommendations(
        self, 
        activity_stats: List, 
        effective_activities: List,
        common_barriers: List,
        mood_improvement: float
    ) -> List[str]:
        """Generate personalized activity recommendations"""
        recommendations = []
        
        # Completion rate recommendations
        total_planned = sum(stat[1] for stat in activity_stats)
        total_completed = sum(stat[2] for stat in activity_stats)
        completion_rate = (total_completed / total_planned * 100) if total_planned > 0 else 0
        
        if completion_rate < 50:
            recommendations.append("Consider reducing the number of planned activities or choosing easier activities to build momentum")
        elif completion_rate > 80:
            recommendations.append("Great job with activity completion! Consider adding more challenging mastery activities")
        
        # Mood improvement recommendations
        if mood_improvement > 1.0:
            recommendations.append("Excellent mood improvement from activities! Continue current activity patterns")
        elif mood_improvement > 0.5:
            recommendations.append("Good mood benefits from activities. Try increasing frequency of most effective activities")
        elif mood_improvement < 0.2:
            recommendations.append("Limited mood improvement. Consider trying different types of activities or addressing barriers")
        
        # Activity type specific recommendations
        activity_types = {stat[0]: stat for stat in activity_stats}
        
        if 'pleasant' in activity_types:
            pleasant_completion = activity_types['pleasant'][2] / activity_types['pleasant'][1] * 100
            if pleasant_completion < 60:
                recommendations.append("Increase engagement in pleasant activities - these are important for mood improvement")
        
        if 'mastery' in activity_types:
            mastery_completion = activity_types['mastery'][2] / activity_types['mastery'][1] * 100
            if mastery_completion < 40:
                recommendations.append("Break down mastery activities into smaller, more manageable steps")
        
        # Most effective activities recommendations
        if effective_activities:
            top_activity = effective_activities[0]
            recommendations.append(f"'{top_activity[0]}' shows the best mood improvement - consider scheduling this more frequently")
        
        # Barrier-based recommendations
        if common_barriers:
            top_barrier = common_barriers[0]
            if top_barrier[0] == "lack of time":
                recommendations.append("Consider scheduling shorter activities or breaking larger activities into smaller chunks")
            elif top_barrier[0] == "low energy":
                recommendations.append("Focus on gentle, low-energy activities when feeling fatigued")
            elif top_barrier[0] == "low motivation":
                recommendations.append("Use 'behavioral activation' - start with very small activities to build momentum")
        
        return recommendations
    
    def get_current_week_progress(self, patient_id: str) -> Dict[str, Any]:
        """Get progress for current week"""
        # Get start of current week (Monday)
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        
        plan = self.get_weekly_plan(patient_id, week_start)
        if not plan:
            return {"error": "No active plan for current week"}
        
        # Calculate progress
        total_activities = len(plan.scheduled_activities)
        completed_activities = len([a for a in plan.scheduled_activities 
                                  if a.status == ActivityStatus.COMPLETED])
        
        # Get today's activities
        today_activities = [a for a in plan.scheduled_activities 
                          if a.scheduled_date.date() == today.date()]
        
        # Calculate mood trends
        completed_with_mood = [a for a in plan.scheduled_activities 
                             if a.status == ActivityStatus.COMPLETED 
                             and a.mood_before and a.mood_after]
        
        mood_improvements = [a.mood_after - a.mood_before for a in completed_with_mood]
        avg_mood_improvement = sum(mood_improvements) / len(mood_improvements) if mood_improvements else 0
        
        return {
            "week_start": week_start.strftime('%Y-%m-%d'),
            "total_planned_activities": total_activities,
            "completed_activities": completed_activities,
            "completion_rate": round((completed_activities / total_activities * 100) if total_activities > 0 else 0, 1),
            "today_activities": len(today_activities),
            "today_completed": len([a for a in today_activities if a.status == ActivityStatus.COMPLETED]),
            "average_mood_improvement": round(avg_mood_improvement, 2),
            "upcoming_activities": [
                {
                    "activity_id": a.activity_id,
                    "schedule_id": a.schedule_id,
                    "scheduled_time": a.scheduled_time.strftime('%H:%M'),
                    "duration_minutes": a.duration_minutes,
                    "status": a.status.value
                }
                for a in plan.scheduled_activities 
                if a.scheduled_date.date() >= today.date() and a.status == ActivityStatus.PLANNED
            ][:5]  # Next 5 upcoming activities
        }
    
    def add_custom_activity(
        self,
        patient_id: str,
        name: str,
        description: str,
        activity_type: ActivityType,
        estimated_duration: int,
        difficulty_level: int = 3,
        required_materials: List[str] = None
    ) -> Activity:
        """Add custom activity to patient's library"""
        activity_id = f"custom_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        activity = Activity(
            activity_id=activity_id,
            name=name,
            description=description,
            activity_type=activity_type,
            estimated_duration=estimated_duration,
            difficulty_level=difficulty_level,
            required_materials=required_materials or []
        )
        
        self._save_activity(activity, is_default=False)
        return activity
    
    def schedule_single_activity(
        self,
        patient_id: str,
        activity_id: str,
        scheduled_date: datetime,
        scheduled_time: time,
        duration_minutes: int = None
    ) -> ScheduledActivity:
        """Schedule a single activity"""
        # Get activity details
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM activity_library WHERE activity_id = ?", (activity_id,))
            activity_data = cursor.fetchone()
            
            if not activity_data:
                raise ValueError(f"Activity {activity_id} not found")
        
        schedule_id = f"single_{patient_id}_{scheduled_date.strftime('%Y%m%d')}_{scheduled_time.strftime('%H%M')}"
        
        scheduled_activity = ScheduledActivity(
            schedule_id=schedule_id,
            activity_id=activity_id,
            patient_id=patient_id,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            duration_minutes=duration_minutes or activity_data[4],  # estimated_duration
            status=ActivityStatus.PLANNED
        )
        
        self._save_scheduled_activity(scheduled_activity)
        return scheduled_activity
    
    def reschedule_activity(
        self,
        schedule_id: str,
        new_date: datetime,
        new_time: time,
        reason: str = ""
    ) -> bool:
        """Reschedule an existing activity"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE scheduled_activities 
                SET scheduled_date = ?, scheduled_time = ?, status = ?,
                    completion_notes = ?
                WHERE schedule_id = ?
            """, (
                new_date.date(), new_time, ActivityStatus.RESCHEDULED.value,
                f"Rescheduled: {reason}", schedule_id
            ))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
    
    def get_activity_insights(self, patient_id: str, days: int = 30) -> Dict[str, Any]:
        """Get behavioral insights from activity patterns"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get completion patterns by day of week
            cursor.execute("""
                SELECT 
                    CASE CAST(strftime('%w', scheduled_date) AS INTEGER)
                        WHEN 0 THEN 'Sunday'
                        WHEN 1 THEN 'Monday'
                        WHEN 2 THEN 'Tuesday'
                        WHEN 3 THEN 'Wednesday'
                        WHEN 4 THEN 'Thursday'
                        WHEN 5 THEN 'Friday'
                        WHEN 6 THEN 'Saturday'
                    END as day_of_week,
                    COUNT(*) as planned,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed
                FROM scheduled_activities
                WHERE patient_id = ? AND scheduled_date BETWEEN ? AND ?
                GROUP BY strftime('%w', scheduled_date)
                ORDER BY CAST(strftime('%w', scheduled_date) AS INTEGER)
            """, (patient_id, start_date.date(), end_date.date()))
            
            day_patterns = cursor.fetchall()
            
            # Get time of day patterns
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN strftime('%H', scheduled_time) < '12' THEN 'Morning'
                        WHEN strftime('%H', scheduled_time) < '17' THEN 'Afternoon'
                        ELSE 'Evening'
                    END as time_period,
                    COUNT(*) as planned,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
                    AVG(CASE WHEN mood_after - mood_before IS NOT NULL 
                        THEN mood_after - mood_before END) as avg_mood_change
                FROM scheduled_activities
                WHERE patient_id = ? AND scheduled_date BETWEEN ? AND ?
                GROUP BY time_period
            """, (patient_id, start_date.date(), end_date.date()))
            
            time_patterns = cursor.fetchall()
            
            # Identify streak patterns
            cursor.execute("""
                SELECT tracking_date, total_activities_completed
                FROM activity_tracking
                WHERE patient_id = ? AND tracking_date BETWEEN ? AND ?
                ORDER BY tracking_date
            """, (patient_id, start_date.date(), end_date.date()))
            
            daily_completions = cursor.fetchall()
            
            # Calculate streaks
            current_streak = 0
            longest_streak = 0
            temp_streak = 0
            
            for day in daily_completions:
                if day[1] > 0:  # Completed at least one activity
                    temp_streak += 1
                    longest_streak = max(longest_streak, temp_streak)
                else:
                    temp_streak = 0
            
            # Current streak is the last consecutive days with completions
            for day in reversed(daily_completions):
                if day[1] > 0:
                    current_streak += 1
                else:
                    break
            
            insights = {
                "analysis_period": f"{days} days",
                "completion_by_day": [
                    {
                        "day": pattern[0],
                        "planned": pattern[1],
                        "completed": pattern[2],
                        "completion_rate": round((pattern[2] / pattern[1] * 100) if pattern[1] > 0 else 0, 1)
                    }
                    for pattern in day_patterns
                ],
                "completion_by_time": [
                    {
                        "time_period": pattern[0],
                        "planned": pattern[1],
                        "completed": pattern[2],
                        "completion_rate": round((pattern[2] / pattern[1] * 100) if pattern[1] > 0 else 0, 1),
                        "avg_mood_improvement": round(pattern[3], 2) if pattern[3] else 0
                    }
                    for pattern in time_patterns
                ],
                "streak_analysis": {
                    "current_streak_days": current_streak,
                    "longest_streak_days": longest_streak,
                    "total_active_days": len([d for d in daily_completions if d[1] > 0])
                },
                "insights": self._generate_behavioral_insights(day_patterns, time_patterns, current_streak)
            }
            
            return insights
    
    def _generate_behavioral_insights(
        self, 
        day_patterns: List, 
        time_patterns: List, 
        current_streak: int
    ) -> List[str]:
        """Generate behavioral insights from patterns"""
        insights = []
        
        # Day of week insights
        if day_patterns:
            best_day = max(day_patterns, key=lambda x: (x[2] / x[1]) if x[1] > 0 else 0)
            worst_day = min(day_patterns, key=lambda x: (x[2] / x[1]) if x[1] > 0 else 1)
            
            if best_day[1] > 0 and worst_day[1] > 0:
                best_rate = best_day[2] / best_day[1] * 100
                worst_rate = worst_day[2] / worst_day[1] * 100
                
                if best_rate - worst_rate > 20:
                    insights.append(f"You're most consistent on {best_day[0]} ({best_rate:.0f}% completion) and struggle most on {worst_day[0]} ({worst_rate:.0f}% completion)")
        
        # Time of day insights
        if time_patterns:
            best_time = max(time_patterns, key=lambda x: (x[2] / x[1]) if x[1] > 0 else 0)
            
            if best_time[1] > 0:
                best_rate = best_time[2] / best_time[1] * 100
                if best_rate > 70:
                    insights.append(f"{best_time[0]} appears to be your most productive time with {best_rate:.0f}% activity completion")
                
                # Mood insights
                if len(time_patterns) > 1:
                    mood_data = [(p[0], p[3]) for p in time_patterns if p[3] is not None]
                    if mood_data:
                        best_mood_time = max(mood_data, key=lambda x: x[1])
                        if best_mood_time[1] > 0.5:
                            insights.append(f"{best_mood_time[0]} activities provide the best mood improvement (+{best_mood_time[1]:.1f} points)")
        
        # Streak insights
        if current_streak >= 7:
            insights.append(f"Excellent! You're on a {current_streak}-day activity streak. Keep up the momentum!")
        elif current_streak >= 3:
            insights.append(f"Good consistency with a {current_streak}-day streak. Try to extend it further!")
        elif current_streak == 0:
            insights.append("Focus on rebuilding consistency - even completing one small activity today can restart your progress")
        
        return insights


# Example usage and utility functions
def create_example_weekly_plan():
    """Example of creating a weekly activity plan"""
    scheduler = ActivityScheduler()
    
    # Example patient preferences
    preferences = {
        'pleasant_activities_per_day': 2,
        'mastery_activities_per_day': 1,
        'preferred_activity_types': [ActivityType.PLEASANT, ActivityType.MASTERY, ActivityType.SOCIAL],
        'max_difficulty': 3,
        'max_duration_per_activity': 60,
        'preferred_times': ['morning', 'afternoon']
    }
    
    # Create weekly plan
    week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    treatment_goals = [
        "Increase daily pleasant activities",
        "Improve mood through behavioral activation",
        "Build sense of accomplishment"
    ]
    
    plan = scheduler.create_weekly_plan(
        patient_id="patient_001",
        week_start_date=week_start,
        treatment_goals=treatment_goals,
        preferences=preferences
    )
    
    print(f"Created weekly plan: {plan.plan_id}")
    print(f"Activities scheduled: {len(plan.scheduled_activities)}")
    
    return plan


def example_activity_completion():
    """Example of recording activity completion"""
    scheduler = ActivityScheduler()
    
    # Record completion of an activity
    success = scheduler.record_activity_completion(
        schedule_id="sched_patient_001_20240101_0_pleasant",
        status=ActivityStatus.COMPLETED,
        mood_before=4,
        mood_after=7,
        pleasure_experienced=8,
        mastery_experienced=3,
        energy_level=6,
        actual_duration=25,
        notes="Felt much better after the walk. Weather was nice.",
        barriers=[]
    )
    
    if success:
        print("Activity completion recorded successfully")
    
    return success


if __name__ == "__main__":
    # Example usage
    create_example_weekly_plan()
    example_activity_completion()
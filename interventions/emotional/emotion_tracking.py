"""
Emotion Tracking Module for AI Therapy System

This module provides comprehensive emotion identification, tracking, and analysis
capabilities for therapeutic interventions. It supports various emotion tracking
methodologies including DBT diary cards, mood tracking, and emotion regulation
monitoring.

Author: AI Therapy System
Created: 2025
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid
import statistics
from pathlib import Path


# ============================================================================
# ENUMS AND DATA STRUCTURES
# ============================================================================

class EmotionCategory(Enum):
    """Primary emotion categories"""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    DISGUST = "disgust"
    SURPRISE = "surprise"
    CONTEMPT = "contempt"
    SHAME = "shame"
    GUILT = "guilt"
    LOVE = "love"
    EXCITEMENT = "excitement"
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    IRRITABILITY = "irritability"
    CONTENTMENT = "contentment"


class EmotionIntensity(Enum):
    """Intensity levels for emotions (1-10 scale)"""
    VERY_LOW = 1
    LOW = 2
    LOW_MODERATE = 3
    MODERATE = 4
    MODERATE_HIGH = 5
    HIGH = 6
    HIGH_VERY = 7
    VERY_HIGH = 8
    EXTREMELY_HIGH = 9
    OVERWHELMING = 10


class TrackingMethod(Enum):
    """Different emotion tracking methodologies"""
    DBT_DIARY_CARD = "dbt_diary_card"
    MOOD_TRACKING = "mood_tracking"
    EMOTION_LOG = "emotion_log"
    CRISIS_TRACKING = "crisis_tracking"
    THERAPY_SESSION = "therapy_session"
    HOMEWORK_ASSIGNMENT = "homework_assignment"


class TriggerType(Enum):
    """Types of emotional triggers"""
    INTERPERSONAL = "interpersonal"
    WORK_STRESS = "work_stress"
    HEALTH_CONCERNS = "health_concerns"
    FINANCIAL = "financial"
    FAMILY = "family"
    ROMANTIC = "romantic"
    SOCIAL = "social"
    INTERNAL_THOUGHTS = "internal_thoughts"
    PHYSICAL_DISCOMFORT = "physical_discomfort"
    ENVIRONMENTAL = "environmental"
    MEMORY = "memory"
    UNKNOWN = "unknown"


@dataclass
class EmotionEntry:
    """Individual emotion tracking entry"""
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Primary emotion data
    emotion: EmotionCategory = EmotionCategory.SADNESS
    intensity: int = 1  # 1-10 scale
    duration_minutes: Optional[int] = None
    
    # Context and triggers
    trigger: Optional[TriggerType] = None
    trigger_description: str = ""
    situation_context: str = ""
    location: str = ""
    people_present: List[str] = field(default_factory=list)
    
    # Physical sensations
    physical_sensations: List[str] = field(default_factory=list)
    
    # Thoughts and behaviors
    thoughts: List[str] = field(default_factory=list)
    behaviors: List[str] = field(default_factory=list)
    
    # Coping and interventions
    coping_skills_used: List[str] = field(default_factory=list)
    coping_effectiveness: Optional[int] = None  # 1-10 scale
    intervention_needed: bool = False
    
    # Tracking metadata
    tracking_method: TrackingMethod = TrackingMethod.EMOTION_LOG
    session_id: Optional[str] = None
    therapist_notes: str = ""
    
    # Created and updated timestamps
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class DBTDiaryCard:
    """DBT-specific diary card for daily emotion tracking"""
    diary_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    date: datetime = field(default_factory=lambda: datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
    
    # Core emotions (0-10 scale)
    emotions: Dict[str, int] = field(default_factory=dict)
    
    # Target behaviors and urges
    self_harm_urges: int = 0  # 0-10 scale
    suicide_urges: int = 0    # 0-10 scale
    
    # Skills used (checkboxes/counts)
    distress_tolerance_skills: List[str] = field(default_factory=list)
    emotion_regulation_skills: List[str] = field(default_factory=list)
    interpersonal_skills: List[str] = field(default_factory=list)
    mindfulness_skills: List[str] = field(default_factory=list)
    
    # Medications and substances
    medications_taken: Dict[str, bool] = field(default_factory=dict)
    substances_used: Dict[str, int] = field(default_factory=dict)  # amount/frequency
    
    # Sleep and self-care
    hours_slept: Optional[float] = None
    self_care_activities: List[str] = field(default_factory=list)
    
    # Notes and observations
    daily_notes: str = ""
    therapist_review: str = ""
    
    # Metadata
    completed: bool = False
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class EmotionPattern:
    """Identified emotion patterns from tracking data"""
    pattern_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    
    # Pattern identification
    primary_emotion: EmotionCategory = EmotionCategory.SADNESS
    common_triggers: List[TriggerType] = field(default_factory=list)
    average_intensity: float = 0.0
    frequency_per_week: float = 0.0
    
    # Temporal patterns
    time_patterns: Dict[str, int] = field(default_factory=dict)  # hour_of_day: frequency
    day_patterns: Dict[str, int] = field(default_factory=dict)   # day_of_week: frequency
    
    # Associated patterns
    common_thoughts: List[str] = field(default_factory=list)
    common_behaviors: List[str] = field(default_factory=list)
    physical_patterns: List[str] = field(default_factory=list)
    
    # Treatment implications
    recommended_interventions: List[str] = field(default_factory=list)
    therapeutic_focus_areas: List[str] = field(default_factory=list)
    
    # Analysis metadata
    date_range_start: datetime = field(default_factory=datetime.now)
    date_range_end: datetime = field(default_factory=datetime.now)
    confidence_score: float = 0.0  # 0-1 scale
    created_date: datetime = field(default_factory=datetime.now)


# ============================================================================
# MAIN CLASS
# ============================================================================

class EmotionTracker:
    """
    Comprehensive emotion tracking system for therapeutic interventions.
    
    This class manages all aspects of emotion tracking including:
    - Individual emotion entries
    - DBT diary cards
    - Pattern analysis and identification
    - Progress monitoring
    - Therapeutic insights generation
    """
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        """Initialize the emotion tracking system"""
        self.db_path = db_path
        self._initialize_database()
        
        # Common emotions list for easier selection
        self.common_emotions = {
            "positive": ["joy", "happiness", "excitement", "contentment", "love", "gratitude", "pride", "relief"],
            "negative": ["sadness", "anger", "fear", "anxiety", "shame", "guilt", "loneliness", "frustration"],
            "complex": ["mixed", "numb", "overwhelmed", "confused", "ambivalent", "empty"]
        }
        
        # DBT skills reference
        self.dbt_skills = {
            "distress_tolerance": ["TIPP", "ACCEPTS", "Distract", "Self-Soothe", "IMPROVE", "Pros/Cons"],
            "emotion_regulation": ["PLEASE", "Mastery Activities", "Pleasant Events", "Opposite Action"],
            "interpersonal": ["DEAR MAN", "GIVE", "FAST", "Boundaries"],
            "mindfulness": ["Observe", "Describe", "Participate", "One-mindfully", "Non-judgmentally"]
        }
    
    # ========================================================================
    # DATABASE INITIALIZATION
    # ========================================================================
    
    def _initialize_database(self):
        """Initialize database tables for emotion tracking"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Emotion entries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS emotion_entries (
                    entry_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    emotion TEXT NOT NULL,
                    intensity INTEGER NOT NULL,
                    duration_minutes INTEGER,
                    trigger_type TEXT,
                    trigger_description TEXT,
                    situation_context TEXT,
                    location TEXT,
                    people_present TEXT,  -- JSON array
                    physical_sensations TEXT,  -- JSON array
                    thoughts TEXT,  -- JSON array
                    behaviors TEXT,  -- JSON array
                    coping_skills_used TEXT,  -- JSON array
                    coping_effectiveness INTEGER,
                    intervention_needed BOOLEAN,
                    tracking_method TEXT,
                    session_id TEXT,
                    therapist_notes TEXT,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            # DBT diary cards table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dbt_diary_cards (
                    diary_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    emotions TEXT,  -- JSON dict {emotion: intensity}
                    self_harm_urges INTEGER DEFAULT 0,
                    suicide_urges INTEGER DEFAULT 0,
                    distress_tolerance_skills TEXT,  -- JSON array
                    emotion_regulation_skills TEXT,  -- JSON array
                    interpersonal_skills TEXT,  -- JSON array
                    mindfulness_skills TEXT,  -- JSON array
                    medications_taken TEXT,  -- JSON dict
                    substances_used TEXT,  -- JSON dict
                    hours_slept REAL,
                    self_care_activities TEXT,  -- JSON array
                    daily_notes TEXT,
                    therapist_review TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            # Emotion patterns table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS emotion_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    primary_emotion TEXT NOT NULL,
                    common_triggers TEXT,  -- JSON array
                    average_intensity REAL,
                    frequency_per_week REAL,
                    time_patterns TEXT,  -- JSON dict
                    day_patterns TEXT,  -- JSON dict
                    common_thoughts TEXT,  -- JSON array
                    common_behaviors TEXT,  -- JSON array
                    physical_patterns TEXT,  -- JSON array
                    recommended_interventions TEXT,  -- JSON array
                    therapeutic_focus_areas TEXT,  -- JSON array
                    date_range_start TEXT,
                    date_range_end TEXT,
                    confidence_score REAL,
                    created_date TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            conn.commit()
    
    # ========================================================================
    # EMOTION ENTRY MANAGEMENT
    # ========================================================================
    
    def log_emotion(self, entry: EmotionEntry) -> str:
        """Log a new emotion entry"""
        entry.last_updated = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO emotion_entries (
                    entry_id, patient_id, timestamp, emotion, intensity,
                    duration_minutes, trigger_type, trigger_description,
                    situation_context, location, people_present,
                    physical_sensations, thoughts, behaviors,
                    coping_skills_used, coping_effectiveness,
                    intervention_needed, tracking_method, session_id,
                    therapist_notes, created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.entry_id, entry.patient_id, entry.timestamp.isoformat(),
                entry.emotion.value, entry.intensity, entry.duration_minutes,
                entry.trigger.value if entry.trigger else None,
                entry.trigger_description, entry.situation_context,
                entry.location, json.dumps(entry.people_present),
                json.dumps(entry.physical_sensations),
                json.dumps(entry.thoughts), json.dumps(entry.behaviors),
                json.dumps(entry.coping_skills_used), entry.coping_effectiveness,
                entry.intervention_needed, entry.tracking_method.value,
                entry.session_id, entry.therapist_notes,
                entry.created_date.isoformat(), entry.last_updated.isoformat()
            ))
            
            conn.commit()
        
        return entry.entry_id
    
    def get_emotion_entries(
        self, 
        patient_id: str, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        emotion_filter: Optional[EmotionCategory] = None,
        limit: Optional[int] = None
    ) -> List[EmotionEntry]:
        """Retrieve emotion entries with optional filtering"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM emotion_entries WHERE patient_id = ?"
            params = [patient_id]
            
            if start_date:
                query += " AND timestamp >= ?"
                params.append(start_date.isoformat())
            
            if end_date:
                query += " AND timestamp <= ?"
                params.append(end_date.isoformat())
                
            if emotion_filter:
                query += " AND emotion = ?"
                params.append(emotion_filter.value)
            
            query += " ORDER BY timestamp DESC"
            
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            entries = []
            for row in rows:
                entry = EmotionEntry(
                    entry_id=row[0],
                    patient_id=row[1],
                    timestamp=datetime.fromisoformat(row[2]),
                    emotion=EmotionCategory(row[3]),
                    intensity=row[4],
                    duration_minutes=row[5],
                    trigger=TriggerType(row[6]) if row[6] else None,
                    trigger_description=row[7] or "",
                    situation_context=row[8] or "",
                    location=row[9] or "",
                    people_present=json.loads(row[10] or '[]'),
                    physical_sensations=json.loads(row[11] or '[]'),
                    thoughts=json.loads(row[12] or '[]'),
                    behaviors=json.loads(row[13] or '[]'),
                    coping_skills_used=json.loads(row[14] or '[]'),
                    coping_effectiveness=row[15],
                    intervention_needed=bool(row[16]),
                    tracking_method=TrackingMethod(row[17]),
                    session_id=row[18],
                    therapist_notes=row[19] or "",
                    created_date=datetime.fromisoformat(row[20]),
                    last_updated=datetime.fromisoformat(row[21])
                )
                entries.append(entry)
            
            return entries
    
    # ========================================================================
    # DBT DIARY CARD MANAGEMENT
    # ========================================================================
    
    def create_dbt_diary_card(self, patient_id: str, date: datetime) -> DBTDiaryCard:
        """Create a new DBT diary card for a specific date"""
        diary_card = DBTDiaryCard(
            patient_id=patient_id,
            date=date.replace(hour=0, minute=0, second=0, microsecond=0)
        )
        
        # Initialize with common DBT emotions
        diary_card.emotions = {
            "anger": 0, "sadness": 0, "fear": 0, "shame": 0, "guilt": 0,
            "joy": 0, "love": 0, "excitement": 0, "contentment": 0
        }
        
        # Initialize medications dict (empty by default)
        diary_card.medications_taken = {}
        
        self._save_dbt_diary_card(diary_card)
        return diary_card
    
    def update_dbt_diary_card(self, diary_card: DBTDiaryCard) -> bool:
        """Update an existing DBT diary card"""
        diary_card.last_updated = datetime.now()
        return self._save_dbt_diary_card(diary_card)
    
    def _save_dbt_diary_card(self, diary_card: DBTDiaryCard) -> bool:
        """Save DBT diary card to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO dbt_diary_cards (
                    diary_id, patient_id, date, emotions, self_harm_urges,
                    suicide_urges, distress_tolerance_skills, emotion_regulation_skills,
                    interpersonal_skills, mindfulness_skills, medications_taken,
                    substances_used, hours_slept, self_care_activities,
                    daily_notes, therapist_review, completed, created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                diary_card.diary_id, diary_card.patient_id, diary_card.date.isoformat(),
                json.dumps(diary_card.emotions), diary_card.self_harm_urges,
                diary_card.suicide_urges, json.dumps(diary_card.distress_tolerance_skills),
                json.dumps(diary_card.emotion_regulation_skills),
                json.dumps(diary_card.interpersonal_skills),
                json.dumps(diary_card.mindfulness_skills),
                json.dumps(diary_card.medications_taken),
                json.dumps(diary_card.substances_used), diary_card.hours_slept,
                json.dumps(diary_card.self_care_activities), diary_card.daily_notes,
                diary_card.therapist_review, diary_card.completed,
                diary_card.created_date.isoformat(), diary_card.last_updated.isoformat()
            ))
            
            conn.commit()
        
        return True
    
    def get_dbt_diary_card(self, patient_id: str, date: datetime) -> Optional[DBTDiaryCard]:
        """Retrieve DBT diary card for a specific date"""
        date_str = date.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM dbt_diary_cards 
                WHERE patient_id = ? AND date = ?
            """, (patient_id, date_str))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return DBTDiaryCard(
                diary_id=row[0],
                patient_id=row[1],
                date=datetime.fromisoformat(row[2]),
                emotions=json.loads(row[3] or '{}'),
                self_harm_urges=row[4],
                suicide_urges=row[5],
                distress_tolerance_skills=json.loads(row[6] or '[]'),
                emotion_regulation_skills=json.loads(row[7] or '[]'),
                interpersonal_skills=json.loads(row[8] or '[]'),
                mindfulness_skills=json.loads(row[9] or '[]'),
                medications_taken=json.loads(row[10] or '{}'),
                substances_used=json.loads(row[11] or '{}'),
                hours_slept=row[12],
                self_care_activities=json.loads(row[13] or '[]'),
                daily_notes=row[14] or "",
                therapist_review=row[15] or "",
                completed=bool(row[16]),
                created_date=datetime.fromisoformat(row[17]),
                last_updated=datetime.fromisoformat(row[18])
            )
    
    def get_dbt_diary_cards_range(
        self, 
        patient_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[DBTDiaryCard]:
        """Get all diary cards within a date range"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM dbt_diary_cards 
                WHERE patient_id = ? AND date BETWEEN ? AND ?
                ORDER BY date ASC
            """, (patient_id, start_date.isoformat(), end_date.isoformat()))
            
            diary_cards = []
            for row in cursor.fetchall():
                diary_card = DBTDiaryCard(
                    diary_id=row[0],
                    patient_id=row[1],
                    date=datetime.fromisoformat(row[2]),
                    emotions=json.loads(row[3] or '{}'),
                    self_harm_urges=row[4],
                    suicide_urges=row[5],
                    distress_tolerance_skills=json.loads(row[6] or '[]'),
                    emotion_regulation_skills=json.loads(row[7] or '[]'),
                    interpersonal_skills=json.loads(row[8] or '[]'),
                    mindfulness_skills=json.loads(row[9] or '[]'),
                    medications_taken=json.loads(row[10] or '{}'),
                    substances_used=json.loads(row[11] or '{}'),
                    hours_slept=row[12],
                    self_care_activities=json.loads(row[13] or '[]'),
                    daily_notes=row[14] or "",
                    therapist_review=row[15] or "",
                    completed=bool(row[16]),
                    created_date=datetime.fromisoformat(row[17]),
                    last_updated=datetime.fromisoformat(row[18])
                )
                diary_cards.append(diary_card)
            
            return diary_cards
    
    # ========================================================================
    # EMOTION PATTERN ANALYSIS
    # ========================================================================
    
    def analyze_emotion_patterns(
        self, 
        patient_id: str, 
        analysis_period_days: int = 30
    ) -> List[EmotionPattern]:
        """Analyze emotion patterns from tracking data"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=analysis_period_days)
        
        # Get all emotion entries in the period
        entries = self.get_emotion_entries(patient_id, start_date, end_date)
        
        if not entries:
            return []
        
        # Group entries by emotion type
        emotion_groups = {}
        for entry in entries:
            emotion_key = entry.emotion.value
            if emotion_key not in emotion_groups:
                emotion_groups[emotion_key] = []
            emotion_groups[emotion_key].append(entry)
        
        patterns = []
        
        for emotion_type, emotion_entries in emotion_groups.items():
            if len(emotion_entries) < 3:  # Need at least 3 entries for pattern analysis
                continue
            
            pattern = self._analyze_single_emotion_pattern(
                patient_id, emotion_type, emotion_entries, start_date, end_date
            )
            patterns.append(pattern)
        
        # Sort by frequency (most common patterns first)
        patterns.sort(key=lambda x: x.frequency_per_week, reverse=True)
        
        # Save patterns to database
        for pattern in patterns:
            self._save_emotion_pattern(pattern)
        
        return patterns
    
    def _analyze_single_emotion_pattern(
        self,
        patient_id: str,
        emotion_type: str,
        entries: List[EmotionEntry],
        start_date: datetime,
        end_date: datetime
    ) -> EmotionPattern:
        """Analyze patterns for a specific emotion"""
        
        pattern = EmotionPattern(
            patient_id=patient_id,
            primary_emotion=EmotionCategory(emotion_type),
            date_range_start=start_date,
            date_range_end=end_date
        )
        
        # Calculate basic statistics
        intensities = [entry.intensity for entry in entries]
        pattern.average_intensity = statistics.mean(intensities)
        
        # Calculate frequency per week
        days_analyzed = (end_date - start_date).days
        weeks_analyzed = max(1, days_analyzed / 7)
        pattern.frequency_per_week = len(entries) / weeks_analyzed
        
        # Analyze triggers
        trigger_counts = {}
        for entry in entries:
            if entry.trigger:
                trigger_key = entry.trigger.value
                trigger_counts[trigger_key] = trigger_counts.get(trigger_key, 0) + 1
        
        # Get most common triggers (at least 20% of entries)
        min_trigger_count = max(1, len(entries) * 0.2)
        common_triggers = [
            TriggerType(trigger) for trigger, count in trigger_counts.items()
            if count >= min_trigger_count
        ]
        pattern.common_triggers = common_triggers
        
        # Analyze time patterns
        time_counts = {}
        day_counts = {}
        
        for entry in entries:
            hour = entry.timestamp.hour
            day_of_week = entry.timestamp.strftime('%A')
            
            time_counts[str(hour)] = time_counts.get(str(hour), 0) + 1
            day_counts[day_of_week] = day_counts.get(day_of_week, 0) + 1
        
        pattern.time_patterns = time_counts
        pattern.day_patterns = day_counts
        
        # Analyze common thoughts and behaviors
        all_thoughts = []
        all_behaviors = []
        all_physical = []
        
        for entry in entries:
            all_thoughts.extend(entry.thoughts)
            all_behaviors.extend(entry.behaviors)
            all_physical.extend(entry.physical_sensations)
        
        # Find most common thoughts/behaviors (simple frequency count)
        thought_counts = {}
        behavior_counts = {}
        physical_counts = {}
        
        for thought in all_thoughts:
            thought_counts[thought] = thought_counts.get(thought, 0) + 1
        
        for behavior in all_behaviors:
            behavior_counts[behavior] = behavior_counts.get(behavior, 0) + 1
            
        for sensation in all_physical:
            physical_counts[sensation] = physical_counts.get(sensation, 0) + 1
        
        # Keep top 5 most common in each category
        pattern.common_thoughts = sorted(thought_counts.keys(), 
                                       key=lambda x: thought_counts[x], reverse=True)[:5]
        pattern.common_behaviors = sorted(behavior_counts.keys(), 
                                        key=lambda x: behavior_counts[x], reverse=True)[:5]
        pattern.physical_patterns = sorted(physical_counts.keys(), 
                                         key=lambda x: physical_counts[x], reverse=True)[:5]
        
        # Generate intervention recommendations
        pattern.recommended_interventions = self._generate_intervention_recommendations(pattern)
        pattern.therapeutic_focus_areas = self._identify_focus_areas(pattern)
        
        # Calculate confidence score
        pattern.confidence_score = self._calculate_confidence_score(pattern, len(entries))
        
        return pattern
    
    def _generate_intervention_recommendations(self, pattern: EmotionPattern) -> List[str]:
        """Generate therapeutic intervention recommendations based on pattern"""
        recommendations = []
        
        emotion_type = pattern.primary_emotion
        
        # Emotion-specific recommendations
        if emotion_type in [EmotionCategory.ANXIETY, EmotionCategory.FEAR]:
            recommendations.extend([
                "Progressive muscle relaxation",
                "Exposure therapy techniques",
                "Cognitive restructuring for anxiety",
                "Mindfulness-based anxiety reduction"
            ])
        
        elif emotion_type in [EmotionCategory.SADNESS, EmotionCategory.DEPRESSION]:
            recommendations.extend([
                "Behavioral activation",
                "Pleasant activity scheduling",
                "Cognitive restructuring for depression",
                "Interpersonal therapy techniques"
            ])
        
        elif emotion_type == EmotionCategory.ANGER:
            recommendations.extend([
                "Anger management techniques",
                "Assertiveness training",
                "Distress tolerance skills",
                "TIPP technique for crisis moments"
            ])
        
        elif emotion_type in [EmotionCategory.SHAME, EmotionCategory.GUILT]:
            recommendations.extend([
                "Self-compassion exercises",
                "Cognitive restructuring for shame",
                "Values clarification work",
                "Radical acceptance techniques"
            ])
        
        # Trigger-specific recommendations
        if TriggerType.INTERPERSONAL in pattern.common_triggers:
            recommendations.extend([
                "Interpersonal effectiveness skills",
                "DEAR MAN communication technique",
                "Boundary setting exercises"
            ])
        
        if TriggerType.WORK_STRESS in pattern.common_triggers:
            recommendations.extend([
                "Workplace stress management",
                "Time management techniques",
                "Professional boundary setting"
            ])
        
        # Intensity-specific recommendations
        if pattern.average_intensity >= 7:
            recommendations.extend([
                "Crisis survival skills",
                "Distress tolerance techniques",
                "Safety planning"
            ])
        
        return list(set(recommendations))  # Remove duplicates
    
    def _identify_focus_areas(self, pattern: EmotionPattern) -> List[str]:
        """Identify therapeutic focus areas based on pattern analysis"""
        focus_areas = []
        
        # High frequency patterns
        if pattern.frequency_per_week >= 5:
            focus_areas.append("High-frequency emotion regulation")
        
        # High intensity patterns
        if pattern.average_intensity >= 7:
            focus_areas.append("Crisis intervention and safety")
        
        # Trigger-based focus areas
        if len(pattern.common_triggers) >= 3:
            focus_areas.append("Multi-trigger awareness and management")
        
        if TriggerType.INTERPERSONAL in pattern.common_triggers:
            focus_areas.append("Interpersonal relationships")
        
        if TriggerType.INTERNAL_THOUGHTS in pattern.common_triggers:
            focus_areas.append("Cognitive restructuring")
        
        # Pattern-specific focus areas
        if pattern.primary_emotion in [EmotionCategory.ANXIETY, EmotionCategory.FEAR]:
            focus_areas.append("Anxiety disorders treatment")
        
        elif pattern.primary_emotion in [EmotionCategory.SADNESS, EmotionCategory.DEPRESSION]:
            focus_areas.append("Depression treatment")
        
        elif pattern.primary_emotion == EmotionCategory.ANGER:
            focus_areas.append("Anger management")
        
        return focus_areas
    
    def _calculate_confidence_score(self, pattern: EmotionPattern, entry_count: int) -> float:
        """Calculate confidence score for pattern reliability"""
        base_confidence = min(0.8, entry_count / 20)  # Higher confidence with more data
        
        # Adjust based on pattern consistency
        if pattern.frequency_per_week >= 3:
            base_confidence += 0.1
        
        if len(pattern.common_triggers) >= 2:
            base_confidence += 0.1
        
        return min(1.0, base_confidence)
    
    def _save_emotion_pattern(self, pattern: EmotionPattern):
        """Save emotion pattern to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO emotion_patterns (
                    pattern_id, patient_id, primary_emotion, common_triggers,
                    average_intensity, frequency_per_week, time_patterns,
                    day_patterns, common_thoughts, common_behaviors,
                    physical_patterns, recommended_interventions,
                    therapeutic_focus_areas, date_range_start, date_range_end,
                    confidence_score, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pattern.pattern_id, pattern.patient_id, pattern.primary_emotion.value,
                json.dumps([t.value for t in pattern.common_triggers]),
                pattern.average_intensity, pattern.frequency_per_week,
                json.dumps(pattern.time_patterns), json.dumps(pattern.day_patterns),
                json.dumps(pattern.common_thoughts), json.dumps(pattern.common_behaviors),
                json.dumps(pattern.physical_patterns),
                json.dumps(pattern.recommended_interventions),
                json.dumps(pattern.therapeutic_focus_areas),
                pattern.date_range_start.isoformat(), pattern.date_range_end.isoformat(),
                pattern.confidence_score, pattern.created_date.isoformat()
            ))
            
            conn.commit()
    
    # ========================================================================
    # REPORTING AND ANALYTICS
    # ========================================================================
    
    def generate_emotion_report(
        self, 
        patient_id: str, 
        report_period_days: int = 30
    ) -> Dict[str, Any]:
        """Generate comprehensive emotion tracking report"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=report_period_days)
        
        # Get all data
        entries = self.get_emotion_entries(patient_id, start_date, end_date)
        diary_cards = self.get_dbt_diary_cards_range(patient_id, start_date, end_date)
        patterns = self.analyze_emotion_patterns(patient_id, report_period_days)
        
        # Basic statistics
        total_entries = len(entries)
        avg_intensity = statistics.mean([e.intensity for e in entries]) if entries else 0
        
        # Most common emotions
        emotion_counts = {}
        for entry in entries:
            emotion_counts[entry.emotion.value] = emotion_counts.get(entry.emotion.value, 0) + 1
        
        # DBT diary card completion rate
        diary_completion_rate = 0
        if diary_cards:
            completed_cards = sum(1 for card in diary_cards if card.completed)
            diary_completion_rate = completed_cards / len(diary_cards)
        
        # Coping skills effectiveness
        coping_effectiveness = []
        for entry in entries:
            if entry.coping_effectiveness is not None:
                coping_effectiveness.append(entry.coping_effectiveness)
        
        avg_coping_effectiveness = statistics.mean(coping_effectiveness) if coping_effectiveness else 0
        
        # Crisis indicators
        high_intensity_count = sum(1 for e in entries if e.intensity >= 8)
        intervention_needed_count = sum(1 for e in entries if e.intervention_needed)
        
        # Generate insights
        insights = self._generate_insights(entries, patterns, diary_cards)
        
        report = {
            "report_period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days_analyzed": report_period_days
            },
            "summary_statistics": {
                "total_emotion_entries": total_entries,
                "average_intensity": round(avg_intensity, 2),
                "diary_cards_completed": len([c for c in diary_cards if c.completed]),
                "diary_completion_rate": round(diary_completion_rate, 2),
                "high_intensity_episodes": high_intensity_count,
                "interventions_needed": intervention_needed_count
            },
            "emotion_breakdown": emotion_counts,
            "most_common_emotions": sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "coping_effectiveness": {
                "average_effectiveness": round(avg_coping_effectiveness, 2),
                "total_coping_attempts": len(coping_effectiveness)
            },
            "identified_patterns": [
                {
                    "emotion": pattern.primary_emotion.value,
                    "frequency_per_week": round(pattern.frequency_per_week, 2),
                    "average_intensity": round(pattern.average_intensity, 2),
                    "common_triggers": [t.value for t in pattern.common_triggers],
                    "confidence_score": round(pattern.confidence_score, 2)
                }
                for pattern in patterns[:5]  # Top 5 patterns
            ],
            "therapeutic_insights": insights,
            "generated_at": datetime.now().isoformat()
        }
        
        return report
    
    def _generate_insights(
        self, 
        entries: List[EmotionEntry], 
        patterns: List[EmotionPattern],
        diary_cards: List[DBTDiaryCard]
    ) -> List[str]:
        """Generate therapeutic insights from data analysis"""
        insights = []
        
        if not entries:
            insights.append("Insufficient tracking data for meaningful insights.")
            return insights
        
        # Intensity insights
        avg_intensity = statistics.mean([e.intensity for e in entries])
        if avg_intensity >= 7:
            insights.append("High average emotional intensity indicates need for crisis management skills.")
        elif avg_intensity <= 3:
            insights.append("Low emotional intensity may indicate emotional numbing or effective coping.")
        
        # Frequency insights
        if len(entries) >= 20:  # High frequency tracking
            insights.append("Consistent emotion tracking shows strong engagement with treatment.")
        
        # Pattern insights
        if patterns:
            top_pattern = patterns[0]
            if top_pattern.frequency_per_week >= 5:
                insights.append(f"High frequency of {top_pattern.primary_emotion.value} suggests this as primary treatment target.")
        
        # DBT-specific insights
        if diary_cards:
            avg_self_harm = statistics.mean([c.self_harm_urges for c in diary_cards])
            avg_suicide = statistics.mean([c.suicide_urges for c in diary_cards])
            
            if avg_self_harm >= 3:
                insights.append("Elevated self-harm urges require immediate attention and safety planning.")
            if avg_suicide >= 2:
                insights.append("Suicide ideation present - requires ongoing safety assessment and intervention.")
        
        # Coping insights
        coping_attempts = [e for e in entries if e.coping_skills_used]
        if coping_attempts:
            avg_effectiveness = statistics.mean([e.coping_effectiveness for e in coping_attempts if e.coping_effectiveness])
            if avg_effectiveness < 5:
                insights.append("Low coping effectiveness suggests need for skills training or strategy modification.")
        
        # Trigger insights
        trigger_counts = {}
        for entry in entries:
            if entry.trigger:
                trigger_counts[entry.trigger.value] = trigger_counts.get(entry.trigger.value, 0) + 1
        
        if trigger_counts:
            most_common_trigger = max(trigger_counts.items(), key=lambda x: x[1])
            insights.append(f"Most common trigger is {most_common_trigger[0]} - consider targeted intervention.")
        
        return insights
    
    def get_weekly_emotion_summary(self, patient_id: str, week_start: datetime) -> Dict[str, Any]:
        """Get a summary of emotions for a specific week"""
        week_end = week_start + timedelta(days=7)
        
        entries = self.get_emotion_entries(patient_id, week_start, week_end)
        diary_cards = self.get_dbt_diary_cards_range(patient_id, week_start, week_end)
        
        # Daily emotion averages
        daily_emotions = {}
        for i in range(7):
            day = week_start + timedelta(days=i)
            day_key = day.strftime('%Y-%m-%d')
            day_entries = [e for e in entries if e.timestamp.date() == day.date()]
            
            if day_entries:
                daily_emotions[day_key] = {
                    "average_intensity": statistics.mean([e.intensity for e in day_entries]),
                    "entry_count": len(day_entries),
                    "most_common_emotion": max(set([e.emotion.value for e in day_entries]), 
                                             key=[e.emotion.value for e in day_entries].count)
                }
            else:
                daily_emotions[day_key] = {
                    "average_intensity": 0,
                    "entry_count": 0,
                    "most_common_emotion": None
                }
        
        # DBT diary completion
        diary_completion = {}
        for card in diary_cards:
            day_key = card.date.strftime('%Y-%m-%d')
            diary_completion[day_key] = card.completed
        
        return {
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "daily_emotions": daily_emotions,
            "diary_completion": diary_completion,
            "total_entries": len(entries),
            "average_weekly_intensity": statistics.mean([e.intensity for e in entries]) if entries else 0
        }
    
    # ========================================================================
    # CLINICAL ALERTS AND SAFETY
    # ========================================================================
    
    def check_safety_alerts(self, patient_id: str) -> List[Dict[str, Any]]:
        """Check for safety alerts based on recent emotion tracking"""
        alerts = []
        
        # Check recent high-intensity episodes
        recent_entries = self.get_emotion_entries(
            patient_id, 
            datetime.now() - timedelta(days=7), 
            limit=50
        )
        
        high_intensity_count = sum(1 for e in recent_entries if e.intensity >= 9)
        if high_intensity_count >= 3:
            alerts.append({
                "type": "high_intensity_episodes",
                "severity": "high",
                "message": f"{high_intensity_count} high-intensity emotional episodes in past week",
                "recommendation": "Consider crisis intervention and safety planning"
            })
        
        # Check intervention requests
        intervention_needed = sum(1 for e in recent_entries if e.intervention_needed)
        if intervention_needed >= 2:
            alerts.append({
                "type": "intervention_requests",
                "severity": "medium",
                "message": f"{intervention_needed} requests for intervention in past week",
                "recommendation": "Increase session frequency or provide additional support"
            })
        
        # Check DBT diary cards for concerning urges
        recent_diaries = self.get_dbt_diary_cards_range(
            patient_id,
            datetime.now() - timedelta(days=7),
            datetime.now()
        )
        
        for diary in recent_diaries:
            if diary.suicide_urges >= 5:
                alerts.append({
                    "type": "suicide_ideation",
                    "severity": "critical",
                    "message": f"High suicide urges reported on {diary.date.strftime('%Y-%m-%d')}",
                    "recommendation": "Immediate safety assessment and intervention required"
                })
            
            if diary.self_harm_urges >= 7:
                alerts.append({
                    "type": "self_harm_urges",
                    "severity": "high",
                    "message": f"High self-harm urges reported on {diary.date.strftime('%Y-%m-%d')}",
                    "recommendation": "Assess safety and provide crisis coping skills"
                })
        
        return alerts
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def get_emotion_suggestions(self, context: str = "") -> List[str]:
        """Get emotion suggestions based on context or common emotions"""
        if "positive" in context.lower() or "good" in context.lower():
            return self.common_emotions["positive"]
        elif "negative" in context.lower() or "bad" in context.lower():
            return self.common_emotions["negative"]
        else:
            # Return a mix of common emotions
            return (self.common_emotions["positive"][:4] + 
                   self.common_emotions["negative"][:6] + 
                   self.common_emotions["complex"][:3])
    
    def get_dbt_skills_list(self, category: str = None) -> List[str]:
        """Get list of DBT skills, optionally filtered by category"""
        if category and category in self.dbt_skills:
            return self.dbt_skills[category]
        elif category:
            return []
        else:
            # Return all skills
            all_skills = []
            for skills_list in self.dbt_skills.values():
                all_skills.extend(skills_list)
            return all_skills
    
    def validate_emotion_entry(self, entry: EmotionEntry) -> List[str]:
        """Validate emotion entry and return list of validation errors"""
        errors = []
        
        if not entry.patient_id:
            errors.append("Patient ID is required")
        
        if entry.intensity < 1 or entry.intensity > 10:
            errors.append("Intensity must be between 1 and 10")
        
        if entry.duration_minutes is not None and entry.duration_minutes < 0:
            errors.append("Duration cannot be negative")
        
        if entry.coping_effectiveness is not None and (entry.coping_effectiveness < 1 or entry.coping_effectiveness > 10):
            errors.append("Coping effectiveness must be between 1 and 10")
        
        return errors
    
    def export_emotion_data(
        self, 
        patient_id: str, 
        start_date: datetime, 
        end_date: datetime,
        format: str = "json"
    ) -> Dict[str, Any]:
        """Export emotion tracking data in specified format"""
        entries = self.get_emotion_entries(patient_id, start_date, end_date)
        diary_cards = self.get_dbt_diary_cards_range(patient_id, start_date, end_date)
        patterns = self.analyze_emotion_patterns(patient_id, (end_date - start_date).days)
        
        export_data = {
            "patient_id": patient_id,
            "export_date": datetime.now().isoformat(),
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "emotion_entries": [
                {
                    "entry_id": entry.entry_id,
                    "timestamp": entry.timestamp.isoformat(),
                    "emotion": entry.emotion.value,
                    "intensity": entry.intensity,
                    "duration_minutes": entry.duration_minutes,
                    "trigger": entry.trigger.value if entry.trigger else None,
                    "trigger_description": entry.trigger_description,
                    "situation_context": entry.situation_context,
                    "coping_skills_used": entry.coping_skills_used,
                    "coping_effectiveness": entry.coping_effectiveness
                }
                for entry in entries
            ],
            "dbt_diary_cards": [
                {
                    "date": card.date.isoformat(),
                    "emotions": card.emotions,
                    "self_harm_urges": card.self_harm_urges,
                    "suicide_urges": card.suicide_urges,
                    "skills_used": {
                        "distress_tolerance": card.distress_tolerance_skills,
                        "emotion_regulation": card.emotion_regulation_skills,
                        "interpersonal": card.interpersonal_skills,
                        "mindfulness": card.mindfulness_skills
                    },
                    "completed": card.completed
                }
                for card in diary_cards
            ],
            "emotion_patterns": [
                {
                    "primary_emotion": pattern.primary_emotion.value,
                    "average_intensity": pattern.average_intensity,
                    "frequency_per_week": pattern.frequency_per_week,
                    "common_triggers": [t.value for t in pattern.common_triggers],
                    "recommended_interventions": pattern.recommended_interventions,
                    "confidence_score": pattern.confidence_score
                }
                for pattern in patterns
            ]
        }
        
        return export_data


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_quick_emotion_entry(
    patient_id: str,
    emotion: str,
    intensity: int,
    situation: str = "",
    coping_skills: List[str] = None
) -> EmotionEntry:
    """Create a quick emotion entry with minimal required information"""
    
    # Convert string emotion to EmotionCategory
    try:
        emotion_category = EmotionCategory(emotion.lower())
    except ValueError:
        emotion_category = EmotionCategory.SADNESS  # Default
    
    entry = EmotionEntry(
        patient_id=patient_id,
        emotion=emotion_category,
        intensity=max(1, min(10, intensity)),  # Ensure valid range
        situation_context=situation,
        coping_skills_used=coping_skills or [],
        tracking_method=TrackingMethod.EMOTION_LOG
    )
    
    return entry


def get_emotion_color_mapping() -> Dict[str, str]:
    """Get color mapping for emotions (useful for UI visualization)"""
    return {
        "joy": "#FFD700",      # Gold
        "happiness": "#FFD700",
        "sadness": "#4169E1",   # Royal Blue
        "anger": "#DC143C",     # Crimson
        "fear": "#9370DB",      # Medium Purple
        "anxiety": "#FF6347",   # Tomato
        "disgust": "#228B22",   # Forest Green
        "surprise": "#FF8C00",  # Dark Orange
        "shame": "#8B008B",     # Dark Magenta
        "guilt": "#2F4F4F",     # Dark Slate Gray
        "love": "#FF1493",      # Deep Pink
        "excitement": "#FF4500", # Orange Red
        "depression": "#191970", # Midnight Blue
        "contentment": "#98FB98" # Pale Green
    }


if __name__ == "__main__":
    # Example usage and testing
    tracker = EmotionTracker()
    
    # Create a sample emotion entry
    entry = create_quick_emotion_entry(
        patient_id="test_patient_001",
        emotion="anxiety",
        intensity=7,
        situation="Work presentation",
        coping_skills=["Deep breathing", "Progressive muscle relaxation"]
    )
    
    # Log the emotion
    entry_id = tracker.log_emotion(entry)
    print(f"Logged emotion entry: {entry_id}")
    
    # Create a DBT diary card
    diary_card = tracker.create_dbt_diary_card("test_patient_001", datetime.now())
    diary_card.emotions["anxiety"] = 6
    diary_card.emotions["sadness"] = 4
    diary_card.distress_tolerance_skills = ["TIPP", "Distraction"]
    tracker.update_dbt_diary_card(diary_card)
    
    print("Created and updated DBT diary card")
    
    # Generate a report
    report = tracker.generate_emotion_report("test_patient_001", 30)
    print("Generated emotion tracking report")
    print(f"Total entries: {report['summary_statistics']['total_emotion_entries']}")
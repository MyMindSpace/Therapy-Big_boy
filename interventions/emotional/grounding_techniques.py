import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid
import random
from pathlib import Path


class GroundingType(Enum):
    SENSORY_5_4_3_2_1 = "sensory_5_4_3_2_1"
    PHYSICAL_MOVEMENT = "physical_movement"
    BREATHING = "breathing"
    COGNITIVE = "cognitive"
    EMOTIONAL = "emotional"
    PROGRESSIVE_MUSCLE = "progressive_muscle"
    MINDFULNESS = "mindfulness"
    VISUALIZATION = "visualization"
    TACTILE = "tactile"
    AUDITORY = "auditory"


class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class GroundingSetting(Enum):
    ANYWHERE = "anywhere"
    HOME = "home"
    WORK = "work"
    PUBLIC = "public"
    PRIVATE = "private"
    QUIET_SPACE = "quiet_space"


@dataclass
class GroundingTechnique:
    technique_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    grounding_type: GroundingType = GroundingType.SENSORY_5_4_3_2_1
    difficulty_level: DifficultyLevel = DifficultyLevel.BEGINNER
    duration_minutes: int = 5
    
    description: str = ""
    instructions: List[str] = field(default_factory=list)
    settings: List[GroundingSetting] = field(default_factory=list)
    
    target_symptoms: List[str] = field(default_factory=list)
    contraindications: List[str] = field(default_factory=list)
    
    materials_needed: List[str] = field(default_factory=list)
    audio_cues: List[str] = field(default_factory=list)
    variations: List[str] = field(default_factory=list)
    
    effectiveness_rating: Optional[float] = None
    usage_count: int = 0
    created_date: datetime = field(default_factory=datetime.now)


@dataclass
class GroundingSession:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    technique_id: str = ""
    
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    
    pre_session_distress: int = 0
    post_session_distress: int = 0
    distress_reduction: Optional[int] = None
    
    completion_status: str = "started"
    
    symptoms_before: List[str] = field(default_factory=list)
    symptoms_after: List[str] = field(default_factory=list)
    
    effectiveness_rating: Optional[int] = None
    notes: str = ""
    barriers_encountered: List[str] = field(default_factory=list)
    
    setting_used: Optional[GroundingSetting] = None
    modifications_made: List[str] = field(default_factory=list)
    
    therapist_guided: bool = False
    crisis_situation: bool = False
    
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class GroundingPlan:
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    
    preferred_techniques: List[str] = field(default_factory=list)
    backup_techniques: List[str] = field(default_factory=list)
    crisis_techniques: List[str] = field(default_factory=list)
    
    daily_practice_schedule: Dict[str, List[str]] = field(default_factory=dict)
    trigger_response_plan: Dict[str, str] = field(default_factory=dict)
    
    personalization_notes: str = ""
    adaptations: List[str] = field(default_factory=list)
    
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


class GroundingTechniqueLibrary:
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self._initialize_database()
        self._populate_default_techniques()
    
    def _initialize_database(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS grounding_techniques (
                    technique_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    grounding_type TEXT NOT NULL,
                    difficulty_level TEXT NOT NULL,
                    duration_minutes INTEGER,
                    description TEXT,
                    instructions TEXT,
                    settings TEXT,
                    target_symptoms TEXT,
                    contraindications TEXT,
                    materials_needed TEXT,
                    audio_cues TEXT,
                    variations TEXT,
                    effectiveness_rating REAL,
                    usage_count INTEGER DEFAULT 0,
                    created_date TEXT NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS grounding_sessions (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    technique_id TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    duration_minutes INTEGER,
                    pre_session_distress INTEGER,
                    post_session_distress INTEGER,
                    distress_reduction INTEGER,
                    completion_status TEXT,
                    symptoms_before TEXT,
                    symptoms_after TEXT,
                    effectiveness_rating INTEGER,
                    notes TEXT,
                    barriers_encountered TEXT,
                    setting_used TEXT,
                    modifications_made TEXT,
                    therapist_guided BOOLEAN,
                    crisis_situation BOOLEAN,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                    FOREIGN KEY (technique_id) REFERENCES grounding_techniques (technique_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS grounding_plans (
                    plan_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    preferred_techniques TEXT,
                    backup_techniques TEXT,
                    crisis_techniques TEXT,
                    daily_practice_schedule TEXT,
                    trigger_response_plan TEXT,
                    personalization_notes TEXT,
                    adaptations TEXT,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            conn.commit()
    
    def _populate_default_techniques(self):
        default_techniques = self._get_default_techniques()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for technique in default_techniques:
                cursor.execute("""
                    INSERT OR IGNORE INTO grounding_techniques (
                        technique_id, name, grounding_type, difficulty_level,
                        duration_minutes, description, instructions, settings,
                        target_symptoms, contraindications, materials_needed,
                        audio_cues, variations, effectiveness_rating,
                        usage_count, created_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    technique.technique_id, technique.name, technique.grounding_type.value,
                    technique.difficulty_level.value, technique.duration_minutes,
                    technique.description, json.dumps(technique.instructions),
                    json.dumps([s.value for s in technique.settings]),
                    json.dumps(technique.target_symptoms),
                    json.dumps(technique.contraindications),
                    json.dumps(technique.materials_needed),
                    json.dumps(technique.audio_cues),
                    json.dumps(technique.variations),
                    technique.effectiveness_rating,
                    technique.usage_count,
                    technique.created_date.isoformat()
                ))
            
            conn.commit()
    
    def _get_default_techniques(self) -> List[GroundingTechnique]:
        return [
            GroundingTechnique(
                technique_id="5_4_3_2_1_sensory",
                name="5-4-3-2-1 Sensory Grounding",
                grounding_type=GroundingType.SENSORY_5_4_3_2_1,
                difficulty_level=DifficultyLevel.BEGINNER,
                duration_minutes=5,
                description="Use all five senses to ground yourself in the present moment",
                instructions=[
                    "Name 5 things you can see around you",
                    "Name 4 things you can touch or feel",
                    "Name 3 things you can hear",
                    "Name 2 things you can smell",
                    "Name 1 thing you can taste"
                ],
                settings=[GroundingSetting.ANYWHERE, GroundingSetting.PUBLIC],
                target_symptoms=["anxiety", "panic", "dissociation", "overwhelm"],
                contraindications=[],
                materials_needed=[],
                variations=[
                    "Focus on colors for visual items",
                    "Focus on textures for touch items",
                    "Use specific categories (nature, furniture, etc.)"
                ]
            ),
            
            GroundingTechnique(
                technique_id="box_breathing",
                name="Box Breathing",
                grounding_type=GroundingType.BREATHING,
                difficulty_level=DifficultyLevel.BEGINNER,
                duration_minutes=3,
                description="Breathing technique using equal counts for inhale, hold, exhale, hold",
                instructions=[
                    "Inhale for 4 counts",
                    "Hold breath for 4 counts",
                    "Exhale for 4 counts",
                    "Hold empty for 4 counts",
                    "Repeat 5-10 cycles"
                ],
                settings=[GroundingSetting.ANYWHERE],
                target_symptoms=["anxiety", "panic", "stress", "anger"],
                contraindications=["severe breathing problems", "recent surgery"],
                materials_needed=[],
                variations=[
                    "3-3-3-3 pattern for beginners",
                    "6-6-6-6 pattern for advanced",
                    "Visual square breathing with hand tracing"
                ]
            ),
            
            GroundingTechnique(
                technique_id="progressive_muscle_relaxation",
                name="Progressive Muscle Relaxation",
                grounding_type=GroundingType.PROGRESSIVE_MUSCLE,
                difficulty_level=DifficultyLevel.INTERMEDIATE,
                duration_minutes=15,
                description="Systematically tense and release muscle groups",
                instructions=[
                    "Start with your toes - tense for 5 seconds, then release",
                    "Move to your calves - tense and release",
                    "Continue up your body: thighs, abdomen, hands, arms",
                    "Finish with shoulders, neck, and face",
                    "Notice the contrast between tension and relaxation"
                ],
                settings=[GroundingSetting.HOME, GroundingSetting.PRIVATE, GroundingSetting.QUIET_SPACE],
                target_symptoms=["anxiety", "tension", "insomnia", "stress"],
                contraindications=["muscle injuries", "severe pain"],
                materials_needed=["comfortable seating or lying position"],
                variations=[
                    "Quick version focusing on main muscle groups",
                    "Mental PMR without physical tensing",
                    "Focus on specific problem areas only"
                ]
            ),
            
            GroundingTechnique(
                technique_id="cold_water_technique",
                name="Cold Water Grounding",
                grounding_type=GroundingType.TACTILE,
                difficulty_level=DifficultyLevel.BEGINNER,
                duration_minutes=2,
                description="Use cold water to activate the dive response and calm the nervous system",
                instructions=[
                    "Run cold water over your wrists",
                    "Splash cold water on your face",
                    "Hold an ice cube in your hand",
                    "Drink cold water slowly",
                    "Focus on the temperature sensation"
                ],
                settings=[GroundingSetting.HOME, GroundingSetting.WORK],
                target_symptoms=["panic", "intense emotions", "dissociation"],
                contraindications=["heart conditions", "eating disorders with purging"],
                materials_needed=["cold water", "ice cubes (optional)"],
                variations=[
                    "Cold compress on face or wrists",
                    "Cold shower or bath",
                    "Step outside in cold weather"
                ]
            ),
            
            GroundingTechnique(
                technique_id="cognitive_grounding",
                name="Cognitive Grounding Categories",
                grounding_type=GroundingType.COGNITIVE,
                difficulty_level=DifficultyLevel.BEGINNER,
                duration_minutes=5,
                description="Use mental categories to focus your mind on concrete details",
                instructions=[
                    "Choose a category (colors, animals, foods, etc.)",
                    "Name as many items in that category as possible",
                    "Go through the alphabet for each category",
                    "Switch to a new category when stuck",
                    "Focus on the mental effort of recall"
                ],
                settings=[GroundingSetting.ANYWHERE],
                target_symptoms=["racing thoughts", "anxiety", "dissociation"],
                contraindications=[],
                materials_needed=[],
                variations=[
                    "Personal categories (friends' names, places visited)",
                    "Complex categories (countries and capitals)",
                    "Rhyming words or word associations"
                ]
            ),
            
            GroundingTechnique(
                technique_id="guided_imagery_safe_place",
                name="Safe Place Visualization",
                grounding_type=GroundingType.VISUALIZATION,
                difficulty_level=DifficultyLevel.INTERMEDIATE,
                duration_minutes=10,
                description="Visualize a safe, calm place in detail to create emotional grounding",
                instructions=[
                    "Close your eyes and imagine your safe place",
                    "Notice what you see - colors, shapes, lighting",
                    "Notice what you hear - sounds, music, silence",
                    "Notice physical sensations - temperature, textures",
                    "Notice any smells or tastes",
                    "Feel the safety and calm of this place",
                    "Remember you can return here anytime"
                ],
                settings=[GroundingSetting.QUIET_SPACE, GroundingSetting.PRIVATE],
                target_symptoms=["trauma", "anxiety", "stress", "insomnia"],
                contraindications=["active psychosis", "severe dissociation"],
                materials_needed=["quiet space", "comfortable position"],
                variations=[
                    "Nature scenes (beach, forest, mountains)",
                    "Childhood safe places",
                    "Created fantasy environments"
                ]
            ),
            
            GroundingTechnique(
                technique_id="movement_grounding",
                name="Physical Movement Grounding",
                grounding_type=GroundingType.PHYSICAL_MOVEMENT,
                difficulty_level=DifficultyLevel.BEGINNER,
                duration_minutes=3,
                description="Use simple physical movements to reconnect with your body",
                instructions=[
                    "Stand up and feel your feet on the ground",
                    "March in place for 30 seconds",
                    "Do 10 jumping jacks or arm circles",
                    "Stretch your arms overhead and side to side",
                    "Roll your shoulders and neck gently",
                    "Notice how your body feels after movement"
                ],
                settings=[GroundingSetting.HOME, GroundingSetting.PRIVATE],
                target_symptoms=["dissociation", "numbness", "restlessness"],
                contraindications=["mobility limitations", "recent injuries"],
                materials_needed=["space to move"],
                variations=[
                    "Chair-based movements for limited mobility",
                    "Dance to favorite music",
                    "Yoga poses or stretches"
                ]
            ),
            
            GroundingTechnique(
                technique_id="auditory_grounding",
                name="Sound Grounding Technique",
                grounding_type=GroundingType.AUDITORY,
                difficulty_level=DifficultyLevel.BEGINNER,
                duration_minutes=5,
                description="Focus on sounds in your environment to anchor in the present",
                instructions=[
                    "Sit quietly and close your eyes",
                    "Listen for the most obvious sound",
                    "Identify more subtle sounds in the background",
                    "Notice sounds from different directions",
                    "Focus on the quality of each sound (pitch, rhythm, texture)",
                    "Return attention to sounds when mind wanders"
                ],
                settings=[GroundingSetting.ANYWHERE],
                target_symptoms=["racing thoughts", "anxiety", "hypervigilance"],
                contraindications=["hearing impairments without adaptation"],
                materials_needed=[],
                variations=[
                    "Listen to specific music or nature sounds",
                    "Use singing bowls or chimes",
                    "Practice with guided audio recordings"
                ]
            ),
            
            GroundingTechnique(
                technique_id="mindful_observation",
                name="Mindful Object Observation",
                grounding_type=GroundingType.MINDFULNESS,
                difficulty_level=DifficultyLevel.INTERMEDIATE,
                duration_minutes=7,
                description="Observe a single object with complete attention and curiosity",
                instructions=[
                    "Choose an object you can hold or see clearly",
                    "Look at it as if seeing it for the first time",
                    "Notice its shape, color, texture, weight",
                    "Observe shadows, reflections, details",
                    "If it has a scent, notice that too",
                    "When your mind wanders, gently return to the object",
                    "Spend full attention on this one thing"
                ],
                settings=[GroundingSetting.ANYWHERE],
                target_symptoms=["rumination", "worry", "disconnection"],
                contraindications=[],
                materials_needed=["any small object"],
                variations=[
                    "Natural objects (stones, leaves, flowers)",
                    "Personal meaningful items",
                    "Food items for mindful eating"
                ]
            ),
            
            GroundingTechnique(
                technique_id="emotional_grounding",
                name="Emotional Acknowledgment Grounding",
                grounding_type=GroundingType.EMOTIONAL,
                difficulty_level=DifficultyLevel.ADVANCED,
                duration_minutes=8,
                description="Acknowledge and ground yourself through difficult emotions",
                instructions=[
                    "Name the emotion you're feeling out loud",
                    "Rate its intensity from 1-10",
                    "Locate where you feel it in your body",
                    "Breathe into that area of your body",
                    "Say: 'This is anxiety (or other emotion) and it will pass'",
                    "Remind yourself: 'I am safe right now'",
                    "Notice if the intensity has changed"
                ],
                settings=[GroundingSetting.PRIVATE, GroundingSetting.QUIET_SPACE],
                target_symptoms=["intense emotions", "panic", "overwhelm"],
                contraindications=["active suicidal ideation without support"],
                materials_needed=[],
                variations=[
                    "Write emotions in a journal",
                    "Use emotion wheel for specific identification",
                    "Practice self-compassionate responses"
                ]
            )
        ]
    
    def get_technique(self, technique_id: str) -> Optional[GroundingTechnique]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM grounding_techniques WHERE technique_id = ?
            """, (technique_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return GroundingTechnique(
                technique_id=row[0],
                name=row[1],
                grounding_type=GroundingType(row[2]),
                difficulty_level=DifficultyLevel(row[3]),
                duration_minutes=row[4],
                description=row[5] or "",
                instructions=json.loads(row[6] or '[]'),
                settings=[GroundingSetting(s) for s in json.loads(row[7] or '[]')],
                target_symptoms=json.loads(row[8] or '[]'),
                contraindications=json.loads(row[9] or '[]'),
                materials_needed=json.loads(row[10] or '[]'),
                audio_cues=json.loads(row[11] or '[]'),
                variations=json.loads(row[12] or '[]'),
                effectiveness_rating=row[13],
                usage_count=row[14],
                created_date=datetime.fromisoformat(row[15])
            )
    
    def get_techniques_by_type(self, grounding_type: GroundingType) -> List[GroundingTechnique]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM grounding_techniques 
                WHERE grounding_type = ?
                ORDER BY effectiveness_rating DESC, usage_count DESC
            """, (grounding_type.value,))
            
            techniques = []
            for row in cursor.fetchall():
                technique = GroundingTechnique(
                    technique_id=row[0],
                    name=row[1],
                    grounding_type=GroundingType(row[2]),
                    difficulty_level=DifficultyLevel(row[3]),
                    duration_minutes=row[4],
                    description=row[5] or "",
                    instructions=json.loads(row[6] or '[]'),
                    settings=[GroundingSetting(s) for s in json.loads(row[7] or '[]')],
                    target_symptoms=json.loads(row[8] or '[]'),
                    contraindications=json.loads(row[9] or '[]'),
                    materials_needed=json.loads(row[10] or '[]'),
                    audio_cues=json.loads(row[11] or '[]'),
                    variations=json.loads(row[12] or '[]'),
                    effectiveness_rating=row[13],
                    usage_count=row[14],
                    created_date=datetime.fromisoformat(row[15])
                )
                techniques.append(technique)
            
            return techniques
    
    def get_recommended_techniques(
        self,
        patient_id: str,
        current_symptoms: List[str] = None,
        available_time: int = None,
        setting: GroundingSetting = None,
        difficulty_level: DifficultyLevel = None
    ) -> List[GroundingTechnique]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM grounding_techniques WHERE 1=1"
            params = []
            
            if available_time:
                query += " AND duration_minutes <= ?"
                params.append(available_time)
            
            if difficulty_level:
                query += " AND difficulty_level = ?"
                params.append(difficulty_level.value)
            
            query += " ORDER BY effectiveness_rating DESC, usage_count DESC LIMIT 10"
            
            cursor.execute(query, params)
            
            all_techniques = []
            for row in cursor.fetchall():
                technique = GroundingTechnique(
                    technique_id=row[0],
                    name=row[1],
                    grounding_type=GroundingType(row[2]),
                    difficulty_level=DifficultyLevel(row[3]),
                    duration_minutes=row[4],
                    description=row[5] or "",
                    instructions=json.loads(row[6] or '[]'),
                    settings=[GroundingSetting(s) for s in json.loads(row[7] or '[]')],
                    target_symptoms=json.loads(row[8] or '[]'),
                    contraindications=json.loads(row[9] or '[]'),
                    materials_needed=json.loads(row[10] or '[]'),
                    audio_cues=json.loads(row[11] or '[]'),
                    variations=json.loads(row[12] or '[]'),
                    effectiveness_rating=row[13],
                    usage_count=row[14],
                    created_date=datetime.fromisoformat(row[15])
                )
                all_techniques.append(technique)
        
        filtered_techniques = all_techniques
        
        if current_symptoms:
            symptom_matches = []
            for technique in all_techniques:
                matches = len(set(current_symptoms) & set(technique.target_symptoms))
                if matches > 0:
                    symptom_matches.append((technique, matches))
            
            symptom_matches.sort(key=lambda x: x[1], reverse=True)
            filtered_techniques = [t[0] for t in symptom_matches[:5]]
        
        if setting:
            filtered_techniques = [
                t for t in filtered_techniques 
                if setting in t.settings or GroundingSetting.ANYWHERE in t.settings
            ]
        
        past_sessions = self.get_patient_session_history(patient_id, days_back=30)
        technique_usage = {}
        for session in past_sessions:
            technique_usage[session.technique_id] = technique_usage.get(session.technique_id, 0) + 1
        
        def sort_key(technique):
            usage_penalty = technique_usage.get(technique.technique_id, 0) * 0.1
            effectiveness = technique.effectiveness_rating or 0
            return effectiveness - usage_penalty
        
        filtered_techniques.sort(key=sort_key, reverse=True)
        
        return filtered_techniques[:5]
    
    def start_grounding_session(
        self, 
        patient_id: str, 
        technique_id: str,
        pre_distress: int,
        symptoms: List[str] = None,
        setting: GroundingSetting = None,
        crisis_situation: bool = False
    ) -> str:
        
        session = GroundingSession(
            patient_id=patient_id,
            technique_id=technique_id,
            pre_session_distress=pre_distress,
            symptoms_before=symptoms or [],
            setting_used=setting,
            crisis_situation=crisis_situation
        )
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO grounding_sessions (
                    session_id, patient_id, technique_id, start_time,
                    end_time, duration_minutes, pre_session_distress,
                    post_session_distress, distress_reduction,
                    completion_status, symptoms_before, symptoms_after,
                    effectiveness_rating, notes, barriers_encountered,
                    setting_used, modifications_made, therapist_guided,
                    crisis_situation, created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id, session.patient_id, session.technique_id,
                session.start_time.isoformat(), None, None,
                session.pre_session_distress, None, None,
                session.completion_status, json.dumps(session.symptoms_before),
                json.dumps(session.symptoms_after), None, session.notes,
                json.dumps(session.barriers_encountered),
                session.setting_used.value if session.setting_used else None,
                json.dumps(session.modifications_made), session.therapist_guided,
                session.crisis_situation, session.created_date.isoformat(),
                session.last_updated.isoformat()
            ))
            
            cursor.execute("""
                UPDATE grounding_techniques 
                SET usage_count = usage_count + 1 
                WHERE technique_id = ?
            """, (technique_id,))
            
            conn.commit()
        
        return session.session_id
    
    def complete_grounding_session(
        self,
        session_id: str,
        post_distress: int,
        effectiveness_rating: int,
        symptoms_after: List[str] = None,
        notes: str = "",
        barriers: List[str] = None,
        modifications: List[str] = None
    ) -> bool:
        
        end_time = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT start_time FROM grounding_sessions WHERE session_id = ?
            """, (session_id,))
            
            result = cursor.fetchone()
            if not result:
                return False
            
            start_time = datetime.fromisoformat(result[0])
            duration = int((end_time - start_time).total_seconds() / 60)
            
            cursor.execute("""
                SELECT pre_session_distress FROM grounding_sessions WHERE session_id = ?
            """, (session_id,))
            
            pre_distress = cursor.fetchone()[0]
            distress_reduction = pre_distress - post_distress
            
            cursor.execute("""
                UPDATE grounding_sessions SET
                    end_time = ?,
                    duration_minutes = ?,
                    post_session_distress = ?,
                    distress_reduction = ?,
                    completion_status = 'completed',
                    symptoms_after = ?,
                    effectiveness_rating = ?,
                    notes = ?,
                    barriers_encountered = ?,
                    modifications_made = ?,
                    last_updated = ?
                WHERE session_id = ?
            """, (
                end_time.isoformat(), duration, post_distress, distress_reduction,
                json.dumps(symptoms_after or []), effectiveness_rating, notes,
                json.dumps(barriers or []), json.dumps(modifications or []),
                end_time.isoformat(), session_id
            ))
            
            cursor.execute("""
                SELECT technique_id FROM grounding_sessions WHERE session_id = ?
            """, (session_id,))
            
            technique_id = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT AVG(effectiveness_rating) FROM grounding_sessions 
                WHERE technique_id = ? AND effectiveness_rating IS NOT NULL
            """, (technique_id,))
            
            avg_effectiveness = cursor.fetchone()[0]
            
            cursor.execute("""
                UPDATE grounding_techniques 
                SET effectiveness_rating = ? 
                WHERE technique_id = ?
            """, (avg_effectiveness, technique_id))
            
            conn.commit()
        
        return True
    
    def get_patient_session_history(
        self, 
        patient_id: str,
        days_back: int = 30,
        limit: Optional[int] = None
    ) -> List[GroundingSession]:
        
        start_date = datetime.now() - timedelta(days=days_back)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM grounding_sessions 
                WHERE patient_id = ? AND start_time >= ?
                ORDER BY start_time DESC
            """
            params = [patient_id, start_date.isoformat()]
            
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            
            sessions = []
            for row in cursor.fetchall():
                session = GroundingSession(
                    session_id=row[0],
                    patient_id=row[1],
                    technique_id=row[2],
                    start_time=datetime.fromisoformat(row[3]),
                    end_time=datetime.fromisoformat(row[4]) if row[4] else None,
                    duration_minutes=row[5],
                    pre_session_distress=row[6],
                    post_session_distress=row[7],
                    distress_reduction=row[8],
                    completion_status=row[9],
                    symptoms_before=json.loads(row[10] or '[]'),
                    symptoms_after=json.loads(row[11] or '[]'),
                    effectiveness_rating=row[12],
                    notes=row[13] or "",
                    barriers_encountered=json.loads(row[14] or '[]'),
                    setting_used=GroundingSetting(row[15]) if row[15] else None,
                    modifications_made=json.loads(row[16] or '[]'),
                    therapist_guided=bool(row[17]),
                    crisis_situation=bool(row[18]),
                    created_date=datetime.fromisoformat(row[19]),
                    last_updated=datetime.fromisoformat(row[20])
                )
                sessions.append(session)
            
            return sessions
    
    def create_personalized_plan(
        self, 
        patient_id: str,
        preferences: Dict[str, Any] = None
    ) -> str:
        
        session_history = self.get_patient_session_history(patient_id, days_back=90)
        
        technique_effectiveness = {}
        technique_usage = {}
        
        for session in session_history:
            if session.effectiveness_rating:
                if session.technique_id not in technique_effectiveness:
                    technique_effectiveness[session.technique_id] = []
                technique_effectiveness[session.technique_id].append(session.effectiveness_rating)
            
            technique_usage[session.technique_id] = technique_usage.get(session.technique_id, 0) + 1
        
        preferred_techniques = []
        backup_techniques = []
        crisis_techniques = []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT technique_id FROM grounding_techniques")
            all_technique_ids = [row[0] for row in cursor.fetchall()]
        
        for technique_id in all_technique_ids:
            if technique_id in technique_effectiveness:
                avg_effectiveness = sum(technique_effectiveness[technique_id]) / len(technique_effectiveness[technique_id])
                if avg_effectiveness >= 7:
                    preferred_techniques.append(technique_id)
                elif avg_effectiveness >= 5:
                    backup_techniques.append(technique_id)
        
        crisis_sessions = [s for s in session_history if s.crisis_situation]
        for session in crisis_sessions:
            if session.effectiveness_rating and session.effectiveness_rating >= 6:
                if session.technique_id not in crisis_techniques:
                    crisis_techniques.append(session.technique_id)
        
        if not preferred_techniques:
            preferred_techniques = ["5_4_3_2_1_sensory", "box_breathing", "cold_water_technique"]
        
        if not backup_techniques:
            backup_techniques = ["progressive_muscle_relaxation", "cognitive_grounding", "movement_grounding"]
        
        if not crisis_techniques:
            crisis_techniques = ["cold_water_technique", "box_breathing", "5_4_3_2_1_sensory"]
        
        daily_schedule = {
            "morning": ["mindful_observation"],
            "afternoon": ["box_breathing"],
            "evening": ["progressive_muscle_relaxation"],
            "crisis": crisis_techniques[:3]
        }
        
        trigger_plan = {
            "anxiety": preferred_techniques[0] if preferred_techniques else "box_breathing",
            "panic": crisis_techniques[0] if crisis_techniques else "cold_water_technique",
            "overwhelm": "5_4_3_2_1_sensory",
            "anger": "cold_water_technique",
            "dissociation": "movement_grounding"
        }
        
        plan = GroundingPlan(
            patient_id=patient_id,
            preferred_techniques=preferred_techniques[:5],
            backup_techniques=backup_techniques[:5],
            crisis_techniques=crisis_techniques[:3],
            daily_practice_schedule=daily_schedule,
            trigger_response_plan=trigger_plan
        )
        
        self._save_grounding_plan(plan)
        return plan.plan_id
    
    def _save_grounding_plan(self, plan: GroundingPlan):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO grounding_plans (
                    plan_id, patient_id, preferred_techniques, backup_techniques,
                    crisis_techniques, daily_practice_schedule, trigger_response_plan,
                    personalization_notes, adaptations, created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plan.plan_id, plan.patient_id,
                json.dumps(plan.preferred_techniques),
                json.dumps(plan.backup_techniques),
                json.dumps(plan.crisis_techniques),
                json.dumps(plan.daily_practice_schedule),
                json.dumps(plan.trigger_response_plan),
                plan.personalization_notes,
                json.dumps(plan.adaptations),
                plan.created_date.isoformat(),
                plan.last_updated.isoformat()
            ))
            
            conn.commit()
    
    def get_grounding_plan(self, patient_id: str) -> Optional[GroundingPlan]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM grounding_plans 
                WHERE patient_id = ? 
                ORDER BY created_date DESC 
                LIMIT 1
            """, (patient_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return GroundingPlan(
                plan_id=row[0],
                patient_id=row[1],
                preferred_techniques=json.loads(row[2] or '[]'),
                backup_techniques=json.loads(row[3] or '[]'),
                crisis_techniques=json.loads(row[4] or '[]'),
                daily_practice_schedule=json.loads(row[5] or '{}'),
                trigger_response_plan=json.loads(row[6] or '{}'),
                personalization_notes=row[7] or "",
                adaptations=json.loads(row[8] or '[]'),
                created_date=datetime.fromisoformat(row[9]),
                last_updated=datetime.fromisoformat(row[10])
            )
    
    def get_technique_for_situation(
        self,
        patient_id: str,
        current_distress: int,
        available_time: int,
        setting: GroundingSetting,
        symptoms: List[str] = None
    ) -> Optional[GroundingTechnique]:
        
        plan = self.get_grounding_plan(patient_id)
        
        if current_distress >= 8:
            technique_pool = plan.crisis_techniques if plan else ["cold_water_technique", "box_breathing"]
        elif current_distress >= 6:
            technique_pool = plan.preferred_techniques if plan else ["5_4_3_2_1_sensory", "box_breathing"]
        else:
            technique_pool = plan.backup_techniques if plan else ["mindful_observation", "progressive_muscle_relaxation"]
        
        suitable_techniques = []
        for technique_id in technique_pool:
            technique = self.get_technique(technique_id)
            if technique:
                if technique.duration_minutes <= available_time:
                    if setting in technique.settings or GroundingSetting.ANYWHERE in technique.settings:
                        if symptoms:
                            if any(symptom in technique.target_symptoms for symptom in symptoms):
                                suitable_techniques.append(technique)
                        else:
                            suitable_techniques.append(technique)
        
        if not suitable_techniques:
            return self.get_technique("5_4_3_2_1_sensory")
        
        recent_usage = {}
        recent_sessions = self.get_patient_session_history(patient_id, days_back=7)
        for session in recent_sessions:
            recent_usage[session.technique_id] = recent_usage.get(session.technique_id, 0) + 1
        
        least_used = min(suitable_techniques, key=lambda t: recent_usage.get(t.technique_id, 0))
        return least_used
    
    def generate_progress_report(self, patient_id: str, days_back: int = 30) -> Dict[str, Any]:
        sessions = self.get_patient_session_history(patient_id, days_back)
        
        if not sessions:
            return {
                "patient_id": patient_id,
                "period_days": days_back,
                "total_sessions": 0,
                "message": "No grounding sessions recorded in this period"
            }
        
        total_sessions = len(sessions)
        completed_sessions = len([s for s in sessions if s.completion_status == "completed"])
        completion_rate = completed_sessions / total_sessions if total_sessions > 0 else 0
        
        distress_reductions = [s.distress_reduction for s in sessions if s.distress_reduction is not None]
        avg_distress_reduction = sum(distress_reductions) / len(distress_reductions) if distress_reductions else 0
        
        effectiveness_ratings = [s.effectiveness_rating for s in sessions if s.effectiveness_rating is not None]
        avg_effectiveness = sum(effectiveness_ratings) / len(effectiveness_ratings) if effectiveness_ratings else 0
        
        technique_usage = {}
        technique_effectiveness = {}
        
        for session in sessions:
            technique_usage[session.technique_id] = technique_usage.get(session.technique_id, 0) + 1
            
            if session.effectiveness_rating:
                if session.technique_id not in technique_effectiveness:
                    technique_effectiveness[session.technique_id] = []
                technique_effectiveness[session.technique_id].append(session.effectiveness_rating)
        
        most_used_techniques = sorted(technique_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        
        most_effective_techniques = []
        for technique_id, ratings in technique_effectiveness.items():
            avg_rating = sum(ratings) / len(ratings)
            technique = self.get_technique(technique_id)
            technique_name = technique.name if technique else technique_id
            most_effective_techniques.append((technique_name, avg_rating, len(ratings)))
        
        most_effective_techniques.sort(key=lambda x: x[1], reverse=True)
        most_effective_techniques = most_effective_techniques[:5]
        
        crisis_sessions = [s for s in sessions if s.crisis_situation]
        crisis_effectiveness = 0
        if crisis_sessions:
            crisis_ratings = [s.effectiveness_rating for s in crisis_sessions if s.effectiveness_rating]
            crisis_effectiveness = sum(crisis_ratings) / len(crisis_ratings) if crisis_ratings else 0
        
        common_barriers = {}
        for session in sessions:
            for barrier in session.barriers_encountered:
                common_barriers[barrier] = common_barriers.get(barrier, 0) + 1
        
        top_barriers = sorted(common_barriers.items(), key=lambda x: x[1], reverse=True)[:3]
        
        weekly_usage = {}
        for session in sessions:
            week = session.start_time.isocalendar()[1]
            weekly_usage[week] = weekly_usage.get(week, 0) + 1
        
        usage_trend = "stable"
        if len(weekly_usage) >= 2:
            weeks = sorted(weekly_usage.keys())
            early_avg = sum(weekly_usage[w] for w in weeks[:len(weeks)//2]) / (len(weeks)//2)
            late_avg = sum(weekly_usage[w] for w in weeks[len(weeks)//2:]) / (len(weeks) - len(weeks)//2)
            
            if late_avg > early_avg * 1.2:
                usage_trend = "increasing"
            elif late_avg < early_avg * 0.8:
                usage_trend = "decreasing"
        
        insights = []
        
        if completion_rate < 0.7:
            insights.append("Low session completion rate suggests need for shorter or simpler techniques")
        
        if avg_distress_reduction < 2:
            insights.append("Limited distress reduction indicates need for technique modification or alternative approaches")
        
        if avg_effectiveness >= 7:
            insights.append("High effectiveness ratings show good technique matching and engagement")
        
        if len(crisis_sessions) > len(sessions) * 0.3:
            insights.append("High proportion of crisis sessions suggests need for preventive strategies")
        
        if crisis_effectiveness < 5:
            insights.append("Crisis techniques showing low effectiveness - consider technique training or alternatives")
        
        return {
            "patient_id": patient_id,
            "analysis_period": {
                "days_back": days_back,
                "start_date": (datetime.now() - timedelta(days=days_back)).isoformat(),
                "end_date": datetime.now().isoformat()
            },
            "session_statistics": {
                "total_sessions": total_sessions,
                "completed_sessions": completed_sessions,
                "completion_rate": round(completion_rate, 2),
                "average_distress_reduction": round(avg_distress_reduction, 2),
                "average_effectiveness": round(avg_effectiveness, 2)
            },
            "technique_analysis": {
                "most_used": [{"technique_id": t[0], "usage_count": t[1]} for t in most_used_techniques],
                "most_effective": [{"technique": t[0], "avg_rating": round(t[1], 2), "session_count": t[2]} for t in most_effective_techniques]
            },
            "crisis_management": {
                "crisis_sessions": len(crisis_sessions),
                "crisis_effectiveness": round(crisis_effectiveness, 2),
                "crisis_rate": round(len(crisis_sessions) / total_sessions, 2) if total_sessions > 0 else 0
            },
            "barriers_and_challenges": [{"barrier": b[0], "frequency": b[1]} for b in top_barriers],
            "usage_patterns": {
                "trend": usage_trend,
                "weekly_usage": dict(weekly_usage)
            },
            "therapeutic_insights": insights,
            "recommendations": self._generate_recommendations(sessions, technique_effectiveness)
        }
    
    def _generate_recommendations(
        self, 
        sessions: List[GroundingSession], 
        technique_effectiveness: Dict[str, List[int]]
    ) -> List[str]:
        
        recommendations = []
        
        if not sessions:
            recommendations.append("Begin regular grounding practice with basic techniques")
            return recommendations
        
        avg_effectiveness = {}
        for technique_id, ratings in technique_effectiveness.items():
            avg_effectiveness[technique_id] = sum(ratings) / len(ratings)
        
        low_effectiveness = [t for t, avg in avg_effectiveness.items() if avg < 5]
        if low_effectiveness:
            recommendations.append(f"Consider replacing techniques with low effectiveness: {', '.join(low_effectiveness[:3])}")
        
        high_effectiveness = [t for t, avg in avg_effectiveness.items() if avg >= 8]
        if high_effectiveness:
            recommendations.append(f"Continue using highly effective techniques: {', '.join(high_effectiveness[:3])}")
        
        incomplete_sessions = [s for s in sessions if s.completion_status != "completed"]
        if len(incomplete_sessions) > len(sessions) * 0.3:
            recommendations.append("Focus on shorter techniques to improve completion rates")
        
        recent_sessions = [s for s in sessions if (datetime.now() - s.start_time).days <= 7]
        if len(recent_sessions) < 3:
            recommendations.append("Increase frequency of grounding practice for better results")
        
        crisis_sessions = [s for s in sessions if s.crisis_situation]
        if crisis_sessions and len(crisis_sessions) > len(sessions) * 0.4:
            recommendations.append("Develop preventive grounding routine to reduce crisis situations")
        
        technique_variety = len(set(s.technique_id for s in sessions))
        if technique_variety < 3:
            recommendations.append("Try variety in grounding techniques to find optimal matches")
        
        return recommendations
    
    def get_guided_session_script(self, technique_id: str) -> Dict[str, Any]:
        technique = self.get_technique(technique_id)
        if not technique:
            return {}
        
        scripts = {
            "5_4_3_2_1_sensory": {
                "introduction": "We're going to practice the 5-4-3-2-1 grounding technique. This helps bring your attention to the present moment through your senses.",
                "steps": [
                    {
                        "instruction": "Look around and name 5 things you can see",
                        "pause_seconds": 30,
                        "guidance": "Take your time. Really notice the colors, shapes, and details of each item."
                    },
                    {
                        "instruction": "Now find 4 things you can touch or feel",
                        "pause_seconds": 25,
                        "guidance": "This could be your clothes, chair, a wall, or any texture around you."
                    },
                    {
                        "instruction": "Listen for 3 things you can hear",
                        "pause_seconds": 20,
                        "guidance": "These might be obvious sounds or very quiet background noises."
                    },
                    {
                        "instruction": "Notice 2 things you can smell",
                        "pause_seconds": 15,
                        "guidance": "If you can't smell anything obvious, that's okay. Even the absence of smell counts."
                    },
                    {
                        "instruction": "Find 1 thing you can taste",
                        "pause_seconds": 10,
                        "guidance": "This might be lingering taste, or just the taste in your mouth right now."
                    }
                ],
                "closing": "Take a moment to notice how you feel now. You've successfully grounded yourself in the present moment."
            },
            
            "box_breathing": {
                "introduction": "We'll practice box breathing. This technique calms your nervous system through controlled breathing.",
                "steps": [
                    {
                        "instruction": "Get comfortable and close your eyes if you'd like",
                        "pause_seconds": 5,
                        "guidance": "Find a position where you can breathe easily."
                    },
                    {
                        "instruction": "Breathe in for 4 counts: 1... 2... 3... 4",
                        "pause_seconds": 4,
                        "guidance": "Fill your lungs completely but comfortably."
                    },
                    {
                        "instruction": "Hold your breath for 4 counts: 1... 2... 3... 4",
                        "pause_seconds": 4,
                        "guidance": "Keep the air in your lungs gently, don't strain."
                    },
                    {
                        "instruction": "Exhale for 4 counts: 1... 2... 3... 4",
                        "pause_seconds": 4,
                        "guidance": "Let the air out slowly and completely."
                    },
                    {
                        "instruction": "Hold empty for 4 counts: 1... 2... 3... 4",
                        "pause_seconds": 4,
                        "guidance": "Rest with empty lungs before the next breath."
                    }
                ],
                "repeat_cycles": 5,
                "closing": "Notice the calm feeling in your body. Your nervous system is now more relaxed."
            }
        }
        
        return scripts.get(technique_id, {
            "introduction": f"Let's practice {technique.name}.",
            "steps": [{"instruction": instruction, "pause_seconds": 10} for instruction in technique.instructions],
            "closing": "Take a moment to notice any changes in how you feel."
        })
    
    def get_emergency_grounding_sequence(self, patient_id: str) -> List[Dict[str, Any]]:
        plan = self.get_grounding_plan(patient_id)
        
        if plan and plan.crisis_techniques:
            crisis_technique_ids = plan.crisis_techniques[:3]
        else:
            crisis_technique_ids = ["cold_water_technique", "box_breathing", "5_4_3_2_1_sensory"]
        
        sequence = []
        for technique_id in crisis_technique_ids:
            technique = self.get_technique(technique_id)
            if technique:
                sequence.append({
                    "technique_id": technique_id,
                    "name": technique.name,
                    "duration_minutes": technique.duration_minutes,
                    "instructions": technique.instructions[:3],
                    "quick_description": technique.description
                })
        
        return sequence
    
    def log_technique_feedback(
        self,
        technique_id: str,
        feedback_type: str,
        feedback_text: str,
        patient_id: Optional[str] = None
    ):
        feedback_entry = {
            "technique_id": technique_id,
            "feedback_type": feedback_type,
            "feedback_text": feedback_text,
            "patient_id": patient_id,
            "timestamp": datetime.now().isoformat()
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS technique_feedback (
                    feedback_id TEXT PRIMARY KEY,
                    technique_id TEXT NOT NULL,
                    feedback_type TEXT NOT NULL,
                    feedback_text TEXT,
                    patient_id TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (technique_id) REFERENCES grounding_techniques (technique_id)
                )
            """)
            
            cursor.execute("""
                INSERT INTO technique_feedback (
                    feedback_id, technique_id, feedback_type, feedback_text,
                    patient_id, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()), technique_id, feedback_type, feedback_text,
                patient_id, feedback_entry["timestamp"]
            ))
            
            conn.commit()


def get_quick_grounding_techniques(distress_level: int, time_available: int) -> List[str]:
    quick_techniques = {
        "high_distress": ["cold_water_technique", "box_breathing", "5_4_3_2_1_sensory"],
        "medium_distress": ["5_4_3_2_1_sensory", "cognitive_grounding", "movement_grounding"],
        "low_distress": ["mindful_observation", "progressive_muscle_relaxation", "guided_imagery_safe_place"]
    }
    
    if distress_level >= 7:
        base_techniques = quick_techniques["high_distress"]
    elif distress_level >= 4:
        base_techniques = quick_techniques["medium_distress"]
    else:
        base_techniques = quick_techniques["low_distress"]
    
    duration_limits = {
        "cold_water_technique": 2,
        "box_breathing": 3,
        "5_4_3_2_1_sensory": 5,
        "cognitive_grounding": 5,
        "movement_grounding": 3,
        "mindful_observation": 7,
        "progressive_muscle_relaxation": 15,
        "guided_imagery_safe_place": 10
    }
    
    suitable_techniques = [
        technique for technique in base_techniques
        if duration_limits.get(technique, 5) <= time_available
    ]
    
    return suitable_techniques[:3]


if __name__ == "__main__":
    library = GroundingTechniqueLibrary()
    
    patient_id = "test_patient_001"
    
    session_id = library.start_grounding_session(
        patient_id=patient_id,
        technique_id="5_4_3_2_1_sensory",
        pre_distress=8,
        symptoms=["anxiety", "panic"],
        setting=GroundingSetting.HOME
    )
    
    library.complete_grounding_session(
        session_id=session_id,
        post_distress=4,
        effectiveness_rating=7,
        symptoms_after=["mild anxiety"],
        notes="Technique worked well, felt much calmer"
    )
    
    plan_id = library.create_personalized_plan(patient_id)
    report = library.generate_progress_report(patient_id, 30)
    
    print(f"Session completed: {session_id}")
    print(f"Plan created: {plan_id}")
    print(f"Progress report generated with {report['session_statistics']['total_sessions']} sessions")
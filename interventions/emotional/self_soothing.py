import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid
import random
from pathlib import Path


class SoothingCategory(Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    TACTILE = "tactile"
    OLFACTORY = "olfactory"
    GUSTATORY = "gustatory"
    MOVEMENT = "movement"
    COGNITIVE = "cognitive"
    CREATIVE = "creative"
    SPIRITUAL = "spiritual"
    SOCIAL = "social"


class IntensityLevel(Enum):
    GENTLE = "gentle"
    MODERATE = "moderate"
    INTENSE = "intense"


class AccessibilityLevel(Enum):
    IMMEDIATE = "immediate"
    QUICK_SETUP = "quick_setup"
    REQUIRES_PREPARATION = "requires_preparation"


class SoothingContext(Enum):
    STRESS = "stress"
    ANXIETY = "anxiety"
    SADNESS = "sadness"
    ANGER = "anger"
    OVERWHELM = "overwhelm"
    LONELINESS = "loneliness"
    INSOMNIA = "insomnia"
    PAIN = "pain"
    TRAUMA_RESPONSE = "trauma_response"
    GENERAL_DISTRESS = "general_distress"


@dataclass
class SoothingActivity:
    activity_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    category: SoothingCategory = SoothingCategory.TACTILE
    description: str = ""
    
    detailed_instructions: List[str] = field(default_factory=list)
    materials_needed: List[str] = field(default_factory=list)
    setup_time_minutes: int = 0
    duration_minutes: int = 10
    
    intensity_level: IntensityLevel = IntensityLevel.GENTLE
    accessibility: AccessibilityLevel = AccessibilityLevel.IMMEDIATE
    
    target_contexts: List[SoothingContext] = field(default_factory=list)
    contraindications: List[str] = field(default_factory=list)
    
    personalization_options: List[str] = field(default_factory=list)
    variations: List[str] = field(default_factory=list)
    
    effectiveness_rating: Optional[float] = None
    usage_count: int = 0
    
    cost_level: str = "free"
    indoor_outdoor: str = "both"
    alone_social: str = "alone"
    
    created_date: datetime = field(default_factory=datetime.now)


@dataclass
class SoothingSession:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    activity_id: str = ""
    
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    planned_duration: int = 0
    actual_duration: Optional[int] = None
    
    pre_distress_level: int = 0
    post_distress_level: Optional[int] = None
    pre_emotions: List[str] = field(default_factory=list)
    post_emotions: List[str] = field(default_factory=list)
    
    context: SoothingContext = SoothingContext.GENERAL_DISTRESS
    trigger_event: str = ""
    
    effectiveness_rating: Optional[int] = None
    enjoyment_rating: Optional[int] = None
    
    modifications_made: List[str] = field(default_factory=list)
    barriers_encountered: List[str] = field(default_factory=list)
    
    notes: str = ""
    would_repeat: Optional[bool] = None
    
    completed: bool = False
    interrupted_reason: str = ""
    
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class SoothingKit:
    kit_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    name: str = ""
    
    emergency_activities: List[str] = field(default_factory=list)
    daily_comfort_activities: List[str] = field(default_factory=list)
    bedtime_activities: List[str] = field(default_factory=list)
    
    physical_comfort_items: List[str] = field(default_factory=list)
    digital_resources: List[str] = field(default_factory=list)
    
    personalized_triggers: Dict[str, List[str]] = field(default_factory=dict)
    backup_options: List[str] = field(default_factory=list)
    
    location_specific: Dict[str, List[str]] = field(default_factory=dict)
    
    last_updated: datetime = field(default_factory=datetime.now)
    created_date: datetime = field(default_factory=datetime.now)


@dataclass
class SoothingPlan:
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    
    morning_routine: List[str] = field(default_factory=list)
    evening_routine: List[str] = field(default_factory=list)
    stress_response_sequence: List[str] = field(default_factory=list)
    
    weekly_schedule: Dict[str, List[str]] = field(default_factory=dict)
    situational_responses: Dict[str, List[str]] = field(default_factory=dict)
    
    preferred_categories: List[SoothingCategory] = field(default_factory=list)
    avoided_categories: List[SoothingCategory] = field(default_factory=list)
    
    goals: List[str] = field(default_factory=list)
    progress_metrics: List[str] = field(default_factory=list)
    
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


class SelfSoothingSystem:
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self._initialize_database()
        self._populate_default_activities()
    
    def _initialize_database(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS soothing_activities (
                    activity_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    detailed_instructions TEXT,
                    materials_needed TEXT,
                    setup_time_minutes INTEGER,
                    duration_minutes INTEGER,
                    intensity_level TEXT,
                    accessibility TEXT,
                    target_contexts TEXT,
                    contraindications TEXT,
                    personalization_options TEXT,
                    variations TEXT,
                    effectiveness_rating REAL,
                    usage_count INTEGER DEFAULT 0,
                    cost_level TEXT,
                    indoor_outdoor TEXT,
                    alone_social TEXT,
                    created_date TEXT NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS soothing_sessions (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    activity_id TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    planned_duration INTEGER,
                    actual_duration INTEGER,
                    pre_distress_level INTEGER,
                    post_distress_level INTEGER,
                    pre_emotions TEXT,
                    post_emotions TEXT,
                    context TEXT,
                    trigger_event TEXT,
                    effectiveness_rating INTEGER,
                    enjoyment_rating INTEGER,
                    modifications_made TEXT,
                    barriers_encountered TEXT,
                    notes TEXT,
                    would_repeat BOOLEAN,
                    completed BOOLEAN,
                    interrupted_reason TEXT,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                    FOREIGN KEY (activity_id) REFERENCES soothing_activities (activity_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS soothing_kits (
                    kit_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    emergency_activities TEXT,
                    daily_comfort_activities TEXT,
                    bedtime_activities TEXT,
                    physical_comfort_items TEXT,
                    digital_resources TEXT,
                    personalized_triggers TEXT,
                    backup_options TEXT,
                    location_specific TEXT,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS soothing_plans (
                    plan_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    morning_routine TEXT,
                    evening_routine TEXT,
                    stress_response_sequence TEXT,
                    weekly_schedule TEXT,
                    situational_responses TEXT,
                    preferred_categories TEXT,
                    avoided_categories TEXT,
                    goals TEXT,
                    progress_metrics TEXT,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            conn.commit()
    
    def _populate_default_activities(self):
        default_activities = self._get_default_activities()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for activity in default_activities:
                cursor.execute("""
                    INSERT OR IGNORE INTO soothing_activities (
                        activity_id, name, category, description, detailed_instructions,
                        materials_needed, setup_time_minutes, duration_minutes,
                        intensity_level, accessibility, target_contexts,
                        contraindications, personalization_options, variations,
                        effectiveness_rating, usage_count, cost_level,
                        indoor_outdoor, alone_social, created_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    activity.activity_id, activity.name, activity.category.value,
                    activity.description, json.dumps(activity.detailed_instructions),
                    json.dumps(activity.materials_needed), activity.setup_time_minutes,
                    activity.duration_minutes, activity.intensity_level.value,
                    activity.accessibility.value,
                    json.dumps([c.value for c in activity.target_contexts]),
                    json.dumps(activity.contraindications),
                    json.dumps(activity.personalization_options),
                    json.dumps(activity.variations), activity.effectiveness_rating,
                    activity.usage_count, activity.cost_level,
                    activity.indoor_outdoor, activity.alone_social,
                    activity.created_date.isoformat()
                ))
            
            conn.commit()
    
    def _get_default_activities(self) -> List[SoothingActivity]:
        return [
            SoothingActivity(
                activity_id="warm_bath_ritual",
                name="Warm Bath Ritual",
                category=SoothingCategory.TACTILE,
                description="A calming warm bath with optional aromatherapy and mindful soaking",
                detailed_instructions=[
                    "Fill bathtub with comfortably warm water",
                    "Add Epsom salts, essential oils, or bath bubbles if desired",
                    "Dim lights or light candles for ambiance",
                    "Soak for 15-20 minutes focusing on the warmth",
                    "Practice deep breathing while soaking",
                    "After bath, wrap in a soft towel or robe"
                ],
                materials_needed=["bathtub", "warm water", "towels", "optional: bath salts, oils"],
                setup_time_minutes=5,
                duration_minutes=20,
                intensity_level=IntensityLevel.MODERATE,
                accessibility=AccessibilityLevel.QUICK_SETUP,
                target_contexts=[SoothingContext.STRESS, SoothingContext.ANXIETY, SoothingContext.PAIN],
                indoor_outdoor="indoor"
            ),
            
            SoothingActivity(
                activity_id="soft_blanket_cocoon",
                name="Soft Blanket Cocoon",
                category=SoothingCategory.TACTILE,
                description="Wrapping yourself in the softest blanket or weighted blanket for comfort",
                detailed_instructions=[
                    "Choose your softest, most comforting blanket",
                    "Find a comfortable position on couch or bed",
                    "Wrap blanket around entire body like a cocoon",
                    "Focus on the texture and weight of the blanket",
                    "Allow yourself to feel completely enclosed and safe",
                    "Stay wrapped for as long as feels good"
                ],
                materials_needed=["soft blanket or weighted blanket"],
                setup_time_minutes=1,
                duration_minutes=15,
                intensity_level=IntensityLevel.GENTLE,
                accessibility=AccessibilityLevel.IMMEDIATE,
                target_contexts=[SoothingContext.ANXIETY, SoothingContext.OVERWHELM, SoothingContext.TRAUMA_RESPONSE],
                indoor_outdoor="indoor"
            ),
            
            SoothingActivity(
                activity_id="nature_sounds_meditation",
                name="Nature Sounds Meditation",
                category=SoothingCategory.AUDITORY,
                description="Listening to calming nature sounds while practicing mindful awareness",
                detailed_instructions=[
                    "Choose nature sounds (rain, ocean, forest, etc.)",
                    "Find comfortable position with eyes closed",
                    "Play sounds at comfortable volume",
                    "Focus entirely on the sounds",
                    "When mind wanders, return to listening",
                    "Allow sounds to wash over you completely"
                ],
                materials_needed=["speaker or headphones", "nature sound recordings"],
                setup_time_minutes=2,
                duration_minutes=10,
                intensity_level=IntensityLevel.GENTLE,
                accessibility=AccessibilityLevel.IMMEDIATE,
                target_contexts=[SoothingContext.STRESS, SoothingContext.INSOMNIA, SoothingContext.ANXIETY],
                indoor_outdoor="both"
            ),
            
            SoothingActivity(
                activity_id="comfort_food_mindful_eating",
                name="Mindful Comfort Food",
                category=SoothingCategory.GUSTATORY,
                description="Slowly and mindfully enjoying a favorite comfort food or drink",
                detailed_instructions=[
                    "Choose a healthy comfort food or warm drink",
                    "Prepare it with care and attention",
                    "Sit in comfortable space without distractions",
                    "Notice colors, textures, and aromas",
                    "Eat or drink very slowly",
                    "Focus on taste sensations and comfort feelings"
                ],
                materials_needed=["favorite comfort food/drink"],
                setup_time_minutes=5,
                duration_minutes=15,
                intensity_level=IntensityLevel.GENTLE,
                accessibility=AccessibilityLevel.QUICK_SETUP,
                target_contexts=[SoothingContext.SADNESS, SoothingContext.LONELINESS, SoothingContext.STRESS],
                contraindications=["eating disorders", "dietary restrictions"]
            ),
            
            SoothingActivity(
                activity_id="aromatherapy_breathing",
                name="Aromatherapy Deep Breathing",
                category=SoothingCategory.OLFACTORY,
                description="Combining calming scents with deep breathing exercises",
                detailed_instructions=[
                    "Choose calming essential oil or scented item",
                    "Apply oil to wrists or use diffuser",
                    "Sit comfortably and close eyes",
                    "Inhale deeply through nose, focusing on scent",
                    "Exhale slowly through mouth",
                    "Continue for 10-15 breaths, staying present with scent"
                ],
                materials_needed=["essential oils", "diffuser or cotton ball"],
                setup_time_minutes=3,
                duration_minutes=8,
                intensity_level=IntensityLevel.GENTLE,
                accessibility=AccessibilityLevel.QUICK_SETUP,
                target_contexts=[SoothingContext.ANXIETY, SoothingContext.STRESS, SoothingContext.INSOMNIA],
                contraindications=["scent sensitivities", "respiratory issues"]
            ),
            
            SoothingActivity(
                activity_id="gentle_self_massage",
                name="Gentle Self-Massage",
                category=SoothingCategory.TACTILE,
                description="Soothing self-massage focusing on hands, feet, neck, or shoulders",
                detailed_instructions=[
                    "Choose area to massage (hands, feet, neck, shoulders)",
                    "Use lotion or oil if desired",
                    "Start with gentle circular motions",
                    "Apply comfortable pressure",
                    "Focus on the sensation of touch",
                    "Spend extra time on areas that feel tense",
                    "End with gentle stroking motions"
                ],
                materials_needed=["optional: massage oil or lotion"],
                setup_time_minutes=1,
                duration_minutes=12,
                intensity_level=IntensityLevel.MODERATE,
                accessibility=AccessibilityLevel.IMMEDIATE,
                target_contexts=[SoothingContext.STRESS, SoothingContext.PAIN, SoothingContext.ANXIETY],
                indoor_outdoor="both"
            ),
            
            SoothingActivity(
                activity_id="creative_coloring",
                name="Mindful Coloring",
                category=SoothingCategory.CREATIVE,
                description="Engaging in meditative coloring with focus on the process",
                detailed_instructions=[
                    "Choose adult coloring book or mandala design",
                    "Select colored pencils, markers, or crayons",
                    "Find quiet, comfortable space with good lighting",
                    "Begin coloring without pressure for perfection",
                    "Focus on color choices and movements",
                    "Allow mind to quiet as you color",
                    "Take breaks to appreciate your progress"
                ],
                materials_needed=["coloring books/pages", "coloring supplies"],
                setup_time_minutes=3,
                duration_minutes=20,
                intensity_level=IntensityLevel.GENTLE,
                accessibility=AccessibilityLevel.QUICK_SETUP,
                target_contexts=[SoothingContext.ANXIETY, SoothingContext.OVERWHELM, SoothingContext.STRESS]
            ),
            
            SoothingActivity(
                activity_id="photo_memory_viewing",
                name="Comforting Photo Memories",
                category=SoothingCategory.VISUAL,
                description="Looking through favorite photos that evoke positive memories and feelings",
                detailed_instructions=[
                    "Gather favorite photos (physical or digital)",
                    "Find comfortable, quiet space",
                    "Look at each photo slowly and mindfully",
                    "Allow positive memories to surface",
                    "Notice feelings of warmth and connection",
                    "Spend extra time with most meaningful images",
                    "End by expressing gratitude for these memories"
                ],
                materials_needed=["photo collection (physical or device)"],
                setup_time_minutes=2,
                duration_minutes=15,
                intensity_level=IntensityLevel.GENTLE,
                accessibility=AccessibilityLevel.IMMEDIATE,
                target_contexts=[SoothingContext.SADNESS, SoothingContext.LONELINESS, SoothingContext.GENERAL_DISTRESS],
                indoor_outdoor="both"
            ),
            
            SoothingActivity(
                activity_id="gentle_stretching",
                name="Gentle Stretching Flow",
                category=SoothingCategory.MOVEMENT,
                description="Slow, gentle stretches focusing on releasing tension",
                detailed_instructions=[
                    "Find comfortable space to move freely",
                    "Start with gentle neck rolls",
                    "Slowly stretch arms overhead and to sides",
                    "Do gentle spinal twists while seated or standing",
                    "Stretch legs and feet if able",
                    "Focus on breath and sensation of release",
                    "Move slowly and listen to your body"
                ],
                materials_needed=["comfortable clothing", "optional: yoga mat"],
                setup_time_minutes=2,
                duration_minutes=10,
                intensity_level=IntensityLevel.GENTLE,
                accessibility=AccessibilityLevel.IMMEDIATE,
                target_contexts=[SoothingContext.STRESS, SoothingContext.PAIN, SoothingContext.ANXIETY],
                contraindications=["severe mobility limitations", "recent injuries"]
            ),
            
            SoothingActivity(
                activity_id="gratitude_journaling",
                name="Gratitude Journaling",
                category=SoothingCategory.COGNITIVE,
                description="Writing down things you're grateful for to shift focus to positive aspects",
                detailed_instructions=[
                    "Get comfortable with journal or paper",
                    "Write date at top of page",
                    "List 3-5 things you're grateful for today",
                    "Write why each item brings gratitude",
                    "Include small daily pleasures and big life gifts",
                    "Read through list when finished",
                    "Notice any shift in mood or perspective"
                ],
                materials_needed=["journal or paper", "pen"],
                setup_time_minutes=1,
                duration_minutes=8,
                intensity_level=IntensityLevel.GENTLE,
                accessibility=AccessibilityLevel.IMMEDIATE,
                target_contexts=[SoothingContext.SADNESS, SoothingContext.OVERWHELM, SoothingContext.GENERAL_DISTRESS],
                indoor_outdoor="both"
            ),
            
            SoothingActivity(
                activity_id="pet_companion_time",
                name="Pet Companion Time",
                category=SoothingCategory.SOCIAL,
                description="Spending focused, mindful time with a pet for mutual comfort",
                detailed_instructions=[
                    "Sit comfortably with your pet",
                    "Give full attention to your companion",
                    "Pet gently while focusing on their fur texture",
                    "Notice their breathing and warmth",
                    "Talk softly or simply be present together",
                    "Allow yourself to receive their comfort",
                    "Appreciate the bond you share"
                ],
                materials_needed=["pet"],
                setup_time_minutes=0,
                duration_minutes=15,
                intensity_level=IntensityLevel.GENTLE,
                accessibility=AccessibilityLevel.IMMEDIATE,
                target_contexts=[SoothingContext.LONELINESS, SoothingContext.SADNESS, SoothingContext.STRESS],
                alone_social="social"
            ),
            
            SoothingActivity(
                activity_id="comfort_music_listening",
                name="Comfort Music Listening",
                category=SoothingCategory.AUDITORY,
                description="Listening to personally meaningful, comforting music with full attention",
                detailed_instructions=[
                    "Choose music that feels comforting and meaningful",
                    "Use good quality headphones or speakers",
                    "Lie down or sit in most comfortable position",
                    "Close eyes and focus entirely on music",
                    "Notice different instruments and melodies",
                    "Allow emotions to flow naturally",
                    "Stay present with each song"
                ],
                materials_needed=["music collection", "headphones/speakers"],
                setup_time_minutes=2,
                duration_minutes=20,
                intensity_level=IntensityLevel.MODERATE,
                accessibility=AccessibilityLevel.IMMEDIATE,
                target_contexts=[SoothingContext.SADNESS, SoothingContext.LONELINESS, SoothingContext.STRESS],
                indoor_outdoor="both"
            ),
            
            SoothingActivity(
                activity_id="visualization_safe_place",
                name="Safe Place Visualization",
                category=SoothingCategory.COGNITIVE,
                description="Mentally visiting a personally meaningful safe and peaceful place",
                detailed_instructions=[
                    "Find quiet space and comfortable position",
                    "Close eyes and take several deep breaths",
                    "Imagine your ideal safe, peaceful place",
                    "Notice visual details: colors, lighting, scenery",
                    "Notice sounds: natural sounds, music, or silence",
                    "Feel the safety and peace of this place",
                    "Stay in visualization as long as feels good",
                    "Slowly return awareness to present when ready"
                ],
                materials_needed=["quiet space"],
                setup_time_minutes=1,
                duration_minutes=12,
                intensity_level=IntensityLevel.MODERATE,
                accessibility=AccessibilityLevel.IMMEDIATE,
                target_contexts=[SoothingContext.ANXIETY, SoothingContext.TRAUMA_RESPONSE, SoothingContext.OVERWHELM],
                contraindications=["active psychosis", "severe dissociation"]
            ),
            
            SoothingActivity(
                activity_id="herbal_tea_ceremony",
                name="Mindful Tea Ceremony",
                category=SoothingCategory.GUSTATORY,
                description="Preparing and mindfully drinking herbal tea as a self-care ritual",
                detailed_instructions=[
                    "Choose calming herbal tea (chamomile, lavender, etc.)",
                    "Heat water mindfully, listening to sounds",
                    "Steep tea for recommended time",
                    "Hold warm cup and notice temperature in hands",
                    "Inhale steam and notice aromas",
                    "Sip slowly, focusing on taste and warmth",
                    "Feel warmth spreading through body",
                    "Continue drinking with full attention"
                ],
                materials_needed=["herbal tea", "hot water", "favorite mug"],
                setup_time_minutes=5,
                duration_minutes=15,
                intensity_level=IntensityLevel.GENTLE,
                accessibility=AccessibilityLevel.QUICK_SETUP,
                target_contexts=[SoothingContext.STRESS, SoothingContext.ANXIETY, SoothingContext.INSOMNIA],
                indoor_outdoor="indoor"
            ),
            
            SoothingActivity(
                activity_id="affirmation_practice",
                name="Self-Compassion Affirmations",
                category=SoothingCategory.COGNITIVE,
                description="Speaking or writing kind, supportive statements to yourself",
                detailed_instructions=[
                    "Choose comfortable, private space",
                    "Select affirmations that feel authentic",
                    "Speak aloud or write: 'I am worthy of love and care'",
                    "Continue with: 'I am doing my best right now'",
                    "Add: 'This difficult moment will pass'",
                    "Include: 'I deserve kindness and compassion'",
                    "End with: 'I am enough just as I am'",
                    "Repeat statements that resonate most"
                ],
                materials_needed=["optional: journal and pen"],
                setup_time_minutes=1,
                duration_minutes=8,
                intensity_level=IntensityLevel.GENTLE,
                accessibility=AccessibilityLevel.IMMEDIATE,
                target_contexts=[SoothingContext.SADNESS, SoothingContext.OVERWHELM, SoothingContext.GENERAL_DISTRESS],
                indoor_outdoor="both"
            )
        ]
    
    def get_activity(self, activity_id: str) -> Optional[SoothingActivity]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM soothing_activities WHERE activity_id = ?
            """, (activity_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return SoothingActivity(
                activity_id=row[0],
                name=row[1],
                category=SoothingCategory(row[2]),
                description=row[3] or "",
                detailed_instructions=json.loads(row[4] or '[]'),
                materials_needed=json.loads(row[5] or '[]'),
                setup_time_minutes=row[6] or 0,
                duration_minutes=row[7] or 10,
                intensity_level=IntensityLevel(row[8]),
                accessibility=AccessibilityLevel(row[9]),
                target_contexts=[SoothingContext(c) for c in json.loads(row[10] or '[]')],
                contraindications=json.loads(row[11] or '[]'),
                personalization_options=json.loads(row[12] or '[]'),
                variations=json.loads(row[13] or '[]'),
                effectiveness_rating=row[14],
                usage_count=row[15] or 0,
                cost_level=row[16] or "free",
                indoor_outdoor=row[17] or "both",
                alone_social=row[18] or "alone",
                created_date=datetime.fromisoformat(row[19])
            )
    
    def get_activities_by_category(self, category: SoothingCategory) -> List[SoothingActivity]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM soothing_activities 
                WHERE category = ?
                ORDER BY effectiveness_rating DESC, usage_count DESC
            """, (category.value,))
            
            activities = []
            for row in cursor.fetchall():
                activity = SoothingActivity(
                    activity_id=row[0],
                    name=row[1],
                    category=SoothingCategory(row[2]),
                    description=row[3] or "",
                    detailed_instructions=json.loads(row[4] or '[]'),
                    materials_needed=json.loads(row[5] or '[]'),
                    setup_time_minutes=row[6] or 0,
                    duration_minutes=row[7] or 10,
                    intensity_level=IntensityLevel(row[8]),
                    accessibility=AccessibilityLevel(row[9]),
                    target_contexts=[SoothingContext(c) for c in json.loads(row[10] or '[]')],
                    contraindications=json.loads(row[11] or '[]'),
                    personalization_options=json.loads(row[12] or '[]'),
                    variations=json.loads(row[13] or '[]'),
                    effectiveness_rating=row[14],
                    usage_count=row[15] or 0,
                    cost_level=row[16] or "free",
                    indoor_outdoor=row[17] or "both",
                    alone_social=row[18] or "alone",
                    created_date=datetime.fromisoformat(row[19])
                )
                activities.append(activity)
            
            return activities
    
    def get_recommended_activities(
        self,
        patient_id: str,
        context: SoothingContext = None,
        available_time: int = None,
        accessibility_level: AccessibilityLevel = None,
        intensity_preference: IntensityLevel = None,
        category_preferences: List[SoothingCategory] = None
    ) -> List[SoothingActivity]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM soothing_activities WHERE 1=1"
            params = []
            
            if available_time:
                query += " AND duration_minutes <= ?"
                params.append(available_time)
            
            if accessibility_level:
                query += " AND accessibility = ?"
                params.append(accessibility_level.value)
            
            if intensity_preference:
                query += " AND intensity_level = ?"
                params.append(intensity_preference.value)
            
            query += " ORDER BY effectiveness_rating DESC, usage_count DESC LIMIT 20"
            
            cursor.execute(query, params)
            
            all_activities = []
            for row in cursor.fetchall():
                activity = SoothingActivity(
                    activity_id=row[0],
                    name=row[1],
                    category=SoothingCategory(row[2]),
                    description=row[3] or "",
                    detailed_instructions=json.loads(row[4] or '[]'),
                    materials_needed=json.loads(row[5] or '[]'),
                    setup_time_minutes=row[6] or 0,
                    duration_minutes=row[7] or 10,
                    intensity_level=IntensityLevel(row[8]),
                    accessibility=AccessibilityLevel(row[9]),
                    target_contexts=[SoothingContext(c) for c in json.loads(row[10] or '[]')],
                    contraindications=json.loads(row[11] or '[]'),
                    personalization_options=json.loads(row[12] or '[]'),
                    variations=json.loads(row[13] or '[]'),
                    effectiveness_rating=row[14],
                    usage_count=row[15] or 0,
                    cost_level=row[16] or "free",
                    indoor_outdoor=row[17] or "both",
                    alone_social=row[18] or "alone",
                    created_date=datetime.fromisoformat(row[19])
                )
                all_activities.append(activity)
        
        filtered_activities = all_activities
        
        if context:
            context_matches = [
                activity for activity in all_activities
                if context in activity.target_contexts
            ]
            if context_matches:
                filtered_activities = context_matches
        
        if category_preferences:
            preferred_activities = [
                activity for activity in filtered_activities
                if activity.category in category_preferences
            ]
            if preferred_activities:
                filtered_activities = preferred_activities
        
        session_history = self.get_patient_session_history(patient_id, days_back=14)
        recent_usage = {}
        for session in session_history:
            recent_usage[session.activity_id] = recent_usage.get(session.activity_id, 0) + 1
        
        def sort_key(activity):
            usage_penalty = recent_usage.get(activity.activity_id, 0) * 0.15
            effectiveness = activity.effectiveness_rating or 0
            return effectiveness - usage_penalty
        
        filtered_activities.sort(key=sort_key, reverse=True)
        
        return filtered_activities[:8]
    
    def start_soothing_session(
        self,
        patient_id: str,
        activity_id: str,
        context: SoothingContext,
        pre_distress: int,
        pre_emotions: List[str] = None,
        trigger_event: str = "",
        planned_duration: int = None
    ) -> str:
        
        activity = self.get_activity(activity_id)
        if not activity:
            return ""
        
        session = SoothingSession(
            patient_id=patient_id,
            activity_id=activity_id,
            context=context,
            pre_distress_level=pre_distress,
            pre_emotions=pre_emotions or [],
            trigger_event=trigger_event,
            planned_duration=planned_duration or activity.duration_minutes
        )
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO soothing_sessions (
                    session_id, patient_id, activity_id, start_time,
                    end_time, planned_duration, actual_duration,
                    pre_distress_level, post_distress_level,
                    pre_emotions, post_emotions, context, trigger_event,
                    effectiveness_rating, enjoyment_rating,
                    modifications_made, barriers_encountered, notes,
                    would_repeat, completed, interrupted_reason,
                    created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id, session.patient_id, session.activity_id,
                session.start_time.isoformat(), None, session.planned_duration,
                None, session.pre_distress_level, None,
                json.dumps(session.pre_emotions), json.dumps(session.post_emotions),
                session.context.value, session.trigger_event, None, None,
                json.dumps(session.modifications_made),
                json.dumps(session.barriers_encountered), session.notes,
                None, session.completed, session.interrupted_reason,
                session.created_date.isoformat(), session.last_updated.isoformat()
            ))
            
            cursor.execute("""
                UPDATE soothing_activities 
                SET usage_count = usage_count + 1 
                WHERE activity_id = ?
            """, (activity_id,))
            
            conn.commit()
        
        return session.session_id
    
    def complete_soothing_session(
        self,
        session_id: str,
        post_distress: int,
        post_emotions: List[str] = None,
        effectiveness_rating: int = None,
        enjoyment_rating: int = None,
        notes: str = "",
        would_repeat: bool = True,
        modifications: List[str] = None,
        barriers: List[str] = None
    ) -> bool:
        
        end_time = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT start_time FROM soothing_sessions WHERE session_id = ?
            """, (session_id,))
            
            result = cursor.fetchone()
            if not result:
                return False
            
            start_time = datetime.fromisoformat(result[0])
            actual_duration = int((end_time - start_time).total_seconds() / 60)
            
            cursor.execute("""
                UPDATE soothing_sessions SET
                    end_time = ?,
                    actual_duration = ?,
                    post_distress_level = ?,
                    post_emotions = ?,
                    effectiveness_rating = ?,
                    enjoyment_rating = ?,
                    notes = ?,
                    would_repeat = ?,
                    modifications_made = ?,
                    barriers_encountered = ?,
                    completed = TRUE,
                    last_updated = ?
                WHERE session_id = ?
            """, (
                end_time.isoformat(), actual_duration, post_distress,
                json.dumps(post_emotions or []), effectiveness_rating,
                enjoyment_rating, notes, would_repeat,
                json.dumps(modifications or []), json.dumps(barriers or []),
                end_time.isoformat(), session_id
            ))
            
            cursor.execute("""
                SELECT activity_id FROM soothing_sessions WHERE session_id = ?
            """, (session_id,))
            
            activity_id = cursor.fetchone()[0]
            
            if effectiveness_rating is not None:
                cursor.execute("""
                    SELECT AVG(effectiveness_rating) FROM soothing_sessions 
                    WHERE activity_id = ? AND effectiveness_rating IS NOT NULL
                """, (activity_id,))
                
                avg_effectiveness = cursor.fetchone()[0]
                
                cursor.execute("""
                    UPDATE soothing_activities 
                    SET effectiveness_rating = ? 
                    WHERE activity_id = ?
                """, (avg_effectiveness, activity_id))
            
            conn.commit()
        
        return True
    
    def interrupt_session(
        self,
        session_id: str,
        interruption_reason: str,
        partial_effectiveness: int = None,
        notes: str = ""
    ) -> bool:
        
        end_time = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT start_time FROM soothing_sessions WHERE session_id = ?
            """, (session_id,))
            
            result = cursor.fetchone()
            if not result:
                return False
            
            start_time = datetime.fromisoformat(result[0])
            actual_duration = int((end_time - start_time).total_seconds() / 60)
            
            cursor.execute("""
                UPDATE soothing_sessions SET
                    end_time = ?,
                    actual_duration = ?,
                    effectiveness_rating = ?,
                    notes = ?,
                    completed = FALSE,
                    interrupted_reason = ?,
                    last_updated = ?
                WHERE session_id = ?
            """, (
                end_time.isoformat(), actual_duration, partial_effectiveness,
                notes, interruption_reason, end_time.isoformat(), session_id
            ))
            
            conn.commit()
        
        return True
    
    def get_patient_session_history(
        self,
        patient_id: str,
        days_back: int = 30,
        limit: Optional[int] = None
    ) -> List[SoothingSession]:
        
        start_date = datetime.now() - timedelta(days=days_back)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM soothing_sessions 
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
                session = SoothingSession(
                    session_id=row[0],
                    patient_id=row[1],
                    activity_id=row[2],
                    start_time=datetime.fromisoformat(row[3]),
                    end_time=datetime.fromisoformat(row[4]) if row[4] else None,
                    planned_duration=row[5] or 0,
                    actual_duration=row[6],
                    pre_distress_level=row[7] or 0,
                    post_distress_level=row[8],
                    pre_emotions=json.loads(row[9] or '[]'),
                    post_emotions=json.loads(row[10] or '[]'),
                    context=SoothingContext(row[11]) if row[11] else SoothingContext.GENERAL_DISTRESS,
                    trigger_event=row[12] or "",
                    effectiveness_rating=row[13],
                    enjoyment_rating=row[14],
                    modifications_made=json.loads(row[15] or '[]'),
                    barriers_encountered=json.loads(row[16] or '[]'),
                    notes=row[17] or "",
                    would_repeat=bool(row[18]) if row[18] is not None else None,
                    completed=bool(row[19]),
                    interrupted_reason=row[20] or "",
                    created_date=datetime.fromisoformat(row[21]),
                    last_updated=datetime.fromisoformat(row[22])
                )
                sessions.append(session)
            
            return sessions
    
    def create_soothing_kit(
        self,
        patient_id: str,
        kit_name: str = "Personal Comfort Kit"
    ) -> str:
        
        session_history = self.get_patient_session_history(patient_id, days_back=90)
        
        high_effectiveness = []
        emergency_suitable = []
        bedtime_suitable = []
        daily_comfort = []
        
        for session in session_history:
            if session.effectiveness_rating and session.effectiveness_rating >= 7:
                high_effectiveness.append(session.activity_id)
            
            activity = self.get_activity(session.activity_id)
            if activity:
                if activity.accessibility == AccessibilityLevel.IMMEDIATE and activity.duration_minutes <= 10:
                    emergency_suitable.append(session.activity_id)
                
                if SoothingContext.INSOMNIA in activity.target_contexts:
                    bedtime_suitable.append(session.activity_id)
                
                if activity.intensity_level == IntensityLevel.GENTLE:
                    daily_comfort.append(session.activity_id)
        
        if not emergency_suitable:
            emergency_suitable = ["soft_blanket_cocoon", "aromatherapy_breathing", "gentle_self_massage"]
        
        if not bedtime_suitable:
            bedtime_suitable = ["herbal_tea_ceremony", "nature_sounds_meditation", "visualization_safe_place"]
        
        if not daily_comfort:
            daily_comfort = ["gratitude_journaling", "comfort_music_listening", "mindful_observation"]
        
        physical_items = [
            "Soft blanket or weighted blanket",
            "Essential oils or calming scents",
            "Comfortable pillow",
            "Favorite tea or warm drink",
            "Comfort object or stuffed animal",
            "Massage lotion or oil",
            "Cozy socks or slippers"
        ]
        
        digital_resources = [
            "Calm or meditation apps",
            "Favorite music playlist",
            "Nature sounds recordings",
            "Photos of loved ones",
            "Inspiring quotes collection",
            "Audiobooks or podcasts",
            "Guided meditation recordings"
        ]
        
        kit = SoothingKit(
            patient_id=patient_id,
            name=kit_name,
            emergency_activities=list(set(emergency_suitable[:5])),
            daily_comfort_activities=list(set(daily_comfort[:7])),
            bedtime_activities=list(set(bedtime_suitable[:4])),
            physical_comfort_items=physical_items,
            digital_resources=digital_resources,
            personalized_triggers={
                SoothingContext.STRESS.value: high_effectiveness[:3],
                SoothingContext.ANXIETY.value: emergency_suitable[:3],
                SoothingContext.SADNESS.value: daily_comfort[:3]
            },
            backup_options=["affirmation_practice", "gentle_stretching", "comfort_food_mindful_eating"],
            location_specific={
                "home": daily_comfort[:5],
                "work": ["aromatherapy_breathing", "gentle_self_massage", "gratitude_journaling"],
                "travel": ["nature_sounds_meditation", "affirmation_practice", "visualization_safe_place"]
            }
        )
        
        self._save_soothing_kit(kit)
        return kit.kit_id
    
    def _save_soothing_kit(self, kit: SoothingKit):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO soothing_kits (
                    kit_id, patient_id, name, emergency_activities,
                    daily_comfort_activities, bedtime_activities,
                    physical_comfort_items, digital_resources,
                    personalized_triggers, backup_options,
                    location_specific, created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                kit.kit_id, kit.patient_id, kit.name,
                json.dumps(kit.emergency_activities),
                json.dumps(kit.daily_comfort_activities),
                json.dumps(kit.bedtime_activities),
                json.dumps(kit.physical_comfort_items),
                json.dumps(kit.digital_resources),
                json.dumps(kit.personalized_triggers),
                json.dumps(kit.backup_options),
                json.dumps(kit.location_specific),
                kit.created_date.isoformat(),
                kit.last_updated.isoformat()
            ))
            
            conn.commit()
    
    def get_soothing_kit(self, patient_id: str) -> Optional[SoothingKit]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM soothing_kits 
                WHERE patient_id = ? 
                ORDER BY created_date DESC 
                LIMIT 1
            """, (patient_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return SoothingKit(
                kit_id=row[0],
                patient_id=row[1],
                name=row[2],
                emergency_activities=json.loads(row[3] or '[]'),
                daily_comfort_activities=json.loads(row[4] or '[]'),
                bedtime_activities=json.loads(row[5] or '[]'),
                physical_comfort_items=json.loads(row[6] or '[]'),
                digital_resources=json.loads(row[7] or '[]'),
                personalized_triggers=json.loads(row[8] or '{}'),
                backup_options=json.loads(row[9] or '[]'),
                location_specific=json.loads(row[10] or '{}'),
                created_date=datetime.fromisoformat(row[11]),
                last_updated=datetime.fromisoformat(row[12])
            )
    
    def create_soothing_plan(
        self,
        patient_id: str,
        goals: List[str] = None
    ) -> str:
        
        kit = self.get_soothing_kit(patient_id)
        session_history = self.get_patient_session_history(patient_id, days_back=60)
        
        category_preferences = []
        category_effectiveness = {}
        
        for session in session_history:
            if session.effectiveness_rating and session.effectiveness_rating >= 6:
                activity = self.get_activity(session.activity_id)
                if activity:
                    category = activity.category
                    if category not in category_effectiveness:
                        category_effectiveness[category] = []
                    category_effectiveness[category].append(session.effectiveness_rating)
        
        for category, ratings in category_effectiveness.items():
            avg_rating = sum(ratings) / len(ratings)
            if avg_rating >= 7:
                category_preferences.append(category)
        
        morning_activities = []
        evening_activities = []
        
        if kit:
            morning_activities = [
                activity_id for activity_id in kit.daily_comfort_activities
                if self.get_activity(activity_id) and 
                self.get_activity(activity_id).intensity_level in [IntensityLevel.GENTLE, IntensityLevel.MODERATE]
            ][:3]
            
            evening_activities = kit.bedtime_activities[:3]
        
        if not morning_activities:
            morning_activities = ["gratitude_journaling", "gentle_stretching", "aromatherapy_breathing"]
        
        if not evening_activities:
            evening_activities = ["herbal_tea_ceremony", "nature_sounds_meditation", "visualization_safe_place"]
        
        stress_sequence = []
        if kit and kit.personalized_triggers.get(SoothingContext.STRESS.value):
            stress_sequence = kit.personalized_triggers[SoothingContext.STRESS.value]
        else:
            stress_sequence = ["aromatherapy_breathing", "gentle_self_massage", "comfort_music_listening"]
        
        weekly_schedule = {
            "monday": ["morning_routine"] + morning_activities[:1],
            "tuesday": ["gentle_stretching"],
            "wednesday": ["creative_coloring", "comfort_music_listening"],
            "thursday": ["nature_sounds_meditation"],
            "friday": ["gratitude_journaling", "comfort_food_mindful_eating"],
            "saturday": ["warm_bath_ritual", "photo_memory_viewing"],
            "sunday": ["visualization_safe_place", "affirmation_practice"]
        }
        
        situational_responses = {
            SoothingContext.ANXIETY.value: kit.emergency_activities[:3] if kit else ["aromatherapy_breathing", "soft_blanket_cocoon", "nature_sounds_meditation"],
            SoothingContext.SADNESS.value: ["comfort_music_listening", "photo_memory_viewing", "gratitude_journaling"],
            SoothingContext.ANGER.value: ["gentle_stretching", "aromatherapy_breathing", "nature_sounds_meditation"],
            SoothingContext.OVERWHELM.value: ["soft_blanket_cocoon", "visualization_safe_place", "gentle_self_massage"],
            SoothingContext.LONELINESS.value: ["comfort_music_listening", "photo_memory_viewing", "pet_companion_time"],
            SoothingContext.INSOMNIA.value: evening_activities
        }
        
        default_goals = [
            "Develop consistent self-care routine",
            "Reduce overall stress levels",
            "Improve emotional regulation",
            "Build resilience and coping skills",
            "Create sense of safety and comfort"
        ]
        
        plan = SoothingPlan(
            patient_id=patient_id,
            morning_routine=morning_activities,
            evening_routine=evening_activities,
            stress_response_sequence=stress_sequence,
            weekly_schedule=weekly_schedule,
            situational_responses=situational_responses,
            preferred_categories=category_preferences,
            goals=goals or default_goals,
            progress_metrics=[
                "Weekly self-soothing session frequency",
                "Average effectiveness ratings",
                "Distress level improvements",
                "Routine consistency",
                "Overall well-being scores"
            ]
        )
        
        self._save_soothing_plan(plan)
        return plan.plan_id
    
    def _save_soothing_plan(self, plan: SoothingPlan):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO soothing_plans (
                    plan_id, patient_id, morning_routine, evening_routine,
                    stress_response_sequence, weekly_schedule, situational_responses,
                    preferred_categories, avoided_categories, goals,
                    progress_metrics, created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plan.plan_id, plan.patient_id,
                json.dumps(plan.morning_routine),
                json.dumps(plan.evening_routine),
                json.dumps(plan.stress_response_sequence),
                json.dumps(plan.weekly_schedule),
                json.dumps(plan.situational_responses),
                json.dumps([c.value for c in plan.preferred_categories]),
                json.dumps([c.value for c in plan.avoided_categories]),
                json.dumps(plan.goals),
                json.dumps(plan.progress_metrics),
                plan.created_date.isoformat(),
                plan.last_updated.isoformat()
            ))
            
            conn.commit()
    
    def get_soothing_plan(self, patient_id: str) -> Optional[SoothingPlan]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM soothing_plans 
                WHERE patient_id = ? 
                ORDER BY created_date DESC 
                LIMIT 1
            """, (patient_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return SoothingPlan(
                plan_id=row[0],
                patient_id=row[1],
                morning_routine=json.loads(row[2] or '[]'),
                evening_routine=json.loads(row[3] or '[]'),
                stress_response_sequence=json.loads(row[4] or '[]'),
                weekly_schedule=json.loads(row[5] or '{}'),
                situational_responses=json.loads(row[6] or '{}'),
                preferred_categories=[SoothingCategory(c) for c in json.loads(row[7] or '[]')],
                avoided_categories=[SoothingCategory(c) for c in json.loads(row[8] or '[]')],
                goals=json.loads(row[9] or '[]'),
                progress_metrics=json.loads(row[10] or '[]'),
                created_date=datetime.fromisoformat(row[11]),
                last_updated=datetime.fromisoformat(row[12])
            )
    
    def generate_progress_report(self, patient_id: str, days_back: int = 30) -> Dict[str, Any]:
        sessions = self.get_patient_session_history(patient_id, days_back)
        
        if not sessions:
            return {
                "patient_id": patient_id,
                "period_days": days_back,
                "total_sessions": 0,
                "message": "No self-soothing sessions recorded in this period"
            }
        
        total_sessions = len(sessions)
        completed_sessions = len([s for s in sessions if s.completed])
        completion_rate = completed_sessions / total_sessions if total_sessions > 0 else 0
        
        distress_reductions = []
        for session in sessions:
            if session.post_distress_level is not None:
                reduction = session.pre_distress_level - session.post_distress_level
                distress_reductions.append(reduction)
        
        avg_distress_reduction = sum(distress_reductions) / len(distress_reductions) if distress_reductions else 0
        
        effectiveness_ratings = [s.effectiveness_rating for s in sessions if s.effectiveness_rating is not None]
        avg_effectiveness = sum(effectiveness_ratings) / len(effectiveness_ratings) if effectiveness_ratings else 0
        
        enjoyment_ratings = [s.enjoyment_rating for s in sessions if s.enjoyment_rating is not None]
        avg_enjoyment = sum(enjoyment_ratings) / len(enjoyment_ratings) if enjoyment_ratings else 0
        
        activity_usage = {}
        activity_effectiveness = {}
        category_usage = {}
        
        for session in sessions:
            activity_usage[session.activity_id] = activity_usage.get(session.activity_id, 0) + 1
            
            if session.effectiveness_rating:
                if session.activity_id not in activity_effectiveness:
                    activity_effectiveness[session.activity_id] = []
                activity_effectiveness[session.activity_id].append(session.effectiveness_rating)
            
            activity = self.get_activity(session.activity_id)
            if activity:
                category = activity.category.value
                category_usage[category] = category_usage.get(category, 0) + 1
        
        most_used_activities = sorted(activity_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        most_effective_activities = []
        
        for activity_id, ratings in activity_effectiveness.items():
            avg_rating = sum(ratings) / len(ratings)
            activity = self.get_activity(activity_id)
            activity_name = activity.name if activity else activity_id
            most_effective_activities.append((activity_name, avg_rating, len(ratings)))
        
        most_effective_activities.sort(key=lambda x: x[1], reverse=True)
        most_effective_activities = most_effective_activities[:5]
        
        context_analysis = {}
        for session in sessions:
            context = session.context.value
            if context not in context_analysis:
                context_analysis[context] = {
                    "count": 0,
                    "avg_effectiveness": 0,
                    "effectiveness_ratings": []
                }
            
            context_analysis[context]["count"] += 1
            if session.effectiveness_rating:
                context_analysis[context]["effectiveness_ratings"].append(session.effectiveness_rating)
        
        for context, data in context_analysis.items():
            if data["effectiveness_ratings"]:
                data["avg_effectiveness"] = sum(data["effectiveness_ratings"]) / len(data["effectiveness_ratings"])
        
        common_barriers = {}
        for session in sessions:
            for barrier in session.barriers_encountered:
                common_barriers[barrier] = common_barriers.get(barrier, 0) + 1
        
        top_barriers = sorted(common_barriers.items(), key=lambda x: x[1], reverse=True)[:3]
        
        repeat_intentions = [s.would_repeat for s in sessions if s.would_repeat is not None]
        repeat_rate = sum(repeat_intentions) / len(repeat_intentions) if repeat_intentions else 0
        
        insights = self._generate_soothing_insights(sessions, activity_effectiveness, context_analysis)
        
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
                "average_effectiveness": round(avg_effectiveness, 2),
                "average_enjoyment": round(avg_enjoyment, 2),
                "repeat_intention_rate": round(repeat_rate, 2)
            },
            "activity_analysis": {
                "most_used": [{"activity_id": a[0], "usage_count": a[1]} for a in most_used_activities],
                "most_effective": [{"activity": a[0], "avg_rating": round(a[1], 2), "session_count": a[2]} for a in most_effective_activities],
                "category_distribution": dict(category_usage)
            },
            "context_analysis": {
                context: {
                    "session_count": data["count"],
                    "avg_effectiveness": round(data["avg_effectiveness"], 2)
                }
                for context, data in context_analysis.items()
            },
            "barriers_and_challenges": [{"barrier": b[0], "frequency": b[1]} for b in top_barriers],
            "therapeutic_insights": insights,
            "recommendations": self._generate_soothing_recommendations(sessions, activity_effectiveness, context_analysis)
        }
    
    def _generate_soothing_insights(
        self,
        sessions: List[SoothingSession],
        activity_effectiveness: Dict[str, List[int]],
        context_analysis: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        
        insights = []
        
        if not sessions:
            insights.append("Begin regular self-soothing practice to build emotional regulation skills")
            return insights
        
        avg_effectiveness = {}
        for activity_id, ratings in activity_effectiveness.items():
            avg_effectiveness[activity_id] = sum(ratings) / len(ratings)
        
        high_effectiveness = [a for a, avg in avg_effectiveness.items() if avg >= 8]
        if high_effectiveness:
            insights.append(f"Excellent effectiveness found with {len(high_effectiveness)} activities - prioritize these in daily routine")
        
        low_effectiveness = [a for a, avg in avg_effectiveness.items() if avg < 5]
        if low_effectiveness:
            insights.append(f"Consider modifying or replacing {len(low_effectiveness)} activities showing low effectiveness")
        
        completion_rate = len([s for s in sessions if s.completed]) / len(sessions)
        if completion_rate < 0.7:
            insights.append("Low completion rate suggests need for shorter or more accessible activities")
        
        distress_reductions = []
        for session in sessions:
            if session.post_distress_level is not None:
                reduction = session.pre_distress_level - session.post_distress_level
                distress_reductions.append(reduction)
        
        if distress_reductions:
            avg_reduction = sum(distress_reductions) / len(distress_reductions)
            if avg_reduction >= 3:
                insights.append("Significant distress reduction shows strong self-soothing skills development")
            elif avg_reduction < 1:
                insights.append("Limited distress reduction indicates need for technique refinement or intensity adjustment")
        
        recent_sessions = [s for s in sessions if (datetime.now() - s.start_time).days <= 7]
        if len(recent_sessions) >= 5:
            insights.append("Consistent recent practice shows good engagement with self-care routine")
        elif len(recent_sessions) < 2:
            insights.append("Increase frequency of self-soothing practice for better emotional regulation")
        
        category_usage = {}
        for session in sessions:
            activity = self.get_activity(session.activity_id)
            if activity:
                category = activity.category.value
                category_usage[category] = category_usage.get(category, 0) + 1
        
        if len(category_usage) < 3:
            insights.append("Explore variety across different soothing categories for comprehensive skill building")
        
        most_common_context = max(context_analysis.keys(), key=lambda x: context_analysis[x]["count"]) if context_analysis else None
        if most_common_context and context_analysis[most_common_context]["count"] > len(sessions) * 0.4:
            insights.append(f"Primary trigger context is {most_common_context} - consider preventive strategies")
        
        enjoyment_ratings = [s.enjoyment_rating for s in sessions if s.enjoyment_rating is not None]
        if enjoyment_ratings:
            avg_enjoyment = sum(enjoyment_ratings) / len(enjoyment_ratings)
            if avg_enjoyment >= 7:
                insights.append("High enjoyment ratings indicate good activity-person fit")
            elif avg_enjoyment < 5:
                insights.append("Low enjoyment suggests need for more personalized activity selection")
        
        return insights
    
    def _generate_soothing_recommendations(
        self,
        sessions: List[SoothingSession],
        activity_effectiveness: Dict[str, List[int]],
        context_analysis: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        
        recommendations = []
        
        if not sessions:
            recommendations.extend([
                "Start with 2-3 gentle self-soothing activities daily",
                "Create a comfort kit with essential soothing items",
                "Establish morning and evening soothing routines"
            ])
            return recommendations
        
        avg_effectiveness = {}
        for activity_id, ratings in activity_effectiveness.items():
            avg_effectiveness[activity_id] = sum(ratings) / len(ratings)
        
        top_activities = sorted(avg_effectiveness.items(), key=lambda x: x[1], reverse=True)[:3]
        if top_activities:
            top_names = []
            for activity_id, _ in top_activities:
                activity = self.get_activity(activity_id)
                if activity:
                    top_names.append(activity.name)
            recommendations.append(f"Continue prioritizing most effective activities: {', '.join(top_names)}")
        
        completion_rate = len([s for s in sessions if s.completed]) / len(sessions)
        if completion_rate < 0.8:
            recommendations.append("Focus on shorter, more accessible activities to improve completion rates")
        
        activity_variety = len(set(s.activity_id for s in sessions))
        if activity_variety < 4:
            recommendations.append("Experiment with new activity categories to find additional effective options")
        
        recent_frequency = len([s for s in sessions if (datetime.now() - s.start_time).days <= 7])
        if recent_frequency < 3:
            recommendations.append("Increase self-soothing frequency to at least 3-4 times per week")
        
        context_counts = {context: data["count"] for context, data in context_analysis.items()}
        if context_counts:
            most_common = max(context_counts, key=context_counts.get)
            if context_counts[most_common] > len(sessions) * 0.3:
                recommendations.append(f"Develop specific strategies for {most_common} situations")
        
        interrupted_sessions = [s for s in sessions if not s.completed and s.interrupted_reason]
        if len(interrupted_sessions) > len(sessions) * 0.2:
            recommendations.append("Address common interruption barriers to improve session completion")
        
        category_usage = {}
        for session in sessions:
            activity = self.get_activity(session.activity_id)
            if activity:
                category_usage[activity.category.value] = category_usage.get(activity.category.value, 0) + 1
        
        underused_categories = []
        all_categories = [c.value for c in SoothingCategory]
        for category in all_categories:
            if category not in category_usage or category_usage[category] < 2:
                underused_categories.append(category)
        
        if underused_categories:
            recommendations.append(f"Explore underused categories: {', '.join(underused_categories[:3])}")
        
        distress_reductions = []
        for session in sessions:
            if session.post_distress_level is not None:
                reduction = session.pre_distress_level - session.post_distress_level
                distress_reductions.append(reduction)
        
        if distress_reductions and sum(distress_reductions) / len(distress_reductions) < 2:
            recommendations.append("Consider longer duration or higher intensity activities for better distress relief")
        
        return recommendations
    
    def get_emergency_soothing_sequence(self, patient_id: str) -> List[Dict[str, Any]]:
        kit = self.get_soothing_kit(patient_id)
        
        if kit and kit.emergency_activities:
            emergency_activity_ids = kit.emergency_activities[:3]
        else:
            emergency_activity_ids = ["soft_blanket_cocoon", "aromatherapy_breathing", "gentle_self_massage"]
        
        sequence = []
        for activity_id in emergency_activity_ids:
            activity = self.get_activity(activity_id)
            if activity:
                sequence.append({
                    "activity_id": activity_id,
                    "name": activity.name,
                    "duration_minutes": activity.duration_minutes,
                    "quick_instructions": activity.detailed_instructions[:3],
                    "materials_needed": activity.materials_needed,
                    "accessibility": activity.accessibility.value
                })
        
        return sequence
    
    def get_daily_soothing_suggestions(
        self, 
        patient_id: str, 
        time_of_day: str = "any",
        available_time: int = 15
    ) -> List[Dict[str, Any]]:
        
        plan = self.get_soothing_plan(patient_id)
        
        if time_of_day == "morning" and plan and plan.morning_routine:
            activity_pool = plan.morning_routine
        elif time_of_day == "evening" and plan and plan.evening_routine:
            activity_pool = plan.evening_routine
        else:
            recommended = self.get_recommended_activities(
                patient_id=patient_id,
                available_time=available_time,
                accessibility_level=AccessibilityLevel.QUICK_SETUP
            )
            activity_pool = [a.activity_id for a in recommended[:5]]
        
        suggestions = []
        for activity_id in activity_pool:
            activity = self.get_activity(activity_id)
            if activity and activity.duration_minutes <= available_time:
                suggestions.append({
                    "activity_id": activity_id,
                    "name": activity.name,
                    "description": activity.description,
                    "duration_minutes": activity.duration_minutes,
                    "category": activity.category.value,
                    "materials_needed": activity.materials_needed,
                    "setup_time": activity.setup_time_minutes
                })
        
        return suggestions[:4]
    
    def track_mood_before_after(
        self, 
        patient_id: str, 
        days_back: int = 14
    ) -> Dict[str, Any]:
        
        sessions = self.get_patient_session_history(patient_id, days_back)
        
        mood_improvements = []
        daily_data = {}
        
        for session in sessions:
            if session.post_distress_level is not None:
                improvement = session.pre_distress_level - session.post_distress_level
                mood_improvements.append(improvement)
                
                date_key = session.start_time.strftime('%Y-%m-%d')
                if date_key not in daily_data:
                    daily_data[date_key] = {
                        "sessions": 0,
                        "total_improvement": 0,
                        "avg_pre_distress": 0,
                        "avg_post_distress": 0,
                        "pre_distress_scores": [],
                        "post_distress_scores": []
                    }
                
                daily_data[date_key]["sessions"] += 1
                daily_data[date_key]["total_improvement"] += improvement
                daily_data[date_key]["pre_distress_scores"].append(session.pre_distress_level)
                daily_data[date_key]["post_distress_scores"].append(session.post_distress_level)
        
        for date_key, data in daily_data.items():
            data["avg_improvement"] = data["total_improvement"] / data["sessions"]
            data["avg_pre_distress"] = sum(data["pre_distress_scores"]) / len(data["pre_distress_scores"])
            data["avg_post_distress"] = sum(data["post_distress_scores"]) / len(data["post_distress_scores"])
        
        overall_improvement = sum(mood_improvements) / len(mood_improvements) if mood_improvements else 0
        
        return {
            "patient_id": patient_id,
            "tracking_period_days": days_back,
            "overall_mood_improvement": round(overall_improvement, 2),
            "total_sessions_analyzed": len([s for s in sessions if s.post_distress_level is not None]),
            "daily_tracking_data": daily_data,
            "improvement_trend": "improving" if overall_improvement > 1.5 else "stable" if overall_improvement > 0.5 else "needs_attention"
        }
    
    def export_soothing_data(
        self, 
        patient_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        
        sessions = self.get_patient_session_history(patient_id, (end_date - start_date).days)
        sessions = [s for s in sessions if start_date <= s.start_time <= end_date]
        
        kit = self.get_soothing_kit(patient_id)
        plan = self.get_soothing_plan(patient_id)
        
        export_data = {
            "patient_id": patient_id,
            "export_date": datetime.now().isoformat(),
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "soothing_sessions": [
                {
                    "session_id": session.session_id,
                    "activity_name": self.get_activity(session.activity_id).name if self.get_activity(session.activity_id) else session.activity_id,
                    "start_time": session.start_time.isoformat(),
                    "duration_minutes": session.actual_duration,
                    "pre_distress": session.pre_distress_level,
                    "post_distress": session.post_distress_level,
                    "effectiveness_rating": session.effectiveness_rating,
                    "enjoyment_rating": session.enjoyment_rating,
                    "completed": session.completed,
                    "context": session.context.value,
                    "notes": session.notes
                }
                for session in sessions
            ],
            "soothing_kit": {
                "emergency_activities": kit.emergency_activities if kit else [],
                "daily_comfort_activities": kit.daily_comfort_activities if kit else [],
                "bedtime_activities": kit.bedtime_activities if kit else [],
                "physical_items": kit.physical_comfort_items if kit else []
            } if kit else None,
            "soothing_plan": {
                "morning_routine": plan.morning_routine if plan else [],
                "evening_routine": plan.evening_routine if plan else [],
                "preferred_categories": [c.value for c in plan.preferred_categories] if plan else [],
                "goals": plan.goals if plan else []
            } if plan else None
        }
        
        return export_data


def get_quick_soothing_activities(distress_level: int, time_available: int) -> List[str]:
    quick_activities = {
        "high_distress": ["soft_blanket_cocoon", "aromatherapy_breathing", "gentle_self_massage"],
        "medium_distress": ["comfort_music_listening", "gratitude_journaling", "nature_sounds_meditation"],
        "low_distress": ["creative_coloring", "photo_memory_viewing", "herbal_tea_ceremony"]
    }
    
    if distress_level >= 7:
        base_activities = quick_activities["high_distress"]
    elif distress_level >= 4:
        base_activities = quick_activities["medium_distress"]
    else:
        base_activities = quick_activities["low_distress"]
    
    duration_limits = {
        "soft_blanket_cocoon": 10,
        "aromatherapy_breathing": 8,
        "gentle_self_massage": 12,
        "comfort_music_listening": 20,
        "gratitude_journaling": 8,
        "nature_sounds_meditation": 10,
        "creative_coloring": 20,
        "photo_memory_viewing": 15,
        "herbal_tea_ceremony": 15
    }
    
    suitable_activities = [
        activity for activity in base_activities
        if duration_limits.get(activity, 10) <= time_available
    ]
    
    return suitable_activities


def create_comfort_kit_checklist() -> Dict[str, List[str]]:
    return {
        "physical_comfort_items": [
            "Soft blanket or weighted blanket",
            "Comfortable pillow or cushion",
            "Essential oils or room spray",
            "Stress ball or fidget toy",
            "Comfort object or stuffed animal",
            "Cozy socks or slippers",
            "Hot water bottle or heating pad",
            "Favorite tea or hot chocolate",
            "Massage lotion or oil",
            "Comfortable clothing"
        ],
        "digital_resources": [
            "Meditation apps (Calm, Headspace, Insight Timer)",
            "Nature sounds or white noise apps",
            "Favorite music playlists",
            "Photo albums of loved ones",
            "Inspirational quotes or affirmations",
            "Guided imagery recordings",
            "Breathing exercise apps",
            "Audiobooks or podcasts",
            "Digital journals or notes apps",
            "Calming games or activities"
        ],
        "environmental_setup": [
            "Dim lighting or candles",
            "Comfortable seating area",
            "Good ventilation",
            "Minimal distractions",
            "Easy access to items",
            "Safe, private space",
            "Temperature control",
            "Background music capability",
            "Writing materials nearby",
            "Emergency contact list"
        ]
    }


if __name__ == "__main__":
    soothing_system = SelfSoothingSystem()
    
    patient_id = "test_patient_001"
    
    session_id = soothing_system.start_soothing_session(
        patient_id=patient_id,
        activity_id="soft_blanket_cocoon",
        context=SoothingContext.ANXIETY,
        pre_distress=8,
        pre_emotions=["anxious", "overwhelmed"],
        trigger_event="Work presentation stress"
    )
    
    soothing_system.complete_soothing_session(
        session_id=session_id,
        post_distress=4,
        post_emotions=["calm", "relaxed"],
        effectiveness_rating=8,
        enjoyment_rating=7,
        notes="Blanket cocoon felt very comforting and safe",
        would_repeat=True
    )
    
    kit_id = soothing_system.create_soothing_kit(patient_id)
    plan_id = soothing_system.create_soothing_plan(patient_id)
    
    report = soothing_system.generate_progress_report(patient_id, 30)
    
    print(f"Session completed: {session_id}")
    print(f"Comfort kit created: {kit_id}")
    print(f"Soothing plan created: {plan_id}")
    print(f"Progress report generated with {report['session_statistics']['total_sessions']} sessions")
    
    emergency_sequence = soothing_system.get_emergency_soothing_sequence(patient_id)
    print(f"Emergency sequence contains {len(emergency_sequence)} activities")
    
    daily_suggestions = soothing_system.get_daily_soothing_suggestions(patient_id, "morning", 10)
    print(f"Daily suggestions: {len(daily_suggestions)} morning activities under 10 minutes")
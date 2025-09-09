
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from enum import Enum
from dataclasses import dataclass, asdict
import json
import math

from config.therapy_protocols import TherapyModality, InterventionType


# ============================================================================
# ENUMS AND DATA STRUCTURES
# ============================================================================

class ExposureType(Enum):
    """Types of exposure interventions"""
    IN_VIVO = "in_vivo"  # Real-life exposure
    IMAGINAL = "imaginal"  # Imagination-based exposure
    INTEROCEPTIVE = "interoceptive"  # Internal sensation exposure
    VIRTUAL_REALITY = "virtual_reality"  # VR-based exposure
    COGNITIVE = "cognitive"  # Cognitive exposure to thoughts/memories
    BEHAVIORAL = "behavioral"  # Behavioral exposure to actions


class ExposureStatus(Enum):
    """Status of exposure sessions"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PARTIALLY_COMPLETED = "partially_completed"
    TERMINATED_EARLY = "terminated_early"
    POSTPONED = "postponed"
    CANCELLED = "cancelled"


class HierarchyLevel(Enum):
    """Difficulty levels for exposure hierarchy"""
    VERY_LOW = 1
    LOW = 2
    MODERATE_LOW = 3
    MODERATE = 4
    MODERATE_HIGH = 5
    HIGH = 6
    VERY_HIGH = 7
    EXTREME = 8


class HabituationLevel(Enum):
    """Levels of anxiety habituation"""
    NO_HABITUATION = 1
    MINIMAL = 2
    SLIGHT = 3
    MODERATE = 4
    GOOD = 5
    EXCELLENT = 6
    COMPLETE = 7


@dataclass
class ExposureItem:
    """Individual item in exposure hierarchy"""
    item_id: str
    description: str
    exposure_type: ExposureType
    difficulty_level: int  # 1-8 scale (SUDS rating)
    estimated_duration: int  # minutes
    
    # Specific details
    location: str = ""
    materials_needed: List[str] = None
    safety_considerations: List[str] = None
    instructions: str = ""
    
    # Tracking
    attempts: int = 0
    successful_completions: int = 0
    average_peak_anxiety: Optional[float] = None
    average_end_anxiety: Optional[float] = None
    notes: str = ""
    
    def __post_init__(self):
        if self.materials_needed is None:
            self.materials_needed = []
        if self.safety_considerations is None:
            self.safety_considerations = []


@dataclass
class ExposureSession:
    """Individual exposure therapy session"""
    session_id: str
    patient_id: str
    item_id: str
    exposure_type: ExposureType
    planned_date: datetime
    planned_duration: int  # minutes
    
    # Session details
    title: str
    description: str
    goals: List[str]
    safety_plan: List[str]
    
    # Execution tracking
    status: ExposureStatus
    actual_start_time: Optional[datetime] = None
    actual_duration: Optional[int] = None
    
    # Anxiety ratings (SUDS: 0-10 scale)
    baseline_anxiety: Optional[int] = None
    peak_anxiety: Optional[int] = None
    end_anxiety: Optional[int] = None
    anxiety_ratings: List[Tuple[int, int]] = None  # (time_minutes, anxiety_level)
    
    # Outcomes
    habituation_achieved: Optional[bool] = None
    premature_termination: Optional[bool] = None
    termination_reason: str = ""
    
    # Learning and progress
    success_indicators: List[str] = None
    difficulties_encountered: List[str] = None
    coping_strategies_used: List[str] = None
    key_learnings: List[str] = None
    
    # Follow-up planning
    next_exposure_recommendations: str = ""
    homework_assigned: List[str] = None
    
    # Metadata
    created_date: datetime
    therapist_notes: str = ""
    
    def __post_init__(self):
        if self.anxiety_ratings is None:
            self.anxiety_ratings = []
        if self.success_indicators is None:
            self.success_indicators = []
        if self.difficulties_encountered is None:
            self.difficulties_encountered = []
        if self.coping_strategies_used is None:
            self.coping_strategies_used = []
        if self.key_learnings is None:
            self.key_learnings = []
        if self.homework_assigned is None:
            self.homework_assigned = []


@dataclass
class ExposureHierarchy:
    """Complete exposure hierarchy for patient"""
    hierarchy_id: str
    patient_id: str
    target_fear: str
    fear_category: str  # e.g., "social_anxiety", "specific_phobia", "ptsd"
    
    # Hierarchy structure
    exposure_items: List[ExposureItem]
    current_level: int  # Current working level (1-8)
    mastery_criteria: Dict[str, Any]  # Criteria for moving up hierarchy
    
    # Progress tracking
    total_sessions_completed: int = 0
    levels_mastered: List[int] = None
    estimated_completion_date: Optional[datetime] = None
    
    # Metadata
    created_date: datetime
    last_updated: datetime
    therapist_notes: str = ""
    
    def __post_init__(self):
        if self.levels_mastered is None:
            self.levels_mastered = []


@dataclass
class ExposureProtocol:
    """Standardized exposure protocol template"""
    protocol_id: str
    name: str
    target_conditions: List[str]  # Conditions this protocol treats
    description: str
    
    # Protocol structure
    typical_hierarchy_items: List[Dict[str, Any]]
    session_structure: List[str]
    safety_guidelines: List[str]
    contraindications: List[str]
    
    # Treatment parameters
    typical_session_duration: int  # minutes
    sessions_per_week: int
    estimated_total_sessions: int
    
    # Customization guidance
    adaptation_notes: str
    prerequisite_skills: List[str]
    evidence_base: str


# ============================================================================
# MAIN CLASS
# ============================================================================

class ExposureTherapyManager:
    """
    Manages exposure therapy protocols, hierarchy development, and session tracking.
    """
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self._initialize_database()
        self._load_exposure_protocols()
    
    # ========================================================================
    # DATABASE INITIALIZATION AND SETUP
    # ========================================================================
    
    def _initialize_database(self):
        """Initialize exposure therapy tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Exposure hierarchies table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS exposure_hierarchies (
                    hierarchy_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    target_fear TEXT NOT NULL,
                    fear_category TEXT NOT NULL,
                    current_level INTEGER DEFAULT 1,
                    mastery_criteria TEXT,
                    total_sessions_completed INTEGER DEFAULT 0,
                    levels_mastered TEXT,
                    estimated_completion_date DATE,
                    created_date TIMESTAMP,
                    last_updated TIMESTAMP,
                    therapist_notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            # Exposure items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS exposure_items (
                    item_id TEXT PRIMARY KEY,
                    hierarchy_id TEXT NOT NULL,
                    description TEXT NOT NULL,
                    exposure_type TEXT NOT NULL,
                    difficulty_level INTEGER NOT NULL,
                    estimated_duration INTEGER,
                    location TEXT,
                    materials_needed TEXT,
                    safety_considerations TEXT,
                    instructions TEXT,
                    attempts INTEGER DEFAULT 0,
                    successful_completions INTEGER DEFAULT 0,
                    average_peak_anxiety REAL,
                    average_end_anxiety REAL,
                    notes TEXT,
                    FOREIGN KEY (hierarchy_id) REFERENCES exposure_hierarchies (hierarchy_id)
                )
            """)
            
            # Exposure sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS exposure_sessions (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    item_id TEXT NOT NULL,
                    exposure_type TEXT NOT NULL,
                    planned_date TIMESTAMP,
                    planned_duration INTEGER,
                    title TEXT NOT NULL,
                    description TEXT,
                    goals TEXT,
                    safety_plan TEXT,
                    status TEXT NOT NULL,
                    actual_start_time TIMESTAMP,
                    actual_duration INTEGER,
                    baseline_anxiety INTEGER,
                    peak_anxiety INTEGER,
                    end_anxiety INTEGER,
                    anxiety_ratings TEXT,
                    habituation_achieved BOOLEAN,
                    premature_termination BOOLEAN,
                    termination_reason TEXT,
                    success_indicators TEXT,
                    difficulties_encountered TEXT,
                    coping_strategies_used TEXT,
                    key_learnings TEXT,
                    next_exposure_recommendations TEXT,
                    homework_assigned TEXT,
                    created_date TIMESTAMP,
                    therapist_notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                    FOREIGN KEY (item_id) REFERENCES exposure_items (item_id)
                )
            """)
            
            # Exposure protocols table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS exposure_protocols (
                    protocol_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    target_conditions TEXT,
                    description TEXT,
                    typical_hierarchy_items TEXT,
                    session_structure TEXT,
                    safety_guidelines TEXT,
                    contraindications TEXT,
                    typical_session_duration INTEGER,
                    sessions_per_week INTEGER,
                    estimated_total_sessions INTEGER,
                    adaptation_notes TEXT,
                    prerequisite_skills TEXT,
                    evidence_base TEXT,
                    is_default BOOLEAN DEFAULT FALSE
                )
            """)
            
            conn.commit()
    
    def _load_exposure_protocols(self):
        """Load default exposure protocols"""
        # Check if protocols already exist
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM exposure_protocols WHERE is_default = TRUE")
            count = cursor.fetchone()[0]
            
            if count == 0:  # Load defaults if not already present
                protocols = self._create_default_protocols()
                for protocol in protocols:
                    self._save_exposure_protocol(protocol, is_default=True)
    
    def _create_default_protocols(self) -> List[ExposureProtocol]:
        """Create default exposure therapy protocols"""
        protocols = [
            ExposureProtocol(
                protocol_id="exp_protocol_001",
                name="Social Anxiety Exposure Protocol",
                target_conditions=["Social Anxiety Disorder", "Social Phobia", "Performance Anxiety"],
                description="Systematic exposure protocol for social anxiety and performance fears",
                typical_hierarchy_items=[
                    {"level": 1, "description": "Make eye contact with stranger", "type": "in_vivo", "duration": 5},
                    {"level": 2, "description": "Ask for directions from stranger", "type": "in_vivo", "duration": 10},
                    {"level": 3, "description": "Make small talk in elevator", "type": "in_vivo", "duration": 15},
                    {"level": 4, "description": "Order food with special request", "type": "in_vivo", "duration": 20},
                    {"level": 5, "description": "Speak up in meeting/class", "type": "in_vivo", "duration": 30},
                    {"level": 6, "description": "Give short presentation", "type": "in_vivo", "duration": 45},
                    {"level": 7, "description": "Attend social gathering alone", "type": "in_vivo", "duration": 60},
                    {"level": 8, "description": "Give formal presentation", "type": "in_vivo", "duration": 60}
                ],
                session_structure=[
                    "Review hierarchy and select exposure",
                    "Rate baseline anxiety (SUDS)",
                    "Plan exposure with safety behaviors identified",
                    "Conduct exposure with ongoing SUDS ratings",
                    "Continue until anxiety reduces by 50% or time limit",
                    "Debrief and process learning",
                    "Plan homework exposure"
                ],
                safety_guidelines=[
                    "Always obtain informed consent",
                    "Start with lower hierarchy items",
                    "Monitor for dissociation or severe distress",
                    "Have exit strategy available",
                    "Process emotions after exposure"
                ],
                contraindications=[
                    "Active psychosis",
                    "Severe depression with suicidal ideation",
                    "Substance abuse",
                    "Unstable medical conditions"
                ],
                typical_session_duration=60,
                sessions_per_week=1,
                estimated_total_sessions=16,
                adaptation_notes="Adjust hierarchy based on individual fears and functioning level",
                prerequisite_skills=["Basic anxiety management", "SUDS rating understanding"],
                evidence_base="Extensive research support for social anxiety treatment"
            ),
            
            ExposureProtocol(
                protocol_id="exp_protocol_002",
                name="Specific Phobia Exposure Protocol",
                target_conditions=["Specific Phobia", "Animal Phobia", "Situational Phobia"],
                description="Graduated exposure protocol for specific phobias",
                typical_hierarchy_items=[
                    {"level": 1, "description": "View photos of feared object", "type": "in_vivo", "duration": 10},
                    {"level": 2, "description": "Watch videos of feared object", "type": "in_vivo", "duration": 15},
                    {"level": 3, "description": "View feared object from distance", "type": "in_vivo", "duration": 20},
                    {"level": 4, "description": "Move closer to feared object", "type": "in_vivo", "duration": 25},
                    {"level": 5, "description": "Touch/interact with feared object briefly", "type": "in_vivo", "duration": 30},
                    {"level": 6, "description": "Extended interaction with feared object", "type": "in_vivo", "duration": 45},
                    {"level": 7, "description": "Handle feared object independently", "type": "in_vivo", "duration": 60},
                    {"level": 8, "description": "Normal interaction without avoidance", "type": "in_vivo", "duration": 60}
                ],
                session_structure=[
                    "Review hierarchy and assess readiness",
                    "Relaxation preparation",
                    "Begin exposure at appropriate level",
                    "Monitor anxiety levels throughout",
                    "Continue until habituation occurs",
                    "Practice coping skills during exposure",
                    "Assign between-session practice"
                ],
                safety_guidelines=[
                    "Ensure medical safety for exposure",
                    "Have emergency procedures ready",
                    "Monitor for panic responses",
                    "Use grounding techniques as needed",
                    "Respect patient's limits while encouraging progress"
                ],
                contraindications=[
                    "Medical conditions affected by exposure",
                    "Severe panic disorder",
                    "Recent traumatic exposure",
                    "Cognitive impairment affecting consent"
                ],
                typical_session_duration=45,
                sessions_per_week=2,
                estimated_total_sessions=8,
                adaptation_notes="Highly individualized based on specific phobia type",
                prerequisite_skills=["Relaxation techniques", "Understanding of exposure rationale"],
                evidence_base="Gold standard treatment for specific phobias with high success rates"
            ),
            
            ExposureProtocol(
                protocol_id="exp_protocol_003",
                name="PTSD Imaginal Exposure Protocol",
                target_conditions=["PTSD", "Acute Stress Disorder", "Trauma-related anxiety"],
                description="Imaginal exposure protocol for trauma processing",
                typical_hierarchy_items=[
                    {"level": 1, "description": "Discuss trauma in general terms", "type": "cognitive", "duration": 15},
                    {"level": 2, "description": "Write brief trauma summary", "type": "cognitive", "duration": 20},
                    {"level": 3, "description": "Imagine trauma periphery details", "type": "imaginal", "duration": 25},
                    {"level": 4, "description": "Imagine trauma beginning", "type": "imaginal", "duration": 30},
                    {"level": 5, "description": "Imagine full trauma sequence", "type": "imaginal", "duration": 45},
                    {"level": 6, "description": "Record trauma narrative", "type": "imaginal", "duration": 45},
                    {"level": 7, "description": "Listen to trauma recording", "type": "imaginal", "duration": 60},
                    {"level": 8, "description": "Process trauma meaning", "type": "cognitive", "duration": 60}
                ],
                session_structure=[
                    "Safety check and grounding",
                    "Review previous session processing",
                    "Prepare for imaginal exposure",
                    "Conduct imaginal reliving",
                    "Record SUDS ratings throughout",
                    "Process emotions and thoughts",
                    "Plan between-session listening"
                ],
                safety_guidelines=[
                    "Establish strong therapeutic alliance first",
                    "Ensure patient stability",
                    "Monitor for dissociation",
                    "Have crisis plan available",
                    "Process emotions thoroughly after exposure"
                ],
                contraindications=[
                    "Active suicidal ideation",
                    "Severe dissociative disorder",
                    "Active substance abuse",
                    "Unstable living situation"
                ],
                typical_session_duration=90,
                sessions_per_week=1,
                estimated_total_sessions=12,
                adaptation_notes="Requires specialized PTSD training and careful case formulation",
                prerequisite_skills=["Grounding techniques", "Emotional regulation", "Strong therapeutic alliance"],
                evidence_base="Empirically supported treatment for PTSD"
            ),
            
            ExposureProtocol(
                protocol_id="exp_protocol_004",
                name="Panic Disorder Interoceptive Exposure",
                target_conditions=["Panic Disorder", "Agoraphobia", "Anxiety Sensitivity"],
                description="Interoceptive exposure protocol for panic-related fears",
                typical_hierarchy_items=[
                    {"level": 1, "description": "Shake head side to side (dizziness)", "type": "interoceptive", "duration": 30},
                    {"level": 2, "description": "Breathe through straw (breathlessness)", "type": "interoceptive", "duration": 60},
                    {"level": 3, "description": "Run in place (heart rate increase)", "type": "interoceptive", "duration": 90},
                    {"level": 4, "description": "Hyperventilation exercise", "type": "interoceptive", "duration": 60},
                    {"level": 5, "description": "Spin in chair (dizziness/nausea)", "type": "interoceptive", "duration": 60},
                    {"level": 6, "description": "Chest tension exercise", "type": "interoceptive", "duration": 90},
                    {"level": 7, "description": "Combined sensation exercises", "type": "interoceptive", "duration": 120},
                    {"level": 8, "description": "Real-world situation exposure", "type": "in_vivo", "duration": 180}
                ],
                session_structure=[
                    "Review panic cycle and rationale",
                    "Select interoceptive exercise",
                    "Rate baseline anxiety and sensation fear",
                    "Conduct exercise with monitoring",
                    "Continue until anxiety habituation",
                    "Discuss catastrophic interpretations",
                    "Plan home practice exercises"
                ],
                safety_guidelines=[
                    "Screen for medical contraindications",
                    "Monitor for actual medical distress",
                    "Have medical emergency plan",
                    "Stop if true medical emergency",
                    "Differentiate anxiety from medical issues"
                ],
                contraindications=[
                    "Cardiac conditions",
                    "Respiratory disorders",
                    "Seizure disorders",
                    "Pregnancy (some exercises)"
                ],
                typical_session_duration=50,
                sessions_per_week=2,
                estimated_total_sessions=10,
                adaptation_notes="Must screen for medical conditions and adapt exercises accordingly",
                prerequisite_skills=["Understanding of panic cycle", "Basic breathing techniques"],
                evidence_base="Core component of panic disorder treatment with strong research support"
            )
        ]
        
        return protocols
    
    def _save_exposure_protocol(self, protocol: ExposureProtocol, is_default: bool = False):
        """Save exposure protocol to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO exposure_protocols (
                    protocol_id, name, target_conditions, description,
                    typical_hierarchy_items, session_structure, safety_guidelines,
                    contraindications, typical_session_duration, sessions_per_week,
                    estimated_total_sessions, adaptation_notes, prerequisite_skills,
                    evidence_base, is_default
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                protocol.protocol_id, protocol.name, json.dumps(protocol.target_conditions),
                protocol.description, json.dumps(protocol.typical_hierarchy_items),
                json.dumps(protocol.session_structure), json.dumps(protocol.safety_guidelines),
                json.dumps(protocol.contraindications), protocol.typical_session_duration,
                protocol.sessions_per_week, protocol.estimated_total_sessions,
                protocol.adaptation_notes, json.dumps(protocol.prerequisite_skills),
                protocol.evidence_base, is_default
            ))
            conn.commit()
    
    # ========================================================================
    # HIERARCHY DEVELOPMENT AND MANAGEMENT
    # ========================================================================
    
    def create_exposure_hierarchy(
        self,
        patient_id: str,
        target_fear: str,
        fear_category: str,
        protocol_id: str = None,
        custom_items: List[Dict[str, Any]] = None
    ) -> ExposureHierarchy:
        """Create exposure hierarchy for patient"""
        hierarchy_id = f"hier_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Default mastery criteria
        mastery_criteria = {
            "anxiety_reduction_percentage": 50,  # 50% reduction from peak
            "successful_completions_required": 2,
            "maximum_end_anxiety": 3,  # End SUDS ≤ 3
            "minimum_session_duration": 0.75  # 75% of planned duration
        }
        
        # Create hierarchy
        hierarchy = ExposureHierarchy(
            hierarchy_id=hierarchy_id,
            patient_id=patient_id,
            target_fear=target_fear,
            fear_category=fear_category,
            exposure_items=[],
            current_level=1,
            mastery_criteria=mastery_criteria,
            created_date=datetime.now(),
            last_updated=datetime.now()
        )
        
        # Generate exposure items
        if protocol_id:
            hierarchy.exposure_items = self._generate_items_from_protocol(hierarchy_id, protocol_id)
        elif custom_items:
            hierarchy.exposure_items = self._generate_custom_items(hierarchy_id, custom_items)
        else:
            raise ValueError("Either protocol_id or custom_items must be provided")
        
        # Save hierarchy
        self._save_exposure_hierarchy(hierarchy)
        
        return hierarchy
    
    def _generate_items_from_protocol(self, hierarchy_id: str, protocol_id: str) -> List[ExposureItem]:
        """Generate exposure items from protocol template"""
        protocol = self._get_protocol_by_id(protocol_id)
        if not protocol:
            raise ValueError(f"Protocol {protocol_id} not found")
        
        items = []
        for item_data in protocol.typical_hierarchy_items:
            item_id = f"item_{hierarchy_id}_{item_data['level']}"
            
            item = ExposureItem(
                item_id=item_id,
                description=item_data['description'],
                exposure_type=ExposureType(item_data['type']),
                difficulty_level=item_data['level'],
                estimated_duration=item_data['duration']
            )
            items.append(item)
        
        return items
    
    def _generate_custom_items(self, hierarchy_id: str, custom_items: List[Dict[str, Any]]) -> List[ExposureItem]:
        """Generate exposure items from custom specifications"""
        items = []
        for i, item_data in enumerate(custom_items):
            item_id = f"item_{hierarchy_id}_{i+1}"
            
            item = ExposureItem(
                item_id=item_id,
                description=item_data['description'],
                exposure_type=ExposureType(item_data.get('type', 'in_vivo')),
                difficulty_level=item_data.get('level', i+1),
                estimated_duration=item_data.get('duration', 30),
                location=item_data.get('location', ''),
                materials_needed=item_data.get('materials_needed', []),
                safety_considerations=item_data.get('safety_considerations', []),
                instructions=item_data.get('instructions', '')
            )
            items.append(item)
        
        return items
    
    def get_hierarchy_suggestions(
        self,
        fear_category: str,
        specific_fears: List[str],
        severity_level: int = 5
    ) -> List[Dict[str, Any]]:
        """Get hierarchy suggestions based on fear type"""
        # Get relevant protocols
        protocols = self._get_protocols_by_category(fear_category)
        
        suggestions = []
        for protocol in protocols:
            # Adapt items based on severity
            adapted_items = []
            for item in protocol.typical_hierarchy_items:
                adapted_item = item.copy()
                
                # Adjust difficulty based on severity
                if severity_level <= 3:  # Mild
                    adapted_item['level'] = max(1, adapted_item['level'] - 1)
                elif severity_level >= 7:  # Severe
                    adapted_item['level'] = min(8, adapted_item['level'] + 1)
                
                adapted_items.append(adapted_item)
            
            suggestions.append({
                'protocol_name': protocol.name,
                'protocol_id': protocol.protocol_id,
                'items': adapted_items,
                'estimated_sessions': protocol.estimated_total_sessions
            })
        
        return suggestions
    
    # ========================================================================
    # EXPOSURE SESSION MANAGEMENT
    # ========================================================================
    
    def plan_exposure_session(
        self,
        patient_id: str,
        hierarchy_id: str,
        target_level: int = None,
        planned_date: datetime = None,
        duration: int = None
    ) -> ExposureSession:
        """Plan next exposure session"""
        hierarchy = self.get_exposure_hierarchy(hierarchy_id)
        if not hierarchy:
            raise ValueError(f"Hierarchy {hierarchy_id} not found")
        
        # Determine target item
        if target_level is None:
            target_level = hierarchy.current_level
        
        target_item = None
        for item in hierarchy.exposure_items:
            if item.difficulty_level == target_level:
                target_item = item
                break
        
        if not target_item:
            raise ValueError(f"No item found for level {target_level}")
        
        # Create session
        session_id = f"exp_session_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = ExposureSession(
            session_id=session_id,
            patient_id=patient_id,
            item_id=target_item.item_id,
            exposure_type=target_item.exposure_type,
            planned_date=planned_date or (datetime.now() + timedelta(days=7)),
            planned_duration=duration or target_item.estimated_duration,
            title=f"Exposure Session - Level {target_level}",
            description=target_item.description,
            goals=[
                f"Complete exposure to: {target_item.description}",
                "Achieve anxiety habituation",
                "Learn that anxiety decreases naturally",
                "Build confidence for next level"
            ],
            safety_plan=[
                "Monitor SUDS ratings throughout",
                "Use grounding techniques if needed",
                "Stop if medical emergency",
                "Process emotions after exposure"
            ],
            status=ExposureStatus.PLANNED,
            created_date=datetime.now()
        )
        
        return session
    
    def conduct_exposure_session(
        self,
        session_id: str,
        baseline_anxiety: int,
        anxiety_ratings: List[Tuple[int, int]],  # (time_minutes, anxiety_level)
        end_anxiety: int,
        habituation_achieved: bool,
        premature_termination: bool = False,
        termination_reason: str = "",
        success_indicators: List[str] = None,
        difficulties: List[str] = None,
        coping_strategies: List[str] = None,
        key_learnings: List[str] = None
    ) -> bool:
        """Record exposure session results"""
        if not anxiety_ratings:
            return False
        
        # Calculate peak anxiety
        peak_anxiety = max([rating[1] for rating in anxiety_ratings])
        
        # Calculate actual duration
        if anxiety_ratings:
            actual_duration = anxiety_ratings[-1][0]  # Last time point
        else:
            actual_duration = 0
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Update session
            cursor.execute("""
                UPDATE exposure_sessions 
                SET status = ?, actual_start_time = ?, actual_duration = ?,
                    baseline_anxiety = ?, peak_anxiety = ?, end_anxiety = ?,
                    anxiety_ratings = ?, habituation_achieved = ?,
                    premature_termination = ?, termination_reason = ?,
                    success_indicators = ?, difficulties_encountered = ?,
                    coping_strategies_used = ?, key_learnings = ?
                WHERE session_id = ?
            """, (
                ExposureStatus.COMPLETED.value, datetime.now(), actual_duration,
                baseline_anxiety, peak_anxiety, end_anxiety,
                json.dumps(anxiety_ratings), habituation_achieved,
                premature_termination, termination_reason,
                json.dumps(success_indicators or []), json.dumps(difficulties or []),
                json.dumps(coping_strategies or []), json.dumps(key_learnings or []),
                session_id
            ))
            
            if cursor.rowcount > 0:
                # Update exposure item statistics
                self._update_item_statistics(cursor, session_id, peak_anxiety, end_anxiety, habituation_achieved)
                
                # Check if level mastery achieved
                self._check_level_mastery(cursor, session_id)
                
                conn.commit()
                return True
            
            return False

    def _update_item_statistics(self, cursor, session_id: str, peak_anxiety: int, end_anxiety: int, success: bool):
        """Update exposure item statistics after session"""
        # Get item_id from session
        cursor.execute("SELECT item_id FROM exposure_sessions WHERE session_id = ?", (session_id,))
        result = cursor.fetchone()
        if not result:
            return
        
        item_id = result[0]
        
        # Update item statistics
        cursor.execute("""
            UPDATE exposure_items 
            SET attempts = attempts + 1,
                successful_completions = CASE WHEN ? THEN successful_completions + 1 ELSE successful_completions END,
                average_peak_anxiety = CASE 
                    WHEN average_peak_anxiety IS NULL THEN ?
                    ELSE (average_peak_anxiety * (attempts - 1) + ?) / attempts
                END,
                average_end_anxiety = CASE 
                    WHEN average_end_anxiety IS NULL THEN ?
                    ELSE (average_end_anxiety * (attempts - 1) + ?) / attempts
                END
            WHERE item_id = ?
        """, (success, peak_anxiety, peak_anxiety, end_anxiety, end_anxiety, item_id))

    def _check_level_mastery(self, cursor, session_id: str):
        """Check if current level has been mastered"""
        # Get session and hierarchy info
        cursor.execute("""
            SELECT es.item_id, ei.difficulty_level, ei.hierarchy_id, eh.mastery_criteria
            FROM exposure_sessions es
            JOIN exposure_items ei ON es.item_id = ei.item_id
            JOIN exposure_hierarchies eh ON ei.hierarchy_id = eh.hierarchy_id
            WHERE es.session_id = ?
        """, (session_id,))
        
        result = cursor.fetchone()
        if not result:
            return
        
        item_id, difficulty_level, hierarchy_id, mastery_criteria_json = result
        mastery_criteria = json.loads(mastery_criteria_json or '{}')
        
        # Check mastery criteria
        cursor.execute("""
            SELECT successful_completions, average_end_anxiety
            FROM exposure_items 
            WHERE item_id = ?
        """, (item_id,))
        
        item_stats = cursor.fetchone()
        if not item_stats:
            return
        
        successful_completions, avg_end_anxiety = item_stats
        
        # Check if mastery criteria met
        required_completions = mastery_criteria.get('successful_completions_required', 2)
        max_end_anxiety = mastery_criteria.get('maximum_end_anxiety', 3)
        
        is_mastered = (
            successful_completions >= required_completions and
            (avg_end_anxiety is None or avg_end_anxiety <= max_end_anxiety)
        )
        
        if is_mastered:
            # Update hierarchy to mark level as mastered
            cursor.execute("""
                SELECT levels_mastered FROM exposure_hierarchies WHERE hierarchy_id = ?
            """, (hierarchy_id,))
            
            levels_data = cursor.fetchone()
            if levels_data:
                levels_mastered = json.loads(levels_data[0] or '[]')
                if difficulty_level not in levels_mastered:
                    levels_mastered.append(difficulty_level)
                    
                    # Update current level if this was the current level
                    cursor.execute("""
                        UPDATE exposure_hierarchies 
                        SET levels_mastered = ?,
                            current_level = CASE 
                                WHEN current_level = ? THEN ? 
                                ELSE current_level 
                            END,
                            last_updated = ?
                        WHERE hierarchy_id = ?
                    """, (
                        json.dumps(levels_mastered), difficulty_level, 
                        min(difficulty_level + 1, 8), datetime.now(), hierarchy_id
                    ))

    # ========================================================================
    # DATA PERSISTENCE AND RETRIEVAL
    # ========================================================================

    def _save_exposure_hierarchy(self, hierarchy: ExposureHierarchy):
        """Save exposure hierarchy to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Save hierarchy
            cursor.execute("""
                INSERT OR REPLACE INTO exposure_hierarchies (
                    hierarchy_id, patient_id, target_fear, fear_category,
                    current_level, mastery_criteria, total_sessions_completed,
                    levels_mastered, estimated_completion_date, created_date,
                    last_updated, therapist_notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                hierarchy.hierarchy_id, hierarchy.patient_id, hierarchy.target_fear,
                hierarchy.fear_category, hierarchy.current_level,
                json.dumps(hierarchy.mastery_criteria), hierarchy.total_sessions_completed,
                json.dumps(hierarchy.levels_mastered), hierarchy.estimated_completion_date,
                hierarchy.created_date, hierarchy.last_updated, hierarchy.therapist_notes
            ))
            
            # Save exposure items
            for item in hierarchy.exposure_items:
                cursor.execute("""
                    INSERT OR REPLACE INTO exposure_items (
                        item_id, hierarchy_id, description, exposure_type,
                        difficulty_level, estimated_duration, location,
                        materials_needed, safety_considerations, instructions,
                        attempts, successful_completions, average_peak_anxiety,
                        average_end_anxiety, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item.item_id, hierarchy.hierarchy_id, item.description,
                    item.exposure_type.value, item.difficulty_level,
                    item.estimated_duration, item.location,
                    json.dumps(item.materials_needed), json.dumps(item.safety_considerations),
                    item.instructions, item.attempts, item.successful_completions,
                    item.average_peak_anxiety, item.average_end_anxiety, item.notes
                ))
            
            conn.commit()

    def save_exposure_session(self, session: ExposureSession):
        """Save exposure session to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO exposure_sessions (
                    session_id, patient_id, item_id, exposure_type, planned_date,
                    planned_duration, title, description, goals, safety_plan,
                    status, actual_start_time, actual_duration, baseline_anxiety,
                    peak_anxiety, end_anxiety, anxiety_ratings, habituation_achieved,
                    premature_termination, termination_reason, success_indicators,
                    difficulties_encountered, coping_strategies_used, key_learnings,
                    next_exposure_recommendations, homework_assigned, created_date,
                    therapist_notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id, session.patient_id, session.item_id,
                session.exposure_type.value, session.planned_date, session.planned_duration,
                session.title, session.description, json.dumps(session.goals),
                json.dumps(session.safety_plan), session.status.value,
                session.actual_start_time, session.actual_duration, session.baseline_anxiety,
                session.peak_anxiety, session.end_anxiety, json.dumps(session.anxiety_ratings),
                session.habituation_achieved, session.premature_termination,
                session.termination_reason, json.dumps(session.success_indicators),
                json.dumps(session.difficulties_encountered), json.dumps(session.coping_strategies_used),
                json.dumps(session.key_learnings), session.next_exposure_recommendations,
                json.dumps(session.homework_assigned), session.created_date, session.therapist_notes
            ))
            conn.commit()

    def get_exposure_hierarchy(self, hierarchy_id: str) -> Optional[ExposureHierarchy]:
        """Retrieve exposure hierarchy by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get hierarchy
            cursor.execute("SELECT * FROM exposure_hierarchies WHERE hierarchy_id = ?", (hierarchy_id,))
            hier_data = cursor.fetchone()
            if not hier_data:
                return None
            
            # Get exposure items
            cursor.execute("""
                SELECT * FROM exposure_items 
                WHERE hierarchy_id = ? 
                ORDER BY difficulty_level
            """, (hierarchy_id,))
            items_data = cursor.fetchall()
            
            return self._reconstruct_hierarchy(hier_data, items_data)

    def get_patient_hierarchies(self, patient_id: str) -> List[ExposureHierarchy]:
        """Get all exposure hierarchies for patient"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT hierarchy_id FROM exposure_hierarchies 
                WHERE patient_id = ? 
                ORDER BY created_date DESC
            """, (patient_id,))
            
            hierarchy_ids = [row[0] for row in cursor.fetchall()]
            
            hierarchies = []
            for hier_id in hierarchy_ids:
                hierarchy = self.get_exposure_hierarchy(hier_id)
                if hierarchy:
                    hierarchies.append(hierarchy)
            
            return hierarchies

    def get_exposure_session(self, session_id: str) -> Optional[ExposureSession]:
        """Retrieve exposure session by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM exposure_sessions WHERE session_id = ?", (session_id,))
            session_data = cursor.fetchone()
            
            if not session_data:
                return None
            
            return self._reconstruct_session(session_data)

    def get_patient_sessions(
        self, 
        patient_id: str, 
        status_filter: ExposureStatus = None,
        limit: int = None
    ) -> List[ExposureSession]:
        """Get exposure sessions for patient"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = "SELECT session_id FROM exposure_sessions WHERE patient_id = ?"
            params = [patient_id]
            
            if status_filter:
                query += " AND status = ?"
                params.append(status_filter.value)
            
            query += " ORDER BY planned_date DESC"
            
            if limit:
                query += f" LIMIT {limit}"
            
            cursor.execute(query, params)
            session_ids = [row[0] for row in cursor.fetchall()]
            
            sessions = []
            for session_id in session_ids:
                session = self.get_exposure_session(session_id)
                if session:
                    sessions.append(session)
            
            return sessions

    # ========================================================================
    # DATA RECONSTRUCTION HELPERS
    # ========================================================================

    def _reconstruct_hierarchy(self, hier_data, items_data) -> ExposureHierarchy:
        """Reconstruct ExposureHierarchy from database data"""
        # Reconstruct items
        items = []
        for row in items_data:
            item = ExposureItem(
                item_id=row[0],
                description=row[2],
                exposure_type=ExposureType(row[3]),
                difficulty_level=row[4],
                estimated_duration=row[5],
                location=row[6] or "",
                materials_needed=json.loads(row[7] or '[]'),
                safety_considerations=json.loads(row[8] or '[]'),
                instructions=row[9] or "",
                attempts=row[10],
                successful_completions=row[11],
                average_peak_anxiety=row[12],
                average_end_anxiety=row[13],
                notes=row[14] or ""
            )
            items.append(item)
        
        # Reconstruct hierarchy
        return ExposureHierarchy(
            hierarchy_id=hier_data[0],
            patient_id=hier_data[1],
            target_fear=hier_data[2],
            fear_category=hier_data[3],
            exposure_items=items,
            current_level=hier_data[4],
            mastery_criteria=json.loads(hier_data[5] or '{}'),
            total_sessions_completed=hier_data[6],
            levels_mastered=json.loads(hier_data[7] or '[]'),
            estimated_completion_date=datetime.fromisoformat(hier_data[8]) if hier_data[8] else None,
            created_date=datetime.fromisoformat(hier_data[9]),
            last_updated=datetime.fromisoformat(hier_data[10]),
            therapist_notes=hier_data[11] or ""
        )

    def _reconstruct_session(self, session_data) -> ExposureSession:
        """Reconstruct ExposureSession from database data"""
        return ExposureSession(
            session_id=session_data[0],
            patient_id=session_data[1],
            item_id=session_data[2],
            exposure_type=ExposureType(session_data[3]),
            planned_date=datetime.fromisoformat(session_data[4]),
            planned_duration=session_data[5],
            title=session_data[6],
            description=session_data[7] or "",
            goals=json.loads(session_data[8] or '[]'),
            safety_plan=json.loads(session_data[9] or '[]'),
            status=ExposureStatus(session_data[10]),
            actual_start_time=datetime.fromisoformat(session_data[11]) if session_data[11] else None,
            actual_duration=session_data[12],
            baseline_anxiety=session_data[13],
            peak_anxiety=session_data[14],
            end_anxiety=session_data[15],
            anxiety_ratings=json.loads(session_data[16] or '[]'),
            habituation_achieved=bool(session_data[17]) if session_data[17] is not None else None,
            premature_termination=bool(session_data[18]) if session_data[18] is not None else None,
            termination_reason=session_data[19] or "",
            success_indicators=json.loads(session_data[20] or '[]'),
            difficulties_encountered=json.loads(session_data[21] or '[]'),
            coping_strategies_used=json.loads(session_data[22] or '[]'),
            key_learnings=json.loads(session_data[23] or '[]'),
            next_exposure_recommendations=session_data[24] or "",
            homework_assigned=json.loads(session_data[25] or '[]'),
            created_date=datetime.fromisoformat(session_data[26]),
            therapist_notes=session_data[27] or ""
        )


    def _get_protocol_by_id(self, protocol_id: str) -> Optional[ExposureProtocol]:
        """Get exposure protocol by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM exposure_protocols WHERE protocol_id = ?", (protocol_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return ExposureProtocol(
                protocol_id=row[0],
                name=row[1],
                target_conditions=json.loads(row[2] or '[]'),
                description=row[3],
                typical_hierarchy_items=json.loads(row[4] or '[]'),
                session_structure=json.loads(row[5] or '[]'),
                safety_guidelines=json.loads(row[6] or '[]'),
                contraindications=json.loads(row[7] or '[]'),
                typical_session_duration=row[8],
                sessions_per_week=row[9],
                estimated_total_sessions=row[10],
                adaptation_notes=row[11] or "",
                prerequisite_skills=json.loads(row[12] or '[]'),
                evidence_base=row[13] or ""
            )

    def _get_protocols_by_category(self, fear_category: str) -> List[ExposureProtocol]:
        """Get protocols relevant to fear category"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM exposure_protocols WHERE is_default = TRUE")
            rows = cursor.fetchall()
            
            protocols = []
            for row in rows:
                protocol = ExposureProtocol(
                    protocol_id=row[0],
                    name=row[1],
                    target_conditions=json.loads(row[2] or '[]'),
                    description=row[3],
                    typical_hierarchy_items=json.loads(row[4] or '[]'),
                    session_structure=json.loads(row[5] or '[]'),
                    safety_guidelines=json.loads(row[6] or '[]'),
                    contraindications=json.loads(row[7] or '[]'),
                    typical_session_duration=row[8],
                    sessions_per_week=row[9],
                    estimated_total_sessions=row[10],
                    adaptation_notes=row[11] or "",
                    prerequisite_skills=json.loads(row[12] or '[]'),
                    evidence_base=row[13] or ""
                )
                
                # Check if protocol is relevant to fear category
                if any(fear_category.lower() in condition.lower() for condition in protocol.target_conditions):
                    protocols.append(protocol)
            
            return protocols

    # ========================================================================
    # PROGRESS ANALYSIS AND REPORTING
    # ========================================================================

    def generate_hierarchy_progress_report(self, hierarchy_id: str) -> Dict[str, Any]:
        """Generate progress report for exposure hierarchy"""
        hierarchy = self.get_exposure_hierarchy(hierarchy_id)
        if not hierarchy:
            return {"error": "Hierarchy not found"}
        
        # Get all sessions for this hierarchy
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT es.* FROM exposure_sessions es
                JOIN exposure_items ei ON es.item_id = ei.item_id
                WHERE ei.hierarchy_id = ? AND es.status = 'completed'
                ORDER BY es.planned_date
            """, (hierarchy_id,))
            
            session_data = cursor.fetchall()
            sessions = [self._reconstruct_session(row) for row in session_data]
        
        # Calculate progress metrics
        total_levels = len(hierarchy.exposure_items)
        levels_mastered = len(hierarchy.levels_mastered)
        completion_percentage = (levels_mastered / total_levels * 100) if total_levels > 0 else 0
        
        # Analyze anxiety trends
        anxiety_trends = self._analyze_anxiety_trends(sessions)
        
        # Calculate session statistics
        session_stats = self._calculate_session_statistics(sessions)
        
        # Identify patterns and recommendations
        patterns = self._identify_exposure_patterns(hierarchy, sessions)
        
        report = {
            "hierarchy_overview": {
                "hierarchy_id": hierarchy.hierarchy_id,
                "target_fear": hierarchy.target_fear,
                "fear_category": hierarchy.fear_category,
                "current_level": hierarchy.current_level,
                "total_levels": total_levels,
                "levels_mastered": levels_mastered,
                "completion_percentage": round(completion_percentage, 1)
            },
            "session_statistics": session_stats,
            "anxiety_trends": anxiety_trends,
            "level_progress": [
                {
                    "level": item.difficulty_level,
                    "description": item.description,
                    "attempts": item.attempts,
                    "successful_completions": item.successful_completions,
                    "success_rate": round((item.successful_completions / item.attempts * 100) if item.attempts > 0 else 0, 1),
                    "average_peak_anxiety": round(item.average_peak_anxiety, 1) if item.average_peak_anxiety else None,
                    "average_end_anxiety": round(item.average_end_anxiety, 1) if item.average_end_anxiety else None,
                    "mastered": item.difficulty_level in hierarchy.levels_mastered
                }
                for item in hierarchy.exposure_items
            ],
            "patterns_and_insights": patterns,
            "recommendations": self._generate_exposure_recommendations(hierarchy, sessions, patterns)
        }
        
        return report

    def _analyze_anxiety_trends(self, sessions: List[ExposureSession]) -> Dict[str, Any]:
        """Analyze anxiety trends across sessions"""
        if not sessions:
            return {}
        
        baseline_anxieties = [s.baseline_anxiety for s in sessions if s.baseline_anxiety is not None]
        peak_anxieties = [s.peak_anxiety for s in sessions if s.peak_anxiety is not None]
        end_anxieties = [s.end_anxiety for s in sessions if s.end_anxiety is not None]
        
        # Calculate habituation rates
        habituation_rates = []
        for session in sessions:
            if session.peak_anxiety and session.end_anxiety:
                rate = (session.peak_anxiety - session.end_anxiety) / session.peak_anxiety * 100
                habituation_rates.append(rate)
        
        return {
            "average_baseline_anxiety": round(sum(baseline_anxieties) / len(baseline_anxieties), 1) if baseline_anxieties else None,
            "average_peak_anxiety": round(sum(peak_anxieties) / len(peak_anxieties), 1) if peak_anxieties else None,
            "average_end_anxiety": round(sum(end_anxieties) / len(end_anxieties), 1) if end_anxieties else None,
            "average_habituation_rate": round(sum(habituation_rates) / len(habituation_rates), 1) if habituation_rates else None,
            "baseline_trend": "decreasing" if len(baseline_anxieties) > 1 and baseline_anxieties[-1] < baseline_anxieties[0] else "stable",
            "sessions_with_good_habituation": len([r for r in habituation_rates if r >= 50])
        }

    def _calculate_session_statistics(self, sessions: List[ExposureSession]) -> Dict[str, Any]:
        """Calculate session-level statistics"""
        if not sessions:
            return {}
        
        completed_sessions = len(sessions)
        habituation_achieved = len([s for s in sessions if s.habituation_achieved])
        premature_terminations = len([s for s in sessions if s.premature_termination])
        
        durations = [s.actual_duration for s in sessions if s.actual_duration]
        avg_duration = sum(durations) / len(durations) if durations else None
        
        return {
            "total_sessions_completed": completed_sessions,
            "sessions_with_habituation": habituation_achieved,
            "habituation_rate": round((habituation_achieved / completed_sessions * 100), 1) if completed_sessions > 0 else 0,
            "premature_terminations": premature_terminations,
            "completion_rate": round(((completed_sessions - premature_terminations) / completed_sessions * 100), 1) if completed_sessions > 0 else 0,
            "average_session_duration": round(avg_duration, 1) if avg_duration else None
        }

    def _identify_exposure_patterns(self, hierarchy: ExposureHierarchy, sessions: List[ExposureSession]) -> List[str]:
        """Identify patterns in exposure progress"""
        patterns = []
        
        if not sessions:
            return patterns
        
        # Check for consistent habituation
        habituation_sessions = [s for s in sessions if s.habituation_achieved]
        habituation_rate = len(habituation_sessions) / len(sessions)
        
        if habituation_rate > 0.8:
            patterns.append("Consistent habituation pattern - excellent progress")
        elif habituation_rate < 0.3:
            patterns.append("Limited habituation - may need longer sessions or different approach")
        
        # Check for anxiety reduction over time
        baseline_anxieties = [s.baseline_anxiety for s in sessions if s.baseline_anxiety is not None]
        if len(baseline_anxieties) > 3:
            recent_avg = sum(baseline_anxieties[-3:]) / 3
            early_avg = sum(baseline_anxieties[:3]) / 3
            if recent_avg < early_avg - 1:
                patterns.append("Baseline anxiety decreasing over time - good generalization")
        
        # Check for stuck levels
        current_level_sessions = len([s for s in sessions if any(
            item.item_id == s.item_id and item.difficulty_level == hierarchy.current_level 
            for item in hierarchy.exposure_items
        )])
        if current_level_sessions > 4:
            patterns.append(f"Multiple attempts at level {hierarchy.current_level} - consider adjusting approach")
        
        # Check termination patterns
        terminations = [s for s in sessions if s.premature_termination]
        if len(terminations) > len(sessions) * 0.3:
            patterns.append("Frequent early terminations - review safety plans and coping strategies")
        
        return patterns

    def _generate_exposure_recommendations(
        self, 
        hierarchy: ExposureHierarchy, 
        sessions: List[ExposureSession],
        patterns: List[str]
    ) -> List[str]:
        """Generate recommendations for exposure therapy"""
        recommendations = []
        
        # Progress-based recommendations
        if hierarchy.exposure_items:
            completion_rate = len(hierarchy.levels_mastered) / len(hierarchy.exposure_items)
            
            if completion_rate < 0.3:
                recommendations.append("Consider starting with easier items or extending session duration")
            elif completion_rate > 0.7:
                recommendations.append("Excellent progress! Focus on generalization and maintenance")
        
        # Session-based recommendations
        if sessions:
            avg_habituation = sum(1 for s in sessions if s.habituation_achieved) / len(sessions)
            
            if avg_habituation < 0.5:
                recommendations.append("Low habituation rate - consider longer sessions or addressing avoidance behaviors")
            
            # Anxiety level recommendations
            recent_sessions = sessions[-3:] if len(sessions) >= 3 else sessions
            high_baseline = sum(1 for s in recent_sessions if s.baseline_anxiety and s.baseline_anxiety > 7)
            
            if high_baseline > len(recent_sessions) * 0.5:
                recommendations.append("High baseline anxiety - increase between-session practice and relaxation skills")
        
        # Pattern-based recommendations
        if "Limited habituation" in str(patterns):
            recommendations.append("Consider interoceptive exposure or addressing safety behaviors")
        
        if "early terminations" in str(patterns):
            recommendations.append("Strengthen coping skills training before continuing exposure")
        
        # Level-specific recommendations
        if hierarchy.current_level <= 3:
            recommendations.append("Focus on building confidence with current level mastery")
        elif hierarchy.current_level >= 6:
            recommendations.append("Prepare for real-world generalization and relapse prevention")
        
        return recommendations

    # ========================================================================
    # UTILITY AND CONVENIENCE METHODS
    # ========================================================================

    def get_next_recommended_exposure(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get next recommended exposure for patient"""
        hierarchies = self.get_patient_hierarchies(patient_id)
        
        if not hierarchies:
            return None
        
        # Find most active hierarchy
        active_hierarchy = max(hierarchies, key=lambda h: h.total_sessions_completed)
        
        # Find appropriate level
        current_level = active_hierarchy.current_level
        current_item = None
        
        for item in active_hierarchy.exposure_items:
            if item.difficulty_level == current_level:
                current_item = item
                break
        
        if not current_item:
            return None
        
        # Check if current level is mastered
        mastery_criteria = active_hierarchy.mastery_criteria
        required_completions = mastery_criteria.get('successful_completions_required', 2)
        
        if current_item.successful_completions >= required_completions:
            # Move to next level
            next_level = min(current_level + 1, 8)
            for item in active_hierarchy.exposure_items:
                if item.difficulty_level == next_level:
                    current_item = item
                    break
        
        return {
            "hierarchy_id": active_hierarchy.hierarchy_id,
            "target_fear": active_hierarchy.target_fear,
            "recommended_item": {
                "item_id": current_item.item_id,
                "description": current_item.description,
                "level": current_item.difficulty_level,
                "type": current_item.exposure_type.value,
                "estimated_duration": current_item.estimated_duration,
                "attempts": current_item.attempts,
                "success_rate": round((current_item.successful_completions / current_item.attempts * 100) if current_item.attempts > 0 else 0, 1)
            },
            "preparation_notes": [
                "Review hierarchy and session goals",
                "Practice relaxation techniques",
                "Prepare any required materials",
                "Plan post-exposure processing"
            ]
        }

    def calculate_exposure_score(self, session: ExposureSession) -> Dict[str, Any]:
        """Calculate exposure effectiveness score"""
        if not all([session.baseline_anxiety, session.peak_anxiety, session.end_anxiety]):
            return {"error": "Incomplete anxiety data"}
        
        # Calculate habituation rate
        habituation_rate = (session.peak_anxiety - session.end_anxiety) / session.peak_anxiety * 100
        
        # Calculate approach behavior (completing vs avoiding)
        approach_score = 0
        if not session.premature_termination:
            approach_score += 40
        if session.habituation_achieved:
            approach_score += 30
        if session.actual_duration and session.planned_duration:
            duration_ratio = session.actual_duration / session.planned_duration
            approach_score += min(30, duration_ratio * 30)
        
        # Calculate overall effectiveness
        effectiveness = (habituation_rate * 0.6) + (approach_score * 0.4)
        effectiveness = max(0, min(100, effectiveness))
        
        return {
            "habituation_rate": round(habituation_rate, 1),
            "approach_score": round(approach_score, 1),
            "overall_effectiveness": round(effectiveness, 1),
            "effectiveness_level": (
                "Excellent" if effectiveness >= 80 else
                "Good" if effectiveness >= 60 else
                "Moderate" if effectiveness >= 40 else
                "Poor"
            ),
            "recommendations": self._get_session_recommendations(session, habituation_rate, approach_score)
        }

    def _get_session_recommendations(self, session: ExposureSession, habituation_rate: float, approach_score: float) -> List[str]:
        """Get recommendations based on session performance"""
        recommendations = []
        
        if habituation_rate < 30:
            recommendations.append("Consider longer exposure duration to allow more habituation")
            recommendations.append("Check for subtle avoidance behaviors during exposure")
        
        if approach_score < 50:
            recommendations.append("Work on increasing willingness to stay in exposure situations")
            recommendations.append("Strengthen coping skills before next exposure")
        
        if session.premature_termination:
            recommendations.append("Identify triggers for early termination and develop specific coping strategies")
        
        if session.peak_anxiety and session.peak_anxiety > 8:
            recommendations.append("Consider starting with slightly easier exposure or more preparation")
        
        if habituation_rate > 70 and approach_score > 70:
            recommendations.append("Excellent session! Consider progressing to next hierarchy level")
        
        return recommendations

    def create_exposure_homework(self, session_id: str) -> Dict[str, Any]:
        """Create homework assignment based on exposure session"""
        session = self.get_exposure_session(session_id)
        if not session:
            return {"error": "Session not found"}
        
        # Get hierarchy context
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT eh.target_fear, ei.description, ei.difficulty_level
                FROM exposure_sessions es
                JOIN exposure_items ei ON es.item_id = ei.item_id
                JOIN exposure_hierarchies eh ON ei.hierarchy_id = eh.hierarchy_id
                WHERE es.session_id = ?
            """, (session_id,))
            
            result = cursor.fetchone()
            if not result:
                return {"error": "Could not find session context"}
            
            target_fear, item_description, difficulty_level = result
        
        # Create homework based on session outcome
        if session.habituation_achieved and session.end_anxiety and session.end_anxiety <= 3:
            # Good session - practice current level
            homework_type = "reinforcement"
            homework_tasks = [
                f"Practice the same exposure: {item_description}",
                "Aim for similar or longer duration",
                "Focus on staying present during anxiety peaks",
                "Record SUDS ratings every 5-10 minutes"
            ]
        elif session.habituation_achieved:
            # Moderate session - repeat with modifications
            homework_type = "consolidation"
            homework_tasks = [
                f"Repeat exposure: {item_description}",
                "Try to extend duration by 10-15 minutes",
                "Practice without any safety behaviors",
                "Notice thoughts and feelings during exposure"
            ]
        else:
            # Difficult session - step back slightly
            homework_type = "preparation"
            homework_tasks = [
                "Practice relaxation techniques daily",
                f"Brief exposure to easier version of: {item_description}",
                "Focus on staying in situation until anxiety drops slightly",
                "Use coping strategies learned in session"
            ]
        
        homework = {
            "session_id": session_id,
            "homework_type": homework_type,
            "target_fear": target_fear,
            "difficulty_level": difficulty_level,
            "tasks": homework_tasks,
            "monitoring_instructions": [
                "Rate anxiety before, during (peak), and after exposure",
                "Note any avoidance behaviors or safety behaviors used",
                "Record duration of exposure",
                "Write brief notes about thoughts and feelings"
            ],
            "success_criteria": [
                "Complete at least 3 exposure practices",
                "Achieve some anxiety reduction in each practice",
                "Avoid early termination due to anxiety",
                "Use coping skills effectively"
            ],
            "emergency_plan": [
                "If anxiety becomes overwhelming, use grounding techniques",
                "Remember that anxiety will decrease naturally",
                "Contact therapist if unable to complete any exposures",
                "Do not avoid the situation completely"
            ]
        }
        
        return homework

    def get_hierarchy_completion_status(self, hierarchy_id: str) -> Dict[str, Any]:
        """Get detailed completion status of hierarchy"""
        hierarchy = self.get_exposure_hierarchy(hierarchy_id)
        if not hierarchy:
            return {"error": "Hierarchy not found"}
        
        status = {
            "hierarchy_id": hierarchy_id,
            "target_fear": hierarchy.target_fear,
            "total_levels": len(hierarchy.exposure_items),
            "current_level": hierarchy.current_level,
            "levels_mastered": hierarchy.levels_mastered,
            "mastery_percentage": round(len(hierarchy.levels_mastered) / len(hierarchy.exposure_items) * 100, 1),
            "next_level": min(hierarchy.current_level + 1, 8) if hierarchy.current_level < 8 else None,
            "estimated_sessions_remaining": max(0, hierarchy.estimated_completion_date.days - datetime.now().days) if hierarchy.estimated_completion_date else None,
            "readiness_for_next_level": self._assess_readiness_for_next_level(hierarchy)
        }
        
        return status

    def _assess_readiness_for_next_level(self, hierarchy: ExposureHierarchy) -> Dict[str, Any]:
        """Assess if patient is ready for next hierarchy level"""
        current_level = hierarchy.current_level
        current_item = None
        
        for item in hierarchy.exposure_items:
            if item.difficulty_level == current_level:
                current_item = item
                break
        
        if not current_item:
            return {"ready": False, "reason": "Current level item not found"}
        
        mastery_criteria = hierarchy.mastery_criteria
        required_completions = mastery_criteria.get('successful_completions_required', 2)
        max_end_anxiety = mastery_criteria.get('maximum_end_anxiety', 3)
        
        # Check mastery criteria
        meets_completion_requirement = current_item.successful_completions >= required_completions
        meets_anxiety_requirement = (current_item.average_end_anxiety is None or 
                                    current_item.average_end_anxiety <= max_end_anxiety)
        
        ready = meets_completion_requirement and meets_anxiety_requirement
        
        readiness = {
            "ready": ready,
            "current_level": current_level,
            "successful_completions": current_item.successful_completions,
            "required_completions": required_completions,
            "average_end_anxiety": current_item.average_end_anxiety,
            "max_allowed_end_anxiety": max_end_anxiety,
            "criteria_met": {
                "completion_requirement": meets_completion_requirement,
                "anxiety_requirement": meets_anxiety_requirement
            }
        }
        
        if not ready:
            if not meets_completion_requirement:
                readiness["recommendation"] = f"Need {required_completions - current_item.successful_completions} more successful completions"
            elif not meets_anxiety_requirement:
                readiness["recommendation"] = f"Need to reduce end anxiety to {max_end_anxiety} or below"
        else:
            readiness["recommendation"] = "Ready to progress to next level"
        
        return readiness
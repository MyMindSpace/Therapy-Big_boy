"""
Behavioral Experiments Module

Implements behavioral experiment design and execution for CBT interventions.
Helps patients test negative predictions and beliefs through structured behavioral tests.
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from enum import Enum
from dataclasses import dataclass, asdict
import json

from config.therapy_protocols import TherapyModality, InterventionType


# ============================================================================
# ENUMS AND DATA STRUCTURES
# ============================================================================

class ExperimentType(Enum):
    """Types of behavioral experiments"""
    PREDICTION_TESTING = "prediction_testing"  # Test specific predictions
    HYPOTHESIS_TESTING = "hypothesis_testing"  # Test broader hypotheses
    BEHAVIORAL_ACTIVATION = "behavioral_activation"  # Activity-based experiments
    SOCIAL_EXPERIMENT = "social_experiment"  # Social interaction experiments
    EXPOSURE_EXPERIMENT = "exposure_experiment"  # Gradual exposure experiments
    PROBLEM_SOLVING = "problem_solving"  # Solution-focused experiments
    SAFETY_BEHAVIOR = "safety_behavior"  # Testing safety behaviors
    AVOIDANCE_TESTING = "avoidance_testing"  # Challenging avoidance patterns


class ExperimentStatus(Enum):
    """Status of behavioral experiments"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PARTIALLY_COMPLETED = "partially_completed"
    POSTPONED = "postponed"
    CANCELLED = "cancelled"
    MODIFIED = "modified"


class ConfidenceLevel(Enum):
    """Confidence levels for predictions"""
    VERY_LOW = 1
    LOW = 2
    SOMEWHAT_LOW = 3
    MODERATE = 4
    SOMEWHAT_HIGH = 5
    HIGH = 6
    VERY_HIGH = 7


class OutcomeRating(Enum):
    """Rating scale for experiment outcomes"""
    MUCH_WORSE = 1
    WORSE = 2
    SLIGHTLY_WORSE = 3
    AS_EXPECTED = 4
    SLIGHTLY_BETTER = 5
    BETTER = 6
    MUCH_BETTER = 7


@dataclass
class Prediction:
    """Specific prediction to test in experiment"""
    prediction_id: str
    prediction_text: str
    confidence_level: int  # 1-7 scale
    probability_percentage: int  # 0-100%
    specific_outcomes: List[str]
    evidence_for: List[str]
    evidence_against: List[str]
    
    # Post-experiment
    actual_outcome: Optional[str] = None
    outcome_rating: Optional[int] = None  # 1-7 scale (much worse to much better)
    confidence_after: Optional[int] = None
    learning_points: List[str] = None
    
    def __post_init__(self):
        if self.learning_points is None:
            self.learning_points = []


@dataclass
class SafetyBehavior:
    """Safety behavior to test or eliminate"""
    behavior_id: str
    behavior_description: str
    purpose: str  # Why patient uses this behavior
    frequency: str  # How often they use it
    consequences: List[str]  # What happens when they use it
    
    # Experiment variables
    test_without: bool = False  # Test experiment without this behavior
    reduce_gradually: bool = False  # Gradually reduce the behavior
    
    # Results
    outcome_without: Optional[str] = None
    anxiety_level_with: Optional[int] = None  # 1-10 scale
    anxiety_level_without: Optional[int] = None  # 1-10 scale


@dataclass
class BehavioralExperiment:
    """Comprehensive behavioral experiment structure"""
    experiment_id: str
    patient_id: str
    experiment_type: ExperimentType
    title: str
    description: str
    
    # Problem identification
    target_belief: str
    automatic_thoughts: List[str]
    emotions_before: Dict[str, int]  # emotion: intensity (1-10)
    
    # Experiment design
    predictions: List[Prediction]
    safety_behaviors: List[SafetyBehavior]
    experiment_steps: List[str]
    success_criteria: List[str]
    potential_obstacles: List[str]
    coping_strategies: List[str]
    
    # Logistics
    planned_date: datetime
    estimated_duration: int  # minutes
    location: str
    required_materials: List[str]
    support_needed: str
    
    # Execution tracking
    status: ExperimentStatus
    actual_date: Optional[datetime] = None
    actual_duration: Optional[int] = None
    
    # Results
    emotions_after: Dict[str, int] = None  # emotion: intensity (1-10)
    overall_outcome: Optional[str] = None
    surprises: List[str] = None
    difficulties: List[str] = None
    
    # Learning and integration
    key_learnings: List[str] = None
    belief_change: Optional[str] = None
    confidence_in_belief_before: Optional[int] = None  # 1-10 scale
    confidence_in_belief_after: Optional[int] = None  # 1-10 scale
    next_experiments: List[str] = None
    
    # Metadata
    created_date: datetime
    last_updated: datetime
    therapist_notes: str = ""
    
    def __post_init__(self):
        if self.emotions_after is None:
            self.emotions_after = {}
        if self.surprises is None:
            self.surprises = []
        if self.difficulties is None:
            self.difficulties = []
        if self.key_learnings is None:
            self.key_learnings = []
        if self.next_experiments is None:
            self.next_experiments = []


@dataclass
class ExperimentTemplate:
    """Template for common behavioral experiments"""
    template_id: str
    name: str
    experiment_type: ExperimentType
    description: str
    target_conditions: List[str]  # When to use this template
    common_beliefs: List[str]  # Beliefs this experiment typically tests
    
    # Template structure
    typical_predictions: List[str]
    suggested_steps: List[str]
    common_obstacles: List[str]
    safety_considerations: List[str]
    
    # Customization guidance
    adaptation_notes: str
    difficulty_level: int  # 1-5 scale
    prerequisite_skills: List[str]


# ============================================================================
# MAIN CLASS
# ============================================================================

class BehavioralExperimentDesigner:
    """
    Manages behavioral experiment design, execution, and analysis.
    """
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self._initialize_database()
        self._load_experiment_templates()
    
    # ========================================================================
    # DATABASE INITIALIZATION AND SETUP
    # ========================================================================
    
    def _initialize_database(self):
        """Initialize behavioral experiment tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Behavioral experiments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS behavioral_experiments (
                    experiment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    experiment_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    target_belief TEXT,
                    automatic_thoughts TEXT,
                    emotions_before TEXT,
                    experiment_steps TEXT,
                    success_criteria TEXT,
                    potential_obstacles TEXT,
                    coping_strategies TEXT,
                    planned_date TIMESTAMP,
                    estimated_duration INTEGER,
                    location TEXT,
                    required_materials TEXT,
                    support_needed TEXT,
                    status TEXT NOT NULL,
                    actual_date TIMESTAMP,
                    actual_duration INTEGER,
                    emotions_after TEXT,
                    overall_outcome TEXT,
                    surprises TEXT,
                    difficulties TEXT,
                    key_learnings TEXT,
                    belief_change TEXT,
                    confidence_in_belief_before INTEGER,
                    confidence_in_belief_after INTEGER,
                    next_experiments TEXT,
                    created_date TIMESTAMP,
                    last_updated TIMESTAMP,
                    therapist_notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            # Predictions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiment_predictions (
                    prediction_id TEXT PRIMARY KEY,
                    experiment_id TEXT NOT NULL,
                    prediction_text TEXT NOT NULL,
                    confidence_level INTEGER,
                    probability_percentage INTEGER,
                    specific_outcomes TEXT,
                    evidence_for TEXT,
                    evidence_against TEXT,
                    actual_outcome TEXT,
                    outcome_rating INTEGER,
                    confidence_after INTEGER,
                    learning_points TEXT,
                    FOREIGN KEY (experiment_id) REFERENCES behavioral_experiments (experiment_id)
                )
            """)
            
            # Safety behaviors table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiment_safety_behaviors (
                    behavior_id TEXT PRIMARY KEY,
                    experiment_id TEXT NOT NULL,
                    behavior_description TEXT NOT NULL,
                    purpose TEXT,
                    frequency TEXT,
                    consequences TEXT,
                    test_without BOOLEAN,
                    reduce_gradually BOOLEAN,
                    outcome_without TEXT,
                    anxiety_level_with INTEGER,
                    anxiety_level_without INTEGER,
                    FOREIGN KEY (experiment_id) REFERENCES behavioral_experiments (experiment_id)
                )
            """)
            
            # Experiment templates table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiment_templates (
                    template_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    experiment_type TEXT NOT NULL,
                    description TEXT,
                    target_conditions TEXT,
                    common_beliefs TEXT,
                    typical_predictions TEXT,
                    suggested_steps TEXT,
                    common_obstacles TEXT,
                    safety_considerations TEXT,
                    adaptation_notes TEXT,
                    difficulty_level INTEGER,
                    prerequisite_skills TEXT,
                    is_default BOOLEAN DEFAULT FALSE
                )
            """)
            
            conn.commit()
    
    def _load_experiment_templates(self):
        """Load default experiment templates"""
        # Check if templates already exist
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM experiment_templates WHERE is_default = TRUE")
            count = cursor.fetchone()[0]
            
            if count == 0:  # Load defaults if not already present
                templates = self._create_default_templates()
                for template in templates:
                    self._save_experiment_template(template, is_default=True)
    
    def _create_default_templates(self) -> List[ExperimentTemplate]:
        """Create default experiment templates"""
        templates = [
            ExperimentTemplate(
                template_id="temp_001",
                name="Social Interaction Test",
                experiment_type=ExperimentType.SOCIAL_EXPERIMENT,
                description="Test predictions about social interactions and rejection",
                target_conditions=["Social anxiety", "Fear of rejection", "Low self-esteem"],
                common_beliefs=[
                    "People will reject me if I approach them",
                    "I will embarrass myself in social situations",
                    "Others will judge me negatively"
                ],
                typical_predictions=[
                    "The person will ignore me or walk away",
                    "I will say something stupid and embarrass myself",
                    "People will think I'm weird or boring"
                ],
                suggested_steps=[
                    "Choose a low-stakes social interaction",
                    "Prepare a simple conversation starter",
                    "Approach the person with a genuine smile",
                    "Make the interaction brief and natural",
                    "Observe the actual response without judgment"
                ],
                common_obstacles=[
                    "High anxiety before attempting",
                    "Avoiding the experiment altogether",
                    "Catastrophizing minor negative responses"
                ],
                safety_considerations=[
                    "Start with very low-risk interactions",
                    "Have coping strategies ready for anxiety",
                    "Debrief with therapist afterwards"
                ],
                adaptation_notes="Adjust difficulty based on patient's current social anxiety level",
                difficulty_level=3,
                prerequisite_skills=["Basic anxiety management", "Thought challenging"]
            ),
            
            ExperimentTemplate(
                template_id="temp_002",
                name="Performance Anxiety Test",
                experiment_type=ExperimentType.PREDICTION_TESTING,
                description="Test catastrophic predictions about performance situations",
                target_conditions=["Performance anxiety", "Perfectionism", "Fear of failure"],
                common_beliefs=[
                    "I must perform perfectly or it's a failure",
                    "People will notice my mistakes and judge me",
                    "Making a mistake will be catastrophic"
                ],
                typical_predictions=[
                    "I will make obvious mistakes that everyone notices",
                    "My anxiety will be visible and embarrassing",
                    "The outcome will be terrible if I'm not perfect"
                ],
                suggested_steps=[
                    "Choose a performance situation with manageable stakes",
                    "Deliberately make a small, intentional mistake",
                    "Continue with the performance normally",
                    "Observe others' reactions and your own feelings",
                    "Note any positive or neutral outcomes"
                ],
                common_obstacles=[
                    "Resistance to making intentional mistakes",
                    "Overwhelming anxiety before performing",
                    "Minimizing positive outcomes"
                ],
                safety_considerations=[
                    "Start with very minor mistakes",
                    "Ensure support system is available",
                    "Practice relaxation techniques beforehand"
                ],
                adaptation_notes="Scale difficulty based on patient's perfectionism level",
                difficulty_level=4,
                prerequisite_skills=["Relaxation techniques", "Cognitive restructuring"]
            ),
            
            ExperimentTemplate(
                template_id="temp_003",
                name="Activity Avoidance Challenge",
                experiment_type=ExperimentType.AVOIDANCE_TESTING,
                description="Test predictions about avoided activities",
                target_conditions=["Depression", "Agoraphobia", "Generalized anxiety"],
                common_beliefs=[
                    "I won't enjoy anything anymore",
                    "I can't handle being out in public",
                    "Something bad will happen if I do this activity"
                ],
                typical_predictions=[
                    "I will feel overwhelmed and need to escape",
                    "The activity will be boring or unpleasant",
                    "I will have a panic attack or lose control"
                ],
                suggested_steps=[
                    "Choose a previously enjoyable but now avoided activity",
                    "Start with a shorter or easier version",
                    "Focus on the experience rather than performance",
                    "Rate mood and anxiety before, during, and after",
                    "Note any positive aspects or surprises"
                ],
                common_obstacles=[
                    "Last-minute cancellation due to anxiety",
                    "Focusing only on negative aspects",
                    "Comparing to past experiences"
                ],
                safety_considerations=[
                    "Have an exit strategy if needed",
                    "Start with activities close to home",
                    "Bring supportive person if helpful"
                ],
                adaptation_notes="Adjust activity difficulty based on current functioning level",
                difficulty_level=2,
                prerequisite_skills=["Basic mood monitoring", "Grounding techniques"]
            ),
            
            ExperimentTemplate(
                template_id="temp_004",
                name="Safety Behavior Drop Test",
                experiment_type=ExperimentType.SAFETY_BEHAVIOR,
                description="Test what happens when dropping safety behaviors",
                target_conditions=["Panic disorder", "Social anxiety", "OCD"],
                common_beliefs=[
                    "I need my safety behaviors to cope",
                    "Something terrible will happen without them",
                    "I can't handle anxiety without these behaviors"
                ],
                typical_predictions=[
                    "My anxiety will become unbearable",
                    "I will lose control or have a panic attack",
                    "The feared outcome will definitely happen"
                ],
                suggested_steps=[
                    "Identify specific safety behavior to test",
                    "Start by reducing the behavior rather than eliminating",
                    "Monitor anxiety levels throughout",
                    "Stay in situation without the safety behavior",
                    "Note actual outcomes vs. predicted outcomes"
                ],
                common_obstacles=[
                    "Strong urge to use safety behavior",
                    "Intense initial anxiety",
                    "Attributing success to luck rather than evidence"
                ],
                safety_considerations=[
                    "Ensure patient has alternative coping skills",
                    "Start with less threatening situations",
                    "Have support available during experiment"
                ],
                adaptation_notes="Critical to build alternative coping skills first",
                difficulty_level=5,
                prerequisite_skills=["Anxiety tolerance", "Alternative coping strategies"]
            )
        ]
        
        return templates
    
    def _save_experiment_template(self, template: ExperimentTemplate, is_default: bool = False):
        """Save experiment template to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO experiment_templates (
                    template_id, name, experiment_type, description,
                    target_conditions, common_beliefs, typical_predictions,
                    suggested_steps, common_obstacles, safety_considerations,
                    adaptation_notes, difficulty_level, prerequisite_skills, is_default
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                template.template_id, template.name, template.experiment_type.value,
                template.description, json.dumps(template.target_conditions),
                json.dumps(template.common_beliefs), json.dumps(template.typical_predictions),
                json.dumps(template.suggested_steps), json.dumps(template.common_obstacles),
                json.dumps(template.safety_considerations), template.adaptation_notes,
                template.difficulty_level, json.dumps(template.prerequisite_skills), is_default
            ))
            conn.commit()
    
    # ========================================================================
    # EXPERIMENT DESIGN AND CREATION
    # ========================================================================
    
    def get_experiment_suggestions(
        self, 
        patient_id: str,
        target_beliefs: List[str],
        current_symptoms: List[str],
        difficulty_preference: int = 3
    ) -> List[ExperimentTemplate]:
        """Get personalized experiment suggestions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM experiment_templates 
                WHERE difficulty_level <= ?
                ORDER BY difficulty_level, name
            """, (difficulty_preference,))
            
            template_data = cursor.fetchall()
            
            suggestions = []
            for row in template_data:
                template = self._reconstruct_template_from_row(row)
                
                # Check relevance to patient's symptoms and beliefs
                relevance_score = self._calculate_template_relevance(
                    template, current_symptoms, target_beliefs
                )
                
                if relevance_score > 0:
                    suggestions.append(template)
            
            # Sort by relevance
            suggestions.sort(key=lambda x: self._calculate_template_relevance(
                x, current_symptoms, target_beliefs
            ), reverse=True)
            
            return suggestions[:5]  # Return top 5 most relevant
    
    def _calculate_template_relevance(
        self, 
        template: ExperimentTemplate, 
        symptoms: List[str], 
        beliefs: List[str]
    ) -> int:
        """Calculate relevance score for template"""
        relevance_score = 0
        
        # Check target conditions match
        for condition in template.target_conditions:
            if any(symptom.lower() in condition.lower() for symptom in symptoms):
                relevance_score += 2
        
        # Check belief match
        for belief in template.common_beliefs:
            if any(target.lower() in belief.lower() for target in beliefs):
                relevance_score += 3
        
        return relevance_score
    
    def design_experiment(
        self,
        patient_id: str,
        template_id: str = None,
        custom_design: Dict[str, Any] = None
    ) -> BehavioralExperiment:
        """Design a new behavioral experiment"""
        experiment_id = f"exp_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if template_id:
            return self._create_experiment_from_template(experiment_id, patient_id, template_id)
        elif custom_design:
            return self._create_custom_experiment(experiment_id, patient_id, custom_design)
        else:
            raise ValueError("Either template_id or custom_design must be provided")
    
    def _create_experiment_from_template(
        self, 
        experiment_id: str, 
        patient_id: str, 
        template_id: str
    ) -> BehavioralExperiment:
        """Create experiment from template"""
        template = self._get_template_by_id(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        return BehavioralExperiment(
            experiment_id=experiment_id,
            patient_id=patient_id,
            experiment_type=template.experiment_type,
            title=f"Custom: {template.name}",
            description=template.description,
            target_belief="",  # To be filled in during session
            automatic_thoughts=[],
            emotions_before={},
            predictions=[],
            safety_behaviors=[],
            experiment_steps=template.suggested_steps.copy(),
            success_criteria=[],
            potential_obstacles=template.common_obstacles.copy(),
            coping_strategies=[],
            planned_date=datetime.now() + timedelta(days=7),
            estimated_duration=60,
            location="",
            required_materials=[],
            support_needed="",
            status=ExperimentStatus.PLANNED,
            created_date=datetime.now(),
            last_updated=datetime.now()
        )
    
    def _create_custom_experiment(
        self, 
        experiment_id: str, 
        patient_id: str, 
        custom_design: Dict[str, Any]
    ) -> BehavioralExperiment:
        """Create completely custom experiment"""
        return BehavioralExperiment(
            experiment_id=experiment_id,
            patient_id=patient_id,
            experiment_type=ExperimentType(custom_design.get('experiment_type', 'prediction_testing')),
            title=custom_design.get('title', 'Custom Experiment'),
            description=custom_design.get('description', ''),
            target_belief=custom_design.get('target_belief', ''),
            automatic_thoughts=custom_design.get('automatic_thoughts', []),
            emotions_before=custom_design.get('emotions_before', {}),
            predictions=[],
            safety_behaviors=[],
            experiment_steps=custom_design.get('experiment_steps', []),
            success_criteria=custom_design.get('success_criteria', []),
            potential_obstacles=custom_design.get('potential_obstacles', []),
            coping_strategies=custom_design.get('coping_strategies', []),
            planned_date=datetime.fromisoformat(custom_design.get('planned_date')) 
                         if custom_design.get('planned_date') 
                         else datetime.now() + timedelta(days=7),
            estimated_duration=custom_design.get('estimated_duration', 60),
            location=custom_design.get('location', ''),
            required_materials=custom_design.get('required_materials', []),
            support_needed=custom_design.get('support_needed', ''),
            status=ExperimentStatus.PLANNED,
            created_date=datetime.now(),
            last_updated=datetime.now()
        )
    
    # ========================================================================
    # PREDICTION AND SAFETY BEHAVIOR MANAGEMENT
    # ========================================================================
    
    def add_prediction_to_experiment(
        self,
        experiment_id: str,
        prediction_text: str,
        confidence_level: int,
        probability_percentage: int,
        specific_outcomes: List[str] = None,
        evidence_for: List[str] = None,
        evidence_against: List[str] = None
    ) -> Prediction:
        """Add a prediction to an existing experiment"""
        prediction_id = f"pred_{experiment_id}_{datetime.now().strftime('%H%M%S')}"
        
        return Prediction(
            prediction_id=prediction_id,
            prediction_text=prediction_text,
            confidence_level=confidence_level,
            probability_percentage=probability_percentage,
            specific_outcomes=specific_outcomes or [],
            evidence_for=evidence_for or [],
            evidence_against=evidence_against or []
        )
    
    def add_safety_behavior_to_experiment(
        self,
        experiment_id: str,
        behavior_description: str,
        purpose: str,
        frequency: str,
        consequences: List[str] = None,
        test_without: bool = True
    ) -> SafetyBehavior:
        """Add a safety behavior to test in the experiment"""
        behavior_id = f"safe_{experiment_id}_{datetime.now().strftime('%H%M%S')}"
        
        return SafetyBehavior(
            behavior_id=behavior_id,
            behavior_description=behavior_description,
            purpose=purpose,
            frequency=frequency,
            consequences=consequences or [],
            test_without=test_without
        )
    
    # ========================================================================
    # EXPERIMENT PERSISTENCE (SAVE/LOAD)
    # ========================================================================
    
    def save_experiment(self, experiment: BehavioralExperiment):
        """Save behavioral experiment to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Save main experiment
            cursor.execute("""
                INSERT OR REPLACE INTO behavioral_experiments (
                    experiment_id, patient_id, experiment_type, title, description,
                    target_belief, automatic_thoughts, emotions_before, experiment_steps,
                    success_criteria, potential_obstacles, coping_strategies, planned_date,
                    estimated_duration, location, required_materials, support_needed,
                    status, actual_date, actual_duration, emotions_after, overall_outcome,
                    surprises, difficulties, key_learnings, belief_change,
                    confidence_in_belief_before, confidence_in_belief_after,
                    next_experiments, created_date, last_updated, therapist_notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                experiment.experiment_id, experiment.patient_id, experiment.experiment_type.value,
                experiment.title, experiment.description, experiment.target_belief,
                json.dumps(experiment.automatic_thoughts), json.dumps(experiment.emotions_before),
                json.dumps(experiment.experiment_steps), json.dumps(experiment.success_criteria),
                json.dumps(experiment.potential_obstacles), json.dumps(experiment.coping_strategies),
                experiment.planned_date, experiment.estimated_duration, experiment.location,
                json.dumps(experiment.required_materials), experiment.support_needed,
                experiment.status.value, experiment.actual_date, experiment.actual_duration,
                json.dumps(experiment.emotions_after), experiment.overall_outcome,
                json.dumps(experiment.surprises), json.dumps(experiment.difficulties),
                json.dumps(experiment.key_learnings), experiment.belief_change,
                experiment.confidence_in_belief_before, experiment.confidence_in_belief_after,
                json.dumps(experiment.next_experiments), experiment.created_date,
                experiment.last_updated, experiment.therapist_notes
            ))
            
            # Save predictions
            self._save_experiment_predictions(cursor, experiment)
            
            # Save safety behaviors
            self._save_experiment_safety_behaviors(cursor, experiment)
            
            conn.commit()
    
    def _save_experiment_predictions(self, cursor, experiment: BehavioralExperiment):
        """Save experiment predictions to database"""
        for prediction in experiment.predictions:
            cursor.execute("""
                INSERT OR REPLACE INTO experiment_predictions (
                    prediction_id, experiment_id, prediction_text, confidence_level,
                    probability_percentage, specific_outcomes, evidence_for,
                    evidence_against, actual_outcome, outcome_rating,
                    confidence_after, learning_points
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                prediction.prediction_id, experiment.experiment_id, prediction.prediction_text,
                prediction.confidence_level, prediction.probability_percentage,
                json.dumps(prediction.specific_outcomes), json.dumps(prediction.evidence_for),
                json.dumps(prediction.evidence_against), prediction.actual_outcome,
                prediction.outcome_rating, prediction.confidence_after,
                json.dumps(prediction.learning_points)
            ))
    
    def _save_experiment_safety_behaviors(self, cursor, experiment: BehavioralExperiment):
        """Save experiment safety behaviors to database"""
        for behavior in experiment.safety_behaviors:
            cursor.execute("""
                INSERT OR REPLACE INTO experiment_safety_behaviors (
                    behavior_id, experiment_id, behavior_description, purpose,
                    frequency, consequences, test_without, reduce_gradually,
                    outcome_without, anxiety_level_with, anxiety_level_without
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                behavior.behavior_id, experiment.experiment_id, behavior.behavior_description,
                behavior.purpose, behavior.frequency, json.dumps(behavior.consequences),
                behavior.test_without, behavior.reduce_gradually, behavior.outcome_without,
                behavior.anxiety_level_with, behavior.anxiety_level_without
            ))
    
    def get_experiment(self, experiment_id: str) -> Optional[BehavioralExperiment]:
        """Retrieve behavioral experiment by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get main experiment
            cursor.execute("SELECT * FROM behavioral_experiments WHERE experiment_id = ?", 
                         (experiment_id,))
            exp_data = cursor.fetchone()
            if not exp_data:
                return None
            
            # Get predictions
            cursor.execute("SELECT * FROM experiment_predictions WHERE experiment_id = ?", 
                         (experiment_id,))
            pred_data = cursor.fetchall()
            
            # Get safety behaviors
            cursor.execute("SELECT * FROM experiment_safety_behaviors WHERE experiment_id = ?", 
                         (experiment_id,))
            safety_data = cursor.fetchall()
            
            return self._reconstruct_experiment(exp_data, pred_data, safety_data)
    
    def get_patient_experiments(
        self, 
        patient_id: str,
        status_filter: ExperimentStatus = None,
        limit: int = None
    ) -> List[BehavioralExperiment]:
        """Get all experiments for a patient"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = "SELECT experiment_id FROM behavioral_experiments WHERE patient_id = ?"
            params = [patient_id]
            
            if status_filter:
                query += " AND status = ?"
                params.append(status_filter.value)
            
            query += " ORDER BY created_date DESC"
            
            if limit:
                query += f" LIMIT {limit}"
            
            cursor
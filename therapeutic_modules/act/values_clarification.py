from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import sqlite3
import json
import uuid
from datetime import datetime


class ValuesArea(Enum):
    FAMILY_RELATIONSHIPS = "family_relationships"
    INTIMATE_RELATIONSHIPS = "intimate_relationships"
    FRIENDSHIPS = "friendships"
    CAREER_WORK = "career_work"
    EDUCATION_LEARNING = "education_learning"
    RECREATION_FUN = "recreation_fun"
    SPIRITUALITY = "spirituality"
    COMMUNITY_CITIZENSHIP = "community_citizenship"
    HEALTH_PHYSICAL_CARE = "health_physical_care"
    PARENTING = "parenting"
    ENVIRONMENT_NATURE = "environment_nature"
    PERSONAL_GROWTH = "personal_growth"


class ValuesExerciseType(Enum):
    CARD_SORT = "card_sort"
    LIFE_DOMAINS_EXPLORATION = "life_domains_exploration"
    FUNERAL_EXERCISE = "funeral_exercise"
    BIRTHDAY_AT_80 = "birthday_at_80"
    VALUES_RANKING = "values_ranking"
    BULL_EYE_ASSESSMENT = "bull_eye_assessment"
    WORKABILITY_ASSESSMENT = "workability_assessment"
    VALUES_GOALS_DISTINCTION = "values_goals_distinction"
    OBSTACLE_EXPLORATION = "obstacle_exploration"
    COMMITTED_ACTION_PLANNING = "committed_action_planning"


class ValuesPriority(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    INACTIVE = "inactive"


class ValuesAlignment(Enum):
    HIGHLY_ALIGNED = "highly_aligned"
    MODERATELY_ALIGNED = "moderately_aligned"
    SOMEWHAT_ALIGNED = "somewhat_aligned"
    POORLY_ALIGNED = "poorly_aligned"
    NOT_ALIGNED = "not_aligned"


@dataclass
class PersonalValue:
    value_id: str
    value_name: str
    values_area: ValuesArea
    personal_definition: str
    priority_level: ValuesPriority
    importance_rating: int
    current_alignment: ValuesAlignment
    alignment_rating: int
    specific_behaviors: List[str]
    obstacles: List[str]
    growth_opportunities: List[str]
    cultural_influences: List[str]
    motivational_strength: int


@dataclass
class ValuesExercise:
    exercise_id: str
    exercise_type: ValuesExerciseType
    name: str
    description: str
    instructions: List[str]
    estimated_duration: int
    materials_needed: List[str]
    experiential_components: List[str]
    metaphors_used: List[str]
    processing_questions: List[str]
    follow_up_actions: List[str]
    therapeutic_goals: List[str]


@dataclass
class ValuesSession:
    session_id: str
    patient_id: str
    exercise_used: ValuesExerciseType
    values_explored: List[str]
    new_values_identified: List[str]
    priority_changes: Dict[str, str]
    insights_gained: List[str]
    emotional_responses: List[str]
    barriers_identified: List[str]
    action_commitments: List[str]
    homework_assigned: List[str]
    therapist_observations: str
    patient_feedback: str
    session_date: datetime = field(default_factory=datetime.now)


@dataclass
class ValuesAssessment:
    assessment_id: str
    patient_id: str
    assessment_date: datetime
    primary_values: List[PersonalValue]
    values_clarity_level: int
    values_commitment_level: int
    values_behavior_alignment: float
    major_discrepancies: List[str]
    strengths_identified: List[str]
    growth_areas: List[str]
    cultural_considerations: List[str]
    recommended_exercises: List[ValuesExerciseType]
    action_plan_items: List[str]


class ACTValuesClarificationModule:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.values_exercises = self._initialize_values_exercises()
        self.metaphor_library = self._initialize_metaphor_library()
        self.assessment_tools = self._initialize_assessment_tools()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS personal_values (
                    value_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    value_name TEXT NOT NULL,
                    values_area TEXT NOT NULL,
                    personal_definition TEXT,
                    priority_level TEXT,
                    importance_rating INTEGER,
                    current_alignment TEXT,
                    alignment_rating INTEGER,
                    specific_behaviors TEXT,
                    obstacles TEXT,
                    growth_opportunities TEXT,
                    cultural_influences TEXT,
                    motivational_strength INTEGER,
                    created_date TEXT,
                    last_updated TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS values_sessions (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    exercise_used TEXT NOT NULL,
                    values_explored TEXT,
                    new_values_identified TEXT,
                    priority_changes TEXT,
                    insights_gained TEXT,
                    emotional_responses TEXT,
                    barriers_identified TEXT,
                    action_commitments TEXT,
                    homework_assigned TEXT,
                    therapist_observations TEXT,
                    patient_feedback TEXT,
                    session_date TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS values_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    assessment_date TEXT,
                    values_clarity_level INTEGER,
                    values_commitment_level INTEGER,
                    values_behavior_alignment REAL,
                    major_discrepancies TEXT,
                    strengths_identified TEXT,
                    growth_areas TEXT,
                    cultural_considerations TEXT,
                    recommended_exercises TEXT,
                    action_plan_items TEXT
                )
            """)
    
    def _initialize_values_exercises(self) -> Dict[ValuesExerciseType, ValuesExercise]:
        exercises = {}
        
        exercises[ValuesExerciseType.CARD_SORT] = ValuesExercise(
            exercise_id="values_card_sort",
            exercise_type=ValuesExerciseType.CARD_SORT,
            name="Values Card Sort",
            description="Interactive sorting of values cards to identify core personal values",
            instructions=[
                "Present patient with comprehensive set of values cards",
                "Have them sort into 'Very Important', 'Somewhat Important', 'Not Important' piles",
                "From 'Very Important' pile, select top 5-7 core values",
                "Rank these core values in order of importance",
                "Discuss personal meaning of each selected value",
                "Explore how each value shows up in daily life"
            ],
            estimated_duration=30,
            materials_needed=["Values card deck", "Three sorting containers", "Ranking worksheet"],
            experiential_components=[
                "Physical sorting and handling of cards",
                "Intuitive decision-making process",
                "Felt sense of values resonance"
            ],
            metaphors_used=["Compass for life direction", "North star for navigation"],
            processing_questions=[
                "What surprised you about your selections?",
                "How do these values show up in your daily life?",
                "Which values feel most alive for you right now?",
                "Where do you notice gaps between values and behavior?"
            ],
            follow_up_actions=[
                "Complete bull's-eye assessment for top values",
                "Identify one small action for each core value",
                "Notice values-behavior alignment in daily life"
            ],
            therapeutic_goals=[
                "Identify authentic core values",
                "Distinguish personal from inherited values",
                "Create foundation for committed action"
            ]
        )
        
        exercises[ValuesExerciseType.FUNERAL_EXERCISE] = ValuesExercise(
            exercise_id="funeral_exercise",
            exercise_type=ValuesExerciseType.FUNERAL_EXERCISE,
            name="Funeral Visualization",
            description="Guided visualization of own funeral to clarify life values and legacy",
            instructions=[
                "Guide patient through relaxation and centering",
                "Have them imagine their own funeral service",
                "Visualize different speakers: family, friends, colleagues",
                "What would they want each person to say about how they lived?",
                "What values would be evident in these eulogies?",
                "What legacy would reflect their deepest values?",
                "Process emotional responses and insights"
            ],
            estimated_duration=25,
            materials_needed=["Guided script", "Comfortable seating", "Tissues"],
            experiential_components=[
                "Guided visualization",
                "Emotional evocation",
                "Legacy perspective-taking"
            ],
            metaphors_used=["Life as a story being written", "Legacy as seeds planted"],
            processing_questions=[
                "What emotions came up during this exercise?",
                "What values emerged as most important?",
                "How does your current life align with this vision?",
                "What changes would honor these values more fully?"
            ],
            follow_up_actions=[
                "Write brief eulogy reflecting identified values",
                "Share insights with trusted person",
                "Commit to one values-based change"
            ],
            therapeutic_goals=[
                "Connect with mortality salience",
                "Clarify authentic life directions",
                "Motivate values-based living"
            ]
        )
        
        exercises[ValuesExerciseType.BULL_EYE_ASSESSMENT] = ValuesExercise(
            exercise_id="bull_eye_assessment",
            exercise_type=ValuesExerciseType.BULL_EYE_ASSESSMENT,
            name="Bull's-Eye Living Assessment",
            description="Visual assessment of current values-behavior alignment",
            instructions=[
                "Present bull's-eye diagram for each life domain",
                "Center represents perfect values alignment",
                "Outer rings represent increasing distance from values",
                "Have patient mark current position in each domain",
                "Discuss discrepancies and patterns",
                "Identify domains needing attention",
                "Plan specific actions to move toward center"
            ],
            estimated_duration=20,
            materials_needed=["Bull's-eye worksheets", "Colored pens", "Domain descriptions"],
            experiential_components=[
                "Visual self-assessment",
                "Spatial representation of alignment",
                "Pattern recognition across domains"
            ],
            metaphors_used=["Target practice for values", "Map of current location"],
            processing_questions=[
                "Which domains show good alignment?",
                "Where are the biggest gaps?",
                "What patterns do you notice?",
                "What would it take to move closer to the center?"
            ],
            follow_up_actions=[
                "Choose one domain for focused attention",
                "Identify specific behaviors to change",
                "Schedule regular bull's-eye check-ins"
            ],
            therapeutic_goals=[
                "Assess current values-behavior alignment",
                "Identify specific change targets",
                "Create visual progress tracking tool"
            ]
        )
        
        exercises[ValuesExerciseType.WORKABILITY_ASSESSMENT] = ValuesExercise(
            exercise_id="workability_assessment",
            exercise_type=ValuesExerciseType.WORKABILITY_ASSESSMENT,
            name="Values Workability Assessment",
            description="Examine how well current patterns serve identified values",
            instructions=[
                "Review previously identified core values",
                "For each value, assess current behavioral patterns",
                "Ask: 'How well is this pattern serving this value?'",
                "Identify patterns that support vs. undermine values",
                "Explore costs and benefits of current approaches",
                "Brainstorm alternative patterns that better serve values",
                "Commit to experimenting with new approaches"
            ],
            estimated_duration=35,
            materials_needed=["Workability worksheet", "Values list", "Pattern tracking forms"],
            experiential_components=[
                "Honest self-assessment",
                "Cost-benefit analysis",
                "Creative problem-solving"
            ],
            metaphors_used=["Tools that work vs. don't work", "Map leading toward vs. away from destination"],
            processing_questions=[
                "Which patterns clearly serve your values?",
                "Which patterns take you away from what matters?",
                "What's the cost of continuing ineffective patterns?",
                "What new approaches might you experiment with?"
            ],
            follow_up_actions=[
                "Implement one new values-serving pattern",
                "Track workability of daily choices",
                "Regular workability check-ins"
            ],
            therapeutic_goals=[
                "Assess behavioral workability",
                "Link values to daily choices",
                "Motivate behavioral change"
            ]
        )
        
        return exercises
    
    def _initialize_metaphor_library(self) -> Dict[str, Dict[str, Any]]:
        return {
            "compass_metaphor": {
                "description": "Values as internal compass providing direction",
                "script": "Imagine your values as a compass. Just like a compass always points north, your values always point toward what matters most to you. Sometimes we get lost in the fog of daily life, but we can always check our values compass to find our direction again.",
                "applications": ["Direction-setting", "Decision-making", "Recovery from setbacks"],
                "processing_questions": [
                    "What direction is your values compass pointing?",
                    "When do you feel most oriented by your internal compass?",
                    "What pulls you away from following your compass?"
                ]
            },
            
            "garden_metaphor": {
                "description": "Values as seeds requiring cultivation and care",
                "script": "Think of your values like seeds in a garden. Seeds have the potential to grow into beautiful plants, but they need the right conditions - water, sunlight, good soil, and regular tending. Your values are similar - they need daily actions, attention, and care to flourish in your life.",
                "applications": ["Daily values cultivation", "Patience with growth", "Consistent action"],
                "processing_questions": [
                    "Which values-seeds are you tending well?",
                    "Which need more attention and care?",
                    "What would help your values garden flourish?"
                ]
            },
            
            "mountain_metaphor": {
                "description": "Values as chosen mountain to climb",
                "script": "Your values are like choosing which mountain to climb. The mountain represents what matters most to you. Some days the climbing is easy, some days it's difficult, but you keep moving toward the summit because that's the mountain you chose. Values aren't the summit - they're the chosen direction of climb.",
                "applications": ["Persistence through difficulty", "Long-term commitment", "Process focus"],
                "processing_questions": [
                    "Which mountain have you chosen to climb?",
                    "What keeps you climbing when it gets difficult?",
                    "How do you want to climb your mountain?"
                ]
            }
        }
    
    def _initialize_assessment_tools(self) -> Dict[str, Dict[str, Any]]:
        return {
            "values_clarity_scale": {
                "name": "Values Clarity Assessment",
                "items": [
                    "I have a clear sense of what values are most important to me",
                    "I can easily identify my top 3-5 core values",
                    "I understand how my values differ from my goals",
                    "I know what each of my values means to me personally",
                    "I can explain my values to others in my own words"
                ],
                "scoring": "5-point Likert scale (1=Strongly Disagree, 5=Strongly Agree)",
                "interpretation": {
                    "high": "20-25: Clear values awareness",
                    "moderate": "15-19: Developing values clarity", 
                    "low": "5-14: Values exploration needed"
                }
            },
            
            "values_commitment_scale": {
                "name": "Values Commitment Assessment",
                "items": [
                    "I am committed to living according to my values",
                    "I make decisions based on my values rather than convenience",
                    "I persist in values-based actions even when difficult",
                    "I regularly check whether my actions align with my values",
                    "I am willing to experience discomfort to live my values"
                ],
                "scoring": "5-point Likert scale (1=Strongly Disagree, 5=Strongly Agree)",
                "interpretation": {
                    "high": "20-25: Strong values commitment",
                    "moderate": "15-19: Developing commitment",
                    "low": "5-14: Commitment building needed"
                }
            }
        }
    
    def conduct_values_exploration(self, patient_id: str, exercise_type: ValuesExerciseType, 
                                 session_notes: str = "") -> ValuesSession:
        session_id = str(uuid.uuid4())
        exercise = self.values_exercises[exercise_type]
        
        values_session = ValuesSession(
            session_id=session_id,
            patient_id=patient_id,
            exercise_used=exercise_type,
            values_explored=[],
            new_values_identified=[],
            priority_changes={},
            insights_gained=[],
            emotional_responses=[],
            barriers_identified=[],
            action_commitments=[],
            homework_assigned=[],
            therapist_observations=session_notes,
            patient_feedback=""
        )
        
        self._save_values_session(values_session)
        return values_session
    
    def assess_values_clarity(self, patient_id: str) -> ValuesAssessment:
        assessment_id = str(uuid.uuid4())
        current_values = self._get_patient_values(patient_id)
        
        assessment = ValuesAssessment(
            assessment_id=assessment_id,
            patient_id=patient_id,
            assessment_date=datetime.now(),
            primary_values=current_values,
            values_clarity_level=0,
            values_commitment_level=0,
            values_behavior_alignment=0.0,
            major_discrepancies=[],
            strengths_identified=[],
            growth_areas=[],
            cultural_considerations=[],
            recommended_exercises=[],
            action_plan_items=[]
        )
        
        self._save_values_assessment(assessment)
        return assessment
    
    def create_personal_value(self, patient_id: str, value_name: str, values_area: ValuesArea,
                            personal_definition: str, importance_rating: int) -> PersonalValue:
        value_id = str(uuid.uuid4())
        
        personal_value = PersonalValue(
            value_id=value_id,
            value_name=value_name,
            values_area=values_area,
            personal_definition=personal_definition,
            priority_level=ValuesPriority.SECONDARY,
            importance_rating=importance_rating,
            current_alignment=ValuesAlignment.MODERATELY_ALIGNED,
            alignment_rating=5,
            specific_behaviors=[],
            obstacles=[],
            growth_opportunities=[],
            cultural_influences=[],
            motivational_strength=importance_rating
        )
        
        self._save_personal_value(personal_value, patient_id)
        return personal_value
    
    def update_values_alignment(self, patient_id: str, value_id: str, 
                              new_alignment: ValuesAlignment, alignment_rating: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE personal_values 
                SET current_alignment = ?, alignment_rating = ?, last_updated = ?
                WHERE patient_id = ? AND value_id = ?
            """, (new_alignment.value, alignment_rating, datetime.now().isoformat(), patient_id, value_id))
            return cursor.rowcount > 0
    
    def get_values_exercises_for_patient(self, patient_id: str) -> List[ValuesExercise]:
        assessment = self._get_latest_assessment(patient_id)
        if assessment:
            return [self.values_exercises[ex_type] for ex_type in assessment.recommended_exercises]
        return list(self.values_exercises.values())
    
    def get_metaphor_for_context(self, context: str) -> Dict[str, Any]:
        metaphor_mapping = {
            "direction": "compass_metaphor",
            "growth": "garden_metaphor", 
            "persistence": "mountain_metaphor"
        }
        metaphor_key = metaphor_mapping.get(context, "compass_metaphor")
        return self.metaphor_library[metaphor_key]
    
    def generate_values_homework(self, patient_id: str, focus_area: ValuesArea) -> List[str]:
        homework_assignments = [
            f"Daily values check-in: Each evening, rate how well you lived your {focus_area.value.replace('_', ' ')} value today (1-10 scale)",
            f"Values moment noticing: Identify 3 moments this week when you felt most connected to your {focus_area.value.replace('_', ' ')} value",
            f"Small steps practice: Take one small action daily that honors your {focus_area.value.replace('_', ' ')} value",
            f"Obstacle awareness: Notice and write down what gets in the way of living this value",
            f"Values intention setting: Each morning, set an intention for how you'll honor this value that day"
        ]
        return homework_assignments[:3]
    
    def _save_personal_value(self, value: PersonalValue, patient_id: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO personal_values (
                    value_id, patient_id, value_name, values_area, personal_definition,
                    priority_level, importance_rating, current_alignment, alignment_rating,
                    specific_behaviors, obstacles, growth_opportunities, cultural_influences,
                    motivational_strength, created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                value.value_id, patient_id, value.value_name, value.values_area.value,
                value.personal_definition, value.priority_level.value, value.importance_rating,
                value.current_alignment.value, value.alignment_rating,
                json.dumps(value.specific_behaviors), json.dumps(value.obstacles),
                json.dumps(value.growth_opportunities), json.dumps(value.cultural_influences),
                value.motivational_strength, datetime.now().isoformat(), datetime.now().isoformat()
            ))
    
    def _save_values_session(self, session: ValuesSession):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO values_sessions (
                    session_id, patient_id, exercise_used, values_explored, new_values_identified,
                    priority_changes, insights_gained, emotional_responses, barriers_identified,
                    action_commitments, homework_assigned, therapist_observations, patient_feedback, session_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id, session.patient_id, session.exercise_used.value,
                json.dumps(session.values_explored), json.dumps(session.new_values_identified),
                json.dumps(session.priority_changes), json.dumps(session.insights_gained),
                json.dumps(session.emotional_responses), json.dumps(session.barriers_identified),
                json.dumps(session.action_commitments), json.dumps(session.homework_assigned),
                session.therapist_observations, session.patient_feedback, session.session_date.isoformat()
            ))
    
    def _save_values_assessment(self, assessment: ValuesAssessment):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO values_assessments (
                    assessment_id, patient_id, assessment_date, values_clarity_level,
                    values_commitment_level, values_behavior_alignment, major_discrepancies,
                    strengths_identified, growth_areas, cultural_considerations,
                    recommended_exercises, action_plan_items
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id, assessment.patient_id, assessment.assessment_date.isoformat(),
                assessment.values_clarity_level, assessment.values_commitment_level,
                assessment.values_behavior_alignment, json.dumps(assessment.major_discrepancies),
                json.dumps(assessment.strengths_identified), json.dumps(assessment.growth_areas),
                json.dumps(assessment.cultural_considerations), 
                json.dumps([ex.value for ex in assessment.recommended_exercises]),
                json.dumps(assessment.action_plan_items)
            ))
    
    def _get_patient_values(self, patient_id: str) -> List[PersonalValue]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM personal_values WHERE patient_id = ?
                ORDER BY importance_rating DESC
            """, (patient_id,))
            rows = cursor.fetchall()
            
            values = []
            for row in rows:
                value = PersonalValue(
                    value_id=row[0],
                    value_name=row[2],
                    values_area=ValuesArea(row[3]),
                    personal_definition=row[4],
                    priority_level=ValuesPriority(row[5]),
                    importance_rating=row[6],
                    current_alignment=ValuesAlignment(row[7]),
                    alignment_rating=row[8],
                    specific_behaviors=json.loads(row[9]) if row[9] else [],
                    obstacles=json.loads(row[10]) if row[10] else [],
                    growth_opportunities=json.loads(row[11]) if row[11] else [],
                    cultural_influences=json.loads(row[12]) if row[12] else [],
                    motivational_strength=row[13]
                )
                values.append(value)
            return values
    
    def _get_latest_assessment(self, patient_id: str) -> Optional[ValuesAssessment]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM values_assessments 
                WHERE patient_id = ? 
                ORDER BY assessment_date DESC 
                LIMIT 1
            """, (patient_id,))
            row = cursor.fetchone()
            
            if row:
                return ValuesAssessment(
                    assessment_id=row[0],
                    patient_id=row[1],
                    assessment_date=datetime.fromisoformat(row[2]),
                    primary_values=[],
                    values_clarity_level=row[3],
                    values_commitment_level=row[4],
                    values_behavior_alignment=row[5],
                    major_discrepancies=json.loads(row[6]) if row[6] else [],
                    strengths_identified=json.loads(row[7]) if row[7] else [],
                    growth_areas=json.loads(row[8]) if row[8] else [],
                    cultural_considerations=json.loads(row[9]) if row[9] else [],
                    recommended_exercises=[ValuesExerciseType(ex) for ex in json.loads(row[10])] if row[10] else [],
                    action_plan_items=json.loads(row[11]) if row[11] else []
                )
            return None
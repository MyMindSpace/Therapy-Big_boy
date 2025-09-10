from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import sqlite3
import json


class AcceptanceType(Enum):
    EMOTIONAL = "emotional"
    PHYSICAL = "physical"
    COGNITIVE = "cognitive"
    SITUATIONAL = "situational"
    EXISTENTIAL = "existential"
    RELATIONAL = "relational"


class AcceptanceLevel(Enum):
    RESISTANCE = "resistance"
    STRUGGLING = "struggling"
    TOLERANCE = "tolerance"
    WILLINGNESS = "willingness"
    ACCEPTANCE = "acceptance"
    EMBRACING = "embracing"


class AcceptanceBarrier(Enum):
    CONTROL_ATTEMPTS = "control_attempts"
    AVOIDANCE_PATTERNS = "avoidance_patterns"
    JUDGMENT_RESISTANCE = "judgment_resistance"
    FEAR_OF_PAIN = "fear_of_pain"
    PERFECTIONISM = "perfectionism"
    ATTACHMENT_TO_OUTCOMES = "attachment_to_outcomes"
    CULTURAL_BELIEFS = "cultural_beliefs"


@dataclass
class AcceptanceStrategy:
    strategy_id: str
    name: str
    acceptance_type: AcceptanceType
    description: str
    core_principles: List[str]
    practice_instructions: List[str]
    metaphors_used: List[str]
    common_obstacles: List[AcceptanceBarrier]
    success_indicators: List[str]
    practice_exercises: List[str]
    integration_tips: List[str]
    contraindications: List[str]
    evidence_base: str


@dataclass
class AcceptancePractice:
    practice_id: str
    patient_id: str
    session_id: str
    strategy_used: str
    target_experience: str
    acceptance_type: AcceptanceType
    pre_practice_resistance: int
    post_practice_acceptance: int
    willingness_rating: int
    barriers_encountered: List[AcceptanceBarrier]
    breakthrough_moments: List[str]
    insights_gained: List[str]
    metaphor_effectiveness: Dict[str, int]
    homework_application: str
    therapist_observations: str
    patient_feedback: str
    practice_date: datetime = field(default_factory=datetime.now)


@dataclass
class AcceptanceAssessment:
    assessment_id: str
    patient_id: str
    assessment_date: datetime
    overall_acceptance_level: AcceptanceLevel
    domain_assessments: Dict[AcceptanceType, AcceptanceLevel]
    primary_barriers: List[AcceptanceBarrier]
    acceptance_strengths: List[str]
    growth_areas: List[str]
    willingness_indicators: List[str]
    avoidance_patterns: List[str]
    recommended_strategies: List[str]
    progress_markers: List[str]


class AcceptanceStrategiesModule:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.acceptance_strategies = self._initialize_acceptance_strategies()
        self.metaphor_library = self._initialize_metaphor_library()
        self.assessment_tools = self._initialize_assessment_tools()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS acceptance_practices (
                    practice_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    strategy_used TEXT NOT NULL,
                    target_experience TEXT,
                    acceptance_type TEXT,
                    pre_practice_resistance INTEGER,
                    post_practice_acceptance INTEGER,
                    willingness_rating INTEGER,
                    barriers_encountered TEXT,
                    breakthrough_moments TEXT,
                    insights_gained TEXT,
                    metaphor_effectiveness TEXT,
                    homework_application TEXT,
                    therapist_observations TEXT,
                    patient_feedback TEXT,
                    practice_date TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS acceptance_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    assessment_date TEXT,
                    overall_acceptance_level TEXT,
                    domain_assessments TEXT,
                    primary_barriers TEXT,
                    acceptance_strengths TEXT,
                    growth_areas TEXT,
                    willingness_indicators TEXT,
                    avoidance_patterns TEXT,
                    recommended_strategies TEXT,
                    progress_markers TEXT
                )
            """)
    
    def _initialize_acceptance_strategies(self) -> Dict[str, AcceptanceStrategy]:
        
        strategies = {}
        
        strategies["radical_acceptance"] = AcceptanceStrategy(
            strategy_id="radical_acceptance",
            name="Radical Acceptance",
            acceptance_type=AcceptanceType.SITUATIONAL,
            description="Complete acceptance of reality as it is, without approval or disapproval",
            core_principles=[
                "Pain is inevitable, suffering is optional",
                "Fighting reality increases suffering",
                "Acceptance is not approval",
                "Acceptance opens space for skillful action",
                "Present moment awareness facilitates acceptance"
            ],
            practice_instructions=[
                "Notice when you're fighting reality",
                "Acknowledge what is true in this moment",
                "Release the demand for things to be different",
                "Breathe into the experience without changing it",
                "Find willingness to experience what's here"
            ],
            metaphors_used=[
                "Swimming with the current vs. against it",
                "Quicksand - the more you struggle, the deeper you sink",
                "Weather - accepting storms as temporary conditions",
                "Holding sand with open vs. closed fists"
            ],
            common_obstacles=[
                AcceptanceBarrier.CONTROL_ATTEMPTS,
                AcceptanceBarrier.JUDGMENT_RESISTANCE,
                AcceptanceBarrier.FEAR_OF_PAIN
            ],
            success_indicators=[
                "Decreased struggle with unchangeable situations",
                "Increased emotional stability during difficulties",
                "Better decision-making from acceptance stance",
                "Reduced rumination about past events",
                "Greater peace with uncertainty"
            ],
            practice_exercises=[
                "Half-smile practice during difficult moments",
                "Willing hands posture during acceptance practice",
                "Reality acceptance phrases: 'This is the reality right now'",
                "Acceptance breathing meditation",
                "Radical acceptance coping statements"
            ],
            integration_tips=[
                "Start with small, less emotionally charged situations",
                "Practice acceptance of physical sensations first",
                "Use acceptance to create space before problem-solving",
                "Combine with mindfulness for present-moment awareness",
                "Apply to both external situations and internal experiences"
            ],
            contraindications=[
                "Active psychosis without insight",
                "Situations requiring immediate safety action",
                "When acceptance could enable harmful behaviors"
            ],
            evidence_base="Core DBT skill with extensive research support"
        )
        
        strategies["emotional_acceptance"] = AcceptanceStrategy(
            strategy_id="emotional_acceptance",
            name="Emotional Acceptance",
            acceptance_type=AcceptanceType.EMOTIONAL,
            description="Welcoming emotional experiences without judgment or immediate change attempts",
            core_principles=[
                "All emotions are valid messengers",
                "Emotions are temporary visitors, not permanent residents",
                "Feeling emotions fully allows them to naturally resolve",
                "Emotional acceptance reduces secondary suffering",
                "Emotions contain important information"
            ],
            practice_instructions=[
                "Notice and name the emotion without judgment",
                "Make space for the emotion in your body",
                "Breathe with the emotion rather than away from it",
                "Get curious about what the emotion is telling you",
                "Thank the emotion for its message"
            ],
            metaphors_used=[
                "Emotions as weather patterns passing through",
                "Emotions as waves - riding rather than being crushed",
                "Emotions as visitors - greeting them at the door",
                "Emotional landscape - being a spacious sky"
            ],
            common_obstacles=[
                AcceptanceBarrier.FEAR_OF_PAIN,
                AcceptanceBarrier.AVOIDANCE_PATTERNS,
                AcceptanceBarrier.JUDGMENT_RESISTANCE
            ],
            success_indicators=[
                "Increased emotional vocabulary and awareness",
                "Reduced emotional numbing or suppression",
                "Faster emotional recovery times",
                "Greater emotional intimacy in relationships",
                "Improved emotional decision-making"
            ],
            practice_exercises=[
                "Emotion surfing meditation",
                "RAIN technique (Recognize, Allow, Investigate, Natural awareness)",
                "Emotional body scan practice",
                "Loving-kindness toward difficult emotions",
                "Emotion acceptance journaling"
            ],
            integration_tips=[
                "Start with less intense emotions",
                "Practice when emotions are present, not just in theory",
                "Combine with self-compassion practices",
                "Use metaphors that resonate personally",
                "Celebrate small moments of emotional acceptance"
            ],
            contraindications=[
                "Severe dissociative episodes",
                "Overwhelming trauma responses requiring stabilization",
                "Active substance use affecting emotional processing"
            ],
            evidence_base="Supported by emotion regulation and ACT research"
        )
        
        strategies["physical_acceptance"] = AcceptanceStrategy(
            strategy_id="physical_acceptance",
            name="Physical Sensation Acceptance",
            acceptance_type=AcceptanceType.PHYSICAL,
            description="Accepting physical sensations, discomfort, and bodily experiences without resistance",
            core_principles=[
                "Body sensations are temporary and changing",
                "Resistance to sensations creates additional tension",
                "Acceptance allows natural healing processes",
                "Physical acceptance builds distress tolerance",
                "The body is a source of wisdom and information"
            ],
            practice_instructions=[
                "Scan your body with curious, non-judgmental attention",
                "Breathe into areas of tension or discomfort",
                "Soften around sensations rather than bracing against them",
                "Notice the changing nature of physical experiences",
                "Send kindness and acceptance to uncomfortable areas"
            ],
            metaphors_used=[
                "Body as a landscape to explore",
                "Sensations as clouds passing through the sky of awareness",
                "Physical discomfort as temporary guests",
                "Breathing space into tight areas"
            ],
            common_obstacles=[
                AcceptanceBarrier.FEAR_OF_PAIN,
                AcceptanceBarrier.CONTROL_ATTEMPTS,
                AcceptanceBarrier.AVOIDANCE_PATTERNS
            ],
            success_indicators=[
                "Reduced physical tension from resistance",
                "Improved pain management",
                "Greater body awareness and connection",
                "Reduced anxiety about physical sensations",
                "Enhanced relaxation capabilities"
            ],
            practice_exercises=[
                "Progressive muscle relaxation with acceptance",
                "Mindful movement with sensation awareness",
                "Breathing into discomfort meditation",
                "Body acceptance visualization",
                "Gentle yoga with acceptance principles"
            ],
            integration_tips=[
                "Practice with mild discomfort before intense pain",
                "Use with chronic conditions for improved coping",
                "Combine with breathing techniques",
                "Apply during medical procedures",
                "Integrate into daily body awareness practices"
            ],
            contraindications=[
                "Medical conditions requiring immediate attention",
                "Severe body dysmorphia",
                "Active eating disorder without proper support"
            ],
            evidence_base="Supported by chronic pain and somatic therapy research"
        )
        
        strategies["cognitive_acceptance"] = AcceptanceStrategy(
            strategy_id="cognitive_acceptance",
            name="Thought and Mind Acceptance",
            acceptance_type=AcceptanceType.COGNITIVE,
            description="Accepting thoughts, mental patterns, and cognitive experiences without fusion or fight",
            core_principles=[
                "Thoughts are mental events, not facts",
                "Fighting thoughts increases their power",
                "Mental acceptance creates space for choice",
                "Thoughts come and go naturally when not resisted",
                "Accepting thoughts reduces their emotional impact"
            ],
            practice_instructions=[
                "Notice thoughts without immediately evaluating them",
                "Observe thoughts as mental phenomena, not truth",
                "Allow thoughts to flow through awareness",
                "Thank your mind for its thoughts, even difficult ones",
                "Practice 'having' thoughts rather than 'being' thoughts"
            ],
            metaphors_used=[
                "Thoughts as leaves floating down a stream",
                "Mind as a radio station you can tune into or not",
                "Thoughts as clouds in the sky of awareness",
                "Mind as a storytelling machine"
            ],
            common_obstacles=[
                AcceptanceBarrier.ATTACHMENT_TO_OUTCOMES,
                AcceptanceBarrier.PERFECTIONISM,
                AcceptanceBarrier.JUDGMENT_RESISTANCE
            ],
            success_indicators=[
                "Reduced struggle with unwanted thoughts",
                "Decreased rumination and worry cycles",
                "Greater cognitive flexibility",
                "Improved concentration and focus",
                "Less reactivity to negative thoughts"
            ],
            practice_exercises=[
                "Leaves on a stream meditation",
                "Thought labeling practice",
                "Mental noting of thought patterns",
                "Cognitive defusion exercises",
                "Mindful observation of mind states"
            ],
            integration_tips=[
                "Practice with everyday thoughts before difficult ones",
                "Use humor and playfulness with thoughts",
                "Combine with defusion techniques",
                "Apply during overthinking episodes",
                "Integrate into daily mindfulness practice"
            ],
            contraindications=[
                "Active psychotic episodes",
                "Severe OCD without proper treatment",
                "Delusional thinking requiring medical intervention"
            ],
            evidence_base="Central to ACT and mindfulness-based interventions"
        )
        
        strategies["existential_acceptance"] = AcceptanceStrategy(
            strategy_id="existential_acceptance",
            name="Existential and Life Circumstance Acceptance",
            acceptance_type=AcceptanceType.EXISTENTIAL,
            description="Accepting fundamental life conditions, mortality, uncertainty, and human limitations",
            core_principles=[
                "Uncertainty is the only certainty in life",
                "Accepting mortality enhances life appreciation",
                "Human limitations are part of the shared condition",
                "Meaning emerges through acceptance of what is",
                "Existential acceptance reduces unnecessary suffering"
            ],
            practice_instructions=[
                "Acknowledge the reality of impermanence",
                "Accept uncertainty as a constant companion",
                "Embrace your humanity with its limitations",
                "Find meaning within, not despite, difficult circumstances",
                "Practice gratitude for what is present now"
            ],
            metaphors_used=[
                "Life as a river with changing currents",
                "Human existence as a temporary dance",
                "Uncertainty as the canvas for creative living",
                "Mortality as what makes each moment precious"
            ],
            common_obstacles=[
                AcceptanceBarrier.ATTACHMENT_TO_OUTCOMES,
                AcceptanceBarrier.CONTROL_ATTEMPTS,
                AcceptanceBarrier.FEAR_OF_PAIN
            ],
            success_indicators=[
                "Reduced anxiety about the future",
                "Greater peace with life's uncertainties",
                "Increased appreciation for present moments",
                "Less despair about uncontrollable circumstances",
                "Enhanced meaning-making capabilities"
            ],
            practice_exercises=[
                "Impermanence meditation",
                "Uncertainty tolerance practice",
                "Mortality reflection exercises",
                "Values clarification in face of limitations",
                "Meaning-making journaling"
            ],
            integration_tips=[
                "Connect to personal values and meaning",
                "Use during major life transitions",
                "Combine with gratitude practices",
                "Apply to aging and health challenges",
                "Integrate into spiritual or philosophical practices"
            ],
            contraindications=[
                "Active suicidal ideation",
                "Severe depression without stabilization",
                "Recent traumatic loss without adequate support"
            ],
            evidence_base="Supported by existential therapy and logotherapy research"
        )
        
        return strategies
    
    def _initialize_metaphor_library(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "weather_metaphors": {
                "emotional_storms": "Emotions are like weather - they arise, peak, and naturally pass. You are the sky that contains all weather patterns.",
                "sunny_cloudy_days": "Just as you don't fight cloudy weather, you can learn not to fight difficult emotional weather.",
                "seasonal_changes": "Life circumstances change like seasons - accepting winter allows you to appreciate spring."
            },
            
            "water_metaphors": {
                "swimming_with_current": "Acceptance is like swimming with the current rather than exhausting yourself fighting against it.",
                "waves_and_ocean": "Difficult experiences are waves on the ocean of your being - let them rise and fall naturally.",
                "quicksand": "Struggling against difficult emotions is like quicksand - the more you fight, the deeper you sink."
            },
            
            "nature_metaphors": {
                "mountain_storms": "Be like a mountain - let storms of emotion pass over you while remaining grounded and stable.",
                "tree_in_wind": "Flexibility in acceptance allows you to bend without breaking, like a tree in strong wind.",
                "river_stones": "Acceptance smooths rough experiences like water gradually smooths river stones."
            },
            
            "container_metaphors": {
                "spacious_room": "Your awareness is like a spacious room that can hold any experience without being damaged.",
                "open_hands": "Hold experiences with open hands - grasping too tightly makes them harder to bear.",
                "guest_house": "Welcome all experiences as temporary guests in the guest house of your awareness."
            }
        }
    
    def _initialize_assessment_tools(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "acceptance_domains": {
                AcceptanceType.EMOTIONAL: [
                    "I can feel difficult emotions without immediately trying to change them",
                    "I notice emotions without judging them as good or bad",
                    "I can stay present with intense feelings",
                    "I allow emotions to naturally come and go"
                ],
                AcceptanceType.PHYSICAL: [
                    "I can accept physical discomfort without excessive worry",
                    "I notice body sensations with curiosity rather than fear",
                    "I can be present with pain without making it worse",
                    "I treat my body with kindness during difficult times"
                ],
                AcceptanceType.COGNITIVE: [
                    "I can observe thoughts without believing them automatically",
                    "I notice mental patterns without getting caught in them",
                    "I can have difficult thoughts without fighting them",
                    "I recognize thoughts as mental events, not facts"
                ],
                AcceptanceType.SITUATIONAL: [
                    "I can accept difficult circumstances I cannot change",
                    "I don't waste energy fighting unchangeable realities",
                    "I can find peace even in challenging situations",
                    "I adapt to life changes with flexibility"
                ]
            },
            
            "acceptance_barriers_assessment": {
                AcceptanceBarrier.CONTROL_ATTEMPTS: [
                    "I often try to control things beyond my influence",
                    "I get frustrated when I can't change outcomes",
                    "I believe I should be able to control my feelings"
                ],
                AcceptanceBarrier.AVOIDANCE_PATTERNS: [
                    "I go to great lengths to avoid difficult experiences",
                    "I distract myself when uncomfortable feelings arise",
                    "I believe avoiding pain is always best"
                ],
                AcceptanceBarrier.JUDGMENT_RESISTANCE: [
                    "I judge myself harshly for having difficult experiences",
                    "I think some emotions are wrong or bad",
                    "I believe I shouldn't feel certain ways"
                ]
            }
        }
    
    def conduct_acceptance_practice(self, patient_id: str, session_id: str, 
                                  strategy_id: str, target_experience: str) -> AcceptancePractice:
        
        practice_id = f"{patient_id}_{strategy_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        strategy = self.acceptance_strategies.get(strategy_id)
        if not strategy:
            raise ValueError(f"Acceptance strategy {strategy_id} not found")
        
        practice = AcceptancePractice(
            practice_id=practice_id,
            patient_id=patient_id,
            session_id=session_id,
            strategy_used=strategy_id,
            target_experience=target_experience,
            acceptance_type=strategy.acceptance_type,
            pre_practice_resistance=0,
            post_practice_acceptance=0,
            willingness_rating=0,
            barriers_encountered=[],
            breakthrough_moments=[],
            insights_gained=[],
            metaphor_effectiveness={},
            homework_application="",
            therapist_observations="",
            patient_feedback=""
        )
        
        self._save_acceptance_practice(practice)
        return practice
    
    def assess_acceptance_levels(self, patient_id: str, assessment_data: Dict[str, Any]) -> AcceptanceAssessment:
        
        assessment_id = f"{patient_id}_acceptance_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        domain_scores = {}
        for domain_type in AcceptanceType:
            domain_items = self.assessment_tools["acceptance_domains"].get(domain_type, [])
            domain_responses = assessment_data.get(f"{domain_type.value}_responses", [])
            
            if domain_responses:
                avg_score = sum(domain_responses) / len(domain_responses)
                domain_scores[domain_type] = self._score_to_acceptance_level(avg_score)
            else:
                domain_scores[domain_type] = AcceptanceLevel.TOLERANCE
        
        overall_acceptance = self._calculate_overall_acceptance(domain_scores)
        primary_barriers = self._identify_primary_barriers(assessment_data)
        acceptance_strengths = self._identify_acceptance_strengths(domain_scores)
        growth_areas = self._identify_growth_areas(domain_scores)
        
        assessment = AcceptanceAssessment(
            assessment_id=assessment_id,
            patient_id=patient_id,
            assessment_date=datetime.now(),
            overall_acceptance_level=overall_acceptance,
            domain_assessments=domain_scores,
            primary_barriers=primary_barriers,
            acceptance_strengths=acceptance_strengths,
            growth_areas=growth_areas,
            willingness_indicators=assessment_data.get("willingness_indicators", []),
            avoidance_patterns=assessment_data.get("avoidance_patterns", []),
            recommended_strategies=self._recommend_strategies(domain_scores, primary_barriers),
            progress_markers=self._generate_progress_markers(domain_scores)
        )
        
        self._save_acceptance_assessment(assessment)
        return assessment
    
    def _score_to_acceptance_level(self, score: float) -> AcceptanceLevel:
        
        if score >= 4.5:
            return AcceptanceLevel.EMBRACING
        elif score >= 3.5:
            return AcceptanceLevel.ACCEPTANCE
        elif score >= 2.5:
            return AcceptanceLevel.WILLINGNESS
        elif score >= 1.5:
            return AcceptanceLevel.TOLERANCE
        elif score >= 0.5:
            return AcceptanceLevel.STRUGGLING
        else:
            return AcceptanceLevel.RESISTANCE
    
    def _calculate_overall_acceptance(self, domain_scores: Dict[AcceptanceType, AcceptanceLevel]) -> AcceptanceLevel:
        
        level_values = {
            AcceptanceLevel.RESISTANCE: 0,
            AcceptanceLevel.STRUGGLING: 1,
            AcceptanceLevel.TOLERANCE: 2,
            AcceptanceLevel.WILLINGNESS: 3,
            AcceptanceLevel.ACCEPTANCE: 4,
            AcceptanceLevel.EMBRACING: 5
        }
        
        total_score = sum(level_values[level] for level in domain_scores.values())
        avg_score = total_score / len(domain_scores)
        
        for level, value in level_values.items():
            if avg_score <= value + 0.5:
                return level
        
        return AcceptanceLevel.EMBRACING
    
    def _identify_primary_barriers(self, assessment_data: Dict[str, Any]) -> List[AcceptanceBarrier]:
        
        barriers = []
        barrier_thresholds = {
            AcceptanceBarrier.CONTROL_ATTEMPTS: 3.0,
            AcceptanceBarrier.AVOIDANCE_PATTERNS: 3.0,
            AcceptanceBarrier.JUDGMENT_RESISTANCE: 3.0,
            AcceptanceBarrier.FEAR_OF_PAIN: 3.0,
            AcceptanceBarrier.PERFECTIONISM: 3.0,
            AcceptanceBarrier.ATTACHMENT_TO_OUTCOMES: 3.0
        }
        
        for barrier, threshold in barrier_thresholds.items():
            barrier_score = assessment_data.get(f"{barrier.value}_score", 0)
            if barrier_score >= threshold:
                barriers.append(barrier)
        
        return barriers[:3]
    
    def _identify_acceptance_strengths(self, domain_scores: Dict[AcceptanceType, AcceptanceLevel]) -> List[str]:
        
        strengths = []
        
        for domain, level in domain_scores.items():
            if level in [AcceptanceLevel.ACCEPTANCE, AcceptanceLevel.EMBRACING]:
                domain_name = domain.value.replace('_', ' ').title()
                strengths.append(f"Strong {domain_name} acceptance")
        
        return strengths
    
    def _identify_growth_areas(self, domain_scores: Dict[AcceptanceType, AcceptanceLevel]) -> List[str]:
        
        growth_areas = []
        
        for domain, level in domain_scores.items():
            if level in [AcceptanceLevel.RESISTANCE, AcceptanceLevel.STRUGGLING]:
                domain_name = domain.value.replace('_', ' ').title()
                growth_areas.append(f"Develop {domain_name} acceptance")
        
        return growth_areas
    
    def _recommend_strategies(self, domain_scores: Dict[AcceptanceType, AcceptanceLevel], 
                            barriers: List[AcceptanceBarrier]) -> List[str]:
        
        recommendations = []
        
        lowest_domains = [domain for domain, level in domain_scores.items() 
                         if level in [AcceptanceLevel.RESISTANCE, AcceptanceLevel.STRUGGLING]]
        
        strategy_mapping = {
            AcceptanceType.EMOTIONAL: "emotional_acceptance",
            AcceptanceType.PHYSICAL: "physical_acceptance",
            AcceptanceType.COGNITIVE: "cognitive_acceptance",
            AcceptanceType.SITUATIONAL: "radical_acceptance",
            AcceptanceType.EXISTENTIAL: "existential_acceptance"
        }
        
        for domain in lowest_domains[:2]:
            strategy_id = strategy_mapping.get(domain)
            if strategy_id:
                recommendations.append(strategy_id)
        
        if AcceptanceBarrier.CONTROL_ATTEMPTS in barriers:
            recommendations.append("radical_acceptance")
        
        if AcceptanceBarrier.FEAR_OF_PAIN in barriers:
            recommendations.append("emotional_acceptance")
        
        return list(set(recommendations))[:3]
    
    def _generate_progress_markers(self, domain_scores: Dict[AcceptanceType, AcceptanceLevel]) -> List[str]:
        
        markers = []
        
        for domain, level in domain_scores.items():
            domain_name = domain.value.replace('_', ' ')
            
            if level == AcceptanceLevel.RESISTANCE:
                markers.append(f"Begin developing awareness of {domain_name} experiences")
            elif level == AcceptanceLevel.STRUGGLING:
                markers.append(f"Reduce struggle with {domain_name} experiences")
            elif level == AcceptanceLevel.TOLERANCE:
                markers.append(f"Increase willingness toward {domain_name} experiences")
            elif level == AcceptanceLevel.WILLINGNESS:
                markers.append(f"Deepen acceptance of {domain_name} experiences")
            elif level == AcceptanceLevel.ACCEPTANCE:
                markers.append(f"Maintain and generalize {domain_name} acceptance")
        
        return markers[:4]
    
    def create_acceptance_intervention_plan(self, patient_id: str, assessment: AcceptanceAssessment) -> Dict[str, Any]:
        
        plan = {
            "patient_id": patient_id,
            "assessment_date": assessment.assessment_date.isoformat(),
            "intervention_focus": [],
            "recommended_strategies": assessment.recommended_strategies,
            "practice_sequence": [],
            "homework_assignments": [],
            "progress_targets": assessment.progress_markers,
            "session_structure": {}
        }
        
        if assessment.overall_acceptance_level in [AcceptanceLevel.RESISTANCE, AcceptanceLevel.STRUGGLING]:
            plan["intervention_focus"].append("psychoeducation_about_acceptance")
            plan["intervention_focus"].append("acceptance_motivation_building")
            plan["practice_sequence"].extend([
                "Start with least threatening acceptance practices",
                "Use metaphors extensively to explain concepts",
                "Focus on willingness rather than full acceptance initially"
            ])
        
        elif assessment.overall_acceptance_level == AcceptanceLevel.TOLERANCE:
            plan["intervention_focus"].append("willingness_cultivation")
            plan["intervention_focus"].append("acceptance_skill_building")
            plan["practice_sequence"].extend([
                "Practice acceptance with moderate difficulty experiences",
                "Develop personal acceptance phrases and cues",
                "Begin homework applications"
            ])
        
        else:
            plan["intervention_focus"].append("acceptance_generalization")
            plan["intervention_focus"].append("integration_with_action")
            plan["practice_sequence"].extend([
                "Apply acceptance to complex life situations",
                "Combine acceptance with values-based action",
                "Develop teaching or mentoring opportunities"
            ])
        
        for strategy_id in assessment.recommended_strategies:
            strategy = self.acceptance_strategies.get(strategy_id)
            if strategy:
                plan["homework_assignments"].extend(strategy.practice_exercises[:2])
        
        plan["session_structure"] = {
            "opening": "Brief mindfulness to center in present moment",
            "assessment": "Check current acceptance challenges",
            "psychoeducation": "Explain acceptance principles relevant to current struggles",
            "practice": "Guided acceptance exercise with target experience",
            "integration": "Connect practice to daily life applications",
            "homework": "Assign specific acceptance practice for coming week"
        }
        
        return plan
    
    def track_acceptance_progress(self, patient_id: str, weeks: int = 4) -> Dict[str, Any]:
        
        start_date = datetime.now() - timedelta(weeks=weeks)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT practice_date, acceptance_type, pre_practice_resistance,
                       post_practice_acceptance, willingness_rating, barriers_encountered
                FROM acceptance_practices
                WHERE patient_id = ? AND practice_date >= ?
                ORDER BY practice_date
            """, (patient_id, start_date.isoformat()))
            
            practices = cursor.fetchall()
        
        if not practices:
            return {"error": "No acceptance practice data found"}
        
        progress = {
            "patient_id": patient_id,
            "tracking_period_weeks": weeks,
            "total_practices": len(practices),
            "acceptance_trends": {},
            "willingness_progression": [],
            "barrier_patterns": {},
            "breakthrough_indicators": [],
            "recommendations": []
        }
        
        acceptance_changes = []
        willingness_scores = []
        all_barriers = []
        
        for practice_date, acceptance_type, pre_resistance, post_acceptance, willingness, barriers_json in practices:
            if pre_resistance is not None and post_acceptance is not None:
                change = post_acceptance - pre_resistance
                acceptance_changes.append(change)
                
                if acceptance_type not in progress["acceptance_trends"]:
                    progress["acceptance_trends"][acceptance_type] = []
                progress["acceptance_trends"][acceptance_type].append(change)
            
            if willingness is not None:
                willingness_scores.append(willingness)
                progress["willingness_progression"].append({
                    "date": practice_date,
                    "score": willingness
                })
            
            if barriers_json:
                barriers = json.loads(barriers_json)
                all_barriers.extend([barrier.value if hasattr(barrier, 'value') else str(barrier) for barrier in barriers])
        
        if acceptance_changes:
            avg_change = sum(acceptance_changes) / len(acceptance_changes)
            progress["average_acceptance_improvement"] = round(avg_change, 2)
            
            if avg_change >= 2.0:
                progress["breakthrough_indicators"].append("Significant acceptance improvements across practices")
            elif avg_change >= 1.0:
                progress["breakthrough_indicators"].append("Consistent moderate acceptance improvements")
        
        if willingness_scores:
            if len(willingness_scores) >= 3:
                recent_avg = sum(willingness_scores[-3:]) / 3
                early_avg = sum(willingness_scores[:3]) / 3
                
                if recent_avg > early_avg + 1.0:
                    progress["breakthrough_indicators"].append("Increasing willingness over time")
        
        barrier_frequency = {}
        for barrier in all_barriers:
            barrier_frequency[barrier] = barrier_frequency.get(barrier, 0) + 1
        
        progress["barrier_patterns"] = dict(sorted(barrier_frequency.items(), key=lambda x: x[1], reverse=True)[:5])
        
        if progress["total_practices"] < weeks:
            progress["recommendations"].append("Increase frequency of acceptance practice")
        
        if progress.get("average_acceptance_improvement", 0) < 0.5:
            progress["recommendations"].append("Explore barriers to acceptance progress")
        
        most_common_barrier = max(barrier_frequency, key=barrier_frequency.get) if barrier_frequency else None
        if most_common_barrier:
            progress["recommendations"].append(f"Focus on addressing {most_common_barrier} barrier")
        
        return progress
    
    def generate_acceptance_homework(self, strategy_id: str, difficulty_level: str = "moderate") -> Dict[str, Any]:
        
        strategy = self.acceptance_strategies.get(strategy_id)
        if not strategy:
            raise ValueError(f"Strategy {strategy_id} not found")
        
        difficulty_exercises = {
            "easy": {
                "duration": "5-10 minutes daily",
                "frequency": "Once daily",
                "intensity": "Low emotional charge situations"
            },
            "moderate": {
                "duration": "10-15 minutes daily",
                "frequency": "Twice daily",
                "intensity": "Moderate emotional charge situations"
            },
            "challenging": {
                "duration": "15-20 minutes daily",
                "frequency": "Multiple times daily",
                "intensity": "Higher emotional charge situations"
            }
        }
        
        level_config = difficulty_exercises.get(difficulty_level, difficulty_exercises["moderate"])
        
        homework = {
            "strategy_name": strategy.name,
            "strategy_type": strategy.acceptance_type.value,
            "duration": level_config["duration"],
            "frequency": level_config["frequency"],
            "target_situations": level_config["intensity"],
            "core_instructions": strategy.practice_instructions[:3],
            "specific_exercises": [],
            "metaphors_to_use": strategy.metaphors_used[:2],
            "success_indicators": strategy.success_indicators[:3],
            "common_obstacles": [barrier.value for barrier in strategy.common_obstacles[:2]],
            "integration_tips": strategy.integration_tips[:3],
            "homework_log": {
                "daily_practice": "Rate acceptance level 1-10 before and after practice",
                "situations_applied": "Note 2-3 situations where you applied acceptance",
                "insights_gained": "Record any insights or breakthroughs",
                "barriers_encountered": "Note obstacles and how you worked with them"
            }
        }
        
        if difficulty_level == "easy":
            homework["specific_exercises"] = [
                "Practice acceptance with minor daily irritations",
                "Use acceptance breathing with mild physical discomfort",
                "Apply acceptance phrases to small disappointments"
            ]
        elif difficulty_level == "moderate":
            homework["specific_exercises"] = [
                "Practice acceptance during moderate stress or conflict",
                "Apply acceptance to recurring worry thoughts",
                "Use acceptance strategies during uncomfortable emotions"
            ]
        else:  # challenging
            homework["specific_exercises"] = [
                "Practice acceptance during intense emotional experiences",
                "Apply acceptance to major life stressors or changes",
                "Use acceptance during interpersonal conflicts or rejections"
            ]
        
        return homework
    
    def create_acceptance_metaphor_session(self, patient_id: str, target_experience: str, 
                                         patient_preferences: Dict[str, Any]) -> Dict[str, Any]:
        
        preferred_imagery = patient_preferences.get("preferred_imagery", ["nature", "water"])
        cultural_considerations = patient_preferences.get("cultural_background", [])
        personal_interests = patient_preferences.get("interests", [])
        
        session_plan = {
            "patient_id": patient_id,
            "target_experience": target_experience,
            "selected_metaphors": [],
            "metaphor_exercises": [],
            "integration_activities": [],
            "personalization_notes": []
        }
        
        metaphor_selection = []
        
        if "nature" in preferred_imagery:
            metaphor_selection.extend([
                "Mountain weathering storms (emotional acceptance)",
                "Tree bending in wind (flexibility with circumstances)",
                "Seasons changing naturally (accepting life transitions)"
            ])
        
        if "water" in preferred_imagery:
            metaphor_selection.extend([
                "Swimming with current vs. against it (radical acceptance)",
                "Waves rising and falling (emotional acceptance)",
                "River finding its way around obstacles (adaptability)"
            ])
        
        if "space" in preferred_imagery:
            metaphor_selection.extend([
                "Sky containing all weather (awareness holding experiences)",
                "Stars shining through darkness (finding peace in difficulty)",
                "Gravity as natural law (accepting unchangeable realities)"
            ])
        
        session_plan["selected_metaphors"] = metaphor_selection[:3]
        
        for metaphor in session_plan["selected_metaphors"]:
            exercise = {
                "metaphor": metaphor,
                "guided_visualization": f"Spend 5 minutes visualizing yourself as {metaphor.split('(')[0].strip()}",
                "application_practice": f"Apply this metaphor to your current experience: {target_experience}",
                "integration_question": f"How does this metaphor change your relationship to {target_experience}?"
            }
            session_plan["metaphor_exercises"].append(exercise)
        
        session_plan["integration_activities"] = [
            "Create a personal metaphor that resonates with your experience",
            "Draw or write about your chosen metaphor",
            "Practice using your metaphor during the week when challenges arise",
            "Share your metaphor with someone you trust"
        ]
        
        if cultural_considerations:
            session_plan["personalization_notes"].append(f"Consider metaphors from {', '.join(cultural_considerations)} traditions")
        
        if personal_interests:
            session_plan["personalization_notes"].append(f"Incorporate interests like {', '.join(personal_interests)} into metaphor development")
        
        return session_plan
    
    def evaluate_acceptance_intervention_effectiveness(self, patient_id: str, 
                                                     intervention_start_date: datetime) -> Dict[str, Any]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*), AVG(post_practice_acceptance), AVG(willingness_rating),
                       AVG(pre_practice_resistance)
                FROM acceptance_practices
                WHERE patient_id = ? AND practice_date >= ?
            """, (patient_id, intervention_start_date.isoformat()))
            
            overall_stats = cursor.fetchone()
            
            cursor.execute("""
                SELECT strategy_used, COUNT(*), AVG(post_practice_acceptance - pre_practice_resistance) as avg_improvement
                FROM acceptance_practices
                WHERE patient_id = ? AND practice_date >= ?
                GROUP BY strategy_used
                ORDER BY avg_improvement DESC
            """, (patient_id, intervention_start_date.isoformat()))
            
            strategy_effectiveness = cursor.fetchall()
        
        evaluation = {
            "patient_id": patient_id,
            "intervention_period": f"Since {intervention_start_date.strftime('%Y-%m-%d')}",
            "overall_metrics": {},
            "strategy_effectiveness": {},
            "intervention_success": "unknown",
            "recommendations": []
        }
        
        if overall_stats and overall_stats[0] > 0:
            total_practices, avg_acceptance, avg_willingness, avg_pre_resistance = overall_stats
            
            evaluation["overall_metrics"] = {
                "total_practices": total_practices,
                "average_post_acceptance": round(avg_acceptance, 2) if avg_acceptance else 0,
                "average_willingness": round(avg_willingness, 2) if avg_willingness else 0,
                "average_improvement": round(avg_acceptance - avg_pre_resistance, 2) if avg_acceptance and avg_pre_resistance else 0
            }
            
            avg_improvement = evaluation["overall_metrics"]["average_improvement"]
            
            if avg_improvement >= 2.5:
                evaluation["intervention_success"] = "highly_effective"
            elif avg_improvement >= 1.5:
                evaluation["intervention_success"] = "moderately_effective"
            elif avg_improvement >= 0.5:
                evaluation["intervention_success"] = "somewhat_effective"
            else:
                evaluation["intervention_success"] = "minimally_effective"
        
        for strategy, count, improvement in strategy_effectiveness:
            evaluation["strategy_effectiveness"][strategy] = {
                "practice_count": count,
                "average_improvement": round(improvement, 2) if improvement else 0
            }
        
        if evaluation["overall_metrics"].get("total_practices", 0) < 8:
            evaluation["recommendations"].append("Increase practice frequency for better outcomes")
        
        if evaluation["overall_metrics"].get("average_improvement", 0) < 1.0:
            evaluation["recommendations"].append("Explore barriers to acceptance progress")
            evaluation["recommendations"].append("Consider modifying intervention approach")
        
        most_effective_strategy = max(strategy_effectiveness, key=lambda x: x[2]) if strategy_effectiveness else None
        if most_effective_strategy:
            evaluation["recommendations"].append(f"Continue focus on {most_effective_strategy[0]} strategy")
        
        return evaluation
    
    def _save_acceptance_practice(self, practice: AcceptancePractice):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO acceptance_practices
                (practice_id, patient_id, session_id, strategy_used, target_experience,
                 acceptance_type, pre_practice_resistance, post_practice_acceptance,
                 willingness_rating, barriers_encountered, breakthrough_moments,
                 insights_gained, metaphor_effectiveness, homework_application,
                 therapist_observations, patient_feedback, practice_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                practice.practice_id, practice.patient_id, practice.session_id,
                practice.strategy_used, practice.target_experience, practice.acceptance_type.value,
                practice.pre_practice_resistance, practice.post_practice_acceptance,
                practice.willingness_rating, json.dumps([b.value for b in practice.barriers_encountered]),
                json.dumps(practice.breakthrough_moments), json.dumps(practice.insights_gained),
                json.dumps(practice.metaphor_effectiveness), practice.homework_application,
                practice.therapist_observations, practice.patient_feedback,
                practice.practice_date.isoformat()
            ))
    
    def _save_acceptance_assessment(self, assessment: AcceptanceAssessment):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO acceptance_assessments
                (assessment_id, patient_id, assessment_date, overall_acceptance_level,
                 domain_assessments, primary_barriers, acceptance_strengths,
                 growth_areas, willingness_indicators, avoidance_patterns,
                 recommended_strategies, progress_markers)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id, assessment.patient_id, assessment.assessment_date.isoformat(),
                assessment.overall_acceptance_level.value,
                json.dumps({k.value: v.value for k, v in assessment.domain_assessments.items()}),
                json.dumps([b.value for b in assessment.primary_barriers]),
                json.dumps(assessment.acceptance_strengths), json.dumps(assessment.growth_areas),
                json.dumps(assessment.willingness_indicators), json.dumps(assessment.avoidance_patterns),
                json.dumps(assessment.recommended_strategies), json.dumps(assessment.progress_markers)
            ))


if __name__ == "__main__":
    acceptance_module = AcceptanceStrategiesModule()
    
    practice = acceptance_module.conduct_acceptance_practice(
        patient_id="patient_123",
        session_id="session_001",
        strategy_id="radical_acceptance",
        target_experience="Anxiety about job interview"
    )
    
    print("=== ACCEPTANCE PRACTICE SESSION ===")
    print(f"Practice ID: {practice.practice_id}")
    print(f"Strategy: {practice.strategy_used}")
    print(f"Target: {practice.target_experience}")
    print(f"Type: {practice.acceptance_type.value}")
    
    assessment_data = {
        "emotional_responses": [3, 4, 3, 2],  # Example ratings 1-5
        "physical_responses": [4, 4, 3, 4],
        "cognitive_responses": [2, 3, 2, 3],
        "situational_responses": [3, 2, 3, 3],
        "control_attempts_score": 4.0,
        "avoidance_patterns_score": 3.5,
        "judgment_resistance_score": 3.0,
        "willingness_indicators": ["Uses acceptance language", "Shows openness to difficult emotions"],
        "avoidance_patterns": ["Distraction when anxious", "Avoids conflict situations"]
    }
    
    assessment = acceptance_module.assess_acceptance_levels("patient_123", assessment_data)
    print(f"\n=== ACCEPTANCE ASSESSMENT ===")
    print(f"Overall Level: {assessment.overall_acceptance_level.value}")
    print(f"Domain Assessments: {[(k.value, v.value) for k, v in assessment.domain_assessments.items()]}")
    print(f"Primary Barriers: {[b.value for b in assessment.primary_barriers]}")
    print(f"Recommended Strategies: {assessment.recommended_strategies}")
    
    intervention_plan = acceptance_module.create_acceptance_intervention_plan("patient_123", assessment)
    print(f"\n=== INTERVENTION PLAN ===")
    print(f"Focus Areas: {intervention_plan['intervention_focus']}")
    print(f"Practice Sequence: {intervention_plan['practice_sequence']}")
    print(f"Homework: {intervention_plan['homework_assignments'][:2]}")
    
    homework = acceptance_module.generate_acceptance_homework("emotional_acceptance", "moderate")
    print(f"\n=== HOMEWORK ASSIGNMENT ===")
    print(f"Strategy: {homework['strategy_name']}")
    print(f"Duration: {homework['duration']}")
    print(f"Exercises: {homework['specific_exercises']}")
    print(f"Metaphors: {homework['metaphors_to_use']}")
    
    patient_prefs = {
        "preferred_imagery": ["nature", "water"],
        "cultural_background": ["mindfulness_tradition"],
        "interests": ["gardening", "hiking"]
    }
    
    metaphor_session = acceptance_module.create_acceptance_metaphor_session(
        "patient_123", "Work stress", patient_prefs
    )
    print(f"\n=== METAPHOR SESSION ===")
    print(f"Target: {metaphor_session['target_experience']}")
    print(f"Selected Metaphors: {metaphor_session['selected_metaphors']}")
    print(f"Personalization: {metaphor_session['personalization_notes']}")
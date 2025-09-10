from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import sqlite3
import json


class MindfulnessType(Enum):
    PRESENT_MOMENT = "present_moment"
    OBSERVING_SELF = "observing_self"
    CONTACT_WITH_NOW = "contact_with_now"
    FLEXIBLE_ATTENTION = "flexible_attention"
    NON_JUDGMENTAL_AWARENESS = "non_judgmental_awareness"
    EXPERIENTIAL_AWARENESS = "experiential_awareness"


class PracticeFormat(Enum):
    FORMAL_MEDITATION = "formal_meditation"
    INFORMAL_PRACTICE = "informal_practice"
    MOVEMENT_BASED = "movement_based"
    EVERYDAY_MINDFULNESS = "everyday_mindfulness"
    BRIEF_CENTERING = "brief_centering"
    EXTENDED_RETREAT = "extended_retreat"


class AttentionQuality(Enum):
    SCATTERED = "scattered"
    WANDERING = "wandering"
    FOCUSED = "focused"
    STABLE = "stable"
    EFFORTLESS = "effortless"
    PANORAMIC = "panoramic"


class MindfulnessBarrier(Enum):
    RESTLESSNESS = "restlessness"
    DROWSINESS = "drowsiness"
    DOUBT = "doubt"
    AVERSION = "aversion"
    CRAVING = "craving"
    IMPATIENCE = "impatience"
    PERFECTIONISM = "perfectionism"
    CONCEPTUAL_THINKING = "conceptual_thinking"


@dataclass
class MindfulnessPractice:
    practice_id: str
    name: str
    mindfulness_type: MindfulnessType
    practice_format: PracticeFormat
    description: str
    core_instructions: List[str]
    duration_range: Tuple[int, int]
    difficulty_level: str
    target_outcomes: List[str]
    preparation_steps: List[str]
    common_experiences: List[str]
    troubleshooting_tips: Dict[MindfulnessBarrier, List[str]]
    integration_suggestions: List[str]
    contraindications: List[str]
    evidence_base: str


@dataclass
class MindfulnessSession:
    session_id: str
    patient_id: str
    practice_used: str
    session_duration: int
    attention_quality_start: AttentionQuality
    attention_quality_end: AttentionQuality
    present_moment_awareness: int
    non_judgmental_stance: int
    observing_self_access: int
    barriers_encountered: List[MindfulnessBarrier]
    insights_gained: List[str]
    body_sensations_noticed: List[str]
    emotional_states_observed: List[str]
    thoughts_patterns_recognized: List[str]
    post_practice_mood: int
    mindfulness_carryover: int
    homework_connection: str
    therapist_observations: str
    patient_feedback: str
    session_date: datetime = field(default_factory=datetime.now)


@dataclass
class MindfulnessAssessment:
    assessment_id: str
    patient_id: str
    assessment_date: datetime
    overall_mindfulness_level: int
    present_moment_awareness: int
    observing_self_strength: int
    non_judgmental_capacity: int
    attention_regulation: int
    emotional_awareness: int
    body_awareness: int
    thought_awareness: int
    daily_life_integration: int
    primary_strengths: List[str]
    development_areas: List[str]
    preferred_practices: List[str]
    challenging_barriers: List[MindfulnessBarrier]
    recommended_interventions: List[str]
    practice_readiness: str


class ACTMindfulnessPracticesModule:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.mindfulness_practices = self._initialize_mindfulness_practices()
        self.guided_scripts = self._initialize_guided_scripts()
        self.assessment_tools = self._initialize_assessment_tools()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mindfulness_sessions (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    practice_used TEXT NOT NULL,
                    session_duration INTEGER,
                    attention_quality_start TEXT,
                    attention_quality_end TEXT,
                    present_moment_awareness INTEGER,
                    non_judgmental_stance INTEGER,
                    observing_self_access INTEGER,
                    barriers_encountered TEXT,
                    insights_gained TEXT,
                    body_sensations_noticed TEXT,
                    emotional_states_observed TEXT,
                    thoughts_patterns_recognized TEXT,
                    post_practice_mood INTEGER,
                    mindfulness_carryover INTEGER,
                    homework_connection TEXT,
                    therapist_observations TEXT,
                    patient_feedback TEXT,
                    session_date TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mindfulness_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    assessment_date TEXT,
                    overall_mindfulness_level INTEGER,
                    present_moment_awareness INTEGER,
                    observing_self_strength INTEGER,
                    non_judgmental_capacity INTEGER,
                    attention_regulation INTEGER,
                    emotional_awareness INTEGER,
                    body_awareness INTEGER,
                    thought_awareness INTEGER,
                    daily_life_integration INTEGER,
                    primary_strengths TEXT,
                    development_areas TEXT,
                    preferred_practices TEXT,
                    challenging_barriers TEXT,
                    recommended_interventions TEXT,
                    practice_readiness TEXT
                )
            """)
    
    def _initialize_mindfulness_practices(self) -> Dict[str, MindfulnessPractice]:
        
        practices = {}
        
        practices["present_moment_awareness"] = MindfulnessPractice(
            practice_id="present_moment_awareness",
            name="Present Moment Awareness",
            mindfulness_type=MindfulnessType.PRESENT_MOMENT,
            practice_format=PracticeFormat.FORMAL_MEDITATION,
            description="Anchoring attention in the immediate here-and-now experience",
            core_instructions=[
                "Sit comfortably with eyes closed or softly focused",
                "Notice what's happening right now in this moment",
                "When mind wanders to past or future, gently return to now",
                "Use breath, body sensations, or sounds as present moment anchors",
                "Practice accepting whatever arises without trying to change it",
                "Cultivate curiosity about immediate experience"
            ],
            duration_range=(5, 30),
            difficulty_level="beginner",
            target_outcomes=[
                "Increased present moment orientation",
                "Reduced mental time travel",
                "Greater awareness of immediate experience",
                "Improved ability to return attention to now",
                "Enhanced appreciation for current moments"
            ],
            preparation_steps=[
                "Find a quiet, comfortable space",
                "Set intention to practice present moment awareness",
                "Choose an anchor for attention (breath, body, sounds)",
                "Release agenda about how practice should go"
            ],
            common_experiences=[
                "Initial restlessness or fidgeting",
                "Frequent mind wandering to past/future",
                "Moments of clear present moment contact",
                "Surprise at how rarely we're actually present",
                "Increased appreciation for simple experiences"
            ],
            troubleshooting_tips={
                MindfulnessBarrier.RESTLESSNESS: [
                    "Start with shorter periods",
                    "Use movement-based mindfulness",
                    "Accept restlessness as part of present moment"
                ],
                MindfulnessBarrier.CONCEPTUAL_THINKING: [
                    "Return to sensory experience",
                    "Use concrete anchors like breath or sounds",
                    "Practice labeling 'thinking' and returning to now"
                ]
            },
            integration_suggestions=[
                "Set random alarms to check present moment awareness",
                "Practice during daily activities like eating or walking",
                "Use present moment awareness during transitions",
                "Apply when feeling anxious about future or stuck in past"
            ],
            contraindications=[
                "Active psychotic episodes",
                "Severe dissociative disorders without support",
                "Acute trauma requiring stabilization"
            ],
            evidence_base="Core ACT mindfulness with extensive research support"
        )
        
        practices["observing_self"] = MindfulnessPractice(
            practice_id="observing_self",
            name="Observing Self Practice",
            mindfulness_type=MindfulnessType.OBSERVING_SELF,
            practice_format=PracticeFormat.FORMAL_MEDITATION,
            description="Connecting with the part of you that observes all experiences",
            core_instructions=[
                "Begin by noticing you are aware right now",
                "Observe your thoughts without being caught in them",
                "Notice you are the one watching emotions come and go",
                "Recognize the stable awareness that observes all changing experiences",
                "Rest in the perspective of the observer rather than the observed",
                "Practice being the sky that contains all weather of experience"
            ],
            duration_range=(10, 45),
            difficulty_level="intermediate",
            target_outcomes=[
                "Stronger connection with observing self",
                "Reduced identification with mental content",
                "Greater psychological flexibility",
                "Increased emotional regulation",
                "Enhanced sense of self-continuity"
            ],
            preparation_steps=[
                "Establish comfortable posture",
                "Set intention to connect with observing awareness",
                "Begin with present moment centering",
                "Cultivate curious, spacious attention"
            ],
            common_experiences=[
                "Moments of clear observer perspective",
                "Recognition of awareness as distinct from content",
                "Sense of spaciousness around experience",
                "Reduced reactivity to mental/emotional content",
                "Glimpses of unchanging awareness"
            ],
            troubleshooting_tips={
                MindfulnessBarrier.CONCEPTUAL_THINKING: [
                    "Return to direct experience of observing",
                    "Use metaphors like sky and weather",
                    "Practice with simple present moment awareness first"
                ],
                MindfulnessBarrier.DOUBT: [
                    "Remember this is practice, not performance",
                    "Trust natural capacity for awareness",
                    "Work with doubt as another observed experience"
                ]
            },
            integration_suggestions=[
                "Throughout day, ask 'Who is aware of this?'",
                "Use observer self during difficult emotions",
                "Practice during conflicts to maintain perspective",
                "Apply when feeling overwhelmed by experiences"
            ],
            contraindications=[
                "Severe depersonalization disorders",
                "Active psychosis",
                "When grounding is more needed than transcendent awareness"
            ],
            evidence_base="ACT self-as-context with supporting research"
        )
        
        practices["five_senses_grounding"] = MindfulnessPractice(
            practice_id="five_senses_grounding",
            name="Five Senses Grounding",
            mindfulness_type=MindfulnessType.CONTACT_WITH_NOW,
            practice_format=PracticeFormat.BRIEF_CENTERING,
            description="Using sensory awareness to anchor in present moment reality",
            core_instructions=[
                "Notice 5 things you can see in your environment",
                "Identify 4 things you can touch or feel",
                "Listen for 3 sounds in your surroundings",
                "Notice 2 scents or smells available",
                "Be aware of 1 taste in your mouth",
                "Spend a moment with each sense fully"
            ],
            duration_range=(3, 10),
            difficulty_level="beginner",
            target_outcomes=[
                "Rapid grounding in present moment",
                "Reduced anxiety and overwhelm",
                "Enhanced sensory awareness",
                "Improved emotional regulation",
                "Stronger connection to immediate reality"
            ],
            preparation_steps=[
                "No special preparation needed",
                "Can be done anywhere, anytime",
                "Set intention to ground in present moment",
                "Approach with curiosity about sensory experience"
            ],
            common_experiences=[
                "Immediate sense of grounding",
                "Surprise at richness of sensory environment",
                "Calming effect on nervous system",
                "Increased presence and clarity",
                "Reduced mental chatter"
            ],
            troubleshooting_tips={
                MindfulnessBarrier.IMPATIENCE: [
                    "Remember this takes only few minutes",
                    "Trust the natural grounding effect",
                    "Use when feeling scattered or anxious"
                ],
                MindfulnessBarrier.DOUBT: [
                    "Notice any immediate shifts in awareness",
                    "Trust simple effectiveness of sensory contact",
                    "Use as foundation for other practices"
                ]
            },
            integration_suggestions=[
                "Use during anxiety or panic episodes",
                "Practice during daily transitions",
                "Apply when feeling disconnected or spacey",
                "Use before important conversations or decisions"
            ],
            contraindications=[
                "Sensory processing disorders requiring adaptation",
                "When immediate action is needed for safety"
            ],
            evidence_base="Grounding techniques with trauma and anxiety research"
        )
        
        practices["mindful_breathing"] = MindfulnessPractice(
            practice_id="mindful_breathing",
            name="Mindful Breathing Practice",
            mindfulness_type=MindfulnessType.FLEXIBLE_ATTENTION,
            practice_format=PracticeFormat.FORMAL_MEDITATION,
            description="Using breath as anchor for mindful attention training",
            core_instructions=[
                "Find comfortable position and close eyes or soften gaze",
                "Begin noticing natural rhythm of your breathing",
                "Feel breath sensations without trying to control breathing",
                "When mind wanders, gently return attention to breath",
                "Notice in-breath, pause, out-breath, pause",
                "Use breath as anchor while staying open to full experience"
            ],
            duration_range=(5, 60),
            difficulty_level="beginner",
            target_outcomes=[
                "Improved attention regulation",
                "Enhanced present moment awareness",
                "Reduced stress and anxiety",
                "Greater emotional stability",
                "Increased body awareness"
            ],
            preparation_steps=[
                "Choose quiet location without distractions",
                "Sit with straight but relaxed posture",
                "Set timer for desired duration",
                "Set intention for mindful breathing practice"
            ],
            common_experiences=[
                "Initial struggle with attention wandering",
                "Gradual settling and calming",
                "Increased awareness of breath subtleties",
                "Moments of effortless attention",
                "Physical and mental relaxation"
            ],
            troubleshooting_tips={
                MindfulnessBarrier.RESTLESSNESS: [
                    "Start with shorter sessions",
                    "Allow movement if needed",
                    "Use restlessness as object of awareness"
                ],
                MindfulnessBarrier.DROWSINESS: [
                    "Sit more upright",
                    "Open eyes slightly",
                    "Practice when more alert"
                ]
            },
            integration_suggestions=[
                "Use mini breathing sessions throughout day",
                "Practice during stressful situations",
                "Apply before sleep for relaxation",
                "Use as foundation for other mindfulness practices"
            ],
            contraindications=[
                "Breathing-related trauma without support",
                "Severe respiratory conditions",
                "When breath focus increases anxiety"
            ],
            evidence_base="Mindfulness-based breathing with extensive research validation"
        )
        
        practices["open_awareness"] = MindfulnessPractice(
            practice_id="open_awareness",
            name="Open Awareness Practice",
            mindfulness_type=MindfulnessType.PANORAMIC,
            practice_format=PracticeFormat.FORMAL_MEDITATION,
            description="Cultivating spacious awareness that includes all experience",
            core_instructions=[
                "Sit with open, relaxed posture",
                "Instead of focusing on one thing, let awareness be spacious",
                "Notice whatever arises in awareness without selecting or rejecting",
                "Include thoughts, emotions, sensations, sounds equally",
                "Rest as awareness itself rather than focusing on objects of awareness",
                "Practice being the space in which all experience happens"
            ],
            duration_range=(15, 60),
            difficulty_level="advanced",
            target_outcomes=[
                "Expanded capacity for awareness",
                "Reduced reactivity to mental content",
                "Increased psychological flexibility",
                "Enhanced emotional regulation",
                "Greater acceptance of all experience"
            ],
            preparation_steps=[
                "Establish stable present moment awareness first",
                "Set intention for open, spacious practice",
                "Begin with grounding in body and breath",
                "Cultivate attitude of welcoming whatever arises"
            ],
            common_experiences=[
                "Sense of spaciousness and openness",
                "Natural arising and passing of experiences",
                "Reduced need to control or change anything",
                "Moments of effortless awareness",
                "Integration of all aspects of experience"
            ],
            troubleshooting_tips={
                MindfulnessBarrier.CONCEPTUAL_THINKING: [
                    "Return to simple sensing and feeling",
                    "Use body awareness as anchor",
                    "Practice shorter periods initially"
                ],
                MindfulnessBarrier.AVERSION: [
                    "Work with smaller difficult experiences first",
                    "Practice self-compassion",
                    "Return to present moment safety"
                ]
            },
            integration_suggestions=[
                "Use during overwhelming emotional experiences",
                "Practice in challenging interpersonal situations",
                "Apply when feeling contracted or defensive",
                "Use for integration after other practices"
            ],
            contraindications=[
                "Without foundation in basic mindfulness",
                "During acute psychological crisis",
                "If practice increases dissociation"
            ],
            evidence_base="Open monitoring meditation with contemplative research"
        )
        
        practices["everyday_mindfulness"] = MindfulnessPractice(
            practice_id="everyday_mindfulness",
            name="Everyday Mindfulness Integration",
            mindfulness_type=MindfulnessType.EVERYDAY_MINDFULNESS,
            practice_format=PracticeFormat.INFORMAL_PRACTICE,
            description="Bringing mindful awareness to routine daily activities",
            core_instructions=[
                "Choose regular daily activity (eating, walking, washing dishes)",
                "Bring full attention to the chosen activity",
                "Notice sensory details usually overlooked",
                "When mind wanders, gently return to activity",
                "Practice patience and curiosity with ordinary experiences",
                "Let activity become meditation in action"
            ],
            duration_range=(5, 60),
            difficulty_level="beginner",
            target_outcomes=[
                "Integration of mindfulness into daily life",
                "Increased appreciation for ordinary moments",
                "Reduced autopilot functioning",
                "Enhanced present moment living",
                "Greater life satisfaction"
            ],
            preparation_steps=[
                "Choose specific daily activity to practice with",
                "Set intention to practice mindfully",
                "Release agenda about efficiency or productivity",
                "Approach activity with beginner's mind"
            ],
            common_experiences=[
                "Surprise at richness of ordinary activities",
                "Increased satisfaction from simple tasks",
                "Recognition of how often we're on autopilot",
                "Moments of presence during routine activities",
                "Enhanced appreciation for daily life"
            ],
            troubleshooting_tips={
                MindfulnessBarrier.IMPATIENCE: [
                    "Start with very brief mindful moments",
                    "Choose enjoyable activities initially",
                    "Remember this enhances rather than slows life"
                ],
                MindfulnessBarrier.PERFECTIONISM: [
                    "Accept intermittent mindfulness as natural",
                    "Practice self-compassion with lapses",
                    "Focus on returning to awareness, not maintaining it"
                ]
            },
            integration_suggestions=[
                "Practice with one meal per day",
                "Use walking to/from locations mindfully",
                "Apply during household chores",
                "Practice during waiting periods"
            ],
            contraindications=[
                "Activities requiring safety attention",
                "When efficiency is critical"
            ],
            evidence_base="Informal mindfulness with daily life application research"
        )
        
        return practices
    
    def _initialize_guided_scripts(self) -> Dict[str, str]:
        
        return {
            "present_moment_awareness": """
                Let's begin by finding a comfortable position... 
                Close your eyes or soften your gaze...
                Take a moment to arrive here, right now...
                
                Notice that you are aware in this moment...
                Whatever you're experiencing right now is perfectly okay...
                This is what's here now...
                
                If your mind moves to the past or future, that's natural...
                Gently guide your attention back to now...
                What's happening in this very moment?
                
                Notice sounds around you... they're happening now...
                Feel your body where it's supported... this is now...
                Sense your breath as it is right now...
                
                Rest in this present moment... nowhere else to be...
                Let this moment be enough, just as it is...
            """,
            
            "observing_self": """
                Settle into a comfortable position...
                Begin by noticing that you are aware right now...
                
                Notice thoughts coming and going in your mind...
                Observe that you are the one watching these thoughts...
                You are not the thoughts... you are the awareness in which thoughts appear...
                
                Now notice any emotions present...
                See that you are the one observing these emotions...
                Emotions come and go, but the observer remains...
                
                Notice body sensations...
                See that you are aware of your body...
                The body changes, but the awareness observing remains constant...
                
                Rest as this observing awareness...
                You are the sky, and all experiences are like weather passing through...
                Stable, spacious awareness that holds all experience...
            """,
            
            "five_senses_grounding": """
                Let's ground ourselves in the present moment through our senses...
                
                First, look around and notice 5 things you can see...
                Really look at each one... notice colors, shapes, textures...
                
                Now notice 4 things you can touch or feel...
                Your feet on the floor... clothes on your skin...
                The temperature of the air... texture of your chair...
                
                Listen for 3 sounds in your environment...
                Maybe sounds from outside... inside... your own breathing...
                
                Notice 2 things you can smell...
                Perhaps subtle scents in the air around you...
                
                Finally, be aware of 1 taste in your mouth...
                Whatever taste is naturally present...
                
                Take a moment to appreciate this rich sensory world...
                You are here, now, grounded in immediate reality...
            """
        }
    
    def _initialize_assessment_tools(self) -> Dict[str, Any]:
        
        return {
            "mindfulness_domains": {
                "present_moment_awareness": [
                    "I notice when my mind wanders to past or future",
                    "I can bring my attention back to the present moment",
                    "I'm aware of what's happening right now",
                    "I spend time in the present rather than mental time travel"
                ],
                "observing_self": [
                    "I can step back and observe my thoughts",
                    "I notice I am the one watching my experiences",
                    "I can observe emotions without being overwhelmed",
                    "I experience myself as awareness, not just mental content"
                ],
                "non_judgmental_awareness": [
                    "I notice experiences without immediately judging them",
                    "I can observe difficult thoughts and feelings with kindness",
                    "I practice accepting what's here without needing to change it",
                    "I treat my inner experience with curiosity rather than criticism"
                ],
                "flexible_attention": [
                    "I can choose where to place my attention",
                    "I notice when I'm caught in mental loops",
                    "I can shift attention between different aspects of experience",
                    "I practice letting go of unhelpful mental focus"
                ]
            },
            
            "barrier_assessment": {
                MindfulnessBarrier.RESTLESSNESS: "I feel fidgety or unable to sit still during mindfulness",
                MindfulnessBarrier.DROWSINESS: "I feel sleepy or dull during mindfulness practice",
                MindfulnessBarrier.DOUBT: "I question whether mindfulness is helpful or working",
                MindfulnessBarrier.AVERSION: "I feel resistant to difficult experiences during practice",
                MindfulnessBarrier.IMPATIENCE: "I want mindfulness to work faster or be easier",
                MindfulnessBarrier.PERFECTIONISM: "I judge my mindfulness practice as not good enough"
            },
            
            "daily_integration_items": [
                "I use mindfulness during stressful situations",
                "I practice mindfulness during routine daily activities",
                "I remember to be mindful throughout my day",
                "Mindfulness helps me in my relationships",
                "I use mindfulness when experiencing difficult emotions"
            ]
        }
    
    def conduct_mindfulness_session(self, patient_id: str, practice_id: str, 
                                  session_duration: int) -> MindfulnessSession:
        
        session_id = f"{patient_id}_{practice_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        practice = self.mindfulness_practices.get(practice_id)
        if not practice:
            raise ValueError(f"Mindfulness practice {practice_id} not found")
        
        session = MindfulnessSession(
            session_id=session_id,
            patient_id=patient_id,
            practice_used=practice_id,
            session_duration=session_duration,
            attention_quality_start=AttentionQuality.WANDERING,
            attention_quality_end=AttentionQuality.FOCUSED,
            present_moment_awareness=0,
            non_judgmental_stance=0,
            observing_self_access=0,
            barriers_encountered=[],
            insights_gained=[],
            body_sensations_noticed=[],
            emotional_states_observed=[],
            thoughts_patterns_recognized=[],
            post_practice_mood=0,
            mindfulness_carryover=0,
            homework_connection="",
            therapist_observations="",
            patient_feedback=""
        )
        
        self._save_mindfulness_session(session)
        return session
    
    def assess_mindfulness_capacity(self, patient_id: str, 
                                  assessment_data: Dict[str, Any]) -> MindfulnessAssessment:
        
        assessment_id = f"{patient_id}_mindfulness_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        domain_scores = self._calculate_domain_scores(assessment_data)
        overall_score = sum(domain_scores.values()) / len(domain_scores)
        
        assessment = MindfulnessAssessment(
            assessment_id=assessment_id,
            patient_id=patient_id,
            assessment_date=datetime.now(),
            overall_mindfulness_level=int(overall_score),
            present_moment_awareness=domain_scores.get("present_moment_awareness", 0),
            observing_self_strength=domain_scores.get("observing_self", 0),
            non_judgmental_capacity=domain_scores.get("non_judgmental_awareness", 0),
            attention_regulation=domain_scores.get("flexible_attention", 0),
            emotional_awareness=assessment_data.get("emotional_awareness", 0),
            body_awareness=assessment_data.get("body_awareness", 0),
            thought_awareness=assessment_data.get("thought_awareness", 0),
            daily_life_integration=assessment_data.get("daily_integration_score", 0),
            primary_strengths=self._identify_mindfulness_strengths(domain_scores),
            development_areas=self._identify_development_areas(domain_scores),
            preferred_practices=assessment_data.get("preferred_practices", []),
            challenging_barriers=self._identify_challenging_barriers(assessment_data),
            recommended_interventions=self._recommend_mindfulness_interventions(domain_scores),
            practice_readiness=self._assess_practice_readiness(overall_score)
        )
        
        self._save_mindfulness_assessment(assessment)
        return assessment
    
    def _calculate_domain_scores(self, assessment_data: Dict[str, Any]) -> Dict[str, int]:
        
        domain_scores = {}
        
        for domain, items in self.assessment_tools["mindfulness_domains"].items():
            responses = assessment_data.get(f"{domain}_responses", [])
            if responses:
                domain_scores[domain] = int(sum(responses) / len(responses))
            else:
                domain_scores[domain] = 5  # Default neutral score
        
        return domain_scores
    
    def _identify_mindfulness_strengths(self, domain_scores: Dict[str, int]) -> List[str]:
        
        strengths = []
        
        for domain, score in domain_scores.items():
            if score >= 7:
                domain_name = domain.replace('_', ' ').title()
                strengths.append(f"Strong {domain_name}")
        
        return strengths
    
    def _identify_development_areas(self, domain_scores: Dict[str, int]) -> List[str]:
        
        development_areas = []
        
        for domain, score in domain_scores.items():
            if score <= 4:
                domain_name = domain.replace('_', ' ').title()
                development_areas.append(f"Develop {domain_name}")
        
        return development_areas
    
    def _identify_challenging_barriers(self, assessment_data: Dict[str, Any]) -> List[MindfulnessBarrier]:
        
        barriers = []
        
        for barrier, description in self.assessment_tools["barrier_assessment"].items():
            barrier_score = assessment_data.get(f"{barrier.value}_score", 0)
            if barrier_score >= 6:
                barriers.append(barrier)
        
        return barriers
    
    def _recommend_mindfulness_interventions(self, domain_scores: Dict[str, int]) -> List[str]:
        
        recommendations = []
        
        if domain_scores.get("present_moment_awareness", 0) <= 4:
            recommendations.append("present_moment_awareness")
        
        if domain_scores.get("observing_self", 0) <= 4:
            recommendations.append("observing_self")
        
        if domain_scores.get("flexible_attention", 0) <= 4:
            recommendations.append("mindful_breathing")
        
        if domain_scores.get("non_judgmental_awareness", 0) <= 4:
            recommendations.append("open_awareness")
        
        if not recommendations:
            recommendations.append("everyday_mindfulness")
        
        return recommendations[:3]
    
    def _assess_practice_readiness(self, overall_score: float) -> str:
        
        if overall_score >= 8:
            return "advanced_practice_ready"
        elif overall_score >= 6:
            return "intermediate_practice_ready"
        elif overall_score >= 4:
            return "basic_practice_ready"
        else:
            return "foundation_building_needed"
    
    def create_personalized_practice_plan(self, patient_id: str, 
                                        assessment: MindfulnessAssessment,
                                        preferences: Dict[str, Any]) -> Dict[str, Any]:
        
        plan = {
            "patient_id": patient_id,
            "assessment_date": assessment.assessment_date.isoformat(),
            "practice_readiness": assessment.practice_readiness,
            "recommended_practices": assessment.recommended_interventions,
            "weekly_schedule": {},
            "progression_pathway": [],
            "integration_strategies": [],
            "barrier_management": {},
            "success_metrics": []
        }
        
        available_time = preferences.get("available_time_per_day", 20)
        preferred_format = preferences.get("preferred_format", "mixed")
        stress_level = preferences.get("current_stress_level", "moderate")
        
        if assessment.practice_readiness == "foundation_building_needed":
            plan["weekly_schedule"] = {
                "formal_practice": "5-10 minutes daily",
                "informal_practice": "3 brief moments daily",
                "focus_practices": ["five_senses_grounding", "present_moment_awareness"]
            }
            plan["progression_pathway"] = [
                "Week 1-2: Establish basic present moment awareness",
                "Week 3-4: Add breath awareness practice",
                "Week 5-6: Introduce everyday mindfulness",
                "Week 7-8: Begin observing self practice"
            ]
        
        elif assessment.practice_readiness == "basic_practice_ready":
            plan["weekly_schedule"] = {
                "formal_practice": "10-20 minutes daily",
                "informal_practice": "Multiple daily applications",
                "focus_practices": ["mindful_breathing", "observing_self"]
            }
            plan["progression_pathway"] = [
                "Week 1-2: Strengthen attention regulation",
                "Week 3-4: Develop observing self capacity",
                "Week 5-6: Practice with difficult emotions",
                "Week 7-8: Integrate into challenging situations"
            ]
        
        elif assessment.practice_readiness == "intermediate_practice_ready":
            plan["weekly_schedule"] = {
                "formal_practice": "20-30 minutes daily",
                "informal_practice": "Consistent daily integration",
                "focus_practices": ["open_awareness", "everyday_mindfulness"]
            }
            plan["progression_pathway"] = [
                "Week 1-2: Expand awareness capacity",
                "Week 3-4: Work with complex emotional states",
                "Week 5-6: Develop advanced defusion skills",
                "Week 7-8: Cultivate wisdom and compassion"
            ]
        
        else:  # advanced_practice_ready
            plan["weekly_schedule"] = {
                "formal_practice": "30+ minutes daily or intensive periods",
                "informal_practice": "Seamless life integration",
                "focus_practices": ["open_awareness", "advanced_contemplative_practices"]
            }
            plan["progression_pathway"] = [
                "Maintain and deepen established practice",
                "Explore contemplative inquiry methods",
                "Develop teaching or mentoring capacity",
                "Integration with values and committed action"
            ]
        
        if preferred_format == "brief_sessions":
            plan["integration_strategies"].extend([
                "Use micro-practices throughout day",
                "Practice during transitions",
                "Apply mindfulness to routine activities"
            ])
        elif preferred_format == "longer_sessions":
            plan["integration_strategies"].extend([
                "Establish consistent formal practice time",
                "Use longer sessions for deeper development",
                "Balance formal practice with informal application"
            ])
        
        for barrier in assessment.challenging_barriers:
            if barrier == MindfulnessBarrier.RESTLESSNESS:
                plan["barrier_management"][barrier.value] = [
                    "Start with movement-based practices",
                    "Use shorter initial sessions",
                    "Practice self-compassion with fidgeting"
                ]
            elif barrier == MindfulnessBarrier.DROWSINESS:
                plan["barrier_management"][barrier.value] = [
                    "Practice when more alert",
                    "Sit with straighter posture",
                    "Use walking meditation"
                ]
            elif barrier == MindfulnessBarrier.DOUBT:
                plan["barrier_management"][barrier.value] = [
                    "Start with practical applications",
                    "Track concrete benefits",
                    "Work with doubt as object of mindfulness"
                ]
        
        plan["success_metrics"] = [
            "Increased present moment awareness in daily life",
            "Improved emotional regulation during stress",
            "Enhanced ability to step back from thoughts",
            "Greater life satisfaction and well-being",
            "Reduced reactivity to difficult experiences"
        ]
        
        return plan
    
    def track_mindfulness_progress(self, patient_id: str, weeks: int = 4) -> Dict[str, Any]:
        
        start_date = datetime.now() - timedelta(weeks=weeks)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT session_date, practice_used, session_duration, 
                       present_moment_awareness, non_judgmental_stance, observing_self_access,
                       post_practice_mood, mindfulness_carryover, barriers_encountered
                FROM mindfulness_sessions
                WHERE patient_id = ? AND session_date >= ?
                ORDER BY session_date
            """, (patient_id, start_date.isoformat()))
            
            sessions = cursor.fetchall()
        
        if not sessions:
            return {"error": "No mindfulness practice data found"}
        
        progress = {
            "patient_id": patient_id,
            "tracking_period_weeks": weeks,
            "total_sessions": len(sessions),
            "total_practice_time": 0,
            "average_session_duration": 0,
            "mindfulness_skill_trends": {},
            "practice_consistency": {},
            "barrier_patterns": {},
            "mood_improvements": [],
            "carryover_effects": [],
            "breakthrough_indicators": [],
            "recommendations": []
        }
        
        skill_scores = {
            "present_moment_awareness": [],
            "non_judgmental_stance": [],
            "observing_self_access": []
        }
        
        mood_scores = []
        carryover_scores = []
        all_barriers = []
        practice_frequency = {}
        
        for session_date, practice_used, duration, pma, njs, osa, mood, carryover, barriers_json in sessions:
            progress["total_practice_time"] += duration if duration else 0
            
            if pma is not None:
                skill_scores["present_moment_awareness"].append(pma)
            if njs is not None:
                skill_scores["non_judgmental_stance"].append(njs)
            if osa is not None:
                skill_scores["observing_self_access"].append(osa)
            
            if mood is not None:
                mood_scores.append(mood)
                progress["mood_improvements"].append({"date": session_date, "mood": mood})
            
            if carryover is not None:
                carryover_scores.append(carryover)
                progress["carryover_effects"].append({"date": session_date, "carryover": carryover})
            
            if barriers_json:
                barriers = json.loads(barriers_json)
                all_barriers.extend([b.value if hasattr(b, 'value') else str(b) for b in barriers])
            
            practice_frequency[practice_used] = practice_frequency.get(practice_used, 0) + 1
        
        if progress["total_sessions"] > 0:
            progress["average_session_duration"] = progress["total_practice_time"] / progress["total_sessions"]
        
        for skill, scores in skill_scores.items():
            if scores:
                progress["mindfulness_skill_trends"][skill] = {
                    "average": round(sum(scores) / len(scores), 2),
                    "trend": "improving" if len(scores) >= 3 and scores[-1] > scores[0] else "stable"
                }
        
        progress["practice_consistency"] = {
            "sessions_per_week": round(progress["total_sessions"] / weeks, 1),
            "most_used_practice": max(practice_frequency.items(), key=lambda x: x[1])[0] if practice_frequency else None,
            "practice_variety": len(practice_frequency)
        }
        
        barrier_frequency = {}
        for barrier in all_barriers:
            barrier_frequency[barrier] = barrier_frequency.get(barrier, 0) + 1
        
        progress["barrier_patterns"] = dict(sorted(barrier_frequency.items(), key=lambda x: x[1], reverse=True)[:5])
        
        if mood_scores and len(mood_scores) >= 3:
            recent_mood = sum(mood_scores[-3:]) / 3
            early_mood = sum(mood_scores[:3]) / 3
            if recent_mood > early_mood + 1:
                progress["breakthrough_indicators"].append("Consistent mood improvements after practice")
        
        if carryover_scores and sum(carryover_scores) / len(carryover_scores) >= 7:
            progress["breakthrough_indicators"].append("Good mindfulness carryover into daily life")
        
        if progress["practice_consistency"]["sessions_per_week"] >= 5:
            progress["breakthrough_indicators"].append("Excellent practice consistency")
        
        skill_improvement_count = sum(1 for trend in progress["mindfulness_skill_trends"].values() 
                                    if trend["trend"] == "improving")
        if skill_improvement_count >= 2:
            progress["breakthrough_indicators"].append("Multiple mindfulness skills improving")
        
        if progress["practice_consistency"]["sessions_per_week"] < 3:
            progress["recommendations"].append("Increase practice frequency for better benefits")
        
        most_common_barrier = max(barrier_frequency, key=barrier_frequency.get) if barrier_frequency else None
        if most_common_barrier:
            progress["recommendations"].append(f"Focus on addressing {most_common_barrier} barrier")
        
        if progress["average_session_duration"] < 10:
            progress["recommendations"].append("Consider gradually increasing session duration")
        
        return progress
    
    def generate_mindfulness_homework(self, practice_id: str, patient_level: str, 
                                    daily_time_available: int) -> Dict[str, Any]:
        
        practice = self.mindfulness_practices.get(practice_id)
        if not practice:
            raise ValueError(f"Practice {practice_id} not found")
        
        homework = {
            "practice_name": practice.name,
            "practice_type": practice.mindfulness_type.value,
            "patient_level": patient_level,
            "daily_time_commitment": daily_time_available,
            "formal_practice": {},
            "informal_practice": {},
            "weekly_goals": [],
            "practice_log": {},
            "troubleshooting_guide": {},
            "integration_suggestions": practice.integration_suggestions
        }
        
        if patient_level == "beginner":
            homework["formal_practice"] = {
                "frequency": "Daily",
                "duration": f"{min(daily_time_available, 10)} minutes",
                "instructions": practice.core_instructions[:3],
                "focus": "Establishing basic practice routine"
            }
            homework["informal_practice"] = {
                "frequency": "3 times daily",
                "duration": "1-2 minutes each",
                "activities": ["Brief centering before meals", "Mindful walking", "Present moment awareness"]
            }
            homework["weekly_goals"] = [
                "Complete 5 formal practice sessions",
                "Practice informal mindfulness 15 times",
                "Notice and record practice benefits"
            ]
        
        elif patient_level == "intermediate":
            homework["formal_practice"] = {
                "frequency": "Daily",
                "duration": f"{min(daily_time_available, 20)} minutes",
                "instructions": practice.core_instructions,
                "focus": "Deepening concentration and awareness"
            }
            homework["informal_practice"] = {
                "frequency": "Multiple times daily",
                "duration": "Variable",
                "activities": ["Mindful daily activities", "Difficult emotion practice", "Challenging situation awareness"]
            }
            homework["weekly_goals"] = [
                "Complete 6-7 formal practice sessions",
                "Apply mindfulness to 2 challenging situations",
                "Practice with difficult emotions when they arise"
            ]
        
        else:  # advanced
            homework["formal_practice"] = {
                "frequency": "Daily",
                "duration": f"{daily_time_available}+ minutes",
                "instructions": practice.core_instructions + ["Explore advanced variations"],
                "focus": "Refinement and integration"
            }
            homework["informal_practice"] = {
                "frequency": "Continuous integration",
                "duration": "Throughout day",
                "activities": ["Seamless daily integration", "Teaching others", "Creative applications"]
            }
            homework["weekly_goals"] = [
                "Maintain consistent advanced practice",
                "Explore new applications or variations",
                "Support others in their practice"
            ]
        
        homework["practice_log"] = {
            "date_time": "Record when you practiced",
            "duration": "How long you practiced",
            "quality_rating": "Rate practice quality 1-10",
            "insights": "Note any insights or observations",
            "challenges": "Record any difficulties encountered",
            "benefits": "Notice any immediate or lasting benefits"
        }
        
        for barrier, tips in practice.troubleshooting_tips.items():
            homework["troubleshooting_guide"][barrier.value] = tips
        
        return homework
    
    def create_guided_meditation_session(self, practice_id: str, duration: int, 
                                       patient_preferences: Dict[str, Any]) -> Dict[str, Any]:
        
        practice = self.mindfulness_practices.get(practice_id)
        if not practice:
            raise ValueError(f"Practice {practice_id} not found")
        
        base_script = self.guided_scripts.get(practice_id, "")
        
        session = {
            "practice_name": practice.name,
            "total_duration": duration,
            "session_structure": {},
            "guided_script": "",
            "timing_cues": [],
            "customizations": [],
            "post_practice_reflection": []
        }
        
        voice_preference = patient_preferences.get("voice_style", "calm")
        pace_preference = patient_preferences.get("pace", "moderate")
        imagery_preference = patient_preferences.get("imagery", "nature")
        
        opening_duration = min(3, duration // 6)
        main_duration = duration - opening_duration - 2
        closing_duration = 2
        
        session["session_structure"] = {
            "opening": f"{opening_duration} minutes - Settling and orientation",
            "main_practice": f"{main_duration} minutes - Core mindfulness practice",
            "closing": f"{closing_duration} minutes - Integration and transition"
        }
        
        session["guided_script"] = f"""
        OPENING ({opening_duration} minutes):
        Welcome to this {practice.name} practice...
        Take a moment to settle into your position...
        Set an intention for this practice session...
        
        MAIN PRACTICE ({main_duration} minutes):
        {base_script}
        
        CLOSING ({closing_duration} minutes):
        Begin to bring this practice to a close...
        Notice any changes from when you began...
        Set an intention to carry this awareness forward...
        When you're ready, gently open your eyes...
        """
        
        session["timing_cues"] = [
            f"{opening_duration} min: Transition to main practice",
            f"{opening_duration + main_duration//2} min: Halfway point, refocus",
            f"{opening_duration + main_duration} min: Begin closing"
        ]
        
        if voice_preference == "energizing":
            session["customizations"].append("Use slightly more energetic tone and pace")
        elif voice_preference == "soothing":
            session["customizations"].append("Use very gentle, soothing vocal quality")
        
        if pace_preference == "slow":
            session["customizations"].append("Allow extra silence between instructions")
        elif pace_preference == "brisk":
            session["customizations"].append("Maintain steady, efficient pacing")
        
        if imagery_preference == "nature":
            session["customizations"].append("Include natural imagery and metaphors")
        elif imagery_preference == "abstract":
            session["customizations"].append("Use spatial and geometric imagery")
        
        session["post_practice_reflection"] = [
            "How was your attention during this practice?",
            "What did you notice about your mind and body?",
            "Were there any particular insights or observations?",
            "How might you apply this awareness in your daily life?",
            "What would support your continued practice?"
        ]
        
        return session
    
    def evaluate_mindfulness_intervention_effectiveness(self, patient_id: str, 
                                                      intervention_start: datetime) -> Dict[str, Any]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT AVG(present_moment_awareness), AVG(non_judgmental_stance), 
                       AVG(observing_self_access), AVG(post_practice_mood),
                       AVG(mindfulness_carryover), COUNT(*)
                FROM mindfulness_sessions
                WHERE patient_id = ? AND session_date >= ?
            """, (patient_id, intervention_start.isoformat()))
            
            post_intervention = cursor.fetchone()
            
            cursor.execute("""
                SELECT AVG(present_moment_awareness), AVG(non_judgmental_stance), 
                       AVG(observing_self_access), AVG(post_practice_mood),
                       AVG(mindfulness_carryover), COUNT(*)
                FROM mindfulness_sessions
                WHERE patient_id = ? AND session_date < ?
            """, (patient_id, intervention_start.isoformat()))
            
            pre_intervention = cursor.fetchone()
        
        evaluation = {
            "patient_id": patient_id,
            "intervention_start": intervention_start.isoformat(),
            "pre_intervention_metrics": {},
            "post_intervention_metrics": {},
            "improvement_analysis": {},
            "effectiveness_rating": "unknown",
            "recommendations": []
        }
        
        if post_intervention and post_intervention[5] > 0:  # Has post-intervention data
            evaluation["post_intervention_metrics"] = {
                "present_moment_awareness": round(post_intervention[0], 2) if post_intervention[0] else 0,
                "non_judgmental_stance": round(post_intervention[1], 2) if post_intervention[1] else 0,
                "observing_self_access": round(post_intervention[2], 2) if post_intervention[2] else 0,
                "post_practice_mood": round(post_intervention[3], 2) if post_intervention[3] else 0,
                "mindfulness_carryover": round(post_intervention[4], 2) if post_intervention[4] else 0,
                "total_sessions": post_intervention[5]
            }
        
        if pre_intervention and pre_intervention[5] > 0:  # Has pre-intervention data
            evaluation["pre_intervention_metrics"] = {
                "present_moment_awareness": round(pre_intervention[0], 2) if pre_intervention[0] else 0,
                "non_judgmental_stance": round(pre_intervention[1], 2) if pre_intervention[1] else 0,
                "observing_self_access": round(pre_intervention[2], 2) if pre_intervention[2] else 0,
                "post_practice_mood": round(pre_intervention[3], 2) if pre_intervention[3] else 0,
                "mindfulness_carryover": round(pre_intervention[4], 2) if pre_intervention[4] else 0,
                "total_sessions": pre_intervention[5]
            }
            
            post_metrics = evaluation["post_intervention_metrics"]
            pre_metrics = evaluation["pre_intervention_metrics"]
            
            improvements = []
            for metric in ["present_moment_awareness", "non_judgmental_stance", "observing_self_access"]:
                if post_metrics.get(metric, 0) > pre_metrics.get(metric, 0):
                    improvement = post_metrics[metric] - pre_metrics[metric]
                    improvements.append(improvement)
                    evaluation["improvement_analysis"][metric] = round(improvement, 2)
            
            if improvements:
                avg_improvement = sum(improvements) / len(improvements)
                if avg_improvement >= 2.0:
                    evaluation["effectiveness_rating"] = "highly_effective"
                elif avg_improvement >= 1.0:
                    evaluation["effectiveness_rating"] = "moderately_effective"
                elif avg_improvement >= 0.5:
                    evaluation["effectiveness_rating"] = "somewhat_effective"
                else:
                    evaluation["effectiveness_rating"] = "minimally_effective"
        
        if evaluation["post_intervention_metrics"].get("total_sessions", 0) < 10:
            evaluation["recommendations"].append("Increase practice frequency for better outcomes")
        
        if evaluation["effectiveness_rating"] in ["minimally_effective", "somewhat_effective"]:
            evaluation["recommendations"].append("Consider modifying practice approach or addressing barriers")
        
        if evaluation["post_intervention_metrics"].get("mindfulness_carryover", 0) < 6:
            evaluation["recommendations"].append("Focus on informal practice and daily life integration")
        
        return evaluation
    
    def _save_mindfulness_session(self, session: MindfulnessSession):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO mindfulness_sessions
                (session_id, patient_id, practice_used, session_duration,
                 attention_quality_start, attention_quality_end, present_moment_awareness,
                 non_judgmental_stance, observing_self_access, barriers_encountered,
                 insights_gained, body_sensations_noticed, emotional_states_observed,
                 thoughts_patterns_recognized, post_practice_mood, mindfulness_carryover,
                 homework_connection, therapist_observations, patient_feedback, session_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id, session.patient_id, session.practice_used,
                session.session_duration, session.attention_quality_start.value,
                session.attention_quality_end.value, session.present_moment_awareness,
                session.non_judgmental_stance, session.observing_self_access,
                json.dumps([b.value for b in session.barriers_encountered]),
                json.dumps(session.insights_gained), json.dumps(session.body_sensations_noticed),
                json.dumps(session.emotional_states_observed), 
                json.dumps(session.thoughts_patterns_recognized),
                session.post_practice_mood, session.mindfulness_carryover,
                session.homework_connection, session.therapist_observations,
                session.patient_feedback, session.session_date.isoformat()
            ))
    
    def _save_mindfulness_assessment(self, assessment: MindfulnessAssessment):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO mindfulness_assessments
                (assessment_id, patient_id, assessment_date, overall_mindfulness_level,
                 present_moment_awareness, observing_self_strength, non_judgmental_capacity,
                 attention_regulation, emotional_awareness, body_awareness, thought_awareness,
                 daily_life_integration, primary_strengths, development_areas,
                 preferred_practices, challenging_barriers, recommended_interventions,
                 practice_readiness)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id, assessment.patient_id,
                assessment.assessment_date.isoformat(), assessment.overall_mindfulness_level,
                assessment.present_moment_awareness, assessment.observing_self_strength,
                assessment.non_judgmental_capacity, assessment.attention_regulation,
                assessment.emotional_awareness, assessment.body_awareness,
                assessment.thought_awareness, assessment.daily_life_integration,
                json.dumps(assessment.primary_strengths), json.dumps(assessment.development_areas),
                json.dumps(assessment.preferred_practices),
                json.dumps([b.value for b in assessment.challenging_barriers]),
                json.dumps(assessment.recommended_interventions), assessment.practice_readiness
            ))


if __name__ == "__main__":
    mindfulness_module = ACTMindfulnessPracticesModule()
    
    session = mindfulness_module.conduct_mindfulness_session(
        patient_id="patient_123",
        practice_id="present_moment_awareness",
        session_duration=15
    )
    
    print("=== MINDFULNESS SESSION ===")
    print(f"Session ID: {session.session_id}")
    print(f"Practice: {session.practice_used}")
    print(f"Duration: {session.session_duration} minutes")
    
    assessment_data = {
        "present_moment_awareness_responses": [6, 7, 5, 6],
        "observing_self_responses": [4, 5, 4, 3],
        "non_judgmental_awareness_responses": [7, 6, 7, 8],
        "flexible_attention_responses": [5, 6, 5, 5],
        "emotional_awareness": 6,
        "body_awareness": 7,
        "thought_awareness": 5,
        "daily_integration_score": 4,
        "restlessness_score": 7,
        "doubt_score": 5,
        "preferred_practices": ["mindful_breathing", "five_senses_grounding"]
    }
    
    assessment = mindfulness_module.assess_mindfulness_capacity("patient_123", assessment_data)
    print(f"\n=== MINDFULNESS ASSESSMENT ===")
    print(f"Overall Level: {assessment.overall_mindfulness_level}/10")
    print(f"Practice Readiness: {assessment.practice_readiness}")
    print(f"Strengths: {assessment.primary_strengths}")
    print(f"Development Areas: {assessment.development_areas}")
    print(f"Recommended Interventions: {assessment.recommended_interventions}")
    
    preferences = {
        "available_time_per_day": 15,
        "preferred_format": "brief_sessions",
        "current_stress_level": "high"
    }
    
    practice_plan = mindfulness_module.create_personalized_practice_plan("patient_123", assessment, preferences)
    print(f"\n=== PERSONALIZED PRACTICE PLAN ===")
    print(f"Practice Readiness: {practice_plan['practice_readiness']}")
    print(f"Weekly Schedule: {practice_plan['weekly_schedule']}")
    print(f"Progression Pathway: {practice_plan['progression_pathway'][:2]}")
    
    homework = mindfulness_module.generate_mindfulness_homework("present_moment_awareness", "beginner", 10)
    print(f"\n=== HOMEWORK ASSIGNMENT ===")
    print(f"Practice: {homework['practice_name']}")
    print(f"Formal Practice: {homework['formal_practice']['frequency']} for {homework['formal_practice']['duration']}")
    print(f"Weekly Goals: {homework['weekly_goals']}")
    
    meditation_prefs = {
        "voice_style": "calm",
        "pace": "slow",
        "imagery": "nature"
    }
    
    guided_session = mindfulness_module.create_guided_meditation_session("present_moment_awareness", 20, meditation_prefs)
    print(f"\n=== GUIDED MEDITATION SESSION ===")
    print(f"Practice: {guided_session['practice_name']}")
    print(f"Duration: {guided_session['total_duration']} minutes")
    print(f"Structure: {guided_session['session_structure']}")
    print(f"Customizations: {guided_session['customizations']}")
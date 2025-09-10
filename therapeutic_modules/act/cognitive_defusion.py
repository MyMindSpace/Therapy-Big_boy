from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import sqlite3
import json


class DefusionTechnique(Enum):
    MENTAL_DISTANCING = "mental_distancing"
    LINGUISTIC_DEFUSION = "linguistic_defusion"
    METAPHORICAL_DEFUSION = "metaphorical_defusion"
    EXPERIENTIAL_DEFUSION = "experiential_defusion"
    MINDFUL_OBSERVATION = "mindful_observation"
    PLAYFUL_DEFUSION = "playful_defusion"
    CONTEXTUAL_DEFUSION = "contextual_defusion"


class FusionLevel(Enum):
    COMPLETE_FUSION = "complete_fusion"
    HIGH_FUSION = "high_fusion"
    MODERATE_FUSION = "moderate_fusion"
    MILD_FUSION = "mild_fusion"
    DEFUSED = "defused"
    HIGHLY_DEFUSED = "highly_defused"


class ThoughtType(Enum):
    SELF_CRITICAL = "self_critical"
    CATASTROPHIC = "catastrophic"
    RUMINATION = "rumination"
    WORRY = "worry"
    PERFECTIONIST = "perfectionist"
    COMPARISON = "comparison"
    SHOULDS = "shoulds"
    HELPLESSNESS = "helplessness"
    FUTURE_FOCUSED = "future_focused"
    PAST_FOCUSED = "past_focused"


class DefusionBarrier(Enum):
    THOUGHT_BELIEVABILITY = "thought_believability"
    EMOTIONAL_INTENSITY = "emotional_intensity"
    HABITUAL_PATTERNS = "habitual_patterns"
    LITERALNESS = "literalness"
    IDENTITY_FUSION = "identity_fusion"
    CONTROL_AGENDA = "control_agenda"


@dataclass
class DefusionTechnique:
    technique_id: str
    name: str
    technique_type: DefusionTechnique
    description: str
    core_principles: List[str]
    step_by_step_instructions: List[str]
    example_applications: List[str]
    target_thought_types: List[ThoughtType]
    difficulty_level: str
    session_duration: int
    homework_adaptations: List[str]
    common_obstacles: List[DefusionBarrier]
    success_indicators: List[str]
    contraindications: List[str]
    evidence_base: str


@dataclass
class DefusionPractice:
    practice_id: str
    patient_id: str
    session_id: str
    technique_used: str
    target_thought: str
    thought_type: ThoughtType
    pre_fusion_rating: int
    post_fusion_rating: int
    believability_change: int
    emotional_impact_change: int
    behavioral_influence_change: int
    barriers_encountered: List[DefusionBarrier]
    breakthrough_moments: List[str]
    insights_gained: List[str]
    technique_effectiveness: int
    patient_feedback: str
    homework_application: str
    therapist_observations: str
    practice_date: datetime = field(default_factory=datetime.now)


@dataclass
class DefusionAssessment:
    assessment_id: str
    patient_id: str
    assessment_date: datetime
    overall_fusion_level: FusionLevel
    thought_type_fusion: Dict[ThoughtType, FusionLevel]
    primary_fusion_patterns: List[str]
    defusion_strengths: List[str]
    challenging_thought_types: List[ThoughtType]
    recommended_techniques: List[str]
    fusion_triggers: List[str]
    progress_indicators: List[str]
    intervention_priorities: List[str]


class CognitiveDefusionModule:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.defusion_techniques = self._initialize_defusion_techniques()
        self.thought_pattern_library = self._initialize_thought_patterns()
        self.assessment_tools = self._initialize_assessment_tools()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS defusion_practices (
                    practice_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    technique_used TEXT NOT NULL,
                    target_thought TEXT,
                    thought_type TEXT,
                    pre_fusion_rating INTEGER,
                    post_fusion_rating INTEGER,
                    believability_change INTEGER,
                    emotional_impact_change INTEGER,
                    behavioral_influence_change INTEGER,
                    barriers_encountered TEXT,
                    breakthrough_moments TEXT,
                    insights_gained TEXT,
                    technique_effectiveness INTEGER,
                    patient_feedback TEXT,
                    homework_application TEXT,
                    therapist_observations TEXT,
                    practice_date TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS defusion_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    assessment_date TEXT,
                    overall_fusion_level TEXT,
                    thought_type_fusion TEXT,
                    primary_fusion_patterns TEXT,
                    defusion_strengths TEXT,
                    challenging_thought_types TEXT,
                    recommended_techniques TEXT,
                    fusion_triggers TEXT,
                    progress_indicators TEXT,
                    intervention_priorities TEXT
                )
            """)
    
    def _initialize_defusion_techniques(self) -> Dict[str, DefusionTechnique]:
        
        techniques = {}
        
        techniques["observer_self"] = DefusionTechnique(
            technique_id="observer_self",
            name="Observer Self Technique",
            technique_type=DefusionTechnique.MENTAL_DISTANCING,
            description="Creating distance by observing thoughts from the perspective of the observing self",
            core_principles=[
                "You are not your thoughts - you are the one observing them",
                "Thoughts are mental events occurring in awareness",
                "The observer self is stable while thoughts change",
                "Distance creates choice and flexibility",
                "Awareness can hold any thought without being defined by it"
            ],
            step_by_step_instructions=[
                "Notice the thought you're having",
                "Step back mentally and observe the thought",
                "Say 'I'm having the thought that...' instead of believing it directly",
                "Notice that you are the one observing this thought",
                "Recognize that thoughts come and go while you remain",
                "Choose your response from this observing perspective"
            ],
            example_applications=[
                "'I'm worthless' becomes 'I'm having the thought that I'm worthless'",
                "'This will be a disaster' becomes 'I notice my mind predicting disaster'",
                "'I can't handle this' becomes 'I'm having the thought that I can't handle this'"
            ],
            target_thought_types=[ThoughtType.SELF_CRITICAL, ThoughtType.CATASTROPHIC, ThoughtType.HELPLESSNESS],
            difficulty_level="beginner",
            session_duration=15,
            homework_adaptations=[
                "Practice observer phrases throughout the day",
                "Set reminders to notice when fused with thoughts",
                "Use observer self during daily challenges"
            ],
            common_obstacles=[
                DefusionBarrier.HABITUAL_PATTERNS,
                DefusionBarrier.EMOTIONAL_INTENSITY,
                DefusionBarrier.LITERALNESS
            ],
            success_indicators=[
                "Increased awareness of thoughts as thoughts",
                "Reduced emotional reactivity to negative thoughts",
                "Greater sense of choice in response to thoughts",
                "Improved ability to step back from mental content"
            ],
            contraindications=[
                "Active psychosis",
                "Severe dissociative episodes",
                "When immediate problem-solving is needed"
            ],
            evidence_base="Core ACT technique with extensive research support"
        )
        
        techniques["silly_voices"] = DefusionTechnique(
            technique_id="silly_voices",
            name="Silly Voices Technique",
            technique_type=DefusionTechnique.PLAYFUL_DEFUSION,
            description="Reducing thought impact by repeating thoughts in silly or cartoon voices",
            core_principles=[
                "Changing the form of thoughts changes their impact",
                "Humor and playfulness reduce thought fusion",
                "Serious thoughts lose power when delivered playfully",
                "The content stays the same but the context changes",
                "Laughter creates psychological distance"
            ],
            step_by_step_instructions=[
                "Identify the troubling thought",
                "Choose a silly voice (cartoon character, accent, singing)",
                "Repeat the thought exactly in the silly voice",
                "Notice how the thought feels different",
                "Experiment with different voices for the same thought",
                "Use the technique when the thought returns"
            ],
            example_applications=[
                "Self-critical thoughts in Elmer Fudd voice",
                "Worry thoughts sung as opera",
                "Catastrophic thoughts in Mickey Mouse voice",
                "Perfectionist thoughts in robot voice"
            ],
            target_thought_types=[ThoughtType.SELF_CRITICAL, ThoughtType.PERFECTIONIST, ThoughtType.WORRY],
            difficulty_level="beginner",
            session_duration=10,
            homework_adaptations=[
                "Practice with different cartoon voices",
                "Use during low-level thought intrusions",
                "Combine with humor and lightness"
            ],
            common_obstacles=[
                DefusionBarrier.LITERALNESS,
                DefusionBarrier.THOUGHT_BELIEVABILITY,
                DefusionBarrier.EMOTIONAL_INTENSITY
            ],
            success_indicators=[
                "Increased lightness around difficult thoughts",
                "Reduced seriousness and weight of thoughts",
                "Spontaneous humor when thoughts arise",
                "Decreased thought believability"
            ],
            contraindications=[
                "When patient finds technique invalidating",
                "During acute grief or trauma processing",
                "If humor is used defensively to avoid emotions"
            ],
            evidence_base="Supported by ACT research on linguistic defusion"
        )
        
        techniques["leaves_on_stream"] = DefusionTechnique(
            technique_id="leaves_on_stream",
            name="Leaves on a Stream",
            technique_type=DefusionTechnique.METAPHORICAL_DEFUSION,
            description="Visualizing thoughts as leaves floating down a stream to create distance",
            core_principles=[
                "Thoughts flow naturally like water when not resisted",
                "Observing thoughts without engaging allows them to pass",
                "Mental content is temporary and changeable",
                "Awareness is like the banks of the stream - stable and enduring",
                "Letting go is more effective than pushing away"
            ],
            step_by_step_instructions=[
                "Sit comfortably and close your eyes",
                "Imagine sitting by a gently flowing stream",
                "See leaves floating down the stream",
                "When thoughts arise, place them on leaves",
                "Watch the leaves carrying thoughts downstream",
                "If you get caught up in a thought, gently return to watching"
            ],
            example_applications=[
                "Worry thoughts placed on autumn leaves",
                "Self-critical thoughts on lily pads",
                "Planning thoughts on floating logs",
                "Memory thoughts on flower petals"
            ],
            target_thought_types=[ThoughtType.RUMINATION, ThoughtType.WORRY, ThoughtType.PAST_FOCUSED],
            difficulty_level="intermediate",
            session_duration=20,
            homework_adaptations=[
                "Practice visualization for 10 minutes daily",
                "Use abbreviated version during the day",
                "Apply to specific recurring thought patterns"
            ],
            common_obstacles=[
                DefusionBarrier.HABITUAL_PATTERNS,
                DefusionBarrier.CONTROL_AGENDA,
                DefusionBarrier.EMOTIONAL_INTENSITY
            ],
            success_indicators=[
                "Improved ability to let thoughts pass",
                "Reduced rumination and mental looping",
                "Increased peace with mental activity",
                "Greater mental flexibility and flow"
            ],
            contraindications=[
                "Severe concentration difficulties",
                "Active visual hallucinations",
                "When grounding is needed more than defusion"
            ],
            evidence_base="Classic ACT metaphor with research validation"
        )
        
        techniques["thanking_mind"] = DefusionTechnique(
            technique_id="thanking_mind",
            name="Thanking Your Mind",
            technique_type=DefusionTechnique.LINGUISTIC_DEFUSION,
            description="Acknowledging thoughts by thanking the mind for its input without buying into content",
            core_principles=[
                "The mind is trying to help, even with unhelpful thoughts",
                "Gratitude creates gentle distance from thoughts",
                "Acknowledging without agreeing reduces internal conflict",
                "The mind's job is to think - we can appreciate without following",
                "Kindness to mental processes reduces struggle"
            ],
            step_by_step_instructions=[
                "Notice when a difficult thought arises",
                "Recognize this as your mind doing its job",
                "Say 'Thank you, mind, for that thought'",
                "Add specificity: 'Thank you for trying to protect me'",
                "Return attention to what you're doing",
                "Use with consistency and genuine appreciation"
            ],
            example_applications=[
                "Thank you, mind, for worrying about tomorrow",
                "Thank you for reminding me of past mistakes",
                "Thank you for trying to keep me safe with anxiety",
                "Thank you for the comparison thoughts"
            ],
            target_thought_types=[ThoughtType.WORRY, ThoughtType.COMPARISON, ThoughtType.FUTURE_FOCUSED],
            difficulty_level="beginner",
            session_duration=10,
            homework_adaptations=[
                "Use throughout the day with any intrusive thoughts",
                "Practice genuine gratitude toward mental activity",
                "Combine with mindful awareness"
            ],
            common_obstacles=[
                DefusionBarrier.IDENTITY_FUSION,
                DefusionBarrier.CONTROL_AGENDA,
                DefusionBarrier.HABITUAL_PATTERNS
            ],
            success_indicators=[
                "Reduced fighting with thoughts",
                "Increased gentleness toward mental activity",
                "Better relationship with mind's activity",
                "Decreased thought suppression efforts"
            ],
            contraindications=[
                "When validation feels inauthentic",
                "During severe self-attack episodes",
                "If technique increases thought frequency"
            ],
            evidence_base="ACT linguistic defusion with mindfulness elements"
        )
        
        techniques["word_repetition"] = DefusionTechnique(
            technique_id="word_repetition",
            name="Word Repetition Exercise",
            technique_type=DefusionTechnique.LINGUISTIC_DEFUSION,
            description="Repeating key words from thoughts rapidly to reduce their literal meaning",
            core_principles=[
                "Words lose meaning when repeated rapidly",
                "Semantic satiation reduces word impact",
                "Separating sound from meaning creates distance",
                "Experiencing words as sounds rather than facts",
                "Linguistic form affects psychological impact"
            ],
            step_by_step_instructions=[
                "Identify the key word in the troubling thought",
                "Say the word out loud rapidly for 30 seconds",
                "Notice how the word changes as you repeat it",
                "Observe the shift from meaning to sound",
                "Return to the original thought and notice differences",
                "Use with specific trigger words"
            ],
            example_applications=[
                "Repeat 'failure' until it becomes just sounds",
                "Say 'stupid' rapidly until meaning dissolves",
                "Repeat 'worthless' until it's just noise",
                "Practice with 'can't' until it loses impact"
            ],
            target_thought_types=[ThoughtType.SELF_CRITICAL, ThoughtType.HELPLESSNESS, ThoughtType.SHOULDS],
            difficulty_level="beginner",
            session_duration=5,
            homework_adaptations=[
                "Practice with trigger words at home",
                "Use when specific words cause distress",
                "Apply to self-talk vocabulary"
            ],
            common_obstacles=[
                DefusionBarrier.LITERALNESS,
                DefusionBarrier.THOUGHT_BELIEVABILITY,
                DefusionBarrier.HABITUAL_PATTERNS
            ],
            success_indicators=[
                "Reduced impact of specific trigger words",
                "Increased awareness of language effects",
                "Less literalness with self-talk",
                "Improved word-meaning flexibility"
            ],
            contraindications=[
                "In public settings where inappropriate",
                "When words are connected to trauma",
                "If technique increases obsessive patterns"
            ],
            evidence_base="Linguistic defusion research supporting semantic satiation"
        )
        
        techniques["thought_labeling"] = DefusionTechnique(
            technique_id="thought_labeling",
            name="Thought Labeling and Categorizing",
            technique_type=DefusionTechnique.MINDFUL_OBSERVATION,
            description="Creating distance by labeling thoughts as mental events rather than facts",
            core_principles=[
                "Labeling creates observer perspective",
                "Categories reduce personal identification",
                "Mental noting increases awareness",
                "Classification reduces thought fusion",
                "Objectivity emerges through labeling"
            ],
            step_by_step_instructions=[
                "Notice when thoughts arise",
                "Label the thought type: 'planning', 'worrying', 'remembering'",
                "Add 'thought' to the label: 'planning thought', 'worry thought'",
                "Observe the thought without engaging content",
                "Return attention to present moment activity",
                "Practice consistent mental noting"
            ],
            example_applications=[
                "Label self-criticism as 'judging thoughts'",
                "Call catastrophizing 'disaster thoughts'",
                "Name rumination 'reviewing thoughts'",
                "Identify perfectionism as 'standards thoughts'"
            ],
            target_thought_types=[ThoughtType.RUMINATION, ThoughtType.PERFECTIONIST, ThoughtType.CATASTROPHIC],
            difficulty_level="intermediate",
            session_duration=15,
            homework_adaptations=[
                "Practice mental noting throughout day",
                "Keep thought category journal",
                "Use during meditation practice"
            ],
            common_obstacles=[
                DefusionBarrier.HABITUAL_PATTERNS,
                DefusionBarrier.EMOTIONAL_INTENSITY,
                DefusionBarrier.IDENTITY_FUSION
            ],
            success_indicators=[
                "Increased thought awareness",
                "Reduced personal identification with thoughts",
                "Better recognition of thought patterns",
                "Improved metacognitive skills"
            ],
            contraindications=[
                "When increased self-monitoring becomes obsessive",
                "During dissociative episodes",
                "If labeling increases rumination"
            ],
            evidence_base="Mindfulness-based defusion with ACT principles"
        )
        
        techniques["physicalizing_thoughts"] = DefusionTechnique(
            technique_id="physicalizing_thoughts",
            name="Physicalizing Thoughts",
            technique_type=DefusionTechnique.EXPERIENTIAL_DEFUSION,
            description="Giving thoughts physical characteristics to reduce their psychological impact",
            core_principles=[
                "Making abstract thoughts concrete reduces their power",
                "Physical representation creates distance",
                "Embodied metaphors change thought relationships",
                "Visualization alters thought impact",
                "Creative representation increases flexibility"
            ],
            step_by_step_instructions=[
                "Identify the troubling thought",
                "Imagine the thought having physical characteristics",
                "Give it shape, size, color, texture, weight",
                "Visualize holding or interacting with this object",
                "Experiment with changing its physical properties",
                "Notice how the thought feels different as an object"
            ],
            example_applications=[
                "Anxiety thoughts as gray clouds that can drift away",
                "Self-criticism as a heavy, dark rock to set down",
                "Worry thoughts as buzzing bees you can observe",
                "Perfectionist thoughts as rigid metal boxes you can soften"
            ],
            target_thought_types=[ThoughtType.SELF_CRITICAL, ThoughtType.WORRY, ThoughtType.PERFECTIONIST],
            difficulty_level="intermediate",
            session_duration=20,
            homework_adaptations=[
                "Practice visualization with recurring thoughts",
                "Create physical representations (drawings, sculptures)",
                "Use during emotional intensity"
            ],
            common_obstacles=[
                DefusionBarrier.LITERALNESS,
                DefusionBarrier.EMOTIONAL_INTENSITY,
                DefusionBarrier.IDENTITY_FUSION
            ],
            success_indicators=[
                "Increased creativity with thought content",
                "Reduced seriousness about thoughts",
                "Better ability to manipulate thought impact",
                "Enhanced psychological flexibility"
            ],
            contraindications=[
                "Limited visualization ability",
                "When concretizing increases distress",
                "During acute psychotic episodes"
            ],
            evidence_base="Creative arts therapy integrated with ACT defusion"
        )
        
        return techniques
    
    def _initialize_thought_patterns(self) -> Dict[ThoughtType, Dict[str, Any]]:
        
        return {
            ThoughtType.SELF_CRITICAL: {
                "common_patterns": [
                    "I'm not good enough",
                    "I'm a failure",
                    "I should be better",
                    "Everyone else is more capable"
                ],
                "fusion_indicators": [
                    "Taking self-criticism as absolute truth",
                    "Making global self-assessments",
                    "Comparing self harshly to others",
                    "Feeling worthless based on thoughts"
                ],
                "best_techniques": ["observer_self", "silly_voices", "thanking_mind"]
            },
            
            ThoughtType.CATASTROPHIC: {
                "common_patterns": [
                    "This will be a disaster",
                    "Everything will go wrong",
                    "I can't handle what's coming",
                    "The worst will definitely happen"
                ],
                "fusion_indicators": [
                    "Believing predictions are certainties",
                    "Planning based on worst-case scenarios",
                    "Feeling overwhelmed by imagined futures",
                    "Avoiding situations based on predictions"
                ],
                "best_techniques": ["observer_self", "leaves_on_stream", "physicalizing_thoughts"]
            },
            
            ThoughtType.RUMINATION: {
                "common_patterns": [
                    "Why did this happen?",
                    "I should have done differently",
                    "What if I had chosen otherwise?",
                    "I keep thinking about this over and over"
                ],
                "fusion_indicators": [
                    "Getting stuck in mental loops",
                    "Believing analysis will solve past events",
                    "Unable to let go of past situations",
                    "Feeling compelled to figure everything out"
                ],
                "best_techniques": ["leaves_on_stream", "thought_labeling", "thanking_mind"]
            },
            
            ThoughtType.WORRY: {
                "common_patterns": [
                    "What if something bad happens?",
                    "I need to figure this out now",
                    "I should be prepared for everything",
                    "Something will definitely go wrong"
                ],
                "fusion_indicators": [
                    "Treating worry as problem-solving",
                    "Believing worry prevents bad outcomes",
                    "Feeling anxious about uncertain futures",
                    "Compulsive mental planning"
                ],
                "best_techniques": ["thanking_mind", "physicalizing_thoughts", "word_repetition"]
            },
            
            ThoughtType.PERFECTIONIST: {
                "common_patterns": [
                    "This has to be perfect",
                    "Anything less than perfect is failure",
                    "I must not make any mistakes",
                    "Others expect perfection from me"
                ],
                "fusion_indicators": [
                    "Setting impossible standards",
                    "All-or-nothing thinking about performance",
                    "Paralyzing fear of making mistakes",
                    "Self-worth tied to perfect performance"
                ],
                "best_techniques": ["silly_voices", "thought_labeling", "observer_self"]
            }
        }
    
    def _initialize_assessment_tools(self) -> Dict[str, Any]:
        
        return {
            "fusion_indicators": {
                "thought_believability": "How much do you believe your thoughts are true (1-10)?",
                "emotional_impact": "How much do thoughts affect your emotions (1-10)?",
                "behavioral_influence": "How much do thoughts control your actions (1-10)?",
                "thought_frequency": "How often do problematic thoughts occur?",
                "rumination_time": "How long do you spend thinking about thoughts?"
            },
            
            "defusion_skills": {
                "observer_awareness": "Can you step back and observe your thoughts?",
                "thought_labeling": "Can you notice thoughts as mental events?",
                "linguistic_flexibility": "Can you play with the form of thoughts?",
                "metaphorical_thinking": "Can you use images or metaphors with thoughts?",
                "humor_application": "Can you use lightness with difficult thoughts?"
            },
            
            "fusion_assessment_items": [
                "My thoughts are always accurate reflections of reality",
                "I am my thoughts - they define who I am",
                "If I think something bad will happen, it probably will",
                "I must pay attention to all my thoughts",
                "Fighting my thoughts is the best way to deal with them",
                "My thoughts control how I feel and act",
                "I need to believe my thoughts to function properly"
            ]
        }
    
    def conduct_defusion_practice(self, patient_id: str, session_id: str, 
                                technique_id: str, target_thought: str) -> DefusionPractice:
        
        practice_id = f"{patient_id}_{technique_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        technique = self.defusion_techniques.get(technique_id)
        if not technique:
            raise ValueError(f"Defusion technique {technique_id} not found")
        
        thought_type = self._classify_thought_type(target_thought)
        
        practice = DefusionPractice(
            practice_id=practice_id,
            patient_id=patient_id,
            session_id=session_id,
            technique_used=technique_id,
            target_thought=target_thought,
            thought_type=thought_type,
            pre_fusion_rating=0,
            post_fusion_rating=0,
            believability_change=0,
            emotional_impact_change=0,
            behavioral_influence_change=0,
            barriers_encountered=[],
            breakthrough_moments=[],
            insights_gained=[],
            technique_effectiveness=0,
            patient_feedback="",
            homework_application="",
            therapist_observations=""
        )
        
        self._save_defusion_practice(practice)
        return practice
    
    def _classify_thought_type(self, thought: str) -> ThoughtType:
        
        thought_lower = thought.lower()
        
        self_critical_keywords = ["worthless", "failure", "stupid", "not good enough", "can't do anything"]
        catastrophic_keywords = ["disaster", "terrible", "worst", "horrible", "awful"]
        worry_keywords = ["what if", "might happen", "could go wrong", "worried about"]
        perfectionist_keywords = ["perfect", "must", "should", "have to", "need to"]
        rumination_keywords = ["why did", "should have", "if only", "keep thinking"]
        
        if any(keyword in thought_lower for keyword in self_critical_keywords):
            return ThoughtType.SELF_CRITICAL
        elif any(keyword in thought_lower for keyword in catastrophic_keywords):
            return ThoughtType.CATASTROPHIC
        elif any(keyword in thought_lower for keyword in worry_keywords):
            return ThoughtType.WORRY
        elif any(keyword in thought_lower for keyword in perfectionist_keywords):
            return ThoughtType.PERFECTIONIST
        elif any(keyword in thought_lower for keyword in rumination_keywords):
            return ThoughtType.RUMINATION
        else:
            return ThoughtType.SELF_CRITICAL  # Default classification
    
    def assess_fusion_levels(self, patient_id: str, assessment_data: Dict[str, Any]) -> DefusionAssessment:
        
        assessment_id = f"{patient_id}_defusion_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        overall_fusion = self._calculate_overall_fusion(assessment_data)
        thought_type_fusion = self._assess_thought_type_fusion(assessment_data)
        primary_patterns = self._identify_fusion_patterns(assessment_data)
        challenging_types = self._identify_challenging_thought_types(thought_type_fusion)
        recommended_techniques = self._recommend_techniques(challenging_types, primary_patterns)
        
        assessment = DefusionAssessment(
            assessment_id=assessment_id,
            patient_id=patient_id,
            assessment_date=datetime.now(),
            overall_fusion_level=overall_fusion,
            thought_type_fusion=thought_type_fusion,
            primary_fusion_patterns=primary_patterns,
            defusion_strengths=self._identify_defusion_strengths(assessment_data),
            challenging_thought_types=challenging_types,
            recommended_techniques=recommended_techniques,
            fusion_triggers=assessment_data.get("fusion_triggers", []),
            progress_indicators=self._generate_progress_indicators(overall_fusion),
            intervention_priorities=self._determine_intervention_priorities(challenging_types)
        )
        
        self._save_defusion_assessment(assessment)
        return assessment
    
    def _calculate_overall_fusion(self, assessment_data: Dict[str, Any]) -> FusionLevel:
        
        believability = assessment_data.get("thought_believability", 5)
        emotional_impact = assessment_data.get("emotional_impact", 5)
        behavioral_influence = assessment_data.get("behavioral_influence", 5)
        
        avg_fusion = (believability + emotional_impact + behavioral_influence) / 3
        
        if avg_fusion >= 9:
            return FusionLevel.COMPLETE_FUSION
        elif avg_fusion >= 7:
            return FusionLevel.HIGH_FUSION
        elif avg_fusion >= 5:
            return FusionLevel.MODERATE_FUSION
        elif avg_fusion >= 3:
            return FusionLevel.MILD_FUSION
        elif avg_fusion >= 1:
            return FusionLevel.DEFUSED
        else:
            return FusionLevel.HIGHLY_DEFUSED
    
    def _assess_thought_type_fusion(self, assessment_data: Dict[str, Any]) -> Dict[ThoughtType, FusionLevel]:
        
        thought_type_fusion = {}
        
        for thought_type in ThoughtType:
            type_score = assessment_data.get(f"{thought_type.value}_fusion_score", 5)
            
            if type_score >= 8:
                thought_type_fusion[thought_type] = FusionLevel.HIGH_FUSION
            elif type_score >= 6:
                thought_type_fusion[thought_type] = FusionLevel.MODERATE_FUSION
            elif type_score >= 4:
                thought_type_fusion[thought_type] = FusionLevel.MILD_FUSION
            else:
                thought_type_fusion[thought_type] = FusionLevel.DEFUSED
        
        return thought_type_fusion
    
    def _identify_fusion_patterns(self, assessment_data: Dict[str, Any]) -> List[str]:
        
        patterns = []
        
        if assessment_data.get("thought_believability", 0) >= 7:
            patterns.append("High literal believability of thoughts")
        
        if assessment_data.get("emotional_impact", 0) >= 7:
            patterns.append("Strong emotional reactivity to thoughts")
        
        if assessment_data.get("behavioral_influence", 0) >= 7:
            patterns.append("Thoughts heavily control behavior")
        
        if assessment_data.get("rumination_frequency", 0) >= 7:
            patterns.append("Frequent rumination and mental loops")
        
        if assessment_data.get("thought_suppression_attempts", 0) >= 7:
            patterns.append("Excessive attempts to control thoughts")
        
        if assessment_data.get("identity_fusion", 0) >= 7:
            patterns.append("Strong identification with thought content")
        
        return patterns
    
    def _identify_challenging_thought_types(self, thought_type_fusion: Dict[ThoughtType, FusionLevel]) -> List[ThoughtType]:
        
        challenging_types = []
        
        for thought_type, fusion_level in thought_type_fusion.items():
            if fusion_level in [FusionLevel.HIGH_FUSION, FusionLevel.COMPLETE_FUSION]:
                challenging_types.append(thought_type)
        
        return challenging_types
    
    def _recommend_techniques(self, challenging_types: List[ThoughtType], 
                            fusion_patterns: List[str]) -> List[str]:
        
        recommendations = set()
        
        for thought_type in challenging_types:
            if thought_type in self.thought_pattern_library:
                best_techniques = self.thought_pattern_library[thought_type]["best_techniques"]
                recommendations.update(best_techniques)
        
        if "High literal believability of thoughts" in fusion_patterns:
            recommendations.update(["observer_self", "word_repetition", "silly_voices"])
        
        if "Strong emotional reactivity to thoughts" in fusion_patterns:
            recommendations.update(["leaves_on_stream", "physicalizing_thoughts", "thanking_mind"])
        
        if "Frequent rumination and mental loops" in fusion_patterns:
            recommendations.update(["leaves_on_stream", "thought_labeling", "thanking_mind"])
        
        return list(recommendations)[:4]
    
    def _identify_defusion_strengths(self, assessment_data: Dict[str, Any]) -> List[str]:
        
        strengths = []
        
        if assessment_data.get("observer_awareness", 0) >= 7:
            strengths.append("Good observer self awareness")
        
        if assessment_data.get("thought_labeling", 0) >= 7:
            strengths.append("Able to recognize thoughts as mental events")
        
        if assessment_data.get("linguistic_flexibility", 0) >= 7:
            strengths.append("Flexible with language and thought forms")
        
        if assessment_data.get("metaphorical_thinking", 0) >= 7:
            strengths.append("Good metaphorical and creative thinking")
        
        if assessment_data.get("humor_application", 0) >= 7:
            strengths.append("Able to use humor with difficult thoughts")
        
        return strengths
    
    def _generate_progress_indicators(self, overall_fusion: FusionLevel) -> List[str]:
        
        indicators = []
        
        if overall_fusion == FusionLevel.COMPLETE_FUSION:
            indicators.extend([
                "Begin noticing thoughts as thoughts, not facts",
                "Develop awareness of mental activity",
                "Start questioning automatic believability"
            ])
        elif overall_fusion == FusionLevel.HIGH_FUSION:
            indicators.extend([
                "Increase observer perspective",
                "Practice basic defusion techniques",
                "Reduce literal interpretation of thoughts"
            ])
        elif overall_fusion == FusionLevel.MODERATE_FUSION:
            indicators.extend([
                "Improve consistency of defusion practice",
                "Apply techniques to challenging thoughts",
                "Develop personalized defusion strategies"
            ])
        else:
            indicators.extend([
                "Maintain defusion skills during stress",
                "Generalize techniques across contexts",
                "Help others with defusion skills"
            ])
        
        return indicators
    
    def _determine_intervention_priorities(self, challenging_types: List[ThoughtType]) -> List[str]:
        
        priorities = []
        
        priority_order = [
            ThoughtType.SELF_CRITICAL,
            ThoughtType.CATASTROPHIC,
            ThoughtType.RUMINATION,
            ThoughtType.WORRY,
            ThoughtType.PERFECTIONIST
        ]
        
        for thought_type in priority_order:
            if thought_type in challenging_types:
                type_name = thought_type.value.replace('_', ' ').title()
                priorities.append(f"Address {type_name} thought fusion")
        
        return priorities[:3]
    
    def create_defusion_intervention_plan(self, patient_id: str, 
                                        assessment: DefusionAssessment) -> Dict[str, Any]:
        
        plan = {
            "patient_id": patient_id,
            "assessment_date": assessment.assessment_date.isoformat(),
            "intervention_focus": assessment.intervention_priorities,
            "recommended_techniques": assessment.recommended_techniques,
            "practice_sequence": [],
            "homework_assignments": [],
            "session_structure": {},
            "progress_targets": assessment.progress_indicators
        }
        
        if assessment.overall_fusion_level in [FusionLevel.COMPLETE_FUSION, FusionLevel.HIGH_FUSION]:
            plan["practice_sequence"] = [
                "Start with psychoeducation about thoughts vs. facts",
                "Begin with observer self technique",
                "Practice with low-intensity thoughts first",
                "Gradually apply to more challenging thoughts"
            ]
            plan["session_structure"]["focus"] = "Basic defusion skill building"
        
        elif assessment.overall_fusion_level == FusionLevel.MODERATE_FUSION:
            plan["practice_sequence"] = [
                "Apply multiple defusion techniques",
                "Practice with personally relevant thoughts",
                "Develop technique preferences",
                "Begin real-world application"
            ]
            plan["session_structure"]["focus"] = "Skill refinement and application"
        
        else:
            plan["practice_sequence"] = [
                "Focus on challenging thought types",
                "Develop advanced defusion skills",
                "Create personalized technique combinations",
                "Work on generalization across contexts"
            ]
            plan["session_structure"]["focus"] = "Advanced application and generalization"
        
        for technique_id in assessment.recommended_techniques:
            technique = self.defusion_techniques.get(technique_id)
            if technique:
                plan["homework_assignments"].extend(technique.homework_adaptations[:2])
        
        plan["session_structure"]["activities"] = [
            "Check-in on fusion experiences since last session",
            "Practice target defusion technique with current thoughts",
            "Process insights and barriers encountered",
            "Plan homework application for coming week"
        ]
        
        return plan
    
    def track_defusion_progress(self, patient_id: str, weeks: int = 4) -> Dict[str, Any]:
        
        start_date = datetime.now() - timedelta(weeks=weeks)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT practice_date, technique_used, pre_fusion_rating, post_fusion_rating,
                       believability_change, emotional_impact_change, technique_effectiveness
                FROM defusion_practices
                WHERE patient_id = ? AND practice_date >= ?
                ORDER BY practice_date
            """, (patient_id, start_date.isoformat()))
            
            practices = cursor.fetchall()
        
        if not practices:
            return {"error": "No defusion practice data found"}
        
        progress = {
            "patient_id": patient_id,
            "tracking_period_weeks": weeks,
            "total_practices": len(practices),
            "fusion_reduction_trend": [],
            "technique_effectiveness": {},
            "average_improvements": {},
            "breakthrough_indicators": [],
            "recommendations": []
        }
        
        fusion_changes = []
        believability_changes = []
        emotional_changes = []
        technique_scores = {}
        
        for practice_date, technique, pre_fusion, post_fusion, believability_change, emotional_change, effectiveness in practices:
            if pre_fusion is not None and post_fusion is not None:
                fusion_change = pre_fusion - post_fusion
                fusion_changes.append(fusion_change)
                progress["fusion_reduction_trend"].append({
                    "date": practice_date,
                    "change": fusion_change
                })
            
            if believability_change is not None:
                believability_changes.append(believability_change)
            
            if emotional_change is not None:
                emotional_changes.append(emotional_change)
            
            if technique not in technique_scores:
                technique_scores[technique] = []
            if effectiveness is not None:
                technique_scores[technique].append(effectiveness)
        
        if fusion_changes:
            progress["average_improvements"]["fusion_reduction"] = round(sum(fusion_changes) / len(fusion_changes), 2)
        
        if believability_changes:
            progress["average_improvements"]["believability_reduction"] = round(sum(believability_changes) / len(believability_changes), 2)
        
        if emotional_changes:
            progress["average_improvements"]["emotional_impact_reduction"] = round(sum(emotional_changes) / len(emotional_changes), 2)
        
        for technique, scores in technique_scores.items():
            if scores:
                progress["technique_effectiveness"][technique] = round(sum(scores) / len(scores), 2)
        
        avg_fusion_reduction = progress["average_improvements"].get("fusion_reduction", 0)
        if avg_fusion_reduction >= 2.0:
            progress["breakthrough_indicators"].append("Consistent significant fusion reduction")
        elif avg_fusion_reduction >= 1.0:
            progress["breakthrough_indicators"].append("Steady moderate fusion reduction")
        
        if len(practices) >= weeks * 2:
            progress["breakthrough_indicators"].append("Good practice consistency")
        
        best_technique = max(progress["technique_effectiveness"].items(), key=lambda x: x[1]) if progress["technique_effectiveness"] else None
        if best_technique:
            progress["breakthrough_indicators"].append(f"Most effective technique: {best_technique[0]}")
        
        if progress["total_practices"] < weeks:
            progress["recommendations"].append("Increase frequency of defusion practice")
        
        if avg_fusion_reduction < 0.5:
            progress["recommendations"].append("Explore barriers to defusion effectiveness")
        
        if progress["technique_effectiveness"]:
            low_effectiveness = [tech for tech, score in progress["technique_effectiveness"].items() if score < 5]
            if low_effectiveness:
                progress["recommendations"].append(f"Consider alternative techniques to: {', '.join(low_effectiveness)}")
        
        return progress
    
    def generate_defusion_homework(self, technique_id: str, thought_type: ThoughtType, 
                                 difficulty_level: str = "moderate") -> Dict[str, Any]:
        
        technique = self.defusion_techniques.get(technique_id)
        if not technique:
            raise ValueError(f"Technique {technique_id} not found")
        
        thought_patterns = self.thought_pattern_library.get(thought_type, {})
        
        homework = {
            "technique_name": technique.name,
            "target_thought_type": thought_type.value,
            "difficulty_level": difficulty_level,
            "practice_instructions": technique.step_by_step_instructions,
            "daily_practice_goals": [],
            "specific_applications": [],
            "practice_log": {},
            "success_indicators": technique.success_indicators,
            "troubleshooting": []
        }
        
        if difficulty_level == "easy":
            homework["daily_practice_goals"] = [
                "Practice technique once daily with mild thoughts",
                "Use for 5-10 minutes per session",
                "Focus on thoughts rated 3-5 in intensity"
            ]
        elif difficulty_level == "moderate":
            homework["daily_practice_goals"] = [
                "Practice technique twice daily",
                "Apply to moderate intensity thoughts (5-7 rating)",
                "Use technique during daily stress situations"
            ]
        else:  # challenging
            homework["daily_practice_goals"] = [
                "Practice technique multiple times daily",
                "Apply to high intensity thoughts (7-10 rating)",
                "Use during crisis or high-stress moments"
            ]
        
        example_thoughts = thought_patterns.get("common_patterns", [])
        for example in example_thoughts[:3]:
            application = f"Apply {technique.name} to: '{example}'"
            homework["specific_applications"].append(application)
        
        homework["practice_log"] = {
            "thought_targeted": "Record the specific thought you worked with",
            "pre_fusion_rating": "Rate how fused you felt before practice (1-10)",
            "post_fusion_rating": "Rate how fused you felt after practice (1-10)",
            "technique_effectiveness": "Rate how well the technique worked (1-10)",
            "insights_gained": "Note any insights or observations",
            "barriers_encountered": "Record any difficulties or obstacles"
        }
        
        common_obstacles = [barrier.value for barrier in technique.common_obstacles]
        for obstacle in common_obstacles:
            troubleshooting_tip = f"If experiencing {obstacle}: Try practicing with easier thoughts first, use technique more playfully, or combine with mindfulness"
            homework["troubleshooting"].append(troubleshooting_tip)
        
        return homework
    
    def create_personalized_defusion_toolkit(self, patient_id: str, 
                                           patient_preferences: Dict[str, Any]) -> Dict[str, Any]:
        
        preferred_style = patient_preferences.get("learning_style", "mixed")
        challenging_thoughts = patient_preferences.get("challenging_thought_types", [])
        personality_factors = patient_preferences.get("personality_factors", [])
        
        toolkit = {
            "patient_id": patient_id,
            "personalized_techniques": {},
            "quick_reference_guide": [],
            "emergency_defusion_plan": [],
            "daily_practice_routine": [],
            "customization_notes": []
        }
        
        if preferred_style == "visual":
            recommended_techniques = ["leaves_on_stream", "physicalizing_thoughts", "thought_labeling"]
        elif preferred_style == "auditory":
            recommended_techniques = ["silly_voices", "word_repetition", "thanking_mind"]
        elif preferred_style == "kinesthetic":
            recommended_techniques = ["physicalizing_thoughts", "observer_self", "leaves_on_stream"]
        else:  # mixed
            recommended_techniques = ["observer_self", "thanking_mind", "silly_voices", "leaves_on_stream"]
        
        for technique_id in recommended_techniques:
            technique = self.defusion_techniques.get(technique_id)
            if technique:
                toolkit["personalized_techniques"][technique_id] = {
                    "name": technique.name,
                    "when_to_use": f"Best for {', '.join([t.value for t in technique.target_thought_types])} thoughts",
                    "quick_instructions": technique.step_by_step_instructions[:3],
                    "customization": self._customize_technique(technique, personality_factors)
                }
        
        toolkit["quick_reference_guide"] = [
            "Notice: Am I fused with this thought?",
            "Choose: Which defusion technique fits this situation?",
            "Apply: Use the technique with curiosity and playfulness",
            "Observe: How did my relationship to the thought change?"
        ]
        
        toolkit["emergency_defusion_plan"] = [
            f"Use {recommended_techniques[0]} for intense thoughts",
            "Remember: Thoughts are just thoughts, not facts",
            "Take three deep breaths before engaging with the thought",
            "Ask: 'Is buying into this thought helpful right now?'"
        ]
        
        toolkit["daily_practice_routine"] = [
            "Morning: Set intention to notice thought fusion",
            "Midday: Practice defusion with any challenging thoughts",
            "Evening: Review day for fusion moments and practice",
            "Bedtime: Use defusion technique with any lingering thoughts"
        ]
        
        if "humor" in personality_factors:
            toolkit["customization_notes"].append("Emphasize playful and humorous defusion techniques")
        
        if "serious" in personality_factors:
            toolkit["customization_notes"].append("Focus on mindful observation and gentle defusion approaches")
        
        if "creative" in personality_factors:
            toolkit["customization_notes"].append("Encourage metaphorical and artistic defusion expressions")
        
        return toolkit
    
    def _customize_technique(self, technique: DefusionTechnique, personality_factors: List[str]) -> str:
        
        customizations = []
        
        if technique.technique_id == "silly_voices" and "humor" in personality_factors:
            customizations.append("Try different character voices and accents for variety")
        
        if technique.technique_id == "leaves_on_stream" and "creative" in personality_factors:
            customizations.append("Visualize thoughts on different objects: flowers, clouds, boats")
        
        if technique.technique_id == "observer_self" and "mindful" in personality_factors:
            customizations.append("Combine with meditation practice for deeper observer awareness")
        
        if technique.technique_id == "physicalizing_thoughts" and "artistic" in personality_factors:
            customizations.append("Draw or sculpt your thoughts to make them more concrete")
        
        return "; ".join(customizations) if customizations else "Use technique as described"
    
    def _save_defusion_practice(self, practice: DefusionPractice):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO defusion_practices
                (practice_id, patient_id, session_id, technique_used, target_thought,
                 thought_type, pre_fusion_rating, post_fusion_rating, believability_change,
                 emotional_impact_change, behavioral_influence_change, barriers_encountered,
                 breakthrough_moments, insights_gained, technique_effectiveness,
                 patient_feedback, homework_application, therapist_observations, practice_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                practice.practice_id, practice.patient_id, practice.session_id,
                practice.technique_used, practice.target_thought, practice.thought_type.value,
                practice.pre_fusion_rating, practice.post_fusion_rating,
                practice.believability_change, practice.emotional_impact_change,
                practice.behavioral_influence_change,
                json.dumps([b.value for b in practice.barriers_encountered]),
                json.dumps(practice.breakthrough_moments), json.dumps(practice.insights_gained),
                practice.technique_effectiveness, practice.patient_feedback,
                practice.homework_application, practice.therapist_observations,
                practice.practice_date.isoformat()
            ))
    
    def _save_defusion_assessment(self, assessment: DefusionAssessment):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO defusion_assessments
                (assessment_id, patient_id, assessment_date, overall_fusion_level,
                 thought_type_fusion, primary_fusion_patterns, defusion_strengths,
                 challenging_thought_types, recommended_techniques, fusion_triggers,
                 progress_indicators, intervention_priorities)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id, assessment.patient_id,
                assessment.assessment_date.isoformat(), assessment.overall_fusion_level.value,
                json.dumps({k.value: v.value for k, v in assessment.thought_type_fusion.items()}),
                json.dumps(assessment.primary_fusion_patterns),
                json.dumps(assessment.defusion_strengths),
                json.dumps([t.value for t in assessment.challenging_thought_types]),
                json.dumps(assessment.recommended_techniques),
                json.dumps(assessment.fusion_triggers),
                json.dumps(assessment.progress_indicators),
                json.dumps(assessment.intervention_priorities)
            ))


if __name__ == "__main__":
    defusion_module = CognitiveDefusionModule()
    
    practice = defusion_module.conduct_defusion_practice(
        patient_id="patient_123",
        session_id="session_001",
        technique_id="observer_self",
        target_thought="I'm going to fail this presentation"
    )
    
    print("=== DEFUSION PRACTICE SESSION ===")
    print(f"Practice ID: {practice.practice_id}")
    print(f"Technique: {practice.technique_used}")
    print(f"Target Thought: {practice.target_thought}")
    print(f"Thought Type: {practice.thought_type.value}")
    
    assessment_data = {
        "thought_believability": 8,
        "emotional_impact": 7,
        "behavioral_influence": 6,
        "rumination_frequency": 8,
        "self_critical_fusion_score": 9,
        "catastrophic_fusion_score": 7,
        "worry_fusion_score": 8,
        "observer_awareness": 4,
        "thought_labeling": 3,
        "linguistic_flexibility": 5,
        "fusion_triggers": ["Work stress", "Social situations"]
    }
    
    assessment = defusion_module.assess_fusion_levels("patient_123", assessment_data)
    print(f"\n=== DEFUSION ASSESSMENT ===")
    print(f"Overall Fusion Level: {assessment.overall_fusion_level.value}")
    print(f"Challenging Thought Types: {[t.value for t in assessment.challenging_thought_types]}")
    print(f"Primary Patterns: {assessment.primary_fusion_patterns}")
    print(f"Recommended Techniques: {assessment.recommended_techniques}")
    
    intervention_plan = defusion_module.create_defusion_intervention_plan("patient_123", assessment)
    print(f"\n=== INTERVENTION PLAN ===")
    print(f"Focus Areas: {intervention_plan['intervention_focus']}")
    print(f"Practice Sequence: {intervention_plan['practice_sequence']}")
    print(f"Session Focus: {intervention_plan['session_structure']['focus']}")
    
    homework = defusion_module.generate_defusion_homework("observer_self", ThoughtType.SELF_CRITICAL, "moderate")
    print(f"\n=== HOMEWORK ASSIGNMENT ===")
    print(f"Technique: {homework['technique_name']}")
    print(f"Target Type: {homework['target_thought_type']}")
    print(f"Daily Goals: {homework['daily_practice_goals']}")
    print(f"Applications: {homework['specific_applications']}")
    
    patient_prefs = {
        "learning_style": "visual",
        "challenging_thought_types": ["self_critical", "worry"],
        "personality_factors": ["creative", "humor"]
    }
    
    toolkit = defusion_module.create_personalized_defusion_toolkit("patient_123", patient_prefs)
    print(f"\n=== PERSONALIZED TOOLKIT ===")
    print(f"Recommended Techniques: {list(toolkit['personalized_techniques'].keys())}")
    print(f"Quick Reference: {toolkit['quick_reference_guide']}")
    print(f"Customization Notes: {toolkit['customization_notes']}")
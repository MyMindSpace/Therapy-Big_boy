"""
Emotional Regulation Prompts Module
Professional emotional regulation intervention prompts for AI therapy system
Specialized prompts for emotion identification, regulation, grounding techniques, self-soothing, and mindfulness
"""

from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime, timedelta


class EmotionalInterventionType(Enum):
    """Types of emotional regulation interventions"""
    EMOTION_IDENTIFICATION = "emotion_identification"
    EMOTION_REGULATION = "emotion_regulation"
    EMOTION_TRACKING = "emotion_tracking"
    GROUNDING_TECHNIQUES = "grounding_techniques"
    SELF_SOOTHING = "self_soothing"
    MINDFULNESS_PRACTICE = "mindfulness_practice"
    DISTRESS_TOLERANCE = "distress_tolerance"
    EMOTIONAL_AWARENESS = "emotional_awareness"
    EMOTIONAL_EXPRESSION = "emotional_expression"
    EMOTIONAL_ACCEPTANCE = "emotional_acceptance"
    CRISIS_SURVIVAL_skills = "crisis_survival_skills"
    TIPP_TECHNIQUE = "tipp_technique"
    WISE_MIND = "wise_mind"
    RADICAL_ACCEPTANCE = "radical_acceptance"


class EmotionCategory(Enum):
    """Primary emotion categories"""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    ANXIETY = "anxiety"
    DISGUST = "disgust"
    SURPRISE = "surprise"
    CONTEMPT = "contempt"
    SHAME = "shame"
    GUILT = "guilt"
    LOVE = "love"
    EXCITEMENT = "excitement"
    DEPRESSION = "depression"
    IRRITABILITY = "irritability"
    CONTENTMENT = "contentment"
    OVERWHELM = "overwhelm"


class GroundingType(Enum):
    """Types of grounding techniques"""
    SENSORY = "sensory"
    BREATHING = "breathing"
    MOVEMENT = "movement"
    COGNITIVE = "cognitive"
    TACTILE = "tactile"
    PROGRESSIVE_MUSCLE = "progressive_muscle"
    EMOTIONAL = "emotional"
    SPIRITUAL = "spiritual"


class SelfSoothingCategory(Enum):
    """Self-soothing categories using the five senses"""
    SIGHT = "sight"
    SOUND = "sound"
    SMELL = "smell"
    TASTE = "taste"
    TOUCH = "touch"
    MOVEMENT = "movement"
    TEMPERATURE = "temperature"


class SessionPhase(Enum):
    """Phases of emotional regulation sessions"""
    ASSESSMENT = "assessment"
    PSYCHOEDUCATION = "psychoeducation"
    SKILL_INTRODUCTION = "skill_introduction"
    GUIDED_PRACTICE = "guided_practice"
    INDEPENDENT_PRACTICE = "independent_practice"
    CRISIS_INTERVENTION = "crisis_intervention"
    SKILL_BUILDING = "skill_building"
    INTEGRATION = "integration"
    HOMEWORK_ASSIGNMENT = "homework_assignment"
    REVIEW = "review"
    TROUBLESHOOTING = "troubleshooting"


class EmotionalIntensity(Enum):
    """Intensity levels for emotions"""
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


@dataclass
class EmotionalPromptTemplate:
    """Template for emotional regulation prompts"""
    intervention_type: EmotionalInterventionType
    phase: SessionPhase
    primary_prompt: str
    follow_up_questions: List[str]
    guided_instructions: List[str]
    therapeutic_techniques: List[str]
    common_obstacles: List[str]
    troubleshooting_strategies: List[str]
    outcome_measures: List[str]
    homework_assignments: List[str]
    therapeutic_rationale: str
    clinical_considerations: List[str]
    safety_considerations: List[str]


@dataclass
class EmotionalInterventionContext:
    """Context for emotional regulation interventions"""
    patient_id: str
    session_id: str
    current_emotions: List[Tuple[EmotionCategory, int]]  # emotion and intensity
    emotional_triggers: List[str]
    regulation_skills_mastered: List[str]
    preferred_soothing_activities: List[str]
    crisis_level: str  # "none", "mild", "moderate", "severe", "emergency"
    distress_tolerance: int  # 1-10 scale
    emotional_awareness: str  # "low", "developing", "good", "high"
    previous_grounding_success: List[str]
    physical_limitations: List[str]
    current_stressors: List[str]
    support_system_available: bool
    medication_effects: Optional[str]
    therapy_phase: str  # "stabilization", "skills_building", "integration"
    dbt_skills_stage: str  # "mindfulness", "distress_tolerance", "emotion_regulation", "interpersonal"


class EmotionalRegulationPrompts:
    """Comprehensive emotional regulation prompt system"""
    
    def __init__(self):
        self.prompt_templates = self._initialize_emotional_prompts()
        self.grounding_techniques = self._initialize_grounding_techniques()
        self.self_soothing_activities = self._initialize_self_soothing_activities()
        self.mindfulness_practices = self._initialize_mindfulness_practices()
        self.crisis_interventions = self._initialize_crisis_interventions()
        self.dbt_skills = self._initialize_dbt_skills()
    
    def get_emotional_intervention_prompt(
        self,
        intervention_type: EmotionalInterventionType,
        phase: SessionPhase,
        context: EmotionalInterventionContext,
        session_info: Dict[str, Any] = None
    ) -> str:
        """Generate contextual emotional regulation prompt"""
        
        template = self.prompt_templates.get((intervention_type, phase))
        if not template:
            return self._get_generic_emotional_prompt(intervention_type, phase)
        
        context_info = self._format_emotional_context(context, session_info)
        
        prompt = f"""
{template.primary_prompt}

PATIENT CONTEXT:
{context_info}

THERAPEUTIC RATIONALE:
{template.therapeutic_rationale}

GUIDED INSTRUCTIONS:
{chr(10).join(f"{i+1}. {instruction}" for i, instruction in enumerate(template.guided_instructions))}

FOLLOW-UP QUESTIONS:
{chr(10).join(f"• {question}" for question in template.follow_up_questions)}

THERAPEUTIC TECHNIQUES:
{chr(10).join(f"• {technique}" for technique in template.therapeutic_techniques)}

COMMON OBSTACLES & SOLUTIONS:
{chr(10).join(f"• {obstacle}" for obstacle in template.common_obstacles)}

SAFETY CONSIDERATIONS:
{chr(10).join(f"• {consideration}" for consideration in template.safety_considerations)}

OUTCOME MEASURES:
{chr(10).join(f"• {measure}" for measure in template.outcome_measures)}

CLINICAL CONSIDERATIONS:
{chr(10).join(f"• {consideration}" for consideration in template.clinical_considerations)}

APPROACH:
- Use a gentle, validating tone throughout
- Meet the patient where they are emotionally
- Focus on present-moment awareness and acceptance
- Provide concrete, practical skills
- Emphasize that all emotions are valid and temporary
- Build skills gradually and systematically
- Prioritize safety and stabilization when needed
"""
        
        return prompt
    
    def _initialize_emotional_prompts(self) -> Dict[Tuple[EmotionalInterventionType, SessionPhase], EmotionalPromptTemplate]:
        """Initialize comprehensive emotional regulation prompts"""
        
        prompts = {}
        
        # EMOTION IDENTIFICATION PROMPTS
        prompts[(EmotionalInterventionType.EMOTION_IDENTIFICATION, SessionPhase.ASSESSMENT)] = EmotionalPromptTemplate(
            intervention_type=EmotionalInterventionType.EMOTION_IDENTIFICATION,
            phase=SessionPhase.ASSESSMENT,
            primary_prompt="""
You are helping the patient develop better emotional awareness and identification skills. Many people struggle to name and understand their emotions, which makes it difficult to regulate them effectively.

Start by saying: "Let's work on understanding and identifying the emotions you're experiencing. Sometimes we feel things strongly but aren't sure exactly what emotions are present. Learning to name our emotions more precisely can be very helpful for managing them."

Focus on helping them develop a rich emotional vocabulary and body awareness of emotional experiences.
""",
            follow_up_questions=[
                "What emotions are you noticing right now in this moment?",
                "Where in your body do you feel this emotion?",
                "On a scale of 1-10, how intense is this feeling?",
                "Are there other emotions mixed in with the primary one you identified?",
                "What does this emotion feel like in your body?",
                "How long have you been feeling this way?",
                "What might have triggered this emotional response?"
            ],
            guided_instructions=[
                "Take a moment to pause and tune into your internal experience",
                "Notice any physical sensations in your body",
                "Scan from head to toe for areas of tension, warmth, or other sensations",
                "Try to put words to what you're feeling emotionally",
                "Consider both primary emotions and any secondary emotions present",
                "Rate the intensity of each emotion you identify"
            ],
            therapeutic_techniques=[
                "Body scan for emotional awareness",
                "Emotion wheel or emotion chart use",
                "Mindful emotional check-ins",
                "Physical sensation mapping",
                "Emotional granularity development",
                "Present-moment emotion identification"
            ],
            common_obstacles=[
                "Limited emotional vocabulary",
                "Alexithymia or emotional numbness",
                "Overwhelming emotional intensity",
                "Fear of experiencing emotions",
                "Cultural suppression of emotional expression",
                "Confusion between thoughts and emotions"
            ],
            troubleshooting_strategies=[
                "Start with basic emotion categories (mad, sad, glad, afraid)",
                "Use visual aids like emotion wheels",
                "Focus on body sensations when words are difficult",
                "Validate any emotional awareness as progress",
                "Use metaphors or imagery for emotional description",
                "Practice with less intense emotions first"
            ],
            outcome_measures=[
                "Ability to name specific emotions",
                "Recognition of emotional intensity levels",
                "Body awareness of emotional experience",
                "Distinction between thoughts and emotions",
                "Improved emotional vocabulary"
            ],
            homework_assignments=[
                "Complete emotion check-ins three times daily",
                "Use emotion tracking app or journal",
                "Practice body scan for emotions",
                "Notice and name emotions throughout the day"
            ],
            therapeutic_rationale="Emotional identification is the foundation of emotional regulation. By developing awareness and vocabulary for emotional experiences, patients can better understand, communicate, and manage their emotional responses.",
            clinical_considerations=[
                "Assess for alexithymia or emotional numbing",
                "Consider cultural factors in emotional expression",
                "Be patient with clients who struggle with emotional awareness",
                "Start with basic emotions before complex ones",
                "Validate all attempts at emotional identification"
            ],
            safety_considerations=[
                "Monitor for overwhelming emotional activation",
                "Have grounding techniques ready if needed",
                "Be prepared for unexpected emotional reactions",
                "Ensure patient feels safe to experience emotions"
            ]
        )
        
        # GROUNDING TECHNIQUES PROMPTS
        prompts[(EmotionalInterventionType.GROUNDING_TECHNIQUES, SessionPhase.GUIDED_PRACTICE)] = EmotionalPromptTemplate(
            intervention_type=EmotionalInterventionType.GROUNDING_TECHNIQUES,
            phase=SessionPhase.GUIDED_PRACTICE,
            primary_prompt="""
You are guiding the patient through grounding techniques to help them manage overwhelming emotions, anxiety, or dissociation. Grounding brings attention back to the present moment and helps regulate the nervous system.

Say: "Let's practice some grounding techniques together. These skills help you feel more centered and present when emotions feel overwhelming or when your mind is racing. I'll guide you through this step by step."

Focus on helping them feel safe, present, and connected to their immediate environment.
""",
            follow_up_questions=[
                "What do you notice happening in your body right now?",
                "How is your breathing feeling?",
                "What are you aware of in your immediate environment?",
                "On a scale of 1-10, how grounded do you feel?",
                "Which of your senses feels most accessible right now?",
                "What feels most solid or stable around you?",
                "How has your emotional intensity changed during this exercise?"
            ],
            guided_instructions=[
                "Find a comfortable position and allow your eyes to close or soften",
                "Take three deep, slow breaths to begin settling",
                "Notice your body's contact with the chair/floor - feel that support",
                "Name 5 things you can see (or visualize if eyes are closed)",
                "Identify 4 things you can physically touch or feel",
                "Listen for 3 different sounds in your environment",
                "Notice 2 scents or smells, or remember comforting smells",
                "Identify 1 taste in your mouth or recall a pleasant taste",
                "Take three more deep breaths and notice how you feel now"
            ],
            therapeutic_techniques=[
                "5-4-3-2-1 sensory grounding",
                "Progressive muscle relaxation",
                "Breathing-based grounding",
                "Object focus grounding",
                "Movement-based grounding",
                "Temperature-based grounding (cold water, ice)"
            ],
            common_obstacles=[
                "High emotional intensity interfering with focus",
                "Dissociation making sensory awareness difficult",
                "Anxiety about the grounding process itself",
                "Difficulty accessing senses due to overwhelm",
                "Resistance to slowing down",
                "Physical environment not conducive to grounding"
            ],
            troubleshooting_strategies=[
                "Start with strongest available sense",
                "Use tactile grounding (holding ice, textured object)",
                "Try movement-based grounding if sitting still is difficult",
                "Use familiar, comforting objects",
                "Adjust technique based on patient's response",
                "Be patient and go slowly"
            ],
            outcome_measures=[
                "Reduced emotional intensity ratings",
                "Increased sense of presence and groundedness",
                "Slower, deeper breathing patterns",
                "Reduced physical tension",
                "Improved focus and concentration"
            ],
            homework_assignments=[
                "Practice 5-4-3-2-1 technique daily",
                "Create personal grounding kit with preferred objects",
                "Use grounding when first noticing emotional escalation",
                "Experiment with different grounding techniques"
            ],
            therapeutic_rationale="Grounding techniques activate the parasympathetic nervous system and help regulate emotional arousal by connecting patients to present-moment sensory experience, providing immediate relief from overwhelming emotions.",
            clinical_considerations=[
                "Adjust techniques based on trauma history",
                "Be mindful of dissociation during grounding",
                "Consider sensory sensitivities or limitations",
                "Have multiple grounding options available",
                "Practice techniques when patient is calm first"
            ],
            safety_considerations=[
                "Monitor for increased dissociation during practice",
                "Be prepared to stop if patient becomes more distressed",
                "Have crisis plan available if grounding is ineffective",
                "Ensure environment feels safe for patient"
            ]
        )
        
        # SELF-SOOTHING PROMPTS
        prompts[(EmotionalInterventionType.SELF_SOOTHING, SessionPhase.SKILL_INTRODUCTION)] = EmotionalPromptTemplate(
            intervention_type=EmotionalInterventionType.SELF_SOOTHING,
            phase=SessionPhase.SKILL_INTRODUCTION,
            primary_prompt="""
You are introducing self-soothing skills using the five senses. Self-soothing helps manage distress and provides comfort during difficult emotional times without making the situation worse.

Say: "Self-soothing involves using your five senses to comfort yourself during distressing times. These skills don't solve problems, but they help you feel better in the moment so you can think more clearly and make better decisions later."

Focus on building a personalized toolkit of soothing activities for each sense.
""",
            follow_up_questions=[
                "What activities typically help you feel calm or comforted?",
                "Which of your five senses do you find most soothing?",
                "What did you use for comfort as a child?",
                "What environments or settings feel most calming to you?",
                "What scents, sounds, or textures do you find comforting?",
                "When you're upset, do you prefer to be active or still?",
                "What are some healthy ways you've comforted yourself in the past?"
            ],
            guided_instructions=[
                "Think about each of your five senses one at a time",
                "For sight: consider calming colors, nature scenes, art, photos",
                "For sound: think about music, nature sounds, voices that comfort you",
                "For smell: consider candles, essential oils, cooking smells, perfumes",
                "For taste: think about comforting foods, drinks, flavors",
                "For touch: consider soft textures, warm baths, massage, gentle pressure",
                "Create a list of 2-3 activities for each sense",
                "Plan how to access these activities when you need them"
            ],
            therapeutic_techniques=[
                "Five senses self-soothing planning",
                "Personalized soothing kit creation",
                "Mindful engagement with soothing activities",
                "Temperature-based soothing",
                "Movement and rhythm for soothing",
                "Breathing combined with sensory soothing"
            ],
            common_obstacles=[
                "Feeling guilty about taking time for self-care",
                "Belief that soothing activities are selfish or weak",
                "Difficulty accessing soothing activities when distressed",
                "Limited financial resources for soothing items",
                "Physical environment constraints",
                "Anhedonia reducing pleasure in typically soothing activities"
            ],
            troubleshooting_strategies=[
                "Address guilt and self-care resistance directly",
                "Focus on free or low-cost soothing options",
                "Create portable soothing kits",
                "Practice using techniques when not in crisis",
                "Start with very simple, accessible activities",
                "Normalize self-soothing as healthy coping"
            ],
            outcome_measures=[
                "Creation of personalized self-soothing plan",
                "Reduced emotional intensity after soothing activities",
                "Increased use of healthy coping strategies",
                "Improved self-care behaviors",
                "Greater emotional stability between sessions"
            ],
            homework_assignments=[
                "Create self-soothing kit with items for each sense",
                "Practice one self-soothing activity daily",
                "Use self-soothing when distress level reaches 6/10",
                "Keep log of which activities are most effective"
            ],
            therapeutic_rationale="Self-soothing provides immediate emotional relief and builds capacity for emotional self-regulation by engaging the nervous system's natural calming responses through sensory experiences.",
            clinical_considerations=[
                "Consider cultural background in activity suggestions",
                "Be mindful of trauma triggers in sensory experiences",
                "Address any shame around self-care needs",
                "Adapt activities to patient's living situation",
                "Start with patient's existing positive coping strategies"
            ],
            safety_considerations=[
                "Ensure activities are genuinely soothing, not numbing",
                "Monitor for avoidance of necessary problem-solving",
                "Watch for excessive dependency on soothing activities",
                "Be aware of potential sensory triggers"
            ]
        )
        
        # DISTRESS TOLERANCE PROMPTS
        prompts[(EmotionalInterventionType.DISTRESS_TOLERANCE, SessionPhase.SKILL_BUILDING)] = EmotionalPromptTemplate(
            intervention_type=EmotionalInterventionType.DISTRESS_TOLERANCE,
            phase=SessionPhase.SKILL_BUILDING,
            primary_prompt="""
You are teaching distress tolerance skills to help the patient survive emotional crises without making them worse through impulsive or harmful behaviors. The goal is building capacity to tolerate painful emotions.

Say: "Distress tolerance is about surviving painful emotions without making the situation worse. We can't always fix problems immediately, but we can learn to tolerate the distress until we can address the situation more effectively."

Focus on practical crisis survival skills and building tolerance for emotional discomfort.
""",
            follow_up_questions=[
                "What typically happens when you feel overwhelmed emotionally?",
                "What behaviors do you turn to when distress feels unbearable?",
                "How long do your most intense emotional states usually last?",
                "What has helped you get through difficult times in the past?",
                "When emotions are intense, what feels most urgent to you?",
                "How do you typically know when you're reaching your limit?",
                "What would happen if you rode out the feeling without acting on it?"
            ],
            guided_instructions=[
                "Recognize when you're in crisis mode (emotions 7/10 or higher)",
                "Remind yourself: 'This feeling is temporary and will pass'",
                "Choose a distress tolerance skill instead of harmful behavior",
                "Use TIPP: Temperature, Intense exercise, Paced breathing, Paired muscle relaxation",
                "Practice distraction techniques to get through the immediate crisis",
                "Focus on surviving the next hour, not solving the whole problem",
                "Return to problem-solving when emotional intensity decreases"
            ],
            therapeutic_techniques=[
                "TIPP technique for crisis survival",
                "Distraction and self-soothing skills",
                "Radical acceptance practices",
                "Urge surfing for behavioral impulses",
                "Reality acceptance vs. reality approval",
                "Crisis survival planning"
            ],
            common_obstacles=[
                "Belief that intense emotions are unbearable",
                "Impulse to act immediately when distressed",
                "Feeling that distress tolerance means giving up",
                "Difficulty remembering skills when in crisis",
                "Secondary emotions about having difficult emotions",
                "Pressure from others to 'fix' emotions quickly"
            ],
            troubleshooting_strategies=[
                "Practice skills when calm to build muscle memory",
                "Create crisis cards with step-by-step instructions",
                "Start with shorter time periods of tolerance",
                "Challenge beliefs about emotional unbearability",
                "Normalize having intense emotions as human experience",
                "Build support system for crisis times"
            ],
            outcome_measures=[
                "Reduced frequency of impulsive behaviors during crises",
                "Increased time between emotional trigger and response",
                "Better ability to wait before making decisions when upset",
                "Decreased intensity of emotional episodes over time",
                "Increased confidence in ability to handle difficult emotions"
            ],
            homework_assignments=[
                "Practice TIPP technique daily for one week",
                "Create personal crisis survival plan",
                "Use distress tolerance skills when emotions reach 7/10",
                "Track emotional intensity and skill use"
            ],
            therapeutic_rationale="Distress tolerance skills prevent impulsive behaviors that often worsen situations and build confidence in one's ability to handle difficult emotions, ultimately leading to better emotional regulation.",
            clinical_considerations=[
                "Assess for self-harm or suicidal behaviors",
                "Consider patient's typical crisis responses",
                "Build skills gradually during stable periods",
                "Address beliefs about emotional tolerance",
                "Consider medication effects on emotional intensity"
            ],
            safety_considerations=[
                "Have crisis plan in place before teaching skills",
                "Monitor for increased risk during emotional intensity",
                "Ensure patient has support system available",
                "Be prepared for emotional activation during skill practice"
            ]
        )
        
        # MINDFULNESS PRACTICE PROMPTS
        prompts[(EmotionalInterventionType.MINDFULNESS_PRACTICE, SessionPhase.GUIDED_PRACTICE)] = EmotionalPromptTemplate(
            intervention_type=EmotionalInterventionType.MINDFULNESS_PRACTICE,
            phase=SessionPhase.GUIDED_PRACTICE,
            primary_prompt="""
You are guiding the patient through mindfulness practice to develop present-moment awareness and emotional regulation skills. Mindfulness helps create space between emotions and reactions.

Say: "Mindfulness is about paying attention to the present moment with curiosity and acceptance. We'll practice observing your thoughts and emotions without immediately trying to change them. This creates space for you to choose how to respond."

Focus on developing the core mindfulness skills of observing, describing, and participating.
""",
            follow_up_questions=[
                "What do you notice happening in your mind right now?",
                "How are you feeling in your body at this moment?",
                "What thoughts are coming and going?",
                "Can you observe your emotions without being overwhelmed by them?",
                "What judgments are you noticing about this experience?",
                "How present do you feel right now (1-10)?",
                "What's it like to just observe without trying to change anything?"
            ],
            guided_instructions=[
                "Find a comfortable position and close your eyes or soften your gaze",
                "Begin by noticing your breath without trying to change it",
                "When you notice thoughts arising, simply observe them without judgment",
                "Label thoughts as 'thinking' and gently return attention to breath",
                "Notice any emotions present and observe them with curiosity",
                "If emotions feel intense, breathe with them rather than pushing away",
                "Practice the stance of 'wise mind' - balanced between emotion and logic",
                "End by setting intention to carry this awareness into your day"
            ],
            therapeutic_techniques=[
                "Breath awareness meditation",
                "Body scan meditation",
                "Loving-kindness meditation",
                "Wise mind practice",
                "Mindful observation skills",
                "Non-judgmental stance development"
            ],
            common_obstacles=[
                "Restless mind with many thoughts",
                "Belief that meditation should empty the mind",
                "Discomfort with sitting still",
                "Emotional intensity arising during practice",
                "Judgment about 'doing it wrong'",
                "Impatience with the process"
            ],
            troubleshooting_strategies=[
                "Normalize busy mind as normal part of practice",
                "Use shorter meditation periods initially",
                "Try walking meditation for active personalities",
                "Provide guidance for working with difficult emotions",
                "Emphasize process over outcome",
                "Use guided meditations rather than silent practice"
            ],
            outcome_measures=[
                "Increased present-moment awareness",
                "Reduced reactivity to thoughts and emotions",
                "Greater acceptance of internal experiences",
                "Improved emotional regulation",
                "Decreased mind wandering and rumination"
            ],
            homework_assignments=[
                "Practice 10-minute daily mindfulness meditation",
                "Use mindful awareness during daily activities",
                "Notice and label emotions mindfully throughout day",
                "Practice wise mind during decision-making"
            ],
            therapeutic_rationale="Mindfulness develops meta-cognitive awareness and emotional regulation by creating psychological distance from thoughts and emotions, allowing for more intentional responses rather than automatic reactions.",
            clinical_considerations=[
                "Start with shorter practices for beginners",
                "Be mindful of trauma history with body awareness",
                "Adapt practices for attention difficulties",
                "Consider spiritual/religious background",
                "Monitor for spiritual bypassing of emotions"
            ],
            safety_considerations=[
                "Be prepared for emotional release during practice",
                "Monitor for dissociation during meditation",
                "Have grounding techniques available",
                "Ensure patient feels safe to experience whatever arises"
            ]
        )
        
        return prompts
    
    def _initialize_grounding_techniques(self) -> Dict[str, Dict[str, Any]]:
        """Initialize specific grounding technique guidance"""
        
        return {
            "5_4_3_2_1_technique": {
                "name": "5-4-3-2-1 Sensory Grounding",
                "description": "Uses all five senses to ground in present moment",
                "instructions": [
                    "Name 5 things you can see",
                    "Name 4 things you can touch", 
                    "Name 3 things you can hear",
                    "Name 2 things you can smell",
                    "Name 1 thing you can taste"
                ],
                "duration": "3-5 minutes",
                "difficulty": "beginner",
                "best_for": ["anxiety", "panic", "dissociation", "overwhelm"]
            },
            
            "box_breathing": {
                "name": "Box Breathing",
                "description": "Structured breathing pattern to calm nervous system",
                "instructions": [
                    "Inhale for 4 counts",
                    "Hold breath for 4 counts",
                    "Exhale for 4 counts", 
                    "Hold empty for 4 counts",
                    "Repeat 5-10 cycles"
                ],
                "duration": "2-5 minutes",
                "difficulty": "beginner",
                "best_for": ["anxiety", "panic", "anger", "stress"]
            },
            
            "progressive_muscle_relaxation": {
                "name": "Progressive Muscle Relaxation",
                "description": "Systematically tense and release muscle groups",
                "instructions": [
                    "Start with toes - tense for 5 seconds, then release",
                    "Move up through legs, abdomen, arms, shoulders",
                    "Finish with neck and face muscles",
                    "Notice the contrast between tension and relaxation",
                    "End with whole body relaxation"
                ],
                "duration": "10-20 minutes",
                "difficulty": "intermediate",
                "best_for": ["anxiety", "tension", "sleep problems", "stress"]
            },
            
            "cold_water_technique": {
                "name": "Cold Water Grounding",
                "description": "Uses temperature to activate parasympathetic nervous system",
                "instructions": [
                    "Hold ice cubes in your hands",
                    "Or splash cold water on face and wrists",
                    "Or hold cold object against neck",
                    "Focus on the sensation of cold",
                    "Breathe normally while experiencing the cold"
                ],
                "duration": "1-2 minutes",
                "difficulty": "beginner",
                "best_for": ["panic attacks", "dissociation", "emotional overwhelm"]
            },
            
            "mindful_movement": {
                "name": "Mindful Movement Grounding",
                "description": "Uses gentle movement to reconnect with body",
                "instructions": [
                    "Stand and slowly stretch arms overhead",
                    "Gently roll shoulders and neck",
                    "Take a few mindful steps",
                    "Notice feet connecting with ground",
                    "Focus entirely on movement sensations"
                ],
                "duration": "2-5 minutes", 
                "difficulty": "beginner",
                "best_for": ["restlessness", "dissociation", "anxiety", "energy buildup"]
            }
        }
    
    def _initialize_self_soothing_activities(self) -> Dict[SelfSoothingCategory, List[Dict[str, Any]]]:
        """Initialize self-soothing activities by sensory category"""
        
        return {
            SelfSoothingCategory.SIGHT: [
                {"activity": "Look at calming photos or artwork", "accessibility": "high", "cost": "free"},
                {"activity": "Watch nature videos or scenes", "accessibility": "high", "cost": "free"},
                {"activity": "Light candles and watch the flames", "accessibility": "moderate", "cost": "low"},
                {"activity": "Look at beautiful or meaningful objects", "accessibility": "high", "cost": "free"},
                {"activity": "Watch fish in an aquarium", "accessibility": "moderate", "cost": "moderate"},
                {"activity": "Gaze at stars or clouds", "accessibility": "moderate", "cost": "free"},
                {"activity": "Look through photo albums of happy memories", "accessibility": "high", "cost": "free"},
                {"activity": "Watch calming color patterns or mandalas", "accessibility": "high", "cost": "free"}
            ],
            
            SelfSoothingCategory.SOUND: [
                {"activity": "Listen to calming music", "accessibility": "high", "cost": "free"},
                {"activity": "Nature sounds (rain, ocean, forest)", "accessibility": "high", "cost": "free"},
                {"activity": "Listen to guided meditations", "accessibility": "high", "cost": "free"},
                {"activity": "Sing or hum favorite songs", "accessibility": "high", "cost": "free"},
                {"activity": "Play a musical instrument", "accessibility": "moderate", "cost": "varies"},
                {"activity": "Listen to audiobooks or podcasts", "accessibility": "high", "cost": "low"},
                {"activity": "Sound of wind chimes", "accessibility": "moderate", "cost": "low"},
                {"activity": "Cat purring or dog breathing sounds", "accessibility": "moderate", "cost": "free"}
            ],
            
            SelfSoothingCategory.SMELL: [
                {"activity": "Use essential oils or aromatherapy", "accessibility": "moderate", "cost": "moderate"},
                {"activity": "Light scented candles", "accessibility": "moderate", "cost": "low"},
                {"activity": "Smell flowers or herbs", "accessibility": "moderate", "cost": "low"},
                {"activity": "Bake cookies or bread for the smell", "accessibility": "moderate", "cost": "low"},
                {"activity": "Use scented lotions or perfumes", "accessibility": "high", "cost": "low"},
                {"activity": "Smell coffee or tea", "accessibility": "high", "cost": "low"},
                {"activity": "Fresh air and outdoor scents", "accessibility": "high", "cost": "free"},
                {"activity": "Scented bath products", "accessibility": "moderate", "cost": "low"}
            ],
            
            SelfSoothingCategory.TASTE: [
                {"activity": "Sip herbal tea slowly and mindfully", "accessibility": "high", "cost": "low"},
                {"activity": "Eat comfort foods in moderation", "accessibility": "high", "cost": "low"},
                {"activity": "Suck on hard candy or mints", "accessibility": "high", "cost": "low"},
                {"activity": "Taste something sweet, sour, or spicy", "accessibility": "high", "cost": "low"},
                {"activity": "Chew gum with strong flavor", "accessibility": "high", "cost": "low"},
                {"activity": "Drink cold water or warm beverages", "accessibility": "high", "cost": "free"},
                {"activity": "Fresh fruit or vegetables", "accessibility": "high", "cost": "low"},
                {"activity": "Dark chocolate (small piece)", "accessibility": "high", "cost": "low"}
            ],
            
            SelfSoothingCategory.TOUCH: [
                {"activity": "Take a warm bath or shower", "accessibility": "high", "cost": "low"},
                {"activity": "Use soft blankets or pillows", "accessibility": "high", "cost": "low"},
                {"activity": "Pet an animal", "accessibility": "moderate", "cost": "free"},
                {"activity": "Hold ice cubes or cold objects", "accessibility": "high", "cost": "free"},
                {"activity": "Self-massage with lotion", "accessibility": "high", "cost": "low"},
                {"activity": "Wear comfortable, soft clothes", "accessibility": "high", "cost": "varies"},
                {"activity": "Touch different textures mindfully", "accessibility": "high", "cost": "free"},
                {"activity": "Use a heating pad or warm compress", "accessibility": "moderate", "cost": "low"}
            ],
            
            SelfSoothingCategory.MOVEMENT: [
                {"activity": "Gentle stretching or yoga", "accessibility": "high", "cost": "free"},
                {"activity": "Take a slow, mindful walk", "accessibility": "high", "cost": "free"},
                {"activity": "Rock back and forth gently", "accessibility": "high", "cost": "free"},
                {"activity": "Dance to calming music", "accessibility": "high", "cost": "free"},
                {"activity": "Progressive muscle relaxation", "accessibility": "high", "cost": "free"},
                {"activity": "Gentle hand or foot massage", "accessibility": "high", "cost": "free"},
                {"activity": "Swing on a swing if available", "accessibility": "low", "cost": "free"},
                {"activity": "Float in water (bath, pool)", "accessibility": "moderate", "cost": "low"}
            ]
        }
    
    def _initialize_mindfulness_practices(self) -> Dict[str, Dict[str, Any]]:
        """Initialize mindfulness practice guidance"""
        
        return {
            "breath_awareness": {
                "name": "Breath Awareness Meditation",
                "duration": "5-20 minutes",
                "difficulty": "beginner",
                "instructions": [
                    "Find comfortable seated position",
                    "Close eyes or soften gaze",
                    "Notice natural rhythm of breathing",
                    "When mind wanders, gently return to breath",
                    "No need to change breathing, just observe"
                ],
                "benefits": ["Calms nervous system", "Increases present-moment awareness", "Reduces anxiety"]
            },
            
            "body_scan": {
                "name": "Body Scan Meditation",
                "duration": "10-30 minutes",
                "difficulty": "beginner",
                "instructions": [
                    "Lie down comfortably",
                    "Start at toes, notice any sensations",
                    "Slowly move attention up through body",
                    "Notice tension, warmth, pressure, or relaxation",
                    "Include areas of no sensation",
                    "End with awareness of whole body"
                ],
                "benefits": ["Increases body awareness", "Promotes relaxation", "Helps with sleep"]
            },
            
            "loving_kindness": {
                "name": "Loving-Kindness Meditation",
                "duration": "10-20 minutes", 
                "difficulty": "intermediate",
                "instructions": [
                    "Begin with yourself: 'May I be happy, safe, peaceful'",
                    "Extend to loved one: 'May you be happy, safe, peaceful'",
                    "Include neutral person: acquaintance or stranger",
                    "Include difficult person in your life",
                    "Extend to all beings everywhere"
                ],
                "benefits": ["Increases self-compassion", "Reduces anger and resentment", "Builds empathy"]
            },
            
            "wise_mind": {
                "name": "Wise Mind Practice",
                "duration": "5-15 minutes",
                "difficulty": "intermediate", 
                "instructions": [
                    "Identify current emotional state",
                    "Notice logical thoughts about situation",
                    "Find place where emotion and reason meet",
                    "Ask: 'What does my wise mind know?'",
                    "Listen for deep inner knowing beyond emotion or logic"
                ],
                "benefits": ["Improves decision-making", "Balances emotion and logic", "Access to intuition"]
            },
            
            "mindful_walking": {
                "name": "Mindful Walking Meditation",
                "duration": "10-30 minutes",
                "difficulty": "beginner",
                "instructions": [
                    "Walk slower than normal pace",
                    "Focus on sensations of feet touching ground",
                    "Notice lifting, moving, placing of each foot",
                    "If mind wanders, return to walking sensations", 
                    "Can be done indoors or outdoors"
                ],
                "benefits": ["Grounds in present moment", "Combines meditation with movement", "Good for restless minds"]
            }
        }
    
    def _initialize_crisis_interventions(self) -> Dict[str, Dict[str, Any]]:
        """Initialize crisis intervention protocols"""
        
        return {
            "tipp_technique": {
                "name": "TIPP Crisis Survival",
                "when_to_use": "Emotional intensity 8-10/10",
                "components": {
                    "Temperature": "Cold water on face, hold ice, cold shower",
                    "Intense_exercise": "Run in place, jumping jacks, push-ups for 10+ minutes",
                    "Paced_breathing": "Exhale longer than inhale (4 in, 6 out)",
                    "Paired_muscle_relaxation": "Tense and release muscle groups"
                },
                "instructions": [
                    "Choose one component that's most accessible",
                    "Use intensely for 10-15 minutes",
                    "Continue until emotional intensity drops below 7/10",
                    "Follow with self-soothing or grounding"
                ]
            },
            
            "crisis_survival_kit": {
                "name": "Personal Crisis Survival Kit",
                "contents": [
                    "List of people to call for support",
                    "Grounding objects (smooth stone, stress ball)",
                    "Comforting scents (essential oil, perfume)",
                    "Photos of loved ones or peaceful places",
                    "Written reminders of reasons for living",
                    "Crisis hotline numbers",
                    "Calming music playlist",
                    "Comfort items (tea, candy, soft fabric)"
                ],
                "instructions": [
                    "Prepare kit when feeling stable",
                    "Keep kit easily accessible",
                    "Practice using items when not in crisis",
                    "Update contents regularly"
                ]
            },
            
            "radical_acceptance": {
                "name": "Radical Acceptance Practice",
                "when_to_use": "When fighting reality increases suffering",
                "steps": [
                    "Notice resistance to current reality",
                    "Acknowledge: 'This is the situation right now'",
                    "Practice phrases: 'I can't change this moment'",
                    "Turn mind toward acceptance when it turns to fighting",
                    "Accept with whole self - mind, body, spirit",
                    "Remember: acceptance doesn't mean approval"
                ],
                "common_barriers": [
                    "Confusing acceptance with approval",
                    "Fear that acceptance means giving up",
                    "Belief that suffering shows you care",
                    "Habit of fighting reality"
                ]
            }
        }
    
    def _initialize_dbt_skills(self) -> Dict[str, Dict[str, Any]]:
        """Initialize DBT-specific emotional regulation skills"""
        
        return {
            "please_skills": {
                "name": "PLEASE Skills for Emotional Vulnerability",
                "components": {
                    "treat_PhysicaL_illness": "Take care of medical issues",
                    "balance_Eating": "Eat regularly and healthily",
                    "avoid_mood_Altering_substances": "No drugs or alcohol",
                    "balance_Sleep": "Get adequate, regular sleep",
                    "get_Exercise": "Regular physical activity"
                },
                "purpose": "Reduce vulnerability to emotional extremes"
            },
            
            "opposite_action": {
                "name": "Opposite Action",
                "when_to_use": "When emotions don't fit facts or are too intense",
                "steps": [
                    "Identify the emotion and its action urge",
                    "Check if emotion fits the facts",
                    "Decide if acting on emotion would be effective",
                    "If not, act opposite to emotion's urge",
                    "Do opposite action all the way",
                    "Continue until emotion changes"
                ],
                "examples": {
                    "fear": "Approach what you're afraid of",
                    "anger": "Gently avoid or be kind", 
                    "sadness": "Get active, engage with others",
                    "shame": "Do what caused shame again",
                    "guilt": "Keep doing what caused guilt (if not harmful)"
                }
            },
            
            "emotion_regulation_abc": {
                "name": "ABC Skills for Managing Emotions",
                "components": {
                    "Accumulate_positive": "Build positive experiences and mastery",
                    "Build_mastery": "Do things that make you feel competent",
                    "Cope_ahead": "Plan for difficult situations"
                },
                "detailed_instructions": {
                    "accumulate_positive": [
                        "Schedule pleasant activities daily",
                        "Pay attention to positive experiences",
                        "Build a life worth living"
                    ],
                    "build_mastery": [
                        "Do one thing daily that gives sense of accomplishment",
                        "Build confidence through success experiences",
                        "Challenge yourself appropriately"
                    ],
                    "cope_ahead": [
                        "Identify likely problem situations",
                        "Plan specific coping strategies",
                        "Rehearse coping plan mentally",
                        "Gather resources needed"
                    ]
                }
            }
        }
    
    def _format_emotional_context(self, context: EmotionalInterventionContext, session_info: Dict[str, Any] = None) -> str:
        """Format emotional intervention context information"""
        
        context_lines = [
            f"Patient ID: {context.patient_id}",
            f"Crisis Level: {context.crisis_level}",
            f"Distress Tolerance: {context.distress_tolerance}/10",
            f"Emotional Awareness: {context.emotional_awareness}",
            f"Therapy Phase: {context.therapy_phase}",
            f"DBT Skills Stage: {context.dbt_skills_stage}"
        ]
        
        if context.current_emotions:
            emotion_strings = [f"{emotion.value} ({intensity}/10)" for emotion, intensity in context.current_emotions]
            context_lines.append(f"Current Emotions: {', '.join(emotion_strings)}")
        
        if context.emotional_triggers:
            context_lines.append(f"Known Triggers: {', '.join(context.emotional_triggers)}")
        
        if context.regulation_skills_mastered:
            context_lines.append(f"Mastered Skills: {', '.join(context.regulation_skills_mastered)}")
        
        if context.preferred_soothing_activities:
            context_lines.append(f"Preferred Soothing: {', '.join(context.preferred_soothing_activities)}")
        
        if context.previous_grounding_success:
            context_lines.append(f"Successful Grounding: {', '.join(context.previous_grounding_success)}")
        
        if context.current_stressors:
            context_lines.append(f"Current Stressors: {', '.join(context.current_stressors)}")
        
        if context.physical_limitations:
            context_lines.append(f"Physical Limitations: {', '.join(context.physical_limitations)}")
        
        context_lines.append(f"Support System Available: {'Yes' if context.support_system_available else 'No'}")
        
        if context.medication_effects:
            context_lines.append(f"Medication Effects: {context.medication_effects}")
        
        return chr(10).join(context_lines)
    
    def _get_generic_emotional_prompt(self, intervention_type: EmotionalInterventionType, phase: SessionPhase) -> str:
        """Generate generic emotional prompt when specific template not found"""
        
        return f"""
You are implementing {intervention_type.value.replace('_', ' ')} in the {phase.value.replace('_', ' ')} phase.

GENERAL EMOTIONAL REGULATION APPROACH:
- Validate all emotions as normal and temporary
- Focus on present-moment awareness and acceptance
- Teach skills for managing emotions rather than avoiding them
- Emphasize safety and stabilization when needed
- Build skills gradually and systematically
- Use gentle, non-judgmental approach

EMOTIONAL REGULATION PRINCIPLES:
- All emotions are temporary and will pass
- Emotions contain important information
- We can learn to experience emotions without being overwhelmed
- Skills practice builds emotional resilience
- Present-moment awareness reduces emotional intensity
- Self-compassion supports emotional healing

Continue with systematic emotional intervention appropriate for {intervention_type.value.replace('_', ' ')}.
"""
    
    def get_crisis_intervention_prompt(
        self,
        crisis_level: str,
        context: EmotionalInterventionContext,
        available_supports: List[str] = None
    ) -> str:
        """Generate crisis-specific intervention prompt"""
        
        crisis_info = self.crisis_interventions.get("tipp_technique", {})
        
        prompt = f"""
CRISIS INTERVENTION MODE - {crisis_level.upper()} LEVEL

You are providing immediate crisis intervention support. The patient is experiencing {crisis_level} level emotional distress.

PATIENT CONTEXT:
{self._format_emotional_context(context)}

IMMEDIATE PRIORITIES:
1. Ensure safety and stabilization
2. Reduce emotional intensity to manageable level
3. Prevent harmful or impulsive behaviors
4. Activate support systems if appropriate
5. Plan for immediate follow-up

CRISIS INTERVENTION TECHNIQUES:

TIPP TECHNIQUE (for emotional intensity 8-10/10):
"""
        
        for component, description in crisis_info.get("components", {}).items():
            prompt += f"• {component.replace('_', ' ')}: {description}\n"
        
        prompt += f"""
GROUNDING OPTIONS:
• 5-4-3-2-1 sensory technique
• Cold water on face and wrists
• Progressive muscle relaxation
• Mindful breathing with longer exhales

SAFETY ASSESSMENT:
• Are you having thoughts of hurting yourself or others?
• Do you have access to means of self-harm?
• Is there someone safe you can be with right now?
• Do you need emergency medical attention?

"""
        
        if available_supports:
            prompt += f"""
AVAILABLE SUPPORTS:
{chr(10).join(f"• {support}" for support in available_supports)}
"""
        
        prompt += f"""
CRISIS COMMUNICATION APPROACH:
- Use calm, steady voice and demeanor
- Provide concrete, step-by-step guidance
- Validate their emotional pain while focusing on safety
- Break down coping strategies into very small steps
- Stay present-focused rather than problem-solving
- Continue support until crisis intensity decreases

WHEN TO ESCALATE:
- Patient expresses imminent suicide or homicide risk
- Patient is unable to contract for safety
- Patient shows signs of psychosis or severe dissociation
- Patient requests emergency services
- Your clinical judgment indicates immediate danger

Remember: Crisis intervention is about getting through the immediate danger, not solving underlying problems.
"""
        
        return prompt
    
    def get_skill_practice_prompt(
        self,
        skill_name: str,
        context: EmotionalInterventionContext,
        practice_type: str = "guided"
    ) -> str:
        """Generate skill-specific practice prompt"""
        
        # Look up skill in various categories
        skill_info = None
        skill_category = "general"
        
        # Check grounding techniques
        if skill_name in self.grounding_techniques:
            skill_info = self.grounding_techniques[skill_name]
            skill_category = "grounding"
        
        # Check mindfulness practices
        elif skill_name in self.mindfulness_practices:
            skill_info = self.mindfulness_practices[skill_name]
            skill_category = "mindfulness"
        
        # Check DBT skills
        elif skill_name in self.dbt_skills:
            skill_info = self.dbt_skills[skill_name]
            skill_category = "dbt"
        
        if not skill_info:
            return f"Skill information not found for {skill_name}. Please use general emotional regulation approach."
        
        prompt = f"""
SKILL PRACTICE: {skill_info.get('name', skill_name)}

PATIENT CONTEXT:
{self._format_emotional_context(context)}

SKILL OVERVIEW:
{skill_info.get('description', 'Emotional regulation skill practice')}

"""
        
        if practice_type == "guided":
            prompt += f"""
GUIDED PRACTICE INSTRUCTIONS:
You will guide the patient through this skill step by step.

"""
            if 'instructions' in skill_info:
                prompt += f"STEP-BY-STEP GUIDANCE:\n"
                for i, instruction in enumerate(skill_info['instructions'], 1):
                    prompt += f"{i}. {instruction}\n"
        
        elif practice_type == "independent":
            prompt += f"""
INDEPENDENT PRACTICE SETUP:
You are preparing the patient to use this skill on their own.

TEACHING POINTS:
• When to use this skill
• How to remember the steps
• What to expect during practice
• How to troubleshoot common problems
• How to track effectiveness
"""
        
        if 'duration' in skill_info:
            prompt += f"\nEXPECTED DURATION: {skill_info['duration']}\n"
        
        if 'difficulty' in skill_info:
            prompt += f"DIFFICULTY LEVEL: {skill_info['difficulty']}\n"
        
        if 'best_for' in skill_info:
            prompt += f"MOST HELPFUL FOR: {', '.join(skill_info['best_for'])}\n"
        
        if 'benefits' in skill_info:
            prompt += f"\nEXPECTED BENEFITS:\n"
            for benefit in skill_info['benefits']:
                prompt += f"• {benefit}\n"
        
        prompt += f"""
COACHING APPROACH:
- Provide gentle, encouraging guidance
- Normalize any difficulty or resistance
- Adjust pace based on patient's response
- Check in frequently about their experience
- Validate any benefits or insights they notice
- Be patient if the skill feels unfamiliar or difficult

TROUBLESHOOTING:
- If patient becomes more distressed, slow down or stop
- If mind wanders frequently, provide more structure
- If physical discomfort arises, suggest modifications
- If emotional intensity increases, add grounding first
- If patient resists, explore their concerns

Remember: The goal is learning and practice, not perfect execution.
"""
        
        return prompt
    
    def get_emotion_tracking_prompt(
        self,
        tracking_method: str,
        context: EmotionalInterventionContext
    ) -> str:
        """Generate emotion tracking guidance prompt"""
        
        prompt = f"""
EMOTION TRACKING: {tracking_method.replace('_', ' ').title()}

PATIENT CONTEXT:
{self._format_emotional_context(context)}

PURPOSE OF EMOTION TRACKING:
• Increase emotional awareness and vocabulary
• Identify patterns in emotional responses
• Track effectiveness of coping strategies
• Monitor progress in emotional regulation
• Provide data for treatment planning

"""
        
        if tracking_method == "dbt_diary_card":
            prompt += f"""
DBT DIARY CARD COMPONENTS:
1. Daily emotions and their intensity (0-5 scale)
2. Urges to self-harm or suicide (0-5 scale)
3. Skills used and their effectiveness
4. Sleep, medications, substances
5. Daily notes about significant events

GUIDANCE FOR COMPLETION:
• Complete card each evening
• Rate emotions based on highest intensity during day
• Be honest about urges and behaviors
• Note which skills were most helpful
• Include brief notes about triggers or stressors
"""
        
        elif tracking_method == "emotion_log":
            prompt += f"""
EMOTION LOG COMPONENTS:
• Date and time of emotional experience
• Triggering situation or event
• Specific emotions experienced
• Intensity level (1-10 scale)
• Physical sensations noticed
• Thoughts associated with emotions
• Actions taken or urges experienced
• Outcome and what helped

GUIDANCE FOR COMPLETION:
• Log emotions in real-time when possible
• Focus on specific emotions rather than general mood
• Include both positive and negative emotions
• Note what helped regulate or intensify emotions
"""
        
        elif tracking_method == "mood_tracking":
            prompt += f"""
MOOD TRACKING COMPONENTS:
• Overall mood rating (1-10 scale)
• Energy level (1-10 scale)
• Sleep quality and duration
• Medication adherence
• Significant events or stressors
• Activities that affected mood
• Social interactions

GUIDANCE FOR COMPLETION:
• Rate mood at same time each day
• Consider overall mood, not just current moment
• Include factors that influenced mood
• Track patterns over time
"""
        
        prompt += f"""
TRACKING SUPPORT STRATEGIES:
• Set reminders to complete tracking
• Start with simple version and add complexity gradually
• Use apps or paper-based systems based on preference
• Review patterns weekly with therapist
• Celebrate insights and awareness gained
• Use data to inform treatment decisions

COMMON OBSTACLES:
• Forgetting to track consistently
• Difficulty identifying specific emotions
• Overwhelm with tracking requirements
• Perfectionism about "doing it right"
• Resistance to examining difficult emotions

TROUBLESHOOTING:
• Start with basic emotion categories (mad, sad, glad, afraid)
• Use emotion wheels or apps for vocabulary support
• Set phone reminders or alarms
• Keep tracking tools easily accessible
• Focus on progress, not perfection
• Process tracking insights in therapy sessions

APPROACH:
Guide the patient to see emotion tracking as a valuable tool for self-understanding rather than another obligation. Emphasize curiosity and self-compassion in the tracking process.
"""
        
        return prompt


class EmotionalRegulationWorkflow:
    """Manages complete emotional regulation intervention workflow"""
    
    def __init__(self):
        self.prompts = EmotionalRegulationPrompts()
        self.workflow_templates = self._initialize_workflow_templates()
    
    def _initialize_workflow_templates(self) -> Dict[EmotionalInterventionType, List[SessionPhase]]:
        """Initialize workflow templates for emotional interventions"""
        
        return {
            EmotionalInterventionType.EMOTION_IDENTIFICATION: [
                SessionPhase.ASSESSMENT,
                SessionPhase.PSYCHOEDUCATION,
                SessionPhase.GUIDED_PRACTICE,
                SessionPhase.INDEPENDENT_PRACTICE,
                SessionPhase.INTEGRATION
            ],
            
            EmotionalInterventionType.GROUNDING_TECHNIQUES: [
                SessionPhase.PSYCHOEDUCATION,
                SessionPhase.SKILL_INTRODUCTION,
                SessionPhase.GUIDED_PRACTICE,
                SessionPhase.INDEPENDENT_PRACTICE,
                SessionPhase.TROUBLESHOOTING,
                SessionPhase.INTEGRATION
            ],
            
            EmotionalInterventionType.DISTRESS_TOLERANCE: [
                SessionPhase.ASSESSMENT,
                SessionPhase.PSYCHOEDUCATION,
                SessionPhase.SKILL_BUILDING,
                SessionPhase.GUIDED_PRACTICE,
                SessionPhase.CRISIS_INTERVENTION,
                SessionPhase.INTEGRATION
            ],
            
            EmotionalInterventionType.SELF_SOOTHING: [
                SessionPhase.ASSESSMENT,
                SessionPhase.SKILL_INTRODUCTION,
                SessionPhase.GUIDED_PRACTICE,
                SessionPhase.INDEPENDENT_PRACTICE,
                SessionPhase.INTEGRATION
            ]
        }
    
    def get_workflow_prompt(
        self,
        intervention_type: EmotionalInterventionType,
        current_phase: SessionPhase,
        context: EmotionalInterventionContext,
        session_number: int = 1
    ) -> str:
        """Get workflow-appropriate prompt for current phase"""
        
        workflow = self.workflow_templates.get(intervention_type, [])
        
        if current_phase not in workflow:
            return self.prompts.get_emotional_intervention_prompt(
                intervention_type, current_phase, context
            )
        
        phase_index = workflow.index(current_phase)
        total_phases = len(workflow)
        
        base_prompt = self.prompts.get_emotional_intervention_prompt(
            intervention_type, current_phase, context
        )
        
        workflow_info = f"""
EMOTIONAL REGULATION WORKFLOW:
Intervention: {intervention_type.value.replace('_', ' ').title()}
Current Phase: {current_phase.value.replace('_', ' ').title()} ({phase_index + 1}/{total_phases})
Session Number: {session_number}

PHASES COMPLETED:
{chr(10).join(f"✓ {phase.value.replace('_', ' ').title()}" for phase in workflow[:phase_index])}

UPCOMING PHASES:
{chr(10).join(f"• {phase.value.replace('_', ' ').title()}" for phase in workflow[phase_index + 1:])}

"""
        
        return workflow_info + base_prompt


# Example usage and utility functions
def example_usage():
    """Example of how to use the emotional regulation prompt system"""
    
    # Initialize the emotional regulation system
    emotional_system = EmotionalRegulationPrompts()
    
    # Create patient context
    context = EmotionalInterventionContext(
        patient_id="PATIENT_001",
        session_id="SESSION_005",
        current_emotions=[(EmotionCategory.ANXIETY, 8), (EmotionCategory.SADNESS, 6)],
        emotional_triggers=["work stress", "relationship conflict"],
        regulation_skills_mastered=["basic breathing", "5-4-3-2-1 grounding"],
        preferred_soothing_activities=["warm bath", "listening to music"],
        crisis_level="moderate",
        distress_tolerance=4,
        emotional_awareness="developing",
        previous_grounding_success=["box breathing", "cold water technique"],
        physical_limitations=[],
        current_stressors=["job deadline", "family visit"],
        support_system_available=True,
        medication_effects="some drowsiness",
        therapy_phase="skills_building",
        dbt_skills_stage="distress_tolerance"
    )
    
    # Get emotion identification prompt
    emotion_id_prompt = emotional_system.get_emotional_intervention_prompt(
        EmotionalInterventionType.EMOTION_IDENTIFICATION,
        SessionPhase.ASSESSMENT,
        context
    )
    
    print("EMOTION IDENTIFICATION PROMPT:")
    print("=" * 60)
    print(emotion_id_prompt)
    print("\n")
    
    # Get grounding technique prompt
    grounding_prompt = emotional_system.get_skill_practice_prompt(
        "5_4_3_2_1_technique",
        context,
        "guided"
    )
    
    print("GROUNDING TECHNIQUE PRACTICE PROMPT:")
    print("=" * 60)
    print(grounding_prompt)
    print("\n")
    
    # Get crisis intervention prompt
    crisis_prompt = emotional_system.get_crisis_intervention_prompt(
        "moderate",
        context,
        ["spouse", "therapist", "crisis hotline"]
    )
    
    print("CRISIS INTERVENTION PROMPT:")
    print("=" * 60)
    print(crisis_prompt)
    print("\n")


if __name__ == "__main__":
    example_usage()
"""
Acceptance and Commitment Therapy (ACT) Prompts Module
Professional ACT-specific prompts for AI therapy system
Specialized prompts for psychological flexibility, values clarification, cognitive defusion, and committed action
"""

from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime, timedelta


class ACTProcess(Enum):
    """The six core ACT processes"""
    PSYCHOLOGICAL_FLEXIBILITY = "psychological_flexibility"
    PRESENT_MOMENT_AWARENESS = "present_moment_awareness"
    ACCEPTANCE = "acceptance"
    COGNITIVE_DEFUSION = "cognitive_defusion"
    VALUES_CLARIFICATION = "values_clarification"
    COMMITTED_ACTION = "committed_action"
    SELF_AS_CONTEXT = "self_as_context"
    MINDFULNESS = "mindfulness"


class ACTInterventionType(Enum):
    """Types of ACT interventions"""
    VALUES_EXPLORATION = "values_exploration"
    COGNITIVE_DEFUSION = "cognitive_defusion"
    ACCEPTANCE_PRACTICE = "acceptance_practice"
    MINDFULNESS_MEDITATION = "mindfulness_meditation"
    COMMITTED_ACTION_PLANNING = "committed_action_planning"
    PSYCHOLOGICAL_FLEXIBILITY_TRAINING = "psychological_flexibility_training"
    WILLINGNESS_EXERCISES = "willingness_exercises"
    CREATIVE_HOPELESSNESS = "creative_hopelessness"
    METAPHOR_WORK = "metaphor_work"
    EXPERIENTIAL_EXERCISES = "experiential_exercises"
    WORKABILITY_ASSESSMENT = "workability_assessment"


class ValuesArea(Enum):
    """Life domains for values exploration"""
    FAMILY_RELATIONSHIPS = "family_relationships"
    INTIMATE_RELATIONSHIPS = "intimate_relationships"
    FRIENDSHIPS = "friendships"
    CAREER_WORK = "career_work"
    EDUCATION_LEARNING = "education_learning"
    RECREATION_FUN = "recreation_fun"
    SPIRITUALITY = "spirituality"
    COMMUNITY_CITIZENSHIP = "community_citizenship"
    HEALTH_PHYSICAL_CARE = "health_physical_care"
    ENVIRONMENT_NATURE = "environment_nature"
    CREATIVITY_AESTHETICS = "creativity_aesthetics"
    PERSONAL_GROWTH = "personal_growth"


class SessionPhase(Enum):
    """Phases of ACT sessions"""
    CENTERING = "centering"
    VALUES_CHECK_IN = "values_check_in"
    WORKABILITY_ASSESSMENT = "workability_assessment"
    DEFUSION_PRACTICE = "defusion_practice"
    ACCEPTANCE_WORK = "acceptance_work"
    VALUES_EXPLORATION = "values_exploration"
    COMMITTED_ACTION = "committed_action"
    INTEGRATION = "integration"
    HOMEWORK_ASSIGNMENT = "homework_assignment"
    CLOSING_MINDFULNESS = "closing_mindfulness"


class DefusionTechnique(Enum):
    """Cognitive defusion techniques"""
    IM_HAVING_THE_THOUGHT = "im_having_the_thought"
    SILLY_VOICE = "silly_voice"
    SINGING_THOUGHTS = "singing_thoughts"
    LEAVES_ON_STREAM = "leaves_on_stream"
    CLOUDS_IN_SKY = "clouds_in_sky"
    THANK_YOUR_MIND = "thank_your_mind"
    COMPUTER_SCREEN = "computer_screen"
    OBSERVING_SELF = "observing_self"
    WORD_REPETITION = "word_repetition"
    THOUGHTS_AS_VISITORS = "thoughts_as_visitors"


@dataclass
class ACTPromptTemplate:
    """Template for ACT-specific prompts"""
    process: ACTProcess
    intervention_type: ACTInterventionType
    phase: SessionPhase
    primary_prompt: str
    experiential_instructions: List[str]
    metaphors_to_use: List[str]
    follow_up_questions: List[str]
    workability_questions: List[str]
    values_connection: str
    common_obstacles: List[str]
    troubleshooting_strategies: List[str]
    homework_assignments: List[str]
    therapeutic_rationale: str
    clinical_considerations: List[str]


@dataclass
class ACTContext:
    """Context for ACT interventions"""
    patient_id: str
    session_id: str
    identified_values: List[Tuple[ValuesArea, str]]  # area and specific value
    psychological_flexibility_level: str  # "low", "developing", "moderate", "high"
    primary_avoidance_patterns: List[str]
    fusion_with_thoughts: List[str]  # specific thoughts patient is fused with
    workability_concerns: List[str]  # behaviors not working toward values
    current_life_struggles: List[str]
    values_behavior_gap: str  # "large", "moderate", "small"
    mindfulness_experience: str  # "none", "some", "regular", "experienced"
    resistance_to_acceptance: str  # "high", "moderate", "low"
    commitment_history: str  # "poor", "inconsistent", "good"
    preferred_metaphors: List[str]
    cultural_values_considerations: List[str]


class ACTTherapeuticPrompts:
    """Comprehensive ACT therapeutic prompt system"""
    
    def __init__(self):
        self.prompt_templates = self._initialize_act_prompts()
        self.values_exploration_guides = self._initialize_values_guides()
        self.defusion_techniques = self._initialize_defusion_techniques()
        self.metaphor_library = self._initialize_metaphor_library()
        self.acceptance_exercises = self._initialize_acceptance_exercises()
        self.mindfulness_practices = self._initialize_mindfulness_practices()
    
    def get_act_prompt(
        self,
        process: ACTProcess,
        intervention_type: ACTInterventionType,
        phase: SessionPhase,
        context: ACTContext,
        session_info: Dict[str, Any] = None
    ) -> str:
        """Generate contextual ACT therapeutic prompt"""
        
        template = self.prompt_templates.get((process, intervention_type, phase))
        if not template:
            return self._get_generic_act_prompt(process, intervention_type, phase)
        
        context_info = self._format_act_context(context, session_info)
        
        prompt = f"""
{template.primary_prompt}

PATIENT CONTEXT:
{context_info}

THERAPEUTIC RATIONALE:
{template.therapeutic_rationale}

EXPERIENTIAL INSTRUCTIONS:
{chr(10).join(f"{i+1}. {instruction}" for i, instruction in enumerate(template.experiential_instructions))}

ACT METAPHORS TO CONSIDER:
{chr(10).join(f"• {metaphor}" for metaphor in template.metaphors_to_use)}

FOLLOW-UP QUESTIONS:
{chr(10).join(f"• {question}" for question in template.follow_up_questions)}

WORKABILITY ASSESSMENT:
{chr(10).join(f"• {question}" for question in template.workability_questions)}

VALUES CONNECTION:
{template.values_connection}

COMMON OBSTACLES & SOLUTIONS:
{chr(10).join(f"• {obstacle}" for obstacle in template.common_obstacles)}

CLINICAL CONSIDERATIONS:
{chr(10).join(f"• {consideration}" for consideration in template.clinical_considerations)}

ACT APPROACH:
- Use experiential exercises rather than just talking about concepts
- Focus on workability rather than truth or logic
- Connect all interventions back to patient's values
- Embrace paradox and use creative hopelessness when appropriate
- Use metaphors and experiential learning extensively
- Maintain focus on psychological flexibility as overarching goal
- Validate difficulty while encouraging willingness to experience
"""
        
        return prompt
    
    def _initialize_act_prompts(self) -> Dict[Tuple[ACTProcess, ACTInterventionType, SessionPhase], ACTPromptTemplate]:
        """Initialize comprehensive ACT therapeutic prompts"""
        
        prompts = {}
        
        # VALUES CLARIFICATION PROMPTS
        prompts[(ACTProcess.VALUES_CLARIFICATION, ACTInterventionType.VALUES_EXPLORATION, SessionPhase.VALUES_EXPLORATION)] = ACTPromptTemplate(
            process=ACTProcess.VALUES_CLARIFICATION,
            intervention_type=ACTInterventionType.VALUES_EXPLORATION,
            phase=SessionPhase.VALUES_EXPLORATION,
            primary_prompt="""
You are facilitating deep values exploration using ACT principles. Values are chosen life directions that guide behavior and provide meaning. This is foundational work in ACT.

Say: "We're going to explore what truly matters to you - your values. These aren't goals you achieve, but ongoing directions you choose to move toward. Think of values like a compass pointing north - they give direction to your life journey."

Use experiential exercises and metaphors to help the patient connect with their authentic values, not what they think they should value.
""",
            experiential_instructions=[
                "Begin with the 'funeral exercise' or 'birthday party at 80' visualization",
                "Have patient imagine what they'd want people to say about how they lived",
                "Use values card sort to identify top 5-7 values across life domains",
                "Explore each value: 'What would this look like in daily life?'",
                "Assess gap between values and current behavior",
                "Identify barriers that prevent values-consistent living"
            ],
            metaphors_to_use=[
                "Values as compass directions vs. goals as destinations",
                "Values as the mountain you're climbing vs. the summit",
                "Values as the way you want to travel vs. where you end up",
                "Life as a garden - values are how you want to tend it"
            ],
            follow_up_questions=[
                "What does this value mean to you personally?",
                "How would someone who didn't know you see this value in your daily life?",
                "When do you feel most connected to this value?",
                "What gets in the way of living this value more fully?",
                "If you could live this value more consistently, what would be different?",
                "What small step toward this value could you take today?"
            ],
            workability_questions=[
                "How well is your current behavior serving this value?",
                "What behaviors take you away from this value?",
                "If you continued your current patterns, where would you be in 5 years regarding this value?",
                "What would need to change for you to feel more aligned with this value?"
            ],
            values_connection="This exercise is designed to connect the patient with their authentic values that will guide all subsequent ACT work and committed actions.",
            common_obstacles=[
                "Confusing values with goals or outcomes",
                "Stating values they think they should have vs. authentic values",
                "Feeling overwhelmed by the gap between values and current behavior",
                "Believing they need to be perfect at living values",
                "Cultural or family values conflicting with personal values"
            ],
            troubleshooting_strategies=[
                "Emphasize values as directions, not destinations",
                "Normalize the gap between values and behavior",
                "Use 'workability' rather than 'right/wrong' framework",
                "Explore whose voice they're hearing when stating 'shoulds'",
                "Start with small, achievable values-based actions"
            ],
            homework_assignments=[
                "Complete values assessment across all life domains",
                "Notice moments when feeling most/least connected to values",
                "Identify one small values-based action to take daily",
                "Write about what each value means personally"
            ],
            therapeutic_rationale="Values clarification provides the foundation for all ACT work by connecting patients with their authentic life directions, which becomes the motivation for psychological flexibility and committed action.",
            clinical_considerations=[
                "Be aware of cultural values vs. personal values",
                "Watch for perfectionism about values-consistent living",
                "Address guilt about past values-inconsistent behavior",
                "Consider developmental stage and life circumstances",
                "Respect patient's pace in values exploration"
            ]
        )
        
        # COGNITIVE DEFUSION PROMPTS
        prompts[(ACTProcess.COGNITIVE_DEFUSION, ACTInterventionType.COGNITIVE_DEFUSION, SessionPhase.DEFUSION_PRACTICE)] = ACTPromptTemplate(
            process=ACTProcess.COGNITIVE_DEFUSION,
            intervention_type=ACTInterventionType.COGNITIVE_DEFUSION,
            phase=SessionPhase.DEFUSION_PRACTICE,
            primary_prompt="""
You are teaching cognitive defusion techniques to help the patient change their relationship with difficult thoughts. The goal is not to eliminate thoughts but to reduce their impact and believability.

Say: "We're going to practice some techniques that help you step back from your thoughts rather than being caught up in them. The goal isn't to get rid of thoughts or make them positive, but to see them as mental events rather than absolute truths."

Use experiential exercises that help the patient observe thoughts with distance and curiosity rather than getting entangled in their content.
""",
            experiential_instructions=[
                "Start with a specific troubling thought the patient is experiencing",
                "Have them repeat the thought as 'I'm having the thought that...'",
                "Practice saying the thought in a silly voice or singing it",
                "Use the 'leaves on a stream' visualization with the thought",
                "Practice 'thanking your mind' for the thought",
                "Try the 'computer screen' technique - seeing thought as text on screen"
            ],
            metaphors_to_use=[
                "Thoughts as clouds passing through the sky of awareness",
                "Mind as a radio that sometimes tunes to unhelpful stations",
                "Thoughts as unwanted passengers on your life bus",
                "Mind as an overly helpful advisor who sometimes gives bad advice"
            ],
            follow_up_questions=[
                "What happens to the believability of that thought when you say it in a silly voice?",
                "Can you observe the thought without getting caught up in whether it's true?",
                "What's it like to see your thought as just mental chatter?",
                "How does it feel to thank your mind for that thought?",
                "What would happen if you carried that thought lightly, like a leaf in your pocket?"
            ],
            workability_questions=[
                "How workable is it to struggle with this thought?",
                "What does fighting this thought cost you in terms of time and energy?",
                "How does getting caught up in this thought affect your behavior?",
                "What would be possible if this thought didn't have to control what you do?"
            ],
            values_connection="Connect defusion practice to values by exploring how getting caught up in thoughts prevents values-consistent behavior and how defusion creates space for valued action.",
            common_obstacles=[
                "Wanting thoughts to go away completely",
                "Believing defusion means the thoughts aren't important",
                "Difficulty with playful, non-serious approach",
                "Getting caught up in whether thoughts are true or false",
                "Feeling silly or resistant to experiential exercises"
            ],
            troubleshooting_strategies=[
                "Emphasize relationship with thoughts, not content",
                "Normalize resistance to playful exercises",
                "Start with less emotionally charged thoughts",
                "Use patient's preferred defusion techniques",
                "Connect to workability rather than truth"
            ],
            homework_assignments=[
                "Practice chosen defusion technique daily with specific thought",
                "Notice when caught up in thoughts vs. observing them",
                "Use 'thank your mind' with judgmental thoughts",
                "Experiment with different defusion techniques"
            ],
            therapeutic_rationale="Cognitive defusion reduces the impact of unhelpful thoughts by changing the relationship to them, creating psychological space for values-based action even in the presence of difficult thoughts.",
            clinical_considerations=[
                "Some patients may need psychoeducation about thoughts vs. reality",
                "Be sensitive to trauma-related thoughts that may need different approach",
                "Monitor for spiritual or religious concerns about 'not taking thoughts seriously'",
                "Adjust playfulness to patient's personality and comfort level"
            ]
        )
        
        # ACCEPTANCE PRACTICE PROMPTS
        prompts[(ACTProcess.ACCEPTANCE, ACTInterventionType.ACCEPTANCE_PRACTICE, SessionPhase.ACCEPTANCE_WORK)] = ACTPromptTemplate(
            process=ACTProcess.ACCEPTANCE,
            intervention_type=ACTInterventionType.ACCEPTANCE_PRACTICE,
            phase=SessionPhase.ACCEPTANCE_WORK,
            primary_prompt="""
You are guiding acceptance practice, which involves willingness to experience difficult internal experiences without struggling against them. This is about psychological willingness, not passive resignation.

Say: "Acceptance in ACT doesn't mean giving up or liking difficult experiences. It means being willing to have them as part of your human experience while you move toward what matters to you. It's like making room for difficult emotions and sensations."

Focus on experiential practice of willingness and openness to internal experiences that the patient typically struggles against.
""",
            experiential_instructions=[
                "Begin with mindful awareness of current internal experience",
                "Identify specific emotions, sensations, or thoughts patient struggles against",
                "Practice 'breathing with' difficult feelings rather than fighting them",
                "Use 'making room' visualization for difficult emotions",
                "Practice the 'struggle switch' exercise",
                "Explore willingness vs. wanting - being willing without wanting the experience"
            ],
            metaphors_to_use=[
                "Emotions as weather patterns - you can experience them without being harmed",
                "Struggle switch - you can choose to turn off the struggle",
                "Quicksand - struggling makes you sink, acceptance allows you to float",
                "Tug of war with anxiety monster - dropping the rope ends the struggle"
            ],
            follow_up_questions=[
                "What's it like to breathe with this feeling instead of fighting it?",
                "What do you notice when you make room for this emotion?",
                "How does your relationship to this feeling change with acceptance?",
                "What becomes possible when you're not spending energy fighting this feeling?",
                "What would willingness look like in this situation?"
            ],
            workability_questions=[
                "How much energy do you spend struggling against this feeling?",
                "What does fighting this emotion cost you?",
                "How does avoidance of this feeling affect your life choices?",
                "What would be different if you could have this feeling and still move toward your values?"
            ],
            values_connection="Connect acceptance to values by exploring how struggling against internal experiences prevents valued action and how acceptance creates space to pursue what matters.",
            common_obstacles=[
                "Confusing acceptance with approval or resignation",
                "Fear that accepting feelings will make them worse or permanent",
                "Belief that they should fight against negative emotions",
                "Difficulty distinguishing acceptance from suppression",
                "Cultural messages about not accepting negative emotions"
            ],
            troubleshooting_strategies=[
                "Clarify acceptance vs. approval through metaphors",
                "Start with less intense emotions to practice acceptance",
                "Use willingness language rather than acceptance",
                "Explore the workability of struggle vs. acceptance",
                "Connect to patient's values as motivation for acceptance"
            ],
            homework_assignments=[
                "Practice mindful acceptance with one difficult emotion daily",
                "Notice when struggling vs. accepting internal experiences",
                "Use 'making room' technique with challenging feelings",
                "Practice willingness exercises during difficult moments"
            ],
            therapeutic_rationale="Acceptance reduces emotional suffering by ending the struggle against inevitable human experiences, freeing up psychological resources for values-based living.",
            clinical_considerations=[
                "Ensure patient doesn't interpret acceptance as passive resignation",
                "Be careful with trauma-related emotions that may need specialized approach",
                "Monitor for dissociation during acceptance exercises",
                "Adjust pace based on patient's emotional regulation capacity"
            ]
        )
        
        # COMMITTED ACTION PROMPTS
        prompts[(ACTProcess.COMMITTED_ACTION, ACTInterventionType.COMMITTED_ACTION_PLANNING, SessionPhase.COMMITTED_ACTION)] = ACTPromptTemplate(
            process=ACTProcess.COMMITTED_ACTION,
            intervention_type=ACTInterventionType.COMMITTED_ACTION_PLANNING,
            phase=SessionPhase.COMMITTED_ACTION,
            primary_prompt="""
You are facilitating committed action planning - translating values into specific, concrete behaviors. This is where psychological flexibility leads to meaningful behavior change.

Say: "Now we're going to work on committed action - taking specific steps in the direction of your values, even when it's difficult. This isn't about perfection, but about consistently choosing values-based actions, learning from setbacks, and recommitting."

Focus on creating specific, values-based action plans with built-in flexibility and self-compassion for inevitable setbacks.
""",
            experiential_instructions=[
                "Review identified values and current behavior patterns",
                "Choose one specific value to focus on for action planning",
                "Identify specific, observable behaviors that serve this value",
                "Create SMART goals that are values-consistent",
                "Anticipate obstacles and plan for them using ACT skills",
                "Develop recommitment strategies for when setbacks occur"
            ],
            metaphors_to_use=[
                "Values as compass direction - committed action as taking steps",
                "Skiing down a mountain - falling is part of the process",
                "Learning to ride a bicycle - falling and getting back on",
                "Planting a garden - consistent tending, not perfect conditions"
            ],
            follow_up_questions=[
                "How does this action serve your value?",
                "What internal barriers might show up when you try to do this?",
                "How will you know if you're moving toward or away from your values?",
                "What would self-compassion look like if you have a setback?",
                "How can you recommit when you notice you've gotten off track?"
            ],
            workability_questions=[
                "How workable has your current pattern been for living this value?",
                "What would need to change to make this commitment sustainable?",
                "How does this action plan fit with your real-life circumstances?",
                "What support do you need to follow through with this commitment?"
            ],
            values_connection="Directly connect all planned actions to specific values, ensuring that commitments are values-driven rather than goal-driven or externally motivated.",
            common_obstacles=[
                "Making commitments too large or overwhelming",
                "Perfectionist expectations about consistency",
                "Lack of specific, observable action steps",
                "Not planning for predictable obstacles",
                "Viewing setbacks as failures rather than learning opportunities"
            ],
            troubleshooting_strategies=[
                "Start with very small, achievable steps",
                "Build in flexibility and self-compassion for setbacks",
                "Create if-then plans for anticipated obstacles",
                "Focus on process goals rather than outcome goals",
                "Use values as motivation for recommitment"
            ],
            homework_assignments=[
                "Implement specific committed action for one week",
                "Track values-consistency of daily actions",
                "Practice recommitment after setbacks",
                "Notice and challenge barriers to committed action"
            ],
            therapeutic_rationale="Committed action translates psychological flexibility into meaningful behavior change, creating a life consistent with values while building patterns of recommitment after inevitable setbacks.",
            clinical_considerations=[
                "Ensure commitments are realistic given patient's current life circumstances",
                "Address perfectionism that might sabotage commitment",
                "Build in adequate support systems for follow-through",
                "Monitor for depression or anxiety that might interfere with action",
                "Celebrate process rather than just outcomes"
            ]
        )
        
        # MINDFULNESS PRACTICE PROMPTS
        prompts[(ACTProcess.PRESENT_MOMENT_AWARENESS, ACTInterventionType.MINDFULNESS_MEDITATION, SessionPhase.CENTERING)] = ACTPromptTemplate(
            process=ACTProcess.PRESENT_MOMENT_AWARENESS,
            intervention_type=ACTInterventionType.MINDFULNESS_MEDITATION,
            phase=SessionPhase.CENTERING,
            primary_prompt="""
You are guiding ACT-specific mindfulness practice focused on present-moment awareness and contacting the observing self. This differs from some mindfulness traditions by emphasizing psychological flexibility.

Say: "We're going to practice contacting the present moment and the part of you that observes your experiences. This helps you step out of the content of your mind and into the perspective from which you can choose how to respond."

Focus on awareness practices that support the other ACT processes and enhance psychological flexibility.
""",
            experiential_instructions=[
                "Begin with grounding in physical sensations and breath",
                "Guide awareness to thoughts and feelings without changing them",
                "Practice 'self-as-context' - the observing self",
                "Notice the difference between experiencing and observing experience",
                "Practice flexible attention - choosing where to focus awareness",
                "Connect present-moment awareness to values and choice"
            ],
            metaphors_to_use=[
                "Consciousness as the sky, experiences as weather",
                "Self as the chessboard, thoughts/feelings as chess pieces",
                "Awareness as a flashlight that can be directed anywhere",
                "Observing self as the theater, experiences as the play"
            ],
            follow_up_questions=[
                "What do you notice about the part of you that's observing right now?",
                "How does it feel to watch your thoughts rather than being caught in them?",
                "What's available to you when you're in contact with this observing perspective?",
                "How might this awareness help you in difficult moments?",
                "What choices become available from this observing perspective?"
            ],
            workability_questions=[
                "How does present-moment awareness serve your values?",
                "What becomes possible when you're not lost in thoughts about past or future?",
                "How does this observing perspective help with difficult emotions?",
                "What would daily life be like with more access to this awareness?"
            ],
            values_connection="Connect mindfulness to values by exploring how present-moment awareness creates space for values-based choices and prevents automatic, values-inconsistent reactions.",
            common_obstacles=[
                "Expecting mindfulness to eliminate difficult thoughts or feelings",
                "Getting caught up in 'doing it right'",
                "Difficulty accessing observing self perspective",
                "Restlessness or resistance to sitting still",
                "Comparing ACT mindfulness to other meditation practices"
            ],
            troubleshooting_strategies=[
                "Emphasize awareness rather than relaxation as the goal",
                "Use eyes-open options for those who struggle with eyes closed",
                "Start with very brief practices (2-3 minutes)",
                "Normalize wandering mind as part of the practice",
                "Connect to functional outcomes rather than perfect execution"
            ],
            homework_assignments=[
                "Practice brief mindfulness sessions daily",
                "Use present-moment awareness during daily activities",
                "Notice when lost in thoughts vs. present to experience",
                "Practice observing self perspective during difficult moments"
            ],
            therapeutic_rationale="Present-moment awareness and self-as-context create the psychological foundation for all other ACT processes by providing perspective and choice in responding to internal experiences.",
            clinical_considerations=[
                "Adapt practices for trauma history or dissociation concerns",
                "Consider cultural or religious background regarding meditation",
                "Start with shorter practices and build gradually",
                "Emphasize functional benefits rather than spiritual aspects",
                "Monitor for increased anxiety in some patients during mindfulness"
            ]
        )
        
        return prompts
    
    def _initialize_values_guides(self) -> Dict[ValuesArea, Dict[str, Any]]:
        """Initialize values exploration guides for different life domains"""
        
        return {
            ValuesArea.FAMILY_RELATIONSHIPS: {
                "exploration_questions": [
                    "What kind of family member do you want to be?",
                    "How do you want to show up in family interactions?",
                    "What legacy do you want to leave with your family?",
                    "How do you want family members to experience you?"
                ],
                "values_examples": [
                    "Love, support, presence, honesty, fun, tradition, growth, acceptance"
                ],
                "behavioral_indicators": [
                    "Regular communication with family",
                    "Being present during family time",
                    "Showing affection and care",
                    "Creating family traditions"
                ]
            },
            
            ValuesArea.CAREER_WORK: {
                "exploration_questions": [
                    "What do you want your work to contribute to the world?",
                    "How do you want to be as a colleague or leader?",
                    "What would make your work feel meaningful?",
                    "What kind of professional legacy do you want?"
                ],
                "values_examples": [
                    "Excellence, service, creativity, integrity, collaboration, learning, impact"
                ],
                "behavioral_indicators": [
                    "Pursuing skill development",
                    "Contributing meaningfully to projects",
                    "Supporting colleagues",
                    "Maintaining professional standards"
                ]
            },
            
            ValuesArea.HEALTH_PHYSICAL_CARE: {
                "exploration_questions": [
                    "How do you want to care for your body?",
                    "What does self-respect look like in terms of health?",
                    "How do you want to age?",
                    "What kind of relationship do you want with your physical self?"
                ],
                "values_examples": [
                    "Vitality, self-care, strength, balance, nourishment, movement, longevity"
                ],
                "behavioral_indicators": [
                    "Regular exercise or movement",
                    "Nutritious eating habits",
                    "Adequate sleep",
                    "Regular medical care"
                ]
            },
            
            ValuesArea.PERSONAL_GROWTH: {
                "exploration_questions": [
                    "How do you want to grow and develop as a person?",
                    "What does living authentically mean to you?",
                    "How do you want to handle life's challenges?",
                    "What kind of person do you want to become?"
                ],
                "values_examples": [
                    "Wisdom, courage, authenticity, resilience, self-awareness, growth"
                ],
                "behavioral_indicators": [
                    "Engaging in self-reflection",
                    "Learning from experiences",
                    "Seeking feedback and growth opportunities",
                    "Practicing self-compassion"
                ]
            }
        }
    
    def _initialize_defusion_techniques(self) -> Dict[DefusionTechnique, Dict[str, Any]]:
        """Initialize cognitive defusion technique guidance"""
        
        return {
            DefusionTechnique.IM_HAVING_THE_THOUGHT: {
                "description": "Prefacing thoughts with 'I'm having the thought that...'",
                "instructions": [
                    "Identify a specific troubling thought",
                    "Have patient state it normally first",
                    "Then repeat with 'I'm having the thought that...' prefix",
                    "Notice any difference in how the thought feels",
                    "Can extend to 'I notice I'm having the thought that...'"
                ],
                "suitable_for": ["beginners", "intellectually-oriented patients"],
                "example": "'I'm a failure' becomes 'I'm having the thought that I'm a failure'"
            },
            
            DefusionTechnique.SILLY_VOICE: {
                "description": "Saying the thought in a cartoon or silly voice",
                "instructions": [
                    "Choose a difficult thought",
                    "Have patient say it in Mickey Mouse or other cartoon voice",
                    "Try different silly voices",
                    "Notice impact on believability",
                    "Can also try slow motion or speeded up versions"
                ],
                "suitable_for": ["patients open to playfulness", "children"],
                "example": "Saying 'I'm worthless' in Elmo's voice"
            },
            
            DefusionTechnique.LEAVES_ON_STREAM: {
                "description": "Visualizing thoughts as leaves floating on a stream",
                "instructions": [
                    "Guide relaxation and visualization",
                    "Imagine sitting by a gently flowing stream",
                    "Place each thought on a leaf",
                    "Watch the leaf float downstream",
                    "If mind wanders, gently place the wandering on a leaf too",
                    "Continue for 5-10 minutes"
                ],
                "suitable_for": ["visual learners", "those comfortable with meditation"],
                "example": "Placing 'I'm anxious about tomorrow' on a leaf and watching it float away"
            },
            
            DefusionTechnique.THANK_YOUR_MIND: {
                "description": "Thanking the mind for producing thoughts",
                "instructions": [
                    "When difficult thought arises, say 'Thank you, mind'",
                    "Can add specifics: 'Thank you mind for that worry'",
                    "Practice with appreciation rather than sarcasm",
                    "Notice mind's attempt to be helpful, even when unhelpful",
                    "Use consistently throughout the day"
                ],
                "suitable_for": ["those who struggle with self-criticism", "mindfulness practitioners"],
                "example": "Thank you, mind, for trying to protect me with that worry"
            },
            
            DefusionTechnique.COMPUTER_SCREEN: {
                "description": "Visualizing thoughts as text on a computer screen",
                "instructions": [
                    "Imagine the thought appearing as text on a screen",
                    "Practice changing the font, size, or color",
                    "Try different backgrounds or scrolling speeds",
                    "Notice the thought as data rather than reality",
                    "Can minimize the window or close the program"
                ],
                "suitable_for": ["tech-savvy individuals", "visual processors"],
                "example": "Seeing 'I'll never succeed' in Comic Sans font on a colorful background"
            },
            
            DefusionTechnique.THOUGHTS_AS_VISITORS: {
                "description": "Treating thoughts as visitors to your mental house",
                "instructions": [
                    "Imagine thoughts as different characters visiting",
                    "Greet them politely but don't invite them to stay",
                    "Some visitors are helpful, others less so",
                    "You can acknowledge visitors without following their advice",
                    "Set boundaries with pushy or unwelcome visitors"
                ],
                "suitable_for": ["those who like story metaphors", "boundary issues"],
                "example": "Greeting 'Worry' as a visitor but not letting it redecorate your house"
            }
        }
    
    def _initialize_metaphor_library(self) -> Dict[str, Dict[str, Any]]:
        """Initialize ACT metaphor library for different purposes"""
        
        return {
            "psychological_flexibility": {
                "tug_of_war_with_monster": {
                    "purpose": "Illustrate futility of fighting anxiety/depression",
                    "metaphor": "You're in a tug of war with an anxiety monster over a pit. The harder you pull, the more tired you get. But what if you dropped the rope?",
                    "therapeutic_point": "Fighting psychological symptoms often makes them stronger",
                    "follow_up": "What would dropping the rope look like in your situation?"
                },
                "quicksand": {
                    "purpose": "Explain acceptance vs. struggle",
                    "metaphor": "Struggling in quicksand makes you sink faster. The way out is to relax, spread your weight, and move slowly and deliberately.",
                    "therapeutic_point": "Struggling against emotions makes them more intense",
                    "follow_up": "How might you 'spread your weight' with this difficult emotion?"
                }
            },
            
            "values_and_commitment": {
                "compass": {
                    "purpose": "Distinguish values from goals",
                    "metaphor": "Values are like a compass direction - you can always move north, but you never arrive at north. Goals are like destinations you reach.",
                    "therapeutic_point": "Values provide ongoing direction for behavior",
                    "follow_up": "What direction does your values compass point?"
                },
                "garden": {
                    "purpose": "Illustrate ongoing values work",
                    "metaphor": "Living your values is like tending a garden. You don't plant once and expect it to thrive forever. It requires ongoing attention, watering, and care.",
                    "therapeutic_point": "Values require consistent, ongoing attention",
                    "follow_up": "How have you been tending your values garden lately?"
                }
            },
            
            "cognitive_defusion": {
                "radio": {
                    "purpose": "Relationship with thoughts",
                    "metaphor": "Your mind is like a radio that sometimes tunes to unhelpful stations. You can't control what it picks up, but you can choose how much attention to give it.",
                    "therapeutic_point": "We can observe thoughts without being controlled by them",
                    "follow_up": "What station is your mind tuned to right now?"
                },
                "bus_driver": {
                    "purpose": "Self-as-context and choice",
                    "metaphor": "You're the bus driver of your life. Thoughts and emotions are passengers who might yell directions, but you decide where the bus goes.",
                    "therapeutic_point": "We can acknowledge internal experiences while maintaining choice over behavior",
                    "follow_up": "Who's been driving your bus lately - you or the passengers?"
                }
            },
            
            "acceptance": {
                "weather": {
                    "purpose": "Temporary nature of emotions",
                    "metaphor": "Emotions are like weather patterns. Storms can be intense, but they always pass. You don't have to like the storm, just weather it.",
                    "therapeutic_point": "Difficult emotions are temporary and survivable",
                    "follow_up": "What kind of weather are you experiencing emotionally right now?"
                },
                "unwanted_party_guest": {
                    "purpose": "Willingness vs. wanting",
                    "metaphor": "Anxiety is like an unwanted party guest. You can't force them to leave, but you don't have to like them or let them ruin your party.",
                    "therapeutic_point": "We can be willing to have experiences we don't want",
                    "follow_up": "How might you make room for this unwanted guest?"
                }
            }
        }
    
    def _initialize_acceptance_exercises(self) -> Dict[str, Dict[str, Any]]:
        """Initialize acceptance and willingness exercises"""
        
        return {
            "making_room": {
                "description": "Visualization exercise for accepting difficult emotions",
                "instructions": [
                    "Identify the difficult emotion or sensation",
                    "Imagine your body as a large, spacious house",
                    "Find where the emotion lives in your house",
                    "Breathe and create more space around the emotion",
                    "Don't try to get rid of it, just make room",
                    "Notice you're bigger than any single emotion"
                ],
                "duration": "5-10 minutes",
                "suitable_for": ["visual learners", "those who feel overwhelmed by emotions"]
            },
            
            "struggle_switch": {
                "description": "Exercise to explore choice in struggling with experience",
                "instructions": [
                    "Identify something you're struggling against",
                    "Imagine a struggle switch in your mind",
                    "Notice the switch is currently 'on'",
                    "Experiment with turning the switch 'off'",
                    "What happens to the experience when you stop struggling?",
                    "Practice turning the switch off throughout the day"
                ],
                "duration": "3-5 minutes",
                "suitable_for": ["those who fight their emotions", "anxiety and depression"]
            },
            
            "willing_hands": {
                "description": "Physical gesture to practice willingness",
                "instructions": [
                    "Make fists with your hands (representing struggle)",
                    "Notice the tension and effort required",
                    "Slowly open your hands, palms up (representing willingness)",
                    "Feel the relaxation and openness",
                    "Use this gesture when practicing acceptance",
                    "Connect the physical opening to psychological willingness"
                ],
                "duration": "2-3 minutes",
                "suitable_for": ["kinesthetic learners", "those who like concrete gestures"]
            },
            
            "breathing_with": {
                "description": "Using breath to practice acceptance",
                "instructions": [
                    "Identify the difficult emotion or sensation",
                    "Breathe naturally, not trying to change anything",
                    "On the inhale, breathe 'with' the difficult experience",
                    "On the exhale, make space for it",
                    "Continue breathing with rather than against the experience",
                    "Notice any softening or shift in relationship"
                ],
                "duration": "5-10 minutes",
                "suitable_for": ["beginners", "those comfortable with breathing exercises"]
            }
        }
    
    def _initialize_mindfulness_practices(self) -> Dict[str, Dict[str, Any]]:
        """Initialize ACT-specific mindfulness practices"""
        
        return {
            "observing_self": {
                "description": "Contacting the part of you that observes experience",
                "instructions": [
                    "Sit comfortably and notice your breathing",
                    "Notice thoughts and feelings arising",
                    "Ask: 'Who is noticing these thoughts and feelings?'",
                    "Contact the observer - the part that's always been there",
                    "Rest in the perspective of the observing self",
                    "Notice this observer is different from what it observes"
                ],
                "benefits": ["Self-as-context", "Psychological flexibility", "Perspective-taking"],
                "duration": "10-20 minutes"
            },
            
            "mindful_values_connection": {
                "description": "Mindfulness practice connected to values",
                "instructions": [
                    "Begin with mindful breathing",
                    "Bring to mind one of your core values",
                    "Notice what the value feels like in your body",
                    "Breathe with the felt sense of this value",
                    "Connect to the deeper 'why' of your life",
                    "End with intention to live this value today"
                ],
                "benefits": ["Values connection", "Motivation", "Present-moment awareness"],
                "duration": "5-15 minutes"
            },
            
            "thoughts_and_feelings_practice": {
                "description": "Observing thoughts and feelings without getting caught",
                "instructions": [
                    "Sit quietly and notice your breath",
                    "When thoughts arise, label them 'thinking'",
                    "When emotions arise, label them 'feeling'",
                    "Don't try to stop or change, just notice and label",
                    "Return attention to breath when ready",
                    "Practice being the observer rather than the observed"
                ],
                "benefits": ["Defusion", "Present-moment awareness", "Self-as-context"],
                "duration": "10-30 minutes"
            }
        }
    
    def _format_act_context(self, context: ACTContext, session_info: Dict[str, Any] = None) -> str:
        """Format ACT-specific context information"""
        
        context_lines = [
            f"Patient ID: {context.patient_id}",
            f"Psychological Flexibility Level: {context.psychological_flexibility_level}",
            f"Values-Behavior Gap: {context.values_behavior_gap}",
            f"Mindfulness Experience: {context.mindfulness_experience}",
            f"Resistance to Acceptance: {context.resistance_to_acceptance}",
            f"Commitment History: {context.commitment_history}"
        ]
        
        if context.identified_values:
            values_strings = [f"{area.value}: {description}" for area, description in context.identified_values]
            context_lines.append(f"Identified Values: {'; '.join(values_strings)}")
        
        if context.primary_avoidance_patterns:
            context_lines.append(f"Avoidance Patterns: {', '.join(context.primary_avoidance_patterns)}")
        
        if context.fusion_with_thoughts:
            context_lines.append(f"Thought Fusion Areas: {', '.join(context.fusion_with_thoughts)}")
        
        if context.workability_concerns:
            context_lines.append(f"Workability Concerns: {', '.join(context.workability_concerns)}")
        
        if context.current_life_struggles:
            context_lines.append(f"Current Struggles: {', '.join(context.current_life_struggles)}")
        
        if context.preferred_metaphors:
            context_lines.append(f"Preferred Metaphors: {', '.join(context.preferred_metaphors)}")
        
        if context.cultural_values_considerations:
            context_lines.append(f"Cultural Considerations: {', '.join(context.cultural_values_considerations)}")
        
        return chr(10).join(context_lines)
    
    def _get_generic_act_prompt(self, process: ACTProcess, intervention_type: ACTInterventionType, phase: SessionPhase) -> str:
        """Generate generic ACT prompt when specific template not found"""
        
        return f"""
You are implementing {process.value.replace('_', ' ')} using {intervention_type.value.replace('_', ' ')} in the {phase.value.replace('_', ' ')} phase.

ACT APPROACH PRINCIPLES:
- Focus on workability rather than truth or logic
- Use experiential exercises rather than just talking about concepts
- Connect all work back to patient's values
- Embrace paradox and creative hopelessness when appropriate
- Use metaphors and experiential learning extensively
- Maintain focus on psychological flexibility as overarching goal

ACT CORE PROCESSES:
- Present moment awareness and self-as-context
- Acceptance and willingness to experience
- Cognitive defusion from unhelpful thoughts
- Values clarification and connection
- Committed action toward values
- Psychological flexibility development

Continue with ACT intervention appropriate for {process.value.replace('_', ' ')}.
"""
    
    def get_values_exploration_prompt(
        self,
        values_area: ValuesArea,
        context: ACTContext,
        depth_level: str = "initial"
    ) -> str:
        """Generate values exploration prompt for specific life domain"""
        
        values_guide = self.values_exploration_guides.get(values_area, {})
        
        prompt = f"""
VALUES EXPLORATION: {values_area.value.replace('_', ' ').title()}

PATIENT CONTEXT:
{self._format_act_context(context)}

VALUES AREA FOCUS: {values_area.value.replace('_', ' ').title()}

"""
        
        if depth_level == "initial":
            prompt += f"""
INITIAL EXPLORATION APPROACH:
- Start with broad, open-ended questions
- Help patient connect with authentic desires vs. "shoulds"
- Use concrete examples and behavioral indicators
- Explore what this area means personally to them

EXPLORATION QUESTIONS:
"""
            for question in values_guide.get('exploration_questions', []):
                prompt += f"• {question}\n"
        
        elif depth_level == "deep":
            prompt += f"""
DEEP EXPLORATION APPROACH:
- Explore the felt sense and meaning of values in this area
- Connect to childhood dreams and authentic desires
- Address any conflicts between personal and cultural values
- Identify specific behavioral expressions of these values

DEEP EXPLORATION QUESTIONS:
• What would this value look like if you lived it fully?
• What gets in the way of expressing this value?
• How would someone who didn't know you see this value in your life?
• What would you regret not doing in this area of life?
"""
        
        if 'values_examples' in values_guide:
            prompt += f"""
COMMON VALUES IN THIS AREA:
{', '.join(values_guide['values_examples'])}
(Use these as prompts, not prescribed answers)
"""
        
        if 'behavioral_indicators' in values_guide:
            prompt += f"""
BEHAVIORAL INDICATORS TO EXPLORE:
"""
            for indicator in values_guide['behavioral_indicators']:
                prompt += f"• {indicator}\n"
        
        prompt += f"""
ACT VALUES PRINCIPLES:
- Values are chosen directions, not goals to achieve
- Focus on intrinsic motivation, not external validation
- Values can be lived imperfectly and still be meaningful
- Different life phases may emphasize different values
- Values conflicts are normal and workable

THERAPEUTIC APPROACH:
- Use experiential exercises to connect with felt sense of values
- Help distinguish authentic values from imposed "shoulds"
- Explore values without judgment about current behavior
- Connect values to committed action planning
- Address any guilt about past values-inconsistent behavior

Remember: The goal is authentic connection with personally meaningful directions, not finding the "right" values.
"""
        
        return prompt
    
    def get_defusion_technique_prompt(
        self,
        technique: DefusionTechnique,
        specific_thought: str,
        context: ACTContext
    ) -> str:
        """Generate prompt for specific defusion technique with specific thought"""
        
        technique_info = self.defusion_techniques.get(technique, {})
        
        prompt = f"""
COGNITIVE DEFUSION TECHNIQUE: {technique_info.get('description', technique.value)}

PATIENT CONTEXT:
{self._format_act_context(context)}

TARGET THOUGHT: "{specific_thought}"

TECHNIQUE INSTRUCTIONS:
"""
        
        for i, instruction in enumerate(technique_info.get('instructions', []), 1):
            prompt += f"{i}. {instruction}\n"
        
        if 'example' in technique_info:
            prompt += f"\nEXAMPLE: {technique_info['example']}\n"
        
        prompt += f"""
SPECIFIC APPLICATION:
Working with the thought "{specific_thought}", guide the patient through this defusion technique step by step.

FOLLOW-UP QUESTIONS:
• What do you notice about the thought when you do this exercise?
• How does the believability or impact of the thought change?
• What's it like to observe the thought rather than being caught in it?
• How might this technique be useful in daily life with this thought?

COACHING POINTS:
• The goal is not to eliminate the thought or make it positive
• Focus on changing relationship to the thought, not its content
• Some techniques may feel silly initially - that's normal and helpful
• Practice builds skill in defusion
• Connect back to workability and values

TROUBLESHOOTING:
• If technique feels too silly, try a different approach
• If patient gets more caught up in thought, slow down and simplify
• If no change noticed, explore what they're expecting vs. what's actually happening
• Normalize that defusion is a skill that develops with practice

Remember: Defusion creates psychological space for values-based action even when difficult thoughts are present.
"""
        
        return prompt
    
    def get_metaphor_prompt(
        self,
        metaphor_category: str,
        specific_metaphor: str,
        context: ACTContext,
        patient_situation: str
    ) -> str:
        """Generate prompt for using specific ACT metaphor"""
        
        metaphor_info = self.metaphor_library.get(metaphor_category, {}).get(specific_metaphor, {})
        
        prompt = f"""
ACT METAPHOR: {specific_metaphor.replace('_', ' ').title()}

PATIENT CONTEXT:
{self._format_act_context(context)}

PATIENT SITUATION: {patient_situation}

METAPHOR PURPOSE: {metaphor_info.get('purpose', 'Illustrate ACT principle')}

THE METAPHOR:
{metaphor_info.get('metaphor', 'Metaphor content not found')}

THERAPEUTIC POINT: {metaphor_info.get('therapeutic_point', 'ACT principle illustration')}

IMPLEMENTATION APPROACH:
1. Set up the metaphor with engaging storytelling
2. Help patient see parallels to their situation
3. Explore the metaphor without over-explaining
4. Let patient discover insights rather than telling them
5. Connect metaphor to concrete next steps

KEY FOLLOW-UP QUESTION:
{metaphor_info.get('follow_up', 'How does this metaphor relate to your situation?')}

ADDITIONAL EXPLORATION:
• What part of this metaphor resonates most with you?
• How might your situation be similar to what we've described?
• What would the metaphor suggest as a next step?
• What wisdom does this metaphor offer for your situation?

METAPHOR PRINCIPLES:
• Use vivid, experiential language
• Allow patient to make their own connections
• Don't over-explain or analyze the metaphor
• Return to the metaphor throughout treatment
• Use patient's own imagery and experiences when possible

CONNECTING TO ACT PROCESSES:
Connect this metaphor to relevant ACT processes and encourage patient to use it as a reference point for understanding their psychological experiences.

Remember: Metaphors work by creating experiential understanding, not intellectual analysis.
"""
        
        return prompt
    
    def get_committed_action_review_prompt(
        self,
        previous_commitments: List[Dict[str, Any]],
        context: ACTContext
    ) -> str:
        """Generate prompt for reviewing committed action progress"""
        
        prompt = f"""
COMMITTED ACTION REVIEW

PATIENT CONTEXT:
{self._format_act_context(context)}

PREVIOUS COMMITMENTS:
"""
        
        for i, commitment in enumerate(previous_commitments, 1):
            prompt += f"""
{i}. {commitment.get('action', 'Not specified')}
   Value: {commitment.get('value', 'Not specified')}
   Completion: {commitment.get('completion_rate', 'Not reported')}%
   Barriers: {', '.join(commitment.get('barriers', []))}
"""
        
        prompt += f"""
REVIEW APPROACH:
1. Celebrate any movement toward values, however small
2. Explore barriers with curiosity, not judgment
3. Assess workability of current approach
4. Practice recommitment to values
5. Adjust action plans based on learning

REVIEW QUESTIONS:
• What did you learn about yourself through these commitments?
• Which actions felt most connected to your values?
• What barriers showed up that we hadn't anticipated?
• How did you handle setbacks or missed commitments?
• What would self-compassion look like around any struggles?
• How might we adjust the approach moving forward?

BARRIERS EXPLORATION:
For each barrier identified, explore:
• Is this barrier controllable or uncontrollable?
• What ACT skills might help with this barrier?
• How could you work with this barrier differently?
• What would willingness look like with this barrier?

RECOMMITMENT PROCESS:
• Reconnect with the underlying values
• Acknowledge any self-judgment with compassion
• Adjust commitments to be more workable
• Practice flexible persistence rather than rigid adherence
• Focus on direction rather than perfect execution

ACT PRINCIPLES FOR REVIEW:
• Progress is not linear - setbacks are part of the process
• The goal is learning and growth, not perfect performance
• Recommitment is a skill that can be strengthened
• Values provide motivation for getting back on track
• Self-compassion enhances rather than undermines commitment

PLANNING NEXT STEPS:
Based on the review, collaboratively plan adjusted committed actions that:
• Are realistically achievable given current circumstances
• Clearly connect to identified values
• Include strategies for anticipated barriers
• Build in self-compassion for inevitable imperfection
• Focus on sustainable, long-term behavior change

Remember: The review itself is an act of self-compassion and values-based living.
"""
        
        return prompt


class ACTWorkflow:
    """Manages ACT-specific therapeutic workflow"""
    
    def __init__(self):
        self.prompts = ACTTherapeuticPrompts()
        self.session_structures = self._initialize_session_structures()
    
    def _initialize_session_structures(self) -> Dict[str, List[SessionPhase]]:
        """Initialize ACT-specific session structures"""
        
        return {
            "values_focused_session": [
                SessionPhase.CENTERING,
                SessionPhase.VALUES_CHECK_IN,
                SessionPhase.VALUES_EXPLORATION,
                SessionPhase.COMMITTED_ACTION,
                SessionPhase.HOMEWORK_ASSIGNMENT,
                SessionPhase.CLOSING_MINDFULNESS
            ],
            
            "defusion_focused_session": [
                SessionPhase.CENTERING,
                SessionPhase.VALUES_CHECK_IN,
                SessionPhase.DEFUSION_PRACTICE,
                SessionPhase.COMMITTED_ACTION,
                SessionPhase.HOMEWORK_ASSIGNMENT,
                SessionPhase.CLOSING_MINDFULNESS
            ],
            
            "acceptance_focused_session": [
                SessionPhase.CENTERING,
                SessionPhase.VALUES_CHECK_IN,
                SessionPhase.ACCEPTANCE_WORK,
                SessionPhase.COMMITTED_ACTION,
                SessionPhase.HOMEWORK_ASSIGNMENT,
                SessionPhase.CLOSING_MINDFULNESS
            ],
            
            "integration_session": [
                SessionPhase.CENTERING,
                SessionPhase.VALUES_CHECK_IN,
                SessionPhase.WORKABILITY_ASSESSMENT,
                SessionPhase.INTEGRATION,
                SessionPhase.COMMITTED_ACTION,
                SessionPhase.CLOSING_MINDFULNESS
            ]
        }
    
    def get_session_prompt(
        self,
        session_type: str,
        current_phase: SessionPhase,
        context: ACTContext,
        session_number: int = 1
    ) -> str:
        """Get session-appropriate ACT prompt"""
        
        session_structure = self.session_structures.get(session_type, [])
        
        if current_phase not in session_structure:
            return self.prompts._get_generic_act_prompt(
                ACTProcess.PSYCHOLOGICAL_FLEXIBILITY,
                ACTInterventionType.PSYCHOLOGICAL_FLEXIBILITY_TRAINING,
                current_phase
            )
        
        phase_index = session_structure.index(current_phase)
        total_phases = len(session_structure)
        
        # Generate appropriate prompt based on session type and phase
        if session_type == "values_focused_session" and current_phase == SessionPhase.VALUES_EXPLORATION:
            base_prompt = self.prompts.get_act_prompt(
                ACTProcess.VALUES_CLARIFICATION,
                ACTInterventionType.VALUES_EXPLORATION,
                SessionPhase.VALUES_EXPLORATION,
                context
            )
        elif session_type == "defusion_focused_session" and current_phase == SessionPhase.DEFUSION_PRACTICE:
            base_prompt = self.prompts.get_act_prompt(
                ACTProcess.COGNITIVE_DEFUSION,
                ACTInterventionType.COGNITIVE_DEFUSION,
                SessionPhase.DEFUSION_PRACTICE,
                context
            )
        elif session_type == "acceptance_focused_session" and current_phase == SessionPhase.ACCEPTANCE_WORK:
            base_prompt = self.prompts.get_act_prompt(
                ACTProcess.ACCEPTANCE,
                ACTInterventionType.ACCEPTANCE_PRACTICE,
                SessionPhase.ACCEPTANCE_WORK,
                context
            )
        else:
            base_prompt = self.prompts._get_generic_act_prompt(
                ACTProcess.PSYCHOLOGICAL_FLEXIBILITY,
                ACTInterventionType.PSYCHOLOGICAL_FLEXIBILITY_TRAINING,
                current_phase
            )
        
        workflow_info = f"""
ACT SESSION WORKFLOW:
Session Type: {session_type.replace('_', ' ').title()}
Current Phase: {current_phase.value.replace('_', ' ').title()} ({phase_index + 1}/{total_phases})
Session Number: {session_number}

PHASES COMPLETED:
{chr(10).join(f"✓ {phase.value.replace('_', ' ').title()}" for phase in session_structure[:phase_index])}

UPCOMING PHASES:
{chr(10).join(f"• {phase.value.replace('_', ' ').title()}" for phase in session_structure[phase_index + 1:])}

"""
        
        return workflow_info + base_prompt


# Example usage and utility functions
def example_usage():
    """Example of how to use the ACT therapeutic prompt system"""
    
    # Initialize the ACT prompt system
    act_system = ACTTherapeuticPrompts()
    
    # Create patient context
    context = ACTContext(
        patient_id="PATIENT_001",
        session_id="SESSION_006",
        identified_values=[
            (ValuesArea.FAMILY_RELATIONSHIPS, "being present and loving"),
            (ValuesArea.CAREER_WORK, "helping others through my work"),
            (ValuesArea.PERSONAL_GROWTH, "living authentically")
        ],
        psychological_flexibility_level="developing",
        primary_avoidance_patterns=["avoiding difficult conversations", "procrastinating on important tasks"],
        fusion_with_thoughts=["I'm not good enough", "People will judge me"],
        workability_concerns=["perfectionism preventing action", "avoidance limiting relationships"],
        current_life_struggles=["work stress", "relationship difficulties"],
        values_behavior_gap="moderate",
        mindfulness_experience="some",
        resistance_to_acceptance="moderate",
        commitment_history="inconsistent",
        preferred_metaphors=["compass", "garden"],
        cultural_values_considerations=["family expectations", "cultural perfectionism"]
    )
    
    # Get values exploration prompt
    values_prompt = act_system.get_act_prompt(
        ACTProcess.VALUES_CLARIFICATION,
        ACTInterventionType.VALUES_EXPLORATION,
        SessionPhase.VALUES_EXPLORATION,
        context
    )
    
    print("ACT VALUES EXPLORATION PROMPT:")
    print("=" * 60)
    print(values_prompt)
    print("\n")
    
    # Get cognitive defusion prompt
    defusion_prompt = act_system.get_defusion_technique_prompt(
        DefusionTechnique.IM_HAVING_THE_THOUGHT,
        "I'm not good enough",
        context
    )
    
    print("COGNITIVE DEFUSION TECHNIQUE PROMPT:")
    print("=" * 60)
    print(defusion_prompt)
    print("\n")
    
    # Get metaphor prompt
    metaphor_prompt = act_system.get_metaphor_prompt(
        "psychological_flexibility",
        "tug_of_war_with_monster",
        context,
        "struggling with anxiety about work performance"
    )
    
    print("ACT METAPHOR PROMPT:")
    print("=" * 60)
    print(metaphor_prompt)
    print("\n")


if __name__ == "__main__":
    example_usage()
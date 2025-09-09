"""
Cognitive Intervention Prompts Module
Professional cognitive intervention prompts for AI therapy system
Specialized prompts for cognitive restructuring, thought challenging, distortion identification, and balanced thinking
"""

from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime, timedelta


class CognitiveInterventionType(Enum):
    """Types of cognitive interventions"""
    COGNITIVE_RESTRUCTURING = "cognitive_restructuring"
    THOUGHT_CHALLENGING = "thought_challenging"
    THOUGHT_RECORDS = "thought_records"
    DISTORTION_IDENTIFICATION = "distortion_identification"
    BALANCED_THINKING = "balanced_thinking"
    EVIDENCE_EXAMINATION = "evidence_examination"
    ALTERNATIVE_PERSPECTIVES = "alternative_perspectives"
    CATASTROPHIC_THINKING_CHALLENGE = "catastrophic_thinking_challenge"
    PROBABILITY_ESTIMATION = "probability_estimation"
    COST_BENEFIT_ANALYSIS = "cost_benefit_analysis"
    TIME_PERSPECTIVE = "time_perspective"
    DECATASTROPHIZING = "decatastrophizing"
    COGNITIVE_DEFUSION = "cognitive_defusion"


class ThoughtType(Enum):
    """Types of thoughts targeted in cognitive interventions"""
    AUTOMATIC_THOUGHTS = "automatic_thoughts"
    NEGATIVE_PREDICTIONS = "negative_predictions"
    SELF_CRITICAL_THOUGHTS = "self_critical_thoughts"
    WORRY_THOUGHTS = "worry_thoughts"
    CATASTROPHIC_THOUGHTS = "catastrophic_thoughts"
    PERFECTIONISTIC_THOUGHTS = "perfectionistic_thoughts"
    HOPELESS_THOUGHTS = "hopeless_thoughts"
    GUILT_SHAME_THOUGHTS = "guilt_shame_thoughts"
    ANGER_THOUGHTS = "anger_thoughts"
    CORE_BELIEFS = "core_beliefs"


class CognitiveDistortion(Enum):
    """Types of cognitive distortions"""
    ALL_OR_NOTHING = "all_or_nothing"
    OVERGENERALIZATION = "overgeneralization"
    MENTAL_FILTER = "mental_filter"
    DISQUALIFYING_POSITIVE = "disqualifying_positive"
    JUMPING_TO_CONCLUSIONS = "jumping_to_conclusions"
    MIND_READING = "mind_reading"
    FORTUNE_TELLING = "fortune_telling"
    MAGNIFICATION = "magnification"
    MINIMIZATION = "minimization"
    EMOTIONAL_REASONING = "emotional_reasoning"
    SHOULD_STATEMENTS = "should_statements"
    LABELING = "labeling"
    PERSONALIZATION = "personalization"
    BLAME = "blame"


class SessionPhase(Enum):
    """Phases of cognitive intervention sessions"""
    ASSESSMENT = "assessment"
    PSYCHOEDUCATION = "psychoeducation"
    THOUGHT_IDENTIFICATION = "thought_identification"
    DISTORTION_IDENTIFICATION = "distortion_identification"
    EVIDENCE_EXAMINATION = "evidence_examination"
    ALTERNATIVE_GENERATION = "alternative_generation"
    BALANCED_THINKING = "balanced_thinking"
    PRACTICE = "practice"
    HOMEWORK_ASSIGNMENT = "homework_assignment"
    REVIEW = "review"
    INTEGRATION = "integration"


class ChallengeMethod(Enum):
    """Methods for challenging thoughts"""
    SOCRATIC_QUESTIONING = "socratic_questioning"
    EVIDENCE_BASED = "evidence_based"
    ALTERNATIVE_PERSPECTIVES = "alternative_perspectives"
    BEHAVIORAL_EXPERIMENTS = "behavioral_experiments"
    COST_BENEFIT = "cost_benefit"
    WORST_CASE_SCENARIO = "worst_case_scenario"
    BEST_FRIEND_TECHNIQUE = "best_friend_technique"
    TIME_PROJECTION = "time_projection"


@dataclass
class CognitivePromptTemplate:
    """Template for cognitive intervention prompts"""
    intervention_type: CognitiveInterventionType
    phase: SessionPhase
    primary_prompt: str
    follow_up_questions: List[str]
    challenge_questions: List[str]
    therapeutic_techniques: List[str]
    common_obstacles: List[str]
    troubleshooting_strategies: List[str]
    outcome_measures: List[str]
    homework_assignments: List[str]
    therapeutic_rationale: str
    clinical_considerations: List[str]


@dataclass
class CognitiveInterventionContext:
    """Context for cognitive interventions"""
    patient_id: str
    session_id: str
    presenting_symptoms: List[str]
    thought_patterns: List[str]
    identified_distortions: List[CognitiveDistortion]
    emotional_intensity: int  # 1-10 scale
    previous_thought_records: int
    successful_challenges: List[str]
    persistent_beliefs: List[str]
    cognitive_flexibility: str  # "low", "moderate", "high"
    insight_level: str  # "minimal", "developing", "good", "excellent"
    homework_compliance: str  # "poor", "fair", "good", "excellent"
    motivation_for_change: int  # 1-10 scale
    education_level: str
    preferred_learning_style: str


class CognitiveInterventionPrompts:
    """Comprehensive cognitive intervention prompt system"""
    
    def __init__(self):
        self.prompt_templates = self._initialize_cognitive_prompts()
        self.distortion_guides = self._initialize_distortion_guides()
        self.challenge_strategies = self._initialize_challenge_strategies()
        self.thought_record_templates = self._initialize_thought_record_templates()
        self.homework_templates = self._initialize_homework_templates()
    
    def get_cognitive_intervention_prompt(
        self,
        intervention_type: CognitiveInterventionType,
        phase: SessionPhase,
        context: CognitiveInterventionContext,
        session_info: Dict[str, Any] = None
    ) -> str:
        """Generate contextual cognitive intervention prompt"""
        
        template = self.prompt_templates.get((intervention_type, phase))
        if not template:
            return self._get_generic_cognitive_prompt(intervention_type, phase)
        
        context_info = self._format_cognitive_context(context, session_info)
        
        prompt = f"""
{template.primary_prompt}

PATIENT CONTEXT:
{context_info}

THERAPEUTIC RATIONALE:
{template.therapeutic_rationale}

FOLLOW-UP QUESTIONS:
{chr(10).join(f"• {question}" for question in template.follow_up_questions)}

CHALLENGE QUESTIONS TO USE:
{chr(10).join(f"• {question}" for question in template.challenge_questions)}

THERAPEUTIC TECHNIQUES:
{chr(10).join(f"• {technique}" for technique in template.therapeutic_techniques)}

COMMON OBSTACLES & SOLUTIONS:
{chr(10).join(f"• {obstacle}" for obstacle in template.common_obstacles)}

OUTCOME MEASURES:
{chr(10).join(f"• {measure}" for measure in template.outcome_measures)}

CLINICAL CONSIDERATIONS:
{chr(10).join(f"• {consideration}" for consideration in template.clinical_considerations)}

APPROACH:
- Use Socratic questioning to guide discovery
- Maintain collaborative, non-judgmental stance
- Focus on specific, concrete examples
- Help patient discover insights rather than telling them
- Validate emotions while examining thoughts
- Encourage curiosity about thinking patterns
- Practice skills in session before assigning homework
"""
        
        return prompt
    
    def _initialize_cognitive_prompts(self) -> Dict[Tuple[CognitiveInterventionType, SessionPhase], CognitivePromptTemplate]:
        """Initialize comprehensive cognitive intervention prompts"""
        
        prompts = {}
        
        # COGNITIVE RESTRUCTURING PROMPTS
        prompts[(CognitiveInterventionType.COGNITIVE_RESTRUCTURING, SessionPhase.ASSESSMENT)] = CognitivePromptTemplate(
            intervention_type=CognitiveInterventionType.COGNITIVE_RESTRUCTURING,
            phase=SessionPhase.ASSESSMENT,
            primary_prompt="""
You are conducting a cognitive assessment to understand the patient's thought patterns and their relationship to emotions and behaviors. The goal is to identify automatic thoughts, thinking patterns, and areas where cognitive restructuring could be helpful.

Start by saying: "I'd like to understand how your thoughts might be connected to how you've been feeling. Often our thoughts have a powerful impact on our emotions and behaviors, and by examining these thoughts, we can find ways to feel better."

Explore the connection between their thoughts, feelings, and behaviors using specific recent examples.
""",
            follow_up_questions=[
                "Can you describe a recent situation where you felt particularly upset?",
                "What thoughts were going through your mind in that moment?",
                "How did those thoughts make you feel?",
                "What did you do as a result of having those thoughts and feelings?",
                "Do you notice any patterns in the types of thoughts you have?",
                "How often do you find yourself having negative thoughts?",
                "Do these thoughts feel automatic or do you choose to think them?"
            ],
            challenge_questions=[
                "What evidence supports this thought?",
                "What evidence contradicts this thought?",
                "Is there another way to look at this situation?",
                "What would you tell a friend who had this thought?",
                "How helpful is thinking this way?"
            ],
            therapeutic_techniques=[
                "CBT triangle explanation (thoughts-feelings-behaviors)",
                "Thought identification exercises",
                "Automatic thought catching practice",
                "Collaborative exploration of thought-emotion connections",
                "Psychoeducation about cognitive patterns"
            ],
            common_obstacles=[
                "Difficulty identifying specific thoughts",
                "Resistance to examining thinking patterns",
                "Belief that thoughts are facts",
                "Overwhelming emotional intensity",
                "Lack of awareness of thought-emotion connection"
            ],
            troubleshooting_strategies=[
                "Use guided imagery to recreate situations",
                "Start with easier, less emotional examples",
                "Normalize the process of examining thoughts",
                "Use emotion as gateway to identify thoughts",
                "Provide psychoeducation about automatic thoughts"
            ],
            outcome_measures=[
                "Ability to identify automatic thoughts",
                "Recognition of thought-emotion connections",
                "Willingness to examine thinking patterns",
                "Understanding of CBT model",
                "Motivation for cognitive work"
            ],
            homework_assignments=[
                "Notice and write down automatic thoughts for one week",
                "Practice identifying thoughts when emotions change",
                "Complete simple thought monitoring log",
                "Read psychoeducation materials about CBT"
            ],
            therapeutic_rationale="Cognitive restructuring is based on the principle that our thoughts significantly influence our emotions and behaviors. By identifying and examining automatic thoughts, patients can develop more balanced, realistic thinking patterns that lead to improved mood and functioning.",
            clinical_considerations=[
                "Assess cognitive capacity and readiness for cognitive work",
                "Consider cultural factors in thought content",
                "Evaluate insight and self-awareness levels",
                "Monitor for signs of cognitive rigidity",
                "Assess education level and adjust language accordingly"
            ]
        )
        
        prompts[(CognitiveInterventionType.THOUGHT_CHALLENGING, SessionPhase.PRACTICE)] = CognitivePromptTemplate(
            intervention_type=CognitiveInterventionType.THOUGHT_CHALLENGING,
            phase=SessionPhase.PRACTICE,
            primary_prompt="""
You are practicing thought challenging techniques with the patient. The goal is to help them learn to examine their automatic thoughts systematically and develop more balanced, realistic alternatives.

Say: "Now let's practice challenging some of the thoughts you've identified. Remember, we're not trying to think positively or convince ourselves of things that aren't true. We're looking for a more balanced, realistic way of thinking about the situation."

Use Socratic questioning to guide the patient through the thought challenging process.
""",
            follow_up_questions=[
                "What specific thought would you like to work on today?",
                "How much do you believe this thought right now (0-100%)?",
                "What emotion does this thought create?",
                "How intense is that emotion (1-10)?",
                "Let's examine the evidence - what supports this thought?",
                "What evidence goes against this thought?",
                "What would you tell a good friend who had this thought?"
            ],
            challenge_questions=[
                "What's the evidence for and against this thought?",
                "Am I looking at the whole picture or just part of it?",
                "Am I being realistic or am I catastrophizing?",
                "What would someone else say about this situation?",
                "Will this matter in 5 years? In 5 months? In 5 days?",
                "What's the most likely outcome, not the worst possible outcome?",
                "Am I confusing a thought with a fact?",
                "What would I need to believe instead to feel better about this?"
            ],
            therapeutic_techniques=[
                "Evidence examination technique",
                "Alternative perspective generation",
                "Best friend technique",
                "Time perspective method",
                "Probability estimation",
                "Balanced thought development"
            ],
            common_obstacles=[
                "Strong emotional attachment to negative thoughts",
                "Belief that challenging thoughts means denying reality",
                "Difficulty generating alternative perspectives",
                "Perfectionist desire for absolute certainty",
                "Fear that positive thinking will lead to disappointment"
            ],
            troubleshooting_strategies=[
                "Validate emotions while examining thoughts",
                "Emphasize balanced vs. positive thinking",
                "Use collaborative approach rather than confrontational",
                "Start with less emotionally charged thoughts",
                "Provide examples and model the process first"
            ],
            outcome_measures=[
                "Reduction in belief in original thought",
                "Decrease in emotional intensity",
                "Generation of alternative perspectives",
                "Development of balanced thoughts",
                "Increased confidence in challenging thoughts"
            ],
            homework_assignments=[
                "Practice challenging one thought daily using worksheet",
                "Use specific challenging questions provided",
                "Record belief levels before and after challenging",
                "Notice situations where challenging might be helpful"
            ],
            therapeutic_rationale="Thought challenging helps patients develop critical thinking skills about their automatic thoughts, leading to more balanced perspectives and reduced emotional distress. This process builds cognitive flexibility and emotional regulation skills.",
            clinical_considerations=[
                "Ensure patient understands goal is balance, not positivity",
                "Monitor for cognitive rigidity or resistance",
                "Adjust questioning style to patient's learning preferences",
                "Be patient with the learning process",
                "Celebrate small improvements in thinking flexibility"
            ]
        )
        
        # DISTORTION IDENTIFICATION PROMPTS
        prompts[(CognitiveInterventionType.DISTORTION_IDENTIFICATION, SessionPhase.PSYCHOEDUCATION)] = CognitivePromptTemplate(
            intervention_type=CognitiveInterventionType.DISTORTION_IDENTIFICATION,
            phase=SessionPhase.PSYCHOEDUCATION,
            primary_prompt="""
You are teaching the patient about cognitive distortions - common thinking errors that can worsen emotional distress. The goal is to help them recognize these patterns in their own thinking.

Say: "There are certain thinking patterns that are very common when people are feeling depressed, anxious, or stressed. These are called cognitive distortions or thinking errors. Learning to recognize these patterns can be very helpful because once you can spot them, you can start to question whether they're actually accurate."

Use specific examples and help the patient identify which distortions they use most frequently.
""",
            follow_up_questions=[
                "Do any of these thinking patterns sound familiar to you?",
                "Which distortions do you think you might use most often?",
                "Can you think of a recent example where you might have used this pattern?",
                "How do you think this thinking pattern affects your mood?",
                "What would be different if you didn't think this way?"
            ],
            challenge_questions=[
                "Is this thought an example of all-or-nothing thinking?",
                "Am I overgeneralizing from one situation?",
                "Am I filtering out the positive and focusing only on the negative?",
                "Am I mind-reading or fortune-telling?",
                "Am I using emotional reasoning - feeling it so it must be true?"
            ],
            therapeutic_techniques=[
                "Cognitive distortion psychoeducation",
                "Personal example identification",
                "Distortion labeling practice",
                "Pattern recognition training",
                "Collaborative distortion hunting"
            ],
            common_obstacles=[
                "Difficulty seeing their own thinking patterns",
                "Belief that their distorted thoughts are accurate",
                "Resistance to labeling their thoughts as distorted",
                "Overwhelm with too many distortion types",
                "Intellectual understanding without emotional connection"
            ],
            troubleshooting_strategies=[
                "Start with one or two main distortions",
                "Use clear, relatable examples",
                "Normalize that everyone uses cognitive distortions",
                "Focus on patterns rather than individual thoughts",
                "Make it collaborative rather than corrective"
            ],
            outcome_measures=[
                "Recognition of personal distortion patterns",
                "Ability to label distortions in examples",
                "Understanding of distortion impact on mood",
                "Motivation to work on distorted thinking",
                "Insight into thinking patterns"
            ],
            homework_assignments=[
                "Review distortion list and identify personal patterns",
                "Notice and label one distortion daily",
                "Keep a distortion awareness log",
                "Practice identifying distortions in low-stakes situations"
            ],
            therapeutic_rationale="Cognitive distortion identification provides patients with a concrete framework for recognizing problematic thinking patterns. This awareness is the first step toward developing more balanced, realistic thinking.",
            clinical_considerations=[
                "Present information in digestible chunks",
                "Use patient's own examples when possible",
                "Avoid overwhelming with too many distortion types",
                "Focus on most relevant distortions for this patient",
                "Maintain non-judgmental approach to distorted thinking"
            ]
        )
        
        # BALANCED THINKING PROMPTS
        prompts[(CognitiveInterventionType.BALANCED_THINKING, SessionPhase.ALTERNATIVE_GENERATION)] = CognitivePromptTemplate(
            intervention_type=CognitiveInterventionType.BALANCED_THINKING,
            phase=SessionPhase.ALTERNATIVE_GENERATION,
            primary_prompt="""
You are helping the patient develop balanced thoughts to replace distorted or unhelpful thinking patterns. The goal is to create realistic, helpful thoughts that acknowledge complexity while reducing emotional distress.

Say: "Now that we've examined this thought and looked at the evidence, let's work together to develop a more balanced way of thinking about this situation. A balanced thought isn't necessarily positive - it's realistic and takes into account all the information we have."

Guide the patient to create thoughts that are realistic, helpful, and emotionally manageable.
""",
            follow_up_questions=[
                "Taking into account all the evidence we've discussed, what would be a more balanced way to think about this?",
                "What thought would be realistic but also more helpful to you?",
                "If a wise, caring friend looked at this situation, what might they say?",
                "What would you need to believe to feel better while still being realistic?",
                "How can we acknowledge your concerns while also including the positive evidence?"
            ],
            challenge_questions=[
                "Is this new thought realistic given the evidence?",
                "Would this thought be helpful to me in this situation?",
                "Does this thought acknowledge complexity rather than being all-or-nothing?",
                "Would I be comfortable sharing this thought with someone I trust?",
                "Does this thought help me cope while still being honest?"
            ],
            therapeutic_techniques=[
                "Balanced thought development",
                "Evidence integration",
                "Perspective taking",
                "Collaborative thought creation",
                "Reality testing of new thoughts"
            ],
            common_obstacles=[
                "Difficulty moving away from familiar negative thoughts",
                "Belief that balanced thoughts are unrealistic optimism",
                "Perfectionist need for absolute certainty",
                "Fear that balanced thinking will lead to complacency",
                "Strong emotional investment in negative thoughts"
            ],
            troubleshooting_strategies=[
                "Emphasize realistic rather than positive thinking",
                "Start with slightly more balanced thoughts rather than complete opposites",
                "Validate the emotional truth behind negative thoughts",
                "Use gradual progression toward more balanced thinking",
                "Test balanced thoughts against evidence"
            ],
            outcome_measures=[
                "Development of realistic balanced thoughts",
                "Reduced emotional intensity with new thoughts",
                "Increased belief in balanced thoughts over time",
                "Improved emotional regulation",
                "Greater cognitive flexibility"
            ],
            homework_assignments=[
                "Practice using balanced thoughts in daily situations",
                "Write balanced thoughts for common triggering situations",
                "Test balanced thoughts against reality and adjust as needed",
                "Notice how balanced thoughts affect mood and behavior"
            ],
            therapeutic_rationale="Balanced thinking helps patients develop more adaptive cognitive patterns that reduce emotional distress while maintaining realistic appraisal of situations. This approach builds resilience and emotional regulation skills.",
            clinical_considerations=[
                "Ensure balanced thoughts are genuinely believable to patient",
                "Balance realism with emotional manageability",
                "Consider patient's values and cultural background",
                "Monitor for balanced thoughts becoming new rigid patterns",
                "Adjust language and complexity to patient's cognitive style"
            ]
        )
        
        # THOUGHT RECORDS PROMPTS
        prompts[(CognitiveInterventionType.THOUGHT_RECORDS, SessionPhase.PRACTICE)] = CognitivePromptTemplate(
            intervention_type=CognitiveInterventionType.THOUGHT_RECORDS,
            phase=SessionPhase.PRACTICE,
            primary_prompt="""
You are teaching the patient to complete thought records - systematic tools for identifying, examining, and challenging automatic thoughts. This is a core CBT skill that they can use independently.

Say: "Thought records are tools that help you work through difficult thoughts step by step. We'll practice completing one together so you can learn to use this technique on your own when challenging thoughts come up."

Guide them through each step of the thought record process using a specific example from their life.
""",
            follow_up_questions=[
                "What specific situation triggered these difficult thoughts and feelings?",
                "What emotions were you experiencing and how intense were they?",
                "What thoughts were going through your mind in that moment?",
                "Which thought was most distressing or seemed most important?",
                "What evidence supports this thought?",
                "What evidence goes against this thought?",
                "What would be a more balanced way to think about this situation?"
            ],
            challenge_questions=[
                "Am I treating this thought as a fact when it's really an opinion?",
                "What thinking errors might I be making?",
                "What's the evidence for and against this thought?",
                "What would I tell someone else in this situation?",
                "How would I look at this if I were in a better mood?",
                "What are the advantages and disadvantages of thinking this way?"
            ],
            therapeutic_techniques=[
                "Step-by-step thought record completion",
                "Situation description",
                "Emotion identification and rating",
                "Automatic thought identification",
                "Evidence examination",
                "Balanced thought development"
            ],
            common_obstacles=[
                "Difficulty identifying specific thoughts",
                "Confusion about emotions vs. thoughts",
                "Tendency to rationalize rather than examine",
                "Feeling overwhelmed by the process",
                "Resistance to writing things down"
            ],
            troubleshooting_strategies=[
                "Use guided questions to identify thoughts",
                "Clarify difference between thoughts and emotions",
                "Model the process first with therapist examples",
                "Break down the process into smaller steps",
                "Explain benefits of written thought records"
            ],
            outcome_measures=[
                "Completion of thought record with assistance",
                "Understanding of thought record steps",
                "Ability to identify automatic thoughts",
                "Skill in evidence examination",
                "Development of balanced thoughts"
            ],
            homework_assignments=[
                "Complete one thought record per day using provided template",
                "Practice with less emotionally intense situations first",
                "Bring completed thought records to next session",
                "Notice patterns in thoughts and emotions over time"
            ],
            therapeutic_rationale="Thought records provide a structured approach to cognitive restructuring that patients can use independently. This skill builds self-efficacy and provides a concrete tool for managing difficult thoughts and emotions.",
            clinical_considerations=[
                "Start with simpler situations before complex ones",
                "Ensure patient understands each step before moving on",
                "Provide clear instructions and examples",
                "Monitor for perfectionism about 'doing it right'",
                "Adapt format to patient's preferences and abilities"
            ]
        )
        
        return prompts
    
    def _initialize_distortion_guides(self) -> Dict[CognitiveDistortion, Dict[str, Any]]:
        """Initialize comprehensive guides for cognitive distortions"""
        
        return {
            CognitiveDistortion.ALL_OR_NOTHING: {
                "name": "All-or-Nothing Thinking",
                "description": "Seeing situations in extreme terms with no middle ground",
                "keywords": ["always", "never", "completely", "totally", "everyone", "no one", "perfect", "disaster"],
                "examples": [
                    "I always mess up presentations",
                    "Nobody ever listens to me", 
                    "This is a complete disaster",
                    "I'm totally worthless at relationships"
                ],
                "challenge_questions": [
                    "Is this really an all-or-nothing situation?",
                    "What would be a more realistic percentage?",
                    "Are there any exceptions to this absolute statement?",
                    "What would I say if a friend used this extreme language?"
                ],
                "alternative_phrases": [
                    "sometimes", "often", "occasionally", "in this instance",
                    "partly", "to some degree", "this time"
                ]
            },
            
            CognitiveDistortion.OVERGENERALIZATION: {
                "name": "Overgeneralization", 
                "description": "Drawing broad conclusions from single events or limited examples",
                "keywords": ["all", "every", "this always happens", "typical", "everyone", "pattern"],
                "examples": [
                    "This presentation went badly, I'm terrible at public speaking",
                    "All relationships end in heartbreak",
                    "Every time I try something new, I fail"
                ],
                "challenge_questions": [
                    "How many examples do I actually have?",
                    "Am I making a pattern from just one or two events?",
                    "What evidence contradicts this generalization?",
                    "What are the exceptions to this rule?"
                ],
                "alternative_phrases": [
                    "in this case", "this time", "sometimes", "in my experience so far",
                    "this particular situation"
                ]
            },
            
            CognitiveDistortion.MENTAL_FILTER: {
                "name": "Mental Filter",
                "description": "Focusing exclusively on negative details while filtering out positive aspects",
                "keywords": ["only", "just", "all that matters", "nothing but", "except"],
                "examples": [
                    "The presentation went well, but I stumbled over one word",
                    "Everyone complimented dinner except one person seemed unimpressed",
                    "I got mostly good feedback, but there was one criticism"
                ],
                "challenge_questions": [
                    "What positive aspects am I filtering out?",
                    "Am I giving equal weight to positive and negative feedback?",
                    "What would the complete picture look like?",
                    "What am I not paying attention to?"
                ],
                "techniques": [
                    "Complete picture technique",
                    "Positive data log",
                    "Balanced evidence examination"
                ]
            },
            
            CognitiveDistortion.JUMPING_TO_CONCLUSIONS: {
                "name": "Jumping to Conclusions",
                "description": "Making negative interpretations without sufficient evidence",
                "subtypes": ["mind_reading", "fortune_telling"],
                "mind_reading_examples": [
                    "She thinks I'm boring",
                    "He can tell I'm nervous", 
                    "They all know I don't belong here"
                ],
                "fortune_telling_examples": [
                    "This is going to be a disaster",
                    "I'll never get promoted",
                    "Things will only get worse"
                ],
                "challenge_questions": [
                    "What evidence do I have for this conclusion?",
                    "What other explanations are possible?",
                    "Am I mind-reading or fortune-telling?",
                    "What would I need to verify this conclusion?"
                ]
            },
            
            CognitiveDistortion.CATASTROPHIZING: {
                "name": "Catastrophizing",
                "description": "Expecting the worst possible outcome or magnifying negative consequences",
                "keywords": ["disaster", "terrible", "awful", "catastrophe", "worst", "ruined"],
                "examples": [
                    "If I fail this test, my entire future is ruined",
                    "Making this mistake means I'm going to get fired",
                    "If they reject me, I'll never find anyone"
                ],
                "challenge_questions": [
                    "What's the worst that could realistically happen?",
                    "What's the most likely outcome?",
                    "Even if the worst happened, how would I cope?",
                    "Will this matter in 5 years?"
                ],
                "techniques": [
                    "Worst case scenario planning",
                    "Probability estimation",
                    "Coping resource identification"
                ]
            }
        }
    
    def _initialize_challenge_strategies(self) -> Dict[ChallengeMethod, Dict[str, Any]]:
        """Initialize challenge strategies for different methods"""
        
        return {
            ChallengeMethod.EVIDENCE_BASED: {
                "description": "Systematically examining evidence for and against thoughts",
                "questions": [
                    "What evidence supports this thought?",
                    "What evidence contradicts this thought?",
                    "What would a jury conclude based on the evidence?",
                    "Am I considering all the evidence or just some of it?",
                    "What would someone who disagreed with me say?"
                ],
                "technique_steps": [
                    "Identify the specific thought to examine",
                    "List evidence that supports the thought",
                    "List evidence that contradicts the thought", 
                    "Weigh the evidence objectively",
                    "Develop a conclusion based on all evidence"
                ]
            },
            
            ChallengeMethod.ALTERNATIVE_PERSPECTIVES: {
                "description": "Generating multiple possible interpretations of situations",
                "questions": [
                    "What are other possible explanations?",
                    "How might someone else interpret this?",
                    "What would I think if I were in a better mood?",
                    "What other angles should I consider?",
                    "What would a neutral observer conclude?"
                ],
                "technique_steps": [
                    "Identify the initial interpretation",
                    "Brainstorm alternative explanations",
                    "Consider multiple perspectives",
                    "Evaluate the likelihood of each interpretation",
                    "Choose the most balanced perspective"
                ]
            },
            
            ChallengeMethod.BEST_FRIEND_TECHNIQUE: {
                "description": "Asking what you would tell a good friend in the same situation",
                "questions": [
                    "What would I tell my best friend if they had this thought?",
                    "What advice would I give someone I care about?",
                    "How would I support a friend going through this?",
                    "What compassionate response would I offer others?",
                    "Why do I treat myself differently than I treat friends?"
                ],
                "benefits": [
                    "Accesses natural compassion and wisdom",
                    "Reduces self-critical bias",
                    "Provides distance from emotional intensity",
                    "Activates problem-solving abilities"
                ]
            },
            
            ChallengeMethod.TIME_PROJECTION: {
                "description": "Examining how the situation will look from different time perspectives",
                "questions": [
                    "How will I feel about this in a week?",
                    "Will this matter in a month? In a year?",
                    "How important will this be in 5 years?",
                    "What would 80-year-old me think about this?",
                    "How much energy is this worth given its long-term importance?"
                ],
                "time_frames": ["1 week", "1 month", "1 year", "5 years", "end of life"],
                "benefits": [
                    "Provides perspective on current distress",
                    "Reduces catastrophic thinking",
                    "Helps prioritize what truly matters",
                    "Calms immediate emotional reactions"
                ]
            },
            
            ChallengeMethod.COST_BENEFIT: {
                "description": "Analyzing the advantages and disadvantages of holding a particular thought",
                "questions": [
                    "What are the advantages of thinking this way?",
                    "What are the disadvantages of this thought?",
                    "How does this thought help me?",
                    "How does this thought hurt me?",
                    "Is this thought serving me well overall?"
                ],
                "categories": [
                    "Emotional costs/benefits",
                    "Behavioral costs/benefits", 
                    "Relationship costs/benefits",
                    "Goal achievement costs/benefits"
                ]
            },
            
            ChallengeMethod.WORST_CASE_SCENARIO: {
                "description": "Systematically examining worst case fears and coping resources",
                "questions": [
                    "What's the absolute worst that could happen?",
                    "How likely is this worst case scenario?",
                    "If it did happen, how would I cope?",
                    "What resources would I have available?",
                    "Have I survived difficult things before?"
                ],
                "steps": [
                    "Identify the feared worst case outcome",
                    "Assess realistic probability",
                    "Develop comprehensive coping plan",
                    "Identify available resources and support",
                    "Practice self-soothing and confidence building"
                ]
            }
        }
    
    def _initialize_thought_record_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize thought record templates for different situations"""
        
        return {
            "basic_thought_record": {
                "name": "Basic Thought Record",
                "columns": [
                    "Date/Time",
                    "Situation", 
                    "Emotion(s)",
                    "Intensity (1-10)",
                    "Automatic Thought(s)",
                    "Evidence For",
                    "Evidence Against", 
                    "Balanced Thought",
                    "New Emotion",
                    "New Intensity"
                ],
                "instructions": [
                    "Describe the specific situation that triggered the thought",
                    "Identify and rate the intensity of emotions experienced",
                    "Write down the automatic thoughts that occurred",
                    "List evidence that supports the thought",
                    "List evidence that contradicts the thought",
                    "Develop a more balanced, realistic thought",
                    "Notice how emotions change with the new thought"
                ]
            },
            
            "distortion_focused_record": {
                "name": "Cognitive Distortion Thought Record",
                "columns": [
                    "Situation",
                    "Automatic Thought",
                    "Emotion & Intensity",
                    "Distortion(s) Present",
                    "Challenge Questions",
                    "Balanced Thought",
                    "Outcome"
                ],
                "distortion_checklist": [
                    "All-or-nothing thinking",
                    "Overgeneralization", 
                    "Mental filter",
                    "Mind reading",
                    "Fortune telling",
                    "Catastrophizing",
                    "Emotional reasoning"
                ]
            },
            
            "behavioral_thought_record": {
                "name": "Thought-Behavior Connection Record",
                "columns": [
                    "Trigger Situation",
                    "Automatic Thought",
                    "Emotion",
                    "Behavior/Action Taken",
                    "Consequence",
                    "Alternative Thought",
                    "Alternative Behavior",
                    "Predicted Outcome"
                ],
                "focus": "Connecting thoughts to behaviors and exploring alternatives"
            }
        }
    
    def _initialize_homework_templates(self) -> Dict[CognitiveInterventionType, List[Dict[str, Any]]]:
        """Initialize homework assignment templates for cognitive interventions"""
        
        return {
            CognitiveInterventionType.THOUGHT_CHALLENGING: [
                {
                    "name": "Daily Thought Challenge Practice",
                    "description": "Practice challenging one automatic thought each day",
                    "instructions": [
                        "Notice when you have a strong negative emotion",
                        "Identify the automatic thought behind the emotion",
                        "Use the challenge questions to examine the thought",
                        "Develop a more balanced alternative",
                        "Notice how your mood changes"
                    ],
                    "materials": ["Challenge questions card", "Practice log"],
                    "frequency": "Daily for 1 week"
                },
                {
                    "name": "Evidence Examination Exercise", 
                    "description": "Systematically examine evidence for recurring negative thoughts",
                    "instructions": [
                        "Choose a recurring negative thought",
                        "List all evidence that supports the thought",
                        "List all evidence that contradicts the thought",
                        "Weigh the evidence objectively",
                        "Write a balanced conclusion"
                    ],
                    "materials": ["Evidence examination worksheet"],
                    "frequency": "3 times this week"
                }
            ],
            
            CognitiveInterventionType.DISTORTION_IDENTIFICATION: [
                {
                    "name": "Distortion Spotting Practice",
                    "description": "Identify cognitive distortions in daily thoughts",
                    "instructions": [
                        "Review the list of cognitive distortions daily",
                        "When you notice strong negative emotions, check for distortions",
                        "Label any distortions you identify",
                        "Practice this without trying to change the thoughts initially"
                    ],
                    "materials": ["Distortion reference card", "Daily log"],
                    "frequency": "Daily awareness practice"
                }
            ],
            
            CognitiveInterventionType.THOUGHT_RECORDS: [
                {
                    "name": "Complete Thought Record Practice",
                    "description": "Complete full thought records for challenging situations",
                    "instructions": [
                        "Use the thought record template for any situation that causes distress",
                        "Complete all columns systematically", 
                        "Focus on being specific and detailed",
                        "Notice patterns in your thinking over time"
                    ],
                    "materials": ["Thought record worksheets"],
                    "frequency": "3-5 times this week"
                }
            ]
        }
    
    def _format_cognitive_context(self, context: CognitiveInterventionContext, session_info: Dict[str, Any] = None) -> str:
        """Format cognitive intervention context information"""
        
        context_lines = [
            f"Patient ID: {context.patient_id}",
            f"Emotional Intensity: {context.emotional_intensity}/10",
            f"Cognitive Flexibility: {context.cognitive_flexibility}",
            f"Insight Level: {context.insight_level}",
            f"Motivation for Change: {context.motivation_for_change}/10"
        ]
        
        if context.presenting_symptoms:
            context_lines.append(f"Presenting Symptoms: {', '.join(context.presenting_symptoms)}")
        
        if context.thought_patterns:
            context_lines.append(f"Thought Patterns: {', '.join(context.thought_patterns)}")
        
        if context.identified_distortions:
            distortion_names = [d.value.replace('_', ' ').title() for d in context.identified_distortions]
            context_lines.append(f"Identified Distortions: {', '.join(distortion_names)}")
        
        if context.successful_challenges:
            context_lines.append(f"Previous Successful Challenges: {', '.join(context.successful_challenges)}")
        
        if context.persistent_beliefs:
            context_lines.append(f"Persistent Beliefs: {', '.join(context.persistent_beliefs)}")
        
        context_lines.append(f"Previous Thought Records: {context.previous_thought_records}")
        context_lines.append(f"Homework Compliance: {context.homework_compliance}")
        
        return chr(10).join(context_lines)
    
    def _get_generic_cognitive_prompt(self, intervention_type: CognitiveInterventionType, phase: SessionPhase) -> str:
        """Generate generic cognitive prompt when specific template not found"""
        
        return f"""
You are implementing {intervention_type.value.replace('_', ' ')} in the {phase.value.replace('_', ' ')} phase.

GENERAL COGNITIVE APPROACH:
- Use Socratic questioning to guide discovery
- Help patient examine thoughts rather than telling them what to think
- Focus on specific, concrete examples
- Validate emotions while examining thoughts
- Encourage curiosity about thinking patterns
- Practice skills collaboratively before independent use

COGNITIVE PRINCIPLES:
- Thoughts significantly influence emotions and behaviors
- Automatic thoughts are often inaccurate or unhelpful
- Examining thoughts can lead to more balanced perspectives
- Cognitive flexibility improves emotional regulation
- Practice builds lasting cognitive skills

Continue with systematic cognitive intervention appropriate for {intervention_type.value.replace('_', ' ')}.
"""
    
    def get_distortion_specific_prompt(
        self,
        distortion: CognitiveDistortion,
        context: CognitiveInterventionContext,
        session_phase: SessionPhase = SessionPhase.PRACTICE
    ) -> str:
        """Generate prompt specific to a particular cognitive distortion"""
        
        distortion_info = self.distortion_guides.get(distortion, {})
        distortion_name = distortion_info.get("name", distortion.value.replace('_', ' ').title())
        
        prompt = f"""
You are working specifically on {distortion_name} with this patient.

DISTORTION OVERVIEW:
{distortion_info.get('description', 'Cognitive distortion that affects thinking patterns')}

COMMON KEYWORDS TO LISTEN FOR:
{', '.join(distortion_info.get('keywords', []))}

PATIENT CONTEXT:
{self._format_cognitive_context(context)}

EXAMPLES OF THIS DISTORTION:
"""
        
        for example in distortion_info.get('examples', []):
            prompt += f"• {example}\n"
        
        prompt += f"""
SPECIFIC CHALLENGE QUESTIONS FOR {distortion_name.upper()}:
"""
        
        for question in distortion_info.get('challenge_questions', []):
            prompt += f"• {question}\n"
        
        if 'alternative_phrases' in distortion_info:
            prompt += f"""
ALTERNATIVE LANGUAGE TO SUGGEST:
Instead of extreme language, help patient use: {', '.join(distortion_info['alternative_phrases'])}
"""
        
        if 'techniques' in distortion_info:
            prompt += f"""
SPECIFIC TECHNIQUES FOR THIS DISTORTION:
{chr(10).join(f"• {technique}" for technique in distortion_info['techniques'])}
"""
        
        prompt += f"""
APPROACH:
- Help patient recognize when they're using this distortion
- Use the specific challenge questions provided
- Guide them to more balanced language and thinking
- Practice identifying this distortion in less emotionally charged situations first
- Celebrate recognition of the distortion pattern
- Focus on progress, not perfection in changing thinking patterns
"""
        
        return prompt
    
    def get_thought_record_training_prompt(
        self,
        record_type: str,
        context: CognitiveInterventionContext,
        difficulty_level: str = "beginner"
    ) -> str:
        """Generate prompt for teaching thought record completion"""
        
        template = self.thought_record_templates.get(record_type, self.thought_record_templates["basic_thought_record"])
        
        prompt = f"""
You are teaching the patient to complete a {template['name']}.

PATIENT CONTEXT:
{self._format_cognitive_context(context)}

THOUGHT RECORD STRUCTURE:
"""
        
        for i, column in enumerate(template['columns'], 1):
            prompt += f"{i}. {column}\n"
        
        prompt += f"""
STEP-BY-STEP INSTRUCTIONS:
"""
        
        for i, instruction in enumerate(template.get('instructions', []), 1):
            prompt += f"{i}. {instruction}\n"
        
        if difficulty_level == "beginner":
            prompt += f"""
BEGINNER GUIDANCE:
- Start with a recent, specific situation (not ongoing problems)
- Choose a situation with moderate emotional intensity (4-7 out of 10)
- Focus on one main automatic thought rather than multiple thoughts
- Provide lots of encouragement and normalize the learning process
- Model the process first if patient seems confused

COMMON BEGINNER MISTAKES TO WATCH FOR:
• Describing situations too vaguely
• Confusing thoughts with emotions
• Listing multiple thoughts instead of focusing on the most important one
• Getting stuck on finding "perfect" evidence
• Trying to make balanced thoughts overly positive
"""
        
        elif difficulty_level == "advanced":
            prompt += f"""
ADVANCED PRACTICE:
- Work with more emotionally intense situations
- Address core beliefs and deep-seated thought patterns
- Connect thought records to behavioral changes
- Identify subtle cognitive distortions
- Develop nuanced, complex balanced thoughts

ADVANCED TECHNIQUES:
• Examine underlying assumptions behind automatic thoughts
• Connect patterns across multiple thought records
• Use thought records for prospective planning
• Address meta-cognitive thoughts (thoughts about thoughts)
"""
        
        prompt += f"""
COACHING APPROACH:
- Guide through Socratic questioning rather than providing answers
- Help patient discover insights rather than telling them what to write
- Validate the difficulty of the process while encouraging persistence
- Focus on learning and practice rather than perfect completion
- Use patient's own language and examples
- Check understanding at each step before moving forward

Remember: The goal is skill building, not immediate thought change. Celebrate effort and learning!
"""
        
        return prompt
    
    def get_homework_review_prompt(
        self,
        intervention_type: CognitiveInterventionType,
        homework_completed: bool,
        completion_details: Dict[str, Any] = None
    ) -> str:
        """Generate prompt for reviewing cognitive homework assignments"""
        
        base_prompt = f"""
You are reviewing {intervention_type.value.replace('_', ' ')} homework.

HOMEWORK COMPLETION STATUS: {'Completed' if homework_completed else 'Not Completed'}
"""
        
        if homework_completed and completion_details:
            base_prompt += f"""
COMPLETION DETAILS:
"""
            for key, value in completion_details.items():
                base_prompt += f"• {key.replace('_', ' ').title()}: {value}\n"
            
            base_prompt += f"""
REVIEW APPROACH FOR COMPLETED HOMEWORK:
1. Acknowledge the effort and completion
2. Review specific examples from their practice
3. Explore what they learned about their thinking patterns
4. Identify which techniques were most helpful
5. Discuss any insights or surprises
6. Connect learning to session goals and overall progress
7. Troubleshoot any difficulties encountered
8. Plan progression for next week's practice

REVIEW QUESTIONS:
• What did you notice about your thinking patterns this week?
• Which challenge questions were most helpful?
• Were there any thoughts that were particularly difficult to challenge?
• How did your emotions change when you used these techniques?
• What was easier or harder than you expected?
• Which situations were most challenging to work with?
• What insights did you gain about your automatic thoughts?
"""
        
        else:
            base_prompt += f"""
REVIEW APPROACH FOR INCOMPLETE HOMEWORK:
1. Explore barriers without judgment
2. Identify specific obstacles that prevented completion
3. Problem-solve collaboratively
4. Adjust assignment difficulty or frequency if needed
5. Address motivation and engagement issues
6. Simplify or modify the approach
7. Increase support and accountability
8. Practice techniques in session before reassigning

REVIEW QUESTIONS:
• What prevented you from completing the homework?
• Was the assignment unclear or too difficult?
• Did you run into specific obstacles we didn't anticipate?
• How can we modify the assignment to make it more manageable?
• What would help you be more successful with this practice?
• Would a different approach or format work better for you?

TROUBLESHOOTING STRATEGIES:
• Reduce frequency (daily to 3x/week, etc.)
• Simplify the format or steps
• Start with less emotional situations
• Provide more structure or reminders
• Practice more in session before independent work
• Address underlying resistance or ambivalence
• Connect homework to patient's personal goals
"""
        
        base_prompt += f"""
GENERAL REVIEW PRINCIPLES:
- Maintain curious, non-judgmental stance
- Focus on learning rather than performance
- Validate the difficulty of changing thought patterns
- Celebrate any progress, however small
- Use homework experiences as teaching opportunities
- Adjust future assignments based on what you learn
- Connect cognitive work to emotional and behavioral improvements
- Encourage self-compassion about the learning process

Remember: Homework difficulties provide valuable information about how to better support the patient's learning!
"""
        
        return base_prompt
    
    def get_cognitive_skill_building_prompt(
        self,
        skill_level: str,
        target_skills: List[str],
        context: CognitiveInterventionContext
    ) -> str:
        """Generate prompt for progressive cognitive skill building"""
        
        prompt = f"""
You are working on cognitive skill building at the {skill_level} level.

TARGET SKILLS FOR THIS SESSION:
{chr(10).join(f"• {skill}" for skill in target_skills)}

PATIENT CONTEXT:
{self._format_cognitive_context(context)}

"""
        
        if skill_level == "foundation":
            prompt += f"""
FOUNDATION LEVEL SKILLS:
- Basic awareness of thoughts vs. emotions
- Recognition that thoughts affect feelings
- Simple automatic thought identification
- Basic challenging questions
- Understanding of cognitive distortions

FOUNDATION APPROACH:
• Use very concrete, specific examples
• Focus on psychoeducation and awareness building
• Practice identifying thoughts in low-stakes situations
• Emphasize curiosity rather than change
• Provide lots of examples and modeling
• Keep techniques simple and straightforward

FOUNDATION GOALS:
- Patient can distinguish thoughts from emotions
- Patient recognizes thought-emotion connections
- Patient can identify obvious automatic thoughts
- Patient understands basic CBT principles
"""
        
        elif skill_level == "intermediate":
            prompt += f"""
INTERMEDIATE LEVEL SKILLS:
- Consistent automatic thought identification
- Effective use of challenge questions
- Recognition of personal distortion patterns
- Basic thought record completion
- Simple balanced thought development

INTERMEDIATE APPROACH:
• Build on foundation skills systematically
• Introduce more sophisticated techniques
• Work with moderate emotional intensity
• Practice technique combinations
• Focus on skill refinement and consistency
• Begin independent skill application

INTERMEDIATE GOALS:
- Patient completes thought records independently
- Patient identifies personal distortion patterns
- Patient generates alternative perspectives
- Patient develops more balanced thoughts
- Patient notices mood improvements with practice
"""
        
        elif skill_level == "advanced":
            prompt += f"""
ADVANCED LEVEL SKILLS:
- Work with highly emotional situations
- Address core beliefs and schemas
- Complex cognitive pattern analysis
- Sophisticated balanced thinking
- Integration with behavioral changes
- Teaching skills to others

ADVANCED APPROACH:
• Work with complex, emotionally charged material
• Address deeper cognitive structures
• Connect cognitive work to life goals and values
• Focus on generalization across situations
• Develop personalized technique combinations
• Prepare for independent maintenance

ADVANCED GOALS:
- Patient handles intense emotions with cognitive skills
- Patient addresses core beliefs and assumptions
- Patient creates sophisticated balanced thoughts
- Patient integrates cognitive skills into daily life
- Patient maintains skills independently
"""
        
        prompt += f"""
SKILL BUILDING STRATEGIES:
• Start where the patient is, not where you think they should be
• Build skills incrementally with lots of practice
• Use scaffolding - provide support then gradually remove it
• Connect new skills to previously mastered techniques
• Practice skills with graduated difficulty levels
• Celebrate skill development and progress
• Address obstacles to skill application
• Customize techniques to patient's learning style and preferences

Remember: Skill building is a gradual process. Focus on solid mastery at each level before advancing!
"""
        
        return prompt


class CognitiveInterventionWorkflow:
    """Manages complete cognitive intervention workflow"""
    
    def __init__(self):
        self.prompts = CognitiveInterventionPrompts()
        self.workflow_templates = self._initialize_workflow_templates()
    
    def _initialize_workflow_templates(self) -> Dict[CognitiveInterventionType, List[SessionPhase]]:
        """Initialize workflow templates for different cognitive interventions"""
        
        return {
            CognitiveInterventionType.COGNITIVE_RESTRUCTURING: [
                SessionPhase.ASSESSMENT,
                SessionPhase.PSYCHOEDUCATION,
                SessionPhase.THOUGHT_IDENTIFICATION,
                SessionPhase.EVIDENCE_EXAMINATION,
                SessionPhase.ALTERNATIVE_GENERATION,
                SessionPhase.PRACTICE,
                SessionPhase.HOMEWORK_ASSIGNMENT,
                SessionPhase.REVIEW
            ],
            
            CognitiveInterventionType.THOUGHT_CHALLENGING: [
                SessionPhase.THOUGHT_IDENTIFICATION,
                SessionPhase.EVIDENCE_EXAMINATION,
                SessionPhase.PRACTICE,
                SessionPhase.HOMEWORK_ASSIGNMENT,
                SessionPhase.REVIEW
            ],
            
            CognitiveInterventionType.DISTORTION_IDENTIFICATION: [
                SessionPhase.PSYCHOEDUCATION,
                SessionPhase.DISTORTION_IDENTIFICATION,
                SessionPhase.PRACTICE,
                SessionPhase.HOMEWORK_ASSIGNMENT,
                SessionPhase.REVIEW
            ],
            
            CognitiveInterventionType.THOUGHT_RECORDS: [
                SessionPhase.PSYCHOEDUCATION,
                SessionPhase.PRACTICE,
                SessionPhase.HOMEWORK_ASSIGNMENT,
                SessionPhase.REVIEW,
                SessionPhase.INTEGRATION
            ]
        }
    
    def get_workflow_prompt(
        self,
        intervention_type: CognitiveInterventionType,
        current_phase: SessionPhase,
        context: CognitiveInterventionContext,
        session_number: int = 1
    ) -> str:
        """Get workflow-appropriate prompt for current phase"""
        
        workflow = self.workflow_templates.get(intervention_type, [])
        
        if current_phase not in workflow:
            return self.prompts.get_cognitive_intervention_prompt(
                intervention_type, current_phase, context
            )
        
        phase_index = workflow.index(current_phase)
        total_phases = len(workflow)
        
        base_prompt = self.prompts.get_cognitive_intervention_prompt(
            intervention_type, current_phase, context
        )
        
        workflow_info = f"""
COGNITIVE INTERVENTION WORKFLOW:
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
    """Example of how to use the cognitive intervention prompt system"""
    
    # Initialize the cognitive intervention system
    cognitive_system = CognitiveInterventionPrompts()
    
    # Create patient context
    context = CognitiveInterventionContext(
        patient_id="PATIENT_001",
        session_id="SESSION_004",
        presenting_symptoms=["depression", "anxiety", "negative thinking"],
        thought_patterns=["self-criticism", "catastrophizing", "all-or-nothing thinking"],
        identified_distortions=[CognitiveDistortion.ALL_OR_NOTHING, CognitiveDistortion.CATASTROPHIZING],
        emotional_intensity=7,
        previous_thought_records=3,
        successful_challenges=["evidence examination", "best friend technique"],
        persistent_beliefs=["I'm not good enough", "I always mess things up"],
        cognitive_flexibility="moderate",
        insight_level="developing",
        homework_compliance="good",
        motivation_for_change=8,
        education_level="college",
        preferred_learning_style="visual and written"
    )
    
    # Get cognitive restructuring assessment prompt
    restructuring_prompt = cognitive_system.get_cognitive_intervention_prompt(
        CognitiveInterventionType.COGNITIVE_RESTRUCTURING,
        SessionPhase.ASSESSMENT,
        context
    )
    
    print("COGNITIVE RESTRUCTURING ASSESSMENT PROMPT:")
    print("=" * 60)
    print(restructuring_prompt)
    print("\n")
    
    # Get distortion-specific prompt
    distortion_prompt = cognitive_system.get_distortion_specific_prompt(
        CognitiveDistortion.ALL_OR_NOTHING,
        context,
        SessionPhase.PRACTICE
    )
    
    print("ALL-OR-NOTHING DISTORTION PROMPT:")
    print("=" * 60)
    print(distortion_prompt)
    print("\n")
    
    # Get thought record training prompt
    thought_record_prompt = cognitive_system.get_thought_record_training_prompt(
        "basic_thought_record",
        context,
        "beginner"
    )
    
    print("THOUGHT RECORD TRAINING PROMPT:")
    print("=" * 60)
    print(thought_record_prompt)
    print("\n")


if __name__ == "__main__":
    example_usage()
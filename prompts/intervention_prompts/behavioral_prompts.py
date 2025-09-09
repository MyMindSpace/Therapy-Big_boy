"""
Behavioral Intervention Prompts Module
Professional behavioral intervention prompts for AI therapy system
Specialized prompts for behavioral activation, exposure therapy, activity scheduling, and behavioral experiments
"""

from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime, timedelta


class BehavioralInterventionType(Enum):
    """Types of behavioral interventions"""
    BEHAVIORAL_ACTIVATION = "behavioral_activation"
    ACTIVITY_SCHEDULING = "activity_scheduling"
    BEHAVIORAL_EXPERIMENTS = "behavioral_experiments"
    EXPOSURE_THERAPY = "exposure_therapy"
    GRADED_EXPOSURE = "graded_exposure"
    RESPONSE_PREVENTION = "response_prevention"
    HOMEWORK_ASSIGNMENTS = "homework_assignments"
    HABIT_FORMATION = "habit_formation"
    BEHAVIORAL_CHAIN_ANALYSIS = "behavioral_chain_analysis"
    CONTINGENCY_MANAGEMENT = "contingency_management"
    RELAXATION_TRAINING = "relaxation_training"
    ACTIVITY_MONITORING = "activity_monitoring"


class ActivityType(Enum):
    """Types of activities for behavioral activation"""
    PLEASANT = "pleasant"
    MASTERY = "mastery"
    SOCIAL = "social"
    PHYSICAL = "physical"
    ROUTINE = "routine"
    CREATIVE = "creative"
    SPIRITUAL = "spiritual"
    EDUCATIONAL = "educational"
    SELF_CARE = "self_care"
    MEANINGFUL = "meaningful"


class ExposureType(Enum):
    """Types of exposure interventions"""
    IN_VIVO = "in_vivo"
    IMAGINAL = "imaginal"
    INTEROCEPTIVE = "interoceptive"
    VIRTUAL_REALITY = "virtual_reality"
    COGNITIVE = "cognitive"
    BEHAVIORAL = "behavioral"


class SessionPhase(Enum):
    """Phases of behavioral intervention sessions"""
    ASSESSMENT = "assessment"
    PLANNING = "planning"
    IMPLEMENTATION = "implementation"
    PRACTICE = "practice"
    REVIEW = "review"
    HOMEWORK_ASSIGNMENT = "homework_assignment"
    PROGRESS_EVALUATION = "progress_evaluation"
    TROUBLESHOOTING = "troubleshooting"


class DifficultyLevel(Enum):
    """Difficulty levels for behavioral interventions"""
    VERY_EASY = 1
    EASY = 2
    MODERATE = 3
    CHALLENGING = 4
    DIFFICULT = 5


@dataclass
class BehavioralPromptTemplate:
    """Template for behavioral intervention prompts"""
    intervention_type: BehavioralInterventionType
    phase: SessionPhase
    primary_prompt: str
    follow_up_questions: List[str]
    implementation_steps: List[str]
    common_obstacles: List[str]
    troubleshooting_strategies: List[str]
    outcome_measures: List[str]
    homework_assignments: List[str]
    therapeutic_rationale: str
    clinical_considerations: List[str]


@dataclass
class BehavioralInterventionContext:
    """Context for behavioral interventions"""
    patient_id: str
    session_id: str
    current_symptoms: List[str]
    target_behaviors: List[str]
    avoidance_patterns: List[str]
    activity_level: str  # "very_low", "low", "moderate", "high"
    motivation_level: int  # 1-10 scale
    previous_assignments: List[Dict[str, Any]]
    successful_strategies: List[str]
    barriers_encountered: List[str]
    support_system: List[str]
    available_time: str
    physical_limitations: List[str]
    preferred_activities: List[str]


class BehavioralInterventionPrompts:
    """Comprehensive behavioral intervention prompt system"""
    
    def __init__(self):
        self.prompt_templates = self._initialize_behavioral_prompts()
        self.activity_suggestions = self._initialize_activity_suggestions()
        self.exposure_protocols = self._initialize_exposure_protocols()
        self.homework_templates = self._initialize_homework_templates()
        self.troubleshooting_guides = self._initialize_troubleshooting_guides()
    
    def get_behavioral_intervention_prompt(
        self,
        intervention_type: BehavioralInterventionType,
        phase: SessionPhase,
        context: BehavioralInterventionContext,
        session_info: Dict[str, Any] = None
    ) -> str:
        """Generate contextual behavioral intervention prompt"""
        
        template = self.prompt_templates.get((intervention_type, phase))
        if not template:
            return self._get_generic_behavioral_prompt(intervention_type, phase)
        
        context_info = self._format_behavioral_context(context, session_info)
        
        prompt = f"""
{template.primary_prompt}

PATIENT CONTEXT:
{context_info}

THERAPEUTIC RATIONALE:
{template.therapeutic_rationale}

IMPLEMENTATION STEPS:
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(template.implementation_steps))}

FOLLOW-UP QUESTIONS:
{chr(10).join(f"• {question}" for question in template.follow_up_questions)}

COMMON OBSTACLES & SOLUTIONS:
{chr(10).join(f"• Obstacle: {obstacle}" for obstacle in template.common_obstacles)}

TROUBLESHOOTING STRATEGIES:
{chr(10).join(f"• {strategy}" for strategy in template.troubleshooting_strategies)}

OUTCOME MEASURES:
{chr(10).join(f"• {measure}" for measure in template.outcome_measures)}

CLINICAL CONSIDERATIONS:
{chr(10).join(f"• {consideration}" for consideration in template.clinical_considerations)}

APPROACH:
- Use a collaborative, non-judgmental approach
- Start with small, achievable steps
- Emphasize the connection between behavior and mood
- Validate difficulties while encouraging action
- Focus on progress, not perfection
- Provide specific, concrete guidance
"""
        
        return prompt
    
    def _initialize_behavioral_prompts(self) -> Dict[Tuple[BehavioralInterventionType, SessionPhase], BehavioralPromptTemplate]:
        """Initialize comprehensive behavioral intervention prompts"""
        
        prompts = {}
        
        # BEHAVIORAL ACTIVATION PROMPTS
        prompts[(BehavioralInterventionType.BEHAVIORAL_ACTIVATION, SessionPhase.ASSESSMENT)] = BehavioralPromptTemplate(
            intervention_type=BehavioralInterventionType.BEHAVIORAL_ACTIVATION,
            phase=SessionPhase.ASSESSMENT,
            primary_prompt="""
You are conducting a behavioral activation assessment. The goal is to understand the patient's current activity patterns, identify areas of behavioral avoidance, and assess the relationship between their activities and mood.

Start by saying: "I'd like to understand how you've been spending your time lately and how different activities affect your mood. This will help us identify ways to improve how you're feeling through changing some of your daily activities."

Explore their current activity patterns, energy levels, and the connection between their behaviors and emotions.
""",
            follow_up_questions=[
                "Can you walk me through a typical day for you?",
                "What activities do you find yourself avoiding lately?",
                "When do you notice your mood is best during the day?",
                "What activities used to give you pleasure that you're not doing now?",
                "How has your activity level changed since your symptoms began?",
                "What prevents you from doing things you used to enjoy?",
                "On a scale of 1-10, how would you rate your overall energy level?",
                "What time of day do you feel most motivated?"
            ],
            implementation_steps=[
                "Conduct activity monitoring assessment",
                "Identify patterns of avoidance and withdrawal",
                "Assess baseline mood and energy levels",
                "Explore historical activity preferences",
                "Identify barriers to activity engagement",
                "Assess available time and resources"
            ],
            common_obstacles=[
                "Low motivation and energy",
                "Overwhelming nature of tasks",
                "Perfectionist tendencies",
                "Social anxiety or isolation",
                "Lack of structure or routine",
                "Physical health limitations"
            ],
            troubleshooting_strategies=[
                "Start with very small, manageable activities",
                "Schedule activities during highest energy times",
                "Use accountability partners or support systems",
                "Break large tasks into smaller components",
                "Address perfectionist thinking patterns",
                "Modify activities to accommodate limitations"
            ],
            outcome_measures=[
                "Daily activity completion rates",
                "Mood ratings before and after activities",
                "Overall activity level increase",
                "Pleasure and mastery ratings",
                "Reduction in avoidance behaviors",
                "Improvement in daily functioning"
            ],
            homework_assignments=[
                "Complete daily activity and mood monitoring log",
                "Identify three previously enjoyed activities",
                "Schedule one small pleasant activity for tomorrow",
                "Notice and record activity-mood connections"
            ],
            therapeutic_rationale="Behavioral activation is based on the principle that depression is maintained by avoidance and withdrawal from positive reinforcement. By gradually increasing meaningful activities, patients can improve mood and break the cycle of depression.",
            clinical_considerations=[
                "Start with assessment before intervention",
                "Consider patient's baseline functioning level",
                "Assess for safety and risk factors",
                "Address motivation and readiness for change",
                "Consider cultural and personal values in activity selection"
            ]
        )
        
        prompts[(BehavioralInterventionType.BEHAVIORAL_ACTIVATION, SessionPhase.PLANNING)] = BehavioralPromptTemplate(
            intervention_type=BehavioralInterventionType.BEHAVIORAL_ACTIVATION,
            phase=SessionPhase.PLANNING,
            primary_prompt="""
You are creating a behavioral activation plan with the patient. The goal is to collaboratively develop a structured, achievable plan for increasing meaningful activities that can improve mood and functioning.

Say: "Based on what we've learned about your current activity patterns, let's work together to create a plan for gradually increasing activities that can help improve your mood. We'll start small and build from there."

Focus on creating a realistic, step-by-step plan that balances pleasant activities, mastery activities, and necessary routine tasks.
""",
            follow_up_questions=[
                "What activities would you most like to start doing again?",
                "What's a small step toward that activity you could take this week?",
                "When during your day would be the best time for this activity?",
                "What support or resources do you need to make this happen?",
                "How will we know if this plan is working for you?",
                "What might get in the way of following through with this plan?"
            ],
            implementation_steps=[
                "Review assessment findings with patient",
                "Collaboratively identify target activities",
                "Create hierarchy from easy to challenging activities",
                "Schedule specific times for activities",
                "Plan for potential obstacles",
                "Establish monitoring and feedback systems"
            ],
            common_obstacles=[
                "Overly ambitious initial goals",
                "Lack of specific planning",
                "Not accounting for energy fluctuations",
                "Insufficient backup plans",
                "Lack of social support",
                "Competing demands and priorities"
            ],
            troubleshooting_strategies=[
                "Reduce activity goals to ensure success",
                "Create specific implementation intentions",
                "Plan activities for optimal energy times",
                "Develop contingency plans for bad days",
                "Involve support system in planning",
                "Prioritize most important activities"
            ],
            outcome_measures=[
                "Completion of planned activities",
                "Patient satisfaction with plan",
                "Mood improvement after activities",
                "Adherence to activity schedule",
                "Quality of activities engaged in"
            ],
            homework_assignments=[
                "Follow activity schedule for upcoming week",
                "Rate mood before and after each planned activity",
                "Note any obstacles encountered",
                "Identify one additional activity to add next week"
            ],
            therapeutic_rationale="Systematic planning increases the likelihood of successful behavioral change by providing structure, accountability, and clear expectations while building on patient strengths and preferences.",
            clinical_considerations=[
                "Ensure plan is realistic and achievable",
                "Balance different types of activities",
                "Consider patient's individual circumstances",
                "Plan for setbacks and difficult days",
                "Maintain flexibility while providing structure"
            ]
        )
        
        # ACTIVITY SCHEDULING PROMPTS
        prompts[(BehavioralInterventionType.ACTIVITY_SCHEDULING, SessionPhase.IMPLEMENTATION)] = BehavioralPromptTemplate(
            intervention_type=BehavioralInterventionType.ACTIVITY_SCHEDULING,
            phase=SessionPhase.IMPLEMENTATION,
            primary_prompt="""
You are implementing activity scheduling with the patient. This involves creating a specific, detailed schedule of activities designed to increase pleasure, mastery, and routine while reducing avoidance and isolation.

Say: "Let's create a detailed activity schedule for the upcoming week. We'll include activities that give you pleasure, help you feel accomplished, and maintain important routines. The key is to be specific about when and how you'll do each activity."

Work collaboratively to create a realistic weekly schedule that includes a balance of different activity types.
""",
            follow_up_questions=[
                "What time of day do you typically have the most energy?",
                "Which days of the week are easiest for you to try new activities?",
                "How long can you realistically commit to each activity?",
                "What backup activities can we plan for difficult days?",
                "Who in your support system could help with these activities?",
                "How will you remind yourself to follow through with the schedule?"
            ],
            implementation_steps=[
                "Create weekly activity calendar template",
                "Schedule pleasant activities during optimal times",
                "Include mastery activities when energy is adequate",
                "Plan routine activities for structure",
                "Build in flexibility for difficult days",
                "Set up reminder systems and accountability"
            ],
            common_obstacles=[
                "Perfectionist expectations",
                "All-or-nothing thinking",
                "Unexpected schedule disruptions",
                "Lack of motivation on difficult days",
                "Social anxiety about planned activities",
                "Overcommitting to too many activities"
            ],
            troubleshooting_strategies=[
                "Emphasize progress over perfection",
                "Create backup plans for disruptions",
                "Develop strategies for low-motivation days",
                "Practice anxiety management for social activities",
                "Adjust schedule based on experience",
                "Start with fewer activities and gradually increase"
            ],
            outcome_measures=[
                "Weekly activity completion percentage",
                "Daily mood ratings",
                "Pleasure and mastery ratings for activities",
                "Overall weekly satisfaction",
                "Reduction in unstructured/empty time"
            ],
            homework_assignments=[
                "Follow detailed activity schedule",
                "Complete daily activity and mood log",
                "Rate pleasure (P) and mastery (M) for each activity",
                "Note which activities were most helpful"
            ],
            therapeutic_rationale="Structured activity scheduling helps break the cycle of depression by ensuring regular engagement in meaningful activities, providing structure to combat amotivation, and creating opportunities for positive experiences and accomplishment.",
            clinical_considerations=[
                "Balance structure with flexibility",
                "Consider patient's natural rhythms and preferences",
                "Include variety to prevent boredom",
                "Plan for gradual increase in activity level",
                "Monitor for signs of overwhelm or burnout"
            ]
        )
        
        # BEHAVIORAL EXPERIMENTS PROMPTS
        prompts[(BehavioralInterventionType.BEHAVIORAL_EXPERIMENTS, SessionPhase.PLANNING)] = BehavioralPromptTemplate(
            intervention_type=BehavioralInterventionType.BEHAVIORAL_EXPERIMENTS,
            phase=SessionPhase.PLANNING,
            primary_prompt="""
You are designing a behavioral experiment with the patient. The goal is to test negative predictions or beliefs by conducting a real-world experiment that provides evidence about the accuracy of their thoughts and fears.

Say: "Let's design an experiment to test some of the thoughts or predictions you've been having. By trying out specific behaviors, we can gather real evidence about whether your concerns are as likely or as catastrophic as you expect them to be."

Focus on creating a specific, measurable experiment that directly tests the patient's predictions or avoidance behaviors.
""",
            follow_up_questions=[
                "What specific prediction or belief would you like to test?",
                "What do you think will happen if you try this behavior?",
                "How confident are you that this prediction will come true? (1-10)",
                "What would be a small step toward testing this prediction?",
                "How will we measure the outcome of this experiment?",
                "What would you learn if your prediction doesn't come true?",
                "What safety measures do we need to include?"
            ],
            implementation_steps=[
                "Identify specific belief or prediction to test",
                "Define the behavioral experiment clearly",
                "Make specific predictions about outcomes",
                "Plan measurement and observation methods",
                "Identify safety measures and supports",
                "Schedule the experiment for specific time/place"
            ],
            common_obstacles=[
                "Fear of confirming negative predictions",
                "Experiments that are too ambitious",
                "Vague or unmeasurable predictions",
                "Lack of motivation to follow through",
                "Safety concerns about the experiment",
                "Cognitive avoidance or rationalization"
            ],
            troubleshooting_strategies=[
                "Start with lower-stakes experiments",
                "Break large experiments into smaller steps",
                "Make predictions very specific and measurable",
                "Use motivation enhancement techniques",
                "Plan appropriate safety measures",
                "Anticipate and address avoidance strategies"
            ],
            outcome_measures=[
                "Completion of planned experiment",
                "Accuracy of pre-experiment predictions",
                "Confidence in belief before vs. after",
                "Learning and insights gained",
                "Willingness to try similar experiments"
            ],
            homework_assignments=[
                "Conduct the planned behavioral experiment",
                "Record detailed observations and outcomes",
                "Compare actual results to predictions",
                "Identify key learnings from the experience"
            ],
            therapeutic_rationale="Behavioral experiments provide direct, experiential evidence that can challenge negative beliefs and predictions more powerfully than cognitive techniques alone, leading to lasting behavioral and cognitive change.",
            clinical_considerations=[
                "Ensure experiments are safe and ethical",
                "Start with lower-risk experiments",
                "Plan for unexpected outcomes",
                "Process results thoroughly",
                "Connect learnings to broader patterns"
            ]
        )
        
        # EXPOSURE THERAPY PROMPTS
        prompts[(BehavioralInterventionType.EXPOSURE_THERAPY, SessionPhase.ASSESSMENT)] = BehavioralPromptTemplate(
            intervention_type=BehavioralInterventionType.EXPOSURE_THERAPY,
            phase=SessionPhase.ASSESSMENT,
            primary_prompt="""
You are conducting an exposure therapy assessment. The goal is to identify specific fears, avoidance behaviors, and create a hierarchy of anxiety-provoking situations for systematic exposure treatment.

Say: "I'd like to understand what situations or things you've been avoiding because they make you anxious or afraid. We'll work together to create a plan for gradually facing these fears in a safe, controlled way."

Focus on detailed assessment of fears, avoidance patterns, and the impact on the patient's life.
""",
            follow_up_questions=[
                "What specific situations do you find yourself avoiding?",
                "On a scale of 1-10, how anxious do these situations make you?",
                "How has this avoidance affected your daily life?",
                "What do you think will happen if you face these situations?",
                "Have you ever faced similar fears successfully in the past?",
                "What physical sensations do you notice when anxious?",
                "What safety behaviors do you use in feared situations?"
            ],
            implementation_steps=[
                "Identify all avoided situations and triggers",
                "Rate anxiety level for each situation (1-10)",
                "Assess impact on functioning and quality of life",
                "Explore catastrophic predictions and expectations",
                "Identify safety behaviors and escape routes used",
                "Create exposure hierarchy from easiest to hardest"
            ],
            common_obstacles=[
                "Reluctance to face feared situations",
                "Catastrophic thinking about exposure",
                "History of traumatic experiences",
                "Secondary gains from avoidance",
                "Lack of understanding of exposure rationale",
                "Physical health concerns or limitations"
            ],
            troubleshooting_strategies=[
                "Provide thorough psychoeducation about exposure",
                "Start with very gradual, manageable exposures",
                "Address catastrophic thinking patterns",
                "Explore benefits of facing fears",
                "Use motivational interviewing techniques",
                "Consider medical clearance if needed"
            ],
            outcome_measures=[
                "Number of situations avoided",
                "Anxiety ratings for specific situations",
                "Functional impairment assessment",
                "Quality of life measures",
                "Avoidance behavior frequency"
            ],
            homework_assignments=[
                "Complete fear and avoidance inventory",
                "Monitor anxiety levels in different situations",
                "Identify current safety behaviors used",
                "Keep anxiety diary for one week"
            ],
            therapeutic_rationale="Exposure therapy is based on principles of habituation and inhibitory learning, where repeated exposure to feared stimuli in a safe context leads to reduction in fear and avoidance.",
            clinical_considerations=[
                "Assess for trauma history that might complicate exposure",
                "Consider co-occurring conditions",
                "Evaluate patient motivation and readiness",
                "Plan for appropriate pacing and safety",
                "Consider need for additional support"
            ]
        )
        
        prompts[(BehavioralInterventionType.EXPOSURE_THERAPY, SessionPhase.IMPLEMENTATION)] = BehavioralPromptTemplate(
            intervention_type=BehavioralInterventionType.EXPOSURE_THERAPY,
            phase=SessionPhase.IMPLEMENTATION,
            primary_prompt="""
You are implementing an exposure therapy session. The goal is to guide the patient through a planned exposure exercise while monitoring anxiety levels and ensuring safety throughout the process.

Say: "Today we're going to practice facing [specific fear] together. Remember, the goal isn't to eliminate anxiety completely, but to learn that you can handle the anxiety and that it will decrease naturally over time."

Focus on supporting the patient through the exposure while monitoring anxiety and preventing avoidance or escape behaviors.
""",
            follow_up_questions=[
                "What's your anxiety level right now on a scale of 1-10?",
                "What thoughts are going through your mind?",
                "What physical sensations are you noticing?",
                "What urges are you having right now?",
                "How is this different from what you expected?",
                "What are you learning from this experience?"
            ],
            implementation_steps=[
                "Review exposure plan and rationale",
                "Establish baseline anxiety rating",
                "Begin exposure at planned intensity level",
                "Monitor anxiety ratings every few minutes",
                "Encourage staying in situation until anxiety decreases",
                "Process experience and learnings afterward"
            ],
            common_obstacles=[
                "Premature escape from exposure",
                "Overwhelming anxiety levels",
                "Use of safety behaviors during exposure",
                "Catastrophic thinking during exposure",
                "Physical symptoms of panic",
                "Resistance to continuing exposure"
            ],
            troubleshooting_strategies=[
                "Use grounding and breathing techniques",
                "Reduce exposure intensity if needed",
                "Block safety behaviors gently",
                "Challenge catastrophic thoughts",
                "Normalize physical anxiety symptoms",
                "Provide encouragement and support"
            ],
            outcome_measures=[
                "Peak anxiety level during exposure",
                "Final anxiety level at end of exposure",
                "Duration able to stay in exposure",
                "Use of safety behaviors",
                "Learning and insights gained"
            ],
            homework_assignments=[
                "Practice similar exposure independently",
                "Record anxiety levels during practice",
                "Notice and record any learning or changes",
                "Prepare for next level exposure"
            ],
            therapeutic_rationale="Direct exposure allows for new learning to occur, where patients discover that feared outcomes are less likely and less catastrophic than expected, and that anxiety naturally decreases over time.",
            clinical_considerations=[
                "Monitor for signs of overwhelming distress",
                "Ensure patient doesn't leave during peak anxiety",
                "Balance support with independence",
                "Process experience thoroughly",
                "Plan appropriate next steps"
            ]
        )
        
        # HOMEWORK ASSIGNMENT PROMPTS
        prompts[(BehavioralInterventionType.HOMEWORK_ASSIGNMENTS, SessionPhase.PLANNING)] = BehavioralPromptTemplate(
            intervention_type=BehavioralInterventionType.HOMEWORK_ASSIGNMENTS,
            phase=SessionPhase.PLANNING,
            primary_prompt="""
You are creating behavioral homework assignments that will help the patient practice skills and make progress between sessions. The goal is to design specific, achievable assignments that reinforce session learning and promote behavioral change.

Say: "Let's plan some specific activities for you to practice this week. These assignments will help you continue the work we're doing here and make real progress toward your goals."

Focus on creating clear, specific, and achievable assignments that connect to session content and patient goals.
""",
            follow_up_questions=[
                "Which of today's skills or insights would be most helpful to practice?",
                "When during your week would be the best time for this practice?",
                "What obstacles might prevent you from completing this assignment?",
                "How can we make this assignment more specific and doable?",
                "What support do you need to be successful with this?",
                "How will you track your progress with this assignment?"
            ],
            implementation_steps=[
                "Connect assignment to session learning",
                "Make assignment specific and measurable",
                "Ensure assignment is appropriately challenging",
                "Plan timing and logistics",
                "Anticipate and plan for obstacles",
                "Create tracking and accountability systems"
            ],
            common_obstacles=[
                "Assignments too vague or general",
                "Unrealistic expectations or difficulty level",
                "Lack of connection to patient goals",
                "Poor timing or logistics planning",
                "Inadequate motivation or buy-in",
                "Competing priorities and demands"
            ],
            troubleshooting_strategies=[
                "Make assignments very specific and concrete",
                "Start with easier assignments to build confidence",
                "Clearly connect to patient's stated goals",
                "Plan specific times and methods",
                "Use motivational interviewing to increase buy-in",
                "Help prioritize and manage competing demands"
            ],
            outcome_measures=[
                "Completion rate of assignments",
                "Quality of assignment completion",
                "Learning and insights from practice",
                "Skill improvement or behavior change",
                "Patient satisfaction with assignments"
            ],
            homework_assignments=[
                "Complete assigned behavioral practice",
                "Track completion and outcomes",
                "Note any obstacles or difficulties",
                "Identify learnings and insights"
            ],
            therapeutic_rationale="Homework assignments extend therapy benefits beyond sessions, provide opportunities for real-world skill practice, and accelerate progress toward therapeutic goals.",
            clinical_considerations=[
                "Ensure assignments match patient's current ability",
                "Consider patient's schedule and resources",
                "Balance structure with flexibility",
                "Review and adjust based on experience",
                "Maintain connection to overall treatment goals"
            ]
        )
        
        return prompts
    
    def _initialize_activity_suggestions(self) -> Dict[ActivityType, List[Dict[str, Any]]]:
        """Initialize activity suggestions for behavioral activation"""
        
        return {
            ActivityType.PLEASANT: [
                {"name": "Listen to favorite music", "duration": 30, "difficulty": 1, "materials": ["music player"]},
                {"name": "Take a warm bath or shower", "duration": 20, "difficulty": 1, "materials": ["bath supplies"]},
                {"name": "Watch a funny video or show", "duration": 30, "difficulty": 1, "materials": ["TV/computer"]},
                {"name": "Call a friend or family member", "duration": 30, "difficulty": 2, "materials": ["phone"]},
                {"name": "Read a book or magazine", "duration": 45, "difficulty": 2, "materials": ["reading material"]},
                {"name": "Work on a hobby or craft", "duration": 60, "difficulty": 3, "materials": ["hobby supplies"]},
                {"name": "Go to a movie or concert", "duration": 120, "difficulty": 4, "materials": ["tickets", "transportation"]},
                {"name": "Plan a social gathering", "duration": 90, "difficulty": 5, "materials": ["planning materials"]}
            ],
            ActivityType.MASTERY: [
                {"name": "Organize a small area", "duration": 30, "difficulty": 2, "materials": ["organizing supplies"]},
                {"name": "Learn something new online", "duration": 45, "difficulty": 3, "materials": ["computer/tablet"]},
                {"name": "Cook a healthy meal", "duration": 60, "difficulty": 3, "materials": ["ingredients", "cooking utensils"]},
                {"name": "Complete a work project", "duration": 90, "difficulty": 4, "materials": ["work materials"]},
                {"name": "Fix something around the house", "duration": 60, "difficulty": 4, "materials": ["tools", "supplies"]},
                {"name": "Start a new skill or course", "duration": 120, "difficulty": 5, "materials": ["course materials"]}
            ],
            ActivityType.SOCIAL: [
                {"name": "Text or message someone", "duration": 10, "difficulty": 1, "materials": ["phone"]},
                {"name": "Have coffee with a friend", "duration": 90, "difficulty": 3, "materials": ["money"]},
                {"name": "Join a group activity", "duration": 120, "difficulty": 4, "materials": ["activity materials"]},
                {"name": "Volunteer for a cause", "duration": 180, "difficulty": 4, "materials": ["commitment"]},
                {"name": "Attend a social event", "duration": 150, "difficulty": 5, "materials": ["appropriate clothing"]}
            ],
            ActivityType.PHYSICAL: [
                {"name": "Take a short walk", "duration": 15, "difficulty": 1, "materials": ["walking shoes"]},
                {"name": "Do gentle stretching", "duration": 20, "difficulty": 1, "materials": ["comfortable clothes"]},
                {"name": "Dance to music", "duration": 30, "difficulty": 2, "materials": ["music"]},
                {"name": "Go for a bike ride", "duration": 45, "difficulty": 3, "materials": ["bicycle", "helmet"]},
                {"name": "Join a fitness class", "duration": 60, "difficulty": 4, "materials": ["workout clothes", "membership"]},
                {"name": "Play a sport", "duration": 90, "difficulty": 4, "materials": ["sports equipment"]}
            ],
            ActivityType.ROUTINE: [
                {"name": "Make your bed", "duration": 5, "difficulty": 1, "materials": []},
                {"name": "Do the dishes", "duration": 20, "difficulty": 1, "materials": ["dish soap"]},
                {"name": "Take a shower", "duration": 20, "difficulty": 1, "materials": ["toiletries"]},
                {"name": "Grocery shopping", "duration": 60, "difficulty": 2, "materials": ["shopping list", "money"]},
                {"name": "Clean a room", "duration": 45, "difficulty": 3, "materials": ["cleaning supplies"]},
                {"name": "Pay bills", "duration": 30, "difficulty": 3, "materials": ["bills", "checkbook/computer"]}
            ]
        }
    
    def _initialize_exposure_protocols(self) -> Dict[str, Dict[str, Any]]:
        """Initialize exposure therapy protocols"""
        
        return {
            "social_anxiety": {
                "hierarchy_levels": [
                    {"level": 1, "description": "Make eye contact with stranger", "anxiety_rating": 2},
                    {"level": 2, "description": "Say hello to cashier", "anxiety_rating": 3},
                    {"level": 3, "description": "Ask for directions", "anxiety_rating": 4},
                    {"level": 4, "description": "Make small talk with acquaintance", "anxiety_rating": 5},
                    {"level": 5, "description": "Initiate conversation with new person", "anxiety_rating": 6},
                    {"level": 6, "description": "Speak up in small group", "anxiety_rating": 7},
                    {"level": 7, "description": "Give opinion in meeting", "anxiety_rating": 8},
                    {"level": 8, "description": "Give presentation to group", "anxiety_rating": 9}
                ],
                "safety_considerations": [
                    "Start in supportive environments",
                    "Have escape plan if overwhelmed",
                    "Practice grounding techniques",
                    "Start with shorter interactions"
                ]
            },
            "agoraphobia": {
                "hierarchy_levels": [
                    {"level": 1, "description": "Stand outside front door for 5 minutes", "anxiety_rating": 3},
                    {"level": 2, "description": "Walk to end of block", "anxiety_rating": 4},
                    {"level": 3, "description": "Drive to nearby store", "anxiety_rating": 5},
                    {"level": 4, "description": "Enter store briefly", "anxiety_rating": 6},
                    {"level": 5, "description": "Shop for 15 minutes", "anxiety_rating": 7},
                    {"level": 6, "description": "Visit crowded store", "anxiety_rating": 8},
                    {"level": 7, "description": "Attend public event", "anxiety_rating": 9}
                ],
                "safety_considerations": [
                    "Bring support person initially",
                    "Have phone for emergency contact",
                    "Plan route and timing",
                    "Start during less crowded times"
                ]
            },
            "specific_phobias": {
                "hierarchy_levels": [
                    {"level": 1, "description": "Look at pictures of feared object", "anxiety_rating": 3},
                    {"level": 2, "description": "Watch videos of feared object", "anxiety_rating": 4},
                    {"level": 3, "description": "Be in same room as feared object", "anxiety_rating": 5},
                    {"level": 4, "description": "Move closer to feared object", "anxiety_rating": 6},
                    {"level": 5, "description": "Touch feared object briefly", "anxiety_rating": 7},
                    {"level": 6, "description": "Hold feared object", "anxiety_rating": 8},
                    {"level": 7, "description": "Interact normally with feared object", "anxiety_rating": 9}
                ],
                "safety_considerations": [
                    "Ensure object is actually safe",
                    "Have therapist present initially",
                    "Use relaxation techniques",
                    "Progress very gradually"
                ]
            }
        }
    
    def _initialize_homework_templates(self) -> Dict[BehavioralInterventionType, List[Dict[str, Any]]]:
        """Initialize homework assignment templates"""
        
        return {
            BehavioralInterventionType.BEHAVIORAL_ACTIVATION: [
                {
                    "name": "Daily Activity and Mood Log",
                    "description": "Track activities and mood ratings throughout the day",
                    "instructions": "Record your activities hourly and rate your mood before and after each activity on a 1-10 scale",
                    "duration": "7 days",
                    "materials": ["activity log sheet", "pen"]
                },
                {
                    "name": "Pleasant Activity Scheduling",
                    "description": "Schedule and complete one pleasant activity each day",
                    "instructions": "Choose a different pleasant activity for each day and rate pleasure experienced",
                    "duration": "7 days",
                    "materials": ["activity list", "calendar"]
                },
                {
                    "name": "Mastery Activity Challenge",
                    "description": "Complete one accomplishment-focused activity",
                    "instructions": "Choose an activity that will give you a sense of achievement and record the experience",
                    "duration": "3 days",
                    "materials": ["varies by activity"]
                }
            ],
            BehavioralInterventionType.EXPOSURE_THERAPY: [
                {
                    "name": "Daily Exposure Practice",
                    "description": "Practice exposure exercise for current hierarchy level",
                    "instructions": "Complete planned exposure, record anxiety levels every 5 minutes, stay until anxiety decreases",
                    "duration": "Daily for 1 week",
                    "materials": ["anxiety tracking sheet", "timer"]
                },
                {
                    "name": "Fear Thought Challenging",
                    "description": "Challenge catastrophic predictions before exposure",
                    "instructions": "Write down predictions, complete exposure, compare actual vs. predicted outcomes",
                    "duration": "With each exposure",
                    "materials": ["thought record sheets"]
                }
            ],
            BehavioralInterventionType.BEHAVIORAL_EXPERIMENTS: [
                {
                    "name": "Prediction Testing Experiment",
                    "description": "Test specific negative prediction through behavioral experiment",
                    "instructions": "Make specific prediction, conduct experiment, record actual outcome and learning",
                    "duration": "1-2 times this week",
                    "materials": ["experiment planning sheet"]
                }
            ]
        }
    
    def _initialize_troubleshooting_guides(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize troubleshooting guides for common problems"""
        
        return {
            "low_motivation": [
                {
                    "problem": "Patient says they don't feel like doing activities",
                    "solution": "Explain that motivation follows action, not the reverse",
                    "technique": "Start with 5-minute commitment and build up",
                    "prompt": "What's the smallest step you could take toward this activity right now?"
                },
                {
                    "problem": "Patient waits to feel better before acting",
                    "solution": "Challenge the assumption that feeling must come before doing",
                    "technique": "Use 'behavioral activation' vs 'feeling activation' concept",
                    "prompt": "What if we tried acting our way into feeling better rather than waiting to feel better before acting?"
                }
            ],
            "perfectionism": [
                {
                    "problem": "Patient won't try unless they can do it perfectly",
                    "solution": "Set 'good enough' standards and emphasize learning over performance",
                    "technique": "Deliberate imperfection exercises",
                    "prompt": "What would 'good enough' look like for this activity?"
                },
                {
                    "problem": "Patient gives up after small mistakes",
                    "solution": "Normalize mistakes as part of learning process",
                    "technique": "Mistake celebration and learning extraction",
                    "prompt": "What can we learn from this experience that will help you next time?"
                }
            ],
            "overwhelming_anxiety": [
                {
                    "problem": "Anxiety too high to complete exposure",
                    "solution": "Break exposure into smaller steps or reduce intensity",
                    "technique": "Micro-exposures and grounding techniques",
                    "prompt": "Let's find an easier version of this exposure that feels manageable"
                },
                {
                    "problem": "Patient wants to escape during exposure",
                    "solution": "Use grounding techniques and stay until anxiety decreases",
                    "technique": "5-4-3-2-1 grounding and breathing exercises",
                    "prompt": "Let's use some grounding techniques to help you stay with this feeling"
                }
            ],
            "social_barriers": [
                {
                    "problem": "Patient lacks social support for activities",
                    "solution": "Help identify existing supports or develop new ones",
                    "technique": "Social network mapping and support recruitment",
                    "prompt": "Who in your life might be willing to support you with this?"
                },
                {
                    "problem": "Family or friends discourage behavioral changes",
                    "solution": "Address family dynamics and educate support system",
                    "technique": "Family education and boundary setting",
                    "prompt": "How can we help your family understand what you're trying to accomplish?"
                }
            ]
        }
    
    def _format_behavioral_context(self, context: BehavioralInterventionContext, session_info: Dict[str, Any] = None) -> str:
        """Format behavioral intervention context information"""
        
        context_lines = [
            f"Patient ID: {context.patient_id}",
            f"Current Activity Level: {context.activity_level}",
            f"Motivation Level: {context.motivation_level}/10",
            f"Available Time: {context.available_time}"
        ]
        
        if context.current_symptoms:
            context_lines.append(f"Current Symptoms: {', '.join(context.current_symptoms)}")
        
        if context.target_behaviors:
            context_lines.append(f"Target Behaviors: {', '.join(context.target_behaviors)}")
        
        if context.avoidance_patterns:
            context_lines.append(f"Avoidance Patterns: {', '.join(context.avoidance_patterns)}")
        
        if context.successful_strategies:
            context_lines.append(f"Previous Successful Strategies: {', '.join(context.successful_strategies)}")
        
        if context.barriers_encountered:
            context_lines.append(f"Known Barriers: {', '.join(context.barriers_encountered)}")
        
        if context.physical_limitations:
            context_lines.append(f"Physical Limitations: {', '.join(context.physical_limitations)}")
        
        if context.preferred_activities:
            context_lines.append(f"Preferred Activities: {', '.join(context.preferred_activities)}")
        
        return chr(10).join(context_lines)
    
    def _get_generic_behavioral_prompt(self, intervention_type: BehavioralInterventionType, phase: SessionPhase) -> str:
        """Generate generic behavioral prompt when specific template not found"""
        
        return f"""
You are implementing {intervention_type.value.replace('_', ' ')} in the {phase.value.replace('_', ' ')} phase.

GENERAL APPROACH:
- Use collaborative, non-judgmental stance
- Start with small, achievable steps
- Emphasize behavior-mood connection
- Focus on progress over perfection
- Provide specific, concrete guidance
- Address obstacles proactively

BEHAVIORAL PRINCIPLES:
- Action precedes motivation
- Small changes lead to big results
- Practice builds confidence
- Gradual exposure reduces fear
- Consistent behavior creates lasting change

Continue with systematic intervention appropriate for {intervention_type.value.replace('_', ' ')}.
"""
    
    def get_activity_suggestion_prompt(
        self,
        activity_type: ActivityType,
        difficulty_level: DifficultyLevel,
        context: BehavioralInterventionContext
    ) -> str:
        """Generate prompt for suggesting specific activities"""
        
        activities = self.activity_suggestions.get(activity_type, [])
        suitable_activities = [a for a in activities if a["difficulty"] <= difficulty_level.value]
        
        if not suitable_activities:
            suitable_activities = activities[:3]  # Default to first few if none match
        
        context_info = self._format_behavioral_context(context)
        
        prompt = f"""
You are suggesting {activity_type.value} activities at {difficulty_level.name.lower()} difficulty level.

PATIENT CONTEXT:
{context_info}

SUGGESTED ACTIVITIES:
"""
        
        for activity in suitable_activities[:5]:  # Limit to top 5
            prompt += f"""
• {activity['name']}
  - Duration: {activity['duration']} minutes
  - Difficulty: {activity['difficulty']}/5
  - Materials needed: {', '.join(activity['materials'])}
"""
        
        prompt += f"""

ACTIVITY SELECTION GUIDANCE:
- Consider patient's current energy and motivation level
- Start with activities that require minimal preparation
- Choose activities that match available time slots
- Select based on patient's interests and preferences
- Consider any physical limitations or constraints

CUSTOMIZATION QUESTIONS:
• Which of these activities appeals to you most?
• What would make this activity more enjoyable for you?
• When would be the best time to do this activity?
• What obstacles might prevent you from doing this?
• How can we modify this to fit your situation better?

APPROACH:
Work collaboratively to select and customize activities that are most likely to be completed successfully and provide positive experiences.
"""
        
        return prompt
    
    def get_exposure_hierarchy_prompt(
        self,
        fear_type: str,
        context: BehavioralInterventionContext
    ) -> str:
        """Generate prompt for creating exposure hierarchy"""
        
        protocol = self.exposure_protocols.get(fear_type, {})
        context_info = self._format_behavioral_context(context)
        
        prompt = f"""
You are creating an exposure hierarchy for {fear_type.replace('_', ' ')} with the patient.

PATIENT CONTEXT:
{context_info}

HIERARCHY CREATION PROCESS:
1. Identify all avoided situations related to the fear
2. Rate anxiety level for each situation (1-10 scale)
3. Arrange situations from least to most anxiety-provoking
4. Ensure gradual progression between levels
5. Include specific, concrete situations
6. Plan for real-world application

"""
        
        if protocol.get("hierarchy_levels"):
            prompt += f"""
EXAMPLE HIERARCHY LEVELS for {fear_type}:
"""
            for level in protocol["hierarchy_levels"]:
                prompt += f"Level {level['level']}: {level['description']} (Anxiety: {level['anxiety_rating']}/10)\n"
        
        if protocol.get("safety_considerations"):
            prompt += f"""
SAFETY CONSIDERATIONS:
{chr(10).join(f"• {consideration}" for consideration in protocol['safety_considerations'])}
"""
        
        prompt += f"""
HIERARCHY DEVELOPMENT QUESTIONS:
• What specific situations do you avoid related to this fear?
• How anxious would each situation make you (1-10)?
• What would be the easiest situation to start with?
• What situations are most important for your daily functioning?
• Are there any situations that would be unsafe to include?

CUSTOMIZATION GUIDELINES:
- Ensure hierarchy reflects patient's specific fears and goals
- Include situations relevant to patient's daily life
- Plan for gradual progression with manageable steps
- Consider patient's motivation and readiness
- Build in flexibility for individual differences

APPROACH:
Work collaboratively to create a personalized hierarchy that balances challenge with manageability, ensuring each step builds confidence for the next level.
"""
        
        return prompt
    
    def get_homework_review_prompt(
        self,
        intervention_type: BehavioralInterventionType,
        assignment_completed: bool,
        completion_details: Dict[str, Any] = None
    ) -> str:
        """Generate prompt for reviewing homework assignments"""
        
        base_prompt = f"""
You are reviewing a {intervention_type.value.replace('_', ' ')} homework assignment.

HOMEWORK COMPLETION STATUS: {'Completed' if assignment_completed else 'Not Completed'}
"""
        
        if assignment_completed and completion_details:
            base_prompt += f"""
COMPLETION DETAILS:
"""
            for key, value in completion_details.items():
                base_prompt += f"• {key.replace('_', ' ').title()}: {value}\n"
            
            base_prompt += f"""
REVIEW APPROACH FOR COMPLETED ASSIGNMENT:
1. Acknowledge the effort and completion
2. Explore what was learned from the experience
3. Identify what was most and least helpful
4. Discuss any surprises or unexpected outcomes
5. Connect learnings to overall treatment goals
6. Plan next steps and progression

REVIEW QUESTIONS:
• How did completing this assignment feel?
• What did you learn about yourself or your situation?
• What was easier or harder than expected?
• How did this assignment affect your mood or symptoms?
• What would you do differently next time?
• How does this connect to your treatment goals?
"""
        
        else:
            base_prompt += f"""
REVIEW APPROACH FOR INCOMPLETE ASSIGNMENT:
1. Explore barriers without judgment
2. Problem-solve obstacles collaboratively
3. Adjust assignment difficulty if needed
4. Increase motivation and buy-in
5. Plan specific strategies for completion
6. Consider alternative approaches

REVIEW QUESTIONS:
• What prevented you from completing this assignment?
• What obstacles came up that we didn't anticipate?
• Was the assignment too difficult or overwhelming?
• How can we modify the assignment to make it more doable?
• What support do you need to be successful?
• What would make you more motivated to try this?

TROUBLESHOOTING STRATEGIES:
• Break assignment into smaller, more manageable steps
• Address specific barriers that arose
• Increase accountability and support
• Modify timing or logistics
• Adjust difficulty level
• Explore and address motivation issues
"""
        
        base_prompt += f"""
APPROACH:
- Maintain non-judgmental, collaborative stance
- Focus on learning and problem-solving
- Validate difficulties while encouraging progress
- Adjust assignments based on experience
- Connect homework completion to overall progress
- Plan next steps that build on current experience
"""
        
        return base_prompt
    
    def get_progress_evaluation_prompt(
        self,
        intervention_type: BehavioralInterventionType,
        baseline_measures: Dict[str, Any],
        current_measures: Dict[str, Any],
        weeks_in_treatment: int
    ) -> str:
        """Generate prompt for evaluating progress in behavioral interventions"""
        
        prompt = f"""
You are evaluating progress in {intervention_type.value.replace('_', ' ')} after {weeks_in_treatment} weeks of treatment.

BASELINE MEASURES:
"""
        for measure, value in baseline_measures.items():
            prompt += f"• {measure.replace('_', ' ').title()}: {value}\n"
        
        prompt += f"""
CURRENT MEASURES:
"""
        for measure, value in current_measures.items():
            prompt += f"• {measure.replace('_', ' ').title()}: {value}\n"
        
        # Calculate improvements
        improvements = {}
        for measure in baseline_measures:
            if measure in current_measures:
                if isinstance(baseline_measures[measure], (int, float)) and isinstance(current_measures[measure], (int, float)):
                    improvement = current_measures[measure] - baseline_measures[measure]
                    improvements[measure] = improvement
        
        if improvements:
            prompt += f"""
CALCULATED IMPROVEMENTS:
"""
            for measure, improvement in improvements.items():
                direction = "increase" if improvement > 0 else "decrease" if improvement < 0 else "no change"
                prompt += f"• {measure.replace('_', ' ').title()}: {abs(improvement)} point {direction}\n"
        
        prompt += f"""
PROGRESS EVALUATION AREAS:
1. Symptom reduction and improvement
2. Functional improvement in daily life
3. Behavior change and goal achievement
4. Skill acquisition and implementation
5. Homework compliance and engagement
6. Overall treatment satisfaction

EVALUATION QUESTIONS:
• What changes have you noticed since we started working together?
• Which interventions have been most helpful?
• What areas still need more work?
• How confident do you feel in using these skills independently?
• What goals would you like to focus on moving forward?
• How satisfied are you with your progress so far?

PROGRESS INDICATORS TO ASSESS:
• Frequency of target behaviors
• Intensity of symptoms
• Functional improvement in key life areas
• Confidence in managing challenges
• Quality of life improvements
• Maintenance of treatment gains

NEXT STEPS PLANNING:
Based on progress evaluation, consider:
• Continuing current interventions
• Modifying or intensifying interventions
• Adding new intervention components
• Focusing on maintenance and relapse prevention
• Preparing for treatment termination
• Addressing remaining treatment goals

APPROACH:
- Celebrate progress made while acknowledging remaining challenges
- Use objective measures alongside subjective reports
- Identify factors contributing to success and barriers
- Collaborate on next phase of treatment planning
- Maintain realistic expectations while encouraging continued progress
"""
        
        return prompt


class BehavioralInterventionWorkflow:
    """Manages complete behavioral intervention workflow"""
    
    def __init__(self):
        self.prompts = BehavioralInterventionPrompts()
        self.workflow_templates = self._initialize_workflow_templates()
    
    def _initialize_workflow_templates(self) -> Dict[BehavioralInterventionType, List[SessionPhase]]:
        """Initialize workflow templates for different interventions"""
        
        return {
            BehavioralInterventionType.BEHAVIORAL_ACTIVATION: [
                SessionPhase.ASSESSMENT,
                SessionPhase.PLANNING,
                SessionPhase.IMPLEMENTATION,
                SessionPhase.REVIEW,
                SessionPhase.PROGRESS_EVALUATION
            ],
            BehavioralInterventionType.EXPOSURE_THERAPY: [
                SessionPhase.ASSESSMENT,
                SessionPhase.PLANNING,
                SessionPhase.PRACTICE,
                SessionPhase.IMPLEMENTATION,
                SessionPhase.REVIEW,
                SessionPhase.PROGRESS_EVALUATION
            ],
            BehavioralInterventionType.BEHAVIORAL_EXPERIMENTS: [
                SessionPhase.PLANNING,
                SessionPhase.IMPLEMENTATION,
                SessionPhase.REVIEW,
                SessionPhase.TROUBLESHOOTING
            ]
        }
    
    def get_workflow_prompt(
        self,
        intervention_type: BehavioralInterventionType,
        current_phase: SessionPhase,
        context: BehavioralInterventionContext,
        session_number: int = 1
    ) -> str:
        """Get workflow-appropriate prompt for current phase"""
        
        workflow = self.workflow_templates.get(intervention_type, [])
        
        if current_phase not in workflow:
            return self.prompts.get_behavioral_intervention_prompt(
                intervention_type, current_phase, context
            )
        
        phase_index = workflow.index(current_phase)
        total_phases = len(workflow)
        
        base_prompt = self.prompts.get_behavioral_intervention_prompt(
            intervention_type, current_phase, context
        )
        
        workflow_info = f"""
WORKFLOW CONTEXT:
Intervention: {intervention_type.value.replace('_', ' ').title()}
Current Phase: {current_phase.value.replace('_', ' ').title()} ({phase_index + 1}/{total_phases})
Session Number: {session_number}

PREVIOUS PHASES COMPLETED:
{chr(10).join(f"✓ {phase.value.replace('_', ' ').title()}" for phase in workflow[:phase_index])}

UPCOMING PHASES:
{chr(10).join(f"• {phase.value.replace('_', ' ').title()}" for phase in workflow[phase_index + 1:])}

"""
        
        return workflow_info + base_prompt


# Example usage and utility functions
def example_usage():
    """Example of how to use the behavioral intervention prompt system"""
    
    # Initialize the behavioral intervention system
    behavioral_system = BehavioralInterventionPrompts()
    
    # Create patient context
    context = BehavioralInterventionContext(
        patient_id="PATIENT_001",
        session_id="SESSION_003",
        current_symptoms=["depression", "low energy", "social withdrawal"],
        target_behaviors=["increase daily activities", "improve social connections"],
        avoidance_patterns=["avoiding social situations", "staying in bed"],
        activity_level="very_low",
        motivation_level=4,
        previous_assignments=[],
        successful_strategies=["listening to music"],
        barriers_encountered=["lack of energy", "feeling overwhelmed"],
        support_system=["spouse", "sister"],
        available_time="evenings and weekends",
        physical_limitations=[],
        preferred_activities=["reading", "cooking", "gardening"]
    )
    
    # Get behavioral activation assessment prompt
    ba_assessment_prompt = behavioral_system.get_behavioral_intervention_prompt(
        BehavioralInterventionType.BEHAVIORAL_ACTIVATION,
        SessionPhase.ASSESSMENT,
        context
    )
    
    print("BEHAVIORAL ACTIVATION ASSESSMENT PROMPT:")
    print("=" * 60)
    print(ba_assessment_prompt)
    print("\n")
    
    # Get activity suggestion prompt
    activity_prompt = behavioral_system.get_activity_suggestion_prompt(
        ActivityType.PLEASANT,
        DifficultyLevel.EASY,
        context
    )
    
    print("ACTIVITY SUGGESTION PROMPT:")
    print("=" * 60)
    print(activity_prompt)
    print("\n")
    
    # Get exposure therapy planning prompt
    exposure_context = BehavioralInterventionContext(
        patient_id="PATIENT_002",
        session_id="SESSION_005",
        current_symptoms=["social anxiety", "panic attacks"],
        target_behaviors=["increase social interactions"],
        avoidance_patterns=["avoiding parties", "not speaking up in meetings"],
        activity_level="moderate",
        motivation_level=7,
        previous_assignments=[],
        successful_strategies=["breathing exercises"],
        barriers_encountered=["fear of judgment"],
        support_system=["therapist", "best friend"],
        available_time="weekends",
        physical_limitations=[],
        preferred_activities=["small group activities"]
    )
    
    exposure_prompt = behavioral_system.get_exposure_hierarchy_prompt(
        "social_anxiety",
        exposure_context
    )
    
    print("EXPOSURE HIERARCHY PROMPT:")
    print("=" * 60)
    print(exposure_prompt)
    print("\n")


if __name__ == "__main__":
    example_usage()
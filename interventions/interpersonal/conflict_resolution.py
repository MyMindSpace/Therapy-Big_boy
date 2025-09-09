import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid
from pathlib import Path


class ConflictType(Enum):
    INTERPERSONAL = "interpersonal"
    WORKPLACE = "workplace"
    FAMILY = "family"
    ROMANTIC = "romantic"
    FRIENDSHIP = "friendship"
    NEIGHBOR = "neighbor"
    CUSTOMER_SERVICE = "customer_service"
    AUTHORITY = "authority"
    GROUP = "group"
    INTERNAL = "internal"


class ConflictSeverity(Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    SIGNIFICANT = "significant"
    MAJOR = "major"
    SEVERE = "severe"


class ConflictStatus(Enum):
    IDENTIFIED = "identified"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    UNRESOLVED = "unresolved"
    ONGOING = "ongoing"


class ResolutionStrategy(Enum):
    COLLABORATION = "collaboration"
    COMPROMISE = "compromise"
    ACCOMMODATION = "accommodation"
    AVOIDANCE = "avoidance"
    COMPETITION = "competition"
    MEDIATION = "mediation"
    NEGOTIATION = "negotiation"
    PROBLEM_SOLVING = "problem_solving"


class ConflictOutcome(Enum):
    WIN_WIN = "win_win"
    WIN_LOSE = "win_lose"
    LOSE_WIN = "lose_win"
    LOSE_LOSE = "lose_lose"
    NO_RESOLUTION = "no_resolution"
    PARTIAL_RESOLUTION = "partial_resolution"


class EmotionRegulationTechnique(Enum):
    DEEP_BREATHING = "deep_breathing"
    PAUSE_AND_COUNT = "pause_and_count"
    REFRAMING = "reframing"
    GROUNDING = "grounding"
    SELF_TALK = "self_talk"
    VISUALIZATION = "visualization"
    PHYSICAL_RELEASE = "physical_release"


@dataclass
class ConflictSituation:
    conflict_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    
    conflict_date: datetime = field(default_factory=datetime.now)
    conflict_type: ConflictType = ConflictType.INTERPERSONAL
    severity: ConflictSeverity = ConflictSeverity.MODERATE
    status: ConflictStatus = ConflictStatus.IDENTIFIED
    
    description: str = ""
    parties_involved: List[str] = field(default_factory=list)
    relationship_context: str = ""
    
    underlying_issues: List[str] = field(default_factory=list)
    surface_issues: List[str] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)
    
    personal_goals: List[str] = field(default_factory=list)
    other_party_goals: List[str] = field(default_factory=list)
    shared_interests: List[str] = field(default_factory=list)
    
    emotions_experienced: Dict[str, int] = field(default_factory=dict)
    physical_reactions: List[str] = field(default_factory=list)
    
    attempted_strategies: List[str] = field(default_factory=list)
    what_worked: List[str] = field(default_factory=list)
    what_didnt_work: List[str] = field(default_factory=list)
    
    planned_approach: str = ""
    backup_strategies: List[str] = field(default_factory=list)
    
    outcome: Optional[ConflictOutcome] = None
    resolution_description: str = ""
    lessons_learned: List[str] = field(default_factory=list)
    
    follow_up_needed: bool = False
    follow_up_plan: str = ""
    
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class ConflictResolutionSkill:
    skill_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    skill_name: str = ""
    category: str = ""
    
    description: str = ""
    when_to_use: List[str] = field(default_factory=list)
    step_by_step_guide: List[str] = field(default_factory=list)
    
    key_phrases: List[str] = field(default_factory=list)
    nonverbal_cues: List[str] = field(default_factory=list)
    
    common_mistakes: List[str] = field(default_factory=list)
    troubleshooting_tips: List[str] = field(default_factory=list)
    
    practice_scenarios: List[str] = field(default_factory=list)
    difficulty_level: int = 3
    
    prerequisites: List[str] = field(default_factory=list)
    related_skills: List[str] = field(default_factory=list)
    
    effectiveness_rating: Optional[float] = None
    usage_count: int = 0
    
    created_date: datetime = field(default_factory=datetime.now)


@dataclass
class ConflictPracticeSession:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    
    practice_date: datetime = field(default_factory=datetime.now)
    duration_minutes: int = 45
    
    conflict_scenario: str = ""
    skills_practiced: List[str] = field(default_factory=list)
    role_play_type: str = "therapist_guided"
    
    pre_session_anxiety: int = 5
    post_session_anxiety: int = 5
    pre_session_confidence: int = 3
    post_session_confidence: int = 3
    
    emotional_regulation_used: List[str] = field(default_factory=list)
    communication_techniques_used: List[str] = field(default_factory=list)
    
    challenges_encountered: List[str] = field(default_factory=list)
    breakthroughs_achieved: List[str] = field(default_factory=list)
    
    observer_feedback: str = ""
    self_reflection: str = ""
    
    areas_for_improvement: List[str] = field(default_factory=list)
    next_practice_goals: List[str] = field(default_factory=list)
    
    homework_assigned: List[str] = field(default_factory=list)
    overall_effectiveness: int = 5
    
    created_date: datetime = field(default_factory=datetime.now)


@dataclass
class ConflictAnalysis:
    analysis_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    conflict_id: str = ""
    patient_id: str = ""
    
    analysis_date: datetime = field(default_factory=datetime.now)
    
    conflict_dynamics: Dict[str, str] = field(default_factory=dict)
    power_imbalances: List[str] = field(default_factory=list)
    communication_patterns: List[str] = field(default_factory=list)
    
    escalation_triggers: List[str] = field(default_factory=list)
    de_escalation_opportunities: List[str] = field(default_factory=list)
    
    personal_contribution: List[str] = field(default_factory=list)
    other_party_contribution: List[str] = field(default_factory=list)
    
    systemic_factors: List[str] = field(default_factory=list)
    cultural_considerations: List[str] = field(default_factory=list)
    
    recommended_strategies: List[str] = field(default_factory=list)
    strategies_to_avoid: List[str] = field(default_factory=list)
    
    success_probability: int = 5
    risk_assessment: List[str] = field(default_factory=list)
    
    created_date: datetime = field(default_factory=datetime.now)


@dataclass
class ConflictResolutionPlan:
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    conflict_id: str = ""
    patient_id: str = ""
    
    created_date: datetime = field(default_factory=datetime.now)
    
    primary_strategy: ResolutionStrategy = ResolutionStrategy.COLLABORATION
    backup_strategies: List[ResolutionStrategy] = field(default_factory=list)
    
    preparation_steps: List[str] = field(default_factory=list)
    conversation_outline: List[str] = field(default_factory=list)
    
    key_messages: List[str] = field(default_factory=list)
    phrases_to_use: List[str] = field(default_factory=list)
    phrases_to_avoid: List[str] = field(default_factory=list)
    
    emotion_regulation_plan: List[str] = field(default_factory=list)
    if_things_go_wrong: List[str] = field(default_factory=list)
    
    success_criteria: List[str] = field(default_factory=list)
    acceptable_outcomes: List[str] = field(default_factory=list)
    
    timeline: str = ""
    follow_up_schedule: List[str] = field(default_factory=list)
    
    support_system: List[str] = field(default_factory=list)
    practice_needed: List[str] = field(default_factory=list)
    
    executed: bool = False
    execution_notes: str = ""
    actual_outcome: Optional[str] = None


class ConflictResolutionSystem:
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self._initialize_database()
        self._populate_resolution_skills()
    
    def _initialize_database(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conflict_situations (
                    conflict_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    conflict_date TEXT NOT NULL,
                    conflict_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    status TEXT NOT NULL,
                    description TEXT,
                    parties_involved TEXT,
                    relationship_context TEXT,
                    underlying_issues TEXT,
                    surface_issues TEXT,
                    triggers TEXT,
                    personal_goals TEXT,
                    other_party_goals TEXT,
                    shared_interests TEXT,
                    emotions_experienced TEXT,
                    physical_reactions TEXT,
                    attempted_strategies TEXT,
                    what_worked TEXT,
                    what_didnt_work TEXT,
                    planned_approach TEXT,
                    backup_strategies TEXT,
                    outcome TEXT,
                    resolution_description TEXT,
                    lessons_learned TEXT,
                    follow_up_needed BOOLEAN,
                    follow_up_plan TEXT,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conflict_resolution_skills (
                    skill_id TEXT PRIMARY KEY,
                    skill_name TEXT NOT NULL,
                    category TEXT,
                    description TEXT,
                    when_to_use TEXT,
                    step_by_step_guide TEXT,
                    key_phrases TEXT,
                    nonverbal_cues TEXT,
                    common_mistakes TEXT,
                    troubleshooting_tips TEXT,
                    practice_scenarios TEXT,
                    difficulty_level INTEGER,
                    prerequisites TEXT,
                    related_skills TEXT,
                    effectiveness_rating REAL,
                    usage_count INTEGER DEFAULT 0,
                    created_date TEXT NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conflict_practice_sessions (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    practice_date TEXT NOT NULL,
                    duration_minutes INTEGER,
                    conflict_scenario TEXT,
                    skills_practiced TEXT,
                    role_play_type TEXT,
                    pre_session_anxiety INTEGER,
                    post_session_anxiety INTEGER,
                    pre_session_confidence INTEGER,
                    post_session_confidence INTEGER,
                    emotional_regulation_used TEXT,
                    communication_techniques_used TEXT,
                    challenges_encountered TEXT,
                    breakthroughs_achieved TEXT,
                    observer_feedback TEXT,
                    self_reflection TEXT,
                    areas_for_improvement TEXT,
                    next_practice_goals TEXT,
                    homework_assigned TEXT,
                    overall_effectiveness INTEGER,
                    created_date TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conflict_analyses (
                    analysis_id TEXT PRIMARY KEY,
                    conflict_id TEXT NOT NULL,
                    patient_id TEXT NOT NULL,
                    analysis_date TEXT NOT NULL,
                    conflict_dynamics TEXT,
                    power_imbalances TEXT,
                    communication_patterns TEXT,
                    escalation_triggers TEXT,
                    de_escalation_opportunities TEXT,
                    personal_contribution TEXT,
                    other_party_contribution TEXT,
                    systemic_factors TEXT,
                    cultural_considerations TEXT,
                    recommended_strategies TEXT,
                    strategies_to_avoid TEXT,
                    success_probability INTEGER,
                    risk_assessment TEXT,
                    created_date TEXT NOT NULL,
                    FOREIGN KEY (conflict_id) REFERENCES conflict_situations (conflict_id),
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conflict_resolution_plans (
                    plan_id TEXT PRIMARY KEY,
                    conflict_id TEXT NOT NULL,
                    patient_id TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    primary_strategy TEXT,
                    backup_strategies TEXT,
                    preparation_steps TEXT,
                    conversation_outline TEXT,
                    key_messages TEXT,
                    phrases_to_use TEXT,
                    phrases_to_avoid TEXT,
                    emotion_regulation_plan TEXT,
                    if_things_go_wrong TEXT,
                    success_criteria TEXT,
                    acceptable_outcomes TEXT,
                    timeline TEXT,
                    follow_up_schedule TEXT,
                    support_system TEXT,
                    practice_needed TEXT,
                    executed BOOLEAN DEFAULT FALSE,
                    execution_notes TEXT,
                    actual_outcome TEXT,
                    FOREIGN KEY (conflict_id) REFERENCES conflict_situations (conflict_id),
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            conn.commit()
    
    def _populate_resolution_skills(self):
        skills = self._get_default_resolution_skills()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for skill in skills:
                cursor.execute("""
                    INSERT OR IGNORE INTO conflict_resolution_skills (
                        skill_id, skill_name, category, description,
                        when_to_use, step_by_step_guide, key_phrases,
                        nonverbal_cues, common_mistakes, troubleshooting_tips,
                        practice_scenarios, difficulty_level, prerequisites,
                        related_skills, effectiveness_rating, usage_count,
                        created_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    skill.skill_id, skill.skill_name, skill.category,
                    skill.description, json.dumps(skill.when_to_use),
                    json.dumps(skill.step_by_step_guide),
                    json.dumps(skill.key_phrases),
                    json.dumps(skill.nonverbal_cues),
                    json.dumps(skill.common_mistakes),
                    json.dumps(skill.troubleshooting_tips),
                    json.dumps(skill.practice_scenarios),
                    skill.difficulty_level, json.dumps(skill.prerequisites),
                    json.dumps(skill.related_skills),
                    skill.effectiveness_rating, skill.usage_count,
                    skill.created_date.isoformat()
                ))
            
            conn.commit()
    
    def _get_default_resolution_skills(self) -> List[ConflictResolutionSkill]:
        return [
            ConflictResolutionSkill(
                skill_id="active_listening_conflict",
                skill_name="Active Listening in Conflict",
                category="communication",
                description="Using focused listening to understand all perspectives in a conflict situation",
                when_to_use=[
                    "When emotions are running high",
                    "When parties feel unheard",
                    "At the beginning of conflict discussions",
                    "When trying to understand underlying issues"
                ],
                step_by_step_guide=[
                    "Create a calm environment for discussion",
                    "Give full attention to the speaker",
                    "Listen without interrupting or planning your response",
                    "Reflect back what you hear in your own words",
                    "Ask clarifying questions to deepen understanding",
                    "Acknowledge emotions you observe",
                    "Summarize key points before responding"
                ],
                key_phrases=[
                    "What I'm hearing is...",
                    "It sounds like you feel...",
                    "Help me understand...",
                    "So from your perspective...",
                    "What's most important to you about this?"
                ],
                nonverbal_cues=[
                    "Maintain appropriate eye contact",
                    "Lean in slightly to show engagement",
                    "Use nodding and minimal encouragers",
                    "Keep an open, relaxed posture",
                    "Avoid defensive body language"
                ],
                common_mistakes=[
                    "Thinking about your rebuttal while they speak",
                    "Interrupting to correct or argue",
                    "Making assumptions about their meaning",
                    "Showing judgment through facial expressions"
                ],
                troubleshooting_tips=[
                    "If you feel defensive, take a deep breath and refocus",
                    "If the person is rambling, gently guide with questions",
                    "If emotions escalate, acknowledge feelings first",
                    "If you're confused, ask for specific examples"
                ],
                practice_scenarios=[
                    "Partner complaining about household responsibilities",
                    "Coworker upset about project decisions",
                    "Family member expressing hurt feelings",
                    "Friend feeling betrayed or disappointed"
                ],
                difficulty_level=2
            ),
            
            ConflictResolutionSkill(
                skill_id="emotional_deescalation",
                skill_name="Emotional De-escalation",
                category="emotion_regulation",
                description="Techniques to calm intense emotions and reduce conflict intensity",
                when_to_use=[
                    "When emotions are escalating rapidly",
                    "When voices are getting raised",
                    "When personal attacks begin",
                    "When the conversation becomes unproductive"
                ],
                step_by_step_guide=[
                    "Recognize early signs of escalation",
                    "Lower your voice and speak more slowly",
                    "Acknowledge the emotions present",
                    "Suggest a brief pause if needed",
                    "Use calming body language",
                    "Redirect focus to the issue, not personalities",
                    "Find something you can agree on"
                ],
                key_phrases=[
                    "I can see this is really important to you",
                    "Let's take a moment to breathe",
                    "I want to understand your concerns",
                    "We're both feeling frustrated - let's step back",
                    "What if we approach this differently?"
                ],
                nonverbal_cues=[
                    "Slower, deliberate movements",
                    "Relaxed facial expression",
                    "Open palms visible",
                    "Slightly increased personal space",
                    "Calm, steady breathing"
                ],
                common_mistakes=[
                    "Telling someone to 'calm down'",
                    "Escalating your own emotions in response",
                    "Dismissing or minimizing their feelings",
                    "Using logic when emotions are high"
                ],
                troubleshooting_tips=[
                    "If they won't calm down, model calmness yourself",
                    "If they walk away, let them cool off",
                    "If you feel triggered, use self-regulation first",
                    "If nothing works, suggest continuing later"
                ],
                practice_scenarios=[
                    "Heated argument with romantic partner",
                    "Angry customer or client interaction",
                    "Family conflict during holidays",
                    "Road rage or public confrontation"
                ],
                difficulty_level=4
            ),
            
            ConflictResolutionSkill(
                skill_id="collaborative_problem_solving",
                skill_name="Collaborative Problem-Solving",
                category="negotiation",
                description="Working together to find mutually beneficial solutions",
                when_to_use=[
                    "When both parties want to resolve the issue",
                    "When there's potential for win-win outcomes",
                    "In ongoing relationships that matter",
                    "When creative solutions are possible"
                ],
                step_by_step_guide=[
                    "Define the problem clearly and objectively",
                    "Identify each party's underlying interests",
                    "Brainstorm multiple solution options",
                    "Evaluate options against both parties' needs",
                    "Choose the best solution together",
                    "Plan implementation steps",
                    "Agree on follow-up and evaluation"
                ],
                key_phrases=[
                    "What if we both...",
                    "Let's brainstorm some options",
                    "What would need to happen for this to work for both of us?",
                    "How can we make this a win-win?",
                    "What's most important to you in a solution?"
                ],
                nonverbal_cues=[
                    "Sitting side by side rather than across",
                    "Using collaborative gestures",
                    "Writing down ideas together",
                    "Maintaining engaged, forward-leaning posture",
                    "Nodding when good ideas emerge"
                ],
                common_mistakes=[
                    "Jumping to solutions too quickly",
                    "Not exploring underlying interests",
                    "Getting attached to your first idea",
                    "Ignoring implementation challenges"
                ],
                troubleshooting_tips=[
                    "If they're stuck on positions, ask about interests",
                    "If no solutions emerge, take a break and come back",
                    "If they reject all ideas, explore what's missing",
                    "If implementation fails, revisit and adjust"
                ],
                practice_scenarios=[
                    "Dividing household chores fairly",
                    "Negotiating work project responsibilities",
                    "Resolving scheduling conflicts",
                    "Finding compromise on major decisions"
                ],
                difficulty_level=3,
                prerequisites=["active_listening_conflict", "emotional_deescalation"]
            ),
            
            ConflictResolutionSkill(
                skill_id="assertive_communication",
                skill_name="Assertive Communication in Conflict",
                category="communication",
                description="Expressing your needs clearly while respecting others during conflicts",
                when_to_use=[
                    "When your needs aren't being heard",
                    "When you need to set boundaries",
                    "When addressing repeated problems",
                    "When standing up for your rights"
                ],
                step_by_step_guide=[
                    "Use 'I' statements to express your experience",
                    "Be specific about behaviors and impacts",
                    "State your needs or requests clearly",
                    "Listen to their response without becoming defensive",
                    "Be willing to negotiate on methods, not core needs",
                    "Stay calm and respectful throughout",
                    "Follow through on agreements made"
                ],
                key_phrases=[
                    "I feel... when... because...",
                    "I need... in order to...",
                    "It's important to me that...",
                    "I'm not comfortable with...",
                    "I'd like us to find a way to..."
                ],
                nonverbal_cues=[
                    "Direct but not aggressive eye contact",
                    "Upright, confident posture",
                    "Calm, steady voice tone",
                    "Appropriate personal space",
                    "Relaxed but alert body language"
                ],
                common_mistakes=[
                    "Being too aggressive or demanding",
                    "Apologizing excessively for your needs",
                    "Using 'you' statements that blame",
                    "Backing down at the first pushback"
                ],
                troubleshooting_tips=[
                    "If you feel guilty, remind yourself of your rights",
                    "If they get defensive, acknowledge their feelings first",
                    "If they dismiss your needs, restate them calmly",
                    "If you feel overwhelmed, ask for time to think"
                ],
                practice_scenarios=[
                    "Asking roommate to clean up after themselves",
                    "Telling boss you're overloaded with work",
                    "Setting boundaries with intrusive family member",
                    "Addressing friend who cancels plans frequently"
                ],
                difficulty_level=3
            ),
            
            ConflictResolutionSkill(
                skill_id="perspective_taking",
                skill_name="Perspective-Taking",
                category="empathy",
                description="Understanding and acknowledging different viewpoints in conflict",
                when_to_use=[
                    "When parties seem to misunderstand each other",
                    "When you feel stuck in your own viewpoint",
                    "When building empathy and connection",
                    "When looking for common ground"
                ],
                step_by_step_guide=[
                    "Set aside your own position temporarily",
                    "Ask genuine questions about their experience",
                    "Try to understand their underlying concerns",
                    "Reflect their perspective back to them",
                    "Acknowledge valid points in their viewpoint",
                    "Look for shared values or goals",
                    "Express understanding without necessarily agreeing"
                ],
                key_phrases=[
                    "I can see how from your perspective...",
                    "It makes sense that you would feel...",
                    "I hadn't considered that...",
                    "We both seem to want...",
                    "I can understand why that would be important to you"
                ],
                nonverbal_cues=[
                    "Curious, open facial expression",
                    "Leaning in to show interest",
                    "Nodding to show understanding",
                    "Relaxed, non-defensive posture",
                    "Appropriate eye contact"
                ],
                common_mistakes=[
                    "Pretending to understand when you don't",
                    "Only looking for flaws in their logic",
                    "Trying to change their perspective",
                    "Getting lost in their viewpoint and losing your own"
                ],
                troubleshooting_tips=[
                    "If you can't relate, focus on their emotions",
                    "If you disagree strongly, find smaller points to acknowledge",
                    "If they don't feel heard, reflect more before sharing your view",
                    "If you feel manipulated, maintain your boundaries"
                ],
                practice_scenarios=[
                    "Political disagreement with family member",
                    "Different parenting approaches with partner",
                    "Workplace conflict over priorities",
                    "Friend making choices you disagree with"
                ],
                difficulty_level=4
            ),
            
            ConflictResolutionSkill(
                skill_id="boundary_setting_conflict",
                skill_name="Boundary Setting in Conflict",
                category="boundaries",
                description="Establishing and maintaining limits during difficult conversations",
                when_to_use=[
                    "When conversations become abusive or disrespectful",
                    "When the same issues keep recurring",
                    "When your well-being is at risk",
                    "When someone violates your values"
                ],
                step_by_step_guide=[
                    "Identify what behavior is unacceptable to you",
                    "Communicate the boundary clearly and calmly",
                    "Explain the consequence if the boundary is crossed",
                    "Stay consistent in enforcing the boundary",
                    "Remove yourself if necessary",
                    "Don't negotiate on core boundaries",
                    "Follow through on stated consequences"
                ],
                key_phrases=[
                    "I'm not willing to continue this conversation if...",
                    "I need you to stop... or I will...",
                    "This isn't working for me, so I'm going to...",
                    "I won't accept... and if it continues...",
                    "I'm ending this conversation now"
                ],
                nonverbal_cues=[
                    "Firm, steady voice tone",
                    "Clear, direct eye contact",
                    "Confident body posture",
                    "Physical distancing if needed",
                    "Calm but serious facial expression"
                ],
                common_mistakes=[
                    "Setting boundaries you won't enforce",
                    "Over-explaining or justifying the boundary",
                    "Setting boundaries in anger",
                    "Being inconsistent in enforcement"
                ],
                troubleshooting_tips=[
                    "If they test the boundary, enforce it immediately",
                    "If you feel guilty, remind yourself of your worth",
                    "If they escalate, remove yourself from the situation",
                    "If boundaries aren't respected, consider the relationship"
                ],
                practice_scenarios=[
                    "Family member who uses guilt manipulation",
                    "Partner who raises their voice during arguments",
                    "Coworker who interrupts or dismisses you",
                    "Friend who consistently crosses personal boundaries"
                ],
                difficulty_level=4,
                prerequisites=["assertive_communication"]
            ),
            
            ConflictResolutionSkill(
                skill_id="mediation_facilitation",
                skill_name="Mediation and Facilitation",
                category="advanced",
                description="Helping others resolve conflicts as a neutral third party",
                when_to_use=[
                    "When asked to help resolve others' conflicts",
                    "When managing team or family disputes",
                    "When conflicts affect group dynamics",
                    "When parties are stuck and need help"
                ],
                step_by_step_guide=[
                    "Establish ground rules for the discussion",
                    "Ensure each party feels heard and understood",
                    "Keep focus on issues, not personalities",
                    "Help identify underlying interests and needs",
                    "Guide brainstorming of potential solutions",
                    "Help evaluate options objectively",
                    "Facilitate agreement and implementation planning"
                ],
                key_phrases=[
                    "Let's make sure everyone gets a chance to speak",
                    "What I'm hearing from both of you is...",
                    "What would need to happen for this to work?",
                    "Let's focus on the issue, not the person",
                    "What are some options we haven't considered?"
                ],
                nonverbal_cues=[
                    "Neutral, calm demeanor",
                    "Equal attention to all parties",
                    "Open, welcoming gestures",
                    "Positioning that shows neutrality",
                    "Confident but humble presence"
                ],
                common_mistakes=[
                    "Taking sides or showing favoritism",
                    "Imposing your own solutions",
                    "Letting discussions get off track",
                    "Not managing emotions effectively"
                ],
                troubleshooting_tips=[
                    "If parties attack each other, redirect to issues",
                    "If someone dominates, ensure equal speaking time",
                    "If emotions escalate, call for a break",
                    "If no progress, try different approaches"
                ],
                practice_scenarios=[
                    "Two coworkers fighting over project credit",
                    "Siblings arguing over parent care responsibilities",
                    "Team members with different work styles",
                    "Neighbors disputing property boundaries"
                ],
                difficulty_level=5,
                prerequisites=["active_listening_conflict", "perspective_taking", "collaborative_problem_solving"]
            )
        ]
    
    def create_conflict_situation(
        self,
        patient_id: str,
        description: str,
        conflict_type: ConflictType,
        severity: ConflictSeverity = ConflictSeverity.MODERATE
    ) -> str:
        
        conflict = ConflictSituation(
            patient_id=patient_id,
            description=description,
            conflict_type=conflict_type,
            severity=severity
        )
        
        self._save_conflict_situation(conflict)
        return conflict.conflict_id
    
    def _save_conflict_situation(self, conflict: ConflictSituation):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO conflict_situations (
                    conflict_id, patient_id, conflict_date, conflict_type,
                    severity, status, description, parties_involved,
                    relationship_context, underlying_issues, surface_issues,
                    triggers, personal_goals, other_party_goals, shared_interests,
                    emotions_experienced, physical_reactions, attempted_strategies,
                    what_worked, what_didnt_work, planned_approach, backup_strategies,
                    outcome, resolution_description, lessons_learned, follow_up_needed,
                    follow_up_plan, created_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                conflict.conflict_id, conflict.patient_id, conflict.conflict_date.isoformat(),
                conflict.conflict_type.value, conflict.severity.value, conflict.status.value,
                conflict.description, json.dumps(conflict.parties_involved),
                conflict.relationship_context, json.dumps(conflict.underlying_issues),
                json.dumps(conflict.surface_issues), json.dumps(conflict.triggers),
                json.dumps(conflict.personal_goals), json.dumps(conflict.other_party_goals),
                json.dumps(conflict.shared_interests), json.dumps(conflict.emotions_experienced),
                json.dumps(conflict.physical_reactions), json.dumps(conflict.attempted_strategies),
                json.dumps(conflict.what_worked), json.dumps(conflict.what_didnt_work),
                conflict.planned_approach, json.dumps(conflict.backup_strategies),
                conflict.outcome.value if conflict.outcome else None,
                conflict.resolution_description, json.dumps(conflict.lessons_learned),
                conflict.follow_up_needed, conflict.follow_up_plan,
                conflict.created_date.isoformat(), conflict.last_updated.isoformat()
            ))
            
            conn.commit()
    
    def update_conflict_outcome(
        self,
        conflict_id: str,
        outcome: ConflictOutcome,
        resolution_description: str,
        lessons_learned: List[str] = None,
        follow_up_needed: bool = False,
        follow_up_plan: str = ""
    ) -> bool:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE conflict_situations SET
                    status = ?,
                    outcome = ?,
                    resolution_description = ?,
                    lessons_learned = ?,
                    follow_up_needed = ?,
                    follow_up_plan = ?,
                    last_updated = ?
                WHERE conflict_id = ?
            """, (
                ConflictStatus.RESOLVED.value if outcome != ConflictOutcome.NO_RESOLUTION else ConflictStatus.UNRESOLVED.value,
                outcome.value, resolution_description,
                json.dumps(lessons_learned or []),
                follow_up_needed, follow_up_plan,
                datetime.now().isoformat(), conflict_id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def analyze_conflict(
        self,
        conflict_id: str,
        patient_id: str
    ) -> str:
        
        conflict = self.get_conflict_situation(conflict_id)
        if not conflict:
            return ""
        
        analysis = ConflictAnalysis(
            conflict_id=conflict_id,
            patient_id=patient_id
        )
        
        analysis.conflict_dynamics = self._analyze_conflict_dynamics(conflict)
        analysis.escalation_triggers = self._identify_escalation_triggers(conflict)
        analysis.de_escalation_opportunities = self._identify_deescalation_opportunities(conflict)
        analysis.recommended_strategies = self._recommend_strategies(conflict)
        analysis.risk_assessment = self._assess_risks(conflict)
        analysis.success_probability = self._estimate_success_probability(conflict)
        
        self._save_conflict_analysis(analysis)
        return analysis.analysis_id
    
    def _analyze_conflict_dynamics(self, conflict: ConflictSituation) -> Dict[str, str]:
        dynamics = {}
        
        if conflict.conflict_type == ConflictType.WORKPLACE:
            dynamics["power_dynamic"] = "hierarchical" if "boss" in conflict.relationship_context.lower() else "peer"
            dynamics["formality_level"] = "professional"
        elif conflict.conflict_type == ConflictType.FAMILY:
            dynamics["emotional_intensity"] = "high"
            dynamics["history_factor"] = "long-term relationship patterns"
        elif conflict.conflict_type == ConflictType.ROMANTIC:
            dynamics["intimacy_level"] = "high"
            dynamics["vulnerability_factor"] = "significant"
        
        if conflict.severity == ConflictSeverity.SEVERE:
            dynamics["urgency"] = "high"
            dynamics["intervention_needed"] = "professional help recommended"
        
        return dynamics
    
    def _identify_escalation_triggers(self, conflict: ConflictSituation) -> List[str]:
        triggers = list(conflict.triggers)
        
        common_triggers = [
            "Raised voices or yelling",
            "Personal attacks or name-calling",
            "Bringing up past grievances",
            "Threats or ultimatums",
            "Dismissive body language",
            "Interrupting or not listening",
            "Making assumptions about motives"
        ]
        
        conflict_specific = {
            ConflictType.WORKPLACE: ["Public embarrassment", "Going over someone's head", "Questioning competence"],
            ConflictType.FAMILY: ["Criticism of parenting", "Financial accusations", "Loyalty tests"],
            ConflictType.ROMANTIC: ["Jealousy accusations", "Comparison to exes", "Withholding affection"]
        }
        
        if conflict.conflict_type in conflict_specific:
            triggers.extend(conflict_specific[conflict.conflict_type])
        
        triggers.extend(common_triggers)
        return list(set(triggers))
    
    def _identify_deescalation_opportunities(self, conflict: ConflictSituation) -> List[str]:
        opportunities = [
            "Taking breaks when emotions get high",
            "Acknowledging valid points from the other side",
            "Using humor appropriately (if relationship allows)",
            "Finding something you both agree on",
            "Focusing on shared goals or values",
            "Speaking more softly and slowly",
            "Asking genuine questions about their perspective"
        ]
        
        if conflict.shared_interests:
            opportunities.append("Emphasizing shared interests: " + ", ".join(conflict.shared_interests))
        
        return opportunities
    
    def _recommend_strategies(self, conflict: ConflictSituation) -> List[str]:
        strategies = []
        
        if conflict.severity in [ConflictSeverity.MINOR, ConflictSeverity.MODERATE]:
            strategies.extend([
                "Direct communication using I-statements",
                "Active listening and perspective-taking",
                "Collaborative problem-solving"
            ])
        
        if conflict.severity in [ConflictSeverity.SIGNIFICANT, ConflictSeverity.MAJOR]:
            strategies.extend([
                "Structured mediation",
                "Professional counseling",
                "Formal conflict resolution process"
            ])
        
        if conflict.conflict_type == ConflictType.WORKPLACE:
            strategies.extend([
                "Document interactions professionally",
                "Involve HR or management if appropriate",
                "Focus on work impact and solutions"
            ])
        elif conflict.conflict_type == ConflictType.FAMILY:
            strategies.extend([
                "Family therapy or counseling",
                "Setting clear boundaries",
                "Focusing on future rather than past"
            ])
        
        return strategies
    
    def _assess_risks(self, conflict: ConflictSituation) -> List[str]:
        risks = []
        
        if conflict.severity == ConflictSeverity.SEVERE:
            risks.extend([
                "Relationship damage may be irreversible",
                "Emotional or psychological harm possible",
                "May require professional intervention"
            ])
        
        if "anger" in conflict.emotions_experienced and conflict.emotions_experienced["anger"] >= 8:
            risks.append("High anger levels increase risk of escalation")
        
        if conflict.conflict_type == ConflictType.WORKPLACE:
            risks.extend([
                "Potential impact on job security",
                "Possible HR involvement",
                "Team dynamics may be affected"
            ])
        
        if not conflict.what_worked and len(conflict.attempted_strategies) > 2:
            risks.append("Multiple failed attempts suggest need for different approach")
        
        return risks
    
    def _estimate_success_probability(self, conflict: ConflictSituation) -> int:
        base_probability = 5
        
        if conflict.shared_interests:
            base_probability += 2
        
        if conflict.what_worked:
            base_probability += 1
        
        if conflict.severity == ConflictSeverity.MINOR:
            base_probability += 2
        elif conflict.severity == ConflictSeverity.SEVERE:
            base_probability -= 2
        
        if len(conflict.attempted_strategies) > 3 and not conflict.what_worked:
            base_probability -= 1
        
        return max(1, min(10, base_probability))
    
    def _save_conflict_analysis(self, analysis: ConflictAnalysis):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO conflict_analyses (
                    analysis_id, conflict_id, patient_id, analysis_date,
                    conflict_dynamics, power_imbalances, communication_patterns,
                    escalation_triggers, de_escalation_opportunities,
                    personal_contribution, other_party_contribution,
                    systemic_factors, cultural_considerations,
                    recommended_strategies, strategies_to_avoid,
                    success_probability, risk_assessment, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                analysis.analysis_id, analysis.conflict_id, analysis.patient_id,
                analysis.analysis_date.isoformat(), json.dumps(analysis.conflict_dynamics),
                json.dumps(analysis.power_imbalances), json.dumps(analysis.communication_patterns),
                json.dumps(analysis.escalation_triggers), json.dumps(analysis.de_escalation_opportunities),
                json.dumps(analysis.personal_contribution), json.dumps(analysis.other_party_contribution),
                json.dumps(analysis.systemic_factors), json.dumps(analysis.cultural_considerations),
                json.dumps(analysis.recommended_strategies), json.dumps(analysis.strategies_to_avoid),
                analysis.success_probability, json.dumps(analysis.risk_assessment),
                analysis.created_date.isoformat()
            ))
            
            conn.commit()
    
    def create_resolution_plan(
        self,
        conflict_id: str,
        patient_id: str,
        primary_strategy: ResolutionStrategy = ResolutionStrategy.COLLABORATION
    ) -> str:
        
        conflict = self.get_conflict_situation(conflict_id)
        if not conflict:
            return ""
        
        plan = ConflictResolutionPlan(
            conflict_id=conflict_id,
            patient_id=patient_id,
            primary_strategy=primary_strategy
        )
        
        plan.preparation_steps = self._generate_preparation_steps(conflict, primary_strategy)
        plan.conversation_outline = self._create_conversation_outline(conflict, primary_strategy)
        plan.key_messages = self._identify_key_messages(conflict)
        plan.phrases_to_use = self._suggest_helpful_phrases(primary_strategy)
        plan.phrases_to_avoid = self._identify_harmful_phrases()
        plan.emotion_regulation_plan = self._create_emotion_regulation_plan(conflict)
        plan.if_things_go_wrong = self._create_contingency_plan(conflict)
        plan.success_criteria = self._define_success_criteria(conflict)
        
        self._save_resolution_plan(plan)
        return plan.plan_id
    
    def _generate_preparation_steps(self, conflict: ConflictSituation, strategy: ResolutionStrategy) -> List[str]:
        steps = [
            "Choose appropriate time and private location",
            "Review your goals and desired outcomes",
            "Practice emotional regulation techniques",
            "Prepare key points you want to communicate"
        ]
        
        if strategy == ResolutionStrategy.COLLABORATION:
            steps.extend([
                "Research potential win-win solutions",
                "Identify shared interests and values",
                "Prepare questions to understand their perspective"
            ])
        elif strategy == ResolutionStrategy.NEGOTIATION:
            steps.extend([
                "Determine your minimum acceptable outcome",
                "Identify areas where you can be flexible",
                "Prepare alternative proposals"
            ])
        
        steps.extend([
            "Plan for emotional regulation during conversation",
            "Identify your support system for after",
            "Set realistic expectations for the outcome"
        ])
        
        return steps
    
    def _create_conversation_outline(self, conflict: ConflictSituation, strategy: ResolutionStrategy) -> List[str]:
        outline = [
            "Opening: Set positive tone and purpose",
            "Share your perspective using I-statements",
            "Listen actively to their perspective",
            "Identify areas of agreement"
        ]
        
        if strategy == ResolutionStrategy.COLLABORATION:
            outline.extend([
                "Brainstorm solutions together",
                "Evaluate options based on both parties' needs",
                "Choose best solution and plan implementation"
            ])
        elif strategy == ResolutionStrategy.COMPROMISE:
            outline.extend([
                "Identify what each party is willing to give up",
                "Find middle ground solutions",
                "Negotiate specific terms"
            ])
        
        outline.extend([
            "Summarize agreements reached",
            "Plan follow-up and check-ins",
            "End on positive note"
        ])
        
        return outline
    
    def _identify_key_messages(self, conflict: ConflictSituation) -> List[str]:
        messages = []
        
        if conflict.personal_goals:
            messages.append("My main goal is: " + conflict.personal_goals[0])
        
        messages.extend([
            "I value our relationship and want to work this out",
            "I believe we can find a solution that works for both of us",
            "I'm committed to listening and understanding your perspective"
        ])
        
        if conflict.shared_interests:
            messages.append("We both want: " + conflict.shared_interests[0])
        
        return messages
    
    def _suggest_helpful_phrases(self, strategy: ResolutionStrategy) -> List[str]:
        common_phrases = [
            "I feel... when... because...",
            "Help me understand your perspective on this",
            "What would need to happen for this to work for both of us?",
            "I appreciate you taking the time to discuss this"
        ]
        
        strategy_specific = {
            ResolutionStrategy.COLLABORATION: [
                "Let's brainstorm some solutions together",
                "What if we both...?",
                "How can we make this a win-win?"
            ],
            ResolutionStrategy.COMPROMISE: [
                "What if we each gave a little on...?",
                "I'm willing to... if you're willing to...",
                "Let's find a middle ground"
            ],
            ResolutionStrategy.ACCOMMODATION: [
                "I understand this is important to you",
                "I'm willing to be flexible on this",
                "Your needs matter to me"
            ]
        }
        
        return common_phrases + strategy_specific.get(strategy, [])
    
    def _identify_harmful_phrases(self) -> List[str]:
        return [
            "You always..." or "You never...",
            "That's not my problem",
            "You're being ridiculous",
            "Calm down",
            "You're wrong",
            "I don't care",
            "Whatever",
            "Fine, have it your way",
            "You're just like...",
            "I told you so"
        ]
    
    def _create_emotion_regulation_plan(self, conflict: ConflictSituation) -> List[str]:
        plan = [
            "Take three deep breaths before starting",
            "Notice physical signs of tension and relax",
            "Use grounding techniques if feeling overwhelmed"
        ]
        
        if "anger" in conflict.emotions_experienced:
            plan.extend([
                "Count to 5 before responding to triggering statements",
                "Lower your voice if you notice it rising",
                "Take a break if anger becomes too intense"
            ])
        
        if "anxiety" in conflict.emotions_experienced:
            plan.extend([
                "Remind yourself that this conversation is important but not dangerous",
                "Focus on breathing slowly and steadily",
                "Use positive self-talk: 'I can handle this'"
            ])
        
        plan.extend([
            "Remember your goals for the conversation",
            "Stay focused on solutions, not blame",
            "Be willing to pause and resume later if needed"
        ])
        
        return plan
    
    def _create_contingency_plan(self, conflict: ConflictSituation) -> List[str]:
        return [
            "If they become hostile: Stay calm and don't match their energy",
            "If they refuse to talk: Respect their choice and suggest trying again later",
            "If you feel overwhelmed: Ask for a break to collect yourself",
            "If no progress is made: Suggest involving a neutral third party",
            "If they make threats: End the conversation and seek support",
            "If you lose your temper: Acknowledge it, apologize, and ask to start over",
            "If the relationship feels unsafe: Prioritize your safety and exit"
        ]
    
    def _define_success_criteria(self, conflict: ConflictSituation) -> List[str]:
        criteria = [
            "Both parties feel heard and understood",
            "Specific agreements are reached about future behavior",
            "The conversation ends respectfully"
        ]
        
        if conflict.personal_goals:
            criteria.append(f"Progress made toward: {conflict.personal_goals[0]}")
        
        criteria.extend([
            "Follow-up plans are established",
            "Both parties are willing to work on the relationship",
            "Emotional connection is maintained or improved"
        ])
        
        return criteria
    
    def _save_resolution_plan(self, plan: ConflictResolutionPlan):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO conflict_resolution_plans (
                    plan_id, conflict_id, patient_id, created_date,
                    primary_strategy, backup_strategies, preparation_steps,
                    conversation_outline, key_messages, phrases_to_use,
                    phrases_to_avoid, emotion_regulation_plan, if_things_go_wrong,
                    success_criteria, acceptable_outcomes, timeline,
                    follow_up_schedule, support_system, practice_needed,
                    executed, execution_notes, actual_outcome
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plan.plan_id, plan.conflict_id, plan.patient_id,
                plan.created_date.isoformat(), plan.primary_strategy.value,
                json.dumps([s.value for s in plan.backup_strategies]),
                json.dumps(plan.preparation_steps), json.dumps(plan.conversation_outline),
                json.dumps(plan.key_messages), json.dumps(plan.phrases_to_use),
                json.dumps(plan.phrases_to_avoid), json.dumps(plan.emotion_regulation_plan),
                json.dumps(plan.if_things_go_wrong), json.dumps(plan.success_criteria),
                json.dumps(plan.acceptable_outcomes), plan.timeline,
                json.dumps(plan.follow_up_schedule), json.dumps(plan.support_system),
                json.dumps(plan.practice_needed), plan.executed,
                plan.execution_notes, plan.actual_outcome
            ))
            
            conn.commit()
    
    def create_practice_session(
        self,
        patient_id: str,
        conflict_scenario: str,
        skills_to_practice: List[str] = None
    ) -> str:
        
        session = ConflictPracticeSession(
            patient_id=patient_id,
            conflict_scenario=conflict_scenario,
            skills_practiced=skills_to_practice or []
        )
        
        self._save_practice_session(session)
        return session.session_id
    
    def _save_practice_session(self, session: ConflictPracticeSession):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO conflict_practice_sessions (
                    session_id, patient_id, practice_date, duration_minutes,
                    conflict_scenario, skills_practiced, role_play_type,
                    pre_session_anxiety, post_session_anxiety, pre_session_confidence,
                    post_session_confidence, emotional_regulation_used,
                    communication_techniques_used, challenges_encountered,
                    breakthroughs_achieved, observer_feedback, self_reflection,
                    areas_for_improvement, next_practice_goals, homework_assigned,
                    overall_effectiveness, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id, session.patient_id, session.practice_date.isoformat(),
                session.duration_minutes, session.conflict_scenario,
                json.dumps(session.skills_practiced), session.role_play_type,
                session.pre_session_anxiety, session.post_session_anxiety,
                session.pre_session_confidence, session.post_session_confidence,
                json.dumps(session.emotional_regulation_used),
                json.dumps(session.communication_techniques_used),
                json.dumps(session.challenges_encountered),
                json.dumps(session.breakthroughs_achieved),
                session.observer_feedback, session.self_reflection,
                json.dumps(session.areas_for_improvement),
                json.dumps(session.next_practice_goals),
                json.dumps(session.homework_assigned),
                session.overall_effectiveness, session.created_date.isoformat()
            ))
            
            conn.commit()
    
    def update_practice_session_results(
        self,
        session_id: str,
        post_anxiety: int,
        post_confidence: int,
        challenges: List[str] = None,
        breakthroughs: List[str] = None,
        effectiveness: int = 5,
        self_reflection: str = "",
        observer_feedback: str = ""
    ) -> bool:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE conflict_practice_sessions SET
                    post_session_anxiety = ?,
                    post_session_confidence = ?,
                    challenges_encountered = ?,
                    breakthroughs_achieved = ?,
                    overall_effectiveness = ?,
                    self_reflection = ?,
                    observer_feedback = ?
                WHERE session_id = ?
            """, (
                post_anxiety, post_confidence,
                json.dumps(challenges or []),
                json.dumps(breakthroughs or []),
                effectiveness, self_reflection, observer_feedback,
                session_id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def get_conflict_situation(self, conflict_id: str) -> Optional[ConflictSituation]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM conflict_situations WHERE conflict_id = ?
            """, (conflict_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return ConflictSituation(
                conflict_id=row[0],
                patient_id=row[1],
                conflict_date=datetime.fromisoformat(row[2]),
                conflict_type=ConflictType(row[3]),
                severity=ConflictSeverity(row[4]),
                status=ConflictStatus(row[5]),
                description=row[6] or "",
                parties_involved=json.loads(row[7] or '[]'),
                relationship_context=row[8] or "",
                underlying_issues=json.loads(row[9] or '[]'),
                surface_issues=json.loads(row[10] or '[]'),
                triggers=json.loads(row[11] or '[]'),
                personal_goals=json.loads(row[12] or '[]'),
                other_party_goals=json.loads(row[13] or '[]'),
                shared_interests=json.loads(row[14] or '[]'),
                emotions_experienced=json.loads(row[15] or '{}'),
                physical_reactions=json.loads(row[16] or '[]'),
                attempted_strategies=json.loads(row[17] or '[]'),
                what_worked=json.loads(row[18] or '[]'),
                what_didnt_work=json.loads(row[19] or '[]'),
                planned_approach=row[20] or "",
                backup_strategies=json.loads(row[21] or '[]'),
                outcome=ConflictOutcome(row[22]) if row[22] else None,
                resolution_description=row[23] or "",
                lessons_learned=json.loads(row[24] or '[]'),
                follow_up_needed=bool(row[25]),
                follow_up_plan=row[26] or "",
                created_date=datetime.fromisoformat(row[27]),
                last_updated=datetime.fromisoformat(row[28])
            )
    
    def get_patient_conflicts(
        self,
        patient_id: str,
        status_filter: Optional[ConflictStatus] = None,
        days_back: int = 90
    ) -> List[ConflictSituation]:
        
        start_date = datetime.now() - timedelta(days=days_back)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT * FROM conflict_situations 
                WHERE patient_id = ? AND conflict_date >= ?
            """
            params = [patient_id, start_date.isoformat()]
            
            if status_filter:
                query += " AND status = ?"
                params.append(status_filter.value)
            
            query += " ORDER BY conflict_date DESC"
            
            cursor.execute(query, params)
            
            conflicts = []
            for row in cursor.fetchall():
                conflict = ConflictSituation(
                    conflict_id=row[0],
                    patient_id=row[1],
                    conflict_date=datetime.fromisoformat(row[2]),
                    conflict_type=ConflictType(row[3]),
                    severity=ConflictSeverity(row[4]),
                    status=ConflictStatus(row[5]),
                    description=row[6] or "",
                    parties_involved=json.loads(row[7] or '[]'),
                    relationship_context=row[8] or "",
                    underlying_issues=json.loads(row[9] or '[]'),
                    surface_issues=json.loads(row[10] or '[]'),
                    triggers=json.loads(row[11] or '[]'),
                    personal_goals=json.loads(row[12] or '[]'),
                    other_party_goals=json.loads(row[13] or '[]'),
                    shared_interests=json.loads(row[14] or '[]'),
                    emotions_experienced=json.loads(row[15] or '{}'),
                    physical_reactions=json.loads(row[16] or '[]'),
                    attempted_strategies=json.loads(row[17] or '[]'),
                    what_worked=json.loads(row[18] or '[]'),
                    what_didnt_work=json.loads(row[19] or '[]'),
                    planned_approach=row[20] or "",
                    backup_strategies=json.loads(row[21] or '[]'),
                    outcome=ConflictOutcome(row[22]) if row[22] else None,
                    resolution_description=row[23] or "",
                    lessons_learned=json.loads(row[24] or '[]'),
                    follow_up_needed=bool(row[25]),
                    follow_up_plan=row[26] or "",
                    created_date=datetime.fromisoformat(row[27]),
                    last_updated=datetime.fromisoformat(row[28])
                )
                conflicts.append(conflict)
            
            return conflicts
    
    def get_practice_history(
        self,
        patient_id: str,
        days_back: int = 30
    ) -> List[ConflictPracticeSession]:
        
        start_date = datetime.now() - timedelta(days=days_back)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM conflict_practice_sessions 
                WHERE patient_id = ? AND practice_date >= ?
                ORDER BY practice_date DESC
            """, (patient_id, start_date.isoformat()))
            
            sessions = []
            for row in cursor.fetchall():
                session = ConflictPracticeSession(
                    session_id=row[0],
                    patient_id=row[1],
                    practice_date=datetime.fromisoformat(row[2]),
                    duration_minutes=row[3] or 45,
                    conflict_scenario=row[4] or "",
                    skills_practiced=json.loads(row[5] or '[]'),
                    role_play_type=row[6] or "therapist_guided",
                    pre_session_anxiety=row[7] or 5,
                    post_session_anxiety=row[8] or 5,
                    pre_session_confidence=row[9] or 3,
                    post_session_confidence=row[10] or 3,
                    emotional_regulation_used=json.loads(row[11] or '[]'),
                    communication_techniques_used=json.loads(row[12] or '[]'),
                    challenges_encountered=json.loads(row[13] or '[]'),
                    breakthroughs_achieved=json.loads(row[14] or '[]'),
                    observer_feedback=row[15] or "",
                    self_reflection=row[16] or "",
                    areas_for_improvement=json.loads(row[17] or '[]'),
                    next_practice_goals=json.loads(row[18] or '[]'),
                    homework_assigned=json.loads(row[19] or '[]'),
                    overall_effectiveness=row[20] or 5,
                    created_date=datetime.fromisoformat(row[21])
                )
                sessions.append(session)
            
            return sessions
    
    def generate_progress_report(self, patient_id: str, days_back: int = 90) -> Dict[str, Any]:
        conflicts = self.get_patient_conflicts(patient_id, days_back=days_back)
        practice_sessions = self.get_practice_history(patient_id, days_back)
        
        if not conflicts and not practice_sessions:
            return {
                "patient_id": patient_id,
                "report_period_days": days_back,
                "message": "No conflict resolution data available for analysis"
            }
        
        # Conflict statistics
        total_conflicts = len(conflicts)
        resolved_conflicts = len([c for c in conflicts if c.status == ConflictStatus.RESOLVED])
        resolution_rate = resolved_conflicts / total_conflicts if total_conflicts > 0 else 0
        
        # Conflict types breakdown
        conflict_types = {}
        for conflict in conflicts:
            conflict_type = conflict.conflict_type.value
            conflict_types[conflict_type] = conflict_types.get(conflict_type, 0) + 1
        
        # Severity analysis
        severity_breakdown = {}
        for conflict in conflicts:
            severity = conflict.severity.value
            severity_breakdown[severity] = severity_breakdown.get(severity, 0) + 1
        
        # Outcomes analysis
        outcomes = {}
        for conflict in conflicts:
            if conflict.outcome:
                outcome = conflict.outcome.value
                outcomes[outcome] = outcomes.get(outcome, 0) + 1
        
        # Practice session analysis
        practice_summary = {
            "total_sessions": len(practice_sessions),
            "avg_effectiveness": 0,
            "confidence_improvement": 0,
            "anxiety_reduction": 0
        }
        
        if practice_sessions:
            effectiveness_scores = [s.overall_effectiveness for s in practice_sessions]
            practice_summary["avg_effectiveness"] = sum(effectiveness_scores) / len(effectiveness_scores)
            
            confidence_improvements = []
            anxiety_reductions = []
            
            for session in practice_sessions:
                if session.post_session_confidence and session.pre_session_confidence:
                    confidence_improvements.append(session.post_session_confidence - session.pre_session_confidence)
                if session.pre_session_anxiety and session.post_session_anxiety:
                    anxiety_reductions.append(session.pre_session_anxiety - session.post_session_anxiety)
            
            if confidence_improvements:
                practice_summary["confidence_improvement"] = sum(confidence_improvements) / len(confidence_improvements)
            if anxiety_reductions:
                practice_summary["anxiety_reduction"] = sum(anxiety_reductions) / len(anxiety_reductions)
        
        # Skills development analysis
        all_skills_practiced = []
        for session in practice_sessions:
            all_skills_practiced.extend(session.skills_practiced)
        
        skill_usage = {}
        for skill in all_skills_practiced:
            skill_usage[skill] = skill_usage.get(skill, 0) + 1
        
        most_practiced_skills = sorted(skill_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Recent trends
        recent_conflicts = [c for c in conflicts if (datetime.now() - c.conflict_date).days <= 30]
        recent_trend = "stable"
        
        if len(conflicts) >= 4:
            early_conflicts = [c for c in conflicts if (datetime.now() - c.conflict_date).days > 45]
            if len(recent_conflicts) < len(early_conflicts) * 0.7:
                recent_trend = "improving"
            elif len(recent_conflicts) > len(early_conflicts) * 1.3:
                recent_trend = "increasing"
        
        # Generate insights
        insights = self._generate_conflict_insights(conflicts, practice_sessions, resolution_rate)
        
        return {
            "patient_id": patient_id,
            "report_period_days": days_back,
            "conflict_summary": {
                "total_conflicts": total_conflicts,
                "resolved_conflicts": resolved_conflicts,
                "resolution_rate": round(resolution_rate, 2),
                "most_common_type": max(conflict_types, key=conflict_types.get) if conflict_types else None,
                "severity_breakdown": severity_breakdown
            },
            "outcomes_analysis": outcomes,
            "practice_summary": {
                "total_sessions": practice_summary["total_sessions"],
                "avg_effectiveness": round(practice_summary["avg_effectiveness"], 2),
                "avg_confidence_improvement": round(practice_summary["confidence_improvement"], 2),
                "avg_anxiety_reduction": round(practice_summary["anxiety_reduction"], 2)
            },
            "skill_development": {
                "most_practiced_skills": [{"skill": skill, "count": count} for skill, count in most_practiced_skills],
                "total_skills_practiced": len(set(all_skills_practiced))
            },
            "trends": {
                "recent_trend": recent_trend,
                "recent_conflicts_count": len(recent_conflicts)
            },
            "insights": insights,
            "recommendations": self._generate_conflict_recommendations(conflicts, practice_sessions, resolution_rate),
            "generated_date": datetime.now().isoformat()
        }
    
    def _generate_conflict_insights(
        self,
        conflicts: List[ConflictSituation],
        practice_sessions: List[ConflictPracticeSession],
        resolution_rate: float
    ) -> List[str]:
        
        insights = []
        
        if not conflicts and not practice_sessions:
            insights.append("Begin conflict resolution skill development with practice scenarios")
            return insights
        
        # Resolution rate insights
        if resolution_rate >= 0.8:
            insights.append("Excellent conflict resolution success rate - strong skills development")
        elif resolution_rate >= 0.6:
            insights.append("Good progress in conflict resolution - continue building skills")
        elif resolution_rate < 0.4:
            insights.append("Low resolution rate suggests need for additional skill development")
        
        # Practice insights
        if len(practice_sessions) >= 8:
            insights.append("Consistent practice shows strong commitment to skill development")
        elif len(practice_sessions) < 3:
            insights.append("Increase practice frequency to build confidence and competence")
        
        # Conflict pattern insights
        if conflicts:
            most_common_type = max(set(c.conflict_type for c in conflicts), 
                                 key=lambda x: sum(1 for c in conflicts if c.conflict_type == x))
            insights.append(f"Most frequent conflicts in {most_common_type.value} context - consider specialized skills")
        
        # Severity insights
        severe_conflicts = [c for c in conflicts if c.severity in [ConflictSeverity.MAJOR, ConflictSeverity.SEVERE]]
        if len(severe_conflicts) > len(conflicts) * 0.3:
            insights.append("High proportion of severe conflicts - consider professional support")
        
        # Effectiveness insights
        if practice_sessions:
            avg_effectiveness = sum(s.overall_effectiveness for s in practice_sessions) / len(practice_sessions)
            if avg_effectiveness >= 7:
                insights.append("High practice effectiveness indicates good skill acquisition")
            elif avg_effectiveness < 5:
                insights.append("Practice sessions showing limited effectiveness - review approach")
        
        return insights
    
    def _generate_conflict_recommendations(
        self,
        conflicts: List[ConflictSituation],
        practice_sessions: List[ConflictPracticeSession],
        resolution_rate: float
    ) -> List[str]:
        
        recommendations = []
        
        if not conflicts and not practice_sessions:
            recommendations.extend([
                "Start with conflict resolution assessment",
                "Begin practicing basic communication skills",
                "Learn emotional regulation techniques for conflicts"
            ])
            return recommendations
        
        # Resolution rate recommendations
        if resolution_rate < 0.5:
            recommendations.append("Focus on collaborative problem-solving and active listening skills")
        
        # Practice frequency recommendations
        if len(practice_sessions) < 1:
            recommendations.append("Begin regular practice sessions to build confidence")
        elif len(practice_sessions) < 4:
            recommendations.append("Increase practice frequency to at least weekly")
        
        # Skill-specific recommendations
        unresolved_conflicts = [c for c in conflicts if c.status != ConflictStatus.RESOLVED]
        if unresolved_conflicts:
            recommendations.append("Develop action plans for ongoing conflicts")
        
        # Severity-based recommendations
        severe_conflicts = [c for c in conflicts if c.severity == ConflictSeverity.SEVERE]
        if severe_conflicts:
            recommendations.append("Consider professional mediation for severe conflicts")
        
        # Type-specific recommendations
        if conflicts:
            conflict_types = [c.conflict_type for c in conflicts]
            most_common = max(set(conflict_types), key=conflict_types.count)
            
            if most_common == ConflictType.WORKPLACE:
                recommendations.append("Focus on professional communication and HR policies")
            elif most_common == ConflictType.FAMILY:
                recommendations.append("Consider family therapy or specialized family conflict skills")
            elif most_common == ConflictType.ROMANTIC:
                recommendations.append("Develop couple communication and intimacy conflict skills")
        
        # Follow-up recommendations
        needs_followup = [c for c in conflicts if c.follow_up_needed and c.status == ConflictStatus.RESOLVED]
        if needs_followup:
            recommendations.append("Schedule follow-up sessions for resolved conflicts")
        
        return recommendations
    
    def get_conflict_resolution_homework(
        self,
        patient_id: str,
        skill_focus: str = "general",
        difficulty_level: int = 3
    ) -> Dict[str, Any]:
        
        homework_templates = {
            "active_listening": {
                1: {
                    "daily_practice": "Practice reflective listening for 10 minutes daily with family/friends",
                    "observation": "Notice and record when you interrupt others vs. when you listen fully",
                    "self_reflection": "Journal about what makes listening difficult for you"
                },
                3: {
                    "real_world_application": "Use active listening in one conflict discussion this week",
                    "skill_integration": "Combine listening with empathy and perspective-taking",
                    "challenge": "Practice listening during emotionally charged conversations"
                },
                5: {
                    "advanced_practice": "Facilitate a conflict discussion between two others",
                    "teaching": "Teach active listening skills to someone else",
                    "mastery": "Use listening skills in high-stakes or professional conflicts"
                }
            },
            "emotional_regulation": {
                1: {
                    "daily_practice": "Practice deep breathing or counting before responding in conflicts",
                    "awareness": "Identify your physical signs of escalating emotions",
                    "basic_skills": "Use grounding techniques when feeling triggered"
                },
                3: {
                    "real_world_application": "Apply emotion regulation during one difficult conversation",
                    "skill_development": "Try different regulation techniques and note what works",
                    "challenge": "Stay regulated while discussing triggering topics"
                },
                5: {
                    "advanced_practice": "Maintain emotional regulation while helping others de-escalate",
                    "complex_situations": "Practice regulation in multi-party conflicts",
                    "mastery": "Model emotional regulation for others in heated situations"
                }
            },
            "general": {
                1: {
                    "skill_building": "Practice one conflict resolution skill daily",
                    "awareness": "Notice conflict patterns in your relationships",
                    "preparation": "Identify one conflict you'd like to address"
                },
                3: {
                    "real_world_practice": "Apply conflict resolution skills to current situation",
                    "skill_integration": "Combine multiple skills in practice scenarios",
                    "reflection": "Analyze what worked and what didn't in recent conflicts"
                },
                5: {
                    "leadership": "Help others resolve their conflicts",
                    "complex_situations": "Handle multi-party or complex organizational conflicts",
                    "mastery": "Develop your own conflict resolution innovations"
                }
            }
        }
        
        selected_homework = homework_templates.get(skill_focus, homework_templates["general"])
        level_homework = selected_homework.get(difficulty_level, selected_homework[3])
        
        return {
            "skill_focus": skill_focus,
            "difficulty_level": difficulty_level,
            "week_assignments": level_homework,
            "practice_scenarios": [
                "Disagreement with family member about holiday plans",
                "Workplace conflict over project responsibilities",
                "Friend conflict about cancelled plans",
                "Neighbor dispute about noise or boundaries",
                "Romantic partner disagreement about finances"
            ][:difficulty_level],
            "reflection_questions": [
                "What emotions did you experience during the conflict?",
                "Which skills felt most natural to use?",
                "What would you do differently next time?",
                "How did the other person respond to your approach?",
                "What did you learn about yourself or the relationship?"
            ],
            "success_metrics": [
                f"Use {skill_focus} skills {difficulty_level} times this week",
                "Complete daily reflection journal",
                "Identify one insight about your conflict patterns",
                "Practice emotional regulation during difficult moments"
            ]
        }
    
    def export_conflict_data(self, patient_id: str) -> Dict[str, Any]:
        conflicts = self.get_patient_conflicts(patient_id, days_back=365)
        practice_sessions = self.get_practice_history(patient_id, days_back=365)
        
        export_data = {
            "patient_id": patient_id,
            "export_date": datetime.now().isoformat(),
            "conflict_situations": [
                {
                    "conflict_date": conflict.conflict_date.isoformat(),
                    "conflict_type": conflict.conflict_type.value,
                    "severity": conflict.severity.value,
                    "status": conflict.status.value,
                    "description": conflict.description,
                    "parties_involved": conflict.parties_involved,
                    "outcome": conflict.outcome.value if conflict.outcome else None,
                    "resolution_description": conflict.resolution_description,
                    "lessons_learned": conflict.lessons_learned,
                    "what_worked": conflict.what_worked,
                    "what_didnt_work": conflict.what_didnt_work
                }
                for conflict in conflicts
            ],
            "practice_sessions": [
                {
                    "practice_date": session.practice_date.isoformat(),
                    "conflict_scenario": session.conflict_scenario,
                    "skills_practiced": session.skills_practiced,
                    "confidence_improvement": (session.post_session_confidence - session.pre_session_confidence) if session.post_session_confidence and session.pre_session_confidence else None,
                    "anxiety_reduction": (session.pre_session_anxiety - session.post_session_anxiety) if session.pre_session_anxiety and session.post_session_anxiety else None,
                    "overall_effectiveness": session.overall_effectiveness,
                    "breakthroughs_achieved": session.breakthroughs_achieved,
                    "areas_for_improvement": session.areas_for_improvement
                }
                for session in practice_sessions
            ],
            "summary_statistics": {
                "total_conflicts": len(conflicts),
                "resolved_conflicts": len([c for c in conflicts if c.status == ConflictStatus.RESOLVED]),
                "total_practice_sessions": len(practice_sessions),
                "avg_practice_effectiveness": sum(s.overall_effectiveness for s in practice_sessions) / len(practice_sessions) if practice_sessions else 0,
                "most_common_conflict_type": max(set(c.conflict_type.value for c in conflicts), key=lambda x: sum(1 for c in conflicts if c.conflict_type.value == x)) if conflicts else None
            }
        }
        
        return export_data


def get_conflict_resolution_tips(conflict_type: ConflictType) -> List[str]:
    tips_by_type = {
        ConflictType.WORKPLACE: [
            "Keep discussions professional and focused on work impact",
            "Document important conversations and agreements",
            "Involve HR or management when appropriate",
            "Focus on solutions rather than blame",
            "Respect organizational hierarchy and policies"
        ],
        ConflictType.FAMILY: [
            "Remember that relationships are long-term",
            "Address issues privately before involving others",
            "Focus on specific behaviors rather than character",
            "Be willing to apologize and forgive",
            "Consider family therapy for ongoing issues"
        ],
        ConflictType.ROMANTIC: [
            "Choose the right time and place for difficult conversations",
            "Use 'I' statements to express feelings",
            "Listen to understand, not to be right",
            "Take breaks when emotions get too high",
            "Focus on strengthening the relationship, not winning"
        ],
        ConflictType.FRIENDSHIP: [
            "Be honest about your feelings and needs",
            "Give friends the benefit of the doubt",
            "Be willing to compromise and find middle ground",
            "Address issues directly rather than avoiding them",
            "Know when a friendship may need space or boundaries"
        ]
    }
    
    return tips_by_type.get(conflict_type, [
        "Stay calm and respectful throughout",
        "Focus on specific behaviors and impacts",
        "Look for common ground and shared interests",
        "Be willing to see the other person's perspective",
        "Work toward mutually beneficial solutions"
    ])


if __name__ == "__main__":
    conflict_system = ConflictResolutionSystem()
    
    patient_id = "test_patient_001"
    
    # Create a conflict situation
    conflict_id = conflict_system.create_conflict_situation(
        patient_id=patient_id,
        description="Ongoing disagreement with coworker about project deadlines and responsibilities",
        conflict_type=ConflictType.WORKPLACE,
        severity=ConflictSeverity.MODERATE
    )
    
    # Analyze the conflict
    analysis_id = conflict_system.analyze_conflict(conflict_id, patient_id)
    
    # Create resolution plan
    plan_id = conflict_system.create_resolution_plan(
        conflict_id=conflict_id,
        patient_id=patient_id,
        primary_strategy=ResolutionStrategy.COLLABORATION
    )
    
    # Practice session
    practice_id = conflict_system.create_practice_session(
        patient_id=patient_id,
        conflict_scenario="Role-play workplace disagreement about project priorities",
        skills_to_practice=["active_listening_conflict", "collaborative_problem_solving"]
    )
    
    # Update practice results
    conflict_system.update_practice_session_results(
        session_id=practice_id,
        post_anxiety=3,
        post_confidence=7,
        challenges=["Felt defensive when criticized", "Hard to stay focused on solutions"],
        breakthroughs=["Successfully used I-statements", "Found common ground on project goals"],
        effectiveness=8,
        self_reflection="Much more confident about handling the real conversation now",
        observer_feedback="Great improvement in staying calm and collaborative"
    )
    
    # Update conflict outcome
    conflict_system.update_conflict_outcome(
        conflict_id=conflict_id,
        outcome=ConflictOutcome.WIN_WIN,
        resolution_description="Reached agreement on clearer roles and regular check-ins",
        lessons_learned=["Preparation and practice really helped", "Coworker was more reasonable than expected"],
        follow_up_needed=True,
        follow_up_plan="Check in after two weeks to ensure new system is working"
    )
    
    # Generate progress report
    progress_report = conflict_system.generate_progress_report(patient_id, 90)
    
    # Get homework assignment
    homework = conflict_system.get_conflict_resolution_homework(
        patient_id=patient_id,
        skill_focus="active_listening",
        difficulty_level=3
    )
    
    print(f"Conflict situation created: {conflict_id}")
    print(f"Analysis completed: {analysis_id}")
    print(f"Resolution plan created: {plan_id}")
    print(f"Practice session completed: {practice_id}")
    print(f"Progress report shows {progress_report['conflict_summary']['total_conflicts']} conflicts tracked")
    print(f"Homework assigned for {homework['skill_focus']} at level {homework['difficulty_level']}")
    
    # Get tips for specific conflict type
    workplace_tips = get_conflict_resolution_tips(ConflictType.WORKPLACE)
    print(f"Generated {len(workplace_tips)} workplace conflict resolution tips")
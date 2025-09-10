from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import sqlite3
import json


class SkillCategory(Enum):
    COGNITIVE = "cognitive"
    BEHAVIORAL = "behavioral"
    EMOTIONAL_REGULATION = "emotional_regulation"
    INTERPERSONAL = "interpersonal"
    MINDFULNESS = "mindfulness"
    DISTRESS_TOLERANCE = "distress_tolerance"
    COMMUNICATION = "communication"
    PROBLEM_SOLVING = "problem_solving"
    COPING = "coping"
    RELAXATION = "relaxation"


class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    MASTERY = "mastery"


class PracticeFormat(Enum):
    GUIDED_PRACTICE = "guided_practice"
    ROLE_PLAY = "role_play"
    SIMULATION = "simulation"
    BEHAVIORAL_REHEARSAL = "behavioral_rehearsal"
    COGNITIVE_EXERCISE = "cognitive_exercise"
    MINDFULNESS_PRACTICE = "mindfulness_practice"
    EXPOSURE_EXERCISE = "exposure_exercise"
    SKILLS_TRAINING = "skills_training"


class MasteryLevel(Enum):
    NOT_DEMONSTRATED = "not_demonstrated"
    EMERGING = "emerging"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class TherapeuticSkill:
    skill_id: str
    name: str
    category: SkillCategory
    description: str
    learning_objectives: List[str]
    prerequisites: List[str]
    difficulty_level: SkillLevel
    estimated_practice_time: int
    practice_formats: List[PracticeFormat]
    assessment_criteria: List[str]
    common_challenges: List[str]
    coaching_tips: List[str]
    generalization_targets: List[str]
    evidence_base: str


@dataclass
class SkillPracticeSession:
    practice_id: str
    session_id: str
    patient_id: str
    skill_id: str
    practice_format: PracticeFormat
    duration_minutes: int
    practice_scenario: str
    coaching_provided: List[str]
    patient_performance: Dict[str, Any]
    mastery_demonstration: MasteryLevel
    challenges_encountered: List[str]
    breakthrough_moments: List[str]
    feedback_given: str
    patient_self_assessment: str
    homework_connection: str
    next_practice_steps: List[str]
    practice_date: datetime = field(default_factory=datetime.now)


@dataclass
class SkillAssessment:
    assessment_id: str
    patient_id: str
    skill_id: str
    assessment_date: datetime
    mastery_level: MasteryLevel
    competency_indicators: List[str]
    areas_for_improvement: List[str]
    practice_recommendations: List[str]
    generalization_evidence: List[str]
    confidence_rating: int
    frequency_of_use: str
    effectiveness_rating: int


@dataclass
class SkillProgression:
    patient_id: str
    skill_id: str
    baseline_level: MasteryLevel
    current_level: MasteryLevel
    practice_sessions_completed: int
    total_practice_time: int
    mastery_milestones: List[Dict[str, Any]]
    progression_rate: str
    projected_mastery_date: Optional[datetime]
    learning_curve_data: List[Dict[str, Any]]


class SkillPracticeSystem:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.skill_library = self._initialize_skill_library()
        self.practice_protocols = self._initialize_practice_protocols()
        self.assessment_rubrics = self._initialize_assessment_rubrics()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS therapeutic_skills (
                    skill_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    learning_objectives TEXT,
                    prerequisites TEXT,
                    difficulty_level TEXT,
                    estimated_practice_time INTEGER,
                    practice_formats TEXT,
                    assessment_criteria TEXT,
                    common_challenges TEXT,
                    coaching_tips TEXT,
                    generalization_targets TEXT,
                    evidence_base TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skill_practice_sessions (
                    practice_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    patient_id TEXT NOT NULL,
                    skill_id TEXT NOT NULL,
                    practice_format TEXT,
                    duration_minutes INTEGER,
                    practice_scenario TEXT,
                    coaching_provided TEXT,
                    patient_performance TEXT,
                    mastery_demonstration TEXT,
                    challenges_encountered TEXT,
                    breakthrough_moments TEXT,
                    feedback_given TEXT,
                    patient_self_assessment TEXT,
                    homework_connection TEXT,
                    next_practice_steps TEXT,
                    practice_date TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skill_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    skill_id TEXT NOT NULL,
                    assessment_date TEXT,
                    mastery_level TEXT,
                    competency_indicators TEXT,
                    areas_for_improvement TEXT,
                    practice_recommendations TEXT,
                    generalization_evidence TEXT,
                    confidence_rating INTEGER,
                    frequency_of_use TEXT,
                    effectiveness_rating INTEGER
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skill_progressions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    skill_id TEXT NOT NULL,
                    baseline_level TEXT,
                    current_level TEXT,
                    practice_sessions_completed INTEGER,
                    total_practice_time INTEGER,
                    mastery_milestones TEXT,
                    progression_rate TEXT,
                    projected_mastery_date TEXT,
                    learning_curve_data TEXT,
                    last_updated TEXT
                )
            """)
    
    def _initialize_skill_library(self) -> Dict[str, TherapeuticSkill]:
        
        skills = {}
        
        skills["cognitive_restructuring"] = TherapeuticSkill(
            skill_id="cognitive_restructuring",
            name="Cognitive Restructuring",
            category=SkillCategory.COGNITIVE,
            description="Ability to identify, examine, and modify negative automatic thoughts",
            learning_objectives=[
                "Identify automatic thoughts in real-time",
                "Examine evidence for and against thoughts",
                "Generate balanced alternative thoughts",
                "Apply cognitive restructuring independently"
            ],
            prerequisites=["thought_awareness", "emotion_identification"],
            difficulty_level=SkillLevel.INTERMEDIATE,
            estimated_practice_time=30,
            practice_formats=[PracticeFormat.GUIDED_PRACTICE, PracticeFormat.COGNITIVE_EXERCISE, PracticeFormat.ROLE_PLAY],
            assessment_criteria=[
                "Accurately identifies automatic thoughts",
                "Systematically examines evidence",
                "Generates realistic alternative thoughts",
                "Reports improved emotional response"
            ],
            common_challenges=[
                "Difficulty catching thoughts in the moment",
                "Resistance to questioning familiar thoughts",
                "Generating overly positive alternatives",
                "Emotional intensity interfering with process"
            ],
            coaching_tips=[
                "Start with written exercises before in-the-moment practice",
                "Use specific recent examples from patient's life",
                "Validate emotions while challenging thoughts",
                "Practice with low-intensity situations first"
            ],
            generalization_targets=[
                "Work situations", "Relationship conflicts", "Social anxiety", "Daily stressors"
            ],
            evidence_base="Extensive research support in CBT literature"
        )
        
        skills["mindfulness_meditation"] = TherapeuticSkill(
            skill_id="mindfulness_meditation",
            name="Mindfulness Meditation",
            category=SkillCategory.MINDFULNESS,
            description="Practice of present-moment awareness without judgment",
            learning_objectives=[
                "Maintain focused attention on chosen object",
                "Notice when mind wanders without judgment",
                "Return attention to present moment",
                "Observe thoughts and emotions without attachment"
            ],
            prerequisites=["basic_breathing_awareness"],
            difficulty_level=SkillLevel.BEGINNER,
            estimated_practice_time=20,
            practice_formats=[PracticeFormat.GUIDED_PRACTICE, PracticeFormat.MINDFULNESS_PRACTICE],
            assessment_criteria=[
                "Maintains attention for target duration",
                "Demonstrates non-judgmental awareness",
                "Successfully returns from mind-wandering",
                "Reports increased present-moment awareness"
            ],
            common_challenges=[
                "Frequent mind wandering",
                "Judging thoughts as good or bad",
                "Expecting immediate results",
                "Physical discomfort during practice"
            ],
            coaching_tips=[
                "Normalize mind wandering as part of practice",
                "Start with very brief sessions (2-3 minutes)",
                "Use guided meditations initially",
                "Focus on process rather than outcomes"
            ],
            generalization_targets=[
                "Daily activities", "Stressful situations", "Emotional regulation", "Sleep preparation"
            ],
            evidence_base="Strong research support for anxiety, depression, and stress reduction"
        )
        
        skills["assertive_communication"] = TherapeuticSkill(
            skill_id="assertive_communication",
            name="Assertive Communication",
            category=SkillCategory.INTERPERSONAL,
            description="Clear, honest communication while respecting others' rights",
            learning_objectives=[
                "Express needs and feelings directly",
                "Set appropriate boundaries",
                "Say no without guilt or aggression",
                "Request behavior changes constructively"
            ],
            prerequisites=["emotion_identification", "basic_communication_skills"],
            difficulty_level=SkillLevel.INTERMEDIATE,
            estimated_practice_time=25,
            practice_formats=[PracticeFormat.ROLE_PLAY, PracticeFormat.BEHAVIORAL_REHEARSAL, PracticeFormat.SIMULATION],
            assessment_criteria=[
                "Uses 'I' statements effectively",
                "Maintains appropriate tone and body language",
                "States requests clearly and specifically",
                "Respects others' responses and boundaries"
            ],
            common_challenges=[
                "Fear of conflict or rejection",
                "Confusing assertiveness with aggression",
                "Guilt about expressing needs",
                "Difficulty with timing of communications"
            ],
            coaching_tips=[
                "Practice with low-stakes situations first",
                "Rehearse specific phrases and responses",
                "Address underlying beliefs about worthiness",
                "Use graduated exposure to assertiveness"
            ],
            generalization_targets=[
                "Workplace interactions", "Family relationships", "Friendships", "Service situations"
            ],
            evidence_base="Well-established in interpersonal effectiveness research"
        )
        
        skills["progressive_muscle_relaxation"] = TherapeuticSkill(
            skill_id="progressive_muscle_relaxation",
            name="Progressive Muscle Relaxation",
            category=SkillCategory.RELAXATION,
            description="Systematic tensing and relaxing of muscle groups to reduce physical tension",
            learning_objectives=[
                "Identify areas of physical tension",
                "Practice tension-relaxation sequence",
                "Achieve deep muscle relaxation",
                "Use technique for stress management"
            ],
            prerequisites=["body_awareness"],
            difficulty_level=SkillLevel.BEGINNER,
            estimated_practice_time=20,
            practice_formats=[PracticeFormat.GUIDED_PRACTICE, PracticeFormat.SKILLS_TRAINING],
            assessment_criteria=[
                "Correctly performs tension-relaxation sequence",
                "Reports significant reduction in muscle tension",
                "Can complete technique independently",
                "Uses skill effectively for stress relief"
            ],
            common_challenges=[
                "Difficulty detecting muscle tension",
                "Creating too much tension during practice",
                "Impatience with gradual process",
                "Physical limitations affecting participation"
            ],
            coaching_tips=[
                "Start with shorter versions focusing on key muscle groups",
                "Use gentle tension if patient has physical limitations",
                "Practice regularly to build body awareness",
                "Combine with breathing techniques for enhanced effect"
            ],
            generalization_targets=[
                "Pre-sleep routine", "Work stress", "Anxiety management", "Pain management"
            ],
            evidence_base="Extensive research for anxiety and stress disorders"
        )
        
        skills["emotional_regulation"] = TherapeuticSkill(
            skill_id="emotional_regulation",
            name="Emotional Regulation",
            category=SkillCategory.EMOTIONAL_REGULATION,
            description="Skills to manage emotional intensity and duration effectively",
            learning_objectives=[
                "Identify emotions and their triggers",
                "Use strategies to modulate emotional intensity",
                "Tolerate distressing emotions without escape",
                "Express emotions appropriately"
            ],
            prerequisites=["emotion_identification", "distress_tolerance_basics"],
            difficulty_level=SkillLevel.ADVANCED,
            estimated_practice_time=35,
            practice_formats=[PracticeFormat.GUIDED_PRACTICE, PracticeFormat.SIMULATION, PracticeFormat.SKILLS_TRAINING],
            assessment_criteria=[
                "Accurately identifies emotional triggers",
                "Effectively uses regulation strategies",
                "Demonstrates improved emotional stability",
                "Maintains functioning during emotional distress"
            ],
            common_challenges=[
                "Overwhelming emotional intensity",
                "Resistance to experiencing difficult emotions",
                "Habitual avoidance patterns",
                "Limited strategy repertoire"
            ],
            coaching_tips=[
                "Build distress tolerance before regulation skills",
                "Practice with mild emotions before intense ones",
                "Validate emotional experiences throughout",
                "Develop personalized regulation toolkit"
            ],
            generalization_targets=[
                "Relationship conflicts", "Work stress", "Trauma triggers", "Daily frustrations"
            ],
            evidence_base="Core component of DBT with strong empirical support"
        )
        
        skills["problem_solving"] = TherapeuticSkill(
            skill_id="problem_solving",
            name="Systematic Problem Solving",
            category=SkillCategory.PROBLEM_SOLVING,
            description="Structured approach to identifying and resolving life problems",
            learning_objectives=[
                "Define problems clearly and specifically",
                "Generate multiple solution options",
                "Evaluate pros and cons of solutions",
                "Implement and evaluate chosen solutions"
            ],
            prerequisites=["cognitive_flexibility"],
            difficulty_level=SkillLevel.INTERMEDIATE,
            estimated_practice_time=30,
            practice_formats=[PracticeFormat.GUIDED_PRACTICE, PracticeFormat.COGNITIVE_EXERCISE, PracticeFormat.SIMULATION],
            assessment_criteria=[
                "Breaks complex problems into manageable parts",
                "Generates diverse solution options",
                "Systematically evaluates alternatives",
                "Follows through with implementation plans"
            ],
            common_challenges=[
                "Overwhelming problems leading to avoidance",
                "Premature closure on first solution",
                "Perfectionism interfering with action",
                "Emotional reactions blocking logical thinking"
            ],
            coaching_tips=[
                "Start with smaller, less emotionally charged problems",
                "Use structured worksheets to guide process",
                "Address emotional barriers to problem-solving",
                "Celebrate partial solutions and progress"
            ],
            generalization_targets=[
                "Work challenges", "Relationship issues", "Financial problems", "Health concerns"
            ],
            evidence_base="Well-established in cognitive-behavioral interventions"
        )
        
        return skills
    
    def _initialize_practice_protocols(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "guided_practice_protocol": {
                "structure": [
                    "Skill explanation and rationale (5 min)",
                    "Demonstration by therapist (5 min)",
                    "Patient practice with coaching (15 min)",
                    "Feedback and refinement (5 min)"
                ],
                "coaching_elements": [
                    "Real-time guidance",
                    "Error correction",
                    "Encouragement and validation",
                    "Skill modification for individual needs"
                ],
                "success_indicators": [
                    "Patient demonstrates understanding",
                    "Skill performance improves during session",
                    "Patient reports increased confidence",
                    "Clear homework application identified"
                ]
            },
            
            "role_play_protocol": {
                "structure": [
                    "Scenario development (5 min)",
                    "Role assignment and preparation (5 min)",
                    "Role play execution (10 min)",
                    "Debrief and skill analysis (10 min)"
                ],
                "scenario_elements": [
                    "Realistic and relevant to patient",
                    "Appropriate difficulty level",
                    "Clear skill application opportunities",
                    "Safe emotional intensity"
                ],
                "debrief_focus": [
                    "What worked well",
                    "Areas for improvement",
                    "Alternative approaches",
                    "Real-world application"
                ]
            },
            
            "behavioral_rehearsal_protocol": {
                "structure": [
                    "Target behavior identification (5 min)",
                    "Behavioral breakdown (5 min)",
                    "Practice trials (15 min)",
                    "Performance feedback (5 min)"
                ],
                "practice_elements": [
                    "Multiple repetition trials",
                    "Gradual complexity increase",
                    "Environmental variation",
                    "Self-monitoring training"
                ],
                "feedback_components": [
                    "Specific behavior observations",
                    "Strength acknowledgment",
                    "Improvement suggestions",
                    "Next steps planning"
                ]
            }
        }
    
    def _initialize_assessment_rubrics(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "mastery_levels": {
                MasteryLevel.NOT_DEMONSTRATED: {
                    "description": "No evidence of skill understanding or application",
                    "indicators": ["Cannot explain skill", "No behavioral demonstration", "No recognition of skill relevance"]
                },
                MasteryLevel.EMERGING: {
                    "description": "Basic understanding with minimal application",
                    "indicators": ["Can explain skill concept", "Requires extensive guidance", "Limited behavioral demonstration"]
                },
                MasteryLevel.DEVELOPING: {
                    "description": "Developing competency with some independence",
                    "indicators": ["Demonstrates skill with coaching", "Shows improvement over time", "Beginning independent use"]
                },
                MasteryLevel.PROFICIENT: {
                    "description": "Consistent independent skill application",
                    "indicators": ["Uses skill without prompting", "Adapts skill to situations", "Reports beneficial outcomes"]
                },
                MasteryLevel.ADVANCED: {
                    "description": "Sophisticated skill application and adaptation",
                    "indicators": ["Modifies skill for complex situations", "Teaches skill to others", "Integrates with other skills"]
                },
                MasteryLevel.EXPERT: {
                    "description": "Masterful skill application across all contexts",
                    "indicators": ["Intuitive skill application", "Creates variations", "Maintains effectiveness under stress"]
                }
            },
            
            "assessment_domains": {
                "understanding": ["Can explain skill rationale", "Identifies when to use skill", "Recognizes skill components"],
                "application": ["Demonstrates skill accurately", "Uses skill in appropriate situations", "Adapts skill to context"],
                "generalization": ["Transfers skill to new situations", "Combines with other skills", "Maintains skill over time"],
                "effectiveness": ["Achieves desired outcomes", "Reports subjective benefit", "Shows measurable improvement"]
            }
        }
    
    def conduct_skill_practice(self, session_id: str, patient_id: str, skill_id: str,
                             practice_format: PracticeFormat, scenario: str = "") -> SkillPracticeSession:
        
        practice_id = f"{patient_id}_{skill_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        skill = self.skill_library.get(skill_id)
        if not skill:
            raise ValueError(f"Skill {skill_id} not found in library")
        
        protocol = self.practice_protocols.get(f"{practice_format.value}_protocol", 
                                             self.practice_protocols["guided_practice_protocol"])
        
        practice_session = SkillPracticeSession(
            practice_id=practice_id,
            session_id=session_id,
            patient_id=patient_id,
            skill_id=skill_id,
            practice_format=practice_format,
            duration_minutes=skill.estimated_practice_time,
            practice_scenario=scenario or f"General practice of {skill.name}",
            coaching_provided=[],
            patient_performance={},
            mastery_demonstration=MasteryLevel.NOT_DEMONSTRATED,
            challenges_encountered=[],
            breakthrough_moments=[],
            feedback_given="",
            patient_self_assessment="",
            homework_connection="",
            next_practice_steps=[]
        )
        
        self._save_skill_practice_session(practice_session)
        return practice_session
    
    def assess_skill_mastery(self, patient_id: str, skill_id: str, 
                           performance_data: Dict[str, Any]) -> SkillAssessment:
        
        assessment_id = f"{patient_id}_{skill_id}_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        skill = self.skill_library.get(skill_id)
        if not skill:
            raise ValueError(f"Skill {skill_id} not found in library")
        
        mastery_level = self._determine_mastery_level(performance_data, skill)
        competency_indicators = self._identify_competency_indicators(performance_data, skill)
        areas_for_improvement = self._identify_improvement_areas(performance_data, skill)
        practice_recommendations = self._generate_practice_recommendations(mastery_level, skill)
        
        assessment = SkillAssessment(
            assessment_id=assessment_id,
            patient_id=patient_id,
            skill_id=skill_id,
            assessment_date=datetime.now(),
            mastery_level=mastery_level,
            competency_indicators=competency_indicators,
            areas_for_improvement=areas_for_improvement,
            practice_recommendations=practice_recommendations,
            generalization_evidence=performance_data.get("generalization_examples", []),
            confidence_rating=performance_data.get("confidence_rating", 0),
            frequency_of_use=performance_data.get("frequency_of_use", "unknown"),
            effectiveness_rating=performance_data.get("effectiveness_rating", 0)
        )
        
        self._save_skill_assessment(assessment)
        self._update_skill_progression(patient_id, skill_id, mastery_level)
        
        return assessment
    
    def _determine_mastery_level(self, performance_data: Dict[str, Any], 
                                skill: TherapeuticSkill) -> MasteryLevel:
        
        understanding_score = performance_data.get("understanding_score", 0)
        application_score = performance_data.get("application_score", 0)
        independence_level = performance_data.get("independence_level", 0)
        generalization_score = performance_data.get("generalization_score", 0)
        
        overall_score = (understanding_score + application_score + independence_level + generalization_score) / 4
        
        if overall_score >= 9:
            return MasteryLevel.EXPERT
        elif overall_score >= 8:
            return MasteryLevel.ADVANCED
        elif overall_score >= 7:
            return MasteryLevel.PROFICIENT
        elif overall_score >= 5:
            return MasteryLevel.DEVELOPING
        elif overall_score >= 3:
            return MasteryLevel.EMERGING
        else:
            return MasteryLevel.NOT_DEMONSTRATED
    
    def _identify_competency_indicators(self, performance_data: Dict[str, Any], 
                                      skill: TherapeuticSkill) -> List[str]:
        
        indicators = []
        
        if performance_data.get("can_explain_skill", False):
            indicators.append("Can clearly explain skill rationale and components")
        
        if performance_data.get("demonstrates_accurately", False):
            indicators.append("Demonstrates skill accurately in practice")
        
        if performance_data.get("uses_independently", False):
            indicators.append("Uses skill independently without prompting")
        
        if performance_data.get("adapts_to_context", False):
            indicators.append("Adapts skill application to different contexts")
        
        if performance_data.get("reports_effectiveness", False):
            indicators.append("Reports positive outcomes from skill use")
        
        if performance_data.get("teaches_others", False):
            indicators.append("Able to teach or help others with skill")
        
        return indicators
    
    def _identify_improvement_areas(self, performance_data: Dict[str, Any], 
                                  skill: TherapeuticSkill) -> List[str]:
        
        areas = []
        
        if performance_data.get("understanding_score", 0) < 6:
            areas.append("Deepen conceptual understanding of skill")
        
        if performance_data.get("application_score", 0) < 6:
            areas.append("Improve accuracy of skill demonstration")
        
        if performance_data.get("independence_level", 0) < 6:
            areas.append("Increase independent skill use")
        
        if performance_data.get("generalization_score", 0) < 6:
            areas.append("Expand skill application to more situations")
        
        if performance_data.get("consistency_score", 0) < 6:
            areas.append("Improve consistency of skill performance")
        
        if performance_data.get("timing_appropriateness", 0) < 6:
            areas.append("Better recognition of when to use skill")
        
        return areas
    
    def _generate_practice_recommendations(self, mastery_level: MasteryLevel, 
                                         skill: TherapeuticSkill) -> List[str]:
        
        recommendations = []
        
        if mastery_level == MasteryLevel.NOT_DEMONSTRATED:
            recommendations.extend([
                "Begin with psychoeducation about skill benefits",
                "Use therapist modeling and demonstration",
                "Start with highly structured practice sessions",
                "Focus on basic skill components first"
            ])
        
        elif mastery_level == MasteryLevel.EMERGING:
            recommendations.extend([
                "Continue guided practice with therapist coaching",
                "Use written prompts and cue cards",
                "Practice in low-stakes situations",
                "Focus on one skill component at a time"
            ])
        
        elif mastery_level == MasteryLevel.DEVELOPING:
            recommendations.extend([
                "Gradually reduce therapist guidance",
                "Practice in increasingly challenging situations",
                "Develop personalized skill modifications",
                "Begin homework applications"
            ])
        
        elif mastery_level == MasteryLevel.PROFICIENT:
            recommendations.extend([
                "Focus on skill generalization",
                "Practice in high-stress situations",
                "Combine with other therapeutic skills",
                "Develop teaching or mentoring opportunities"
            ])
        
        elif mastery_level in [MasteryLevel.ADVANCED, MasteryLevel.EXPERT]:
            recommendations.extend([
                "Maintain skill through regular practice",
                "Explore advanced skill variations",
                "Mentor others in skill development",
                "Integrate skill into personal philosophy"
            ])
        
        return recommendations[:4]
    
    def track_skill_progression(self, patient_id: str, skill_id: str) -> SkillProgression:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT baseline_level, current_level, practice_sessions_completed,
                       total_practice_time, mastery_milestones, progression_rate,
                       projected_mastery_date, learning_curve_data
                FROM skill_progressions
                WHERE patient_id = ? AND skill_id = ?
                ORDER BY last_updated DESC
                LIMIT 1
            """, (patient_id, skill_id))
            
            result = cursor.fetchone()
        
        if result:
            return SkillProgression(
                patient_id=patient_id,
                skill_id=skill_id,
                baseline_level=MasteryLevel(result[0]),
                current_level=MasteryLevel(result[1]),
                practice_sessions_completed=result[2],
                total_practice_time=result[3],
                mastery_milestones=json.loads(result[4]) if result[4] else [],
                progression_rate=result[5],
                projected_mastery_date=datetime.fromisoformat(result[6]) if result[6] else None,
                learning_curve_data=json.loads(result[7]) if result[7] else []
            )
        else:
            return SkillProgression(
                patient_id=patient_id,
                skill_id=skill_id,
                baseline_level=MasteryLevel.NOT_DEMONSTRATED,
                current_level=MasteryLevel.NOT_DEMONSTRATED,
                practice_sessions_completed=0,
                total_practice_time=0,
                mastery_milestones=[],
                progression_rate="unknown",
                projected_mastery_date=None,
                learning_curve_data=[]
            )
    
    def create_personalized_practice_plan(self, patient_id: str, goals: List[str], 
                                        constraints: Dict[str, Any]) -> Dict[str, Any]:
        
        current_skills = self._get_patient_skill_levels(patient_id)
        recommended_skills = self._recommend_skills_for_goals(goals)
        
        practice_plan = {
            "patient_id": patient_id,
            "goals": goals,
            "skill_priorities": [],
            "practice_schedule": {},
            "progression_timeline": {},
            "resource_requirements": []
        }
        
        time_available = constraints.get("time_per_week", 60)
        difficulty_preference = constraints.get("difficulty_preference", "moderate")
        focus_areas = constraints.get("focus_areas", [])
        
        priority_skills = []
        for skill_id in recommended_skills:
            skill = self.skill_library.get(skill_id)
            current_level = current_skills.get(skill_id, MasteryLevel.NOT_DEMONSTRATED)
            
            if skill and current_level != MasteryLevel.EXPERT:
                priority_score = self._calculate_skill_priority(skill, goals, current_level, focus_areas)
                priority_skills.append((skill_id, priority_score, skill.difficulty_level))
        
        priority_skills.sort(key=lambda x: x[1], reverse=True)
        
        time_allocated = 0
        for skill_id, priority_score, difficulty in priority_skills[:5]:
            skill = self.skill_library[skill_id]
            
            if time_allocated + skill.estimated_practice_time <= time_available:
                practice_plan["skill_priorities"].append({
                    "skill_id": skill_id,
                    "skill_name": skill.name,
                    "priority_score": priority_score,
                    "current_level": current_skills.get(skill_id, MasteryLevel.NOT_DEMONSTRATED).value,
                    "target_level": "proficient",
                    "estimated_weeks": self._estimate_learning_time(skill, current_skills.get(skill_id, MasteryLevel.NOT_DEMONSTRATED))
                })
                
                practice_plan["practice_schedule"][skill_id] = {
                    "sessions_per_week": 2 if skill.difficulty_level == SkillLevel.ADVANCED else 1,
                    "minutes_per_session": skill.estimated_practice_time,
                    "practice_format": skill.practice_formats[0].value,
                    "homework_frequency": "daily" if skill.category in [SkillCategory.MINDFULNESS, SkillCategory.RELAXATION] else "3x_per_week"
                }
                
                time_allocated += skill.estimated_practice_time
        
        return practice_plan
    
    def _calculate_skill_priority(self, skill: TherapeuticSkill, goals: List[str], 
                                current_level: MasteryLevel, focus_areas: List[str]) -> float:
        
        priority_score = 0.0
        
        goal_keywords = {
            "anxiety": ["cognitive", "relaxation", "mindfulness", "exposure"],
            "depression": ["cognitive", "behavioral", "problem_solving"],
            "relationships": ["interpersonal", "communication", "assertive"],
            "stress": ["relaxation", "mindfulness", "emotional_regulation"],
            "trauma": ["emotional_regulation", "distress_tolerance", "mindfulness"],
            "anger": ["emotional_regulation", "interpersonal", "mindfulness"]
        }
        
        for goal in goals:
            goal_lower = goal.lower()
            for goal_type, keywords in goal_keywords.items():
                if goal_type in goal_lower:
                    if any(keyword in skill.name.lower() or keyword in skill.description.lower() 
                           for keyword in keywords):
                        priority_score += 2.0
        
        if skill.category.value in focus_areas:
            priority_score += 1.5
        
        mastery_bonus = {
            MasteryLevel.NOT_DEMONSTRATED: 3.0,
            MasteryLevel.EMERGING: 2.5,
            MasteryLevel.DEVELOPING: 2.0,
            MasteryLevel.PROFICIENT: 1.0,
            MasteryLevel.ADVANCED: 0.5,
            MasteryLevel.EXPERT: 0.0
        }
        priority_score += mastery_bonus.get(current_level, 0.0)
        
        difficulty_modifier = {
            SkillLevel.BEGINNER: 1.2,
            SkillLevel.INTERMEDIATE: 1.0,
            SkillLevel.ADVANCED: 0.8
        }
        priority_score *= difficulty_modifier.get(skill.difficulty_level, 1.0)
        
        return priority_score
    
    def _estimate_learning_time(self, skill: TherapeuticSkill, current_level: MasteryLevel) -> int:
        
        base_weeks = {
            SkillLevel.BEGINNER: 4,
            SkillLevel.INTERMEDIATE: 6,
            SkillLevel.ADVANCED: 8
        }
        
        level_adjustment = {
            MasteryLevel.NOT_DEMONSTRATED: 1.0,
            MasteryLevel.EMERGING: 0.8,
            MasteryLevel.DEVELOPING: 0.6,
            MasteryLevel.PROFICIENT: 0.2,
            MasteryLevel.ADVANCED: 0.1,
            MasteryLevel.EXPERT: 0.0
        }
        
        base_time = base_weeks.get(skill.difficulty_level, 6)
        adjustment = level_adjustment.get(current_level, 1.0)
        
        return max(1, int(base_time * adjustment))
    
    def _recommend_skills_for_goals(self, goals: List[str]) -> List[str]:
        
        recommended = set()
        
        skill_mappings = {
            "anxiety": ["cognitive_restructuring", "mindfulness_meditation", "progressive_muscle_relaxation"],
            "depression": ["cognitive_restructuring", "behavioral_activation", "problem_solving"],
            "relationships": ["assertive_communication", "interpersonal_effectiveness", "emotional_regulation"],
            "stress": ["mindfulness_meditation", "progressive_muscle_relaxation", "emotional_regulation"],
            "communication": ["assertive_communication", "interpersonal_effectiveness"],
            "emotions": ["emotional_regulation", "mindfulness_meditation", "distress_tolerance"],
            "coping": ["problem_solving", "emotional_regulation", "mindfulness_meditation"]
        }
        
        for goal in goals:
            goal_lower = goal.lower()
            for category, skills in skill_mappings.items():
                if category in goal_lower:
                    recommended.update(skills)
        
        return list(recommended)
    
    def _get_patient_skill_levels(self, patient_id: str) -> Dict[str, MasteryLevel]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT skill_id, mastery_level
                FROM skill_assessments
                WHERE patient_id = ?
                ORDER BY assessment_date DESC
            """, (patient_id,))
            
            results = cursor.fetchall()
        
        skill_levels = {}
        seen_skills = set()
        
        for skill_id, mastery_level in results:
            if skill_id not in seen_skills:
                skill_levels[skill_id] = MasteryLevel(mastery_level)
                seen_skills.add(skill_id)
        
        return skill_levels
    
    def generate_practice_feedback(self, practice_session: SkillPracticeSession, 
                                 performance_observations: Dict[str, Any]) -> str:
        
        skill = self.skill_library.get(practice_session.skill_id)
        if not skill:
            return "Unable to generate feedback - skill not found."
        
        feedback_parts = []
        
        strengths = performance_observations.get("strengths", [])
        if strengths:
            feedback_parts.append(f"Strengths demonstrated: {', '.join(strengths)}")
        
        improvement_areas = performance_observations.get("areas_for_improvement", [])
        if improvement_areas:
            feedback_parts.append(f"Areas for continued development: {', '.join(improvement_areas)}")
        
        mastery_level = practice_session.mastery_demonstration
        level_feedback = {
            MasteryLevel.EMERGING: "You're beginning to understand this skill. Keep practicing the basics.",
            MasteryLevel.DEVELOPING: "You're making good progress. Focus on consistency and independence.",
            MasteryLevel.PROFICIENT: "Excellent work! You're using this skill effectively. Consider applying it to new situations.",
            MasteryLevel.ADVANCED: "Outstanding mastery. You might help others learn this skill.",
            MasteryLevel.EXPERT: "Exceptional expertise. Continue refining and teaching others."
        }
        
        if mastery_level in level_feedback:
            feedback_parts.append(level_feedback[mastery_level])
        
        if practice_session.breakthrough_moments:
            feedback_parts.append(f"Breakthrough moments: {'; '.join(practice_session.breakthrough_moments)}")
        
        if practice_session.challenges_encountered:
            challenge_feedback = "Common challenges you experienced: " + ", ".join(practice_session.challenges_encountered)
            feedback_parts.append(challenge_feedback)
            
            relevant_tips = [tip for tip in skill.coaching_tips 
                           if any(challenge.lower() in tip.lower() for challenge in practice_session.challenges_encountered)]
            if relevant_tips:
                feedback_parts.append(f"Helpful tips: {'; '.join(relevant_tips[:2])}")
        
        if practice_session.next_practice_steps:
            feedback_parts.append(f"Next steps: {'; '.join(practice_session.next_practice_steps)}")
        
        return " ".join(feedback_parts)
    
    def create_skill_development_report(self, patient_id: str, months: int = 3) -> Dict[str, Any]:
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT sps.skill_id, sps.practice_date, sps.mastery_demonstration,
                       sps.duration_minutes, sps.challenges_encountered, sps.breakthrough_moments
                FROM skill_practice_sessions sps
                WHERE sps.patient_id = ? AND sps.practice_date >= ?
                ORDER BY sps.practice_date
            """, (patient_id, start_date.isoformat()))
            
            practice_data = cursor.fetchall()
            
            cursor.execute("""
                SELECT sa.skill_id, sa.mastery_level, sa.assessment_date,
                       sa.confidence_rating, sa.effectiveness_rating
                FROM skill_assessments sa
                WHERE sa.patient_id = ? AND sa.assessment_date >= ?
                ORDER BY sa.assessment_date
            """, (patient_id, start_date.isoformat()))
            
            assessment_data = cursor.fetchall()
        
        report = {
            "patient_id": patient_id,
            "report_period": f"{start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}",
            "skills_practiced": {},
            "mastery_progressions": {},
            "total_practice_time": 0,
            "breakthrough_moments": [],
            "common_challenges": {},
            "skill_effectiveness": {},
            "recommendations": []
        }
        
        for skill_id, practice_date, mastery_level, duration, challenges_json, breakthroughs_json in practice_data:
            if skill_id not in report["skills_practiced"]:
                report["skills_practiced"][skill_id] = {
                    "skill_name": self.skill_library.get(skill_id, {}).name if skill_id in self.skill_library else skill_id,
                    "practice_sessions": 0,
                    "total_time": 0,
                    "latest_mastery": mastery_level
                }
            
            report["skills_practiced"][skill_id]["practice_sessions"] += 1
            report["skills_practiced"][skill_id]["total_time"] += duration
            report["total_practice_time"] += duration
            
            if breakthroughs_json:
                breakthroughs = json.loads(breakthroughs_json)
                report["breakthrough_moments"].extend(breakthroughs)
            
            if challenges_json:
                challenges = json.loads(challenges_json)
                for challenge in challenges:
                    report["common_challenges"][challenge] = report["common_challenges"].get(challenge, 0) + 1
        
        for skill_id, mastery_level, assessment_date, confidence, effectiveness in assessment_data:
            if skill_id not in report["mastery_progressions"]:
                report["mastery_progressions"][skill_id] = []
            
            report["mastery_progressions"][skill_id].append({
                "date": assessment_date,
                "mastery_level": mastery_level,
                "confidence": confidence,
                "effectiveness": effectiveness
            })
            
            if skill_id not in report["skill_effectiveness"]:
                report["skill_effectiveness"][skill_id] = []
            report["skill_effectiveness"][skill_id].append(effectiveness)
        
        for skill_id, effectiveness_scores in report["skill_effectiveness"].items():
            if effectiveness_scores:
                avg_effectiveness = sum(effectiveness_scores) / len(effectiveness_scores)
                report["skill_effectiveness"][skill_id] = round(avg_effectiveness, 1)
        
        if report["total_practice_time"] < 180:  # Less than 3 hours per month
            report["recommendations"].append("Consider increasing practice frequency for better skill development")
        
        top_challenges = sorted(report["common_challenges"].items(), key=lambda x: x[1], reverse=True)
        if top_challenges:
            most_common_challenge = top_challenges[0][0]
            report["recommendations"].append(f"Focus on addressing recurring challenge: {most_common_challenge}")
        
        low_effectiveness_skills = [skill_id for skill_id, eff in report["skill_effectiveness"].items() if eff < 6]
        if low_effectiveness_skills:
            report["recommendations"].append(f"Review approach for skills with lower effectiveness: {', '.join(low_effectiveness_skills)}")
        
        if len(report["breakthrough_moments"]) > 5:
            report["recommendations"].append("Excellent progress with breakthrough moments - continue current approach")
        
        return report
    
    def _update_skill_progression(self, patient_id: str, skill_id: str, new_mastery_level: MasteryLevel):
        
        current_progression = self.track_skill_progression(patient_id, skill_id)
        
        if current_progression.current_level != new_mastery_level:
            milestone = {
                "date": datetime.now().isoformat(),
                "level_achieved": new_mastery_level.value,
                "previous_level": current_progression.current_level.value
            }
            
            current_progression.mastery_milestones.append(milestone)
            current_progression.current_level = new_mastery_level
            current_progression.practice_sessions_completed += 1
            
            progression_rate = self._calculate_progression_rate(current_progression)
            current_progression.progression_rate = progression_rate
            
            self._save_skill_progression(current_progression)
    
    def _calculate_progression_rate(self, progression: SkillProgression) -> str:
        
        if len(progression.mastery_milestones) < 2:
            return "insufficient_data"
        
        level_values = {
            MasteryLevel.NOT_DEMONSTRATED: 0,
            MasteryLevel.EMERGING: 1,
            MasteryLevel.DEVELOPING: 2,
            MasteryLevel.PROFICIENT: 3,
            MasteryLevel.ADVANCED: 4,
            MasteryLevel.EXPERT: 5
        }
        
        first_milestone = progression.mastery_milestones[0]
        latest_milestone = progression.mastery_milestones[-1]
        
        first_level = level_values.get(MasteryLevel(first_milestone["level_achieved"]), 0)
        latest_level = level_values.get(MasteryLevel(latest_milestone["level_achieved"]), 0)
        
        level_change = latest_level - first_level
        
        first_date = datetime.fromisoformat(first_milestone["date"])
        latest_date = datetime.fromisoformat(latest_milestone["date"])
        time_span_weeks = (latest_date - first_date).days / 7
        
        if time_span_weeks == 0:
            return "rapid"
        
        rate = level_change / time_span_weeks
        
        if rate >= 0.5:
            return "rapid"
        elif rate >= 0.25:
            return "moderate"
        elif rate >= 0.1:
            return "gradual"
        else:
            return "slow"
    
    def _save_skill_practice_session(self, session: SkillPracticeSession):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO skill_practice_sessions
                (practice_id, session_id, patient_id, skill_id, practice_format,
                 duration_minutes, practice_scenario, coaching_provided,
                 patient_performance, mastery_demonstration, challenges_encountered,
                 breakthrough_moments, feedback_given, patient_self_assessment,
                 homework_connection, next_practice_steps, practice_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.practice_id, session.session_id, session.patient_id,
                session.skill_id, session.practice_format.value, session.duration_minutes,
                session.practice_scenario, json.dumps(session.coaching_provided),
                json.dumps(session.patient_performance), session.mastery_demonstration.value,
                json.dumps(session.challenges_encountered), json.dumps(session.breakthrough_moments),
                session.feedback_given, session.patient_self_assessment,
                session.homework_connection, json.dumps(session.next_practice_steps),
                session.practice_date.isoformat()
            ))
    
    def _save_skill_assessment(self, assessment: SkillAssessment):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO skill_assessments
                (assessment_id, patient_id, skill_id, assessment_date, mastery_level,
                 competency_indicators, areas_for_improvement, practice_recommendations,
                 generalization_evidence, confidence_rating, frequency_of_use,
                 effectiveness_rating)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment.assessment_id, assessment.patient_id, assessment.skill_id,
                assessment.assessment_date.isoformat(), assessment.mastery_level.value,
                json.dumps(assessment.competency_indicators),
                json.dumps(assessment.areas_for_improvement),
                json.dumps(assessment.practice_recommendations),
                json.dumps(assessment.generalization_evidence),
                assessment.confidence_rating, assessment.frequency_of_use,
                assessment.effectiveness_rating
            ))
    
    def _save_skill_progression(self, progression: SkillProgression):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO skill_progressions
                (patient_id, skill_id, baseline_level, current_level,
                 practice_sessions_completed, total_practice_time, mastery_milestones,
                 progression_rate, projected_mastery_date, learning_curve_data,
                 last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                progression.patient_id, progression.skill_id,
                progression.baseline_level.value, progression.current_level.value,
                progression.practice_sessions_completed, progression.total_practice_time,
                json.dumps(progression.mastery_milestones), progression.progression_rate,
                progression.projected_mastery_date.isoformat() if progression.projected_mastery_date else None,
                json.dumps(progression.learning_curve_data), datetime.now().isoformat()
            ))


if __name__ == "__main__":
    skill_system = SkillPracticeSystem()
    
    practice_session = skill_system.conduct_skill_practice(
        session_id="session_001",
        patient_id="patient_123",
        skill_id="cognitive_restructuring",
        practice_format=PracticeFormat.GUIDED_PRACTICE,
        scenario="Challenging thoughts about work presentation"
    )
    
    print("=== SKILL PRACTICE SESSION ===")
    print(f"Practice ID: {practice_session.practice_id}")
    print(f"Skill: {practice_session.skill_id}")
    print(f"Format: {practice_session.practice_format.value}")
    print(f"Duration: {practice_session.duration_minutes} minutes")
    
    performance_data = {
        "understanding_score": 7,
        "application_score": 6,
        "independence_level": 5,
        "generalization_score": 4,
        "confidence_rating": 6,
        "effectiveness_rating": 7,
        "can_explain_skill": True,
        "demonstrates_accurately": True,
        "uses_independently": False,
        "adapts_to_context": False
    }
    
    assessment = skill_system.assess_skill_mastery("patient_123", "cognitive_restructuring", performance_data)
    print(f"\n=== SKILL ASSESSMENT ===")
    print(f"Mastery Level: {assessment.mastery_level.value}")
    print(f"Competency Indicators: {assessment.competency_indicators}")
    print(f"Areas for Improvement: {assessment.areas_for_improvement}")
    print(f"Practice Recommendations: {assessment.practice_recommendations}")
    
    progression = skill_system.track_skill_progression("patient_123", "cognitive_restructuring")
    print(f"\n=== SKILL PROGRESSION ===")
    print(f"Current Level: {progression.current_level.value}")
    print(f"Practice Sessions: {progression.practice_sessions_completed}")
    print(f"Progression Rate: {progression.progression_rate}")
    
    goals = ["reduce anxiety", "improve relationships", "manage stress"]
    constraints = {"time_per_week": 90, "difficulty_preference": "moderate"}
    
    practice_plan = skill_system.create_personalized_practice_plan("patient_123", goals, constraints)
    print(f"\n=== PERSONALIZED PRACTICE PLAN ===")
    print(f"Goals: {practice_plan['goals']}")
    print(f"Priority Skills: {len(practice_plan['skill_priorities'])}")
    for skill_priority in practice_plan['skill_priorities']:
        print(f"- {skill_priority['skill_name']}: {skill_priority['current_level']} → {skill_priority['target_level']}")
    
    report = skill_system.create_skill_development_report("patient_123", 3)
    print(f"\n=== SKILL DEVELOPMENT REPORT ===")
    print(f"Total Practice Time: {report['total_practice_time']} minutes")
    print(f"Skills Practiced: {len(report['skills_practiced'])}")
    print(f"Breakthrough Moments: {len(report['breakthrough_moments'])}")
    print(f"Recommendations: {report['recommendations']}")
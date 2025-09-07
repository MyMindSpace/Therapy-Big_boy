"""
Therapy Protocols Module
Evidence-based therapy protocols for AI therapy system
Provides structured treatment protocols for different therapeutic modalities
"""

from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json


class TherapyModality(Enum):
    """Therapeutic modalities"""
    CBT = "cognitive_behavioral_therapy"
    DBT = "dialectical_behavior_therapy"
    ACT = "acceptance_commitment_therapy"
    PSYCHODYNAMIC = "psychodynamic_therapy"
    HUMANISTIC = "humanistic_therapy"
    EMDR = "eye_movement_desensitization_reprocessing"
    IPT = "interpersonal_therapy"
    SOLUTION_FOCUSED = "solution_focused_brief_therapy"


class SessionPhase(Enum):
    """Phases within a therapy session"""
    OPENING = "opening"
    CHECK_IN = "check_in"
    HOMEWORK_REVIEW = "homework_review"
    AGENDA_SETTING = "agenda_setting"
    MAIN_WORK = "main_work"
    SKILL_PRACTICE = "skill_practice"
    HOMEWORK_ASSIGNMENT = "homework_assignment"
    SUMMARY = "summary"
    CLOSING = "closing"


class TreatmentPhase(Enum):
    """Overall treatment phases"""
    ASSESSMENT = "assessment"
    STABILIZATION = "stabilization"
    PREPARATION = "preparation"
    WORKING = "working"
    INTEGRATION = "integration"
    MAINTENANCE = "maintenance"
    TERMINATION = "termination"


class InterventionType(Enum):
    """Types of therapeutic interventions"""
    PSYCHOEDUCATION = "psychoeducation"
    COGNITIVE_RESTRUCTURING = "cognitive_restructuring"
    BEHAVIORAL_ACTIVATION = "behavioral_activation"
    EXPOSURE = "exposure"
    MINDFULNESS = "mindfulness"
    SKILLS_TRAINING = "skills_training"
    EMOTIONAL_REGULATION = "emotional_regulation"
    INTERPERSONAL_SKILLS = "interpersonal_skills"
    TRAUMA_PROCESSING = "trauma_processing"
    RELAPSE_PREVENTION = "relapse_prevention"


@dataclass
class SessionStructure:
    """Structure of a therapy session"""
    phase: SessionPhase
    duration_minutes: int
    objectives: List[str]
    interventions: List[InterventionType]
    required: bool = True
    adaptable: bool = True
    clinical_notes: str = ""


@dataclass
class TherapeuticIntervention:
    """Individual therapeutic intervention"""
    intervention_id: str
    name: str
    intervention_type: InterventionType
    modality: TherapyModality
    description: str
    objectives: List[str]
    contraindications: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    materials_needed: List[str] = field(default_factory=list)
    estimated_duration: int = 15  # minutes
    difficulty_level: str = "beginner"  # beginner, intermediate, advanced
    evidence_base: str = ""
    instructions: str = ""
    homework_suggestions: List[str] = field(default_factory=list)


@dataclass
class TreatmentProtocol:
    """Complete treatment protocol for a specific condition/modality"""
    protocol_id: str
    name: str
    modality: TherapyModality
    target_conditions: List[str]
    treatment_phases: List[TreatmentPhase]
    total_sessions: int
    session_frequency: str  # weekly, biweekly, etc.
    session_structures: Dict[SessionPhase, SessionStructure]
    interventions: List[TherapeuticIntervention]
    assessment_schedule: Dict[str, int]  # assessment_type: session_number
    outcome_measures: List[str]
    contraindications: List[str] = field(default_factory=list)
    prerequisite_skills: List[str] = field(default_factory=list)
    therapist_qualifications: List[str] = field(default_factory=list)
    evidence_level: str = "Level 1"  # Evidence-based treatment levels
    references: List[str] = field(default_factory=list)


@dataclass
class ProtocolAdaptation:
    """Adaptations to protocols for specific patient needs"""
    adaptation_id: str
    base_protocol_id: str
    patient_characteristics: Dict[str, Any]
    modifications: List[str]
    rationale: str
    additional_interventions: List[str] = field(default_factory=list)
    session_adjustments: Dict[str, Any] = field(default_factory=dict)


class TherapyProtocolManager:
    """Manages therapy protocols and treatment guidelines"""
    
    def __init__(self):
        self.protocols = self._initialize_protocols()
        self.interventions_library = self._initialize_interventions()
        self.session_templates = self._initialize_session_templates()
        self.adaptation_rules = self._initialize_adaptation_rules()
    
    def _initialize_protocols(self) -> Dict[str, TreatmentProtocol]:
        """Initialize evidence-based treatment protocols"""
        
        protocols = {}
        
        # CBT Protocol for Depression
        protocols["CBT_DEPRESSION"] = TreatmentProtocol(
            protocol_id="CBT_DEPRESSION",
            name="Cognitive Behavioral Therapy for Depression",
            modality=TherapyModality.CBT,
            target_conditions=["Major Depressive Disorder", "Persistent Depressive Disorder", "Depression NOS"],
            treatment_phases=[
                TreatmentPhase.ASSESSMENT,
                TreatmentPhase.STABILIZATION,
                TreatmentPhase.WORKING,
                TreatmentPhase.INTEGRATION,
                TreatmentPhase.TERMINATION
            ],
            total_sessions=16,
            session_frequency="weekly",
            session_structures={
                SessionPhase.OPENING: SessionStructure(
                    phase=SessionPhase.OPENING,
                    duration_minutes=5,
                    objectives=["Establish rapport", "Review mood"],
                    interventions=[InterventionType.PSYCHOEDUCATION],
                    required=True
                ),
                SessionPhase.CHECK_IN: SessionStructure(
                    phase=SessionPhase.CHECK_IN,
                    duration_minutes=10,
                    objectives=["Assess current mood", "Review week's events", "Safety check"],
                    interventions=[InterventionType.PSYCHOEDUCATION],
                    required=True
                ),
                SessionPhase.HOMEWORK_REVIEW: SessionStructure(
                    phase=SessionPhase.HOMEWORK_REVIEW,
                    duration_minutes=10,
                    objectives=["Review homework completion", "Process learning"],
                    interventions=[InterventionType.COGNITIVE_RESTRUCTURING, InterventionType.BEHAVIORAL_ACTIVATION],
                    required=False
                ),
                SessionPhase.MAIN_WORK: SessionStructure(
                    phase=SessionPhase.MAIN_WORK,
                    duration_minutes=20,
                    objectives=["Address session agenda", "Practice core CBT skills"],
                    interventions=[InterventionType.COGNITIVE_RESTRUCTURING, InterventionType.BEHAVIORAL_ACTIVATION],
                    required=True
                ),
                SessionPhase.HOMEWORK_ASSIGNMENT: SessionStructure(
                    phase=SessionPhase.HOMEWORK_ASSIGNMENT,
                    duration_minutes=5,
                    objectives=["Assign relevant homework", "Ensure understanding"],
                    interventions=[InterventionType.BEHAVIORAL_ACTIVATION],
                    required=True
                )
            },
            interventions=[
                "cognitive_restructuring_basic",
                "thought_records",
                "behavioral_activation",
                "activity_scheduling",
                "mood_monitoring",
                "relapse_prevention"
            ],
            assessment_schedule={
                "PHQ9": 1,  # Every session initially
                "GAD7": 4,  # Every 4 sessions
                "ORS": 1    # Every session
            },
            outcome_measures=["PHQ-9", "BDI-II", "BAI", "ORS"],
            contraindications=["Active psychosis", "Severe cognitive impairment", "Active substance abuse"],
            evidence_level="Level 1 - Strong Research Support",
            references=[
                "Beck, A. T., Rush, A. J., Shaw, B. F., & Emery, G. (1979). Cognitive therapy of depression.",
                "Butler, A. C., et al. (2006). The empirical status of cognitive-behavioral therapy: A review of meta-analyses."
            ]
        )
        
        # DBT Protocol for Borderline Personality Disorder
        protocols["DBT_BPD"] = TreatmentProtocol(
            protocol_id="DBT_BPD",
            name="Dialectical Behavior Therapy for Borderline Personality Disorder",
            modality=TherapyModality.DBT,
            target_conditions=["Borderline Personality Disorder", "Emotion Dysregulation", "Self-harm behaviors"],
            treatment_phases=[
                TreatmentPhase.STABILIZATION,
                TreatmentPhase.WORKING,
                TreatmentPhase.INTEGRATION,
                TreatmentPhase.MAINTENANCE
            ],
            total_sessions=52,  # 1 year of weekly sessions
            session_frequency="weekly",
            session_structures={
                SessionPhase.CHECK_IN: SessionStructure(
                    phase=SessionPhase.CHECK_IN,
                    duration_minutes=10,
                    objectives=["Assess current distress", "Review diary card", "Safety assessment"],
                    interventions=[InterventionType.EMOTIONAL_REGULATION],
                    required=True
                ),
                SessionPhase.MAIN_WORK: SessionStructure(
                    phase=SessionPhase.MAIN_WORK,
                    duration_minutes=35,
                    objectives=["Skills training", "Crisis management", "Behavioral analysis"],
                    interventions=[
                        InterventionType.MINDFULNESS,
                        InterventionType.EMOTIONAL_REGULATION,
                        InterventionType.INTERPERSONAL_SKILLS,
                        InterventionType.SKILLS_TRAINING
                    ],
                    required=True
                )
            },
            interventions=[
                "mindfulness_core",
                "distress_tolerance",
                "emotion_regulation",
                "interpersonal_effectiveness",
                "crisis_survival_skills",
                "behavioral_chain_analysis"
            ],
            assessment_schedule={
                "CSSRS": 1,     # Every session
                "BPD_CHECKLIST": 4,  # Every 4 sessions
                "ORS": 2        # Every other session
            },
            outcome_measures=["Borderline Evaluation of Severity over Time", "Difficulties in Emotion Regulation Scale"],
            contraindications=["Active psychosis without insight", "Severe cognitive impairment"],
            therapist_qualifications=["DBT training certification", "Experience with personality disorders"],
            evidence_level="Level 1 - Strong Research Support",
            references=[
                "Linehan, M. M. (2014). DBT Skills Training Manual, Second Edition.",
                "Kliem, S., et al. (2010). A meta-analysis of DBT for borderline personality disorder."
            ]
        )
        
        # ACT Protocol for Anxiety Disorders
        protocols["ACT_ANXIETY"] = TreatmentProtocol(
            protocol_id="ACT_ANXIETY",
            name="Acceptance and Commitment Therapy for Anxiety Disorders",
            modality=TherapyModality.ACT,
            target_conditions=["Generalized Anxiety Disorder", "Social Anxiety", "Panic Disorder"],
            treatment_phases=[
                TreatmentPhase.ASSESSMENT,
                TreatmentPhase.PREPARATION,
                TreatmentPhase.WORKING,
                TreatmentPhase.INTEGRATION
            ],
            total_sessions=12,
            session_frequency="weekly",
            session_structures={
                SessionPhase.OPENING: SessionStructure(
                    phase=SessionPhase.OPENING,
                    duration_minutes=5,
                    objectives=["Present moment awareness", "Connect with values"],
                    interventions=[InterventionType.MINDFULNESS],
                    required=True
                ),
                SessionPhase.MAIN_WORK: SessionStructure(
                    phase=SessionPhase.MAIN_WORK,
                    duration_minutes=35,
                    objectives=["Practice psychological flexibility", "Values clarification", "Committed action"],
                    interventions=[
                        InterventionType.MINDFULNESS,
                        InterventionType.COGNITIVE_RESTRUCTURING,
                        InterventionType.BEHAVIORAL_ACTIVATION
                    ],
                    required=True
                ),
                SessionPhase.CLOSING: SessionStructure(
                    phase=SessionPhase.CLOSING,
                    duration_minutes=10,
                    objectives=["Summarize insights", "Plan values-based actions"],
                    interventions=[InterventionType.BEHAVIORAL_ACTIVATION],
                    required=True
                )
            },
            interventions=[
                "mindfulness_meditation",
                "cognitive_defusion",
                "acceptance_strategies",
                "values_clarification",
                "committed_action_planning",
                "psychological_flexibility_training"
            ],
            assessment_schedule={
                "GAD7": 1,
                "AAQ_II": 4,  # Acceptance and Action Questionnaire
                "VLQ": 6      # Valued Living Questionnaire
            },
            outcome_measures=["GAD-7", "AAQ-II", "VLQ", "DASS-21"],
            evidence_level="Level 1 - Strong Research Support",
            references=[
                "Hayes, S. C., Strosahl, K. D., & Wilson, K. G. (2011). Acceptance and Commitment Therapy.",
                "A-Tjak, J. G., et al. (2015). A meta-analysis of the efficacy of ACT for clinically relevant mental and physical health problems."
            ]
        )
        
        # EMDR Protocol for PTSD
        protocols["EMDR_PTSD"] = TreatmentProtocol(
            protocol_id="EMDR_PTSD",
            name="Eye Movement Desensitization and Reprocessing for PTSD",
            modality=TherapyModality.EMDR,
            target_conditions=["Post-Traumatic Stress Disorder", "Acute Stress Disorder", "Complex PTSD"],
            treatment_phases=[
                TreatmentPhase.ASSESSMENT,
                TreatmentPhase.PREPARATION,
                TreatmentPhase.WORKING,
                TreatmentPhase.INTEGRATION
            ],
            total_sessions=12,
            session_frequency="weekly",
            session_structures={
                SessionPhase.PREPARATION: SessionStructure(
                    phase=SessionPhase.PREPARATION,
                    duration_minutes=15,
                    objectives=["Establish safety", "Resource installation", "Stabilization"],
                    interventions=[InterventionType.PSYCHOEDUCATION, InterventionType.EMOTIONAL_REGULATION],
                    required=True
                ),
                SessionPhase.MAIN_WORK: SessionStructure(
                    phase=SessionPhase.MAIN_WORK,
                    duration_minutes=30,
                    objectives=["Process traumatic memories", "Bilateral stimulation", "Installation"],
                    interventions=[InterventionType.TRAUMA_PROCESSING],
                    required=True
                )
            },
            interventions=[
                "trauma_history_taking",
                "resource_installation",
                "bilateral_stimulation",
                "memory_processing",
                "positive_cognition_installation",
                "body_scan_completion"
            ],
            assessment_schedule={
                "PCL5": 1,      # Every session initially
                "CSSRS": 1,     # Safety monitoring
                "SUD": 1        # Subjective Units of Disturbance
            },
            outcome_measures=["PCL-5", "IES-R", "DES", "CAPS-5"],
            contraindications=[
                "Unstable psychiatric condition",
                "Active substance abuse",
                "Severe dissociative disorder without stabilization",
                "Recent suicide attempt"
            ],
            therapist_qualifications=["EMDR certification", "Trauma therapy training"],
            evidence_level="Level 1 - Strong Research Support",
            references=[
                "Shapiro, F. (2001). Eye Movement Desensitization and Reprocessing: Basic Principles, Protocols, and Procedures.",
                "Chen, L., et al. (2014). EMDR for PTSD: A systematic review and meta-analysis."
            ]
        )
        
        return protocols
    
    def _initialize_interventions(self) -> Dict[str, TherapeuticIntervention]:
        """Initialize library of therapeutic interventions"""
        
        interventions = {}
        
        # CBT Interventions
        interventions["cognitive_restructuring_basic"] = TherapeuticIntervention(
            intervention_id="cognitive_restructuring_basic",
            name="Basic Cognitive Restructuring",
            intervention_type=InterventionType.COGNITIVE_RESTRUCTURING,
            modality=TherapyModality.CBT,
            description="Teaching patients to identify and challenge negative thought patterns",
            objectives=[
                "Identify automatic thoughts",
                "Examine evidence for/against thoughts",
                "Develop balanced alternative thoughts",
                "Practice new thinking patterns"
            ],
            materials_needed=["Thought record worksheet", "CBT triangle diagram"],
            estimated_duration=20,
            difficulty_level="beginner",
            evidence_base="Extensive research support in CBT literature",
            instructions="""
1. Introduce the CBT model (thoughts, feelings, behaviors)
2. Help patient identify specific automatic thoughts
3. Examine evidence supporting and contradicting the thought
4. Develop a more balanced, realistic thought
5. Practice using the new thought in similar situations
6. Assign homework to practice between sessions
            """,
            homework_suggestions=[
                "Complete daily thought records",
                "Practice challenging one negative thought per day",
                "Notice patterns in thinking errors"
            ]
        )
        
        interventions["behavioral_activation"] = TherapeuticIntervention(
            intervention_id="behavioral_activation",
            name="Behavioral Activation",
            intervention_type=InterventionType.BEHAVIORAL_ACTIVATION,
            modality=TherapyModality.CBT,
            description="Increasing engagement in meaningful and pleasant activities",
            objectives=[
                "Identify valued activities",
                "Schedule pleasant and meaningful activities",
                "Increase activity level gradually",
                "Break cycle of depression and inactivity"
            ],
            materials_needed=["Activity scheduling worksheet", "Pleasant activities list"],
            estimated_duration=25,
            difficulty_level="beginner",
            evidence_base="Strong evidence for depression treatment",
            instructions="""
1. Assess current activity level and patterns
2. Identify activities that provide mastery or pleasure
3. Schedule specific activities at specific times
4. Start with small, achievable goals
5. Monitor mood before and after activities
6. Gradually increase activity level
            """,
            homework_suggestions=[
                "Complete activity schedule daily",
                "Engage in one pleasant activity per day",
                "Rate mood before and after activities"
            ]
        )
        
        # DBT Interventions
        interventions["mindfulness_core"] = TherapeuticIntervention(
            intervention_id="mindfulness_core",
            name="Core Mindfulness Skills",
            intervention_type=InterventionType.MINDFULNESS,
            modality=TherapyModality.DBT,
            description="Teaching present-moment awareness and non-judgmental observation",
            objectives=[
                "Learn wise mind concept",
                "Practice observe, describe, participate skills",
                "Develop non-judgmental stance",
                "Increase present-moment awareness"
            ],
            materials_needed=["Mindfulness worksheets", "Audio recordings for guided practice"],
            estimated_duration=30,
            difficulty_level="beginner",
            evidence_base="Core component of DBT with extensive research support",
            instructions="""
1. Introduce three states of mind: emotion mind, reasonable mind, wise mind
2. Practice 'observe' skill - noticing without describing
3. Practice 'describe' skill - putting words to experience
4. Practice 'participate' skill - fully engaging in activity
5. Teach one-mindfully and non-judgmentally
6. Assign daily mindfulness practice
            """,
            homework_suggestions=[
                "Practice mindfulness meditation 10 minutes daily",
                "Complete mindfulness worksheets",
                "Use mindfulness skills during daily activities"
            ]
        )
        
        interventions["distress_tolerance"] = TherapeuticIntervention(
            intervention_id="distress_tolerance",
            name="Distress Tolerance Skills",
            intervention_type=InterventionType.EMOTIONAL_REGULATION,
            modality=TherapyModality.DBT,
            description="Skills for surviving crisis situations without making them worse",
            objectives=[
                "Learn crisis survival skills",
                "Practice TIPP technique",
                "Develop distraction strategies",
                "Build tolerance for difficult emotions"
            ],
            materials_needed=["Distress tolerance skills sheet", "Crisis survival kit items"],
            estimated_duration=25,
            difficulty_level="intermediate",
            evidence_base="Essential component of DBT with research support",
            instructions="""
1. Introduce TIPP skills: Temperature, Intense exercise, Paced breathing, Paired muscle relaxation
2. Practice ACCEPTS: Activities, Contributing, Comparisons, Emotions, Push away, Thoughts, Sensations
3. Teach self-soothing through five senses
4. Practice improving the moment techniques
5. Discuss pros and cons of tolerating vs. not tolerating distress
6. Create personalized crisis survival kit
            """,
            homework_suggestions=[
                "Practice TIPP when distressed",
                "Use ACCEPTS techniques daily",
                "Create and use crisis survival kit"
            ]
        )
        
        # ACT Interventions
        interventions["cognitive_defusion"] = TherapeuticIntervention(
            intervention_id="cognitive_defusion",
            name="Cognitive Defusion Techniques",
            intervention_type=InterventionType.COGNITIVE_RESTRUCTURING,
            modality=TherapyModality.ACT,
            description="Changing relationship with thoughts rather than content",
            objectives=[
                "Recognize thoughts as mental events",
                "Reduce belief in/attachment to thoughts",
                "Practice defusion techniques",
                "Increase psychological flexibility"
            ],
            materials_needed=["Defusion exercise worksheets"],
            estimated_duration=20,
            difficulty_level="intermediate",
            evidence_base="Core ACT process with research support",
            instructions="""
1. Explain difference between being caught up in thoughts vs. observing them
2. Practice 'I'm having the thought that...' technique
3. Use silly voice or singing techniques for difficult thoughts
4. Practice leaves on a stream or clouds in the sky metaphors
5. Teach thank your mind technique
6. Practice defusion with specific problematic thoughts
            """,
            homework_suggestions=[
                "Practice daily defusion exercises",
                "Notice when caught up in thoughts",
                "Use defusion techniques with worry thoughts"
            ]
        )
        
        interventions["values_clarification"] = TherapeuticIntervention(
            intervention_id="values_clarification",
            name="Values Clarification",
            intervention_type=InterventionType.PSYCHOEDUCATION,
            modality=TherapyModality.ACT,
            description="Identifying personal values to guide behavioral choices",
            objectives=[
                "Identify core personal values",
                "Distinguish values from goals",
                "Assess current value-consistent living",
                "Plan values-based actions"
            ],
            materials_needed=["Values card sort", "Values worksheets", "Life domains chart"],
            estimated_duration=30,
            difficulty_level="beginner",
            evidence_base="Essential ACT component with research support",
            instructions="""
1. Explain difference between values and goals
2. Use values card sort or similar exercise
3. Explore values in different life domains
4. Assess current values-consistent living
5. Identify barriers to values-based action
6. Plan specific values-based behaviors
            """,
            homework_suggestions=[
                "Engage in one values-based action daily",
                "Complete values assessment worksheet",
                "Notice values conflicts in daily life"
            ]
        )
        
        return interventions
    
    def _initialize_session_templates(self) -> Dict[str, List[SessionStructure]]:
        """Initialize session structure templates"""
        
        templates = {}
        
        # Standard CBT session template
        templates["CBT_STANDARD"] = [
            SessionStructure(
                phase=SessionPhase.OPENING,
                duration_minutes=5,
                objectives=["Greet patient", "Brief mood check"],
                interventions=[InterventionType.PSYCHOEDUCATION],
                required=True
            ),
            SessionStructure(
                phase=SessionPhase.CHECK_IN,
                duration_minutes=10,
                objectives=["Review week", "Assess mood and functioning"],
                interventions=[InterventionType.PSYCHOEDUCATION],
                required=True
            ),
            SessionStructure(
                phase=SessionPhase.HOMEWORK_REVIEW,
                duration_minutes=10,
                objectives=["Review homework", "Process learning"],
                interventions=[InterventionType.COGNITIVE_RESTRUCTURING],
                required=False,
                adaptable=True
            ),
            SessionStructure(
                phase=SessionPhase.AGENDA_SETTING,
                duration_minutes=5,
                objectives=["Set session agenda", "Prioritize topics"],
                interventions=[InterventionType.PSYCHOEDUCATION],
                required=True
            ),
            SessionStructure(
                phase=SessionPhase.MAIN_WORK,
                duration_minutes=20,
                objectives=["Address agenda items", "Practice skills"],
                interventions=[InterventionType.COGNITIVE_RESTRUCTURING, InterventionType.BEHAVIORAL_ACTIVATION],
                required=True
            ),
            SessionStructure(
                phase=SessionPhase.HOMEWORK_ASSIGNMENT,
                duration_minutes=5,
                objectives=["Assign homework", "Ensure understanding"],
                interventions=[InterventionType.BEHAVIORAL_ACTIVATION],
                required=True
            ),
            SessionStructure(
                phase=SessionPhase.SUMMARY,
                duration_minutes=5,
                objectives=["Summarize session", "Get feedback"],
                interventions=[InterventionType.PSYCHOEDUCATION],
                required=True
            )
        ]
        
        # DBT skills training session template
        templates["DBT_SKILLS"] = [
            SessionStructure(
                phase=SessionPhase.CHECK_IN,
                duration_minutes=10,
                objectives=["Review diary card", "Assess distress level"],
                interventions=[InterventionType.EMOTIONAL_REGULATION],
                required=True
            ),
            SessionStructure(
                phase=SessionPhase.HOMEWORK_REVIEW,
                duration_minutes=15,
                objectives=["Review skills practice", "Troubleshoot problems"],
                interventions=[InterventionType.SKILLS_TRAINING],
                required=True
            ),
            SessionStructure(
                phase=SessionPhase.MAIN_WORK,
                duration_minutes=20,
                objectives=["Teach new skill", "Practice skill"],
                interventions=[InterventionType.MINDFULNESS, InterventionType.EMOTIONAL_REGULATION],
                required=True
            ),
            SessionStructure(
                phase=SessionPhase.HOMEWORK_ASSIGNMENT,
                duration_minutes=5,
                objectives=["Assign skills practice", "Plan application"],
                interventions=[InterventionType.SKILLS_TRAINING],
                required=True
            )
        ]
        
        return templates
    
    def _initialize_adaptation_rules(self) -> Dict[str, Any]:
        """Initialize protocol adaptation rules"""
        
        return {
            "comorbidity_adaptations": {
                "depression_anxiety": {
                    "modifications": [
                        "Increase anxiety-specific interventions",
                        "Add relaxation training",
                        "Monitor both depression and anxiety symptoms"
                    ],
                    "additional_assessments": ["GAD7", "BAI"]
                },
                "trauma_depression": {
                    "modifications": [
                        "Prioritize stabilization phase",
                        "Add trauma-informed approaches",
                        "Careful pacing of exposure work"
                    ],
                    "additional_assessments": ["PCL5", "DES"]
                }
            },
            "severity_adaptations": {
                "severe_symptoms": {
                    "session_frequency": "twice_weekly",
                    "session_duration": 60,
                    "safety_protocols": "enhanced",
                    "additional_support": "crisis_planning"
                },
                "mild_symptoms": {
                    "session_frequency": "biweekly",
                    "session_duration": 45,
                    "self_directed_components": "increased"
                }
            },
            "demographic_adaptations": {
                "adolescent": {
                    "modifications": [
                        "Shorter session components",
                        "More interactive interventions",
                        "Family involvement when appropriate"
                    ]
                },
                "older_adult": {
                    "modifications": [
                        "Slower pacing",
                        "Cognitive assessment considerations",
                        "Medical factors integration"
                    ]
                }
            }
        }
    
    def get_protocol(self, protocol_id: str) -> Optional[TreatmentProtocol]:
        """Get treatment protocol by ID"""
        return self.protocols.get(protocol_id)
    
    def get_intervention(self, intervention_id: str) -> Optional[TherapeuticIntervention]:
        """Get therapeutic intervention by ID"""
        return self.interventions_library.get(intervention_id)
    
    def list_protocols_by_modality(self, modality: TherapyModality) -> List[str]:
        """List protocols for specific therapy modality"""
        return [pid for pid, protocol in self.protocols.items() 
                if protocol.modality == modality]
    
    def list_protocols_by_condition(self, condition: str) -> List[str]:
        """List protocols that target specific condition"""
        return [pid for pid, protocol in self.protocols.items() 
                if condition.lower() in [c.lower() for c in protocol.target_conditions]]
    
    def recommend_protocol(self, conditions: List[str], 
                          patient_factors: Dict[str, Any]) -> List[Tuple[str, float]]:
        """Recommend treatment protocols based on conditions and patient factors"""
        
        recommendations = []
        
        for protocol_id, protocol in self.protocols.items():
            score = 0.0
            
            # Score based on condition match
            condition_matches = sum(1 for condition in conditions 
                                  if any(target.lower() in condition.lower() 
                                        for target in protocol.target_conditions))
            score += condition_matches * 3.0
            
            # Score based on patient factors
            age = patient_factors.get('age', 30)
            severity = patient_factors.get('severity', 'moderate')
            comorbidities = patient_factors.get('comorbidities', [])
            
            # Age appropriateness
            if protocol.modality == TherapyModality.DBT and 16 <= age <= 25:
                score += 1.0
            elif protocol.modality == TherapyModality.CBT and age >= 18:
                score += 1.0
            
            # Severity considerations
            if severity == 'severe' and protocol.total_sessions >= 16:
                score += 1.0
            elif severity == 'mild' and protocol.total_sessions <= 12:
                score += 0.5
            
            # Comorbidity considerations
            if 'anxiety' in comorbidities and protocol.modality in [TherapyModality.CBT, TherapyModality.ACT]:
                score += 0.5
            if 'trauma' in comorbidities and protocol.modality in [TherapyModality.EMDR, TherapyModality.DBT]:
                score += 0.5
            
            # Evidence level
            if protocol.evidence_level.startswith("Level 1"):
                score += 1.0
            
            if score > 0:
                recommendations.append((protocol_id, score))
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations
    
    def adapt_protocol(self, protocol_id: str, patient_characteristics: Dict[str, Any]) -> ProtocolAdaptation:
        """Adapt protocol based on patient characteristics"""
        
        protocol = self.get_protocol(protocol_id)
        if not protocol:
            raise ValueError(f"Protocol {protocol_id} not found")
        
        adaptations = []
        session_adjustments = {}
        additional_interventions = []
        
        # Age-based adaptations
        age = patient_characteristics.get('age', 30)
        if age < 18:
            adaptations.extend([
                "Shorter session components (30-40 minutes)",
                "More interactive and engaging interventions",
                "Include family/caregiver involvement when appropriate",
                "Use age-appropriate materials and examples"
            ])
            session_adjustments['duration'] = 40
        elif age > 65:
            adaptations.extend([
                "Slower pacing to accommodate processing time",
                "Consider cognitive factors in intervention selection",
                "Include medical factors in treatment planning",
                "Shorter homework assignments"
            ])
            session_adjustments['pacing'] = 'slower'
        
        # Severity-based adaptations
        severity = patient_characteristics.get('severity', 'moderate')
        if severity == 'severe':
            adaptations.extend([
                "Increase session frequency to twice weekly initially",
                "Enhanced safety monitoring and crisis planning",
                "Consider medication consultation",
                "Extended stabilization phase"
            ])
            session_adjustments['frequency'] = 'twice_weekly'
            additional_interventions.extend(['crisis_planning', 'safety_monitoring'])
        elif severity == 'mild':
            adaptations.extend([
                "Consider biweekly sessions after initial phase",
                "Increase self-directed learning components",
                "Shorter overall treatment duration",
                "Group therapy consideration"
            ])
            session_adjustments['frequency'] = 'biweekly_after_phase1'
        
        # Comorbidity adaptations
        comorbidities = patient_characteristics.get('comorbidities', [])
        if 'anxiety' in comorbidities:
            adaptations.append("Add anxiety-specific interventions and assessments")
            additional_interventions.extend(['relaxation_training', 'anxiety_management'])
        if 'trauma' in comorbidities:
            adaptations.append("Include trauma-informed approaches and safety considerations")
            additional_interventions.extend(['trauma_stabilization', 'grounding_techniques'])
        if 'substance_use' in comorbidities:
            adaptations.append("Coordinate with substance abuse treatment")
            additional_interventions.append('substance_use_monitoring')
        
        # Cultural considerations
        cultural_factors = patient_characteristics.get('cultural_factors', [])
        if cultural_factors:
            adaptations.extend([
                "Adapt interventions for cultural relevance",
                "Consider cultural values in treatment planning",
                "Use culturally appropriate examples and metaphors"
            ])
        
        # Learning style adaptations
        learning_style = patient_characteristics.get('learning_style', 'mixed')
        if learning_style == 'visual':
            adaptations.append("Emphasize visual aids, diagrams, and written materials")
        elif learning_style == 'kinesthetic':
            adaptations.append("Include movement-based and experiential interventions")
        elif learning_style == 'auditory':
            adaptations.append("Use verbal processing and audio materials")
        
        adaptation_id = f"{protocol_id}_adapted_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return ProtocolAdaptation(
            adaptation_id=adaptation_id,
            base_protocol_id=protocol_id,
            patient_characteristics=patient_characteristics,
            modifications=adaptations,
            rationale=f"Protocol adapted based on patient age ({age}), severity ({severity}), and other characteristics",
            additional_interventions=additional_interventions,
            session_adjustments=session_adjustments
        )
    
    def generate_session_plan(self, protocol_id: str, session_number: int,
                            patient_progress: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific session plan based on protocol and progress"""
        
        protocol = self.get_protocol(protocol_id)
        if not protocol:
            raise ValueError(f"Protocol {protocol_id} not found")
        
        # Determine treatment phase based on session number
        sessions_per_phase = protocol.total_sessions // len(protocol.treatment_phases)
        current_phase_index = min((session_number - 1) // sessions_per_phase, 
                                len(protocol.treatment_phases) - 1)
        current_phase = protocol.treatment_phases[current_phase_index]
        
        # Get session structure template
        if protocol.modality == TherapyModality.CBT:
            session_template = self.session_templates.get("CBT_STANDARD", [])
        elif protocol.modality == TherapyModality.DBT:
            session_template = self.session_templates.get("DBT_SKILLS", [])
        else:
            session_template = self.session_templates.get("CBT_STANDARD", [])  # Default
        
        # Customize based on session number and progress
        session_plan = {
            'session_number': session_number,
            'protocol_id': protocol_id,
            'treatment_phase': current_phase.value,
            'total_duration': sum(phase.duration_minutes for phase in session_template),
            'phases': [],
            'assessments': [],
            'homework_assignments': [],
            'clinical_notes': f"Session {session_number} of {protocol.total_sessions}"
        }
        
        # Add session phases
        for phase_structure in session_template:
            phase_plan = {
                'phase': phase_structure.phase.value,
                'duration_minutes': phase_structure.duration_minutes,
                'objectives': phase_structure.objectives.copy(),
                'interventions': [i.value for i in phase_structure.interventions],
                'materials_needed': [],
                'notes': ''
            }
            
            # Customize based on session number
            if session_number == 1:
                if phase_structure.phase == SessionPhase.OPENING:
                    phase_plan['objectives'].extend([
                        "Orient to therapy structure",
                        "Establish treatment goals",
                        "Explain confidentiality"
                    ])
                elif phase_structure.phase == SessionPhase.HOMEWORK_REVIEW:
                    phase_plan['objectives'] = ["No homework to review - first session"]
                    phase_plan['duration_minutes'] = 0
            
            # Customize based on treatment phase
            if current_phase == TreatmentPhase.ASSESSMENT:
                if phase_structure.phase == SessionPhase.MAIN_WORK:
                    phase_plan['objectives'].extend([
                        "Complete comprehensive assessment",
                        "Identify treatment targets",
                        "Develop treatment plan"
                    ])
            elif current_phase == TreatmentPhase.TERMINATION:
                if phase_structure.phase == SessionPhase.MAIN_WORK:
                    phase_plan['objectives'].extend([
                        "Review treatment progress",
                        "Plan for maintenance",
                        "Address termination feelings"
                    ])
            
            session_plan['phases'].append(phase_plan)
        
        # Add assessments based on schedule
        for assessment, frequency in protocol.assessment_schedule.items():
            if session_number % frequency == 1:  # Every nth session starting with session 1
                session_plan['assessments'].append({
                    'assessment_type': assessment,
                    'reason': f"Scheduled every {frequency} sessions",
                    'timing': 'beginning_of_session'
                })
        
        # Add phase-specific interventions
        if current_phase == TreatmentPhase.STABILIZATION:
            session_plan['homework_assignments'].extend([
                "Complete mood monitoring daily",
                "Practice safety planning",
                "Use crisis resources if needed"
            ])
        elif current_phase == TreatmentPhase.WORKING:
            session_plan['homework_assignments'].extend([
                "Practice main therapeutic techniques",
                "Complete between-session exercises",
                "Apply skills to real-life situations"
            ])
        elif current_phase == TreatmentPhase.INTEGRATION:
            session_plan['homework_assignments'].extend([
                "Continue practicing key skills",
                "Plan for challenging situations",
                "Prepare for reduced session frequency"
            ])
        
        return session_plan
    
    def track_protocol_adherence(self, protocol_id: str, completed_sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Track adherence to treatment protocol"""
        
        protocol = self.get_protocol(protocol_id)
        if not protocol:
            raise ValueError(f"Protocol {protocol_id} not found")
        
        adherence_report = {
            'protocol_id': protocol_id,
            'total_planned_sessions': protocol.total_sessions,
            'completed_sessions': len(completed_sessions),
            'adherence_percentage': 0.0,
            'missed_components': [],
            'completed_interventions': [],
            'assessment_compliance': {},
            'recommendations': []
        }
        
        # Calculate basic adherence
        if protocol.total_sessions > 0:
            adherence_report['adherence_percentage'] = (
                len(completed_sessions) / protocol.total_sessions * 100
            )
        
        # Track intervention completion
        planned_interventions = set(protocol.interventions)
        completed_interventions = set()
        
        for session in completed_sessions:
            session_interventions = session.get('interventions_used', [])
            completed_interventions.update(session_interventions)
        
        adherence_report['completed_interventions'] = list(completed_interventions)
        adherence_report['missed_components'] = list(
            planned_interventions - completed_interventions
        )
        
        # Track assessment compliance
        for assessment, frequency in protocol.assessment_schedule.items():
            expected_count = len(completed_sessions) // frequency
            actual_count = sum(1 for session in completed_sessions 
                             if assessment in session.get('assessments_completed', []))
            
            adherence_report['assessment_compliance'][assessment] = {
                'expected': expected_count,
                'actual': actual_count,
                'compliance_rate': actual_count / max(expected_count, 1) * 100
            }
        
        # Generate recommendations
        if adherence_report['adherence_percentage'] < 80:
            adherence_report['recommendations'].append(
                "Consider addressing barriers to session attendance"
            )
        
        if len(adherence_report['missed_components']) > 2:
            adherence_report['recommendations'].append(
                "Review missed interventions and plan to incorporate in remaining sessions"
            )
        
        for assessment, compliance in adherence_report['assessment_compliance'].items():
            if compliance['compliance_rate'] < 75:
                adherence_report['recommendations'].append(
                    f"Improve {assessment} assessment completion - current rate: {compliance['compliance_rate']:.1f}%"
                )
        
        return adherence_report
    
    def generate_protocol_summary(self, protocol_id: str) -> str:
        """Generate human-readable protocol summary"""
        
        protocol = self.get_protocol(protocol_id)
        if not protocol:
            return f"Protocol {protocol_id} not found"
        
        summary_sections = []
        
        # Header
        summary_sections.append(f"TREATMENT PROTOCOL: {protocol.name}")
        summary_sections.append(f"Protocol ID: {protocol_id}")
        summary_sections.append(f"Modality: {protocol.modality.value.replace('_', ' ').title()}")
        summary_sections.append("")
        
        # Target conditions
        summary_sections.append("TARGET CONDITIONS:")
        for condition in protocol.target_conditions:
            summary_sections.append(f"  • {condition}")
        summary_sections.append("")
        
        # Treatment structure
        summary_sections.append("TREATMENT STRUCTURE:")
        summary_sections.append(f"  Total Sessions: {protocol.total_sessions}")
        summary_sections.append(f"  Session Frequency: {protocol.session_frequency}")
        summary_sections.append(f"  Treatment Phases: {len(protocol.treatment_phases)}")
        for phase in protocol.treatment_phases:
            summary_sections.append(f"    - {phase.value.replace('_', ' ').title()}")
        summary_sections.append("")
        
        # Key interventions
        summary_sections.append("KEY INTERVENTIONS:")
        for intervention_id in protocol.interventions:
            intervention = self.get_intervention(intervention_id)
            if intervention:
                summary_sections.append(f"  • {intervention.name}")
            else:
                summary_sections.append(f"  • {intervention_id}")
        summary_sections.append("")
        
        # Assessment schedule
        summary_sections.append("ASSESSMENT SCHEDULE:")
        for assessment, frequency in protocol.assessment_schedule.items():
            summary_sections.append(f"  • {assessment}: Every {frequency} session(s)")
        summary_sections.append("")
        
        # Contraindications
        if protocol.contraindications:
            summary_sections.append("CONTRAINDICATIONS:")
            for contraindication in protocol.contraindications:
                summary_sections.append(f"  • {contraindication}")
            summary_sections.append("")
        
        # Evidence base
        summary_sections.append(f"EVIDENCE LEVEL: {protocol.evidence_level}")
        
        # References
        if protocol.references:
            summary_sections.append("")
            summary_sections.append("KEY REFERENCES:")
            for ref in protocol.references:
                summary_sections.append(f"  • {ref}")
        
        return "\n".join(summary_sections)


# Example usage and testing
if __name__ == "__main__":
    # Initialize therapy protocol manager
    protocol_manager = TherapyProtocolManager()
    
    print("=== THERAPY PROTOCOLS SYSTEM DEMONSTRATION ===\n")
    
    # List available protocols
    print("Available Treatment Protocols:")
    for protocol_id in protocol_manager.protocols.keys():
        protocol = protocol_manager.get_protocol(protocol_id)
        print(f"  • {protocol_id}: {protocol.name}")
    print()
    
    # Demonstrate protocol recommendation
    print("=== PROTOCOL RECOMMENDATION DEMONSTRATION ===")
    patient_conditions = ["Major Depressive Disorder", "Generalized Anxiety Disorder"]
    patient_factors = {
        'age': 32,
        'severity': 'moderate',
        'comorbidities': ['anxiety'],
        'learning_style': 'visual'
    }
    
    recommendations = protocol_manager.recommend_protocol(patient_conditions, patient_factors)
    print("Recommended protocols for patient with depression and anxiety:")
    for protocol_id, score in recommendations:
        protocol = protocol_manager.get_protocol(protocol_id)
        print(f"  {protocol_id}: {protocol.name} (Score: {score:.1f})")
    print()
    
    # Demonstrate protocol adaptation
    print("=== PROTOCOL ADAPTATION DEMONSTRATION ===")
    best_protocol = recommendations[0][0]
    adaptation = protocol_manager.adapt_protocol(best_protocol, patient_factors)
    
    print(f"Adaptations for {best_protocol}:")
    print(f"Patient characteristics: {patient_factors}")
    print("Modifications:")
    for mod in adaptation.modifications:
        print(f"  • {mod}")
    print(f"Additional interventions: {adaptation.additional_interventions}")
    print(f"Session adjustments: {adaptation.session_adjustments}")
    print()
    
    # Demonstrate session planning
    print("=== SESSION PLANNING DEMONSTRATION ===")
    session_plan = protocol_manager.generate_session_plan(
        best_protocol, 
        session_number=3,
        patient_progress={'mood_improvement': 'moderate', 'homework_completion': 'good'}
    )
    
    print(f"Session Plan for Session {session_plan['session_number']}:")
    print(f"Treatment Phase: {session_plan['treatment_phase']}")
    print(f"Total Duration: {session_plan['total_duration']} minutes")
    print("Session Phases:")
    for phase in session_plan['phases']:
        print(f"  {phase['phase']} ({phase['duration_minutes']} min): {phase['objectives']}")
    
    if session_plan['assessments']:
        print("Scheduled Assessments:")
        for assessment in session_plan['assessments']:
            print(f"  • {assessment['assessment_type']}: {assessment['reason']}")
    
    print("Homework Assignments:")
    for homework in session_plan['homework_assignments']:
        print(f"  • {homework}")
    print()
    
    # Demonstrate protocol summary
    print("=== PROTOCOL SUMMARY DEMONSTRATION ===")
    summary = protocol_manager.generate_protocol_summary("CBT_DEPRESSION")
    print(summary)
    print()
    
    # Demonstrate intervention details
    print("=== INTERVENTION DETAILS DEMONSTRATION ===")
    intervention = protocol_manager.get_intervention("cognitive_restructuring_basic")
    if intervention:
        print(f"Intervention: {intervention.name}")
        print(f"Type: {intervention.intervention_type.value}")
        print(f"Duration: {intervention.estimated_duration} minutes")
        print(f"Difficulty: {intervention.difficulty_level}")
        print("Objectives:")
        for obj in intervention.objectives:
            print(f"  • {obj}")
        print("Homework Suggestions:")
        for hw in intervention.homework_suggestions:
            print(f"  • {hw}")
    
    print("\n" + "="*60)
    print("Therapy protocols system ready for clinical implementation!")
    print("Evidence-based protocols with structured interventions and adaptations.")
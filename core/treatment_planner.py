"""
Treatment Planner Module

Handles treatment planning, goal setting, protocol selection, and treatment plan adaptation.
Implements evidence-based treatment planning with SMART goals and progress monitoring.
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, asdict
import json

from config.therapy_protocols import TherapyModality, TreatmentPhase, THERAPY_PROTOCOLS
from config.assessment_templates import AssessmentType, CLINICAL_CUTOFFS


class GoalStatus(Enum):
    """Goal achievement status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ACHIEVED = "achieved"
    PARTIALLY_ACHIEVED = "partially_achieved"
    DISCONTINUED = "discontinued"
    MODIFIED = "modified"


class GoalPriority(Enum):
    """Goal priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TreatmentPlanType(Enum):
    """Types of treatment plans"""
    INITIAL = "initial"
    REVISED = "revised"
    UPDATED = "updated"
    TERMINATION = "termination"


@dataclass
class TreatmentGoal:
    """SMART treatment goal structure"""
    goal_id: str
    specific: str  # Specific: What exactly will be accomplished?
    measurable: str  # Measurable: How will progress be measured?
    achievable: str  # Achievable: Is this realistic given current circumstances?
    relevant: str  # Relevant: How does this relate to treatment needs?
    time_bound: str  # Time-bound: When will this be accomplished?
    
    priority: GoalPriority
    status: GoalStatus
    target_sessions: int
    current_progress: float  # 0.0 to 1.0
    interventions: List[str]
    success_criteria: List[str]
    barriers: List[str]
    
    created_date: datetime
    last_updated: datetime
    achieved_date: Optional[datetime] = None
    notes: str = ""


@dataclass
class TreatmentPlan:
    """Comprehensive treatment plan"""
    plan_id: str
    patient_id: str
    plan_type: TreatmentPlanType
    modality: TherapyModality
    current_phase: TreatmentPhase
    
    primary_diagnosis: str
    secondary_diagnoses: List[str]
    treatment_goals: List[TreatmentGoal]
    
    estimated_sessions: int
    session_frequency: str  # "weekly", "biweekly", "monthly"
    estimated_duration: str  # "3-6 months", "6-12 months"
    
    risk_factors: List[str]
    protective_factors: List[str]
    treatment_barriers: List[str]
    
    milestones: Dict[int, str]  # session_number: milestone_description
    phase_transitions: Dict[TreatmentPhase, Dict[str, Any]]
    
    created_date: datetime
    last_updated: datetime
    created_by: str = "AI Therapist"
    notes: str = ""


class TreatmentPlanner:
    """
    Manages treatment planning, goal setting, and treatment plan adaptation.
    """
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize treatment planning tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Treatment plans table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS treatment_plans (
                    plan_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    plan_type TEXT NOT NULL,
                    modality TEXT NOT NULL,
                    current_phase TEXT NOT NULL,
                    primary_diagnosis TEXT NOT NULL,
                    secondary_diagnoses TEXT,
                    estimated_sessions INTEGER,
                    session_frequency TEXT,
                    estimated_duration TEXT,
                    risk_factors TEXT,
                    protective_factors TEXT,
                    treatment_barriers TEXT,
                    milestones TEXT,
                    phase_transitions TEXT,
                    created_date TIMESTAMP,
                    last_updated TIMESTAMP,
                    created_by TEXT,
                    notes TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            # Treatment goals table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS treatment_goals (
                    goal_id TEXT PRIMARY KEY,
                    plan_id TEXT NOT NULL,
                    specific TEXT NOT NULL,
                    measurable TEXT NOT NULL,
                    achievable TEXT NOT NULL,
                    relevant TEXT NOT NULL,
                    time_bound TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL,
                    target_sessions INTEGER,
                    current_progress REAL DEFAULT 0.0,
                    interventions TEXT,
                    success_criteria TEXT,
                    barriers TEXT,
                    created_date TIMESTAMP,
                    last_updated TIMESTAMP,
                    achieved_date TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (plan_id) REFERENCES treatment_plans (plan_id)
                )
            """)
            
            # Goal progress tracking table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS goal_progress (
                    progress_id TEXT PRIMARY KEY,
                    goal_id TEXT NOT NULL,
                    session_id TEXT,
                    progress_value REAL NOT NULL,
                    progress_notes TEXT,
                    recorded_date TIMESTAMP,
                    recorded_by TEXT,
                    FOREIGN KEY (goal_id) REFERENCES treatment_goals (goal_id)
                )
            """)
            
            conn.commit()
    
    def create_treatment_plan(
        self, 
        patient_id: str, 
        assessment_results: Dict[str, Any],
        clinical_presentation: Dict[str, Any]
    ) -> TreatmentPlan:
        """
        Create initial treatment plan based on assessment results
        """
        plan_id = f"plan_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Determine primary modality based on assessment
        modality = self._select_treatment_modality(assessment_results, clinical_presentation)
        
        # Determine primary diagnosis and treatment targets
        primary_diagnosis = self._determine_primary_diagnosis(assessment_results)
        secondary_diagnoses = self._identify_secondary_diagnoses(assessment_results)
        
        # Generate SMART goals based on assessment
        treatment_goals = self._generate_smart_goals(
            assessment_results, 
            clinical_presentation,
            modality
        )
        
        # Estimate treatment parameters
        estimated_sessions, duration = self._estimate_treatment_parameters(
            modality, 
            assessment_results
        )
        
        # Identify risk and protective factors
        risk_factors = self._identify_risk_factors(assessment_results, clinical_presentation)
        protective_factors = self._identify_protective_factors(clinical_presentation)
        treatment_barriers = self._identify_treatment_barriers(clinical_presentation)
        
        # Create treatment milestones
        milestones = self._create_treatment_milestones(modality, estimated_sessions)
        
        # Define phase transitions
        phase_transitions = self._define_phase_transitions(modality)
        
        treatment_plan = TreatmentPlan(
            plan_id=plan_id,
            patient_id=patient_id,
            plan_type=TreatmentPlanType.INITIAL,
            modality=modality,
            current_phase=TreatmentPhase.ASSESSMENT,
            primary_diagnosis=primary_diagnosis,
            secondary_diagnoses=secondary_diagnoses,
            treatment_goals=treatment_goals,
            estimated_sessions=estimated_sessions,
            session_frequency="weekly",
            estimated_duration=duration,
            risk_factors=risk_factors,
            protective_factors=protective_factors,
            treatment_barriers=treatment_barriers,
            milestones=milestones,
            phase_transitions=phase_transitions,
            created_date=datetime.now(),
            last_updated=datetime.now()
        )
        
        self._save_treatment_plan(treatment_plan)
        return treatment_plan
    
    def _select_treatment_modality(
        self, 
        assessment_results: Dict[str, Any], 
        clinical_presentation: Dict[str, Any]
    ) -> TherapyModality:
        """
        Select appropriate treatment modality based on assessment
        """
        scores = {}
        
        # Check depression scores
        if 'phq9' in assessment_results:
            phq9_score = assessment_results['phq9'].get('total_score', 0)
            if phq9_score >= 15:  # Severe depression
                scores['CBT'] = scores.get('CBT', 0) + 3
                scores['Psychodynamic'] = scores.get('Psychodynamic', 0) + 2
        
        # Check anxiety scores
        if 'gad7' in assessment_results:
            gad7_score = assessment_results['gad7'].get('total_score', 0)
            if gad7_score >= 10:  # Moderate to severe anxiety
                scores['CBT'] = scores.get('CBT', 0) + 3
                scores['DBT'] = scores.get('DBT', 0) + 1
        
        # Check PTSD scores
        if 'pcl5' in assessment_results:
            pcl5_score = assessment_results['pcl5'].get('total_score', 0)
            if pcl5_score >= 33:  # Probable PTSD
                scores['CBT'] = scores.get('CBT', 0) + 2
                scores['ACT'] = scores.get('ACT', 0) + 2
        
        # Consider clinical presentation factors
        presentation = clinical_presentation.get('symptoms', [])
        if 'emotional_dysregulation' in presentation:
            scores['DBT'] = scores.get('DBT', 0) + 3
        if 'avoidance_behaviors' in presentation:
            scores['ACT'] = scores.get('ACT', 0) + 2
        if 'relationship_patterns' in presentation:
            scores['Psychodynamic'] = scores.get('Psychodynamic', 0) + 2
        
        # Default to CBT if no clear preference
        if not scores:
            return TherapyModality.CBT
        
        # Return highest scoring modality
        best_modality = max(scores, key=scores.get)
        return TherapyModality(best_modality.upper())
    
    def _determine_primary_diagnosis(self, assessment_results: Dict[str, Any]) -> str:
        """Determine primary diagnosis from assessment results"""
        diagnoses = []
        
        if 'phq9' in assessment_results:
            phq9_score = assessment_results['phq9'].get('total_score', 0)
            if phq9_score >= CLINICAL_CUTOFFS['PHQ9']['severe']:
                diagnoses.append(("Major Depressive Disorder, Severe", phq9_score))
            elif phq9_score >= CLINICAL_CUTOFFS['PHQ9']['moderate']:
                diagnoses.append(("Major Depressive Disorder, Moderate", phq9_score))
            elif phq9_score >= CLINICAL_CUTOFFS['PHQ9']['mild']:
                diagnoses.append(("Major Depressive Disorder, Mild", phq9_score))
        
        if 'gad7' in assessment_results:
            gad7_score = assessment_results['gad7'].get('total_score', 0)
            if gad7_score >= CLINICAL_CUTOFFS['GAD7']['severe']:
                diagnoses.append(("Generalized Anxiety Disorder, Severe", gad7_score))
            elif gad7_score >= CLINICAL_CUTOFFS['GAD7']['moderate']:
                diagnoses.append(("Generalized Anxiety Disorder, Moderate", gad7_score))
        
        if 'pcl5' in assessment_results:
            pcl5_score = assessment_results['pcl5'].get('total_score', 0)
            if pcl5_score >= CLINICAL_CUTOFFS['PCL5']['probable_ptsd']:
                diagnoses.append(("Post-Traumatic Stress Disorder", pcl5_score))
        
        if not diagnoses:
            return "Adjustment Disorder with Mixed Anxiety and Depressed Mood"
        
        # Return diagnosis with highest severity score
        return max(diagnoses, key=lambda x: x[1])[0]
    
    def _identify_secondary_diagnoses(self, assessment_results: Dict[str, Any]) -> List[str]:
        """Identify secondary diagnoses"""
        secondary = []
        
        # Logic to identify comorbid conditions
        if 'phq9' in assessment_results and 'gad7' in assessment_results:
            phq9_score = assessment_results['phq9'].get('total_score', 0)
            gad7_score = assessment_results['gad7'].get('total_score', 0)
            
            if phq9_score >= 10 and gad7_score >= 10:
                secondary.append("Mixed Anxiety-Depression")
        
        return secondary
    
    def _generate_smart_goals(
        self, 
        assessment_results: Dict[str, Any],
        clinical_presentation: Dict[str, Any],
        modality: TherapyModality
    ) -> List[TreatmentGoal]:
        """Generate SMART treatment goals"""
        goals = []
        current_time = datetime.now()
        
        # Depression-related goals
        if 'phq9' in assessment_results:
            phq9_score = assessment_results['phq9'].get('total_score', 0)
            if phq9_score >= 10:
                goal = TreatmentGoal(
                    goal_id=f"goal_depression_{current_time.strftime('%Y%m%d_%H%M%S')}",
                    specific="Reduce depression symptoms to minimal level",
                    measurable=f"Decrease PHQ-9 score from {phq9_score} to below 5",
                    achievable="Through weekly therapy and homework practice",
                    relevant="Depression significantly impacts daily functioning",
                    time_bound="Within 12-16 therapy sessions",
                    priority=GoalPriority.HIGH,
                    status=GoalStatus.NOT_STARTED,
                    target_sessions=16,
                    current_progress=0.0,
                    interventions=["Cognitive restructuring", "Behavioral activation", "Mood monitoring"],
                    success_criteria=[
                        "PHQ-9 score below 5",
                        "Improved daily functioning",
                        "Increased engagement in activities"
                    ],
                    barriers=["Low motivation", "Negative thinking patterns"],
                    created_date=current_time,
                    last_updated=current_time
                )
                goals.append(goal)
        
        # Anxiety-related goals
        if 'gad7' in assessment_results:
            gad7_score = assessment_results['gad7'].get('total_score', 0)
            if gad7_score >= 10:
                goal = TreatmentGoal(
                    goal_id=f"goal_anxiety_{current_time.strftime('%Y%m%d_%H%M%S')}_1",
                    specific="Develop effective anxiety management skills",
                    measurable=f"Reduce GAD-7 score from {gad7_score} to below 8",
                    achievable="Through relaxation training and exposure exercises",
                    relevant="Anxiety interferes with work and relationships",
                    time_bound="Within 10-12 therapy sessions",
                    priority=GoalPriority.HIGH,
                    status=GoalStatus.NOT_STARTED,
                    target_sessions=12,
                    current_progress=0.0,
                    interventions=["Progressive muscle relaxation", "Grounding techniques", "Gradual exposure"],
                    success_criteria=[
                        "GAD-7 score below 8",
                        "Use coping skills independently",
                        "Reduced avoidance behaviors"
                    ],
                    barriers=["Fear of anxiety symptoms", "Avoidance patterns"],
                    created_date=current_time,
                    last_updated=current_time
                )
                goals.append(goal)
        
        # Functional goals
        functional_goal = TreatmentGoal(
            goal_id=f"goal_functional_{current_time.strftime('%Y%m%d_%H%M%S')}",
            specific="Improve overall daily functioning and quality of life",
            measurable="Score 7 or higher on Outcome Rating Scale for 3 consecutive sessions",
            achievable="Through consistent therapy attendance and homework completion",
            relevant="Functioning impacts all life domains",
            time_bound="By session 20",
            priority=GoalPriority.MEDIUM,
            status=GoalStatus.NOT_STARTED,
            target_sessions=20,
            current_progress=0.0,
            interventions=["Activity scheduling", "Problem-solving skills", "Self-care planning"],
            success_criteria=[
                "Consistent ORS scores ≥ 7",
                "Improved work/school performance",
                "Better relationship satisfaction"
            ],
            barriers=["Time management difficulties", "Perfectionism"],
            created_date=current_time,
            last_updated=current_time
        )
        goals.append(functional_goal)
        
        return goals
    
    def _estimate_treatment_parameters(
        self, 
        modality: TherapyModality,
        assessment_results: Dict[str, Any]
    ) -> Tuple[int, str]:
        """Estimate number of sessions and treatment duration"""
        base_sessions = {
            TherapyModality.CBT: 16,
            TherapyModality.DBT: 24,
            TherapyModality.ACT: 12,
            TherapyModality.PSYCHODYNAMIC: 20
        }
        
        sessions = base_sessions.get(modality, 16)
        
        # Adjust based on severity
        severity_multiplier = 1.0
        if 'phq9' in assessment_results:
            phq9_score = assessment_results['phq9'].get('total_score', 0)
            if phq9_score >= 20:
                severity_multiplier += 0.5
            elif phq9_score >= 15:
                severity_multiplier += 0.25
        
        if 'gad7' in assessment_results:
            gad7_score = assessment_results['gad7'].get('total_score', 0)
            if gad7_score >= 15:
                severity_multiplier += 0.25
        
        sessions = int(sessions * severity_multiplier)
        
        # Determine duration
        weeks = sessions  # Assuming weekly sessions
        if weeks <= 12:
            duration = "3 months"
        elif weeks <= 24:
            duration = "6 months"
        elif weeks <= 48:
            duration = "12 months"
        else:
            duration = "12+ months"
        
        return sessions, duration
    
    def _identify_risk_factors(
        self, 
        assessment_results: Dict[str, Any],
        clinical_presentation: Dict[str, Any]
    ) -> List[str]:
        """Identify treatment risk factors"""
        risk_factors = []
        
        # Suicide risk
        if assessment_results.get('suicide_risk', {}).get('level') in ['moderate', 'high']:
            risk_factors.append("Suicide risk")
        
        # Substance use
        if clinical_presentation.get('substance_use', False):
            risk_factors.append("Substance use concerns")
        
        # Trauma history
        if clinical_presentation.get('trauma_history', False):
            risk_factors.append("Trauma history")
        
        # Social isolation
        if clinical_presentation.get('social_support') == 'poor':
            risk_factors.append("Limited social support")
        
        return risk_factors
    
    def _identify_protective_factors(self, clinical_presentation: Dict[str, Any]) -> List[str]:
        """Identify protective factors"""
        protective_factors = []
        
        if clinical_presentation.get('social_support') in ['good', 'excellent']:
            protective_factors.append("Strong social support system")
        
        if clinical_presentation.get('motivation', 'low') in ['moderate', 'high']:
            protective_factors.append("High motivation for change")
        
        if clinical_presentation.get('insight', 'poor') in ['good', 'excellent']:
            protective_factors.append("Good insight into problems")
        
        return protective_factors
    
    def _identify_treatment_barriers(self, clinical_presentation: Dict[str, Any]) -> List[str]:
        """Identify potential treatment barriers"""
        barriers = []
        
        if clinical_presentation.get('transportation') == 'difficult':
            barriers.append("Transportation challenges")
        
        if clinical_presentation.get('financial_concerns', False):
            barriers.append("Financial constraints")
        
        if clinical_presentation.get('work_schedule') == 'inflexible':
            barriers.append("Work schedule conflicts")
        
        return barriers
    
    def _create_treatment_milestones(self, modality: TherapyModality, total_sessions: int) -> Dict[int, str]:
        """Create treatment milestones"""
        milestones = {}
        
        # Universal milestones
        milestones[1] = "Complete intake and initial assessment"
        milestones[3] = "Establish therapeutic alliance and treatment goals"
        milestones[total_sessions // 4] = "Complete stabilization phase"
        milestones[total_sessions // 2] = "Mid-treatment progress review"
        milestones[int(total_sessions * 0.75)] = "Begin integration and termination planning"
        milestones[total_sessions] = "Complete treatment and develop maintenance plan"
        
        # Modality-specific milestones
        if modality == TherapyModality.CBT:
            milestones[6] = "Master thought record technique"
            milestones[10] = "Demonstrate behavioral activation skills"
        elif modality == TherapyModality.DBT:
            milestones[8] = "Complete mindfulness skills module"
            milestones[16] = "Complete emotion regulation skills module"
        
        return milestones
    
    def _define_phase_transitions(self, modality: TherapyModality) -> Dict[TreatmentPhase, Dict[str, Any]]:
        """Define criteria for phase transitions"""
        transitions = {
            TreatmentPhase.STABILIZATION: {
                "criteria": [
                    "Crisis risk stabilized",
                    "Basic coping skills established",
                    "Therapeutic alliance formed"
                ],
                "typical_session": 4
            },
            TreatmentPhase.WORKING: {
                "criteria": [
                    "Treatment goals refined",
                    "Core skills developed",
                    "Symptom reduction evident"
                ],
                "typical_session": 8
            },
            TreatmentPhase.INTEGRATION: {
                "criteria": [
                    "Significant progress on goals",
                    "Skills generalization demonstrated",
                    "Increased independence"
                ],
                "typical_session": None  # Varies by treatment length
            },
            TreatmentPhase.TERMINATION: {
                "criteria": [
                    "Treatment goals substantially met",
                    "Relapse prevention plan developed",
                    "Patient ready for independence"
                ],
                "typical_session": None
            }
        }
        
        return transitions
    
    def _save_treatment_plan(self, plan: TreatmentPlan):
        """Save treatment plan to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Save treatment plan
            cursor.execute("""
                INSERT INTO treatment_plans (
                    plan_id, patient_id, plan_type, modality, current_phase,
                    primary_diagnosis, secondary_diagnoses, estimated_sessions,
                    session_frequency, estimated_duration, risk_factors,
                    protective_factors, treatment_barriers, milestones,
                    phase_transitions, created_date, last_updated, created_by, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plan.plan_id, plan.patient_id, plan.plan_type.value,
                plan.modality.value, plan.current_phase.value,
                plan.primary_diagnosis, json.dumps(plan.secondary_diagnoses),
                plan.estimated_sessions, plan.session_frequency,
                plan.estimated_duration, json.dumps(plan.risk_factors),
                json.dumps(plan.protective_factors), json.dumps(plan.treatment_barriers),
                json.dumps(plan.milestones), json.dumps(plan.phase_transitions, default=str),
                plan.created_date, plan.last_updated, plan.created_by, plan.notes
            ))
            
            # Save treatment goals
            for goal in plan.treatment_goals:
                cursor.execute("""
                    INSERT INTO treatment_goals (
                        goal_id, plan_id, specific, measurable, achievable,
                        relevant, time_bound, priority, status, target_sessions,
                        current_progress, interventions, success_criteria, barriers,
                        created_date, last_updated, achieved_date, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    goal.goal_id, plan.plan_id, goal.specific, goal.measurable,
                    goal.achievable, goal.relevant, goal.time_bound,
                    goal.priority.value, goal.status.value, goal.target_sessions,
                    goal.current_progress, json.dumps(goal.interventions),
                    json.dumps(goal.success_criteria), json.dumps(goal.barriers),
                    goal.created_date, goal.last_updated, goal.achieved_date, goal.notes
                ))
            
            conn.commit()
    
    def update_goal_progress(
        self, 
        goal_id: str, 
        progress_value: float,
        session_id: Optional[str] = None,
        notes: str = ""
    ):
        """Update progress on a specific goal"""
        progress_id = f"progress_{goal_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Record progress entry
            cursor.execute("""
                INSERT INTO goal_progress (
                    progress_id, goal_id, session_id, progress_value,
                    progress_notes, recorded_date, recorded_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                progress_id, goal_id, session_id, progress_value,
                notes, datetime.now(), "AI Therapist"
            ))
            
            # Update goal current progress
            cursor.execute("""
                UPDATE treatment_goals 
                SET current_progress = ?, last_updated = ?
                WHERE goal_id = ?
            """, (progress_value, datetime.now(), goal_id))
            
            # Check if goal is achieved
            if progress_value >= 1.0:
                cursor.execute("""
                    UPDATE treatment_goals 
                    SET status = ?, achieved_date = ?
                    WHERE goal_id = ?
                """, (GoalStatus.ACHIEVED.value, datetime.now(), goal_id))
            elif progress_value > 0.0:
                cursor.execute("""
                    UPDATE treatment_goals 
                    SET status = ?
                    WHERE goal_id = ? AND status = ?
                """, (GoalStatus.IN_PROGRESS.value, goal_id, GoalStatus.NOT_STARTED.value))
            
            conn.commit()
    
    def get_treatment_plan(self, patient_id: str) -> Optional[TreatmentPlan]:
        """Retrieve active treatment plan for patient"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get treatment plan
            cursor.execute("""
                SELECT * FROM treatment_plans 
                WHERE patient_id = ? AND is_active = TRUE
                ORDER BY created_date DESC LIMIT 1
            """, (patient_id,))
            
            plan_data = cursor.fetchone()
            if not plan_data:
                return None
            
            # Get treatment goals
            cursor.execute("""
                SELECT * FROM treatment_goals 
                WHERE plan_id = ?
                ORDER BY priority, created_date
            """, (plan_data[0],))  # plan_id is first column
            
            goals_data = cursor.fetchall()
            
            return self._reconstruct_treatment_plan(plan_data, goals_data)
    
    def _reconstruct_treatment_plan(self, plan_data, goals_data) -> TreatmentPlan:
        """Reconstruct TreatmentPlan object from database data"""
        # Map database columns to TreatmentPlan fields
        goals = []
        for goal_row in goals_data:
            goal = TreatmentGoal(
                goal_id=goal_row[0],
                specific=goal_row[2],
                measurable=goal_row[3],
                achievable=goal_row[4],
                relevant=goal_row[5],
                time_bound=goal_row[6],
                priority=GoalPriority(goal_row[7]),
                status=GoalStatus(goal_row[8]),
                target_sessions=goal_row[9],
                current_progress=goal_row[10],
                interventions=json.loads(goal_row[11] or '[]'),
                success_criteria=json.loads(goal_row[12] or '[]'),
                barriers=json.loads(goal_row[13] or '[]'),
                created_date=datetime.fromisoformat(goal_row[14]),
                last_updated=datetime.fromisoformat(goal_row[15]),
                achieved_date=datetime.fromisoformat(goal_row[16]) if goal_row[16] else None,
                notes=goal_row[17] or ""
            )
            goals.append(goal)
        
        return TreatmentPlan(
            plan_id=plan_data[0],
            patient_id=plan_data[1],
            plan_type=TreatmentPlanType(plan_data[2]),
            modality=TherapyModality(plan_data[3]),
            current_phase=TreatmentPhase(plan_data[4]),
            primary_diagnosis=plan_data[5],
            secondary_diagnoses=json.loads(plan_data[6] or '[]'),
            treatment_goals=goals,
            estimated_sessions=plan_data[7],
            session_frequency=plan_data[8],
            estimated_duration=plan_data[9],
            risk_factors=json.loads(plan_data[10] or '[]'),
            protective_factors=json.loads(plan_data[11] or '[]'),
            treatment_barriers=json.loads(plan_data[12] or '[]'),
            milestones=json.loads(plan_data[13] or '{}'),
            phase_transitions=json.loads(plan_data[14] or '{}'),
            created_date=datetime.fromisoformat(plan_data[15]),
            last_updated=datetime.fromisoformat(plan_data[16]),
            created_by=plan_data[17] or "AI Therapist",
            notes=plan_data[18] or ""
        )
    
    def update_treatment_phase(self, plan_id: str, new_phase: TreatmentPhase) -> bool:
        """Update treatment phase and adjust plan accordingly"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE treatment_plans 
                SET current_phase = ?, last_updated = ?
                WHERE plan_id = ?
            """, (new_phase.value, datetime.now(), plan_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
    
    def revise_treatment_plan(
        self, 
        plan_id: str, 
        revision_reason: str,
        new_goals: Optional[List[TreatmentGoal]] = None,
        modality_change: Optional[TherapyModality] = None
    ) -> TreatmentPlan:
        """Create revised treatment plan"""
        # Get current plan
        current_plan = self.get_treatment_plan_by_id(plan_id)
        if not current_plan:
            raise ValueError(f"Treatment plan {plan_id} not found")
        
        # Deactivate current plan
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE treatment_plans 
                SET is_active = FALSE 
                WHERE plan_id = ?
            """, (plan_id,))
            conn.commit()
        
        # Create new revised plan
        new_plan_id = f"plan_{current_plan.patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_rev"
        
        revised_plan = TreatmentPlan(
            plan_id=new_plan_id,
            patient_id=current_plan.patient_id,
            plan_type=TreatmentPlanType.REVISED,
            modality=modality_change or current_plan.modality,
            current_phase=current_plan.current_phase,
            primary_diagnosis=current_plan.primary_diagnosis,
            secondary_diagnoses=current_plan.secondary_diagnoses,
            treatment_goals=new_goals or current_plan.treatment_goals,
            estimated_sessions=current_plan.estimated_sessions,
            session_frequency=current_plan.session_frequency,
            estimated_duration=current_plan.estimated_duration,
            risk_factors=current_plan.risk_factors,
            protective_factors=current_plan.protective_factors,
            treatment_barriers=current_plan.treatment_barriers,
            milestones=current_plan.milestones,
            phase_transitions=current_plan.phase_transitions,
            created_date=datetime.now(),
            last_updated=datetime.now(),
            notes=f"Revised plan. Reason: {revision_reason}"
        )
        
        self._save_treatment_plan(revised_plan)
        return revised_plan
    
    def get_treatment_plan_by_id(self, plan_id: str) -> Optional[TreatmentPlan]:
        """Get treatment plan by specific ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM treatment_plans WHERE plan_id = ?
            """, (plan_id,))
            
            plan_data = cursor.fetchone()
            if not plan_data:
                return None
            
            cursor.execute("""
                SELECT * FROM treatment_goals 
                WHERE plan_id = ?
                ORDER BY priority, created_date
            """, (plan_id,))
            
            goals_data = cursor.fetchall()
            
            return self._reconstruct_treatment_plan(plan_data, goals_data)
    
    def assess_treatment_progress(self, patient_id: str) -> Dict[str, Any]:
        """Assess overall treatment progress"""
        plan = self.get_treatment_plan(patient_id)
        if not plan:
            return {"error": "No active treatment plan found"}
        
        total_goals = len(plan.treatment_goals)
        achieved_goals = len([g for g in plan.treatment_goals if g.status == GoalStatus.ACHIEVED])
        in_progress_goals = len([g for g in plan.treatment_goals if g.status == GoalStatus.IN_PROGRESS])
        
        # Calculate overall progress
        total_progress = sum(goal.current_progress for goal in plan.treatment_goals)
        overall_progress = total_progress / total_goals if total_goals > 0 else 0.0
        
        # Get session count
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM sessions 
                WHERE patient_id = ? AND status = 'completed'
            """, (patient_id,))
            completed_sessions = cursor.fetchone()[0]
        
        progress_summary = {
            "overall_progress": overall_progress,
            "completed_sessions": completed_sessions,
            "estimated_sessions": plan.estimated_sessions,
            "total_goals": total_goals,
            "achieved_goals": achieved_goals,
            "in_progress_goals": in_progress_goals,
            "current_phase": plan.current_phase.value,
            "goals_summary": [
                {
                    "goal_id": goal.goal_id,
                    "specific": goal.specific,
                    "progress": goal.current_progress,
                    "status": goal.status.value,
                    "priority": goal.priority.value
                }
                for goal in plan.treatment_goals
            ],
            "recommendations": self._generate_progress_recommendations(plan, completed_sessions)
        }
        
        return progress_summary
    
    def _generate_progress_recommendations(
        self, 
        plan: TreatmentPlan, 
        completed_sessions: int
    ) -> List[str]:
        """Generate recommendations based on treatment progress"""
        recommendations = []
        
        # Session progress recommendations
        progress_ratio = completed_sessions / plan.estimated_sessions if plan.estimated_sessions > 0 else 0
        
        if progress_ratio > 0.75:
            recommendations.append("Consider termination planning and relapse prevention")
        elif progress_ratio > 0.5:
            recommendations.append("Begin integration phase and skill consolidation")
        elif progress_ratio > 0.25:
            recommendations.append("Focus on core therapeutic work and skill building")
        else:
            recommendations.append("Continue stabilization and goal clarification")
        
        # Goal progress recommendations
        achieved_count = len([g for g in plan.treatment_goals if g.status == GoalStatus.ACHIEVED])
        total_goals = len(plan.treatment_goals)
        
        if achieved_count == 0 and completed_sessions > 8:
            recommendations.append("Review and potentially revise treatment goals")
        elif achieved_count / total_goals > 0.7:
            recommendations.append("Consider developing new goals or termination planning")
        
        # Phase transition recommendations
        if plan.current_phase == TreatmentPhase.ASSESSMENT and completed_sessions > 3:
            recommendations.append("Consider transitioning to stabilization phase")
        elif plan.current_phase == TreatmentPhase.STABILIZATION and completed_sessions > 6:
            recommendations.append("Assess readiness for working phase")
        
        return recommendations
    
    def create_termination_plan(self, patient_id: str) -> Dict[str, Any]:
        """Create termination and maintenance plan"""
        plan = self.get_treatment_plan(patient_id)
        if not plan:
            return {"error": "No active treatment plan found"}
        
        # Assess readiness for termination
        readiness_criteria = [
            "Primary treatment goals achieved",
            "Symptoms significantly reduced",
            "Coping skills demonstrated",
            "Functional improvement evident",
            "Patient expresses readiness"
        ]
        
        # Generate maintenance recommendations
        maintenance_plan = {
            "relapse_prevention": [
                "Continue using learned coping skills",
                "Maintain regular self-monitoring",
                "Engage in preventive activities",
                "Recognize early warning signs"
            ],
            "follow_up_schedule": [
                "1-month check-in session",
                "3-month follow-up",
                "6-month assessment",
                "Annual review"
            ],
            "emergency_plan": [
                "Contact crisis hotline if needed",
                "Return to therapy if symptoms worsen",
                "Use learned crisis management skills",
                "Reach out to support system"
            ],
            "skill_maintenance": [
                f"Continue practicing {plan.modality.value} techniques",
                "Regular homework/exercises",
                "Self-assessment tools",
                "Booster sessions as needed"
            ]
        }
        
        return {
            "readiness_criteria": readiness_criteria,
            "maintenance_plan": maintenance_plan,
            "achieved_goals": [
                goal.specific for goal in plan.treatment_goals 
                if goal.status == GoalStatus.ACHIEVED
            ],
            "areas_for_continued_growth": [
                goal.specific for goal in plan.treatment_goals 
                if goal.status in [GoalStatus.IN_PROGRESS, GoalStatus.PARTIALLY_ACHIEVED]
            ]
        }
    
    def generate_treatment_summary(self, patient_id: str) -> Dict[str, Any]:
        """Generate comprehensive treatment summary"""
        plan = self.get_treatment_plan(patient_id)
        if not plan:
            return {"error": "No active treatment plan found"}
        
        # Get all sessions
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT session_id, session_date, session_type, notes
                FROM sessions 
                WHERE patient_id = ? AND status = 'completed'
                ORDER BY session_date
            """, (patient_id,))
            sessions = cursor.fetchall()
        
        # Get goal progress history
        goal_progress = {}
        for goal in plan.treatment_goals:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT recorded_date, progress_value, progress_notes
                    FROM goal_progress
                    WHERE goal_id = ?
                    ORDER BY recorded_date
                """, (goal.goal_id,))
                goal_progress[goal.goal_id] = cursor.fetchall()
        
        summary = {
            "treatment_overview": {
                "modality": plan.modality.value,
                "primary_diagnosis": plan.primary_diagnosis,
                "total_sessions": len(sessions),
                "treatment_duration": f"{plan.created_date.strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}",
                "current_phase": plan.current_phase.value
            },
            "goals_achieved": [
                {
                    "goal": goal.specific,
                    "progress": goal.current_progress,
                    "status": goal.status.value
                }
                for goal in plan.treatment_goals
            ],
            "key_interventions": list(set([
                intervention 
                for goal in plan.treatment_goals 
                for intervention in goal.interventions
            ])),
            "progress_highlights": self._extract_progress_highlights(goal_progress),
            "outcomes": self._calculate_treatment_outcomes(plan),
            "recommendations": self._generate_treatment_recommendations(plan)
        }
        
        return summary
    
    def _extract_progress_highlights(self, goal_progress: Dict[str, List]) -> List[str]:
        """Extract key progress highlights"""
        highlights = []
        
        for goal_id, progress_entries in goal_progress.items():
            if progress_entries:
                first_entry = progress_entries[0]
                last_entry = progress_entries[-1]
                
                if len(progress_entries) > 1:
                    improvement = last_entry[1] - first_entry[1]  # progress_value difference
                    if improvement > 0.3:
                        highlights.append(f"Significant progress on goal {goal_id}")
        
        return highlights
    
    def _calculate_treatment_outcomes(self, plan: TreatmentPlan) -> Dict[str, Any]:
        """Calculate treatment outcomes"""
        outcomes = {
            "goal_achievement_rate": 0.0,
            "average_goal_progress": 0.0,
            "treatment_completion_rate": 0.0
        }
        
        if plan.treatment_goals:
            achieved_goals = len([g for g in plan.treatment_goals if g.status == GoalStatus.ACHIEVED])
            outcomes["goal_achievement_rate"] = achieved_goals / len(plan.treatment_goals)
            
            total_progress = sum(goal.current_progress for goal in plan.treatment_goals)
            outcomes["average_goal_progress"] = total_progress / len(plan.treatment_goals)
        
        # Calculate completion rate based on sessions
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM sessions 
                WHERE patient_id = ? AND status = 'completed'
            """, (plan.patient_id,))
            completed_sessions = cursor.fetchone()[0]
        
        if plan.estimated_sessions > 0:
            outcomes["treatment_completion_rate"] = min(1.0, completed_sessions / plan.estimated_sessions)
        
        return outcomes
    
    def _generate_treatment_recommendations(self, plan: TreatmentPlan) -> List[str]:
        """Generate final treatment recommendations"""
        recommendations = []
        
        # Based on goal achievement
        achieved_goals = len([g for g in plan.treatment_goals if g.status == GoalStatus.ACHIEVED])
        total_goals = len(plan.treatment_goals)
        
        if achieved_goals / total_goals >= 0.8:
            recommendations.append("Treatment goals substantially achieved")
            recommendations.append("Patient ready for treatment termination")
        elif achieved_goals / total_goals >= 0.5:
            recommendations.append("Good progress made on treatment goals")
            recommendations.append("Consider continuation or termination based on patient preference")
        else:
            recommendations.append("Limited goal achievement")
            recommendations.append("Consider treatment plan revision or extended therapy")
        
        # Maintenance recommendations
        recommendations.extend([
            f"Continue {plan.modality.value} self-help techniques",
            "Regular self-monitoring and skill practice",
            "Follow-up sessions as needed"
        ])
        
        return recommendations


# Example usage and testing functions
def example_usage():
    """Example of how to use the TreatmentPlanner"""
    planner = TreatmentPlanner()
    
    # Example assessment results
    assessment_results = {
        'phq9': {'total_score': 18, 'severity': 'severe'},
        'gad7': {'total_score': 14, 'severity': 'severe'},
        'suicide_risk': {'level': 'low'}
    }
    
    clinical_presentation = {
        'symptoms': ['depression', 'anxiety', 'sleep_problems'],
        'social_support': 'good',
        'motivation': 'high',
        'insight': 'good'
    }
    
    # Create treatment plan
    plan = planner.create_treatment_plan(
        patient_id="patient_001",
        assessment_results=assessment_results,
        clinical_presentation=clinical_presentation
    )
    
    print(f"Created treatment plan: {plan.plan_id}")
    print(f"Modality: {plan.modality.value}")
    print(f"Estimated sessions: {plan.estimated_sessions}")
    print(f"Goals: {len(plan.treatment_goals)}")
    
    # Update goal progress
    if plan.treatment_goals:
        planner.update_goal_progress(
            goal_id=plan.treatment_goals[0].goal_id,
            progress_value=0.3,
            notes="Good progress in session 5"
        )
    
    # Assess progress
    progress = planner.assess_treatment_progress("patient_001")
    print(f"Overall progress: {progress.get('overall_progress', 0):.2f}")


if __name__ == "__main__":
    example_usage()
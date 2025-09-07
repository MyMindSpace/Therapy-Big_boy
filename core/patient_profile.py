"""
Patient Profile Module
Comprehensive patient data and profile management for AI therapy system
Handles patient demographics, clinical history, preferences, and treatment data
"""

import sqlite3
import json
import uuid
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, date, timedelta
from enum import Enum
import hashlib
import logging
from pathlib import Path


class Gender(Enum):
    """Gender options"""
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"
    TRANSGENDER_MALE = "transgender_male"
    TRANSGENDER_FEMALE = "transgender_female"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"
    OTHER = "other"


class MaritalStatus(Enum):
    """Marital status options"""
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    SEPARATED = "separated"
    WIDOWED = "widowed"
    DOMESTIC_PARTNER = "domestic_partner"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class EducationLevel(Enum):
    """Education level options"""
    LESS_THAN_HIGH_SCHOOL = "less_than_high_school"
    HIGH_SCHOOL = "high_school"
    SOME_COLLEGE = "some_college"
    ASSOCIATES_DEGREE = "associates_degree"
    BACHELORS_DEGREE = "bachelors_degree"
    MASTERS_DEGREE = "masters_degree"
    DOCTORAL_DEGREE = "doctoral_degree"
    PROFESSIONAL_DEGREE = "professional_degree"


class EmploymentStatus(Enum):
    """Employment status options"""
    EMPLOYED_FULL_TIME = "employed_full_time"
    EMPLOYED_PART_TIME = "employed_part_time"
    UNEMPLOYED = "unemployed"
    STUDENT = "student"
    RETIRED = "retired"
    DISABLED = "disabled"
    HOMEMAKER = "homemaker"
    SELF_EMPLOYED = "self_employed"


class RiskLevel(Enum):
    """Risk assessment levels"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class TreatmentStatus(Enum):
    """Treatment status options"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPLETED = "completed"
    TERMINATED = "terminated"
    ON_HOLD = "on_hold"


@dataclass
class Demographics:
    """Patient demographic information"""
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    preferred_pronouns: str = ""
    phone_number: str = ""
    email: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    country: str = "USA"
    emergency_contact_name: str = ""
    emergency_contact_phone: str = ""
    emergency_contact_relationship: str = ""


@dataclass
class ClinicalInformation:
    """Clinical information and history"""
    primary_diagnosis: Optional[str] = None
    secondary_diagnoses: List[str] = field(default_factory=list)
    current_medications: List[Dict[str, str]] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    medical_conditions: List[str] = field(default_factory=list)
    psychiatric_history: List[Dict[str, Any]] = field(default_factory=list)
    substance_use_history: List[Dict[str, Any]] = field(default_factory=list)
    trauma_history: List[Dict[str, Any]] = field(default_factory=list)
    family_mental_health_history: List[Dict[str, str]] = field(default_factory=list)
    hospitalization_history: List[Dict[str, Any]] = field(default_factory=list)
    suicide_attempts: List[Dict[str, Any]] = field(default_factory=list)
    current_risk_level: RiskLevel = RiskLevel.LOW
    last_risk_assessment: Optional[datetime] = None


@dataclass
class SocialHistory:
    """Social and background information"""
    marital_status: MaritalStatus = MaritalStatus.SINGLE
    children: List[Dict[str, Any]] = field(default_factory=list)
    education_level: EducationLevel = EducationLevel.HIGH_SCHOOL
    employment_status: EmploymentStatus = EmploymentStatus.EMPLOYED_FULL_TIME
    occupation: str = ""
    living_situation: str = ""
    support_system: List[str] = field(default_factory=list)
    cultural_background: List[str] = field(default_factory=list)
    religious_spiritual_preferences: str = ""
    language_preferences: List[str] = field(default_factory=list)
    accessibility_needs: List[str] = field(default_factory=list)


@dataclass
class TreatmentPreferences:
    """Patient treatment preferences and goals"""
    preferred_therapy_modality: Optional[str] = None
    therapy_goals: List[str] = field(default_factory=list)
    treatment_motivations: List[str] = field(default_factory=list)
    preferred_communication_style: str = "collaborative"
    session_frequency_preference: str = "weekly"
    homework_preferences: Dict[str, Any] = field(default_factory=dict)
    trigger_warnings: List[str] = field(default_factory=list)
    coping_strategies: List[str] = field(default_factory=list)
    previous_therapy_experiences: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AssessmentHistory:
    """History of assessments and their results"""
    assessments: List[Dict[str, Any]] = field(default_factory=list)
    latest_scores: Dict[str, float] = field(default_factory=dict)
    score_trends: Dict[str, List[Tuple[datetime, float]]] = field(default_factory=dict)
    last_assessment_date: Optional[datetime] = None


@dataclass
class TreatmentProgress:
    """Treatment progress tracking"""
    treatment_start_date: Optional[date] = None
    current_treatment_phase: str = "assessment"
    total_sessions: int = 0
    sessions_attended: int = 0
    sessions_missed: int = 0
    homework_completion_rate: float = 0.0
    goal_progress: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    milestones_achieved: List[Dict[str, Any]] = field(default_factory=list)
    treatment_modifications: List[Dict[str, Any]] = field(default_factory=list)
    last_session_date: Optional[date] = None
    next_session_date: Optional[date] = None


@dataclass
class PatientProfile:
    """Complete patient profile"""
    patient_id: str
    demographics: Demographics
    clinical_info: ClinicalInformation
    social_history: SocialHistory
    treatment_preferences: TreatmentPreferences
    assessment_history: AssessmentHistory
    treatment_progress: TreatmentProgress
    treatment_status: TreatmentStatus = TreatmentStatus.ACTIVE
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    notes: List[Dict[str, str]] = field(default_factory=list)
    consent_status: Dict[str, bool] = field(default_factory=dict)
    privacy_settings: Dict[str, Any] = field(default_factory=dict)


class PatientProfileManager:
    """Manages patient profiles with database integration"""
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._ensure_database_exists()
        self._create_tables()
    
    def _ensure_database_exists(self):
        """Ensure database directory and file exist"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def _create_tables(self):
        """Create database tables for patient profiles"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Patient profiles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patient_profiles (
                    patient_id TEXT PRIMARY KEY,
                    demographics TEXT NOT NULL,
                    clinical_info TEXT NOT NULL,
                    social_history TEXT NOT NULL,
                    treatment_preferences TEXT NOT NULL,
                    assessment_history TEXT NOT NULL,
                    treatment_progress TEXT NOT NULL,
                    treatment_status TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    notes TEXT,
                    consent_status TEXT,
                    privacy_settings TEXT
                )
            """)
            
            # Assessment results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS assessment_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    assessment_type TEXT NOT NULL,
                    assessment_date TEXT NOT NULL,
                    scores TEXT NOT NULL,
                    interpretation TEXT,
                    administered_by TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patient_profiles (patient_id)
                )
            """)
            
            # Session records table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    session_date TEXT NOT NULL,
                    session_type TEXT NOT NULL,
                    duration_minutes INTEGER,
                    interventions_used TEXT,
                    homework_assigned TEXT,
                    session_notes TEXT,
                    mood_rating INTEGER,
                    progress_notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patient_profiles (patient_id)
                )
            """)
            
            # Goals and objectives table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS treatment_goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    goal_text TEXT NOT NULL,
                    target_date TEXT,
                    status TEXT NOT NULL,
                    progress_percentage REAL DEFAULT 0.0,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patient_profiles (patient_id)
                )
            """)
            
            # Crisis and safety plans table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS safety_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    plan_type TEXT NOT NULL,
                    warning_signs TEXT,
                    coping_strategies TEXT,
                    support_contacts TEXT,
                    professional_contacts TEXT,
                    environmental_safety TEXT,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (patient_id) REFERENCES patient_profiles (patient_id)
                )
            """)
            
            conn.commit()
    
    def create_patient_profile(self, demographics: Demographics, 
                             clinical_info: Optional[ClinicalInformation] = None,
                             social_history: Optional[SocialHistory] = None,
                             treatment_preferences: Optional[TreatmentPreferences] = None) -> PatientProfile:
        """Create new patient profile"""
        
        # Generate unique patient ID
        patient_id = self._generate_patient_id(demographics)
        
        # Initialize optional components with defaults
        clinical_info = clinical_info or ClinicalInformation()
        social_history = social_history or SocialHistory()
        treatment_preferences = treatment_preferences or TreatmentPreferences()
        assessment_history = AssessmentHistory()
        treatment_progress = TreatmentProgress()
        
        # Set default consent and privacy settings
        consent_status = {
            "treatment_consent": True,
            "data_sharing_consent": False,
            "research_participation_consent": False,
            "emergency_contact_consent": True
        }
        
        privacy_settings = {
            "share_with_emergency_contact": True,
            "allow_session_recordings": False,
            "data_retention_years": 7,
            "anonymous_data_use": False
        }
        
        profile = PatientProfile(
            patient_id=patient_id,
            demographics=demographics,
            clinical_info=clinical_info,
            social_history=social_history,
            treatment_preferences=treatment_preferences,
            assessment_history=assessment_history,
            treatment_progress=treatment_progress,
            consent_status=consent_status,
            privacy_settings=privacy_settings
        )
        
        # Save to database
        self._save_profile_to_db(profile)
        
        self.logger.info(f"Created new patient profile: {patient_id}")
        return profile
    
    def _generate_patient_id(self, demographics: Demographics) -> str:
        """Generate unique patient ID"""
        
        # Create hash from demographic info for uniqueness
        demographic_string = f"{demographics.first_name}{demographics.last_name}{demographics.date_of_birth}"
        hash_object = hashlib.sha256(demographic_string.encode())
        hash_hex = hash_object.hexdigest()[:8]
        
        # Combine with timestamp for additional uniqueness
        timestamp = datetime.now().strftime("%Y%m%d")
        patient_id = f"PT_{timestamp}_{hash_hex.upper()}"
        
        # Ensure uniqueness in database
        counter = 1
        base_id = patient_id
        while self.get_patient_profile(patient_id) is not None:
            patient_id = f"{base_id}_{counter:02d}"
            counter += 1
        
        return patient_id
    
    def _save_profile_to_db(self, profile: PatientProfile):
        """Save patient profile to database"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO patient_profiles (
                    patient_id, demographics, clinical_info, social_history,
                    treatment_preferences, assessment_history, treatment_progress,
                    treatment_status, created_date, last_updated, notes,
                    consent_status, privacy_settings
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                profile.patient_id,
                json.dumps(asdict(profile.demographics), default=str),
                json.dumps(asdict(profile.clinical_info), default=str),
                json.dumps(asdict(profile.social_history), default=str),
                json.dumps(asdict(profile.treatment_preferences), default=str),
                json.dumps(asdict(profile.assessment_history), default=str),
                json.dumps(asdict(profile.treatment_progress), default=str),
                profile.treatment_status.value,
                profile.created_date.isoformat(),
                profile.last_updated.isoformat(),
                json.dumps(profile.notes),
                json.dumps(profile.consent_status),
                json.dumps(profile.privacy_settings, default=str)
            ))
            
            conn.commit()
    
    def get_patient_profile(self, patient_id: str) -> Optional[PatientProfile]:
        """Retrieve patient profile by ID"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM patient_profiles WHERE patient_id = ?
            """, (patient_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return self._row_to_profile(row)
    
    def _row_to_profile(self, row: Tuple) -> PatientProfile:
        """Convert database row to PatientProfile object"""
        
        (patient_id, demographics_json, clinical_info_json, social_history_json,
         treatment_preferences_json, assessment_history_json, treatment_progress_json,
         treatment_status, created_date, last_updated, notes_json,
         consent_status_json, privacy_settings_json) = row
        
        # Parse JSON data
        demographics_data = json.loads(demographics_json)
        clinical_info_data = json.loads(clinical_info_json)
        social_history_data = json.loads(social_history_json)
        treatment_preferences_data = json.loads(treatment_preferences_json)
        assessment_history_data = json.loads(assessment_history_json)
        treatment_progress_data = json.loads(treatment_progress_json)
        
        # Convert date strings back to date objects
        demographics_data['date_of_birth'] = datetime.fromisoformat(demographics_data['date_of_birth']).date()
        
        # Convert enum values
        demographics_data['gender'] = Gender(demographics_data['gender'])
        social_history_data['marital_status'] = MaritalStatus(social_history_data['marital_status'])
        social_history_data['education_level'] = EducationLevel(social_history_data['education_level'])
        social_history_data['employment_status'] = EmploymentStatus(social_history_data['employment_status'])
        clinical_info_data['current_risk_level'] = RiskLevel(clinical_info_data['current_risk_level'])
        
        # Convert datetime strings
        if clinical_info_data['last_risk_assessment']:
            clinical_info_data['last_risk_assessment'] = datetime.fromisoformat(clinical_info_data['last_risk_assessment'])
        if assessment_history_data['last_assessment_date']:
            assessment_history_data['last_assessment_date'] = datetime.fromisoformat(assessment_history_data['last_assessment_date'])
        
        # Convert date strings in treatment progress
        if treatment_progress_data['treatment_start_date']:
            treatment_progress_data['treatment_start_date'] = datetime.fromisoformat(treatment_progress_data['treatment_start_date']).date()
        if treatment_progress_data['last_session_date']:
            treatment_progress_data['last_session_date'] = datetime.fromisoformat(treatment_progress_data['last_session_date']).date()
        if treatment_progress_data['next_session_date']:
            treatment_progress_data['next_session_date'] = datetime.fromisoformat(treatment_progress_data['next_session_date']).date()
        
        # Create profile object
        return PatientProfile(
            patient_id=patient_id,
            demographics=Demographics(**demographics_data),
            clinical_info=ClinicalInformation(**clinical_info_data),
            social_history=SocialHistory(**social_history_data),
            treatment_preferences=TreatmentPreferences(**treatment_preferences_data),
            assessment_history=AssessmentHistory(**assessment_history_data),
            treatment_progress=TreatmentProgress(**treatment_progress_data),
            treatment_status=TreatmentStatus(treatment_status),
            created_date=datetime.fromisoformat(created_date),
            last_updated=datetime.fromisoformat(last_updated),
            notes=json.loads(notes_json) if notes_json else [],
            consent_status=json.loads(consent_status_json) if consent_status_json else {},
            privacy_settings=json.loads(privacy_settings_json) if privacy_settings_json else {}
        )
    
    def update_patient_profile(self, profile: PatientProfile) -> bool:
        """Update existing patient profile"""
        
        profile.last_updated = datetime.now()
        
        try:
            self._save_profile_to_db(profile)
            self.logger.info(f"Updated patient profile: {profile.patient_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update patient profile {profile.patient_id}: {e}")
            return False
    
    def add_assessment_result(self, patient_id: str, assessment_type: str,
                            scores: Dict[str, float], interpretation: str = "",
                            administered_by: str = "AI_System") -> bool:
        """Add assessment result to patient profile"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO assessment_results (
                        patient_id, assessment_type, assessment_date, scores,
                        interpretation, administered_by
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    patient_id,
                    assessment_type,
                    datetime.now().isoformat(),
                    json.dumps(scores),
                    interpretation,
                    administered_by
                ))
                
                conn.commit()
            
            # Update profile assessment history
            profile = self.get_patient_profile(patient_id)
            if profile:
                # Add to assessment history
                assessment_record = {
                    'assessment_type': assessment_type,
                    'date': datetime.now(),
                    'scores': scores,
                    'interpretation': interpretation
                }
                profile.assessment_history.assessments.append(assessment_record)
                
                # Update latest scores
                for scale, score in scores.items():
                    profile.assessment_history.latest_scores[f"{assessment_type}_{scale}"] = score
                
                # Update score trends
                for scale, score in scores.items():
                    trend_key = f"{assessment_type}_{scale}"
                    if trend_key not in profile.assessment_history.score_trends:
                        profile.assessment_history.score_trends[trend_key] = []
                    profile.assessment_history.score_trends[trend_key].append((datetime.now(), score))
                
                profile.assessment_history.last_assessment_date = datetime.now()
                
                self.update_patient_profile(profile)
            
            self.logger.info(f"Added assessment result for patient {patient_id}: {assessment_type}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add assessment result: {e}")
            return False
    
    def add_session_record(self, patient_id: str, session_data: Dict[str, Any]) -> bool:
        """Add session record to patient profile"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO session_records (
                        patient_id, session_id, session_date, session_type,
                        duration_minutes, interventions_used, homework_assigned,
                        session_notes, mood_rating, progress_notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    patient_id,
                    session_data.get('session_id'),
                    session_data.get('session_date', datetime.now().isoformat()),
                    session_data.get('session_type', 'therapy'),
                    session_data.get('duration_minutes', 50),
                    json.dumps(session_data.get('interventions_used', [])),
                    json.dumps(session_data.get('homework_assigned', [])),
                    session_data.get('session_notes', ''),
                    session_data.get('mood_rating'),
                    session_data.get('progress_notes', '')
                ))
                
                conn.commit()
            
            # Update profile treatment progress
            profile = self.get_patient_profile(patient_id)
            if profile:
                profile.treatment_progress.sessions_attended += 1
                profile.treatment_progress.total_sessions += 1
                profile.treatment_progress.last_session_date = datetime.now().date()
                
                # Update homework completion rate if applicable
                if 'homework_completion' in session_data:
                    current_rate = profile.treatment_progress.homework_completion_rate
                    total_sessions = profile.treatment_progress.sessions_attended
                    new_completion = session_data['homework_completion']
                    
                    # Running average calculation
                    profile.treatment_progress.homework_completion_rate = (
                        (current_rate * (total_sessions - 1) + new_completion) / total_sessions
                    )
                
                self.update_patient_profile(profile)
            
            self.logger.info(f"Added session record for patient {patient_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add session record: {e}")
            return False
    
    def update_treatment_goals(self, patient_id: str, goals: List[Dict[str, Any]]) -> bool:
        """Update treatment goals for patient"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clear existing goals
                cursor.execute("DELETE FROM treatment_goals WHERE patient_id = ?", (patient_id,))
                
                # Add new goals
                for goal in goals:
                    cursor.execute("""
                        INSERT INTO treatment_goals (
                            patient_id, goal_text, target_date, status,
                            progress_percentage, created_date, last_updated, notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        patient_id,
                        goal['goal_text'],
                        goal.get('target_date'),
                        goal.get('status', 'active'),
                        goal.get('progress_percentage', 0.0),
                        datetime.now().isoformat(),
                        datetime.now().isoformat(),
                        goal.get('notes', '')
                    ))
                
                conn.commit()
            
            # Update profile
            profile = self.get_patient_profile(patient_id)
            if profile:
                profile.treatment_preferences.therapy_goals = [goal['goal_text'] for goal in goals]
                
                # Update goal progress tracking
                for goal in goals:
                    goal_text = goal['goal_text']
                    profile.treatment_progress.goal_progress[goal_text] = {
                        'status': goal.get('status', 'active'),
                        'progress_percentage': goal.get('progress_percentage', 0.0),
                        'target_date': goal.get('target_date'),
                        'last_updated': datetime.now()
                    }
                
                self.update_patient_profile(profile)
            
            self.logger.info(f"Updated treatment goals for patient {patient_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update treatment goals: {e}")
            return False
    
    def update_risk_assessment(self, patient_id: str, risk_level: RiskLevel,
                             risk_factors: List[str], safety_plan: Optional[Dict[str, Any]] = None) -> bool:
        """Update patient risk assessment"""
        
        try:
            profile = self.get_patient_profile(patient_id)
            if not profile:
                return False
            
            # Update clinical info
            profile.clinical_info.current_risk_level = risk_level
            profile.clinical_info.last_risk_assessment = datetime.now()
            
            # Add risk assessment note
            risk_note = {
                'date': datetime.now().isoformat(),
                'type': 'risk_assessment',
                'content': f"Risk level updated to {risk_level.value}. Factors: {', '.join(risk_factors)}"
            }
            profile.notes.append(risk_note)
            
            # Save safety plan if provided
            if safety_plan:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    cursor.execute("""
                        INSERT INTO safety_plans (
                            patient_id, plan_type, warning_signs, coping_strategies,
                            support_contacts, professional_contacts, environmental_safety,
                            created_date, last_updated
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        patient_id,
                        safety_plan.get('plan_type', 'crisis'),
                        json.dumps(safety_plan.get('warning_signs', [])),
                        json.dumps(safety_plan.get('coping_strategies', [])),
                        json.dumps(safety_plan.get('support_contacts', [])),
                        json.dumps(safety_plan.get('professional_contacts', [])),
                        json.dumps(safety_plan.get('environmental_safety', [])),
                        datetime.now().isoformat(),
                        datetime.now().isoformat()
                    ))
                    
                    conn.commit()
            
            self.update_patient_profile(profile)
            self.logger.info(f"Updated risk assessment for patient {patient_id}: {risk_level.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update risk assessment: {e}")
            return False
    
    def get_patient_summary(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive patient summary"""
        
        profile = self.get_patient_profile(patient_id)
        if not profile:
            return None
        
        # Calculate age
        today = date.today()
        age = today.year - profile.demographics.date_of_birth.year
        if today < profile.demographics.date_of_birth.replace(year=today.year):
            age -= 1
        
        # Get latest assessment scores
        latest_assessments = {}
        for key, score in profile.assessment_history.latest_scores.items():
            assessment_type = key.split('_')[0]
            if assessment_type not in latest_assessments:
                latest_assessments[assessment_type] = {}
            scale_name = '_'.join(key.split('_')[1:])
            latest_assessments[assessment_type][scale_name] = score
        
        summary = {
            'patient_info': {
                'patient_id': profile.patient_id,
                'name': f"{profile.demographics.first_name} {profile.demographics.last_name}",
                'age': age,
                'gender': profile.demographics.gender.value,
                'preferred_pronouns': profile.demographics.preferred_pronouns
            },
            'clinical_status': {
                'primary_diagnosis': profile.clinical_info.primary_diagnosis,
                'current_risk_level': profile.clinical_info.current_risk_level.value,
                'treatment_status': profile.treatment_status.value,
                'treatment_phase': profile.treatment_progress.current_treatment_phase
            },
            'treatment_summary': {
                'therapy_modality': profile.treatment_preferences.preferred_therapy_modality,
                'total_sessions': profile.treatment_progress.total_sessions,
                'sessions_attended': profile.treatment_progress.sessions_attended,
                'attendance_rate': (
                    profile.treatment_progress.sessions_attended / max(profile.treatment_progress.total_sessions, 1) * 100
                ),
                'homework_completion_rate': profile.treatment_progress.homework_completion_rate * 100,
                'active_goals': profile.treatment_preferences.therapy_goals
            },
            'recent_assessments': latest_assessments,
            'last_session': profile.treatment_progress.last_session_date.isoformat() if profile.treatment_progress.last_session_date else None,
            'next_session': profile.treatment_progress.next_session_date.isoformat() if profile.treatment_progress.next_session_date else None,
            'emergency_contact': {
                'name': profile.demographics.emergency_contact_name,
                'phone': profile.demographics.emergency_contact_phone,
                'relationship': profile.demographics.emergency_contact_relationship
            }
        }
        
        return summary
    
    def search_patients(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search patients based on criteria"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Build dynamic query based on criteria
            query = "SELECT patient_id FROM patient_profiles WHERE 1=1"
            params = []
            
            if 'treatment_status' in criteria:
                query += " AND treatment_status = ?"
                params.append(criteria['treatment_status'])
            
            if 'risk_level' in criteria:
                query += " AND clinical_info LIKE ?"
                params.append(f'%"current_risk_level": "{criteria["risk_level"]}"%')
            
            if 'age_range' in criteria:
                min_age, max_age = criteria['age_range']
                # Calculate birth date range
                today = date.today()
                max_birth_date = today.replace(year=today.year - min_age)
                min_birth_date = today.replace(year=today.year - max_age)
                query += " AND demographics LIKE ? AND demographics LIKE ?"
                params.extend([f'%"date_of_birth": "{min_birth_date.isoformat()}"%', 
                              f'%"date_of_birth": "{max_birth_date.isoformat()}"%'])
            
            cursor.execute(query, params)
            patient_ids = [row[0] for row in cursor.fetchall()]
        
        # Get summaries for found patients
        results = []
        for patient_id in patient_ids:
            summary = self.get_patient_summary(patient_id)
            if summary:
                results.append(summary)
        
        return results
    
    def get_patients_requiring_attention(self) -> List[Dict[str, Any]]:
        """Get patients requiring immediate attention"""
        
        attention_list = []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get all active patients
            cursor.execute("""
                SELECT patient_id FROM patient_profiles 
                WHERE treatment_status = 'active'
            """)
            
            active_patients = [row[0] for row in cursor.fetchall()]
        
        for patient_id in active_patients:
            profile = self.get_patient_profile(patient_id)
            if not profile:
                continue
            
            reasons = []
            priority = "normal"
            
            # Check risk level
            if profile.clinical_info.current_risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                reasons.append(f"High risk level: {profile.clinical_info.current_risk_level.value}")
                priority = "urgent"
            
            # Check overdue sessions
            if profile.treatment_progress.next_session_date:
                if profile.treatment_progress.next_session_date < date.today():
                    days_overdue = (date.today() - profile.treatment_progress.next_session_date).days
                    reasons.append(f"Session overdue by {days_overdue} days")
                    if days_overdue > 14:
                        priority = "high"
            
            # Check missed sessions
            if profile.treatment_progress.sessions_missed > 3:
                reasons.append(f"Multiple missed sessions: {profile.treatment_progress.sessions_missed}")
                priority = "high"
            
            # Check overdue risk assessment
            if profile.clinical_info.last_risk_assessment:
                days_since_assessment = (datetime.now() - profile.clinical_info.last_risk_assessment).days
                if days_since_assessment > 30:
                    reasons.append(f"Risk assessment overdue: {days_since_assessment} days")
                    priority = "high"
            
            # Check low homework completion
            if profile.treatment_progress.homework_completion_rate < 0.3:
                reasons.append(f"Low homework completion: {profile.treatment_progress.homework_completion_rate:.1%}")
            
            if reasons:
                attention_list.append({
                    'patient_id': patient_id,
                    'patient_name': f"{profile.demographics.first_name} {profile.demographics.last_name}",
                    'priority': priority,
                    'reasons': reasons,
                    'last_session': profile.treatment_progress.last_session_date,
                    'risk_level': profile.clinical_info.current_risk_level.value
                })
        
        # Sort by priority
        priority_order = {"urgent": 0, "high": 1, "normal": 2}
        attention_list.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return attention_list
    
    def get_treatment_statistics(self, patient_id: str) -> Dict[str, Any]:
        """Get comprehensive treatment statistics for patient"""
        
        profile = self.get_patient_profile(patient_id)
        if not profile:
            return {}
        
        # Calculate treatment duration
        treatment_duration = None
        if profile.treatment_progress.treatment_start_date:
            duration_days = (date.today() - profile.treatment_progress.treatment_start_date).days
            treatment_duration = {
                'days': duration_days,
                'weeks': duration_days // 7,
                'months': duration_days // 30
            }
        
        # Calculate attendance rate
        attendance_rate = 0.0
        if profile.treatment_progress.total_sessions > 0:
            attendance_rate = (profile.treatment_progress.sessions_attended / 
                             profile.treatment_progress.total_sessions) * 100
        
        # Get assessment trends
        assessment_trends = {}
        for trend_key, trend_data in profile.assessment_history.score_trends.items():
            if len(trend_data) >= 2:
                first_score = trend_data[0][1]
                latest_score = trend_data[-1][1]
                change = latest_score - first_score
                change_percentage = (change / first_score) * 100 if first_score != 0 else 0
                
                assessment_trends[trend_key] = {
                    'first_score': first_score,
                    'latest_score': latest_score,
                    'change': change,
                    'change_percentage': change_percentage,
                    'trend': 'improving' if change < 0 else 'worsening' if change > 0 else 'stable',
                    'data_points': len(trend_data)
                }
        
        # Calculate goal progress
        goals_summary = {
            'total_goals': len(profile.treatment_preferences.therapy_goals),
            'active_goals': len([g for g in profile.treatment_progress.goal_progress.values() if g.get('status') == 'active']),
            'completed_goals': len([g for g in profile.treatment_progress.goal_progress.values() if g.get('status') == 'completed']),
            'average_progress': 0.0
        }
        
        if profile.treatment_progress.goal_progress:
            total_progress = sum(g.get('progress_percentage', 0) for g in profile.treatment_progress.goal_progress.values())
            goals_summary['average_progress'] = total_progress / len(profile.treatment_progress.goal_progress)
        
        return {
            'treatment_duration': treatment_duration,
            'session_statistics': {
                'total_sessions': profile.treatment_progress.total_sessions,
                'attended_sessions': profile.treatment_progress.sessions_attended,
                'missed_sessions': profile.treatment_progress.sessions_missed,
                'attendance_rate': attendance_rate,
                'homework_completion_rate': profile.treatment_progress.homework_completion_rate * 100
            },
            'assessment_trends': assessment_trends,
            'goals_summary': goals_summary,
            'milestones_achieved': len(profile.treatment_progress.milestones_achieved),
            'treatment_modifications': len(profile.treatment_progress.treatment_modifications)
        }
    
    def export_patient_data(self, patient_id: str, include_sensitive: bool = False) -> Dict[str, Any]:
        """Export patient data for backup or transfer"""
        
        profile = self.get_patient_profile(patient_id)
        if not profile:
            return {}
        
        export_data = {
            'export_info': {
                'export_date': datetime.now().isoformat(),
                'patient_id': patient_id,
                'include_sensitive': include_sensitive
            },
            'profile': asdict(profile)
        }
        
        # Get additional data from database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Assessment results
            cursor.execute("""
                SELECT * FROM assessment_results WHERE patient_id = ?
                ORDER BY assessment_date DESC
            """, (patient_id,))
            
            assessment_results = []
            for row in cursor.fetchall():
                assessment_results.append({
                    'assessment_type': row[2],
                    'assessment_date': row[3],
                    'scores': json.loads(row[4]),
                    'interpretation': row[5],
                    'administered_by': row[6]
                })
            
            export_data['assessment_results'] = assessment_results
            
            # Session records (excluding sensitive notes if requested)
            if include_sensitive:
                cursor.execute("""
                    SELECT * FROM session_records WHERE patient_id = ?
                    ORDER BY session_date DESC
                """, (patient_id,))
            else:
                cursor.execute("""
                    SELECT patient_id, session_id, session_date, session_type,
                           duration_minutes, interventions_used, homework_assigned,
                           '', mood_rating, ''
                    FROM session_records WHERE patient_id = ?
                    ORDER BY session_date DESC
                """, (patient_id,))
            
            session_records = []
            for row in cursor.fetchall():
                session_records.append({
                    'session_id': row[2],
                    'session_date': row[3],
                    'session_type': row[4],
                    'duration_minutes': row[5],
                    'interventions_used': json.loads(row[6]) if row[6] else [],
                    'homework_assigned': json.loads(row[7]) if row[7] else [],
                    'session_notes': row[8] if include_sensitive else '[REDACTED]',
                    'mood_rating': row[9],
                    'progress_notes': row[10] if include_sensitive else '[REDACTED]'
                })
            
            export_data['session_records'] = session_records
            
            # Treatment goals
            cursor.execute("""
                SELECT * FROM treatment_goals WHERE patient_id = ?
                ORDER BY created_date DESC
            """, (patient_id,))
            
            treatment_goals = []
            for row in cursor.fetchall():
                treatment_goals.append({
                    'goal_text': row[2],
                    'target_date': row[3],
                    'status': row[4],
                    'progress_percentage': row[5],
                    'created_date': row[6],
                    'last_updated': row[7],
                    'notes': row[8]
                })
            
            export_data['treatment_goals'] = treatment_goals
            
            # Safety plans
            cursor.execute("""
                SELECT * FROM safety_plans WHERE patient_id = ? AND active = 1
                ORDER BY created_date DESC
            """, (patient_id,))
            
            safety_plans = []
            for row in cursor.fetchall():
                safety_plans.append({
                    'plan_type': row[2],
                    'warning_signs': json.loads(row[3]) if row[3] else [],
                    'coping_strategies': json.loads(row[4]) if row[4] else [],
                    'support_contacts': json.loads(row[5]) if row[5] else [],
                    'professional_contacts': json.loads(row[6]) if row[6] else [],
                    'environmental_safety': json.loads(row[7]) if row[7] else [],
                    'created_date': row[8],
                    'last_updated': row[9]
                })
            
            export_data['safety_plans'] = safety_plans
        
        # Remove sensitive information if not requested
        if not include_sensitive:
            # Redact sensitive demographic info
            export_data['profile']['demographics']['phone_number'] = '[REDACTED]'
            export_data['profile']['demographics']['email'] = '[REDACTED]'
            export_data['profile']['demographics']['address'] = '[REDACTED]'
            
            # Redact detailed clinical notes
            export_data['profile']['notes'] = '[REDACTED]'
        
        return export_data
    
    def anonymize_patient_data(self, patient_id: str) -> Dict[str, Any]:
        """Create anonymized version of patient data for research"""
        
        profile = self.get_patient_profile(patient_id)
        if not profile:
            return {}
        
        # Create anonymized copy
        anonymized = asdict(profile)
        
        # Remove all identifying information
        anonymized['patient_id'] = f"ANON_{uuid.uuid4().hex[:8]}"
        anonymized['demographics'] = {
            'age_range': self._get_age_range(profile.demographics.date_of_birth),
            'gender': profile.demographics.gender.value,
            'region': 'REDACTED'  # Could keep general region if needed
        }
        
        # Keep clinical and treatment data but remove identifying details
        anonymized['clinical_info']['primary_diagnosis'] = profile.clinical_info.primary_diagnosis
        anonymized['clinical_info']['secondary_diagnoses'] = profile.clinical_info.secondary_diagnoses
        anonymized['clinical_info']['current_risk_level'] = profile.clinical_info.current_risk_level.value
        
        # Keep assessment trends and scores
        anonymized['assessment_history'] = profile.assessment_history.__dict__
        
        # Keep treatment progress metrics
        anonymized['treatment_progress'] = {
            'treatment_duration_days': (
                (date.today() - profile.treatment_progress.treatment_start_date).days
                if profile.treatment_progress.treatment_start_date else None
            ),
            'total_sessions': profile.treatment_progress.total_sessions,
            'sessions_attended': profile.treatment_progress.sessions_attended,
            'attendance_rate': (
                profile.treatment_progress.sessions_attended / 
                max(profile.treatment_progress.total_sessions, 1)
            ),
            'homework_completion_rate': profile.treatment_progress.homework_completion_rate,
            'treatment_phase': profile.treatment_progress.current_treatment_phase
        }
        
        return anonymized
    
    def _get_age_range(self, birth_date: date) -> str:
        """Get age range for anonymization"""
        today = date.today()
        age = today.year - birth_date.year
        if today < birth_date.replace(year=today.year):
            age -= 1
        
        if age < 18:
            return "under_18"
        elif age < 25:
            return "18_24"
        elif age < 35:
            return "25_34"
        elif age < 45:
            return "35_44"
        elif age < 55:
            return "45_54"
        elif age < 65:
            return "55_64"
        else:
            return "65_plus"
    
    def delete_patient_profile(self, patient_id: str, permanent: bool = False) -> bool:
        """Delete or deactivate patient profile"""
        
        try:
            if permanent:
                # Permanent deletion - remove all data
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Delete from all tables
                    tables = ['safety_plans', 'treatment_goals', 'session_records', 
                             'assessment_results', 'patient_profiles']
                    
                    for table in tables:
                        cursor.execute(f"DELETE FROM {table} WHERE patient_id = ?", (patient_id,))
                    
                    conn.commit()
                
                self.logger.info(f"Permanently deleted patient profile: {patient_id}")
            else:
                # Soft deletion - deactivate
                profile = self.get_patient_profile(patient_id)
                if profile:
                    profile.treatment_status = TreatmentStatus.TERMINATED
                    profile.notes.append({
                        'date': datetime.now().isoformat(),
                        'type': 'deactivation',
                        'content': 'Patient profile deactivated'
                    })
                    self.update_patient_profile(profile)
                
                self.logger.info(f"Deactivated patient profile: {patient_id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete patient profile {patient_id}: {e}")
            return False


# Example usage and testing
if __name__ == "__main__":
    print("=== PATIENT PROFILE SYSTEM DEMONSTRATION ===\n")
    
    # Initialize patient profile manager
    profile_manager = PatientProfileManager()
    
    # Create sample patient demographics
    demographics = Demographics(
        first_name="Jane",
        last_name="Smith",
        date_of_birth=date(1985, 3, 15),
        gender=Gender.FEMALE,
        preferred_pronouns="she/her",
        phone_number="555-0123",
        email="jane.smith@email.com",
        emergency_contact_name="John Smith",
        emergency_contact_phone="555-0124",
        emergency_contact_relationship="spouse"
    )
    
    # Create clinical information
    clinical_info = ClinicalInformation(
        primary_diagnosis="Major Depressive Disorder",
        secondary_diagnoses=["Generalized Anxiety Disorder"],
        current_medications=[
            {"name": "Sertraline", "dosage": "50mg", "frequency": "daily"},
            {"name": "Lorazepam", "dosage": "0.5mg", "frequency": "as needed"}
        ],
        current_risk_level=RiskLevel.MODERATE
    )
    
    # Create social history
    social_history = SocialHistory(
        marital_status=MaritalStatus.MARRIED,
        education_level=EducationLevel.BACHELORS_DEGREE,
        employment_status=EmploymentStatus.EMPLOYED_FULL_TIME,
        occupation="Software Engineer",
        support_system=["spouse", "close friends", "family"],
        cultural_background=["European American"],
        language_preferences=["English"]
    )
    
    # Create treatment preferences
    treatment_preferences = TreatmentPreferences(
        preferred_therapy_modality="CBT",
        therapy_goals=[
            "Reduce depressive symptoms",
            "Manage anxiety",
            "Improve work-life balance"
        ],
        session_frequency_preference="weekly",
        coping_strategies=["exercise", "journaling", "meditation"]
    )
    
    # Create patient profile
    print("Creating patient profile...")
    profile = profile_manager.create_patient_profile(
        demographics=demographics,
        clinical_info=clinical_info,
        social_history=social_history,
        treatment_preferences=treatment_preferences
    )
    
    print(f"Created patient: {profile.patient_id}")
    print(f"Patient name: {profile.demographics.first_name} {profile.demographics.last_name}")
    print()
    
    # Add assessment result
    print("Adding assessment result...")
    assessment_scores = {
        "Depression Severity": 14.0,
        "Functional Impairment": 2.0
    }
    
    profile_manager.add_assessment_result(
        profile.patient_id,
        "PHQ9",
        assessment_scores,
        "Moderate depression with functional impairment"
    )
    
    # Add session record
    print("Adding session record...")
    session_data = {
        'session_id': 'SESSION_001',
        'session_type': 'therapy',
        'duration_minutes': 50,
        'interventions_used': ['cognitive_restructuring', 'behavioral_activation'],
        'homework_assigned': ['mood monitoring', 'activity scheduling'],
        'session_notes': 'Good engagement, practiced thought challenging',
        'mood_rating': 6,
        'progress_notes': 'Patient showing increased awareness of thought patterns',
        'homework_completion': 0.8
    }
    
    profile_manager.add_session_record(profile.patient_id, session_data)
    
    # Update treatment goals
    print("Updating treatment goals...")
    goals = [
        {
            'goal_text': 'Reduce PHQ-9 score to below 10',
            'target_date': (date.today() + timedelta(weeks=8)).isoformat(),
            'status': 'active',
            'progress_percentage': 25.0
        },
        {
            'goal_text': 'Exercise 3 times per week',
            'target_date': (date.today() + timedelta(weeks=4)).isoformat(),
            'status': 'active',
            'progress_percentage': 60.0
        }
    ]
    
    profile_manager.update_treatment_goals(profile.patient_id, goals)
    
    # Get patient summary
    print("=== PATIENT SUMMARY ===")
    summary = profile_manager.get_patient_summary(profile.patient_id)
    if summary:
        print(f"Patient: {summary['patient_info']['name']}")
        print(f"Age: {summary['patient_info']['age']}")
        print(f"Primary Diagnosis: {summary['clinical_status']['primary_diagnosis']}")
        print(f"Risk Level: {summary['clinical_status']['current_risk_level']}")
        print(f"Sessions Attended: {summary['treatment_summary']['sessions_attended']}")
        print(f"Homework Completion: {summary['treatment_summary']['homework_completion_rate']:.1f}%")
        print(f"Active Goals: {summary['treatment_summary']['active_goals']}")
    
    print()
    
    # Get treatment statistics
    print("=== TREATMENT STATISTICS ===")
    stats = profile_manager.get_treatment_statistics(profile.patient_id)
    if stats:
        print(f"Total Sessions: {stats['session_statistics']['total_sessions']}")
        print(f"Attendance Rate: {stats['session_statistics']['attendance_rate']:.1f}%")
        print(f"Goals Summary: {stats['goals_summary']}")
        print(f"Assessment Trends: {len(stats['assessment_trends'])} tracked")
    
    print()
    
    # Demonstrate search functionality
    print("=== PATIENT SEARCH ===")
    search_results = profile_manager.search_patients({
        'treatment_status': 'active',
        'risk_level': 'moderate'
    })
    print(f"Found {len(search_results)} patients matching criteria")
    
    # Check patients requiring attention
    print("=== PATIENTS REQUIRING ATTENTION ===")
    attention_list = profile_manager.get_patients_requiring_attention()
    print(f"Patients requiring attention: {len(attention_list)}")
    for patient in attention_list:
        print(f"  {patient['patient_name']} - Priority: {patient['priority']}")
        for reason in patient['reasons']:
            print(f"    • {reason}")
    
    print("\n" + "="*60)
    print("Patient profile system demonstration complete!")
    print("Comprehensive patient management with clinical data integration.")
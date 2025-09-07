"""
System Settings Configuration
Centralized configuration management for AI therapy system
Handles all system settings, API configurations, and environment variables
"""

import os
import json
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path


class Environment(Enum):
    """System environment types"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class TherapyModality(Enum):
    """Available therapy modalities"""
    CBT = "cognitive_behavioral_therapy"
    DBT = "dialectical_behavior_therapy"
    ACT = "acceptance_commitment_therapy"
    PSYCHODYNAMIC = "psychodynamic_therapy"
    HUMANISTIC = "humanistic_therapy"
    INTEGRATIVE = "integrative_therapy"


class AssessmentFrequency(Enum):
    """Assessment frequency options"""
    EVERY_SESSION = "every_session"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    AS_NEEDED = "as_needed"


@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    db_type: str = "sqlite"
    db_path: str = "data/therapy_system.db"
    backup_enabled: bool = True
    backup_frequency_hours: int = 24
    backup_retention_days: int = 30
    encryption_enabled: bool = True
    connection_timeout: int = 30
    max_connections: int = 10
    
    # SQLite specific settings
    sqlite_settings: Dict[str, Any] = field(default_factory=lambda: {
        "journal_mode": "WAL",
        "synchronous": "NORMAL",
        "cache_size": 10000,
        "temp_store": "MEMORY",
        "mmap_size": 268435456,  # 256MB
        "foreign_keys": True,
        "auto_vacuum": "INCREMENTAL"
    })


@dataclass
class GeminiConfig:
    """Gemini AI configuration settings"""
    api_key: Optional[str] = None
    model_name: str = "gemini-2.5-pro"
    max_tokens: int = 8192
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    safety_settings: Dict[str, str] = field(default_factory=lambda: {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE"
    })
    timeout_seconds: int = 120
    retry_attempts: int = 3
    retry_delay_seconds: int = 2
    
    # Prompt engineering settings
    system_prompt_template: str = """You are an AI therapy assistant providing professional, 
    empathetic, and evidence-based mental health support. Always prioritize patient safety, 
    maintain professional boundaries, and provide appropriate clinical interventions."""
    
    conversation_memory_limit: int = 10  # Number of previous exchanges to remember
    context_window_tokens: int = 32000


@dataclass
class SecurityConfig:
    """Security and privacy configuration"""
    encryption_key_path: str = "config/encryption.key"
    session_timeout_minutes: int = 60
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 30
    password_min_length: int = 12
    require_mfa: bool = True
    
    # HIPAA compliance settings
    hipaa_compliance_enabled: bool = True
    audit_logging_enabled: bool = True
    data_retention_days: int = 2555  # 7 years for HIPAA
    anonymization_enabled: bool = True
    
    # API security
    api_rate_limit_per_minute: int = 100
    api_key_rotation_days: int = 90
    
    # Data encryption
    encrypt_at_rest: bool = True
    encrypt_in_transit: bool = True
    encryption_algorithm: str = "AES-256-GCM"


@dataclass
class ClinicalConfig:
    """Clinical practice configuration"""
    default_therapy_modality: TherapyModality = TherapyModality.CBT
    available_modalities: List[TherapyModality] = field(default_factory=lambda: [
        TherapyModality.CBT,
        TherapyModality.DBT,
        TherapyModality.ACT,
        TherapyModality.PSYCHODYNAMIC
    ])
    
    # Session settings
    default_session_duration_minutes: int = 50
    session_reminder_minutes: int = 15
    max_sessions_per_day: int = 8
    break_between_sessions_minutes: int = 10
    
    # Assessment settings
    mandatory_assessments: List[str] = field(default_factory=lambda: ["PHQ9", "GAD7", "ORS"])
    assessment_frequency: AssessmentFrequency = AssessmentFrequency.WEEKLY
    risk_assessment_frequency: AssessmentFrequency = AssessmentFrequency.EVERY_SESSION
    
    # Risk management
    suicide_risk_threshold: str = "moderate"
    automatic_risk_escalation: bool = True
    crisis_contact_required: bool = True
    emergency_protocols_enabled: bool = True
    
    # Treatment planning
    treatment_plan_review_weeks: int = 4
    goal_review_frequency_weeks: int = 2
    homework_reminder_enabled: bool = True
    progress_tracking_enabled: bool = True
    
    # Documentation requirements
    session_notes_required: bool = True
    risk_documentation_required: bool = True
    outcome_tracking_required: bool = True
    
    # Clinical decision support
    diagnostic_suggestions_enabled: bool = True
    treatment_recommendations_enabled: bool = True
    medication_interaction_checks: bool = True


@dataclass
class SystemConfig:
    """General system configuration"""
    system_name: str = "AI Therapy System"
    version: str = "1.0.0"
    environment: Environment = Environment.DEVELOPMENT
    
    # Logging
    log_level: LogLevel = LogLevel.INFO
    log_file_path: str = "logs/therapy_system.log"
    log_max_size_mb: int = 100
    log_backup_count: int = 5
    log_rotation_enabled: bool = True
    
    # Performance
    max_concurrent_sessions: int = 50
    session_cleanup_interval_hours: int = 24
    cache_enabled: bool = True
    cache_size_mb: int = 256
    
    # Backup and recovery
    backup_enabled: bool = True
    backup_schedule: str = "daily"  # daily, weekly, monthly
    backup_location: str = "data/backups"
    disaster_recovery_enabled: bool = False
    
    # Integration settings
    external_apis_enabled: bool = False
    webhook_enabled: bool = False
    export_enabled: bool = True
    import_enabled: bool = True
    
    # User interface
    theme: str = "professional"
    language: str = "en"
    timezone: str = "UTC"
    date_format: str = "%Y-%m-%d"
    time_format: str = "%H:%M:%S"


@dataclass
class ComplianceConfig:
    """Regulatory compliance configuration"""
    # HIPAA compliance
    hipaa_enabled: bool = True
    minimum_necessary_standard: bool = True
    access_controls_enabled: bool = True
    
    # International compliance
    gdpr_enabled: bool = False  # EU General Data Protection Regulation
    ccpa_enabled: bool = False  # California Consumer Privacy Act
    pipeda_enabled: bool = False  # Personal Information Protection and Electronic Documents Act (Canada)
    
    # Clinical standards
    dsm5_compliance: bool = True
    icd10_compliance: bool = True
    apa_guidelines_compliance: bool = True
    
    # Documentation standards
    soap_notes_format: bool = True  # Subjective, Objective, Assessment, Plan
    dap_notes_format: bool = False  # Data, Assessment, Plan
    
    # Quality assurance
    clinical_supervision_required: bool = False
    peer_review_enabled: bool = False
    outcome_measurement_required: bool = True


class TherapySystemSettings:
    """Main settings manager for the AI therapy system"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or "config/settings.json"
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)
        
        # Initialize configuration objects
        self.database = DatabaseConfig()
        self.gemini = GeminiConfig()
        self.security = SecurityConfig()
        self.clinical = ClinicalConfig()
        self.system = SystemConfig()
        self.compliance = ComplianceConfig()
        
        # Load configuration from file if exists
        self.load_settings()
        
        # Load environment variables
        self.load_environment_variables()
        
        # Validate configuration
        self.validate_settings()
    
    def load_settings(self):
        """Load settings from configuration file"""
        config_path = Path(self.config_file)
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config_data = json.load(f)
                
                # Update configuration objects with loaded data
                if 'database' in config_data:
                    self._update_config(self.database, config_data['database'])
                
                if 'gemini' in config_data:
                    self._update_config(self.gemini, config_data['gemini'])
                
                if 'security' in config_data:
                    self._update_config(self.security, config_data['security'])
                
                if 'clinical' in config_data:
                    self._update_config(self.clinical, config_data['clinical'])
                
                if 'system' in config_data:
                    self._update_config(self.system, config_data['system'])
                
                if 'compliance' in config_data:
                    self._update_config(self.compliance, config_data['compliance'])
                
                print(f"Settings loaded from {config_path}")
                
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error loading settings: {e}. Using default settings.")
    
    def _update_config(self, config_obj: Any, data: Dict[str, Any]):
        """Update configuration object with dictionary data"""
        for key, value in data.items():
            if hasattr(config_obj, key):
                # Handle enum conversions
                attr_type = type(getattr(config_obj, key))
                if hasattr(attr_type, '__bases__') and Enum in attr_type.__bases__:
                    try:
                        setattr(config_obj, key, attr_type(value))
                    except ValueError:
                        print(f"Invalid enum value for {key}: {value}")
                else:
                    setattr(config_obj, key, value)
    
    def load_environment_variables(self):
        """Load settings from environment variables"""
        
        # Database settings
        if os.getenv("DB_PATH"):
            self.database.db_path = os.getenv("DB_PATH")
        
        # Gemini API settings
        if os.getenv("GEMINI_API_KEY"):
            self.gemini.api_key = os.getenv("GEMINI_API_KEY")
        
        if os.getenv("GEMINI_MODEL"):
            self.gemini.model_name = os.getenv("GEMINI_MODEL")
        
        # Environment type
        env_type = os.getenv("ENVIRONMENT", "development")
        try:
            self.system.environment = Environment(env_type.lower())
        except ValueError:
            print(f"Invalid environment type: {env_type}")
        
        # Security settings
        if os.getenv("ENCRYPTION_KEY_PATH"):
            self.security.encryption_key_path = os.getenv("ENCRYPTION_KEY_PATH")
        
        # Compliance settings
        if os.getenv("HIPAA_ENABLED"):
            self.compliance.hipaa_enabled = os.getenv("HIPAA_ENABLED").lower() == "true"
        
        if os.getenv("GDPR_ENABLED"):
            self.compliance.gdpr_enabled = os.getenv("GDPR_ENABLED").lower() == "true"
        
        # Logging
        if os.getenv("LOG_LEVEL"):
            try:
                self.system.log_level = LogLevel(os.getenv("LOG_LEVEL").upper())
            except ValueError:
                print(f"Invalid log level: {os.getenv('LOG_LEVEL')}")
    
    def save_settings(self):
        """Save current settings to configuration file"""
        config_data = {
            'database': self._config_to_dict(self.database),
            'gemini': self._config_to_dict(self.gemini),
            'security': self._config_to_dict(self.security),
            'clinical': self._config_to_dict(self.clinical),
            'system': self._config_to_dict(self.system),
            'compliance': self._config_to_dict(self.compliance),
            'last_updated': datetime.now().isoformat()
        }
        
        # Create config directory if it doesn't exist
        Path(self.config_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=2, default=str)
        
        print(f"Settings saved to {self.config_file}")
    
    def _config_to_dict(self, config_obj: Any) -> Dict[str, Any]:
        """Convert configuration object to dictionary"""
        result = {}
        for key, value in config_obj.__dict__.items():
            if isinstance(value, Enum):
                result[key] = value.value
            elif isinstance(value, (list, dict, str, int, float, bool)) or value is None:
                result[key] = value
            else:
                result[key] = str(value)
        return result
    
    def validate_settings(self):
        """Validate configuration settings"""
        validation_errors = []
        
        # Validate database settings
        if not self.database.db_path:
            validation_errors.append("Database path is required")
        
        # Validate Gemini API settings
        if not self.gemini.api_key and self.system.environment == Environment.PRODUCTION:
            validation_errors.append("Gemini API key is required for production environment")
        
        if self.gemini.temperature < 0 or self.gemini.temperature > 2:
            validation_errors.append("Gemini temperature must be between 0 and 2")
        
        if self.gemini.max_tokens < 1 or self.gemini.max_tokens > 32000:
            validation_errors.append("Gemini max_tokens must be between 1 and 32000")
        
        # Validate security settings
        if self.security.session_timeout_minutes < 5:
            validation_errors.append("Session timeout must be at least 5 minutes")
        
        if self.security.password_min_length < 8:
            validation_errors.append("Minimum password length must be at least 8 characters")
        
        # Validate clinical settings
        if self.clinical.default_session_duration_minutes < 15:
            validation_errors.append("Session duration must be at least 15 minutes")
        
        if self.clinical.max_sessions_per_day < 1:
            validation_errors.append("Maximum sessions per day must be at least 1")
        
        # Log validation errors
        if validation_errors:
            for error in validation_errors:
                print(f"Configuration Error: {error}")
            
            if self.system.environment == Environment.PRODUCTION:
                raise ValueError("Configuration validation failed in production environment")
        else:
            print("Configuration validation passed")
    
    def get_database_url(self) -> str:
        """Get database connection URL"""
        if self.database.db_type == "sqlite":
            return f"sqlite:///{self.database.db_path}"
        else:
            return f"{self.database.db_type}:///{self.database.db_path}"
    
    def get_gemini_config(self) -> Dict[str, Any]:
        """Get Gemini API configuration dictionary"""
        return {
            'api_key': self.gemini.api_key,
            'model_name': self.gemini.model_name,
            'max_tokens': self.gemini.max_tokens,
            'temperature': self.gemini.temperature,
            'top_p': self.gemini.top_p,
            'top_k': self.gemini.top_k,
            'safety_settings': self.gemini.safety_settings,
            'timeout_seconds': self.gemini.timeout_seconds,
            'retry_attempts': self.gemini.retry_attempts,
            'retry_delay_seconds': self.gemini.retry_delay_seconds
        }
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.system.environment == Environment.PRODUCTION
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.system.environment == Environment.DEVELOPMENT
    
    def get_log_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return {
            'level': self.system.log_level.value,
            'filename': self.system.log_file_path,
            'maxBytes': self.system.log_max_size_mb * 1024 * 1024,
            'backupCount': self.system.log_backup_count,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    
    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers for HTTP responses"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'",
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
    
    def update_setting(self, section: str, key: str, value: Any):
        """Update a specific setting"""
        config_sections = {
            'database': self.database,
            'gemini': self.gemini,
            'security': self.security,
            'clinical': self.clinical,
            'system': self.system,
            'compliance': self.compliance
        }
        
        if section in config_sections:
            config_obj = config_sections[section]
            if hasattr(config_obj, key):
                setattr(config_obj, key, value)
                print(f"Updated {section}.{key} = {value}")
            else:
                print(f"Setting {section}.{key} does not exist")
        else:
            print(f"Configuration section '{section}' does not exist")
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.database = DatabaseConfig()
        self.gemini = GeminiConfig()
        self.security = SecurityConfig()
        self.clinical = ClinicalConfig()
        self.system = SystemConfig()
        self.compliance = ComplianceConfig()
        print("Settings reset to defaults")
    
    def export_settings(self, export_path: str):
        """Export settings to external file"""
        config_data = {
            'database': self._config_to_dict(self.database),
            'gemini': self._config_to_dict(self.gemini),
            'security': self._config_to_dict(self.security),
            'clinical': self._config_to_dict(self.clinical),
            'system': self._config_to_dict(self.system),
            'compliance': self._config_to_dict(self.compliance),
            'exported_at': datetime.now().isoformat(),
            'system_version': self.system.version
        }
        
        with open(export_path, 'w') as f:
            json.dump(config_data, f, indent=2, default=str)
        
        print(f"Settings exported to {export_path}")


# Global settings instance
settings = TherapySystemSettings()


# Example usage and testing
if __name__ == "__main__":
    print("=== AI THERAPY SYSTEM SETTINGS DEMONSTRATION ===\n")
    
    # Display current settings
    print("Current System Configuration:")
    print(f"Environment: {settings.system.environment.value}")
    print(f"Version: {settings.system.version}")
    print(f"Database Path: {settings.database.db_path}")
    print(f"Gemini Model: {settings.gemini.model_name}")
    print(f"HIPAA Compliance: {settings.compliance.hipaa_enabled}")
    print(f"Default Therapy Modality: {settings.clinical.default_therapy_modality.value}")
    print()
    
    # Demonstrate setting updates
    print("=== UPDATING SETTINGS ===")
    settings.update_setting('clinical', 'default_session_duration_minutes', 60)
    settings.update_setting('system', 'log_level', LogLevel.DEBUG)
    settings.update_setting('gemini', 'temperature', 0.5)
    print()
    
    # Show configuration validation
    print("=== CONFIGURATION VALIDATION ===")
    try:
        settings.validate_settings()
        print("✅ All settings are valid")
    except ValueError as e:
        print(f"❌ Validation error: {e}")
    print()
    
    # Demonstrate getting specific configurations
    print("=== CONFIGURATION ACCESS ===")
    gemini_config = settings.get_gemini_config()
    print("Gemini Configuration:")
    for key, value in gemini_config.items():
        if key != 'api_key':  # Don't print API key
            print(f"  {key}: {value}")
    print()
    
    log_config = settings.get_log_config()
    print("Logging Configuration:")
    for key, value in log_config.items():
        print(f"  {key}: {value}")
    print()
    
    # Show environment detection
    print("=== ENVIRONMENT DETECTION ===")
    print(f"Is Production: {settings.is_production()}")
    print(f"Is Development: {settings.is_development()}")
    print()
    
    # Demonstrate saving and loading
    print("=== SETTINGS PERSISTENCE ===")
    settings.save_settings()
    print("Settings saved successfully")
    
    # Export settings
    settings.export_settings("config/settings_backup.json")
    print("Settings exported for backup")
    
    print("\n" + "="*60)
    print("Settings system ready for AI therapy application!")
    print("All configurations are centralized and easily manageable.")
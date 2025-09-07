"""
Progress Tracker Module
Comprehensive treatment progress monitoring and analytics for AI therapy system
Tracks patient progress across multiple dimensions with evidence-based metrics
"""

import sqlite3
import json
import statistics
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum
import logging
import numpy as np
from pathlib import Path


class ProgressMetricType(Enum):
    """Types of progress metrics"""
    SYMPTOM_SEVERITY = "symptom_severity"
    FUNCTIONAL_IMPROVEMENT = "functional_improvement"
    QUALITY_OF_LIFE = "quality_of_life"
    GOAL_ACHIEVEMENT = "goal_achievement"
    THERAPEUTIC_ALLIANCE = "therapeutic_alliance"
    HOMEWORK_COMPLIANCE = "homework_compliance"
    SESSION_ENGAGEMENT = "session_engagement"
    RISK_LEVEL = "risk_level"
    MEDICATION_ADHERENCE = "medication_adherence"
    SOCIAL_FUNCTIONING = "social_functioning"


class TrendDirection(Enum):
    """Direction of progress trends"""
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    MIXED = "mixed"
    INSUFFICIENT_DATA = "insufficient_data"


class ProgressPhase(Enum):
    """Phases of treatment progress"""
    EARLY_TREATMENT = "early_treatment"  # Sessions 1-4
    STABILIZATION = "stabilization"      # Sessions 5-8
    WORKING_PHASE = "working_phase"      # Sessions 9-16
    CONSOLIDATION = "consolidation"      # Sessions 17-20
    MAINTENANCE = "maintenance"          # Sessions 21+


class AlertLevel(Enum):
    """Alert levels for progress monitoring"""
    GREEN = "green"    # Progress on track
    YELLOW = "yellow"  # Minor concerns
    ORANGE = "orange"  # Significant concerns
    RED = "red"        # Critical concerns


@dataclass
class ProgressDataPoint:
    """Individual progress measurement"""
    metric_type: ProgressMetricType
    value: float
    timestamp: datetime
    session_number: Optional[int] = None
    source: str = "assessment"  # assessment, observation, self_report
    notes: str = ""
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProgressTrend:
    """Analysis of progress trend over time"""
    metric_type: ProgressMetricType
    direction: TrendDirection
    slope: float  # Rate of change
    confidence: float  # Confidence in trend analysis
    data_points: int
    start_value: float
    current_value: float
    change_magnitude: float
    change_percentage: float
    statistical_significance: bool
    time_period_days: int


@dataclass
class GoalProgress:
    """Progress tracking for individual goals"""
    goal_id: str
    goal_text: str
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    progress_percentage: float = 0.0
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    target_date: Optional[date] = None
    status: str = "active"  # active, achieved, paused, discontinued
    last_updated: datetime = field(default_factory=datetime.now)
    interventions_used: List[str] = field(default_factory=list)


@dataclass
class SessionProgress:
    """Progress within individual session"""
    session_id: str
    session_number: int
    session_date: datetime
    pre_session_mood: Optional[int] = None
    post_session_mood: Optional[int] = None
    engagement_level: Optional[int] = None  # 1-10 scale
    homework_completion: Optional[float] = None  # 0-1 scale
    skills_practiced: List[str] = field(default_factory=list)
    breakthrough_moments: List[str] = field(default_factory=list)
    challenges_encountered: List[str] = field(default_factory=list)
    therapist_observations: str = ""
    patient_feedback: str = ""


@dataclass
class ProgressAlert:
    """Alert for concerning progress patterns"""
    alert_id: str
    patient_id: str
    alert_level: AlertLevel
    metric_type: ProgressMetricType
    description: str
    recommendations: List[str]
    created_date: datetime
    acknowledged: bool = False
    resolved: bool = False
    resolution_notes: str = ""


@dataclass
class ProgressSummary:
    """Comprehensive progress summary"""
    patient_id: str
    assessment_period_start: date
    assessment_period_end: date
    overall_trend: TrendDirection
    key_improvements: List[str]
    areas_of_concern: List[str]
    goal_completion_rate: float
    session_attendance_rate: float
    homework_completion_rate: float
    risk_level_trend: TrendDirection
    treatment_response: str  # excellent, good, partial, poor, deteriorating
    recommendations: List[str]
    next_review_date: date


class ProgressTracker:
    """Comprehensive progress tracking and analytics system"""
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._ensure_database_exists()
        self._create_tables()
        
        # Configuration
        self.reliable_change_indices = self._initialize_rci_values()
        self.progress_thresholds = self._initialize_progress_thresholds()
        self.alert_criteria = self._initialize_alert_criteria()
    
    def _ensure_database_exists(self):
        """Ensure database directory and file exist"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def _create_tables(self):
        """Create database tables for progress tracking"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Progress data points table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS progress_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    metric_type TEXT NOT NULL,
                    value REAL NOT NULL,
                    timestamp TEXT NOT NULL,
                    session_number INTEGER,
                    source TEXT NOT NULL,
                    notes TEXT,
                    context TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patient_profiles (patient_id)
                )
            """)
            
            # Goal progress table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS goal_progress (
                    goal_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    goal_text TEXT NOT NULL,
                    target_value REAL,
                    current_value REAL,
                    progress_percentage REAL DEFAULT 0.0,
                    milestones TEXT,
                    target_date TEXT,
                    status TEXT DEFAULT 'active',
                    last_updated TEXT NOT NULL,
                    interventions_used TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patient_profiles (patient_id)
                )
            """)
            
            # Session progress table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_progress (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    session_number INTEGER NOT NULL,
                    session_date TEXT NOT NULL,
                    pre_session_mood INTEGER,
                    post_session_mood INTEGER,
                    engagement_level INTEGER,
                    homework_completion REAL,
                    skills_practiced TEXT,
                    breakthrough_moments TEXT,
                    challenges_encountered TEXT,
                    therapist_observations TEXT,
                    patient_feedback TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patient_profiles (patient_id)
                )
            """)
            
            # Progress alerts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS progress_alerts (
                    alert_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    alert_level TEXT NOT NULL,
                    metric_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    recommendations TEXT,
                    created_date TEXT NOT NULL,
                    acknowledged BOOLEAN DEFAULT 0,
                    resolved BOOLEAN DEFAULT 0,
                    resolution_notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patient_profiles (patient_id)
                )
            """)
            
            # Progress trends table (cached calculations)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS progress_trends (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    metric_type TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    slope REAL NOT NULL,
                    confidence REAL NOT NULL,
                    data_points INTEGER NOT NULL,
                    start_value REAL NOT NULL,
                    current_value REAL NOT NULL,
                    change_magnitude REAL NOT NULL,
                    change_percentage REAL NOT NULL,
                    statistical_significance BOOLEAN NOT NULL,
                    time_period_days INTEGER NOT NULL,
                    calculated_date TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patient_profiles (patient_id)
                )
            """)
            
            conn.commit()
    
    def _initialize_rci_values(self) -> Dict[str, float]:
        """Initialize Reliable Change Index values for assessments"""
        return {
            "PHQ9": 6.0,      # Depression
            "GAD7": 4.0,      # Anxiety
            "PCL5": 10.0,     # PTSD
            "ORS": 5.0,       # Outcome Rating Scale
            "SRS": 2.5,       # Session Rating Scale
            "BDI_II": 8.46,   # Beck Depression Inventory
            "BAI": 7.0,       # Beck Anxiety Inventory
            "DASS21": 4.0     # Depression Anxiety Stress Scales
        }
    
    def _initialize_progress_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Initialize progress thresholds for different metrics"""
        return {
            "homework_completion": {
                "excellent": 0.9,
                "good": 0.7,
                "fair": 0.5,
                "poor": 0.3
            },
            "session_engagement": {
                "excellent": 8.0,
                "good": 6.0,
                "fair": 4.0,
                "poor": 2.0
            },
            "goal_progress": {
                "on_track": 75.0,
                "moderate": 50.0,
                "slow": 25.0,
                "concerning": 10.0
            },
            "attendance_rate": {
                "excellent": 0.95,
                "good": 0.8,
                "fair": 0.6,
                "poor": 0.4
            }
        }
    
    def _initialize_alert_criteria(self) -> Dict[str, Dict[str, Any]]:
        """Initialize criteria for generating progress alerts"""
        return {
            "deteriorating_symptoms": {
                "threshold_increase": 30,  # % increase in symptom scores
                "min_sessions": 3,
                "alert_level": AlertLevel.ORANGE
            },
            "poor_attendance": {
                "missed_sessions": 3,
                "consecutive_misses": 2,
                "alert_level": AlertLevel.YELLOW
            },
            "low_homework_compliance": {
                "completion_rate": 0.3,
                "min_sessions": 4,
                "alert_level": AlertLevel.YELLOW
            },
            "lack_of_progress": {
                "sessions_without_improvement": 6,
                "goal_progress_threshold": 10,  # % progress
                "alert_level": AlertLevel.ORANGE
            },
            "risk_escalation": {
                "risk_level_increase": True,
                "alert_level": AlertLevel.RED
            }
        }
    
    def add_progress_data(self, patient_id: str, metric_type: ProgressMetricType,
                         value: float, session_number: Optional[int] = None,
                         source: str = "assessment", notes: str = "",
                         context: Optional[Dict[str, Any]] = None) -> bool:
        """Add progress data point"""
        
        try:
            data_point = ProgressDataPoint(
                metric_type=metric_type,
                value=value,
                timestamp=datetime.now(),
                session_number=session_number,
                source=source,
                notes=notes,
                context=context or {}
            )
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO progress_data (
                        patient_id, metric_type, value, timestamp, session_number,
                        source, notes, context
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    patient_id,
                    metric_type.value,
                    value,
                    data_point.timestamp.isoformat(),
                    session_number,
                    source,
                    notes,
                    json.dumps(context or {})
                ))
                
                conn.commit()
            
            # Check for alerts
            self._check_progress_alerts(patient_id, metric_type, value)
            
            self.logger.info(f"Added progress data for patient {patient_id}: {metric_type.value} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add progress data: {e}")
            return False
    
    def add_session_progress(self, session_progress: SessionProgress) -> bool:
        """Add session-specific progress data"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO session_progress (
                        session_id, patient_id, session_number, session_date,
                        pre_session_mood, post_session_mood, engagement_level,
                        homework_completion, skills_practiced, breakthrough_moments,
                        challenges_encountered, therapist_observations, patient_feedback
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_progress.session_id,
                    # Note: We need patient_id - should be added to SessionProgress dataclass
                    # For now, extract from session_id assuming format PATIENT_ID_SESSION_X
                    session_progress.session_id.split('_SESSION_')[0] if '_SESSION_' in session_progress.session_id else '',
                    session_progress.session_number,
                    session_progress.session_date.isoformat(),
                    session_progress.pre_session_mood,
                    session_progress.post_session_mood,
                    session_progress.engagement_level,
                    session_progress.homework_completion,
                    json.dumps(session_progress.skills_practiced),
                    json.dumps(session_progress.breakthrough_moments),
                    json.dumps(session_progress.challenges_encountered),
                    session_progress.therapist_observations,
                    session_progress.patient_feedback
                ))
                
                conn.commit()
            
            # Add derived progress metrics
            patient_id = session_progress.session_id.split('_SESSION_')[0] if '_SESSION_' in session_progress.session_id else ''
            
            if session_progress.homework_completion is not None:
                self.add_progress_data(
                    patient_id,
                    ProgressMetricType.HOMEWORK_COMPLIANCE,
                    session_progress.homework_completion,
                    session_progress.session_number,
                    "session_report"
                )
            
            if session_progress.engagement_level is not None:
                self.add_progress_data(
                    patient_id,
                    ProgressMetricType.SESSION_ENGAGEMENT,
                    session_progress.engagement_level,
                    session_progress.session_number,
                    "therapist_observation"
                )
            
            # Calculate mood change if both pre and post available
            if (session_progress.pre_session_mood is not None and 
                session_progress.post_session_mood is not None):
                mood_change = session_progress.post_session_mood - session_progress.pre_session_mood
                self.add_progress_data(
                    patient_id,
                    ProgressMetricType.SYMPTOM_SEVERITY,
                    mood_change,
                    session_progress.session_number,
                    "mood_change",
                    f"Pre: {session_progress.pre_session_mood}, Post: {session_progress.post_session_mood}"
                )
            
            self.logger.info(f"Added session progress: {session_progress.session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add session progress: {e}")
            return False
    
    def update_goal_progress(self, patient_id: str, goal_id: str, 
                           progress_percentage: float, current_value: Optional[float] = None,
                           milestone: Optional[str] = None, 
                           interventions_used: Optional[List[str]] = None) -> bool:
        """Update progress for specific treatment goal"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get existing goal
                cursor.execute("SELECT * FROM goal_progress WHERE goal_id = ?", (goal_id,))
                existing_goal = cursor.fetchone()
                
                if existing_goal:
                    # Update existing goal
                    milestones = json.loads(existing_goal[5]) if existing_goal[5] else []
                    if milestone:
                        milestones.append({
                            'milestone': milestone,
                            'date': datetime.now().isoformat(),
                            'progress_percentage': progress_percentage
                        })
                    
                    interventions = json.loads(existing_goal[10]) if existing_goal[10] else []
                    if interventions_used:
                        interventions.extend(interventions_used)
                        interventions = list(set(interventions))  # Remove duplicates
                    
                    status = "achieved" if progress_percentage >= 100 else "active"
                    
                    cursor.execute("""
                        UPDATE goal_progress SET
                            current_value = ?, progress_percentage = ?, milestones = ?,
                            status = ?, last_updated = ?, interventions_used = ?
                        WHERE goal_id = ?
                    """, (
                        current_value,
                        progress_percentage,
                        json.dumps(milestones),
                        status,
                        datetime.now().isoformat(),
                        json.dumps(interventions),
                        goal_id
                    ))
                
                conn.commit()
            
            # Add progress data point
            self.add_progress_data(
                patient_id,
                ProgressMetricType.GOAL_ACHIEVEMENT,
                progress_percentage,
                notes=f"Goal: {goal_id}"
            )
            
            self.logger.info(f"Updated goal progress: {goal_id} = {progress_percentage}%")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update goal progress: {e}")
            return False
    
    def calculate_progress_trends(self, patient_id: str, 
                                metric_type: Optional[ProgressMetricType] = None,
                                days_lookback: int = 90) -> List[ProgressTrend]:
        """Calculate progress trends for patient"""
        
        trends = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get metrics to analyze
                if metric_type:
                    metrics = [metric_type]
                else:
                    cursor.execute("""
                        SELECT DISTINCT metric_type FROM progress_data 
                        WHERE patient_id = ? AND timestamp >= ?
                    """, (patient_id, (datetime.now() - timedelta(days=days_lookback)).isoformat()))
                    metrics = [ProgressMetricType(row[0]) for row in cursor.fetchall()]
                
                for metric in metrics:
                    # Get data points for this metric
                    cursor.execute("""
                        SELECT value, timestamp FROM progress_data
                        WHERE patient_id = ? AND metric_type = ? AND timestamp >= ?
                        ORDER BY timestamp
                    """, (patient_id, metric.value, (datetime.now() - timedelta(days=days_lookback)).isoformat()))
                    
                    data_points = cursor.fetchall()
                    
                    if len(data_points) < 2:
                        continue
                    
                    # Calculate trend
                    trend = self._calculate_trend_analysis(metric, data_points)
                    if trend:
                        trends.append(trend)
                        
                        # Cache trend in database
                        self._cache_trend_calculation(patient_id, trend)
            
            return trends
            
        except Exception as e:
            self.logger.error(f"Failed to calculate progress trends: {e}")
            return []
    
    def _calculate_trend_analysis(self, metric_type: ProgressMetricType, 
                                 data_points: List[Tuple[float, str]]) -> Optional[ProgressTrend]:
        """Calculate statistical trend analysis"""
        
        try:
            if len(data_points) < 2:
                return None
            
            # Extract values and convert timestamps to days
            values = [point[0] for point in data_points]
            timestamps = [datetime.fromisoformat(point[1]) for point in data_points]
            
            # Convert to days from first measurement
            start_time = timestamps[0]
            days = [(ts - start_time).days for ts in timestamps]
            
            # Calculate linear regression
            if len(set(days)) < 2:  # All measurements on same day
                return None
            
            # Simple linear regression
            n = len(values)
            sum_x = sum(days)
            sum_y = sum(values)
            sum_xy = sum(x * y for x, y in zip(days, values))
            sum_x_squared = sum(x * x for x in days)
            
            # Calculate slope and correlation
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x * sum_x)
            
            # Calculate correlation coefficient
            mean_x = sum_x / n
            mean_y = sum_y / n
            
            numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(days, values))
            denominator_x = sum((x - mean_x) ** 2 for x in days)
            denominator_y = sum((y - mean_y) ** 2 for y in values)
            
            if denominator_x == 0 or denominator_y == 0:
                correlation = 0
            else:
                correlation = numerator / (denominator_x * denominator_y) ** 0.5
            
            # Determine trend direction
            if abs(slope) < 0.01:  # Very small change
                direction = TrendDirection.STABLE
            elif slope > 0:
                # For symptom measures, positive slope = worsening
                if metric_type in [ProgressMetricType.SYMPTOM_SEVERITY, ProgressMetricType.RISK_LEVEL]:
                    direction = TrendDirection.DECLINING
                else:
                    direction = TrendDirection.IMPROVING
            else:
                # Negative slope
                if metric_type in [ProgressMetricType.SYMPTOM_SEVERITY, ProgressMetricType.RISK_LEVEL]:
                    direction = TrendDirection.IMPROVING
                else:
                    direction = TrendDirection.DECLINING
            
            # Calculate change metrics
            start_value = values[0]
            current_value = values[-1]
            change_magnitude = abs(current_value - start_value)
            change_percentage = (change_magnitude / abs(start_value)) * 100 if start_value != 0 else 0
            
            # Statistical significance (simplified)
            statistical_significance = abs(correlation) > 0.3 and len(values) >= 5
            
            # Confidence based on correlation and sample size
            confidence = min(abs(correlation) * (len(values) / 10), 1.0)
            
            time_period_days = (timestamps[-1] - timestamps[0]).days
            
            return ProgressTrend(
                metric_type=metric_type,
                direction=direction,
                slope=slope,
                confidence=confidence,
                data_points=len(values),
                start_value=start_value,
                current_value=current_value,
                change_magnitude=change_magnitude,
                change_percentage=change_percentage,
                statistical_significance=statistical_significance,
                time_period_days=time_period_days
            )
            
        except Exception as e:
            self.logger.error(f"Error in trend analysis: {e}")
            return None
    
    def _cache_trend_calculation(self, patient_id: str, trend: ProgressTrend):
        """Cache trend calculation in database"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO progress_trends (
                        patient_id, metric_type, direction, slope, confidence,
                        data_points, start_value, current_value, change_magnitude,
                        change_percentage, statistical_significance, time_period_days,
                        calculated_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    patient_id,
                    trend.metric_type.value,
                    trend.direction.value,
                    trend.slope,
                    trend.confidence,
                    trend.data_points,
                    trend.start_value,
                    trend.current_value,
                    trend.change_magnitude,
                    trend.change_percentage,
                    trend.statistical_significance,
                    trend.time_period_days,
                    datetime.now().isoformat()
                ))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to cache trend calculation: {e}")
    
    def _check_progress_alerts(self, patient_id: str, metric_type: ProgressMetricType, value: float):
        """Check if new data point triggers any alerts"""
        
        try:
            # Get recent data for this metric
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT value, timestamp FROM progress_data
                    WHERE patient_id = ? AND metric_type = ?
                    ORDER BY timestamp DESC LIMIT 10
                """, (patient_id, metric_type.value))
                
                recent_data = cursor.fetchall()
            
            if len(recent_data) < 2:
                return
            
            # Check for deteriorating symptoms
            if metric_type == ProgressMetricType.SYMPTOM_SEVERITY:
                baseline = recent_data[-1][0]  # Oldest in recent data
                current = recent_data[0][0]   # Most recent
                
                if baseline > 0:
                    increase_percentage = ((current - baseline) / baseline) * 100
                    
                    if increase_percentage > self.alert_criteria["deteriorating_symptoms"]["threshold_increase"]:
                        self._create_alert(
                            patient_id,
                            AlertLevel.ORANGE,
                            metric_type,
                            f"Symptom severity increased by {increase_percentage:.1f}% over recent sessions",
                            ["Review treatment approach", "Consider intensifying interventions", "Assess for external stressors"]
                        )
            
            # Check homework compliance
            elif metric_type == ProgressMetricType.HOMEWORK_COMPLIANCE:
                if len(recent_data) >= 4:
                    avg_compliance = sum(point[0] for point in recent_data[:4]) / 4
                    threshold = self.alert_criteria["low_homework_compliance"]["completion_rate"]
                    
                    if avg_compliance < threshold:
                        self._create_alert(
                            patient_id,
                            AlertLevel.YELLOW,
                            metric_type,
                            f"Low homework completion rate: {avg_compliance:.1%}",
                            ["Explore barriers to homework completion", "Simplify assignments", "Increase motivation"]
                        )
            
            # Check session engagement
            elif metric_type == ProgressMetricType.SESSION_ENGAGEMENT:
                if len(recent_data) >= 3:
                    avg_engagement = sum(point[0] for point in recent_data[:3]) / 3
                    
                    if avg_engagement < 4.0:  # Below fair threshold
                        self._create_alert(
                            patient_id,
                            AlertLevel.YELLOW,
                            metric_type,
                            f"Low session engagement: {avg_engagement:.1f}/10",
                            ["Explore therapeutic alliance", "Adjust intervention approach", "Address motivation"]
                        )
            
        except Exception as e:
            self.logger.error(f"Error checking progress alerts: {e}")
    
    def _create_alert(self, patient_id: str, alert_level: AlertLevel, 
                     metric_type: ProgressMetricType, description: str, 
                     recommendations: List[str]):
        """Create progress alert"""
        
        try:
            alert_id = f"ALERT_{patient_id}_{metric_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            alert = ProgressAlert(
                alert_id=alert_id,
                patient_id=patient_id,
                alert_level=alert_level,
                metric_type=metric_type,
                description=description,
                recommendations=recommendations,
                created_date=datetime.now()
            )
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO progress_alerts (
                        alert_id, patient_id, alert_level, metric_type, description,
                        recommendations, created_date, acknowledged, resolved
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    alert.alert_id,
                    alert.patient_id,
                    alert.alert_level.value,
                    alert.metric_type.value,
                    alert.description,
                    json.dumps(alert.recommendations),
                    alert.created_date.isoformat(),
                    alert.acknowledged,
                    alert.resolved
                ))
                
                conn.commit()
            
            self.logger.info(f"Created progress alert: {alert_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to create alert: {e}")
    
    def get_progress_summary(self, patient_id: str, days_lookback: int = 30) -> Optional[ProgressSummary]:
        """Generate comprehensive progress summary"""
        
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=days_lookback)
            
            # Calculate trends
            trends = self.calculate_progress_trends(patient_id, days_lookback=days_lookback)
            
            # Determine overall trend
            overall_trend = self._determine_overall_trend(trends)
            
            # Get key improvements and concerns
            key_improvements = []
            areas_of_concern = []
            
            for trend in trends:
                if trend.direction == TrendDirection.IMPROVING:
                    key_improvements.append(f"{trend.metric_type.value}: {trend.change_percentage:.1f}% improvement")
                elif trend.direction == TrendDirection.DECLINING:
                    areas_of_concern.append(f"{trend.metric_type.value}: {trend.change_percentage:.1f}% decline")
            
            # Calculate completion rates
            goal_completion_rate = self._calculate_goal_completion_rate(patient_id)
            session_attendance_rate = self._calculate_attendance_rate(patient_id, days_lookback)
            homework_completion_rate = self._calculate_homework_completion_rate(patient_id, days_lookback)
            
            # Determine risk level trend
            risk_trend = self._get_risk_level_trend(patient_id, days_lookback)
            
            # Determine treatment response
            treatment_response = self._assess_treatment_response(trends, goal_completion_rate)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(trends, areas_of_concern, 
                                                           homework_completion_rate, session_attendance_rate)
            
            return ProgressSummary(
                patient_id=patient_id,
                assessment_period_start=start_date,
                assessment_period_end=end_date,
                overall_trend=overall_trend,
                key_improvements=key_improvements,
                areas_of_concern=areas_of_concern,
                goal_completion_rate=goal_completion_rate,
                session_attendance_rate=session_attendance_rate,
                homework_completion_rate=homework_completion_rate,
                risk_level_trend=risk_trend,
                treatment_response=treatment_response,
                recommendations=recommendations,
                next_review_date=end_date + timedelta(days=14)
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate progress summary: {e}")
            return None
    
    def _determine_overall_trend(self, trends: List[ProgressTrend]) -> TrendDirection:
        """Determine overall trend from multiple metrics"""
        
        if not trends:
            return TrendDirection.INSUFFICIENT_DATA
        
        improving_count = sum(1 for trend in trends if trend.direction == TrendDirection.IMPROVING)
        declining_count = sum(1 for trend in trends if trend.direction == TrendDirection.DECLINING)
        stable_count = sum(1 for trend in trends if trend.direction == TrendDirection.STABLE)
        
        total_trends = len(trends)
        
        if improving_count / total_trends > 0.6:
            return TrendDirection.IMPROVING
        elif declining_count / total_trends > 0.6:
            return TrendDirection.DECLINING
        elif stable_count / total_trends > 0.6:
            return TrendDirection.STABLE
        else:
            return TrendDirection.MIXED
    
    def _calculate_goal_completion_rate(self, patient_id: str) -> float:
        """Calculate goal completion rate"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT COUNT(*) as total_goals,
                           SUM(CASE WHEN status = 'achieved' THEN 1 ELSE 0 END) as completed_goals
                    FROM goal_progress WHERE patient_id = ?
                """, (patient_id,))
                
                result = cursor.fetchone()
                if result and result[0] > 0:
                    return (result[1] / result[0]) * 100
                
            return 0.0
            
        except Exception as e:
            self.logger.error(f"Error calculating goal completion rate: {e}")
            return 0.0
    
    def _calculate_attendance_rate(self, patient_id: str, days_lookback: int) -> float:
        """Calculate session attendance rate"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                start_date = (datetime.now() - timedelta(days=days_lookback)).isoformat()
                
                cursor.execute("""
                    SELECT COUNT(*) as attended FROM session_progress
                    WHERE patient_id = ? AND session_date >= ?
                """, (patient_id, start_date))
                
                attended = cursor.fetchone()[0] or 0
                
                # Estimate expected sessions (assuming weekly)
                expected_sessions = max(days_lookback // 7, 1)
                
                return min((attended / expected_sessions) * 100, 100.0)
                
        except Exception as e:
            self.logger.error(f"Error calculating attendance rate: {e}")
            return 0.0
    
    def _calculate_homework_completion_rate(self, patient_id: str, days_lookback: int) -> float:
        """Calculate homework completion rate"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                start_date = (datetime.now() - timedelta(days=days_lookback)).isoformat()
                
                cursor.execute("""
                    SELECT AVG(value) FROM progress_data
                    WHERE patient_id = ? AND metric_type = ? AND timestamp >= ?
                """, (patient_id, ProgressMetricType.HOMEWORK_COMPLIANCE.value, start_date))
                
                result = cursor.fetchone()[0]
                return (result * 100) if result else 0.0
                
        except Exception as e:
            self.logger.error(f"Error calculating homework completion rate: {e}")
            return 0.0
    
    def _get_risk_level_trend(self, patient_id: str, days_lookback: int) -> TrendDirection:
        """Get trend in risk level"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                start_date = (datetime.now() - timedelta(days=days_lookback)).isoformat()
                
                cursor.execute("""
                    SELECT value, timestamp FROM progress_data
                    WHERE patient_id = ? AND metric_type = ? AND timestamp >= ?
                    ORDER BY timestamp
                """, (patient_id, ProgressMetricType.RISK_LEVEL.value, start_date))
                
                risk_data = cursor.fetchall()
                
                if len(risk_data) < 2:
                    return TrendDirection.INSUFFICIENT_DATA
                
                first_risk = risk_data[0][0]
                last_risk = risk_data[-1][0]
                
                if last_risk < first_risk:
                    return TrendDirection.IMPROVING
                elif last_risk > first_risk:
                    return TrendDirection.DECLINING
                else:
                    return TrendDirection.STABLE
                    
        except Exception as e:
            self.logger.error(f"Error getting risk level trend: {e}")
            return TrendDirection.INSUFFICIENT_DATA
    
    def _assess_treatment_response(self, trends: List[ProgressTrend], goal_completion_rate: float) -> str:
        """Assess overall treatment response"""
        
        improving_trends = [t for t in trends if t.direction == TrendDirection.IMPROVING]
        declining_trends = [t for t in trends if t.direction == TrendDirection.DECLINING]
        
        # Calculate weighted improvement score
        improvement_score = 0
        for trend in improving_trends:
            if trend.metric_type in [ProgressMetricType.SYMPTOM_SEVERITY, ProgressMetricType.RISK_LEVEL]:
                improvement_score += trend.change_percentage * 2  # Weight symptom improvement higher
            else:
                improvement_score += trend.change_percentage
        
        # Subtract for declining trends
        for trend in declining_trends:
            if trend.metric_type in [ProgressMetricType.SYMPTOM_SEVERITY, ProgressMetricType.RISK_LEVEL]:
                improvement_score -= trend.change_percentage * 2
            else:
                improvement_score -= trend.change_percentage
        
        # Factor in goal completion
        improvement_score += goal_completion_rate
        
        if improvement_score > 50:
            return "excellent"
        elif improvement_score > 25:
            return "good"
        elif improvement_score > 0:
            return "partial"
        elif improvement_score > -25:
            return "poor"
        else:
            return "deteriorating"
    
    def _generate_recommendations(self, trends: List[ProgressTrend], areas_of_concern: List[str],
                                homework_completion_rate: float, session_attendance_rate: float) -> List[str]:
        """Generate recommendations based on progress analysis"""
        
        recommendations = []
        
        # Address declining trends
        declining_symptoms = any(t.metric_type == ProgressMetricType.SYMPTOM_SEVERITY and 
                               t.direction == TrendDirection.DECLINING for t in trends)
        
        if declining_symptoms:
            recommendations.extend([
                "Review and adjust treatment approach",
                "Consider increasing session frequency",
                "Assess for external stressors or life changes",
                "Evaluate medication effectiveness if applicable"
            ])
        
        # Address low engagement
        low_engagement = any(t.metric_type == ProgressMetricType.SESSION_ENGAGEMENT and
                           t.current_value < 5.0 for t in trends)
        
        if low_engagement:
            recommendations.extend([
                "Explore therapeutic alliance and rapport",
                "Adjust therapeutic approach to better match patient preferences",
                "Address motivation and treatment goals"
            ])
        
        # Address homework compliance
        if homework_completion_rate < 50:
            recommendations.extend([
                "Simplify homework assignments",
                "Explore barriers to completion",
                "Increase motivation and relevance of assignments"
            ])
        
        # Address attendance issues
        if session_attendance_rate < 80:
            recommendations.extend([
                "Address barriers to session attendance",
                "Consider flexible scheduling options",
                "Explore motivation for treatment"
            ])
        
        # Positive reinforcement for improvements
        improving_trends = [t for t in trends if t.direction == TrendDirection.IMPROVING]
        if improving_trends:
            recommendations.append("Continue current successful interventions")
        
        return recommendations
    
    def get_active_alerts(self, patient_id: str) -> List[ProgressAlert]:
        """Get active alerts for patient"""
        
        alerts = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM progress_alerts
                    WHERE patient_id = ? AND resolved = 0
                    ORDER BY created_date DESC
                """, (patient_id,))
                
                for row in cursor.fetchall():
                    alert = ProgressAlert(
                        alert_id=row[0],
                        patient_id=row[1],
                        alert_level=AlertLevel(row[2]),
                        metric_type=ProgressMetricType(row[3]),
                        description=row[4],
                        recommendations=json.loads(row[5]) if row[5] else [],
                        created_date=datetime.fromisoformat(row[6]),
                        acknowledged=bool(row[7]),
                        resolved=bool(row[8]),
                        resolution_notes=row[9] or ""
                    )
                    alerts.append(alert)
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Error getting active alerts: {e}")
            return []
    
    def resolve_alert(self, alert_id: str, resolution_notes: str = "") -> bool:
        """Resolve progress alert"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE progress_alerts SET resolved = 1, resolution_notes = ?
                    WHERE alert_id = ?
                """, (resolution_notes, alert_id))
                
                conn.commit()
            
            self.logger.info(f"Resolved alert: {alert_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to resolve alert: {e}")
            return False
    
    def get_progress_dashboard(self, patient_id: str) -> Dict[str, Any]:
        """Get comprehensive progress dashboard data"""
        
        try:
            # Get progress summary
            summary = self.get_progress_summary(patient_id)
            
            # Get recent trends
            trends = self.calculate_progress_trends(patient_id, days_lookback=30)
            
            # Get active alerts
            alerts = self.get_active_alerts(patient_id)
            
            # Get recent session progress
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM session_progress
                    WHERE patient_id = ?
                    ORDER BY session_date DESC LIMIT 5
                """, (patient_id,))
                
                recent_sessions = []
                for row in cursor.fetchall():
                    session = {
                        'session_id': row[0],
                        'session_number': row[2],
                        'session_date': row[3],
                        'pre_session_mood': row[4],
                        'post_session_mood': row[5],
                        'engagement_level': row[6],
                        'homework_completion': row[7],
                        'skills_practiced': json.loads(row[8]) if row[8] else [],
                        'breakthrough_moments': json.loads(row[9]) if row[9] else []
                    }
                    recent_sessions.append(session)
            
            # Get goal progress
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT goal_text, progress_percentage, status, target_date
                    FROM goal_progress WHERE patient_id = ? AND status = 'active'
                """, (patient_id,))
                
                active_goals = [
                    {
                        'goal_text': row[0],
                        'progress_percentage': row[1],
                        'status': row[2],
                        'target_date': row[3]
                    }
                    for row in cursor.fetchall()
                ]
            
            dashboard = {
                'patient_id': patient_id,
                'summary': summary.__dict__ if summary else None,
                'trends': [
                    {
                        'metric_type': trend.metric_type.value,
                        'direction': trend.direction.value,
                        'change_percentage': trend.change_percentage,
                        'confidence': trend.confidence
                    }
                    for trend in trends
                ],
                'alerts': [
                    {
                        'alert_level': alert.alert_level.value,
                        'description': alert.description,
                        'metric_type': alert.metric_type.value,
                        'created_date': alert.created_date.isoformat()
                    }
                    for alert in alerts
                ],
                'recent_sessions': recent_sessions,
                'active_goals': active_goals,
                'key_metrics': {
                    'session_attendance_rate': summary.session_attendance_rate if summary else 0,
                    'homework_completion_rate': summary.homework_completion_rate if summary else 0,
                    'goal_completion_rate': summary.goal_completion_rate if summary else 0,
                    'overall_trend': summary.overall_trend.value if summary else 'insufficient_data'
                }
            }
            
            return dashboard
            
        except Exception as e:
            self.logger.error(f"Error generating progress dashboard: {e}")
            return {}
    
    def export_progress_report(self, patient_id: str, days_lookback: int = 90) -> str:
        """Export comprehensive progress report"""
        
        try:
            dashboard = self.get_progress_dashboard(patient_id)
            summary = self.get_progress_summary(patient_id, days_lookback)
            
            if not summary:
                return "Insufficient data for progress report"
            
            report_sections = []
            
            # Header
            report_sections.append("THERAPY PROGRESS REPORT")
            report_sections.append("=" * 50)
            report_sections.append(f"Patient ID: {patient_id}")
            report_sections.append(f"Assessment Period: {summary.assessment_period_start} to {summary.assessment_period_end}")
            report_sections.append(f"Overall Trend: {summary.overall_trend.value.replace('_', ' ').title()}")
            report_sections.append(f"Treatment Response: {summary.treatment_response.title()}")
            report_sections.append("")
            
            # Key Metrics
            report_sections.append("KEY METRICS:")
            report_sections.append(f"  Session Attendance Rate: {summary.session_attendance_rate:.1f}%")
            report_sections.append(f"  Homework Completion Rate: {summary.homework_completion_rate:.1f}%")
            report_sections.append(f"  Goal Completion Rate: {summary.goal_completion_rate:.1f}%")
            report_sections.append(f"  Risk Level Trend: {summary.risk_level_trend.value.replace('_', ' ').title()}")
            report_sections.append("")
            
            # Improvements
            if summary.key_improvements:
                report_sections.append("KEY IMPROVEMENTS:")
                for improvement in summary.key_improvements:
                    report_sections.append(f"  ✓ {improvement}")
                report_sections.append("")
            
            # Areas of Concern
            if summary.areas_of_concern:
                report_sections.append("AREAS OF CONCERN:")
                for concern in summary.areas_of_concern:
                    report_sections.append(f"  ⚠ {concern}")
                report_sections.append("")
            
            # Active Alerts
            alerts = dashboard.get('alerts', [])
            if alerts:
                report_sections.append("ACTIVE ALERTS:")
                for alert in alerts:
                    report_sections.append(f"  {alert['alert_level'].upper()}: {alert['description']}")
                report_sections.append("")
            
            # Recommendations
            if summary.recommendations:
                report_sections.append("RECOMMENDATIONS:")
                for i, rec in enumerate(summary.recommendations, 1):
                    report_sections.append(f"  {i}. {rec}")
                report_sections.append("")
            
            # Next Review
            report_sections.append(f"Next Progress Review: {summary.next_review_date}")
            
            return "\n".join(report_sections)
            
        except Exception as e:
            self.logger.error(f"Error exporting progress report: {e}")
            return "Error generating progress report"


# Example usage and testing
if __name__ == "__main__":
    print("=== PROGRESS TRACKER SYSTEM DEMONSTRATION ===\n")
    
    # Initialize progress tracker
    tracker = ProgressTracker()
    
    # Sample patient ID
    patient_id = "PT_20240101_ABC123"
    
    print("Adding sample progress data...")
    
    # Add sample progress data points
    progress_data = [
        (ProgressMetricType.SYMPTOM_SEVERITY, 18.0, 1, "PHQ-9 baseline"),
        (ProgressMetricType.SYMPTOM_SEVERITY, 15.0, 3, "PHQ-9 week 3"),
        (ProgressMetricType.SYMPTOM_SEVERITY, 12.0, 6, "PHQ-9 week 6"),
        (ProgressMetricType.SYMPTOM_SEVERITY, 8.0, 9, "PHQ-9 week 9"),
        (ProgressMetricType.HOMEWORK_COMPLIANCE, 0.8, 2, "Week 2 homework"),
        (ProgressMetricType.HOMEWORK_COMPLIANCE, 0.6, 3, "Week 3 homework"),
        (ProgressMetricType.HOMEWORK_COMPLIANCE, 0.9, 4, "Week 4 homework"),
        (ProgressMetricType.SESSION_ENGAGEMENT, 7.0, 2, "Therapist rating"),
        (ProgressMetricType.SESSION_ENGAGEMENT, 8.0, 3, "Therapist rating"),
        (ProgressMetricType.SESSION_ENGAGEMENT, 8.5, 4, "Therapist rating"),
    ]
    
    for metric_type, value, session_num, notes in progress_data:
        tracker.add_progress_data(patient_id, metric_type, value, session_num, "assessment", notes)
    
    # Add session progress
    session_progress = SessionProgress(
        session_id=f"{patient_id}_SESSION_004",
        session_number=4,
        session_date=datetime.now(),
        pre_session_mood=6,
        post_session_mood=7,
        engagement_level=8,
        homework_completion=0.9,
        skills_practiced=["cognitive_restructuring", "mindfulness"],
        breakthrough_moments=["Connected thought patterns to mood"],
        therapist_observations="Excellent progress, very engaged",
        patient_feedback="Feeling more hopeful"
    )
    
    tracker.add_session_progress(session_progress)
    
    # Update goal progress
    tracker.update_goal_progress(
        patient_id, 
        "GOAL_001", 
        75.0, 
        milestone="Reduced PHQ-9 score below 10",
        interventions_used=["CBT", "behavioral_activation"]
    )
    
    # Calculate trends
    print("Calculating progress trends...")
    trends = tracker.calculate_progress_trends(patient_id)
    
    print(f"Found {len(trends)} trends:")
    for trend in trends:
        print(f"  {trend.metric_type.value}: {trend.direction.value} "
              f"({trend.change_percentage:.1f}% change, confidence: {trend.confidence:.2f})")
    
    # Get progress summary
    print("\n=== PROGRESS SUMMARY ===")
    summary = tracker.get_progress_summary(patient_id)
    
    if summary:
        print(f"Overall Trend: {summary.overall_trend.value}")
        print(f"Treatment Response: {summary.treatment_response}")
        print(f"Key Improvements: {summary.key_improvements}")
        print(f"Areas of Concern: {summary.areas_of_concern}")
        print(f"Session Attendance: {summary.session_attendance_rate:.1f}%")
        print(f"Homework Completion: {summary.homework_completion_rate:.1f}%")
        print(f"Goal Completion: {summary.goal_completion_rate:.1f}%")
    
    # Get active alerts
    print("\n=== ACTIVE ALERTS ===")
    alerts = tracker.get_active_alerts(patient_id)
    
    if alerts:
        for alert in alerts:
            print(f"  {alert.alert_level.value.upper()}: {alert.description}")
    else:
        print("  No active alerts")
    
    # Get progress dashboard
    print("\n=== PROGRESS DASHBOARD ===")
    dashboard = tracker.get_progress_dashboard(patient_id)
    
    print(f"Dashboard metrics: {dashboard.get('key_metrics', {})}")
    print(f"Recent sessions: {len(dashboard.get('recent_sessions', []))}")
    print(f"Active goals: {len(dashboard.get('active_goals', []))}")
    
    # Export progress report
    print("\n=== PROGRESS REPORT ===")
    report = tracker.export_progress_report(patient_id)
    print(report)
    
    print("\n" + "="*60)
    print("Progress tracker system demonstration complete!")
    print("Comprehensive progress monitoring with trend analysis and alerts.")
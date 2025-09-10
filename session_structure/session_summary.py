from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import sqlite3
import json


class SummaryType(Enum):
    SESSION_SUMMARY = "session_summary"
    PROGRESS_SUMMARY = "progress_summary"
    TREATMENT_SUMMARY = "treatment_summary"
    CRISIS_SUMMARY = "crisis_summary"
    OUTCOME_SUMMARY = "outcome_summary"


class ProgressDirection(Enum):
    SIGNIFICANT_IMPROVEMENT = "significant_improvement"
    MODERATE_IMPROVEMENT = "moderate_improvement"
    SLIGHT_IMPROVEMENT = "slight_improvement"
    NO_CHANGE = "no_change"
    SLIGHT_DECLINE = "slight_decline"
    MODERATE_DECLINE = "moderate_decline"
    SIGNIFICANT_DECLINE = "significant_decline"


class InterventionEffectiveness(Enum):
    HIGHLY_EFFECTIVE = "highly_effective"
    MODERATELY_EFFECTIVE = "moderately_effective"
    SOMEWHAT_EFFECTIVE = "somewhat_effective"
    MINIMALLY_EFFECTIVE = "minimally_effective"
    NOT_EFFECTIVE = "not_effective"
    COUNTERPRODUCTIVE = "counterproductive"


@dataclass
class SessionSummary:
    session_id: str
    patient_id: str
    therapist_id: str
    session_date: datetime
    session_number: int
    therapy_modality: str
    session_duration: int
    attendance_status: str
    mood_assessment: Dict[str, Any]
    interventions_used: List[str]
    goals_addressed: List[str]
    homework_reviewed: bool
    homework_assigned: bool
    crisis_addressed: bool
    safety_concerns: List[str]
    key_insights: List[str]
    therapeutic_breakthroughs: List[str]
    challenges_encountered: List[str]
    patient_engagement: int
    session_effectiveness: int
    progress_indicators: Dict[str, Any]
    next_session_focus: List[str]
    clinical_observations: str
    patient_feedback: str
    therapist_reflections: str
    summary_type: SummaryType = SummaryType.SESSION_SUMMARY
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ProgressSummary:
    patient_id: str
    period_start: datetime
    period_end: datetime
    total_sessions: int
    sessions_attended: int
    attendance_rate: float
    primary_goals: List[str]
    goal_progress: Dict[str, int]
    overall_progress: ProgressDirection
    significant_changes: List[str]
    intervention_effectiveness: Dict[str, InterventionEffectiveness]
    homework_compliance: float
    crisis_episodes: int
    safety_improvements: List[str]
    symptom_changes: Dict[str, str]
    functional_improvements: List[str]
    remaining_challenges: List[str]
    treatment_recommendations: List[str]
    next_phase_goals: List[str]


@dataclass
class TherapeuticMilestone:
    milestone_id: str
    patient_id: str
    achievement_date: datetime
    milestone_type: str
    description: str
    significance_level: int
    supporting_evidence: List[str]
    impact_on_treatment: str


class SessionSummarySystem:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.summary_templates = self._initialize_summary_templates()
        self.progress_indicators = self._initialize_progress_indicators()
        self.milestone_criteria = self._initialize_milestone_criteria()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_summaries (
                    session_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    therapist_id TEXT NOT NULL,
                    session_date TEXT NOT NULL,
                    session_number INTEGER,
                    therapy_modality TEXT,
                    session_duration INTEGER,
                    attendance_status TEXT,
                    mood_assessment TEXT,
                    interventions_used TEXT,
                    goals_addressed TEXT,
                    homework_reviewed BOOLEAN,
                    homework_assigned BOOLEAN,
                    crisis_addressed BOOLEAN,
                    safety_concerns TEXT,
                    key_insights TEXT,
                    therapeutic_breakthroughs TEXT,
                    challenges_encountered TEXT,
                    patient_engagement INTEGER,
                    session_effectiveness INTEGER,
                    progress_indicators TEXT,
                    next_session_focus TEXT,
                    clinical_observations TEXT,
                    patient_feedback TEXT,
                    therapist_reflections TEXT,
                    summary_type TEXT,
                    created_at TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS progress_summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    period_start TEXT NOT NULL,
                    period_end TEXT NOT NULL,
                    total_sessions INTEGER,
                    sessions_attended INTEGER,
                    attendance_rate REAL,
                    primary_goals TEXT,
                    goal_progress TEXT,
                    overall_progress TEXT,
                    significant_changes TEXT,
                    intervention_effectiveness TEXT,
                    homework_compliance REAL,
                    crisis_episodes INTEGER,
                    safety_improvements TEXT,
                    symptom_changes TEXT,
                    functional_improvements TEXT,
                    remaining_challenges TEXT,
                    treatment_recommendations TEXT,
                    next_phase_goals TEXT,
                    created_at TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS therapeutic_milestones (
                    milestone_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    achievement_date TEXT NOT NULL,
                    milestone_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    significance_level INTEGER,
                    supporting_evidence TEXT,
                    impact_on_treatment TEXT,
                    created_at TEXT
                )
            """)
    
    def _initialize_summary_templates(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "session_summary_template": {
                "required_sections": [
                    "Session Overview",
                    "Mood and Functioning Assessment",
                    "Interventions and Techniques",
                    "Goal Progress",
                    "Homework Review and Assignment",
                    "Clinical Observations",
                    "Next Session Planning"
                ],
                "assessment_scales": {
                    "patient_engagement": "1-10 scale (1=no engagement, 10=highly engaged)",
                    "session_effectiveness": "1-10 scale (1=not effective, 10=highly effective)",
                    "mood_rating": "1-10 scale (1=very low, 10=very high)"
                }
            },
            
            "progress_summary_template": {
                "time_periods": ["weekly", "monthly", "quarterly", "treatment_phase"],
                "progress_metrics": [
                    "Goal achievement percentage",
                    "Symptom severity changes",
                    "Functional improvement indicators",
                    "Homework compliance rates",
                    "Session attendance patterns"
                ],
                "outcome_measures": [
                    "Standardized assessment scores",
                    "Clinical rating scales",
                    "Patient self-report measures",
                    "Behavioral observations"
                ]
            },
            
            "crisis_summary_template": {
                "crisis_elements": [
                    "Crisis triggers and precipitants",
                    "Risk assessment and safety measures",
                    "Interventions implemented",
                    "Support systems activated",
                    "Outcome and resolution",
                    "Lessons learned and prevention"
                ]
            }
        }
    
    def _initialize_progress_indicators(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "mood_indicators": {
                "improvement_signs": [
                    "Increased mood ratings over time",
                    "More positive emotional expressions",
                    "Reduced mood swings or instability",
                    "Better emotional regulation",
                    "Increased enjoyment in activities"
                ],
                "decline_signs": [
                    "Decreasing mood ratings",
                    "Increased negative emotions",
                    "Mood instability or volatility",
                    "Emotional numbing or withdrawal",
                    "Loss of interest in activities"
                ]
            },
            
            "behavioral_indicators": {
                "improvement_signs": [
                    "Increased activity levels",
                    "Better self-care behaviors",
                    "Improved social engagement",
                    "Reduced avoidance behaviors",
                    "Increased goal-directed activities"
                ],
                "decline_signs": [
                    "Decreased activity levels",
                    "Neglect of self-care",
                    "Social withdrawal",
                    "Increased avoidance",
                    "Reduced motivation"
                ]
            },
            
            "cognitive_indicators": {
                "improvement_signs": [
                    "More balanced thinking patterns",
                    "Reduced negative thought frequency",
                    "Improved problem-solving",
                    "Increased cognitive flexibility",
                    "Better concentration and focus"
                ],
                "decline_signs": [
                    "Increased negative thinking",
                    "Cognitive rigidity",
                    "Poor concentration",
                    "Impaired decision-making",
                    "Rumination or obsessive thoughts"
                ]
            },
            
            "functional_indicators": {
                "improvement_signs": [
                    "Better work or school performance",
                    "Improved relationships",
                    "Increased independence",
                    "Better daily functioning",
                    "Achievement of personal goals"
                ],
                "decline_signs": [
                    "Work or school difficulties",
                    "Relationship problems",
                    "Increased dependence",
                    "Functional impairment",
                    "Goal abandonment"
                ]
            }
        }
    
    def _initialize_milestone_criteria(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "treatment_engagement": {
                "first_session_completion": {
                    "significance": 3,
                    "description": "Successfully completed initial therapy session"
                },
                "consistent_attendance": {
                    "significance": 4,
                    "description": "Attended 80% or more sessions over 4-week period"
                },
                "therapeutic_alliance": {
                    "significance": 5,
                    "description": "Established strong therapeutic relationship"
                }
            },
            
            "skill_development": {
                "first_skill_demonstration": {
                    "significance": 4,
                    "description": "First successful demonstration of therapeutic skill"
                },
                "independent_skill_use": {
                    "significance": 6,
                    "description": "Used therapeutic skills independently outside session"
                },
                "skill_generalization": {
                    "significance": 7,
                    "description": "Applied skills across multiple life domains"
                }
            },
            
            "symptom_improvement": {
                "first_mood_improvement": {
                    "significance": 5,
                    "description": "First significant improvement in mood ratings"
                },
                "sustained_improvement": {
                    "significance": 7,
                    "description": "Maintained improvement for 4+ weeks"
                },
                "symptom_remission": {
                    "significance": 9,
                    "description": "Achieved clinical remission of primary symptoms"
                }
            },
            
            "behavioral_changes": {
                "first_behavior_change": {
                    "significance": 5,
                    "description": "First successful behavioral modification"
                },
                "habit_formation": {
                    "significance": 6,
                    "description": "Established new positive behavioral patterns"
                },
                "lifestyle_changes": {
                    "significance": 8,
                    "description": "Made significant positive lifestyle modifications"
                }
            },
            
            "crisis_management": {
                "crisis_survived": {
                    "significance": 6,
                    "description": "Successfully navigated crisis without self-harm"
                },
                "crisis_skills_used": {
                    "significance": 7,
                    "description": "Independently used crisis management skills"
                },
                "crisis_prevention": {
                    "significance": 8,
                    "description": "Prevented crisis through early intervention"
                }
            }
        }
    
    def create_session_summary(self, session_data: Dict[str, Any]) -> SessionSummary:
        
        summary = SessionSummary(
            session_id=session_data["session_id"],
            patient_id=session_data["patient_id"],
            therapist_id=session_data["therapist_id"],
            session_date=datetime.fromisoformat(session_data["session_date"]),
            session_number=session_data["session_number"],
            therapy_modality=session_data.get("therapy_modality", ""),
            session_duration=session_data.get("session_duration", 50),
            attendance_status=session_data.get("attendance_status", "attended"),
            mood_assessment=session_data.get("mood_assessment", {}),
            interventions_used=session_data.get("interventions_used", []),
            goals_addressed=session_data.get("goals_addressed", []),
            homework_reviewed=session_data.get("homework_reviewed", False),
            homework_assigned=session_data.get("homework_assigned", False),
            crisis_addressed=session_data.get("crisis_addressed", False),
            safety_concerns=session_data.get("safety_concerns", []),
            key_insights=session_data.get("key_insights", []),
            therapeutic_breakthroughs=session_data.get("therapeutic_breakthroughs", []),
            challenges_encountered=session_data.get("challenges_encountered", []),
            patient_engagement=session_data.get("patient_engagement", 0),
            session_effectiveness=session_data.get("session_effectiveness", 0),
            progress_indicators=session_data.get("progress_indicators", {}),
            next_session_focus=session_data.get("next_session_focus", []),
            clinical_observations=session_data.get("clinical_observations", ""),
            patient_feedback=session_data.get("patient_feedback", ""),
            therapist_reflections=session_data.get("therapist_reflections", "")
        )
        
        self._save_session_summary(summary)
        self._check_for_milestones(summary)
        
        return summary
    
    def generate_progress_summary(self, patient_id: str, start_date: datetime, 
                                end_date: datetime) -> ProgressSummary:
        
        sessions_data = self._get_sessions_in_period(patient_id, start_date, end_date)
        
        if not sessions_data:
            raise ValueError("No sessions found for the specified period")
        
        total_sessions = len(sessions_data)
        attended_sessions = len([s for s in sessions_data if s.get("attendance_status") == "attended"])
        attendance_rate = (attended_sessions / total_sessions) * 100 if total_sessions > 0 else 0
        
        goal_progress = self._analyze_goal_progress(sessions_data)
        overall_progress = self._determine_overall_progress(sessions_data)
        intervention_effectiveness = self._analyze_intervention_effectiveness(sessions_data)
        homework_compliance = self._calculate_homework_compliance(sessions_data)
        crisis_episodes = len([s for s in sessions_data if s.get("crisis_addressed", False)])
        
        progress_summary = ProgressSummary(
            patient_id=patient_id,
            period_start=start_date,
            period_end=end_date,
            total_sessions=total_sessions,
            sessions_attended=attended_sessions,
            attendance_rate=attendance_rate,
            primary_goals=self._extract_primary_goals(sessions_data),
            goal_progress=goal_progress,
            overall_progress=overall_progress,
            significant_changes=self._identify_significant_changes(sessions_data),
            intervention_effectiveness=intervention_effectiveness,
            homework_compliance=homework_compliance,
            crisis_episodes=crisis_episodes,
            safety_improvements=self._identify_safety_improvements(sessions_data),
            symptom_changes=self._analyze_symptom_changes(sessions_data),
            functional_improvements=self._identify_functional_improvements(sessions_data),
            remaining_challenges=self._identify_remaining_challenges(sessions_data),
            treatment_recommendations=self._generate_treatment_recommendations(sessions_data),
            next_phase_goals=self._suggest_next_phase_goals(sessions_data)
        )
        
        self._save_progress_summary(progress_summary)
        return progress_summary
    
    def _analyze_goal_progress(self, sessions_data: List[Dict[str, Any]]) -> Dict[str, int]:
        
        goal_mentions = {}
        goal_progress = {}
        
        for session in sessions_data:
            goals = session.get("goals_addressed", [])
            progress_indicators = session.get("progress_indicators", {})
            
            for goal in goals:
                if goal not in goal_mentions:
                    goal_mentions[goal] = 0
                    goal_progress[goal] = []
                
                goal_mentions[goal] += 1
                
                if goal in progress_indicators:
                    goal_progress[goal].append(progress_indicators[goal])
        
        final_progress = {}
        for goal, progress_list in goal_progress.items():
            if progress_list:
                final_progress[goal] = int(sum(progress_list) / len(progress_list))
            else:
                final_progress[goal] = 0
        
        return final_progress
    
    def _determine_overall_progress(self, sessions_data: List[Dict[str, Any]]) -> ProgressDirection:
        
        if len(sessions_data) < 2:
            return ProgressDirection.NO_CHANGE
        
        early_sessions = sessions_data[:len(sessions_data)//2]
        recent_sessions = sessions_data[len(sessions_data)//2:]
        
        early_effectiveness = sum(s.get("session_effectiveness", 0) for s in early_sessions) / len(early_sessions)
        recent_effectiveness = sum(s.get("session_effectiveness", 0) for s in recent_sessions) / len(recent_sessions)
        
        difference = recent_effectiveness - early_effectiveness
        
        if difference >= 2:
            return ProgressDirection.SIGNIFICANT_IMPROVEMENT
        elif difference >= 1:
            return ProgressDirection.MODERATE_IMPROVEMENT
        elif difference >= 0.5:
            return ProgressDirection.SLIGHT_IMPROVEMENT
        elif difference >= -0.5:
            return ProgressDirection.NO_CHANGE
        elif difference >= -1:
            return ProgressDirection.SLIGHT_DECLINE
        elif difference >= -2:
            return ProgressDirection.MODERATE_DECLINE
        else:
            return ProgressDirection.SIGNIFICANT_DECLINE
    
    def _analyze_intervention_effectiveness(self, sessions_data: List[Dict[str, Any]]) -> Dict[str, InterventionEffectiveness]:
        
        intervention_outcomes = {}
        
        for session in sessions_data:
            interventions = session.get("interventions_used", [])
            effectiveness = session.get("session_effectiveness", 0)
            
            for intervention in interventions:
                if intervention not in intervention_outcomes:
                    intervention_outcomes[intervention] = []
                intervention_outcomes[intervention].append(effectiveness)
        
        effectiveness_ratings = {}
        for intervention, outcomes in intervention_outcomes.items():
            avg_effectiveness = sum(outcomes) / len(outcomes)
            
            if avg_effectiveness >= 8:
                effectiveness_ratings[intervention] = InterventionEffectiveness.HIGHLY_EFFECTIVE
            elif avg_effectiveness >= 6:
                effectiveness_ratings[intervention] = InterventionEffectiveness.MODERATELY_EFFECTIVE
            elif avg_effectiveness >= 4:
                effectiveness_ratings[intervention] = InterventionEffectiveness.SOMEWHAT_EFFECTIVE
            elif avg_effectiveness >= 2:
                effectiveness_ratings[intervention] = InterventionEffectiveness.MINIMALLY_EFFECTIVE
            else:
                effectiveness_ratings[intervention] = InterventionEffectiveness.NOT_EFFECTIVE
        
        return effectiveness_ratings
    
    def _calculate_homework_compliance(self, sessions_data: List[Dict[str, Any]]) -> float:
        
        homework_sessions = [s for s in sessions_data if s.get("homework_assigned", False)]
        
        if not homework_sessions:
            return 0.0
        
        completed_homework = 0
        total_homework = 0
        
        for i, session in enumerate(homework_sessions):
            if i > 0:
                previous_session = homework_sessions[i-1]
                if previous_session.get("homework_assigned", False):
                    total_homework += 1
                    if session.get("homework_reviewed", False):
                        completed_homework += 1
        
        return (completed_homework / total_homework * 100) if total_homework > 0 else 0.0
    
    def _identify_significant_changes(self, sessions_data: List[Dict[str, Any]]) -> List[str]:
        
        changes = []
        
        if len(sessions_data) >= 3:
            early_mood = [s.get("mood_assessment", {}).get("rating", 0) for s in sessions_data[:3]]
            recent_mood = [s.get("mood_assessment", {}).get("rating", 0) for s in sessions_data[-3:]]
            
            early_avg = sum(early_mood) / len(early_mood) if early_mood else 0
            recent_avg = sum(recent_mood) / len(recent_mood) if recent_mood else 0
            
            mood_change = recent_avg - early_avg
            
            if mood_change >= 2:
                changes.append(f"Significant mood improvement (increased by {mood_change:.1f} points)")
            elif mood_change <= -2:
                changes.append(f"Concerning mood decline (decreased by {abs(mood_change):.1f} points)")
        
        breakthroughs = []
        for session in sessions_data:
            breakthroughs.extend(session.get("therapeutic_breakthroughs", []))
        
        if breakthroughs:
            changes.append(f"Therapeutic breakthroughs achieved: {len(breakthroughs)} instances")
        
        crisis_count = len([s for s in sessions_data if s.get("crisis_addressed", False)])
        if crisis_count > 0:
            changes.append(f"Crisis episodes addressed: {crisis_count}")
        
        return changes
    
    def _check_for_milestones(self, session_summary: SessionSummary):
        
        milestones_achieved = []
        
        if session_summary.session_number == 1:
            milestone = TherapeuticMilestone(
                milestone_id=f"{session_summary.patient_id}_first_session_{datetime.now().strftime('%Y%m%d')}",
                patient_id=session_summary.patient_id,
                achievement_date=session_summary.session_date,
                milestone_type="treatment_engagement",
                description="Successfully completed first therapy session",
                significance_level=3,
                supporting_evidence=["Session attended", "Initial engagement established"],
                impact_on_treatment="Foundation for therapeutic relationship established"
            )
            milestones_achieved.append(milestone)
        
        if session_summary.patient_engagement >= 8:
            milestone = TherapeuticMilestone(
                milestone_id=f"{session_summary.patient_id}_high_engagement_{session_summary.session_id}",
                patient_id=session_summary.patient_id,
                achievement_date=session_summary.session_date,
                milestone_type="treatment_engagement",
                description="Demonstrated high level of engagement in therapy",
                significance_level=5,
                supporting_evidence=[f"Engagement rating: {session_summary.patient_engagement}/10"],
                impact_on_treatment="Strong engagement facilitates therapeutic progress"
            )
            milestones_achieved.append(milestone)
        
        if session_summary.therapeutic_breakthroughs:
            for breakthrough in session_summary.therapeutic_breakthroughs:
                milestone = TherapeuticMilestone(
                    milestone_id=f"{session_summary.patient_id}_breakthrough_{session_summary.session_id}",
                    patient_id=session_summary.patient_id,
                    achievement_date=session_summary.session_date,
                    milestone_type="therapeutic_breakthrough",
                    description=f"Therapeutic breakthrough: {breakthrough}",
                    significance_level=7,
                    supporting_evidence=[breakthrough],
                    impact_on_treatment="Breakthrough moments accelerate therapeutic progress"
                )
                milestones_achieved.append(milestone)
        
        for milestone in milestones_achieved:
            self._save_milestone(milestone)
    
    def generate_session_narrative(self, session_summary: SessionSummary) -> str:
        
        narrative_parts = []
        
        narrative_parts.append(f"Session {session_summary.session_number} Summary")
        narrative_parts.append(f"Date: {session_summary.session_date.strftime('%B %d, %Y')}")
        narrative_parts.append(f"Duration: {session_summary.session_duration} minutes")
        narrative_parts.append("")
        
        if session_summary.mood_assessment:
            mood_rating = session_summary.mood_assessment.get("rating", 0)
            mood_desc = session_summary.mood_assessment.get("description", "")
            narrative_parts.append(f"Patient arrived with mood rating of {mood_rating}/10. {mood_desc}")
        
        if session_summary.attendance_status != "attended":
            narrative_parts.append(f"Session status: {session_summary.attendance_status}")
        
        if session_summary.crisis_addressed:
            narrative_parts.append("Crisis intervention was provided during this session.")
            if session_summary.safety_concerns:
                narrative_parts.append(f"Safety concerns addressed: {', '.join(session_summary.safety_concerns)}")
        
        if session_summary.homework_reviewed:
            narrative_parts.append("Previous homework assignment was reviewed.")
        
        if session_summary.interventions_used:
            narrative_parts.append(f"Therapeutic interventions included: {', '.join(session_summary.interventions_used)}")
        
        if session_summary.goals_addressed:
            narrative_parts.append(f"Session focused on goals: {', '.join(session_summary.goals_addressed)}")
        
        if session_summary.key_insights:
            narrative_parts.append("Key insights gained:")
            for insight in session_summary.key_insights:
                narrative_parts.append(f"- {insight}")
        
        if session_summary.therapeutic_breakthroughs:
            narrative_parts.append("Therapeutic breakthroughs:")
            for breakthrough in session_summary.therapeutic_breakthroughs:
                narrative_parts.append(f"- {breakthrough}")
        
        if session_summary.challenges_encountered:
            narrative_parts.append("Challenges encountered:")
            for challenge in session_summary.challenges_encountered:
                narrative_parts.append(f"- {challenge}")
        
        narrative_parts.append(f"Patient engagement: {session_summary.patient_engagement}/10")
        narrative_parts.append(f"Session effectiveness: {session_summary.session_effectiveness}/10")
        
        if session_summary.homework_assigned:
            narrative_parts.append("New homework assignment provided for practice between sessions.")
        
        if session_summary.next_session_focus:
            narrative_parts.append(f"Next session will focus on: {', '.join(session_summary.next_session_focus)}")
        
        if session_summary.clinical_observations:
            narrative_parts.append(f"Clinical observations: {session_summary.clinical_observations}")
        
        if session_summary.patient_feedback:
            narrative_parts.append(f"Patient feedback: {session_summary.patient_feedback}")
        
        return "\n".join(narrative_parts)
    
    def create_treatment_summary_report(self, patient_id: str, months: int = 3) -> Dict[str, Any]:
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        progress_summary = self.generate_progress_summary(patient_id, start_date, end_date)
        milestones = self._get_patient_milestones(patient_id, start_date, end_date)
        
        report = {
            "patient_id": patient_id,
            "report_period": f"{start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}",
            "treatment_summary": {
                "total_sessions": progress_summary.total_sessions,
                "attendance_rate": f"{progress_summary.attendance_rate:.1f}%",
                "overall_progress": progress_summary.overall_progress.value,
                "homework_compliance": f"{progress_summary.homework_compliance:.1f}%"
            },
            "goal_progress": progress_summary.goal_progress,
            "significant_achievements": [],
            "intervention_effectiveness": {k: v.value for k, v in progress_summary.intervention_effectiveness.items()},
            "milestones_achieved": len(milestones),
            "milestone_details": [
                {
                    "type": m.milestone_type,
                    "description": m.description,
                    "date": m.achievement_date.strftime('%B %d, %Y'),
                    "significance": m.significance_level
                }
                for m in milestones
            ],
            "areas_of_improvement": progress_summary.functional_improvements,
            "remaining_challenges": progress_summary.remaining_challenges,
            "treatment_recommendations": progress_summary.treatment_recommendations,
            "next_phase_focus": progress_summary.next_phase_goals
        }
        
        for change in progress_summary.significant_changes:
            report["significant_achievements"].append(change)
        
        return report
    
    def _get_sessions_in_period(self, patient_id: str, start_date: datetime, 
                               end_date: datetime) -> List[Dict[str, Any]]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT session_id, session_date, session_number, therapy_modality,
                       attendance_status, mood_assessment, interventions_used,
                       goals_addressed, homework_reviewed, homework_assigned,
                       crisis_addressed, safety_concerns, key_insights,
                       therapeutic_breakthroughs, challenges_encountered,
                       patient_engagement, session_effectiveness, progress_indicators
                FROM session_summaries
                WHERE patient_id = ? AND session_date BETWEEN ? AND ?
                ORDER BY session_date
            """, (patient_id, start_date.isoformat(), end_date.isoformat()))
            
            results = cursor.fetchall()
        
        sessions = []
        for row in results:
            session_data = {
                "session_id": row[0],
                "session_date": row[1],
                "session_number": row[2],
                "therapy_modality": row[3],
                "attendance_status": row[4],
                "mood_assessment": json.loads(row[5]) if row[5] else {},
                "interventions_used": json.loads(row[6]) if row[6] else [],
                "goals_addressed": json.loads(row[7]) if row[7] else [],
                "homework_reviewed": row[8],
                "homework_assigned": row[9],
                "crisis_addressed": row[10],
                "safety_concerns": json.loads(row[11]) if row[11] else [],
                "key_insights": json.loads(row[12]) if row[12] else [],
                "therapeutic_breakthroughs": json.loads(row[13]) if row[13] else [],
                "challenges_encountered": json.loads(row[14]) if row[14] else [],
                "patient_engagement": row[15],
                "session_effectiveness": row[16],
                "progress_indicators": json.loads(row[17]) if row[17] else {}
            }
            sessions.append(session_data)
        
        return sessions
    
    def _extract_primary_goals(self, sessions_data: List[Dict[str, Any]]) -> List[str]:
        
        goal_frequency = {}
        
        for session in sessions_data:
            goals = session.get("goals_addressed", [])
            for goal in goals:
                goal_frequency[goal] = goal_frequency.get(goal, 0) + 1
        
        sorted_goals = sorted(goal_frequency.items(), key=lambda x: x[1], reverse=True)
        return [goal for goal, freq in sorted_goals[:5]]
    
    def _identify_safety_improvements(self, sessions_data: List[Dict[str, Any]]) -> List[str]:
        
        improvements = []
        
        early_sessions = sessions_data[:len(sessions_data)//2] if len(sessions_data) > 2 else sessions_data[:1]
        recent_sessions = sessions_data[len(sessions_data)//2:] if len(sessions_data) > 2 else sessions_data[-1:]
        
        early_crises = sum(1 for s in early_sessions if s.get("crisis_addressed", False))
        recent_crises = sum(1 for s in recent_sessions if s.get("crisis_addressed", False))
        
        if early_crises > recent_crises:
            improvements.append(f"Reduced crisis episodes from {early_crises} to {recent_crises}")
        
        early_safety_concerns = []
        recent_safety_concerns = []
        
        for session in early_sessions:
            early_safety_concerns.extend(session.get("safety_concerns", []))
        
        for session in recent_sessions:
            recent_safety_concerns.extend(session.get("safety_concerns", []))
        
        if len(early_safety_concerns) > len(recent_safety_concerns):
            improvements.append("Decreased overall safety concerns")
        
        return improvements
    
    def _analyze_symptom_changes(self, sessions_data: List[Dict[str, Any]]) -> Dict[str, str]:
        
        symptom_changes = {}
        
        if len(sessions_data) < 2:
            return symptom_changes
        
        early_sessions = sessions_data[:len(sessions_data)//2]
        recent_sessions = sessions_data[len(sessions_data)//2:]
        
        early_mood_ratings = [s.get("mood_assessment", {}).get("rating", 0) for s in early_sessions]
        recent_mood_ratings = [s.get("mood_assessment", {}).get("rating", 0) for s in recent_sessions]
        
        if early_mood_ratings and recent_mood_ratings:
            early_avg = sum(early_mood_ratings) / len(early_mood_ratings)
            recent_avg = sum(recent_mood_ratings) / len(recent_mood_ratings)
            
            change = recent_avg - early_avg
            
            if change >= 1.5:
                symptom_changes["mood"] = "significant_improvement"
            elif change >= 0.5:
                symptom_changes["mood"] = "moderate_improvement"
            elif change >= -0.5:
                symptom_changes["mood"] = "stable"
            elif change >= -1.5:
                symptom_changes["mood"] = "moderate_decline"
            else:
                symptom_changes["mood"] = "significant_decline"
        
        early_engagement = [s.get("patient_engagement", 0) for s in early_sessions]
        recent_engagement = [s.get("patient_engagement", 0) for s in recent_sessions]
        
        if early_engagement and recent_engagement:
            early_avg_eng = sum(early_engagement) / len(early_engagement)
            recent_avg_eng = sum(recent_engagement) / len(recent_engagement)
            
            engagement_change = recent_avg_eng - early_avg_eng
            
            if engagement_change >= 1.5:
                symptom_changes["engagement"] = "significant_improvement"
            elif engagement_change >= 0.5:
                symptom_changes["engagement"] = "moderate_improvement"
            elif engagement_change >= -0.5:
                symptom_changes["engagement"] = "stable"
            else:
                symptom_changes["engagement"] = "decline"
        
        return symptom_changes
    
    def _identify_functional_improvements(self, sessions_data: List[Dict[str, Any]]) -> List[str]:
        
        improvements = []
        
        all_insights = []
        for session in sessions_data:
            all_insights.extend(session.get("key_insights", []))
        
        functional_keywords = ["work", "job", "relationship", "family", "social", "daily", "routine", "self-care"]
        
        functional_insights = [insight for insight in all_insights 
                             if any(keyword in insight.lower() for keyword in functional_keywords)]
        
        if functional_insights:
            improvements.extend(functional_insights[:3])
        
        recent_sessions = sessions_data[-3:] if len(sessions_data) >= 3 else sessions_data
        
        for session in recent_sessions:
            breakthroughs = session.get("therapeutic_breakthroughs", [])
            for breakthrough in breakthroughs:
                if any(keyword in breakthrough.lower() for keyword in functional_keywords):
                    improvements.append(f"Breakthrough: {breakthrough}")
        
        return improvements[:5]
    
    def _identify_remaining_challenges(self, sessions_data: List[Dict[str, Any]]) -> List[str]:
        
        challenges = []
        
        recent_sessions = sessions_data[-3:] if len(sessions_data) >= 3 else sessions_data
        
        challenge_frequency = {}
        for session in recent_sessions:
            session_challenges = session.get("challenges_encountered", [])
            for challenge in session_challenges:
                challenge_frequency[challenge] = challenge_frequency.get(challenge, 0) + 1
        
        recurring_challenges = [challenge for challenge, freq in challenge_frequency.items() if freq > 1]
        challenges.extend(recurring_challenges)
        
        low_effectiveness_sessions = [s for s in recent_sessions if s.get("session_effectiveness", 0) < 5]
        if len(low_effectiveness_sessions) > len(recent_sessions) * 0.5:
            challenges.append("Consistently low session effectiveness")
        
        homework_compliance = self._calculate_homework_compliance(sessions_data)
        if homework_compliance < 50:
            challenges.append("Poor homework compliance")
        
        crisis_sessions = [s for s in recent_sessions if s.get("crisis_addressed", False)]
        if len(crisis_sessions) > 1:
            challenges.append("Frequent crisis episodes")
        
        return challenges[:5]
    
    def _generate_treatment_recommendations(self, sessions_data: List[Dict[str, Any]]) -> List[str]:
        
        recommendations = []
        
        overall_progress = self._determine_overall_progress(sessions_data)
        
        if overall_progress in [ProgressDirection.SIGNIFICANT_DECLINE, ProgressDirection.MODERATE_DECLINE]:
            recommendations.append("Consider treatment plan modification or consultation")
            recommendations.append("Assess for underlying factors contributing to decline")
        
        homework_compliance = self._calculate_homework_compliance(sessions_data)
        if homework_compliance < 60:
            recommendations.append("Address homework compliance barriers")
            recommendations.append("Simplify or modify homework assignments")
        
        avg_engagement = sum(s.get("patient_engagement", 0) for s in sessions_data) / len(sessions_data)
        if avg_engagement < 6:
            recommendations.append("Focus on improving therapeutic engagement")
            recommendations.append("Explore motivational factors and treatment goals")
        
        crisis_count = len([s for s in sessions_data if s.get("crisis_addressed", False)])
        if crisis_count > len(sessions_data) * 0.3:
            recommendations.append("Implement enhanced crisis prevention strategies")
            recommendations.append("Consider increasing session frequency")
        
        intervention_effectiveness = self._analyze_intervention_effectiveness(sessions_data)
        ineffective_interventions = [k for k, v in intervention_effectiveness.items() 
                                   if v in [InterventionEffectiveness.NOT_EFFECTIVE, 
                                          InterventionEffectiveness.MINIMALLY_EFFECTIVE]]
        
        if ineffective_interventions:
            recommendations.append(f"Modify or replace ineffective interventions: {', '.join(ineffective_interventions)}")
        
        return recommendations[:5]
    
    def _suggest_next_phase_goals(self, sessions_data: List[Dict[str, Any]]) -> List[str]:
        
        next_goals = []
        
        current_goals = self._extract_primary_goals(sessions_data)
        goal_progress = self._analyze_goal_progress(sessions_data)
        
        achieved_goals = [goal for goal, progress in goal_progress.items() if progress >= 80]
        
        if achieved_goals:
            next_goals.append(f"Maintain progress on achieved goals: {', '.join(achieved_goals)}")
        
        struggling_goals = [goal for goal, progress in goal_progress.items() if progress < 40]
        
        if struggling_goals:
            next_goals.append(f"Intensify focus on challenging goals: {', '.join(struggling_goals)}")
        
        recent_insights = []
        for session in sessions_data[-3:]:
            recent_insights.extend(session.get("key_insights", []))
        
        if "relapse prevention" not in [goal.lower() for goal in current_goals]:
            if any("improved" in insight.lower() for insight in recent_insights):
                next_goals.append("Begin relapse prevention planning")
        
        if any("relationship" in insight.lower() for insight in recent_insights):
            if "interpersonal skills" not in [goal.lower() for goal in current_goals]:
                next_goals.append("Develop interpersonal effectiveness skills")
        
        avg_effectiveness = sum(s.get("session_effectiveness", 0) for s in sessions_data) / len(sessions_data)
        if avg_effectiveness >= 7:
            next_goals.append("Consider transitioning to maintenance phase")
        
        return next_goals[:4]
    
    def _get_patient_milestones(self, patient_id: str, start_date: datetime, 
                               end_date: datetime) -> List[TherapeuticMilestone]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT milestone_id, patient_id, achievement_date, milestone_type,
                       description, significance_level, supporting_evidence, impact_on_treatment
                FROM therapeutic_milestones
                WHERE patient_id = ? AND achievement_date BETWEEN ? AND ?
                ORDER BY achievement_date DESC
            """, (patient_id, start_date.isoformat(), end_date.isoformat()))
            
            results = cursor.fetchall()
        
        milestones = []
        for row in results:
            milestone = TherapeuticMilestone(
                milestone_id=row[0],
                patient_id=row[1],
                achievement_date=datetime.fromisoformat(row[2]),
                milestone_type=row[3],
                description=row[4],
                significance_level=row[5],
                supporting_evidence=json.loads(row[6]) if row[6] else [],
                impact_on_treatment=row[7]
            )
            milestones.append(milestone)
        
        return milestones
    
    def generate_executive_summary(self, patient_id: str, months: int = 6) -> Dict[str, Any]:
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        treatment_report = self.create_treatment_summary_report(patient_id, months)
        sessions_data = self._get_sessions_in_period(patient_id, start_date, end_date)
        milestones = self._get_patient_milestones(patient_id, start_date, end_date)
        
        executive_summary = {
            "patient_id": patient_id,
            "summary_period": f"{months} months",
            "key_metrics": {
                "total_sessions": treatment_report["treatment_summary"]["total_sessions"],
                "attendance_rate": treatment_report["treatment_summary"]["attendance_rate"],
                "overall_progress": treatment_report["treatment_summary"]["overall_progress"],
                "milestones_achieved": len(milestones),
                "crisis_episodes": len([s for s in sessions_data if s.get("crisis_addressed", False)])
            },
            "clinical_highlights": [],
            "treatment_effectiveness": "unknown",
            "risk_factors": [],
            "protective_factors": [],
            "recommendations": treatment_report["treatment_recommendations"][:3],
            "prognosis": "unknown"
        }
        
        avg_effectiveness = sum(s.get("session_effectiveness", 0) for s in sessions_data) / len(sessions_data) if sessions_data else 0
        
        if avg_effectiveness >= 8:
            executive_summary["treatment_effectiveness"] = "highly_effective"
        elif avg_effectiveness >= 6:
            executive_summary["treatment_effectiveness"] = "moderately_effective"
        elif avg_effectiveness >= 4:
            executive_summary["treatment_effectiveness"] = "somewhat_effective"
        else:
            executive_summary["treatment_effectiveness"] = "minimally_effective"
        
        high_significance_milestones = [m for m in milestones if m.significance_level >= 7]
        if high_significance_milestones:
            executive_summary["clinical_highlights"].append(f"Achieved {len(high_significance_milestones)} significant therapeutic milestones")
        
        recent_crises = len([s for s in sessions_data[-4:] if s.get("crisis_addressed", False)])
        if recent_crises == 0:
            executive_summary["protective_factors"].append("No recent crisis episodes")
        elif recent_crises > 2:
            executive_summary["risk_factors"].append("Frequent recent crisis episodes")
        
        homework_compliance = self._calculate_homework_compliance(sessions_data)
        if homework_compliance >= 80:
            executive_summary["protective_factors"].append("Excellent homework compliance")
        elif homework_compliance < 50:
            executive_summary["risk_factors"].append("Poor homework compliance")
        
        attendance_rate = float(treatment_report["treatment_summary"]["attendance_rate"].rstrip('%'))
        if attendance_rate >= 90:
            executive_summary["protective_factors"].append("Excellent session attendance")
        elif attendance_rate < 70:
            executive_summary["risk_factors"].append("Poor session attendance")
        
        overall_progress = treatment_report["treatment_summary"]["overall_progress"]
        if "improvement" in overall_progress:
            executive_summary["prognosis"] = "positive"
        elif "decline" in overall_progress:
            executive_summary["prognosis"] = "concerning"
        else:
            executive_summary["prognosis"] = "stable"
        
        return executive_summary
    
    def _save_session_summary(self, summary: SessionSummary):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO session_summaries
                (session_id, patient_id, therapist_id, session_date, session_number,
                 therapy_modality, session_duration, attendance_status, mood_assessment,
                 interventions_used, goals_addressed, homework_reviewed, homework_assigned,
                 crisis_addressed, safety_concerns, key_insights, therapeutic_breakthroughs,
                 challenges_encountered, patient_engagement, session_effectiveness,
                 progress_indicators, next_session_focus, clinical_observations,
                 patient_feedback, therapist_reflections, summary_type, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                summary.session_id, summary.patient_id, summary.therapist_id,
                summary.session_date.isoformat(), summary.session_number, summary.therapy_modality,
                summary.session_duration, summary.attendance_status, json.dumps(summary.mood_assessment),
                json.dumps(summary.interventions_used), json.dumps(summary.goals_addressed),
                summary.homework_reviewed, summary.homework_assigned, summary.crisis_addressed,
                json.dumps(summary.safety_concerns), json.dumps(summary.key_insights),
                json.dumps(summary.therapeutic_breakthroughs), json.dumps(summary.challenges_encountered),
                summary.patient_engagement, summary.session_effectiveness,
                json.dumps(summary.progress_indicators), json.dumps(summary.next_session_focus),
                summary.clinical_observations, summary.patient_feedback, summary.therapist_reflections,
                summary.summary_type.value, summary.created_at.isoformat()
            ))
    
    def _save_progress_summary(self, summary: ProgressSummary):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO progress_summaries
                (patient_id, period_start, period_end, total_sessions, sessions_attended,
                 attendance_rate, primary_goals, goal_progress, overall_progress,
                 significant_changes, intervention_effectiveness, homework_compliance,
                 crisis_episodes, safety_improvements, symptom_changes,
                 functional_improvements, remaining_challenges, treatment_recommendations,
                 next_phase_goals, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                summary.patient_id, summary.period_start.isoformat(), summary.period_end.isoformat(),
                summary.total_sessions, summary.sessions_attended, summary.attendance_rate,
                json.dumps(summary.primary_goals), json.dumps(summary.goal_progress),
                summary.overall_progress.value, json.dumps(summary.significant_changes),
                json.dumps({k: v.value for k, v in summary.intervention_effectiveness.items()}),
                summary.homework_compliance, summary.crisis_episodes,
                json.dumps(summary.safety_improvements), json.dumps(summary.symptom_changes),
                json.dumps(summary.functional_improvements), json.dumps(summary.remaining_challenges),
                json.dumps(summary.treatment_recommendations), json.dumps(summary.next_phase_goals),
                datetime.now().isoformat()
            ))
    
    def _save_milestone(self, milestone: TherapeuticMilestone):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO therapeutic_milestones
                (milestone_id, patient_id, achievement_date, milestone_type,
                 description, significance_level, supporting_evidence,
                 impact_on_treatment, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                milestone.milestone_id, milestone.patient_id, milestone.achievement_date.isoformat(),
                milestone.milestone_type, milestone.description, milestone.significance_level,
                json.dumps(milestone.supporting_evidence), milestone.impact_on_treatment,
                datetime.now().isoformat()
            ))


if __name__ == "__main__":
    summary_system = SessionSummarySystem()
    
    session_data = {
        "session_id": "session_001",
        "patient_id": "patient_123",
        "therapist_id": "therapist_001",
        "session_date": "2024-01-15T10:00:00",
        "session_number": 5,
        "therapy_modality": "CBT",
        "session_duration": 50,
        "attendance_status": "attended",
        "mood_assessment": {"rating": 6, "description": "Feeling somewhat better today"},
        "interventions_used": ["cognitive_restructuring", "thought_records", "behavioral_activation"],
        "goals_addressed": ["reduce_anxiety", "improve_mood"],
        "homework_reviewed": True,
        "homework_assigned": True,
        "crisis_addressed": False,
        "safety_concerns": [],
        "key_insights": ["Noticed pattern of catastrophic thinking before work meetings"],
        "therapeutic_breakthroughs": ["First time successfully challenging automatic thoughts"],
        "challenges_encountered": ["Difficulty identifying emotions initially"],
        "patient_engagement": 8,
        "session_effectiveness": 7,
        "progress_indicators": {"reduce_anxiety": 60, "improve_mood": 70},
        "next_session_focus": ["Continue thought challenging", "Practice relaxation techniques"],
        "clinical_observations": "Patient showing increased awareness of thought patterns",
        "patient_feedback": "Found the thought record exercise very helpful",
        "therapist_reflections": "Good progress with cognitive restructuring skills"
    }
    
    session_summary = summary_system.create_session_summary(session_data)
    print("=== SESSION SUMMARY CREATED ===")
    print(f"Session ID: {session_summary.session_id}")
    print(f"Engagement: {session_summary.patient_engagement}/10")
    print(f"Effectiveness: {session_summary.session_effectiveness}/10")
    
    narrative = summary_system.generate_session_narrative(session_summary)
    print(f"\n=== SESSION NARRATIVE ===")
    print(narrative)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    try:
        progress_summary = summary_system.generate_progress_summary("patient_123", start_date, end_date)
        print(f"\n=== PROGRESS SUMMARY ===")
        print(f"Total Sessions: {progress_summary.total_sessions}")
        print(f"Attendance Rate: {progress_summary.attendance_rate:.1f}%")
        print(f"Overall Progress: {progress_summary.overall_progress.value}")
        print(f"Homework Compliance: {progress_summary.homework_compliance:.1f}%")
    except ValueError as e:
        print(f"\n=== PROGRESS SUMMARY ===")
        print(f"Error: {e}")
    
    executive_summary = summary_system.generate_executive_summary("patient_123", 3)
    print(f"\n=== EXECUTIVE SUMMARY ===")
    print(f"Treatment Effectiveness: {executive_summary['treatment_effectiveness']}")
    print(f"Prognosis: {executive_summary['prognosis']}")
    print(f"Key Metrics: {executive_summary['key_metrics']}")
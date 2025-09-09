import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from enum import Enum
from dataclasses import dataclass
import json

from config.therapy_protocols import TherapyModality, InterventionType


class ThinkingStyle(Enum):
    ALL_OR_NOTHING = "all_or_nothing"
    OVERGENERALIZATION = "overgeneralization"
    MENTAL_FILTER = "mental_filter"
    DISCOUNTING_POSITIVE = "discounting_positive"
    JUMPING_TO_CONCLUSIONS = "jumping_to_conclusions"
    MAGNIFICATION = "magnification"
    EMOTIONAL_REASONING = "emotional_reasoning"
    SHOULD_STATEMENTS = "should_statements"
    LABELING = "labeling"
    PERSONALIZATION = "personalization"


class ThoughtType(Enum):
    AUTOMATIC_THOUGHT = "automatic_thought"
    INTERMEDIATE_BELIEF = "intermediate_belief"
    CORE_BELIEF = "core_belief"
    BALANCED_THOUGHT = "balanced_thought"


class EvidenceType(Enum):
    SUPPORTING = "supporting"
    CONTRADICTING = "contradicting"
    ALTERNATIVE = "alternative"


@dataclass
class ThoughtRecord:
    record_id: str
    patient_id: str
    situation: str
    automatic_thought: str
    emotion: str
    emotion_intensity: int
    thinking_errors: List[str]
    evidence_for: List[str]
    evidence_against: List[str]
    balanced_thought: str
    new_emotion: str
    new_emotion_intensity: int
    created_date: datetime
    session_id: Optional[str] = None
    homework_id: Optional[str] = None
    notes: str = ""


@dataclass
class BalancedThinkingExercise:
    exercise_id: str
    patient_id: str
    original_thought: str
    thought_type: ThoughtType
    distortions_identified: List[str]
    evidence_analysis: Dict[str, List[str]]
    alternative_perspectives: List[str]
    balanced_statement: str
    confidence_before: int
    confidence_after: int
    created_date: datetime
    completed_date: Optional[datetime] = None
    effectiveness_rating: Optional[int] = None


class BalancedThinkingProcessor:
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS thought_records (
                    record_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    situation TEXT NOT NULL,
                    automatic_thought TEXT NOT NULL,
                    emotion TEXT NOT NULL,
                    emotion_intensity INTEGER NOT NULL,
                    thinking_errors TEXT,
                    evidence_for TEXT,
                    evidence_against TEXT,
                    balanced_thought TEXT,
                    new_emotion TEXT,
                    new_emotion_intensity INTEGER,
                    created_date TIMESTAMP,
                    session_id TEXT,
                    homework_id TEXT,
                    notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS balanced_thinking_exercises (
                    exercise_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    original_thought TEXT NOT NULL,
                    thought_type TEXT NOT NULL,
                    distortions_identified TEXT,
                    evidence_analysis TEXT,
                    alternative_perspectives TEXT,
                    balanced_statement TEXT,
                    confidence_before INTEGER,
                    confidence_after INTEGER,
                    created_date TIMESTAMP,
                    completed_date TIMESTAMP,
                    effectiveness_rating INTEGER,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            conn.commit()
    
    def create_thought_record(
        self,
        patient_id: str,
        situation: str,
        automatic_thought: str,
        emotion: str,
        emotion_intensity: int,
        session_id: Optional[str] = None
    ) -> ThoughtRecord:
        record_id = f"thought_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        record = ThoughtRecord(
            record_id=record_id,
            patient_id=patient_id,
            situation=situation,
            automatic_thought=automatic_thought,
            emotion=emotion,
            emotion_intensity=emotion_intensity,
            thinking_errors=[],
            evidence_for=[],
            evidence_against=[],
            balanced_thought="",
            new_emotion="",
            new_emotion_intensity=0,
            created_date=datetime.now(),
            session_id=session_id
        )
        
        return record
    
    def identify_thinking_errors(self, thought: str) -> List[str]:
        errors = []
        thought_lower = thought.lower()
        
        all_or_nothing_words = ['always', 'never', 'everyone', 'no one', 'everything', 'nothing', 'completely', 'totally']
        if any(word in thought_lower for word in all_or_nothing_words):
            errors.append(ThinkingStyle.ALL_OR_NOTHING.value)
        
        overgeneralization_words = ['all', 'every', 'constantly', 'forever', 'typical']
        if any(word in thought_lower for word in overgeneralization_words):
            errors.append(ThinkingStyle.OVERGENERALIZATION.value)
        
        should_words = ['should', 'must', 'have to', 'ought to', 'supposed to']
        if any(word in thought_lower for word in should_words):
            errors.append(ThinkingStyle.SHOULD_STATEMENTS.value)
        
        catastrophic_words = ['disaster', 'terrible', 'awful', 'horrible', 'catastrophe', 'ruined']
        if any(word in thought_lower for word in catastrophic_words):
            errors.append(ThinkingStyle.MAGNIFICATION.value)
        
        emotional_words = ['feel like', 'feel that', 'sense that']
        if any(phrase in thought_lower for phrase in emotional_words):
            errors.append(ThinkingStyle.EMOTIONAL_REASONING.value)
        
        return errors
    
    def generate_evidence_questions(self, thought: str) -> Dict[str, List[str]]:
        questions = {
            'evidence_for': [
                "What facts support this thought?",
                "What evidence do I have that this is true?",
                "What specific examples confirm this?",
                "What would I tell a friend who had this thought?",
                "What data backs up this conclusion?"
            ],
            'evidence_against': [
                "What facts contradict this thought?",
                "What evidence suggests this might not be true?",
                "What would someone who disagrees say?",
                "What are alternative explanations?",
                "What would I say to a friend having this thought?",
                "What have I learned from similar situations before?"
            ],
            'alternative_perspectives': [
                "What would a friend tell me about this?",
                "How might I view this in 5 years?",
                "What would someone who cares about me say?",
                "What's another way to look at this situation?",
                "What would I tell someone else in this situation?"
            ]
        }
        
        return questions
    
    def create_balanced_thought(
        self,
        original_thought: str,
        evidence_for: List[str],
        evidence_against: List[str],
        alternatives: List[str]
    ) -> str:
        balanced_elements = []
        
        if evidence_for:
            balanced_elements.append("While there may be some truth to my concerns")
        
        if evidence_against:
            balanced_elements.append("there's also evidence that contradicts this")
        
        if alternatives:
            balanced_elements.append("and other ways to interpret the situation")
        
        balanced_thought = "It's possible that " + original_thought.lower()
        balanced_thought += ", but it's also possible that this isn't entirely accurate. "
        
        if evidence_against:
            balanced_thought += "The evidence suggests that "
            if len(evidence_against) == 1:
                balanced_thought += evidence_against[0].lower() + ". "
            else:
                balanced_thought += "there are several factors that contradict this view. "
        
        balanced_thought += "A more balanced perspective might be that this situation is complex "
        balanced_thought += "and there are multiple ways to understand what's happening."
        
        return balanced_thought
    
    def process_thought_record(
        self,
        record: ThoughtRecord,
        evidence_for: List[str],
        evidence_against: List[str],
        balanced_thought: str,
        new_emotion: str,
        new_emotion_intensity: int
    ) -> ThoughtRecord:
        record.evidence_for = evidence_for
        record.evidence_against = evidence_against
        record.balanced_thought = balanced_thought
        record.new_emotion = new_emotion
        record.new_emotion_intensity = new_emotion_intensity
        record.thinking_errors = self.identify_thinking_errors(record.automatic_thought)
        
        self.save_thought_record(record)
        return record
    
    def save_thought_record(self, record: ThoughtRecord):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO thought_records (
                    record_id, patient_id, situation, automatic_thought, emotion,
                    emotion_intensity, thinking_errors, evidence_for, evidence_against,
                    balanced_thought, new_emotion, new_emotion_intensity, created_date,
                    session_id, homework_id, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.record_id, record.patient_id, record.situation,
                record.automatic_thought, record.emotion, record.emotion_intensity,
                json.dumps(record.thinking_errors), json.dumps(record.evidence_for),
                json.dumps(record.evidence_against), record.balanced_thought,
                record.new_emotion, record.new_emotion_intensity, record.created_date,
                record.session_id, record.homework_id, record.notes
            ))
            conn.commit()
    
    def create_balanced_thinking_exercise(
        self,
        patient_id: str,
        original_thought: str,
        thought_type: ThoughtType
    ) -> BalancedThinkingExercise:
        exercise_id = f"balance_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        exercise = BalancedThinkingExercise(
            exercise_id=exercise_id,
            patient_id=patient_id,
            original_thought=original_thought,
            thought_type=thought_type,
            distortions_identified=self.identify_thinking_errors(original_thought),
            evidence_analysis={},
            alternative_perspectives=[],
            balanced_statement="",
            confidence_before=0,
            confidence_after=0,
            created_date=datetime.now()
        )
        
        return exercise
    
    def complete_balanced_thinking_exercise(
        self,
        exercise: BalancedThinkingExercise,
        evidence_for: List[str],
        evidence_against: List[str],
        alternatives: List[str],
        confidence_before: int,
        confidence_after: int,
        effectiveness_rating: int
    ) -> BalancedThinkingExercise:
        exercise.evidence_analysis = {
            'supporting': evidence_for,
            'contradicting': evidence_against
        }
        exercise.alternative_perspectives = alternatives
        exercise.balanced_statement = self.create_balanced_thought(
            exercise.original_thought, evidence_for, evidence_against, alternatives
        )
        exercise.confidence_before = confidence_before
        exercise.confidence_after = confidence_after
        exercise.completed_date = datetime.now()
        exercise.effectiveness_rating = effectiveness_rating
        
        self.save_balanced_thinking_exercise(exercise)
        return exercise
    
    def save_balanced_thinking_exercise(self, exercise: BalancedThinkingExercise):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO balanced_thinking_exercises (
                    exercise_id, patient_id, original_thought, thought_type,
                    distortions_identified, evidence_analysis, alternative_perspectives,
                    balanced_statement, confidence_before, confidence_after,
                    created_date, completed_date, effectiveness_rating
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                exercise.exercise_id, exercise.patient_id, exercise.original_thought,
                exercise.thought_type.value, json.dumps(exercise.distortions_identified),
                json.dumps(exercise.evidence_analysis), json.dumps(exercise.alternative_perspectives),
                exercise.balanced_statement, exercise.confidence_before, exercise.confidence_after,
                exercise.created_date, exercise.completed_date, exercise.effectiveness_rating
            ))
            conn.commit()
    
    def get_thought_records(self, patient_id: str, limit: int = 10) -> List[ThoughtRecord]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM thought_records 
                WHERE patient_id = ? 
                ORDER BY created_date DESC 
                LIMIT ?
            """, (patient_id, limit))
            
            records = []
            for row in cursor.fetchall():
                record = ThoughtRecord(
                    record_id=row[0],
                    patient_id=row[1],
                    situation=row[2],
                    automatic_thought=row[3],
                    emotion=row[4],
                    emotion_intensity=row[5],
                    thinking_errors=json.loads(row[6] or '[]'),
                    evidence_for=json.loads(row[7] or '[]'),
                    evidence_against=json.loads(row[8] or '[]'),
                    balanced_thought=row[9] or "",
                    new_emotion=row[10] or "",
                    new_emotion_intensity=row[11] or 0,
                    created_date=datetime.fromisoformat(row[12]),
                    session_id=row[13],
                    homework_id=row[14],
                    notes=row[15] or ""
                )
                records.append(record)
            
            return records
    
    def get_thinking_patterns_analysis(self, patient_id: str, days: int = 30) -> Dict[str, Any]:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT thinking_errors, emotion_intensity, new_emotion_intensity
                FROM thought_records 
                WHERE patient_id = ? AND created_date >= ?
            """, (patient_id, start_date))
            
            records = cursor.fetchall()
        
        if not records:
            return {"error": "No thought records found"}
        
        all_errors = []
        mood_improvements = []
        
        for row in records:
            errors = json.loads(row[0] or '[]')
            all_errors.extend(errors)
            
            if row[1] and row[2]:
                improvement = row[1] - row[2]
                mood_improvements.append(improvement)
        
        error_counts = {}
        for error in all_errors:
            error_counts[error] = error_counts.get(error, 0) + 1
        
        most_common_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        avg_mood_improvement = sum(mood_improvements) / len(mood_improvements) if mood_improvements else 0
        
        analysis = {
            "analysis_period_days": days,
            "total_thought_records": len(records),
            "most_common_thinking_errors": [
                {"error": error, "frequency": count} for error, count in most_common_errors
            ],
            "average_mood_improvement": round(avg_mood_improvement, 1),
            "mood_improvement_rate": round(len([x for x in mood_improvements if x > 0]) / len(mood_improvements) * 100, 1) if mood_improvements else 0
        }
        
        return analysis
    
    def generate_balanced_thinking_homework(self, patient_id: str) -> Dict[str, Any]:
        patterns = self.get_thinking_patterns_analysis(patient_id, days=14)
        
        if "error" in patterns:
            homework_focus = "general"
        else:
            most_common = patterns.get("most_common_thinking_errors", [])
            homework_focus = most_common[0]["error"] if most_common else "general"
        
        homework_templates = {
            "all_or_nothing": {
                "title": "Finding the Gray Areas",
                "instructions": [
                    "Notice when you use words like 'always', 'never', 'completely'",
                    "Ask yourself: What percentage of the time is this really true?",
                    "Look for exceptions to absolute statements",
                    "Practice using words like 'sometimes', 'often', 'in this case'"
                ]
            },
            "overgeneralization": {
                "title": "Specific vs General",
                "instructions": [
                    "When you notice broad conclusions, ask: What specifically happened?",
                    "Look for words like 'all', 'everyone', 'every time'",
                    "Challenge yourself to be more specific about situations",
                    "Remember that one event doesn't predict all future events"
                ]
            },
            "should_statements": {
                "title": "Preferences vs Demands",
                "instructions": [
                    "Notice 'should', 'must', 'have to' in your thoughts",
                    "Ask: Is this a preference or a demand?",
                    "Replace 'should' with 'would prefer' or 'it would be nice if'",
                    "Consider that people and situations don't always meet our expectations"
                ]
            },
            "general": {
                "title": "Daily Balanced Thinking Practice",
                "instructions": [
                    "Complete one thought record daily",
                    "Focus on situations that caused strong emotions",
                    "Always look for evidence both for and against your thoughts",
                    "Practice creating balanced, realistic alternatives"
                ]
            }
        }
        
        template = homework_templates.get(homework_focus, homework_templates["general"])
        
        homework = {
            "patient_id": patient_id,
            "focus_area": homework_focus,
            "title": template["title"],
            "daily_practice": template["instructions"],
            "thought_record_goal": 5,
            "monitoring_questions": [
                "What was the situation?",
                "What went through your mind?",
                "What emotion did you feel and how intense was it (1-10)?",
                "What thinking errors might be present?",
                "What evidence supports and contradicts this thought?",
                "What's a more balanced way to think about this?"
            ],
            "success_criteria": [
                "Complete thought records for situations with emotion intensity 6+",
                "Identify at least one thinking error per record",
                "Generate evidence both for and against automatic thoughts",
                "Create balanced alternatives that feel realistic"
            ]
        }
        
        return homework
    
    def get_progress_summary(self, patient_id: str, weeks: int = 4) -> Dict[str, Any]:
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=weeks)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT emotion_intensity, new_emotion_intensity, created_date
                FROM thought_records 
                WHERE patient_id = ? AND created_date >= ? AND new_emotion_intensity > 0
                ORDER BY created_date
            """, (patient_id, start_date))
            
            records = cursor.fetchall()
        
        if not records:
            return {"error": "No completed thought records found"}
        
        weekly_progress = {}
        for row in records:
            week = datetime.fromisoformat(row[2]).isocalendar()[1]
            improvement = row[0] - row[1]
            
            if week not in weekly_progress:
                weekly_progress[week] = []
            weekly_progress[week].append(improvement)
        
        weekly_averages = []
        for week, improvements in weekly_progress.items():
            avg_improvement = sum(improvements) / len(improvements)
            weekly_averages.append({
                "week": week,
                "average_mood_improvement": round(avg_improvement, 1),
                "records_completed": len(improvements)
            })
        
        weekly_averages.sort(key=lambda x: x["week"])
        
        total_records = len(records)
        total_improvement = sum(row[0] - row[1] for row in records)
        average_improvement = total_improvement / total_records
        
        progress_summary = {
            "analysis_period_weeks": weeks,
            "total_completed_records": total_records,
            "overall_average_improvement": round(average_improvement, 1),
            "weekly_progress": weekly_averages,
            "trend": "improving" if len(weekly_averages) > 1 and weekly_averages[-1]["average_mood_improvement"] > weekly_averages[0]["average_mood_improvement"] else "stable"
        }
        
        return progress_summary
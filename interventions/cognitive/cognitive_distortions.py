import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from enum import Enum
from dataclasses import dataclass
import json
import re

from config.therapy_protocols import TherapyModality, InterventionType


class DistortionType(Enum):
    ALL_OR_NOTHING = "all_or_nothing"
    OVERGENERALIZATION = "overgeneralization"
    MENTAL_FILTER = "mental_filter"
    DISCOUNTING_POSITIVE = "discounting_positive"
    JUMPING_TO_CONCLUSIONS = "jumping_to_conclusions"
    MIND_READING = "mind_reading"
    FORTUNE_TELLING = "fortune_telling"
    MAGNIFICATION = "magnification"
    MINIMIZATION = "minimization"
    EMOTIONAL_REASONING = "emotional_reasoning"
    SHOULD_STATEMENTS = "should_statements"
    LABELING = "labeling"
    PERSONALIZATION = "personalization"
    BLAME = "blame"


class DistortionSeverity(Enum):
    MILD = 1
    MODERATE = 2
    SEVERE = 3


@dataclass
class DistortionPattern:
    pattern_id: str
    distortion_type: DistortionType
    trigger_words: List[str]
    trigger_phrases: List[str]
    context_indicators: List[str]
    severity_markers: Dict[str, List[str]]
    description: str
    examples: List[str]


@dataclass
class DistortionIdentification:
    identification_id: str
    patient_id: str
    original_thought: str
    distortions_found: List[str]
    severity_levels: Dict[str, int]
    confidence_scores: Dict[str, float]
    context_factors: List[str]
    created_date: datetime
    session_id: Optional[str] = None


@dataclass
class DistortionChallenge:
    challenge_id: str
    identification_id: str
    distortion_type: str
    original_thought: str
    challenge_questions: List[str]
    evidence_collected: Dict[str, List[str]]
    alternative_thoughts: List[str]
    effectiveness_rating: Optional[int] = None
    created_date: datetime
    completed_date: Optional[datetime] = None


class CognitiveDistortionDetector:
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self._initialize_database()
        self._load_distortion_patterns()
    
    def _initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS distortion_identifications (
                    identification_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    original_thought TEXT NOT NULL,
                    distortions_found TEXT,
                    severity_levels TEXT,
                    confidence_scores TEXT,
                    context_factors TEXT,
                    created_date TIMESTAMP,
                    session_id TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS distortion_challenges (
                    challenge_id TEXT PRIMARY KEY,
                    identification_id TEXT NOT NULL,
                    distortion_type TEXT NOT NULL,
                    original_thought TEXT NOT NULL,
                    challenge_questions TEXT,
                    evidence_collected TEXT,
                    alternative_thoughts TEXT,
                    effectiveness_rating INTEGER,
                    created_date TIMESTAMP,
                    completed_date TIMESTAMP,
                    FOREIGN KEY (identification_id) REFERENCES distortion_identifications (identification_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS distortion_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    distortion_type TEXT NOT NULL,
                    frequency INTEGER DEFAULT 1,
                    contexts TEXT,
                    triggers TEXT,
                    last_occurrence TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            conn.commit()
    
    def _load_distortion_patterns(self):
        self.distortion_patterns = {
            DistortionType.ALL_OR_NOTHING: DistortionPattern(
                pattern_id="aon_001",
                distortion_type=DistortionType.ALL_OR_NOTHING,
                trigger_words=["always", "never", "everyone", "no one", "everything", "nothing", "completely", "totally", "absolutely", "perfectly"],
                trigger_phrases=["all the time", "every time", "without exception", "100%", "0%"],
                context_indicators=["performance", "relationships", "self-worth"],
                severity_markers={
                    "mild": ["sometimes", "often"],
                    "moderate": ["always", "never"],
                    "severe": ["absolutely always", "completely never", "without exception"]
                },
                description="Viewing situations in extreme terms with no middle ground",
                examples=["I always mess everything up", "Nobody ever listens to me", "I'm a complete failure"]
            ),
            
            DistortionType.OVERGENERALIZATION: DistortionPattern(
                pattern_id="over_001",
                distortion_type=DistortionType.OVERGENERALIZATION,
                trigger_words=["all", "every", "entire", "whole", "constant", "continuous", "typical", "usual"],
                trigger_phrases=["this always happens", "every single time", "all men/women", "all people"],
                context_indicators=["pattern", "future", "group"],
                severity_markers={
                    "mild": ["often", "frequently"],
                    "moderate": ["all", "every"],
                    "severe": ["absolutely all", "every single"]
                },
                description="Drawing broad conclusions from single events",
                examples=["This always happens to me", "All relationships end badly", "I can never do anything right"]
            ),
            
            DistortionType.MENTAL_FILTER: DistortionPattern(
                pattern_id="filter_001",
                distortion_type=DistortionType.MENTAL_FILTER,
                trigger_words=["only", "just", "except", "but", "however", "although"],
                trigger_phrases=["the only thing", "all that matters", "nothing but", "except for"],
                context_indicators=["negative focus", "dismissal", "selective attention"],
                severity_markers={
                    "mild": ["mostly", "mainly"],
                    "moderate": ["only", "just"],
                    "severe": ["absolutely nothing but", "the only thing that matters"]
                },
                description="Focusing exclusively on negative details while ignoring positive aspects",
                examples=["The only thing people notice are my mistakes", "All I do is fail", "Nothing good ever happens"]
            ),
            
            DistortionType.DISCOUNTING_POSITIVE: DistortionPattern(
                pattern_id="discount_001",
                distortion_type=DistortionType.DISCOUNTING_POSITIVE,
                trigger_words=["luck", "fluke", "accident", "doesn't count", "anyone could"],
                trigger_phrases=["it was just luck", "that doesn't count", "anyone could do that", "it was nothing"],
                context_indicators=["achievement", "compliment", "success"],
                severity_markers={
                    "mild": ["maybe", "probably"],
                    "moderate": ["just", "only"],
                    "severe": ["definitely just", "absolutely nothing"]
                },
                description="Dismissing positive experiences as unimportant or accidental",
                examples=["That compliment doesn't count", "I just got lucky", "Anyone could have done that"]
            ),
            
            DistortionType.MIND_READING: DistortionPattern(
                pattern_id="mind_001",
                distortion_type=DistortionType.MIND_READING,
                trigger_words=["thinks", "knows", "realizes", "sees", "understands", "feels"],
                trigger_phrases=["he thinks", "she knows", "they realize", "everyone can see", "it's obvious that"],
                context_indicators=["others' thoughts", "assumptions", "social situations"],
                severity_markers={
                    "mild": ["probably thinks", "might think"],
                    "moderate": ["thinks", "knows"],
                    "severe": ["definitely thinks", "absolutely knows", "can clearly see"]
                },
                description="Assuming you know what others are thinking without evidence",
                examples=["She thinks I'm stupid", "Everyone knows I'm a fraud", "He can see right through me"]
            ),
            
            DistortionType.FORTUNE_TELLING: DistortionPattern(
                pattern_id="fortune_001",
                distortion_type=DistortionType.FORTUNE_TELLING,
                trigger_words=["will", "going to", "won't", "never will", "always will"],
                trigger_phrases=["will never", "will always", "is going to", "won't ever"],
                context_indicators=["future", "prediction", "outcome"],
                severity_markers={
                    "mild": ["might", "probably will"],
                    "moderate": ["will", "going to"],
                    "severe": ["definitely will", "absolutely going to", "will never ever"]
                },
                description="Predicting negative outcomes without considering alternatives",
                examples=["This will never work", "I'm going to fail", "Everything will go wrong"]
            ),
            
            DistortionType.MAGNIFICATION: DistortionPattern(
                pattern_id="mag_001",
                distortion_type=DistortionType.MAGNIFICATION,
                trigger_words=["disaster", "catastrophe", "terrible", "horrible", "awful", "ruined", "destroyed"],
                trigger_phrases=["complete disaster", "total catastrophe", "absolutely terrible", "completely ruined"],
                context_indicators=["crisis", "exaggeration", "worst case"],
                severity_markers={
                    "mild": ["bad", "unfortunate"],
                    "moderate": ["terrible", "horrible"],
                    "severe": ["complete disaster", "absolute catastrophe", "totally ruined"]
                },
                description="Exaggerating the importance or severity of problems",
                examples=["This is a complete disaster", "My life is ruined", "It's absolutely terrible"]
            ),
            
            DistortionType.EMOTIONAL_REASONING: DistortionPattern(
                pattern_id="emotion_001",
                distortion_type=DistortionType.EMOTIONAL_REASONING,
                trigger_words=["feel", "feeling", "sense"],
                trigger_phrases=["I feel like", "I feel that", "my feeling is", "I sense that"],
                context_indicators=["emotion", "intuition", "feeling"],
                severity_markers={
                    "mild": ["I think", "I sense"],
                    "moderate": ["I feel", "I'm feeling"],
                    "severe": ["I absolutely feel", "I know because I feel"]
                },
                description="Believing that emotions reflect reality without examining evidence",
                examples=["I feel stupid so I must be stupid", "I feel guilty so I did something wrong"]
            ),
            
            DistortionType.SHOULD_STATEMENTS: DistortionPattern(
                pattern_id="should_001",
                distortion_type=DistortionType.SHOULD_STATEMENTS,
                trigger_words=["should", "must", "ought", "have to", "need to", "supposed to"],
                trigger_phrases=["should have", "must be", "ought to", "have to be", "supposed to"],
                context_indicators=["obligation", "expectation", "rules"],
                severity_markers={
                    "mild": ["could", "might want to"],
                    "moderate": ["should", "ought to"],
                    "severe": ["absolutely must", "have to", "no choice but to"]
                },
                description="Using rigid rules about how things should be",
                examples=["I should be perfect", "People must like me", "I have to succeed"]
            ),
            
            DistortionType.LABELING: DistortionPattern(
                pattern_id="label_001",
                distortion_type=DistortionType.LABELING,
                trigger_words=["am", "is", "are", "loser", "idiot", "failure", "worthless"],
                trigger_phrases=["I am a", "he is a", "she is a", "they are", "what a"],
                context_indicators=["identity", "character", "global assessment"],
                severity_markers={
                    "mild": ["sometimes", "can be"],
                    "moderate": ["am", "is"],
                    "severe": ["complete", "total", "absolute"]
                },
                description="Defining yourself or others with negative labels",
                examples=["I'm a complete failure", "He's an idiot", "What a loser"]
            ),
            
            DistortionType.PERSONALIZATION: DistortionPattern(
                pattern_id="personal_001",
                distortion_type=DistortionType.PERSONALIZATION,
                trigger_words=["my fault", "because of me", "I caused", "my responsibility"],
                trigger_phrases=["it's my fault", "because of me", "I'm responsible", "I caused this"],
                context_indicators=["blame", "responsibility", "causation"],
                severity_markers={
                    "mild": ["partly my fault", "somewhat responsible"],
                    "moderate": ["my fault", "because of me"],
                    "severe": ["completely my fault", "entirely because of me", "all my responsibility"]
                },
                description="Taking responsibility for things outside your control",
                examples=["It's all my fault", "I ruined everything", "This happened because of me"]
            )
        }
    
    def identify_distortions(self, thought: str, context: str = "") -> DistortionIdentification:
        identification_id = f"distort_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        thought_lower = thought.lower()
        
        distortions_found = []
        severity_levels = {}
        confidence_scores = {}
        context_factors = []
        
        for distortion_type, pattern in self.distortion_patterns.items():
            confidence = 0.0
            severity = 1
            
            word_matches = sum(1 for word in pattern.trigger_words if word in thought_lower)
            if word_matches > 0:
                confidence += (word_matches / len(pattern.trigger_words)) * 0.6
            
            phrase_matches = sum(1 for phrase in pattern.trigger_phrases if phrase in thought_lower)
            if phrase_matches > 0:
                confidence += (phrase_matches / len(pattern.trigger_phrases)) * 0.8
            
            context_matches = sum(1 for indicator in pattern.context_indicators if indicator in context.lower())
            if context_matches > 0:
                confidence += (context_matches / len(pattern.context_indicators)) * 0.4
                context_factors.extend([indicator for indicator in pattern.context_indicators if indicator in context.lower()])
            
            for sev_level, markers in pattern.severity_markers.items():
                marker_matches = sum(1 for marker in markers if marker in thought_lower)
                if marker_matches > 0:
                    if sev_level == "severe":
                        severity = 3
                        confidence += 0.3
                    elif sev_level == "moderate":
                        severity = 2
                        confidence += 0.2
                    else:
                        severity = 1
                        confidence += 0.1
            
            if confidence >= 0.3:
                distortions_found.append(distortion_type.value)
                severity_levels[distortion_type.value] = severity
                confidence_scores[distortion_type.value] = min(1.0, confidence)
        
        identification = DistortionIdentification(
            identification_id=identification_id,
            patient_id="",
            original_thought=thought,
            distortions_found=distortions_found,
            severity_levels=severity_levels,
            confidence_scores=confidence_scores,
            context_factors=list(set(context_factors)),
            created_date=datetime.now()
        )
        
        return identification
    
    def generate_challenge_questions(self, distortion_type: str, thought: str) -> List[str]:
        question_templates = {
            "all_or_nothing": [
                "Is this really an all-or-nothing situation, or are there degrees?",
                "What would be between the extremes in this case?",
                "Can you think of any exceptions to this absolute statement?",
                "How often does this actually happen - 100% of the time or something less?",
                "What would you tell a friend who had this same thought?"
            ],
            
            "overgeneralization": [
                "Is this pattern really true for ALL situations?",
                "What evidence do you have that this always happens?",
                "Can you think of any times when this wasn't the case?",
                "How many examples do you actually have of this pattern?",
                "What would be more accurate - 'always' or 'sometimes'?"
            ],
            
            "mental_filter": [
                "What positive aspects of this situation are you overlooking?",
                "If you had to list 3 good things about this situation, what would they be?",
                "Are you focusing on one negative detail and ignoring everything else?",
                "What would someone else notice about this situation?",
                "What's the complete picture here, not just the negative part?"
            ],
            
            "discounting_positive": [
                "Why doesn't this positive thing count?",
                "Would you dismiss a friend's accomplishments this way?",
                "What would it mean if this positive experience actually does matter?",
                "Are you setting an impossible standard for what counts as success?",
                "How would you help a friend who was dismissing their own achievements?"
            ],
            
            "mind_reading": [
                "What actual evidence do you have for what they're thinking?",
                "Could there be other explanations for their behavior?",
                "What would you need to do to actually know what they think?",
                "Are you assuming the worst without checking?",
                "What would happen if you asked them directly?"
            ],
            
            "fortune_telling": [
                "What evidence suggests this outcome is certain?",
                "What other outcomes are possible?",
                "Have you been wrong about predictions before?",
                "What would you do if this prediction doesn't come true?",
                "How often do your worst-case predictions actually happen?"
            ],
            
            "magnification": [
                "How important will this be in 5 years?",
                "On a scale of 1-10, how serious is this really?",
                "What's the worst that could realistically happen?",
                "Are you turning a problem into a catastrophe?",
                "How would you help a friend who was facing this same situation?"
            ],
            
            "emotional_reasoning": [
                "Just because you feel this way, does it make it true?",
                "What would the evidence say, separate from your feelings?",
                "Could your emotions be influenced by other factors?",
                "What would you conclude if you weren't feeling this way?",
                "How reliable are feelings as sources of factual information?"
            ],
            
            "should_statements": [
                "According to who says this should be this way?",
                "What would happen if you replaced 'should' with 'prefer'?",
                "Are you using rules that don't actually exist?",
                "How realistic is this expectation?",
                "What would be a more flexible way to think about this?"
            ],
            
            "labeling": [
                "Are you defining yourself by one characteristic or mistake?",
                "What evidence contradicts this label?",
                "Would you call a friend this name for the same behavior?",
                "What's the difference between what you did and who you are?",
                "How would describing the behavior (instead of labeling) change things?"
            ],
            
            "personalization": [
                "What other factors might have contributed to this outcome?",
                "How much control did you actually have over this situation?",
                "Would you blame a friend this much for the same outcome?",
                "What percentage of responsibility is really yours?",
                "What would happen if you weren't responsible for everything?"
            ]
        }
        
        return question_templates.get(distortion_type, [
            "What evidence supports this thought?",
            "What evidence contradicts this thought?",
            "Is there another way to look at this?",
            "What would you tell a friend in this situation?",
            "How helpful is this thought?"
        ])
    
    def create_distortion_challenge(self, identification: DistortionIdentification, distortion_type: str) -> DistortionChallenge:
        challenge_id = f"challenge_{identification.identification_id}_{distortion_type}"
        
        challenge = DistortionChallenge(
            challenge_id=challenge_id,
            identification_id=identification.identification_id,
            distortion_type=distortion_type,
            original_thought=identification.original_thought,
            challenge_questions=self.generate_challenge_questions(distortion_type, identification.original_thought),
            evidence_collected={},
            alternative_thoughts=[],
            created_date=datetime.now()
        )
        
        return challenge
    
    def save_distortion_identification(self, identification: DistortionIdentification, patient_id: str):
        identification.patient_id = patient_id
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO distortion_identifications (
                    identification_id, patient_id, original_thought, distortions_found,
                    severity_levels, confidence_scores, context_factors, created_date, session_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                identification.identification_id, identification.patient_id, identification.original_thought,
                json.dumps(identification.distortions_found), json.dumps(identification.severity_levels),
                json.dumps(identification.confidence_scores), json.dumps(identification.context_factors),
                identification.created_date, identification.session_id
            ))
            conn.commit()
    
    def save_distortion_challenge(self, challenge: DistortionChallenge):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO distortion_challenges (
                    challenge_id, identification_id, distortion_type, original_thought,
                    challenge_questions, evidence_collected, alternative_thoughts,
                    effectiveness_rating, created_date, completed_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                challenge.challenge_id, challenge.identification_id, challenge.distortion_type,
                challenge.original_thought, json.dumps(challenge.challenge_questions),
                json.dumps(challenge.evidence_collected), json.dumps(challenge.alternative_thoughts),
                challenge.effectiveness_rating, challenge.created_date, challenge.completed_date
            ))
            conn.commit()
    
    def get_patient_distortion_patterns(self, patient_id: str, days: int = 30) -> Dict[str, Any]:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT distortions_found, severity_levels, created_date
                FROM distortion_identifications
                WHERE patient_id = ? AND created_date >= ?
            """, (patient_id, start_date))
            
            records = cursor.fetchall()
        
        if not records:
            return {"error": "No distortion records found"}
        
        distortion_counts = {}
        severity_totals = {}
        dates = []
        
        for row in records:
            distortions = json.loads(row[0])
            severities = json.loads(row[1])
            dates.append(datetime.fromisoformat(row[2]))
            
            for distortion in distortions:
                distortion_counts[distortion] = distortion_counts.get(distortion, 0) + 1
                severity = severities.get(distortion, 1)
                if distortion not in severity_totals:
                    severity_totals[distortion] = {"total": 0, "count": 0}
                severity_totals[distortion]["total"] += severity
                severity_totals[distortion]["count"] += 1
        
        most_common = sorted(distortion_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        average_severities = {}
        for distortion, data in severity_totals.items():
            average_severities[distortion] = round(data["total"] / data["count"], 1)
        
        frequency_trend = "stable"
        if len(dates) > 1:
            recent_count = len([d for d in dates if d >= datetime.now() - timedelta(days=7)])
            older_count = len([d for d in dates if d < datetime.now() - timedelta(days=7)])
            if recent_count > older_count * 1.2:
                frequency_trend = "increasing"
            elif recent_count < older_count * 0.8:
                frequency_trend = "decreasing"
        
        patterns = {
            "analysis_period_days": days,
            "total_identifications": len(records),
            "most_common_distortions": [
                {"distortion": dist, "frequency": count, "average_severity": average_severities.get(dist, 1)}
                for dist, count in most_common
            ],
            "frequency_trend": frequency_trend,
            "recommendations": self._generate_distortion_recommendations(most_common, average_severities)
        }
        
        return patterns
    
    def _generate_distortion_recommendations(self, most_common: List[Tuple], severities: Dict[str, float]) -> List[str]:
        recommendations = []
        
        if not most_common:
            return ["Continue monitoring thoughts for cognitive distortions"]
        
        top_distortion = most_common[0][0]
        
        distortion_recommendations = {
            "all_or_nothing": [
                "Practice finding middle ground between extremes",
                "Use percentage thinking instead of absolute terms",
                "Look for exceptions to absolute statements"
            ],
            "overgeneralization": [
                "Focus on specific situations rather than broad patterns",
                "Collect counter-examples to challenge generalizations",
                "Use 'sometimes' instead of 'always'"
            ],
            "mental_filter": [
                "Practice noting both positive and negative aspects",
                "Keep a daily gratitude or positive events log",
                "Challenge yourself to find three good things in difficult situations"
            ],
            "mind_reading": [
                "Practice checking assumptions with direct communication",
                "Generate alternative explanations for others' behavior",
                "Focus on observable facts rather than assumed thoughts"
            ],
            "fortune_telling": [
                "Practice uncertainty tolerance - 'I don't know what will happen'",
                "Generate multiple possible outcomes, not just negative ones",
                "Review past predictions to check accuracy"
            ],
            "magnification": [
                "Use the '5-year rule' - will this matter in 5 years?",
                "Rate problems on a 1-10 scale for realistic perspective",
                "Practice distinguishing between problems and catastrophes"
            ]
        }
        
        specific_recs = distortion_recommendations.get(top_distortion, [
            "Continue working on identifying and challenging this distortion",
            "Practice alternative ways of thinking about situations"
        ])
        
        recommendations.extend(specific_recs)
        
        if len(most_common) > 3:
            recommendations.append("Focus on the top 2-3 most frequent distortions rather than trying to address all at once")
        
        high_severity = [dist for dist, sev in severities.items() if sev >= 2.5]
        if high_severity:
            recommendations.append(f"Pay special attention to {high_severity[0]} as it shows high severity ratings")
        
        return recommendations
    
    def generate_distortion_homework(self, patient_id: str) -> Dict[str, Any]:
        patterns = self.get_patient_distortion_patterns(patient_id, days=14)
        
        if "error" in patterns:
            focus_distortion = "general"
        else:
            most_common = patterns.get("most_common_distortions", [])
            focus_distortion = most_common[0]["distortion"] if most_common else "general"
        
        homework_exercises = {
            "all_or_nothing": {
                "title": "Finding the Gray Areas",
                "daily_practice": [
                    "Notice absolute words (always, never, completely)",
                    "Ask: 'What percentage of the time is this true?'",
                    "Practice using words like 'sometimes', 'often', 'rarely'",
                    "Look for evidence that contradicts absolute statements"
                ],
                "tracking": "Record instances of all-or-nothing thinking and practice finding middle ground"
            },
            
            "overgeneralization": {
                "title": "Challenging Broad Conclusions",
                "daily_practice": [
                    "Notice words like 'all', 'every', 'always' in your thoughts",
                    "Ask: 'How many examples do I actually have?'",
                    "Look for counter-examples that don't fit the pattern",
                    "Practice being more specific about situations"
                ],
                "tracking": "Keep a log of generalizations and specific counter-examples"
            },
            
            "mental_filter": {
                "title": "Balanced Perspective Practice",
                "daily_practice": [
                    "When you notice focusing on negatives, deliberately look for positives",
                    "Practice the 'Three Good Things' exercise daily",
                    "Ask: 'What am I overlooking in this situation?'",
                    "Rate situations on both positive and negative aspects"
                ],
                "tracking": "Daily log of both positive and negative aspects of situations"
            },
            
            "general": {
                "title": "Cognitive Distortion Detection",
                "daily_practice": [
                    "Monitor thoughts during emotional situations",
                    "Use distortion identification checklist",
                    "Practice challenging questions for each distortion found",
                    "Develop alternative, more balanced thoughts"
                ],
                "tracking": "Complete thought records focusing on distortion identification"
            }
        }
        
        exercise = homework_exercises.get(focus_distortion, homework_exercises["general"])
        
        homework = {
            "patient_id": patient_id,
            "focus_distortion": focus_distortion,
            "title": exercise["title"],
            "daily_practice": exercise["daily_practice"],
            "tracking_method": exercise["tracking"],
            "challenge_questions": self.generate_challenge_questions(focus_distortion, ""),
            "success_metrics": [
                "Identify distortions in real-time",
                "Challenge distorted thoughts with questions",
                "Generate more balanced alternative thoughts",
                "Notice reduction in emotional intensity after challenging"
            ]
        }
        
        return homework
    
    def get_distortion_progress(self, patient_id: str, weeks: int = 4) -> Dict[str, Any]:
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=weeks)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT distortions_found, severity_levels, created_date
                FROM distortion_identifications
                WHERE patient_id = ? AND created_date >= ?
                ORDER BY created_date
            """, (patient_id, start_date))
            
            records = cursor.fetchall()
        
        if not records:
            return {"error": "No progress data found"}
        
        weekly_data = {}
        for row in records:
            distortions = json.loads(row[0])
            severities = json.loads(row[1])
            week = datetime.fromisoformat(row[2]).isocalendar()[1]
            
            if week not in weekly_data:
                weekly_data[week] = {"count": 0, "severity_sum": 0, "distortions": set()}
            
            weekly_data[week]["count"] += len(distortions)
            weekly_data[week]["distortions"].update(distortions)
            
            for distortion in distortions:
                severity = severities.get(distortion, 1)
                weekly_data[week]["severity_sum"] += severity
        
        weekly_progress = []
        for week, data in sorted(weekly_data.items()):
            avg_severity = data["severity_sum"] / data["count"] if data["count"] > 0 else 0
            weekly_progress.append({
                "week": week,
                "total_distortions": data["count"],
                "unique_distortions": len(data["distortions"]),
                "average_severity": round(avg_severity, 1)
            })
        
        trend_analysis = "stable"
        if len(weekly_progress) > 1:
            recent_avg = sum(w["total_distortions"] for w in weekly_progress[-2:]) / 2
            earlier_avg = sum(w["total_distortions"] for w in weekly_progress[:-2]) / len(weekly_progress[:-2]) if len(weekly_progress) > 2 else recent_avg
            
            if recent_avg < earlier_avg * 0.8:
                trend_analysis = "improving"
            elif recent_avg > earlier_avg * 1.2:
                trend_analysis = "worsening"
        
        progress = {
            "analysis_period_weeks": weeks,
            "weekly_breakdown": weekly_progress,
            "trend": trend_analysis,
            "total_identifications": len(records),
            "improvement_indicators": self._generate_improvement_indicators(weekly_progress)
        }
        
        return progress
    
    def _generate_improvement_indicators(self, weekly_progress: List[Dict]) -> List[str]:
        indicators = []
        
        if not weekly_progress:
            return indicators
        
        if len(weekly_progress) > 1:
            recent_week = weekly_progress[-1]
            previous_week = weekly_progress[-2]
            
            if recent_week["total_distortions"] < previous_week["total_distortions"]:
                indicators.append("Decreased total distortions this week")
            
            if recent_week["average_severity"] < previous_week["average_severity"]:
                indicators.append("Reduced average severity of distortions")
            
            if recent_week["unique_distortions"] < previous_week["unique_distortions"]:
                indicators.append("Fewer types of distortions identified")
        
        avg_severity = sum(w["average_severity"] for w in weekly_progress) / len(weekly_progress)
        if avg_severity < 1.5:
            indicators.append("Consistently low severity ratings")
        elif avg_severity > 2.5:
            indicators.append("High severity ratings - focus on intensity reduction")
        
        return indicators
    
    def create_distortion_summary_report(self, patient_id: str, days: int = 30) -> Dict[str, Any]:
        patterns = self.get_patient_distortion_patterns(patient_id, days)
        progress = self.get_distortion_progress(patient_id, weeks=4)
        
        if "error" in patterns:
            return {"error": "Insufficient data for report generation"}
        
        report = {
            "patient_id": patient_id,
            "report_period": f"{days} days",
            "executive_summary": {
                "total_distortion_episodes": patterns["total_identifications"],
                "most_frequent_distortion": patterns["most_common_distortions"][0]["distortion"] if patterns["most_common_distortions"] else "None",
                "trend": progress.get("trend", "stable"),
                "primary_recommendation": patterns["recommendations"][0] if patterns["recommendations"] else "Continue monitoring"
            },
            "detailed_patterns": patterns,
            "progress_tracking": progress,
            "intervention_suggestions": self._generate_intervention_suggestions(patterns, progress)
        }
        
        return report
    
    def _generate_intervention_suggestions(self, patterns: Dict, progress: Dict) -> List[str]:
        suggestions = []
        
        if "most_common_distortions" in patterns and patterns["most_common_distortions"]:
            top_distortion = patterns["most_common_distortions"][0]
            
            if top_distortion["frequency"] > 5:
                suggestions.append(f"Prioritize intensive work on {top_distortion['distortion']} - appears frequently")
            
            if top_distortion["average_severity"] >= 2.5:
                suggestions.append(f"Focus on reducing intensity of {top_distortion['distortion']} episodes")
        
        trend = progress.get("trend", "stable")
        if trend == "worsening":
            suggestions.append("Consider increasing session frequency or adding stress management techniques")
        elif trend == "improving":
            suggestions.append("Current approach is working - maintain consistency")
        
        if len(patterns.get("most_common_distortions", [])) > 5:
            suggestions.append("Many different distortions present - consider foundational cognitive skills work")
        
        return suggestions
    
    def get_distortion_education_content(self, distortion_type: str) -> Dict[str, Any]:
        distortion_info = {
            "all_or_nothing": {
                "name": "All-or-Nothing Thinking",
                "description": "Seeing situations in extreme terms with no middle ground",
                "common_phrases": ["always", "never", "completely", "totally", "everyone", "no one"],
                "examples": [
                    "I always mess up presentations",
                    "Nobody ever listens to me",
                    "I'm a complete failure at relationships"
                ],
                "challenge_strategies": [
                    "Look for evidence of middle ground",
                    "Use percentage thinking - 'What percent of the time?'",
                    "Find exceptions to absolute statements",
                    "Replace extremes with more accurate words like 'sometimes', 'often'"
                ],
                "practice_exercises": [
                    "When you catch an absolute word, immediately ask for a percentage",
                    "List exceptions to any 'always' or 'never' statement",
                    "Practice using graduated language instead of extremes"
                ]
            },
            
            "overgeneralization": {
                "name": "Overgeneralization",
                "description": "Drawing broad conclusions from single events or limited examples",
                "common_phrases": ["all", "every", "this always happens", "typical", "everyone"],
                "examples": [
                    "This presentation went badly, I'm terrible at public speaking",
                    "All relationships end in heartbreak",
                    "Every time I try something new, I fail"
                ],
                "challenge_strategies": [
                    "Ask 'How many examples do I actually have?'",
                    "Look for counter-examples",
                    "Focus on the specific situation rather than creating patterns",
                    "Use precise language about individual events"
                ],
                "practice_exercises": [
                    "When you notice a pattern claim, list specific examples",
                    "Actively search for exceptions to the generalization",
                    "Practice describing single events without broader conclusions"
                ]
            },
            
            "mental_filter": {
                "name": "Mental Filter",
                "description": "Focusing exclusively on negative details while filtering out positive aspects",
                "common_phrases": ["only", "just", "all that matters", "nothing but"],
                "examples": [
                    "The presentation went well, but I stumbled over one word",
                    "Everyone complimented the dinner except one person who seemed unimpressed",
                    "I got mostly good feedback, but there was one criticism"
                ],
                "challenge_strategies": [
                    "Deliberately look for positive aspects you might be ignoring",
                    "Ask 'What am I filtering out?'",
                    "Practice noting both positives and negatives",
                    "Use the 'complete picture' technique"
                ],
                "practice_exercises": [
                    "Daily practice: find three positive things in challenging situations",
                    "Keep a balanced perspective journal with both positives and negatives",
                    "When focusing on negatives, force yourself to identify equal number of positives"
                ]
            },
            
            "mind_reading": {
                "name": "Mind Reading",
                "description": "Assuming you know what others are thinking without evidence",
                "common_phrases": ["he thinks", "she knows", "they can see", "everyone realizes"],
                "examples": [
                    "She thinks I'm boring",
                    "He can tell I'm nervous",
                    "They all know I don't belong here"
                ],
                "challenge_strategies": [
                    "Ask 'What evidence do I have for this?'",
                    "Consider alternative explanations for behavior",
                    "Practice direct communication instead of assuming",
                    "Focus on what you can observe, not what you imagine"
                ],
                "practice_exercises": [
                    "When you catch yourself mind reading, generate 3 alternative explanations",
                    "Practice asking people directly instead of guessing",
                    "Keep a reality check log - how often are your assumptions correct?"
                ]
            }
        }
        
        return distortion_info.get(distortion_type, {
            "name": "Unknown Distortion",
            "description": "Information not available for this distortion type",
            "challenge_strategies": [
                "Question the accuracy of the thought",
                "Look for evidence both for and against",
                "Consider alternative perspectives",
                "Ask what you would tell a friend"
            ]
        })
    
    def create_distortion_intervention_plan(self, patient_id: str) -> Dict[str, Any]:
        patterns = self.get_patient_distortion_patterns(patient_id, days=21)
        
        if "error" in patterns:
            return {
                "plan_type": "foundational",
                "focus": "Basic distortion awareness and identification",
                "interventions": [
                    "Psychoeducation about cognitive distortions",
                    "Daily thought monitoring",
                    "Basic challenging questions practice"
                ]
            }
        
        top_distortions = patterns["most_common_distortions"][:3]
        
        intervention_plan = {
            "patient_id": patient_id,
            "plan_type": "targeted",
            "primary_targets": [d["distortion"] for d in top_distortions],
            "intervention_phases": []
        }
        
        for i, distortion_data in enumerate(top_distortions):
            distortion = distortion_data["distortion"]
            frequency = distortion_data["frequency"]
            severity = distortion_data["average_severity"]
            
            phase = {
                "phase": i + 1,
                "target_distortion": distortion,
                "duration_weeks": 2 if severity < 2 else 3,
                "interventions": [],
                "homework_assignments": [],
                "success_criteria": []
            }
            
            education = self.get_distortion_education_content(distortion)
            
            phase["interventions"] = [
                f"Psychoeducation about {education['name']}",
                "In-session practice with personal examples",
                "Challenge question development",
                "Alternative thought generation practice"
            ]
            
            phase["homework_assignments"] = [
                f"Daily monitoring for {distortion} instances",
                "Complete thought records using specific challenge questions",
                "Practice exercises: " + "; ".join(education.get("practice_exercises", [])[:2])
            ]
            
            phase["success_criteria"] = [
                f"Identify {distortion} in real-time at least 80% of the time",
                "Generate appropriate challenge questions independently",
                f"Reduce average severity from {severity} to below 2.0",
                "Create balanced alternative thoughts"
            ]
            
            intervention_plan["intervention_phases"].append(phase)
        
        return intervention_plan
    
    def track_intervention_effectiveness(self, patient_id: str, intervention_start_date: datetime) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT distortions_found, severity_levels, created_date
                FROM distortion_identifications
                WHERE patient_id = ? AND created_date >= ?
                ORDER BY created_date
            """, (patient_id, intervention_start_date))
            
            post_intervention = cursor.fetchall()
            
            cursor.execute("""
                SELECT distortions_found, severity_levels, created_date
                FROM distortion_identifications
                WHERE patient_id = ? AND created_date < ?
                ORDER BY created_date DESC
                LIMIT 20
            """, (patient_id, intervention_start_date))
            
            pre_intervention = cursor.fetchall()
        
        if not pre_intervention or not post_intervention:
            return {"error": "Insufficient data for effectiveness tracking"}
        
        def analyze_period(records):
            total_distortions = 0
            severity_sum = 0
            distortion_types = set()
            
            for row in records:
                distortions = json.loads(row[0])
                severities = json.loads(row[1])
                total_distortions += len(distortions)
                distortion_types.update(distortions)
                
                for d in distortions:
                    severity_sum += severities.get(d, 1)
            
            return {
                "total_episodes": total_distortions,
                "unique_types": len(distortion_types),
                "average_severity": severity_sum / total_distortions if total_distortions > 0 else 0,
                "episodes_per_record": total_distortions / len(records) if records else 0
            }
        
        pre_stats = analyze_period(pre_intervention)
        post_stats = analyze_period(post_intervention)
        
        effectiveness = {
            "intervention_start": intervention_start_date.strftime('%Y-%m-%d'),
            "pre_intervention": pre_stats,
            "post_intervention": post_stats,
            "improvements": {
                "episode_reduction": pre_stats["total_episodes"] - post_stats["total_episodes"],
                "severity_reduction": round(pre_stats["average_severity"] - post_stats["average_severity"], 2),
                "type_reduction": pre_stats["unique_types"] - post_stats["unique_types"]
            },
            "effectiveness_rating": self._calculate_effectiveness_rating(pre_stats, post_stats)
        }
        
        return effectiveness
    
    def _calculate_effectiveness_rating(self, pre_stats: Dict, post_stats: Dict) -> str:
        episode_improvement = (pre_stats["total_episodes"] - post_stats["total_episodes"]) / pre_stats["total_episodes"] if pre_stats["total_episodes"] > 0 else 0
        severity_improvement = (pre_stats["average_severity"] - post_stats["average_severity"]) / pre_stats["average_severity"] if pre_stats["average_severity"] > 0 else 0
        
        overall_improvement = (episode_improvement + severity_improvement) / 2
        
        if overall_improvement >= 0.4:
            return "highly_effective"
        elif overall_improvement >= 0.2:
            return "moderately_effective"
        elif overall_improvement >= 0.1:
            return "mildly_effective"
        else:
            return "minimal_effectiveness"
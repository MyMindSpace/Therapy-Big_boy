import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from enum import Enum
from dataclasses import dataclass
import json

from config.therapy_protocols import TherapyModality, InterventionType


class ChallengeType(Enum):
    EVIDENCE_EXAMINATION = "evidence_examination"
    ALTERNATIVE_PERSPECTIVES = "alternative_perspectives"
    CATASTROPHIC_THINKING = "catastrophic_thinking"
    COST_BENEFIT_ANALYSIS = "cost_benefit_analysis"
    PROBABILITY_ESTIMATION = "probability_estimation"
    WORST_BEST_REALISTIC = "worst_best_realistic"
    FRIEND_PERSPECTIVE = "friend_perspective"
    TIME_PERSPECTIVE = "time_perspective"


class ThoughtCategory(Enum):
    SELF_CRITICISM = "self_criticism"
    WORRY_ANXIETY = "worry_anxiety"
    DEPRESSION = "depression"
    ANGER_IRRITATION = "anger_irritation"
    PERFECTIONISM = "perfectionism"
    RELATIONSHIPS = "relationships"
    WORK_PERFORMANCE = "work_performance"
    HEALTH_BODY = "health_body"


@dataclass
class ThoughtChallenge:
    challenge_id: str
    patient_id: str
    original_thought: str
    thought_category: str
    emotion: str
    emotion_intensity_before: int
    situation_context: str
    challenge_type: ChallengeType
    challenge_questions: List[str]
    responses: List[str]
    evidence_for: List[str]
    evidence_against: List[str]
    alternative_thoughts: List[str]
    new_balanced_thought: str
    emotion_intensity_after: int
    confidence_in_original: int
    confidence_in_balanced: int
    created_date: datetime
    completed_date: Optional[datetime] = None
    session_id: Optional[str] = None
    effectiveness_rating: Optional[int] = None


@dataclass
class ChallengeTemplate:
    template_id: str
    name: str
    challenge_type: ChallengeType
    target_categories: List[str]
    description: str
    questions: List[str]
    follow_up_questions: List[str]
    effectiveness_indicators: List[str]


class ThoughtChallenger:
    
    def __init__(self, db_path: str = "data/therapy_system.db"):
        self.db_path = db_path
        self._initialize_database()
        self._load_challenge_templates()
    
    def _initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS thought_challenges (
                    challenge_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    original_thought TEXT NOT NULL,
                    thought_category TEXT,
                    emotion TEXT,
                    emotion_intensity_before INTEGER,
                    situation_context TEXT,
                    challenge_type TEXT,
                    challenge_questions TEXT,
                    responses TEXT,
                    evidence_for TEXT,
                    evidence_against TEXT,
                    alternative_thoughts TEXT,
                    new_balanced_thought TEXT,
                    emotion_intensity_after INTEGER,
                    confidence_in_original INTEGER,
                    confidence_in_balanced INTEGER,
                    created_date TIMESTAMP,
                    completed_date TIMESTAMP,
                    session_id TEXT,
                    effectiveness_rating INTEGER,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS challenge_templates (
                    template_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    challenge_type TEXT NOT NULL,
                    target_categories TEXT,
                    description TEXT,
                    questions TEXT,
                    follow_up_questions TEXT,
                    effectiveness_indicators TEXT,
                    is_default BOOLEAN DEFAULT FALSE
                )
            """)
            
            conn.commit()
    
    def _load_challenge_templates(self):
        templates = [
            ChallengeTemplate(
                template_id="evidence_001",
                name="Evidence Examination",
                challenge_type=ChallengeType.EVIDENCE_EXAMINATION,
                target_categories=["self_criticism", "worry_anxiety", "depression"],
                description="Systematically examine evidence for and against the thought",
                questions=[
                    "What evidence do I have that this thought is true?",
                    "What evidence do I have that this thought is not true or not completely true?",
                    "What would I tell a good friend who had this thought?",
                    "What evidence would convince me that this thought might be wrong?",
                    "Am I confusing a thought with a fact?",
                    "What would someone who disagreed with this thought say?",
                    "What are the facts of the situation, separate from my interpretation?"
                ],
                follow_up_questions=[
                    "How strong is the evidence on each side?",
                    "What would a neutral observer conclude?",
                    "What assumptions am I making?"
                ],
                effectiveness_indicators=[
                    "Reduced emotional intensity",
                    "Identification of contradictory evidence",
                    "More balanced perspective"
                ]
            ),
            
            ChallengeTemplate(
                template_id="alternative_001",
                name="Alternative Perspectives",
                challenge_type=ChallengeType.ALTERNATIVE_PERSPECTIVES,
                target_categories=["relationships", "work_performance", "worry_anxiety"],
                description="Generate multiple alternative explanations for situations",
                questions=[
                    "What are other possible explanations for this situation?",
                    "If my best friend was in this situation, what would I tell them?",
                    "What would someone who cares about me say about this?",
                    "How might someone else interpret this situation?",
                    "What would I think about this if I was in a better mood?",
                    "What are some other ways to look at this?",
                    "What would I have thought about this last year?"
                ],
                follow_up_questions=[
                    "Which alternative seems most likely?",
                    "What would change if I adopted this alternative view?",
                    "How would this alternative affect my feelings?"
                ],
                effectiveness_indicators=[
                    "Multiple perspectives generated",
                    "Reduced certainty in original thought",
                    "Increased flexibility in thinking"
                ]
            ),
            
            ChallengeTemplate(
                template_id="catastrophic_001",
                name="Catastrophic Thinking Challenge",
                challenge_type=ChallengeType.CATASTROPHIC_THINKING,
                target_categories=["worry_anxiety", "perfectionism"],
                description="Challenge catastrophic predictions and worst-case scenarios",
                questions=[
                    "What's the worst that could realistically happen?",
                    "What's the best that could happen?",
                    "What's most likely to happen?",
                    "If the worst did happen, how would I cope?",
                    "How important will this be in 5 years?",
                    "Am I overestimating how bad this would be?",
                    "Am I underestimating my ability to cope with problems?"
                ],
                follow_up_questions=[
                    "What resources would help me cope?",
                    "Have I handled difficult situations before?",
                    "What would I tell someone else in this situation?"
                ],
                effectiveness_indicators=[
                    "Realistic assessment of probability",
                    "Recognition of coping abilities",
                    "Reduced anxiety about outcomes"
                ]
            ),
            
            ChallengeTemplate(
                template_id="cost_benefit_001",
                name="Cost-Benefit Analysis",
                challenge_type=ChallengeType.COST_BENEFIT_ANALYSIS,
                target_categories=["perfectionism", "self_criticism", "work_performance"],
                description="Analyze advantages and disadvantages of holding the thought",
                questions=[
                    "What are the advantages of thinking this way?",
                    "What are the disadvantages of thinking this way?",
                    "How does this thought help me?",
                    "How does this thought hurt me?",
                    "What does believing this thought cost me emotionally?",
                    "What would I gain by letting go of this thought?",
                    "Is this thought worth the emotional energy it requires?"
                ],
                follow_up_questions=[
                    "Do the costs outweigh the benefits?",
                    "What would be a more helpful way to think?",
                    "How would changing this thought change my behavior?"
                ],
                effectiveness_indicators=[
                    "Clear identification of costs and benefits",
                    "Motivation to change thinking pattern",
                    "Recognition of thought's impact"
                ]
            ),
            
            ChallengeTemplate(
                template_id="friend_001",
                name="Friend Perspective",
                challenge_type=ChallengeType.FRIEND_PERSPECTIVE,
                target_categories=["self_criticism", "depression", "perfectionism"],
                description="Consider what you would tell a friend in the same situation",
                questions=[
                    "What would I tell my best friend if they had this thought?",
                    "What would someone who loves me say about this thought?",
                    "How would I comfort a friend who was thinking this way?",
                    "What advice would I give to someone I care about?",
                    "Would I be this harsh with a friend?",
                    "What would a caring, wise friend tell me right now?",
                    "How would I help a friend challenge this thought?"
                ],
                follow_up_questions=[
                    "Why is it easier to be kind to others than to myself?",
                    "What would happen if I treated myself like I treat my friends?",
                    "How can I be my own good friend right now?"
                ],
                effectiveness_indicators=[
                    "Increased self-compassion",
                    "Recognition of double standards",
                    "More balanced self-talk"
                ]
            ),
            
            ChallengeTemplate(
                template_id="time_001",
                name="Time Perspective",
                challenge_type=ChallengeType.TIME_PERSPECTIVE,
                target_categories=["worry_anxiety", "anger_irritation", "perfectionism"],
                description="Examine the thought from different time perspectives",
                questions=[
                    "How will I feel about this in an hour?",
                    "How will I feel about this tomorrow?",
                    "How will I feel about this in a week?",
                    "How will I feel about this in a month?",
                    "How will I feel about this in a year?",
                    "Will this matter in 5 years?",
                    "How did I handle similar situations in the past?"
                ],
                follow_up_questions=[
                    "What does this time perspective tell me?",
                    "How does thinking about the future change how I feel now?",
                    "What have I learned from past similar experiences?"
                ],
                effectiveness_indicators=[
                    "Reduced immediate emotional intensity",
                    "Broader perspective on situation",
                    "Recognition of temporary nature"
                ]
            )
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM challenge_templates WHERE is_default = TRUE")
            count = cursor.fetchone()[0]
            
            if count == 0:
                for template in templates:
                    cursor.execute("""
                        INSERT INTO challenge_templates (
                            template_id, name, challenge_type, target_categories,
                            description, questions, follow_up_questions,
                            effectiveness_indicators, is_default
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        template.template_id, template.name, template.challenge_type.value,
                        json.dumps(template.target_categories), template.description,
                        json.dumps(template.questions), json.dumps(template.follow_up_questions),
                        json.dumps(template.effectiveness_indicators), True
                    ))
                conn.commit()
    
    def categorize_thought(self, thought: str, emotion: str = "", context: str = "") -> str:
        thought_lower = thought.lower()
        context_lower = context.lower()
        emotion_lower = emotion.lower()
        
        category_indicators = {
            "self_criticism": [
                "I'm", "I am", "stupid", "worthless", "failure", "can't do anything",
                "terrible at", "not good enough", "should be better", "disappointing"
            ],
            "worry_anxiety": [
                "what if", "worried about", "anxious", "something bad", "go wrong",
                "can't handle", "disaster", "terrible", "scared that"
            ],
            "depression": [
                "hopeless", "pointless", "nothing matters", "no one cares", "give up",
                "can't see", "dark", "empty", "meaningless"
            ],
            "perfectionism": [
                "should be perfect", "must be", "have to", "not good enough",
                "mistake", "mess up", "flawless", "exactly right"
            ],
            "relationships": [
                "he thinks", "she said", "they don't", "nobody likes", "rejected",
                "relationship", "friend", "family", "partner", "love"
            ],
            "work_performance": [
                "work", "job", "boss", "colleagues", "performance", "career",
                "promotion", "fired", "incompetent", "professional"
            ],
            "anger_irritation": [
                "angry", "furious", "irritated", "annoyed", "hate", "can't stand",
                "ridiculous", "unfair", "shouldn't have"
            ]
        }
        
        emotion_categories = {
            "angry": "anger_irritation",
            "sad": "depression",
            "worried": "worry_anxiety",
            "anxious": "worry_anxiety",
            "frustrated": "anger_irritation",
            "ashamed": "self_criticism",
            "guilty": "self_criticism"
        }
        
        if emotion_lower in emotion_categories:
            return emotion_categories[emotion_lower]
        
        scores = {}
        for category, indicators in category_indicators.items():
            score = 0
            for indicator in indicators:
                if indicator in thought_lower:
                    score += 2
                if indicator in context_lower:
                    score += 1
            scores[category] = score
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return "worry_anxiety"
    
    def select_challenge_method(self, thought_category: str, thought: str) -> ChallengeType:
        thought_lower = thought.lower()
        
        if "worst" in thought_lower or "terrible" in thought_lower or "disaster" in thought_lower:
            return ChallengeType.CATASTROPHIC_THINKING
        
        if thought_category == "self_criticism":
            return ChallengeType.FRIEND_PERSPECTIVE
        elif thought_category == "worry_anxiety":
            if "what if" in thought_lower:
                return ChallengeType.CATASTROPHIC_THINKING
            else:
                return ChallengeType.EVIDENCE_EXAMINATION
        elif thought_category == "perfectionism":
            return ChallengeType.COST_BENEFIT_ANALYSIS
        elif thought_category == "relationships":
            return ChallengeType.ALTERNATIVE_PERSPECTIVES
        elif thought_category == "anger_irritation":
            return ChallengeType.TIME_PERSPECTIVE
        else:
            return ChallengeType.EVIDENCE_EXAMINATION
    
    def create_thought_challenge(
        self,
        patient_id: str,
        original_thought: str,
        emotion: str,
        emotion_intensity: int,
        situation_context: str = "",
        session_id: Optional[str] = None
    ) -> ThoughtChallenge:
        
        challenge_id = f"challenge_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        thought_category = self.categorize_thought(original_thought, emotion, situation_context)
        challenge_type = self.select_challenge_method(thought_category, original_thought)
        challenge_questions = self.get_challenge_questions(challenge_type, thought_category)
        
        challenge = ThoughtChallenge(
            challenge_id=challenge_id,
            patient_id=patient_id,
            original_thought=original_thought,
            thought_category=thought_category,
            emotion=emotion,
            emotion_intensity_before=emotion_intensity,
            situation_context=situation_context,
            challenge_type=challenge_type,
            challenge_questions=challenge_questions,
            responses=[],
            evidence_for=[],
            evidence_against=[],
            alternative_thoughts=[],
            new_balanced_thought="",
            emotion_intensity_after=0,
            confidence_in_original=0,
            confidence_in_balanced=0,
            created_date=datetime.now(),
            session_id=session_id
        )
        
        return challenge
    
    def get_challenge_questions(self, challenge_type: ChallengeType, thought_category: str) -> List[str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT questions FROM challenge_templates 
                WHERE challenge_type = ? AND ? IN (
                    SELECT json_each.value FROM json_each(target_categories)
                )
            """, (challenge_type.value, thought_category))
            
            result = cursor.fetchone()
            if result:
                return json.loads(result[0])
        
        default_questions = {
            ChallengeType.EVIDENCE_EXAMINATION: [
                "What evidence supports this thought?",
                "What evidence contradicts this thought?",
                "What would a neutral observer say?",
                "Am I confusing thoughts with facts?"
            ],
            ChallengeType.ALTERNATIVE_PERSPECTIVES: [
                "What are other ways to view this situation?",
                "How would someone else interpret this?",
                "What would I tell a friend in this situation?",
                "What other explanations are possible?"
            ],
            ChallengeType.CATASTROPHIC_THINKING: [
                "What's the worst that could realistically happen?",
                "What's most likely to happen?",
                "How would I cope if this happened?",
                "How important will this be in the future?"
            ]
        }
        
        return default_questions.get(challenge_type, [
            "Is this thought helpful?",
            "Is this thought accurate?",
            "What would be a more balanced thought?",
            "How would changing this thought change my feelings?"
        ])
    
    def complete_challenge(
        self,
        challenge: ThoughtChallenge,
        responses: List[str],
        evidence_for: List[str],
        evidence_against: List[str],
        alternative_thoughts: List[str],
        new_balanced_thought: str,
        emotion_intensity_after: int,
        confidence_in_original: int,
        confidence_in_balanced: int,
        effectiveness_rating: int
    ) -> ThoughtChallenge:
        
        challenge.responses = responses
        challenge.evidence_for = evidence_for
        challenge.evidence_against = evidence_against
        challenge.alternative_thoughts = alternative_thoughts
        challenge.new_balanced_thought = new_balanced_thought
        challenge.emotion_intensity_after = emotion_intensity_after
        challenge.confidence_in_original = confidence_in_original
        challenge.confidence_in_balanced = confidence_in_balanced
        challenge.completed_date = datetime.now()
        challenge.effectiveness_rating = effectiveness_rating
        
        self.save_challenge(challenge)
        return challenge
    
    def save_challenge(self, challenge: ThoughtChallenge):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO thought_challenges (
                    challenge_id, patient_id, original_thought, thought_category,
                    emotion, emotion_intensity_before, situation_context,
                    challenge_type, challenge_questions, responses, evidence_for,
                    evidence_against, alternative_thoughts, new_balanced_thought,
                    emotion_intensity_after, confidence_in_original, confidence_in_balanced,
                    created_date, completed_date, session_id, effectiveness_rating
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                challenge.challenge_id, challenge.patient_id, challenge.original_thought,
                challenge.thought_category, challenge.emotion, challenge.emotion_intensity_before,
                challenge.situation_context, challenge.challenge_type.value,
                json.dumps(challenge.challenge_questions), json.dumps(challenge.responses),
                json.dumps(challenge.evidence_for), json.dumps(challenge.evidence_against),
                json.dumps(challenge.alternative_thoughts), challenge.new_balanced_thought,
                challenge.emotion_intensity_after, challenge.confidence_in_original,
                challenge.confidence_in_balanced, challenge.created_date, challenge.completed_date,
                challenge.session_id, challenge.effectiveness_rating
            ))
            conn.commit()
    
    def get_patient_challenges(self, patient_id: str, limit: int = 10) -> List[ThoughtChallenge]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM thought_challenges 
                WHERE patient_id = ? 
                ORDER BY created_date DESC 
                LIMIT ?
            """, (patient_id, limit))
            
            challenges = []
            for row in cursor.fetchall():
                challenge = ThoughtChallenge(
                    challenge_id=row[0],
                    patient_id=row[1],
                    original_thought=row[2],
                    thought_category=row[3],
                    emotion=row[4],
                    emotion_intensity_before=row[5],
                    situation_context=row[6] or "",
                    challenge_type=ChallengeType(row[7]),
                    challenge_questions=json.loads(row[8] or '[]'),
                    responses=json.loads(row[9] or '[]'),
                    evidence_for=json.loads(row[10] or '[]'),
                    evidence_against=json.loads(row[11] or '[]'),
                    alternative_thoughts=json.loads(row[12] or '[]'),
                    new_balanced_thought=row[13] or "",
                    emotion_intensity_after=row[14] or 0,
                    confidence_in_original=row[15] or 0,
                    confidence_in_balanced=row[16] or 0,
                    created_date=datetime.fromisoformat(row[17]),
                    completed_date=datetime.fromisoformat(row[18]) if row[18] else None,
                    session_id=row[19],
                    effectiveness_rating=row[20]
                )
                challenges.append(challenge)
            
            return challenges
    
    def analyze_challenge_effectiveness(self, patient_id: str, days: int = 30) -> Dict[str, Any]:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT emotion_intensity_before, emotion_intensity_after, 
                       confidence_in_original, confidence_in_balanced,
                       effectiveness_rating, challenge_type, thought_category
                FROM thought_challenges 
                WHERE patient_id = ? AND created_date >= ? AND completed_date IS NOT NULL
            """, (patient_id, start_date))
            
            challenges = cursor.fetchall()
        
        if not challenges:
            return {"error": "No completed challenges found"}
        
        total_challenges = len(challenges)
        emotion_improvements = []
        confidence_changes = []
        effectiveness_ratings = []
        method_effectiveness = {}
        category_effectiveness = {}
        
        for row in challenges:
            before_emotion, after_emotion, conf_orig, conf_balanced, rating, method, category = row
            
            if before_emotion and after_emotion:
                improvement = before_emotion - after_emotion
                emotion_improvements.append(improvement)
            
            if conf_orig and conf_balanced:
                confidence_change = conf_orig - conf_balanced
                confidence_changes.append(confidence_change)
            
            if rating:
                effectiveness_ratings.append(rating)
            
            if method not in method_effectiveness:
                method_effectiveness[method] = []
            if rating:
                method_effectiveness[method].append(rating)
            
            if category not in category_effectiveness:
                category_effectiveness[category] = []
            if rating:
                category_effectiveness[category].append(rating)
        
        avg_emotion_improvement = sum(emotion_improvements) / len(emotion_improvements) if emotion_improvements else 0
        avg_confidence_change = sum(confidence_changes) / len(confidence_changes) if confidence_changes else 0
        avg_effectiveness = sum(effectiveness_ratings) / len(effectiveness_ratings) if effectiveness_ratings else 0
        
        best_methods = []
        for method, ratings in method_effectiveness.items():
            if len(ratings) >= 3:
                avg_rating = sum(ratings) / len(ratings)
                best_methods.append((method, avg_rating, len(ratings)))
        
        best_methods.sort(key=lambda x: x[1], reverse=True)
        
        analysis = {
            "analysis_period_days": days,
            "total_completed_challenges": total_challenges,
            "average_emotion_improvement": round(avg_emotion_improvement, 1),
            "average_confidence_change": round(avg_confidence_change, 1),
            "average_effectiveness_rating": round(avg_effectiveness, 1),
            "most_effective_methods": [
                {"method": method, "avg_rating": round(rating, 1), "uses": count}
                for method, rating, count in best_methods[:3]
            ],
            "success_rate": len([r for r in effectiveness_ratings if r >= 3]) / len(effectiveness_ratings) * 100 if effectiveness_ratings else 0,
            "recommendations": self._generate_challenge_recommendations(best_methods, avg_emotion_improvement, avg_effectiveness)
        }
        
        return analysis
    
    def _generate_challenge_recommendations(self, best_methods: List, avg_improvement: float, avg_effectiveness: float) -> List[str]:
        recommendations = []
        
        if avg_improvement < 1.0:
            recommendations.append("Consider spending more time on evidence gathering before challenging")
            recommendations.append("Practice generating more alternative thoughts for each situation")
        elif avg_improvement >= 2.0:
            recommendations.append("Excellent emotion regulation through thought challenging - maintain current approach")
        
        if avg_effectiveness < 3.0:
            recommendations.append("Focus on thought challenging techniques that feel most natural and effective")
            recommendations.append("Consider increasing session frequency for more intensive practice")
        
        if best_methods:
            top_method = best_methods[0][0].replace('_', ' ').title()
            recommendations.append(f"{top_method} appears most effective - consider using this approach more frequently")
        
        if len(best_methods) < 2:
            recommendations.append("Experiment with different challenging techniques to find what works best")
        
        return recommendations
    
    def create_personalized_challenge_plan(self, patient_id: str) -> Dict[str, Any]:
        analysis = self.analyze_challenge_effectiveness(patient_id, days=21)
        recent_challenges = self.get_patient_challenges(patient_id, limit=5)
        
        if "error" in analysis:
            return {
                "plan_type": "foundational",
                "focus": "Basic thought challenging skills",
                "recommended_methods": ["evidence_examination", "friend_perspective"],
                "practice_frequency": "daily",
                "session_goals": [
                    "Learn to identify automatic thoughts",
                    "Practice basic questioning techniques",
                    "Develop awareness of thought-emotion connection"
                ]
            }
        
        common_categories = {}
        for challenge in recent_challenges:
            cat = challenge.thought_category
            common_categories[cat] = common_categories.get(cat, 0) + 1
        
        most_common_category = max(common_categories, key=common_categories.get) if common_categories else "worry_anxiety"
        
        effective_methods = analysis.get("most_effective_methods", [])
        recommended_methods = [method["method"] for method in effective_methods[:2]]
        
        if not recommended_methods:
            if most_common_category == "self_criticism":
                recommended_methods = ["friend_perspective", "cost_benefit_analysis"]
            elif most_common_category == "worry_anxiety":
                recommended_methods = ["catastrophic_thinking", "evidence_examination"]
            else:
                recommended_methods = ["evidence_examination", "alternative_perspectives"]
        
        plan = {
            "patient_id": patient_id,
            "plan_type": "personalized",
            "primary_thought_category": most_common_category,
            "recommended_methods": recommended_methods,
            "current_effectiveness": analysis.get("average_effectiveness_rating", 0),
            "practice_frequency": "daily" if analysis.get("average_effectiveness_rating", 0) < 3 else "as_needed",
            "session_goals": [
                f"Master challenging techniques for {most_common_category.replace('_', ' ')} thoughts",
                "Achieve consistent emotion intensity reduction of 2+ points",
                "Build automatic challenging response to trigger thoughts"
            ],
            "homework_suggestions": self._generate_challenge_homework(most_common_category, recommended_methods)
        }
        
        return plan
    
    def _generate_challenge_homework(self, category: str, methods: List[str]) -> List[str]:
        homework = []
        
        if "evidence_examination" in methods:
            homework.append("Complete daily thought records with evidence for and against columns")
            homework.append("Practice asking 'What evidence do I have?' for each negative thought")
        
        if "friend_perspective" in methods:
            homework.append("When self-critical thoughts arise, ask 'What would I tell a friend?'")
            homework.append("Write compassionate responses to your own negative thoughts")
        
        if "catastrophic_thinking" in methods:
            homework.append("Use worst-best-realistic scenario planning for worry thoughts")
            homework.append("Practice the '5-year rule' - ask how important this will be in 5 years")
        
        category_specific = {
            "self_criticism": [
                "Keep a self-compassion journal with kind responses to mistakes",
                "Practice reframing harsh self-talk into constructive feedback"
            ],
            "worry_anxiety": [
                "Set aside 15 minutes daily for 'worry time' - challenge worries systematically",
                "Practice probability estimates for feared outcomes"
            ],
            "perfectionism": [
                "Experiment with deliberate imperfection in low-stakes situations",
                "Challenge 'should' statements by asking 'according to who?'"
            ]
        }
        
        homework.extend(category_specific.get(category, [
            "Practice identifying and challenging negative thoughts daily",
            "Use balanced thinking worksheets for intense emotional situations"
        ]))
        
        return homework
    
    def generate_challenge_summary(self, patient_id: str, weeks: int = 4) -> Dict[str, Any]:
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=weeks)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) as total,
                       AVG(emotion_intensity_before - emotion_intensity_after) as avg_improvement,
                       AVG(effectiveness_rating) as avg_effectiveness,
                       COUNT(CASE WHEN effectiveness_rating >= 3 THEN 1 END) as successful_challenges
                FROM thought_challenges 
                WHERE patient_id = ? AND created_date >= ? AND completed_date IS NOT NULL
            """, (patient_id, start_date))
            
            overall_stats = cursor.fetchone()
            
            cursor.execute("""
                SELECT thought_category, COUNT(*) as frequency,
                       AVG(emotion_intensity_before - emotion_intensity_after) as avg_improvement
                FROM thought_challenges 
                WHERE patient_id = ? AND created_date >= ? AND completed_date IS NOT NULL
                GROUP BY thought_category
                ORDER BY frequency DESC
            """, (patient_id, start_date))
            
            category_stats = cursor.fetchall()
            
            cursor.execute("""
                SELECT challenge_type, COUNT(*) as uses,
                       AVG(effectiveness_rating) as avg_effectiveness
                FROM thought_challenges 
                WHERE patient_id = ? AND created_date >= ? AND completed_date IS NOT NULL
                GROUP BY challenge_type
                ORDER BY avg_effectiveness DESC
            """, (patient_id, start_date))
            
            method_stats = cursor.fetchall()
        
        if not overall_stats or overall_stats[0] == 0:
            return {"error": "No completed challenges found in the specified period"}
        
        total, avg_improvement, avg_effectiveness, successful = overall_stats
        success_rate = (successful / total * 100) if total > 0 else 0
        
        summary = {
            "analysis_period_weeks": weeks,
            "overall_performance": {
                "total_challenges_completed": total,
                "average_emotion_improvement": round(avg_improvement or 0, 1),
                "average_effectiveness_rating": round(avg_effectiveness or 0, 1),
                "success_rate_percentage": round(success_rate, 1)
            },
            "thought_categories": [
                {
                    "category": cat,
                    "frequency": freq,
                    "average_improvement": round(imp or 0, 1)
                }
                for cat, freq, imp in category_stats
            ],
            "method_effectiveness": [
                {
                    "method": method,
                    "times_used": uses,
                    "average_effectiveness": round(eff or 0, 1)
                }
                for method, uses, eff in method_stats
            ],
            "progress_indicators": self._generate_progress_indicators(
                avg_improvement or 0, avg_effectiveness or 0, success_rate
            )
        }
        
        return summary
    
    def _generate_progress_indicators(self, avg_improvement: float, avg_effectiveness: float, success_rate: float) -> List[str]:
        indicators = []
        
        if avg_improvement >= 2.0:
            indicators.append("Strong emotional regulation through thought challenging")
        elif avg_improvement >= 1.0:
            indicators.append("Moderate improvement in emotional intensity")
        elif avg_improvement < 0.5:
            indicators.append("Limited emotional improvement - may need technique adjustment")
        
        if avg_effectiveness >= 4.0:
            indicators.append("High confidence in thought challenging techniques")
        elif avg_effectiveness >= 3.0:
            indicators.append("Developing proficiency with challenging methods")
        else:
            indicators.append("Building foundational challenging skills")
        
        if success_rate >= 80:
            indicators.append("Consistently effective thought challenging")
        elif success_rate >= 60:
            indicators.append("Generally successful with room for improvement")
        else:
            indicators.append("Inconsistent results - focus on technique refinement")
        
        return indicators
    
    def get_thought_challenging_insights(self, patient_id: str) -> Dict[str, Any]:
        challenges = self.get_patient_challenges(patient_id, limit=20)
        
        if len(challenges) < 3:
            return {
                "insight_type": "insufficient_data",
                "recommendation": "Complete more thought challenges to generate insights"
            }
        
        thought_patterns = {}
        trigger_situations = {}
        effective_techniques = {}
        time_patterns = {}
        
        for challenge in challenges:
            if challenge.completed_date:
                category = challenge.thought_category
                thought_patterns[category] = thought_patterns.get(category, 0) + 1
                
                if challenge.situation_context:
                    context = challenge.situation_context[:50]
                    trigger_situations[context] = trigger_situations.get(context, 0) + 1
                
                if challenge.effectiveness_rating and challenge.effectiveness_rating >= 3:
                    method = challenge.challenge_type.value
                    effective_techniques[method] = effective_techniques.get(method, 0) + 1
                
                hour = challenge.created_date.hour
                time_slot = "morning" if hour < 12 else "afternoon" if hour < 18 else "evening"
                time_patterns[time_slot] = time_patterns.get(time_slot, 0) + 1
        
        most_common_pattern = max(thought_patterns, key=thought_patterns.get) if thought_patterns else "unknown"
        most_effective_technique = max(effective_techniques, key=effective_techniques.get) if effective_techniques else "unknown"
        peak_time = max(time_patterns, key=time_patterns.get) if time_patterns else "unknown"
        
        insights = {
            "dominant_thought_pattern": {
                "category": most_common_pattern,
                "frequency": thought_patterns.get(most_common_pattern, 0),
                "percentage": round(thought_patterns.get(most_common_pattern, 0) / len(challenges) * 100, 1)
            },
            "most_effective_technique": {
                "method": most_effective_technique,
                "success_count": effective_techniques.get(most_effective_technique, 0)
            },
            "peak_challenge_time": {
                "time_period": peak_time,
                "frequency": time_patterns.get(peak_time, 0)
            },
            "common_triggers": [
                {"situation": situation[:40], "frequency": freq}
                for situation, freq in sorted(trigger_situations.items(), key=lambda x: x[1], reverse=True)[:3]
            ],
            "personalized_recommendations": self._generate_personalized_recommendations(
                most_common_pattern, most_effective_technique, peak_time
            )
        }
        
        return insights
    
    def _generate_personalized_recommendations(self, pattern: str, technique: str, peak_time: str) -> List[str]:
        recommendations = []
        
        pattern_recommendations = {
            "self_criticism": [
                "Practice self-compassion techniques daily",
                "Use the friend perspective method more frequently",
                "Challenge perfectionist standards"
            ],
            "worry_anxiety": [
                "Implement regular worry time sessions",
                "Practice worst-case scenario planning",
                "Use grounding techniques before challenging"
            ],
            "perfectionism": [
                "Experiment with intentional imperfection",
                "Challenge should statements daily",
                "Focus on progress over perfection"
            ]
        }
        
        recommendations.extend(pattern_recommendations.get(pattern, [
            "Continue identifying and challenging automatic thoughts",
            "Practice regular thought monitoring"
        ]))
        
        if technique != "unknown":
            technique_name = technique.replace('_', ' ').title()
            recommendations.append(f"Continue using {technique_name} as your primary technique")
        
        time_recommendations = {
            "morning": "Consider morning thought challenging as preventive practice",
            "afternoon": "Use mid-day check-ins to catch negative thoughts early",
            "evening": "Practice evening thought challenging to process the day"
        }
        
        if peak_time in time_recommendations:
            recommendations.append(time_recommendations[peak_time])
        
        return recommendations
    
    def create_challenge_homework_assignment(self, patient_id: str, focus_area: str = None) -> Dict[str, Any]:
        if not focus_area:
            insights = self.get_thought_challenging_insights(patient_id)
            focus_area = insights.get("dominant_thought_pattern", {}).get("category", "general")
        
        homework_templates = {
            "self_criticism": {
                "title": "Self-Compassion Challenge Practice",
                "daily_exercises": [
                    "Notice self-critical thoughts and rate intensity (1-10)",
                    "Ask: 'What would I tell a good friend in this situation?'",
                    "Write a compassionate response to yourself",
                    "Re-rate emotional intensity after challenging"
                ],
                "weekly_goal": "Complete 5 self-compassion challenges",
                "tracking_method": "Self-criticism challenge log"
            },
            
            "worry_anxiety": {
                "title": "Worry Thought Challenging",
                "daily_exercises": [
                    "Identify worry thoughts and write them down",
                    "Ask: 'What's the evidence this will actually happen?'",
                    "Generate 3 alternative outcomes (worst, best, realistic)",
                    "Focus on the realistic outcome and plan coping strategies"
                ],
                "weekly_goal": "Challenge 7 worry thoughts using evidence examination",
                "tracking_method": "Worry challenge worksheet"
            },
            
            "perfectionism": {
                "title": "Perfectionism Reality Check",
                "daily_exercises": [
                    "Notice perfectionist thoughts ('I must', 'I should', 'have to')",
                    "Ask: 'What would be good enough in this situation?'",
                    "Deliberately aim for 'good enough' instead of perfect",
                    "Notice the outcome and your feelings about it"
                ],
                "weekly_goal": "Practice 'good enough' standard 5 times",
                "tracking_method": "Perfectionism challenge journal"
            },
            
            "general": {
                "title": "Daily Thought Challenging Practice",
                "daily_exercises": [
                    "Identify one negative automatic thought",
                    "Rate emotional intensity before challenging (1-10)",
                    "Ask challenging questions appropriate to the thought type",
                    "Develop a more balanced alternative thought",
                    "Re-rate emotional intensity after challenging"
                ],
                "weekly_goal": "Complete 7 thought challenges using various methods",
                "tracking_method": "Daily thought challenge log"
            }
        }
        
        template = homework_templates.get(focus_area, homework_templates["general"])
        
        assignment = {
            "patient_id": patient_id,
            "focus_area": focus_area,
            "title": template["title"],
            "duration": "1 week",
            "daily_exercises": template["daily_exercises"],
            "weekly_goal": template["weekly_goal"],
            "tracking_method": template["tracking_method"],
            "success_criteria": [
                "Complete daily thought challenging exercises",
                "Achieve average 2-point reduction in emotional intensity",
                "Generate balanced alternative thoughts",
                "Use appropriate challenging questions for thought types"
            ],
            "reminder_questions": [
                "What was the situation?",
                "What thought went through my mind?",
                "How did this make me feel?",
                "What questions can I ask to challenge this thought?",
                "What would be a more balanced way to think about this?"
            ]
        }
        
        return assignment
    
    def evaluate_challenge_quality(self, challenge: ThoughtChallenge) -> Dict[str, Any]:
        quality_score = 0
        feedback = []
        strengths = []
        areas_for_improvement = []
        
        if challenge.evidence_for or challenge.evidence_against:
            quality_score += 20
            strengths.append("Good evidence gathering")
        else:
            areas_for_improvement.append("Include more evidence examination")
        
        if len(challenge.alternative_thoughts) >= 2:
            quality_score += 20
            strengths.append("Multiple alternative perspectives generated")
        elif len(challenge.alternative_thoughts) == 1:
            quality_score += 10
            areas_for_improvement.append("Try generating more alternative thoughts")
        else:
            areas_for_improvement.append("Practice creating alternative perspectives")
        
        if challenge.new_balanced_thought and len(challenge.new_balanced_thought) > 20:
            quality_score += 20
            strengths.append("Developed comprehensive balanced thought")
        elif challenge.new_balanced_thought:
            quality_score += 10
            areas_for_improvement.append("Expand on balanced thought development")
        else:
            areas_for_improvement.append("Create a balanced alternative thought")
        
        if challenge.emotion_intensity_before > challenge.emotion_intensity_after:
            improvement = challenge.emotion_intensity_before - challenge.emotion_intensity_after
            if improvement >= 3:
                quality_score += 25
                strengths.append("Significant emotional improvement achieved")
            elif improvement >= 1:
                quality_score += 15
                strengths.append("Moderate emotional improvement")
            else:
                quality_score += 5
                areas_for_improvement.append("Focus on achieving greater emotional relief")
        else:
            areas_for_improvement.append("Work on reducing emotional intensity through challenging")
        
        if challenge.confidence_in_original > challenge.confidence_in_balanced:
            quality_score += 15
            strengths.append("Reduced confidence in original negative thought")
        else:
            areas_for_improvement.append("Work on increasing confidence in balanced alternatives")
        
        quality_level = "excellent" if quality_score >= 80 else "good" if quality_score >= 60 else "developing" if quality_score >= 40 else "needs_work"
        
        evaluation = {
            "quality_score": quality_score,
            "quality_level": quality_level,
            "strengths": strengths,
            "areas_for_improvement": areas_for_improvement,
            "specific_feedback": self._generate_specific_feedback(challenge, quality_score),
            "next_steps": self._suggest_next_steps(challenge, areas_for_improvement)
        }
        
        return evaluation
    
    def _generate_specific_feedback(self, challenge: ThoughtChallenge, score: int) -> List[str]:
        feedback = []
        
        if score >= 80:
            feedback.append("Excellent thought challenging work - you're using techniques effectively")
        elif score >= 60:
            feedback.append("Good progress with thought challenging - continue building these skills")
        else:
            feedback.append("Keep practicing - thought challenging becomes more effective with repetition")
        
        if challenge.challenge_type == ChallengeType.EVIDENCE_EXAMINATION and not challenge.evidence_against:
            feedback.append("Try harder to find evidence that contradicts the negative thought")
        
        if challenge.emotion_intensity_before == challenge.emotion_intensity_after:
            feedback.append("If emotions don't shift, try a different challenging approach or spend more time on the exercise")
        
        return feedback
    
    def _suggest_next_steps(self, challenge: ThoughtChallenge, improvements: List[str]) -> List[str]:
        next_steps = []
        
        if "Include more evidence examination" in improvements:
            next_steps.append("Practice the evidence examination technique with this same thought")
        
        if "Try generating more alternative thoughts" in improvements:
            next_steps.append("Brainstorm 3-5 different ways to interpret this situation")
        
        if "Create a balanced alternative thought" in improvements:
            next_steps.append("Combine your evidence and alternatives into one realistic, balanced statement")
        
        if not next_steps:
            next_steps.append("Continue practicing with new automatic thoughts as they arise")
            next_steps.append("Try using this same technique with similar thoughts")
        
        return next_steps
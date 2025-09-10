from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import sqlite3
import json


class CompletionStatus(Enum):
    NOT_ATTEMPTED = "not_attempted"
    PARTIALLY_COMPLETED = "partially_completed"
    COMPLETED = "completed"
    EXCEEDED_EXPECTATIONS = "exceeded_expectations"
    MODIFIED = "modified"
    UNABLE_TO_COMPLETE = "unable_to_complete"


class HomeworkType(Enum):
    THOUGHT_RECORD = "thought_record"
    BEHAVIORAL_EXPERIMENT = "behavioral_experiment"
    ACTIVITY_SCHEDULING = "activity_scheduling"
    EXPOSURE_EXERCISE = "exposure_exercise"
    MINDFULNESS_PRACTICE = "mindfulness_practice"
    JOURNALING = "journaling"
    SKILL_PRACTICE = "skill_practice"
    READING_ASSIGNMENT = "reading_assignment"
    MONITORING = "monitoring"
    SOCIAL_EXPERIMENT = "social_experiment"


class DifficultyLevel(Enum):
    VERY_EASY = "very_easy"
    EASY = "easy"
    MODERATE = "moderate"
    CHALLENGING = "challenging"
    VERY_DIFFICULT = "very_difficult"


@dataclass
class HomeworkAssignment:
    assignment_id: str
    patient_id: str
    session_id: str
    homework_type: HomeworkType
    title: str
    description: str
    specific_instructions: List[str]
    expected_frequency: str
    due_date: datetime
    difficulty_level: DifficultyLevel
    learning_objectives: List[str]
    materials_needed: List[str] = field(default_factory=list)
    estimated_time: int = 0
    therapist_notes: str = ""
    assigned_date: datetime = field(default_factory=datetime.now)


@dataclass
class HomeworkCompletion:
    assignment_id: str
    patient_id: str
    completion_status: CompletionStatus
    completion_percentage: int
    time_spent: int
    completion_details: str
    challenges_encountered: List[str]
    insights_gained: List[str]
    emotional_reactions: List[str]
    effectiveness_rating: int
    patient_feedback: str
    modifications_made: str = ""
    supporting_evidence: List[str] = field(default_factory=list)
    completion_date: datetime = field(default_factory=datetime.now)


@dataclass
class HomeworkReview:
    assignment_id: str
    session_id: str
    review_date: datetime
    completion_analysis: str
    skill_demonstration: str
    learning_assessment: str
    obstacles_addressed: List[str]
    reinforcement_provided: str
    next_steps: List[str]
    homework_effectiveness: int
    therapist_observations: str


class HomeworkReviewSystem:
    
    def __init__(self, db_path: str = "therapy_system.db"):
        self.db_path = db_path
        self.review_frameworks = self._initialize_review_frameworks()
        self.compliance_strategies = self._initialize_compliance_strategies()
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS homework_assignments (
                    assignment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    homework_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    specific_instructions TEXT,
                    expected_frequency TEXT,
                    due_date TEXT,
                    difficulty_level TEXT,
                    learning_objectives TEXT,
                    materials_needed TEXT,
                    estimated_time INTEGER,
                    therapist_notes TEXT,
                    assigned_date TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS homework_completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assignment_id TEXT,
                    patient_id TEXT,
                    completion_status TEXT,
                    completion_percentage INTEGER,
                    time_spent INTEGER,
                    completion_details TEXT,
                    challenges_encountered TEXT,
                    insights_gained TEXT,
                    emotional_reactions TEXT,
                    effectiveness_rating INTEGER,
                    patient_feedback TEXT,
                    modifications_made TEXT,
                    supporting_evidence TEXT,
                    completion_date TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS homework_reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assignment_id TEXT,
                    session_id TEXT,
                    review_date TEXT,
                    completion_analysis TEXT,
                    skill_demonstration TEXT,
                    learning_assessment TEXT,
                    obstacles_addressed TEXT,
                    reinforcement_provided TEXT,
                    next_steps TEXT,
                    homework_effectiveness INTEGER,
                    therapist_observations TEXT
                )
            """)
    
    def _initialize_review_frameworks(self) -> Dict[str, Dict[str, Any]]:
        
        return {
            "thought_record_review": {
                "completion_check": [
                    "Was situation clearly identified?",
                    "Were automatic thoughts recorded?",
                    "Were emotions and intensity ratings included?",
                    "Was evidence examination completed?",
                    "Were balanced thoughts generated?"
                ],
                "skill_assessment": [
                    "Ability to identify automatic thoughts",
                    "Quality of evidence examination",
                    "Effectiveness of balanced thinking",
                    "Emotional impact of cognitive work"
                ],
                "learning_indicators": [
                    "Increased thought awareness",
                    "Improved cognitive flexibility",
                    "Reduced emotional intensity",
                    "Better mood regulation"
                ]
            },
            
            "behavioral_experiment_review": {
                "completion_check": [
                    "Was experiment carried out as planned?",
                    "Were predictions clearly stated?",
                    "Was actual outcome recorded?",
                    "Were predictions compared to reality?",
                    "Was learning extracted from experience?"
                ],
                "skill_assessment": [
                    "Willingness to test beliefs behaviorally",
                    "Accuracy of prediction vs outcome",
                    "Ability to learn from contradictory evidence",
                    "Integration of new information"
                ],
                "learning_indicators": [
                    "Reduced catastrophic thinking",
                    "Increased behavioral confidence",
                    "Reality-based thinking",
                    "Reduced avoidance behaviors"
                ]
            },
            
            "exposure_exercise_review": {
                "completion_check": [
                    "Was exposure completed as assigned?",
                    "Were anxiety levels tracked throughout?",
                    "Was exposure maintained until anxiety decreased?",
                    "Were safety behaviors minimized?",
                    "Was learning processed afterward?"
                ],
                "skill_assessment": [
                    "Tolerance for anxiety during exposure",
                    "Ability to stay in situation despite discomfort",
                    "Recognition of anxiety's natural decrease",
                    "Confidence building through experience"
                ],
                "learning_indicators": [
                    "Reduced anticipatory anxiety",
                    "Increased confidence in feared situations",
                    "Decreased avoidance behaviors",
                    "Improved functioning in target areas"
                ]
            },
            
            "activity_scheduling_review": {
                "completion_check": [
                    "Were activities scheduled as planned?",
                    "What percentage of activities were completed?",
                    "Were mood ratings recorded?",
                    "Was activity-mood connection observed?",
                    "Were barriers to completion identified?"
                ],
                "skill_assessment": [
                    "Ability to plan and structure activities",
                    "Follow-through on scheduled activities",
                    "Recognition of activity-mood relationship",
                    "Problem-solving around barriers"
                ],
                "learning_indicators": [
                    "Improved mood through activity",
                    "Increased motivation and energy",
                    "Better daily structure",
                    "Enhanced sense of accomplishment"
                ]
            },
            
            "mindfulness_practice_review": {
                "completion_check": [
                    "Was practice completed daily as assigned?",
                    "What was the duration of each practice?",
                    "Were different techniques tried?",
                    "Were insights or observations recorded?",
                    "How was present-moment awareness?"
                ],
                "skill_assessment": [
                    "Ability to maintain attention during practice",
                    "Non-judgmental awareness development",
                    "Recognition of mind wandering",
                    "Integration of mindfulness into daily life"
                ],
                "learning_indicators": [
                    "Increased present-moment awareness",
                    "Reduced reactivity to thoughts/emotions",
                    "Improved emotional regulation",
                    "Greater self-compassion"
                ]
            }
        }
    
    def _initialize_compliance_strategies(self) -> Dict[str, List[str]]:
        
        return {
            "low_compliance": [
                "Explore barriers and obstacles to completion",
                "Simplify homework assignments",
                "Increase collaboration in homework design",
                "Address motivation and engagement",
                "Provide more support and check-ins"
            ],
            
            "partial_compliance": [
                "Acknowledge partial efforts positively",
                "Problem-solve specific obstacles",
                "Adjust difficulty level if needed",
                "Reinforce successful aspects",
                "Modify approach based on learning style"
            ],
            
            "good_compliance": [
                "Reinforce consistent effort",
                "Explore insights and learning",
                "Gradually increase complexity",
                "Use successes to build confidence",
                "Maintain optimal challenge level"
            ],
            
            "resistance_patterns": [
                "Explore meaning of homework resistance",
                "Address underlying fears or concerns",
                "Increase patient choice and autonomy",
                "Connect homework to patient goals",
                "Work through therapeutic relationship issues"
            ]
        }
    
    def conduct_homework_review(self, assignment_id: str, session_id: str, 
                              completion_data: Dict[str, Any]) -> HomeworkReview:
        
        assignment = self._get_homework_assignment(assignment_id)
        if not assignment:
            raise ValueError(f"Assignment {assignment_id} not found")
        
        completion = HomeworkCompletion(
            assignment_id=assignment_id,
            patient_id=assignment.patient_id,
            completion_status=CompletionStatus(completion_data.get("status", "not_attempted")),
            completion_percentage=completion_data.get("percentage", 0),
            time_spent=completion_data.get("time_spent", 0),
            completion_details=completion_data.get("details", ""),
            challenges_encountered=completion_data.get("challenges", []),
            insights_gained=completion_data.get("insights", []),
            emotional_reactions=completion_data.get("emotions", []),
            effectiveness_rating=completion_data.get("effectiveness", 0),
            patient_feedback=completion_data.get("feedback", ""),
            modifications_made=completion_data.get("modifications", ""),
            supporting_evidence=completion_data.get("evidence", [])
        )
        
        self._save_homework_completion(completion)
        
        review_framework = self.review_frameworks.get(
            f"{assignment.homework_type.value}_review",
            self.review_frameworks["thought_record_review"]
        )
        
        completion_analysis = self._analyze_completion(completion, review_framework)
        skill_demonstration = self._assess_skill_demonstration(completion, review_framework)
        learning_assessment = self._evaluate_learning(completion, review_framework)
        obstacles_addressed = self._identify_obstacles(completion)
        reinforcement = self._provide_reinforcement(completion)
        next_steps = self._determine_next_steps(completion, assignment)
        
        review = HomeworkReview(
            assignment_id=assignment_id,
            session_id=session_id,
            review_date=datetime.now(),
            completion_analysis=completion_analysis,
            skill_demonstration=skill_demonstration,
            learning_assessment=learning_assessment,
            obstacles_addressed=obstacles_addressed,
            reinforcement_provided=reinforcement,
            next_steps=next_steps,
            homework_effectiveness=completion.effectiveness_rating,
            therapist_observations=""
        )
        
        self._save_homework_review(review)
        return review
    
    def _analyze_completion(self, completion: HomeworkCompletion, 
                          framework: Dict[str, Any]) -> str:
        
        analysis_parts = []
        
        status_analysis = {
            CompletionStatus.NOT_ATTEMPTED: "Patient did not attempt the homework assignment.",
            CompletionStatus.PARTIALLY_COMPLETED: f"Patient completed {completion.completion_percentage}% of the assignment.",
            CompletionStatus.COMPLETED: "Patient successfully completed the homework assignment.",
            CompletionStatus.EXCEEDED_EXPECTATIONS: "Patient went above and beyond the assignment requirements.",
            CompletionStatus.MODIFIED: "Patient modified the assignment but demonstrated engagement.",
            CompletionStatus.UNABLE_TO_COMPLETE: "Patient was unable to complete due to circumstances."
        }
        
        analysis_parts.append(status_analysis[completion.completion_status])
        
        if completion.time_spent > 0:
            analysis_parts.append(f"Time invested: {completion.time_spent} minutes.")
        
        if completion.challenges_encountered:
            challenges_summary = ", ".join(completion.challenges_encountered[:3])
            analysis_parts.append(f"Main challenges: {challenges_summary}.")
        
        if completion.effectiveness_rating > 0:
            effectiveness_desc = {
                1: "minimally effective",
                2: "somewhat effective", 
                3: "moderately effective",
                4: "quite effective",
                5: "very effective"
            }
            rating_desc = effectiveness_desc.get(completion.effectiveness_rating, "unrated")
            analysis_parts.append(f"Patient rated homework as {rating_desc}.")
        
        return " ".join(analysis_parts)
    
    def _assess_skill_demonstration(self, completion: HomeworkCompletion, 
                                  framework: Dict[str, Any]) -> str:
        
        skill_indicators = framework.get("skill_assessment", [])
        demonstrated_skills = []
        
        if completion.completion_status in [CompletionStatus.COMPLETED, CompletionStatus.EXCEEDED_EXPECTATIONS]:
            if completion.insights_gained:
                demonstrated_skills.append("Ability to extract learning from experience")
            
            if completion.completion_details and len(completion.completion_details) > 50:
                demonstrated_skills.append("Detailed self-observation and reporting")
            
            if completion.effectiveness_rating >= 3:
                demonstrated_skills.append("Recognition of homework value and impact")
            
            if completion.modifications_made:
                demonstrated_skills.append("Adaptive problem-solving and flexibility")
        
        if not demonstrated_skills:
            return "Limited skill demonstration in this homework completion."
        
        return f"Demonstrated skills: {', '.join(demonstrated_skills)}."
    
    def _evaluate_learning(self, completion: HomeworkCompletion, 
                          framework: Dict[str, Any]) -> str:
        
        learning_indicators = framework.get("learning_indicators", [])
        observed_learning = []
        
        if completion.insights_gained:
            for insight in completion.insights_gained:
                if any(indicator.lower() in insight.lower() for indicator in learning_indicators):
                    observed_learning.append(insight)
        
        if completion.emotional_reactions:
            positive_emotions = ["relief", "confidence", "hope", "proud", "accomplished"]
            if any(emotion.lower() in " ".join(completion.emotional_reactions).lower() 
                   for emotion in positive_emotions):
                observed_learning.append("Positive emotional response to skill use")
        
        if completion.effectiveness_rating >= 4:
            observed_learning.append("High perceived effectiveness suggests meaningful learning")
        
        if not observed_learning:
            return "Learning outcomes require further exploration and development."
        
        return f"Learning achieved: {'; '.join(observed_learning)}."
    
    def _identify_obstacles(self, completion: HomeworkCompletion) -> List[str]:
        
        obstacles = list(completion.challenges_encountered)
        
        if completion.completion_status == CompletionStatus.NOT_ATTEMPTED:
            obstacles.extend(["Lack of initial engagement", "Possible avoidance or resistance"])
        
        elif completion.completion_percentage < 50:
            obstacles.extend(["Incomplete follow-through", "Possible overwhelming difficulty"])
        
        if completion.time_spent == 0 and completion.completion_status != CompletionStatus.NOT_ATTEMPTED:
            obstacles.append("Time management or scheduling difficulties")
        
        return obstacles[:5]
    
    def _provide_reinforcement(self, completion: HomeworkCompletion) -> str:
        
        reinforcement_messages = []
        
        if completion.completion_status == CompletionStatus.EXCEEDED_EXPECTATIONS:
            reinforcement_messages.append("Excellent work exceeding expectations")
        
        elif completion.completion_status == CompletionStatus.COMPLETED:
            reinforcement_messages.append("Great job completing the assignment")
        
        elif completion.completion_status == CompletionStatus.PARTIALLY_COMPLETED:
            reinforcement_messages.append("Good effort in partially completing the homework")
        
        elif completion.completion_status == CompletionStatus.MODIFIED:
            reinforcement_messages.append("Creative adaptation showing engagement and problem-solving")
        
        if completion.insights_gained:
            reinforcement_messages.append("Valuable insights gained from the experience")
        
        if completion.effectiveness_rating >= 3:
            reinforcement_messages.append("Recognition of homework value is encouraging")
        
        if completion.challenges_encountered and completion.completion_percentage > 0:
            reinforcement_messages.append("Persistence despite challenges is commendable")
        
        return ". ".join(reinforcement_messages) + "." if reinforcement_messages else "Effort acknowledged."
    
    def _determine_next_steps(self, completion: HomeworkCompletion, 
                            assignment: HomeworkAssignment) -> List[str]:
        
        next_steps = []
        
        if completion.completion_status == CompletionStatus.NOT_ATTEMPTED:
            next_steps.extend([
                "Explore barriers to homework engagement",
                "Simplify or modify assignment approach",
                "Increase collaborative homework planning"
            ])
        
        elif completion.completion_status == CompletionStatus.PARTIALLY_COMPLETED:
            next_steps.extend([
                "Problem-solve specific completion obstacles",
                "Adjust assignment difficulty if needed",
                "Reinforce partial success and build on it"
            ])
        
        elif completion.completion_status in [CompletionStatus.COMPLETED, CompletionStatus.EXCEEDED_EXPECTATIONS]:
            next_steps.extend([
                "Build on successful homework completion",
                "Gradually increase assignment complexity",
                "Apply learning to new situations"
            ])
        
        if completion.challenges_encountered:
            next_steps.append("Address identified challenges in future assignments")
        
        if completion.effectiveness_rating <= 2:
            next_steps.append("Modify homework approach to increase perceived value")
        
        if completion.insights_gained:
            next_steps.append("Integrate insights into broader therapeutic work")
        
        return next_steps[:4]
    
    def analyze_homework_patterns(self, patient_id: str, weeks: int = 4) -> Dict[str, Any]:
        
        start_date = datetime.now() - timedelta(weeks=weeks)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT ha.homework_type, hc.completion_status, hc.completion_percentage,
                       hc.effectiveness_rating, hc.challenges_encountered
                FROM homework_assignments ha
                LEFT JOIN homework_completions hc ON ha.assignment_id = hc.assignment_id
                WHERE ha.patient_id = ? AND ha.assigned_date >= ?
                ORDER BY ha.assigned_date DESC
            """, (patient_id, start_date.isoformat()))
            
            results = cursor.fetchall()
        
        if not results:
            return {"error": "No homework data found for specified period"}
        
        analysis = {
            "total_assignments": len(results),
            "completion_rates": {},
            "homework_types": {},
            "effectiveness_ratings": [],
            "common_challenges": {},
            "trends": {}
        }
        
        completed_count = 0
        partially_completed_count = 0
        not_attempted_count = 0
        
        for hw_type, status, percentage, effectiveness, challenges_json in results:
            if status == "completed" or status == "exceeded_expectations":
                completed_count += 1
            elif status == "partially_completed":
                partially_completed_count += 1
            elif status == "not_attempted":
                not_attempted_count += 1
            
            if hw_type not in analysis["homework_types"]:
                analysis["homework_types"][hw_type] = {"count": 0, "avg_completion": 0}
            
            analysis["homework_types"][hw_type]["count"] += 1
            analysis["homework_types"][hw_type]["avg_completion"] += (percentage or 0)
            
            if effectiveness:
                analysis["effectiveness_ratings"].append(effectiveness)
            
            if challenges_json:
                challenges = json.loads(challenges_json)
                for challenge in challenges:
                    analysis["common_challenges"][challenge] = analysis["common_challenges"].get(challenge, 0) + 1
        
        analysis["completion_rates"] = {
            "completed": round(completed_count / len(results) * 100, 1),
            "partially_completed": round(partially_completed_count / len(results) * 100, 1),
            "not_attempted": round(not_attempted_count / len(results) * 100, 1)
        }
        
        for hw_type in analysis["homework_types"]:
            if analysis["homework_types"][hw_type]["count"] > 0:
                analysis["homework_types"][hw_type]["avg_completion"] = round(
                    analysis["homework_types"][hw_type]["avg_completion"] / 
                    analysis["homework_types"][hw_type]["count"], 1
                )
        
        if analysis["effectiveness_ratings"]:
            analysis["avg_effectiveness"] = round(
                sum(analysis["effectiveness_ratings"]) / len(analysis["effectiveness_ratings"]), 1
            )
        
        return analysis
    
    def generate_compliance_recommendations(self, patient_id: str) -> List[str]:
        
        patterns = self.analyze_homework_patterns(patient_id)
        
        if "error" in patterns:
            return ["Establish baseline homework compliance data"]
        
        recommendations = []
        completion_rate = patterns["completion_rates"]["completed"]
        
        if completion_rate < 30:
            recommendations.extend(self.compliance_strategies["low_compliance"])
        elif completion_rate < 70:
            recommendations.extend(self.compliance_strategies["partial_compliance"])
        else:
            recommendations.extend(self.compliance_strategies["good_compliance"])
        
        if patterns["common_challenges"]:
            top_challenge = max(patterns["common_challenges"].items(), key=lambda x: x[1])[0]
            recommendations.append(f"Address recurring challenge: {top_challenge}")
        
        if patterns.get("avg_effectiveness", 0) < 3:
            recommendations.append("Increase homework relevance and perceived value")
        
        return recommendations[:5]
    
    def create_homework_summary(self, session_id: str) -> Dict[str, Any]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT hr.assignment_id, ha.title, ha.homework_type, 
                       hr.completion_analysis, hr.homework_effectiveness,
                       hr.reinforcement_provided, hr.next_steps
                FROM homework_reviews hr
                JOIN homework_assignments ha ON hr.assignment_id = ha.assignment_id
                WHERE hr.session_id = ?
                ORDER BY hr.review_date
            """, (session_id,))
            
            reviews = cursor.fetchall()
        
        summary = {
            "session_id": session_id,
            "total_assignments_reviewed": len(reviews),
            "homework_details": [],
            "overall_compliance": "unknown",
            "key_insights": [],
            "recommended_actions": []
        }
        
        if not reviews:
            summary["overall_compliance"] = "no_homework_reviewed"
            return summary
        
        effectiveness_scores = []
        compliance_indicators = []
        
        for assignment_id, title, hw_type, analysis, effectiveness, reinforcement, next_steps in reviews:
            homework_detail = {
                "title": title,
                "type": hw_type,
                "analysis": analysis,
                "effectiveness": effectiveness,
                "reinforcement": reinforcement,
                "next_steps": json.loads(next_steps) if next_steps else []
            }
            
            summary["homework_details"].append(homework_detail)
            
            if effectiveness:
                effectiveness_scores.append(effectiveness)
            
            if "completed" in analysis.lower():
                compliance_indicators.append("high")
            elif "partially" in analysis.lower():
                compliance_indicators.append("medium")
            else:
                compliance_indicators.append("low")
        
        if compliance_indicators:
            high_compliance = compliance_indicators.count("high")
            medium_compliance = compliance_indicators.count("medium")
            
            if high_compliance >= len(compliance_indicators) * 0.7:
                summary["overall_compliance"] = "good"
            elif high_compliance + medium_compliance >= len(compliance_indicators) * 0.5:
                summary["overall_compliance"] = "fair"
            else:
                summary["overall_compliance"] = "poor"
        
        if effectiveness_scores:
            avg_effectiveness = sum(effectiveness_scores) / len(effectiveness_scores)
            if avg_effectiveness >= 4:
                summary["key_insights"].append("Homework perceived as highly effective")
            elif avg_effectiveness >= 3:
                summary["key_insights"].append("Homework moderately effective")
            else:
                summary["key_insights"].append("Homework effectiveness needs improvement")
        
        return summary
    
    def _get_homework_assignment(self, assignment_id: str) -> Optional[HomeworkAssignment]:
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT assignment_id, patient_id, session_id, homework_type, title,
                       description, specific_instructions, expected_frequency, due_date,
                       difficulty_level, learning_objectives, materials_needed,
                       estimated_time, therapist_notes, assigned_date
                FROM homework_assignments
                WHERE assignment_id = ?
            """, (assignment_id,))
            
            result = cursor.fetchone()
        
        if not result:
            return None
        
        return HomeworkAssignment(
            assignment_id=result[0],
            patient_id=result[1],
            session_id=result[2],
            homework_type=HomeworkType(result[3]),
            title=result[4],
            description=result[5],
            specific_instructions=json.loads(result[6]) if result[6] else [],
            expected_frequency=result[7],
            due_date=datetime.fromisoformat(result[8]) if result[8] else datetime.now(),
            difficulty_level=DifficultyLevel(result[9]),
            learning_objectives=json.loads(result[10]) if result[10] else [],
            materials_needed=json.loads(result[11]) if result[11] else [],
            estimated_time=result[12],
            therapist_notes=result[13],
            assigned_date=datetime.fromisoformat(result[14])
        )
    
    def _save_homework_completion(self, completion: HomeworkCompletion):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO homework_completions
                (assignment_id, patient_id, completion_status, completion_percentage,
                 time_spent, completion_details, challenges_encountered, insights_gained,
                 emotional_reactions, effectiveness_rating, patient_feedback,
                 modifications_made, supporting_evidence, completion_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                completion.assignment_id, completion.patient_id, completion.completion_status.value,
                completion.completion_percentage, completion.time_spent, completion.completion_details,
                json.dumps(completion.challenges_encountered), json.dumps(completion.insights_gained),
                json.dumps(completion.emotional_reactions), completion.effectiveness_rating,
                completion.patient_feedback, completion.modifications_made,
                json.dumps(completion.supporting_evidence), completion.completion_date.isoformat()
            ))
    
    def _save_homework_review(self, review: HomeworkReview):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO homework_reviews
                (assignment_id, session_id, review_date, completion_analysis,
                 skill_demonstration, learning_assessment, obstacles_addressed,
                 reinforcement_provided, next_steps, homework_effectiveness,
                 therapist_observations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                review.assignment_id, review.session_id, review.review_date.isoformat(),
                review.completion_analysis, review.skill_demonstration, review.learning_assessment,
                json.dumps(review.obstacles_addressed), review.reinforcement_provided,
                json.dumps(review.next_steps), review.homework_effectiveness,
                review.therapist_observations
            ))


if __name__ == "__main__":
    homework_reviewer = HomeworkReviewSystem()
    
    completion_data = {
        "status": "completed",
        "percentage": 85,
        "time_spent": 45,
        "details": "Completed 6 out of 7 thought records. Found the exercise helpful for noticing patterns.",
        "challenges": ["Hard to remember to do it", "Emotional intensity made it difficult"],
        "insights": ["I notice I catastrophize about work situations", "My mood improves when I challenge thoughts"],
        "emotions": ["Initially frustrated", "Then relieved", "More confident"],
        "effectiveness": 4,
        "feedback": "This really helped me see my thinking patterns more clearly"
    }
    
    print("=== HOMEWORK COMPLETION DATA ===")
    for key, value in completion_data.items():
        print(f"{key}: {value}")
    
    patterns = homework_reviewer.analyze_homework_patterns("patient_123")
    print("\n=== HOMEWORK PATTERNS ANALYSIS ===")
    if "error" not in patterns:
        print(f"Total assignments: {patterns['total_assignments']}")
        print(f"Completion rates: {patterns['completion_rates']}")
        print(f"Average effectiveness: {patterns.get('avg_effectiveness', 'N/A')}")
    else:
        print(patterns["error"])
    
    recommendations = homework_reviewer.generate_compliance_recommendations("patient_123")
    print(f"\n=== COMPLIANCE RECOMMENDATIONS ===")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")
"""
Individual Learning Profile System
Comprehensive assessment for neurodivergent-friendly personalized education
"""

from pydantic import BaseModel
from typing import Dict, List, Optional
from enum import Enum

class LearningStyle(str, Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"
    MULTIMODAL = "multimodal"

class CommunicationStyle(str, Enum):
    DIRECT = "direct"
    SUPPORTIVE = "supportive"
    STRUCTURED = "structured"
    CREATIVE = "creative"
    TECHNICAL = "technical"

class ProcessingSpeed(str, Enum):
    SLOW_DELIBERATE = "slow_deliberate"
    MODERATE = "moderate"
    FAST = "fast"
    VARIABLE = "variable"

class AttentionProfile(str, Enum):
    SUSTAINED_FOCUS = "sustained_focus"
    SHORT_BURSTS = "short_bursts"
    HYPERFOCUS_PRONE = "hyperfocus_prone"
    EASILY_DISTRACTED = "easily_distracted"

class MotivationStyle(str, Enum):
    INTRINSIC = "intrinsic"
    ACHIEVEMENT = "achievement"
    SOCIAL = "social"
    CHALLENGE = "challenge"
    STRUCTURE = "structure"

class LearningProfile(BaseModel):
    """Comprehensive learning profile for individualized education"""
    
    # Basic Demographics
    user_id: str
    age: int
    name: str
    
    # Cognitive Profile
    learning_style_primary: LearningStyle
    learning_style_secondary: Optional[LearningStyle] = None
    communication_preference: CommunicationStyle
    processing_speed: ProcessingSpeed
    attention_profile: AttentionProfile
    motivation_style: MotivationStyle
    
    # Neurodivergent Factors
    has_adhd: bool = False
    has_autism: bool = False
    has_dyslexia: bool = False
    has_anxiety: bool = False
    other_conditions: List[str] = []
    
    # Personality (MBTI-style)
    mbti_type: Optional[str] = None
    introversion_score: int = 50  # 0-100 scale
    thinking_feeling_score: int = 50  # 0=thinking, 100=feeling
    judging_perceiving_score: int = 50  # 0=judging, 100=perceiving
    
    # Intelligence Profile
    verbal_iq_estimate: Optional[int] = None
    performance_iq_estimate: Optional[int] = None
    processing_speed_iq: Optional[int] = None
    working_memory_score: Optional[int] = None
    
    # Learning Preferences
    prefers_structure: bool = True
    needs_frequent_breaks: bool = False
    responds_to_gamification: bool = False
    prefers_collaborative: bool = False
    needs_emotional_support: bool = False
    
    # Sensory Preferences
    sensitive_to_noise: bool = False
    sensitive_to_light: bool = False
    prefers_minimal_visual_clutter: bool = False
    needs_fidget_tools: bool = False
    
    # Subject Interests & Strengths
    strong_subjects: List[str] = []
    challenging_subjects: List[str] = []
    interest_areas: List[str] = []
    
    # Goals & Aspirations
    short_term_goals: List[str] = []
    long_term_goals: List[str] = []
    career_interests: List[str] = []

class LearningPathGenerator:
    """Generates personalized learning paths based on individual profiles"""
    
    @staticmethod
    def generate_teaching_strategy(profile: LearningProfile) -> Dict:
        """Generate teaching strategy based on profile"""
        
        strategy = {
            "communication_style": profile.communication_preference,
            "lesson_structure": {},
            "content_delivery": {},
            "assessment_methods": {},
            "support_mechanisms": {}
        }
        
        # Lesson Structure
        if profile.attention_profile == AttentionProfile.SHORT_BURSTS:
            strategy["lesson_structure"] = {
                "duration": "10-15 minutes",
                "breaks": "every 10 minutes",
                "activities_per_session": 2
            }
        elif profile.attention_profile == AttentionProfile.HYPERFOCUS_PRONE:
            strategy["lesson_structure"] = {
                "duration": "flexible 20-60 minutes",
                "breaks": "self-directed",
                "depth_over_breadth": True
            }
        
        # Content Delivery
        if profile.learning_style_primary == LearningStyle.VISUAL:
            strategy["content_delivery"] = {
                "visual_aids": "diagrams, flowcharts, mind maps",
                "code_visualization": "syntax highlighting, visual debuggers",
                "minimal_text": True
            }
        elif profile.learning_style_primary == LearningStyle.KINESTHETIC:
            strategy["content_delivery"] = {
                "hands_on": "immediate coding practice",
                "interactive_examples": True,
                "physical_metaphors": True
            }
        
        # Neurodivergent Adaptations
        if profile.has_adhd:
            strategy["support_mechanisms"]["adhd"] = {
                "clear_objectives": True,
                "progress_tracking": "visual progress bars",
                "variety": "multiple activity types",
                "movement_breaks": True
            }
        
        if profile.has_autism:
            strategy["support_mechanisms"]["autism"] = {
                "predictable_structure": True,
                "clear_expectations": True,
                "reduced_social_pressure": True,
                "special_interests_integration": profile.interest_areas
            }
        
        # Emotional Support
        if profile.needs_emotional_support or profile.has_anxiety:
            strategy["support_mechanisms"]["emotional"] = {
                "frequent_encouragement": True,
                "low_pressure_environment": True,
                "emotion_check_ins": True,
                "celebrating_small_wins": True
            }
        
        return strategy

    @staticmethod
    def adapt_frontend_curriculum(profile: LearningProfile) -> List[Dict]:
        """Create adapted frontend development curriculum"""
        
        base_curriculum = [
            {"topic": "HTML Basics", "weeks": 2},
            {"topic": "CSS Fundamentals", "weeks": 3},
            {"topic": "JavaScript Intro", "weeks": 4},
            {"topic": "DOM Manipulation", "weeks": 2},
            {"topic": "React Basics", "weeks": 4},
            {"topic": "State Management", "weeks": 3},
            {"topic": "API Integration", "weeks": 2},
            {"topic": "Project Building", "weeks": 4}
        ]
        
        # Adapt based on processing speed
        if profile.processing_speed == ProcessingSpeed.SLOW_DELIBERATE:
            for module in base_curriculum:
                module["weeks"] = int(module["weeks"] * 1.5)
                module["extra_practice"] = True
        
        # Add interest-based projects
        if "gaming" in profile.interest_areas:
            base_curriculum.append({
                "topic": "Game Development with JS",
                "weeks": 3,
                "special_interest": True
            })
        
        if "art" in profile.interest_areas:
            base_curriculum.append({
                "topic": "CSS Animations & Visual Effects",
                "weeks": 2,
                "special_interest": True
            })
        
        return base_curriculum

# Survey Questions for Profile Creation
ASSESSMENT_QUESTIONS = {
    "learning_style": [
        "When learning something new, I prefer to: a) See diagrams/pictures b) Hear explanations c) Try it hands-on d) Read about it",
        "I remember information best when: a) I can visualize it b) I hear it repeated c) I practice it d) I write it down",
        "When following directions, I prefer: a) Maps/visual guides b) Spoken instructions c) Walking through it d) Written steps"
    ],
    
    "neurodivergent_screening": [
        "Do you have difficulty maintaining attention during lengthy tasks?",
        "Do you prefer detailed routines and predictable schedules?",
        "Do you have sensitivity to sounds, lights, or textures?",
        "Do you sometimes get intensely focused on specific topics?",
        "Do you find social interactions draining or confusing?"
    ],
    
    "cognitive_strengths": [
        "Rate your comfort with: logical reasoning (1-10)",
        "Rate your comfort with: creative thinking (1-10)",
        "Rate your comfort with: remembering details (1-10)",
        "Rate your comfort with: seeing big picture patterns (1-10)"
    ],
    
    "motivation_preferences": [
        "I'm most motivated when: a) I set my own goals b) I compete with others c) I help others d) I master something difficult",
        "I prefer feedback that is: a) Immediate b) Detailed c) Encouraging d) Direct and honest",
        "I work best: a) Alone b) In small groups c) With a mentor d) In structured classes"
    ]
}
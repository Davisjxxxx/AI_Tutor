#!/usr/bin/env python3
"""
Advanced Personalization Engine
AI-powered audience segmentation and personalized content generation
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import uuid
import numpy as np
from collections import defaultdict

from ai.next_gen_providers import ai_orchestrator, AIRequest, ContentType

logger = logging.getLogger(__name__)


class PersonalityType(Enum):
    """Audience personality types based on psychological profiling"""
    ACHIEVER = "achiever"  # Goal-oriented, success-driven
    EXPLORER = "explorer"  # Curious, adventure-seeking
    SOCIALIZER = "socializer"  # Community-focused, relationship-driven
    KILLER = "killer"  # Competitive, dominance-seeking
    CREATOR = "creator"  # Artistic, innovation-focused
    CAREGIVER = "caregiver"  # Nurturing, helping others
    REBEL = "rebel"  # Anti-establishment, freedom-seeking
    SAGE = "sage"  # Knowledge-seeking, wisdom-focused


class ContentPersonality(Enum):
    """Content personality styles"""
    AUTHORITATIVE = "authoritative"
    FRIENDLY = "friendly"
    HUMOROUS = "humorous"
    INSPIRATIONAL = "inspirational"
    EDUCATIONAL = "educational"
    CONTROVERSIAL = "controversial"
    EMPATHETIC = "empathetic"
    TRENDY = "trendy"


class EngagementPattern(Enum):
    """User engagement patterns"""
    BINGE_CONSUMER = "binge_consumer"  # Consumes lots of content at once
    CASUAL_BROWSER = "casual_browser"  # Light, occasional engagement
    ACTIVE_COMMENTER = "active_commenter"  # High interaction, comments frequently
    SILENT_LURKER = "silent_lurker"  # Views but rarely interacts
    TREND_FOLLOWER = "trend_follower"  # Engages with trending content
    NICHE_ENTHUSIAST = "niche_enthusiast"  # Deep engagement in specific topics


@dataclass
class UserProfile:
    """Comprehensive user profile for personalization"""
    user_id: str
    personality_type: PersonalityType
    engagement_pattern: EngagementPattern
    preferred_content_personality: ContentPersonality
    
    # Demographic data
    age_range: str
    location: str
    timezone: str
    language: str
    
    # Behavioral data
    active_hours: List[int]  # Hours of day when most active
    preferred_platforms: List[str]
    content_preferences: Dict[str, float]  # Topic -> preference score
    engagement_history: Dict[str, Any]
    
    # Psychographic data
    values: List[str]
    interests: List[str]
    pain_points: List[str]
    aspirations: List[str]
    
    # Interaction patterns
    average_session_duration: float
    content_completion_rate: float
    sharing_propensity: float
    comment_sentiment: float  # -1 to 1
    
    # Personalization metadata
    last_updated: datetime
    confidence_score: float  # How confident we are in this profile


@dataclass
class PersonalizedContent:
    """Personalized content recommendation"""
    content_id: str
    user_id: str
    content_type: str
    title: str
    description: str
    script: str
    
    # Personalization data
    personalization_score: float
    personality_match: float
    engagement_prediction: float
    conversion_probability: float
    
    # Content metadata
    optimal_posting_time: datetime
    recommended_platform: str
    personalized_hashtags: List[str]
    call_to_action: str
    
    # A/B testing variants
    variants: List[Dict[str, Any]]
    
    # Performance tracking
    generated_timestamp: datetime
    expires_at: datetime


class PsychographicAnalyzer:
    """Analyzes user psychology for personalization"""
    
    def __init__(self):
        self.personality_indicators = self._load_personality_indicators()
        self.behavioral_patterns = self._load_behavioral_patterns()
    
    def _load_personality_indicators(self) -> Dict[PersonalityType, Dict[str, Any]]:
        """Load personality type indicators"""
        return {
            PersonalityType.ACHIEVER: {
                "keywords": ["success", "goal", "achievement", "win", "progress", "growth"],
                "content_preferences": ["business", "productivity", "self-improvement"],
                "engagement_triggers": ["results", "metrics", "before-after", "testimonials"],
                "optimal_cta": ["Get Results Now", "Achieve Your Goals", "Start Winning"]
            },
            PersonalityType.EXPLORER: {
                "keywords": ["adventure", "discover", "explore", "new", "travel", "experience"],
                "content_preferences": ["travel", "technology", "culture", "innovation"],
                "engagement_triggers": ["curiosity", "mystery", "behind-scenes", "exclusive"],
                "optimal_cta": ["Discover More", "Explore Now", "Uncover Secrets"]
            },
            PersonalityType.SOCIALIZER: {
                "keywords": ["community", "friends", "share", "together", "connect", "social"],
                "content_preferences": ["lifestyle", "relationships", "community", "events"],
                "engagement_triggers": ["social-proof", "community", "sharing", "collaboration"],
                "optimal_cta": ["Join the Community", "Share with Friends", "Connect Now"]
            },
            PersonalityType.CREATOR: {
                "keywords": ["create", "build", "make", "design", "art", "innovation"],
                "content_preferences": ["art", "design", "technology", "DIY", "tutorials"],
                "engagement_triggers": ["creativity", "inspiration", "tutorials", "tools"],
                "optimal_cta": ["Start Creating", "Build Something Amazing", "Get Inspired"]
            },
            PersonalityType.SAGE: {
                "keywords": ["learn", "knowledge", "wisdom", "understand", "research", "study"],
                "content_preferences": ["education", "science", "philosophy", "analysis"],
                "engagement_triggers": ["insights", "research", "data", "expert-opinion"],
                "optimal_cta": ["Learn More", "Gain Insights", "Discover Truth"]
            }
        }
    
    def _load_behavioral_patterns(self) -> Dict[EngagementPattern, Dict[str, Any]]:
        """Load behavioral pattern indicators"""
        return {
            EngagementPattern.BINGE_CONSUMER: {
                "session_duration": "> 30 minutes",
                "content_per_session": "> 10 pieces",
                "return_frequency": "daily",
                "optimal_content_length": "long-form",
                "best_posting_times": [19, 20, 21, 22]  # Evening hours
            },
            EngagementPattern.CASUAL_BROWSER: {
                "session_duration": "< 10 minutes",
                "content_per_session": "< 5 pieces",
                "return_frequency": "weekly",
                "optimal_content_length": "short-form",
                "best_posting_times": [12, 13, 17, 18]  # Lunch and commute
            },
            EngagementPattern.ACTIVE_COMMENTER: {
                "comment_frequency": "high",
                "engagement_rate": "> 8%",
                "social_sharing": "frequent",
                "optimal_content_type": "discussion-starter",
                "best_posting_times": [9, 12, 15, 18]  # Business hours
            },
            EngagementPattern.TREND_FOLLOWER: {
                "trending_content_engagement": "high",
                "hashtag_usage": "frequent",
                "viral_content_sharing": "high",
                "optimal_content_type": "trending",
                "best_posting_times": [16, 17, 18, 19]  # Peak social hours
            }
        }
    
    async def analyze_user_personality(self, user_data: Dict[str, Any]) -> PersonalityType:
        """Analyze user personality type from behavioral data"""
        
        # Extract behavioral indicators
        content_interactions = user_data.get("content_interactions", [])
        comments = user_data.get("comments", [])
        search_history = user_data.get("search_history", [])
        
        # Score each personality type
        personality_scores = {}
        
        for personality_type, indicators in self.personality_indicators.items():
            score = 0.0
            
            # Analyze content preferences
            for content in content_interactions:
                content_category = content.get("category", "")
                if content_category in indicators["content_preferences"]:
                    score += content.get("engagement_score", 0) * 0.3
            
            # Analyze language patterns in comments
            comment_text = " ".join([c.get("text", "") for c in comments]).lower()
            for keyword in indicators["keywords"]:
                score += comment_text.count(keyword) * 0.2
            
            # Analyze search patterns
            for search in search_history:
                search_text = search.get("query", "").lower()
                for keyword in indicators["keywords"]:
                    if keyword in search_text:
                        score += 0.1
            
            personality_scores[personality_type] = score
        
        # Return personality type with highest score
        if personality_scores:
            return max(personality_scores, key=personality_scores.get)
        
        return PersonalityType.ACHIEVER  # Default
    
    async def analyze_engagement_pattern(self, user_data: Dict[str, Any]) -> EngagementPattern:
        """Analyze user engagement pattern"""
        
        session_data = user_data.get("session_data", [])
        if not session_data:
            return EngagementPattern.CASUAL_BROWSER
        
        # Calculate metrics
        avg_session_duration = np.mean([s.get("duration", 0) for s in session_data])
        avg_content_per_session = np.mean([s.get("content_viewed", 0) for s in session_data])
        comment_frequency = len(user_data.get("comments", []))
        sharing_frequency = len(user_data.get("shares", []))
        
        # Determine pattern based on metrics
        if avg_session_duration > 1800:  # 30 minutes
            return EngagementPattern.BINGE_CONSUMER
        elif comment_frequency > 10:
            return EngagementPattern.ACTIVE_COMMENTER
        elif sharing_frequency > 5:
            return EngagementPattern.TREND_FOLLOWER
        elif avg_session_duration < 300:  # 5 minutes
            return EngagementPattern.CASUAL_BROWSER
        else:
            return EngagementPattern.SILENT_LURKER


class ContentPersonalizer:
    """Personalizes content based on user profiles"""
    
    def __init__(self):
        self.personalization_templates = self._load_personalization_templates()
        self.a_b_test_variants = self._load_ab_test_variants()
    
    def _load_personalization_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load content personalization templates"""
        return {
            "achiever_business": {
                "hook_templates": [
                    "The {number} strategies that helped me {achievement}",
                    "How I {action} and achieved {result} in {timeframe}",
                    "The secret to {goal} that nobody talks about"
                ],
                "content_structure": ["problem", "solution", "results", "action_steps"],
                "language_style": "direct, results-focused, metric-driven",
                "emotional_triggers": ["success", "achievement", "progress", "winning"]
            },
            "explorer_travel": {
                "hook_templates": [
                    "I discovered {secret} in {location} that changed everything",
                    "The hidden {thing} in {place} that locals don't want you to know",
                    "What I learned from {experience} in {location}"
                ],
                "content_structure": ["discovery", "journey", "revelation", "invitation"],
                "language_style": "curious, adventurous, story-driven",
                "emotional_triggers": ["curiosity", "adventure", "discovery", "mystery"]
            },
            "socializer_lifestyle": {
                "hook_templates": [
                    "Everyone is talking about {trend} - here's why",
                    "The {thing} that brought our community together",
                    "How {activity} changed my relationships"
                ],
                "content_structure": ["community_context", "shared_experience", "connection", "invitation"],
                "language_style": "warm, inclusive, community-focused",
                "emotional_triggers": ["belonging", "connection", "sharing", "community"]
            }
        }
    
    def _load_ab_test_variants(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load A/B test variant templates"""
        return {
            "hook_variants": [
                {"type": "question", "template": "What if I told you {statement}?"},
                {"type": "statistic", "template": "{percentage}% of people don't know {fact}"},
                {"type": "story", "template": "Last {timeframe}, I {action} and {result}"},
                {"type": "controversy", "template": "Unpopular opinion: {statement}"},
                {"type": "curiosity", "template": "The {adjective} secret to {outcome}"}
            ],
            "cta_variants": [
                {"type": "urgency", "template": "Don't miss out - {action} now!"},
                {"type": "benefit", "template": "{Action} to {benefit}"},
                {"type": "social", "template": "Join {number} others who {action}"},
                {"type": "exclusive", "template": "Get exclusive access - {action}"},
                {"type": "simple", "template": "{Action} here"}
            ]
        }
    
    async def personalize_content(self, base_content: Dict[str, Any], 
                                user_profile: UserProfile) -> PersonalizedContent:
        """Generate personalized content for specific user"""
        
        # Select personalization template
        template_key = f"{user_profile.personality_type.value}_{self._get_primary_interest(user_profile)}"
        template = self.personalization_templates.get(
            template_key, 
            self.personalization_templates["achiever_business"]
        )
        
        # Generate personalized content
        personalized_script = await self._generate_personalized_script(
            base_content, user_profile, template
        )
        
        # Generate variants for A/B testing
        variants = await self._generate_content_variants(
            personalized_script, user_profile
        )
        
        # Calculate personalization scores
        personality_match = self._calculate_personality_match(base_content, user_profile)
        engagement_prediction = self._predict_engagement(user_profile, personalized_script)
        conversion_probability = self._predict_conversion(user_profile, personalized_script)
        
        # Determine optimal posting time
        optimal_time = self._calculate_optimal_posting_time(user_profile)
        
        # Generate personalized hashtags
        personalized_hashtags = await self._generate_personalized_hashtags(
            base_content, user_profile
        )
        
        return PersonalizedContent(
            content_id=f"pers_{uuid.uuid4().hex[:8]}",
            user_id=user_profile.user_id,
            content_type=base_content.get("type", "social_post"),
            title=personalized_script.get("title", ""),
            description=personalized_script.get("description", ""),
            script=personalized_script.get("script", ""),
            personalization_score=personality_match * engagement_prediction,
            personality_match=personality_match,
            engagement_prediction=engagement_prediction,
            conversion_probability=conversion_probability,
            optimal_posting_time=optimal_time,
            recommended_platform=self._recommend_platform(user_profile),
            personalized_hashtags=personalized_hashtags,
            call_to_action=self._generate_personalized_cta(user_profile),
            variants=variants,
            generated_timestamp=datetime.now(),
            expires_at=datetime.now() + timedelta(days=7)
        )
    
    async def _generate_personalized_script(self, base_content: Dict[str, Any],
                                          user_profile: UserProfile,
                                          template: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized script using AI"""
        
        prompt = f"""Personalize this content for a specific user:

Base Content: {base_content.get('script', '')}
User Personality: {user_profile.personality_type.value}
User Interests: {', '.join(user_profile.interests)}
User Pain Points: {', '.join(user_profile.pain_points)}
User Aspirations: {', '.join(user_profile.aspirations)}

Personalization Guidelines:
- Language Style: {template.get('language_style', 'engaging')}
- Emotional Triggers: {', '.join(template.get('emotional_triggers', []))}
- Content Structure: {' -> '.join(template.get('content_structure', []))}

Create personalized content that:
1. Resonates with their personality type
2. Addresses their specific pain points
3. Aligns with their aspirations
4. Uses their preferred language style
5. Incorporates relevant emotional triggers

Return as JSON with: title, description, script, hook"""
        
        ai_request = AIRequest(
            prompt=prompt,
            content_type=ContentType.SOCIAL_MEDIA_POST,
            platform="multi_platform",
            target_audience=user_profile.personality_type.value,
            temperature=0.7
        )
        
        try:
            response = await ai_orchestrator.generate_content(ai_request)
            return json.loads(response.content)
        except:
            # Fallback to template-based personalization
            return {
                "title": f"Personalized content for {user_profile.personality_type.value}",
                "description": "AI-personalized content based on user profile",
                "script": base_content.get('script', ''),
                "hook": "Personalized hook based on user preferences"
            }
    
    async def _generate_content_variants(self, base_script: Dict[str, Any],
                                       user_profile: UserProfile) -> List[Dict[str, Any]]:
        """Generate A/B test variants"""
        variants = []
        
        # Hook variants
        hook_variants = self.a_b_test_variants["hook_variants"]
        for i, variant_template in enumerate(hook_variants[:3]):  # Top 3 variants
            variants.append({
                "variant_id": f"hook_{i}",
                "type": "hook_variant",
                "content": variant_template["template"].format(
                    statement="you can achieve your goals faster",
                    percentage="87",
                    fact="this simple strategy",
                    timeframe="week",
                    action="tried this method",
                    result="got amazing results",
                    adjective="surprising",
                    outcome="success"
                )
            })
        
        # CTA variants
        cta_variants = self.a_b_test_variants["cta_variants"]
        for i, variant_template in enumerate(cta_variants[:3]):  # Top 3 variants
            variants.append({
                "variant_id": f"cta_{i}",
                "type": "cta_variant",
                "content": variant_template["template"].format(
                    action="Start your journey",
                    benefit="achieve your dreams",
                    number="10,000"
                )
            })
        
        return variants
    
    def _get_primary_interest(self, user_profile: UserProfile) -> str:
        """Get user's primary interest category"""
        if user_profile.content_preferences:
            return max(user_profile.content_preferences, key=user_profile.content_preferences.get)
        return "business"  # Default
    
    def _calculate_personality_match(self, content: Dict[str, Any], 
                                   user_profile: UserProfile) -> float:
        """Calculate how well content matches user personality"""
        # Simplified personality matching algorithm
        base_score = 0.5
        
        # Boost for personality-aligned content
        personality_keywords = self.personalization_templates.get(
            f"{user_profile.personality_type.value}_business", {}
        ).get("emotional_triggers", [])
        
        content_text = content.get("script", "").lower()
        for keyword in personality_keywords:
            if keyword in content_text:
                base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _predict_engagement(self, user_profile: UserProfile, content: Dict[str, Any]) -> float:
        """Predict engagement rate for personalized content"""
        base_engagement = user_profile.engagement_history.get("average_engagement", 0.03)
        
        # Boost for personalization
        personalization_boost = 0.02  # 2% boost for personalization
        
        # Boost for optimal timing
        timing_boost = 0.01 if self._is_optimal_time(user_profile) else 0
        
        return min(base_engagement + personalization_boost + timing_boost, 0.15)
    
    def _predict_conversion(self, user_profile: UserProfile, content: Dict[str, Any]) -> float:
        """Predict conversion probability"""
        base_conversion = 0.02  # 2% base conversion rate
        
        # Boost for high-value personality types
        if user_profile.personality_type in [PersonalityType.ACHIEVER, PersonalityType.CREATOR]:
            base_conversion += 0.01
        
        # Boost for high engagement users
        if user_profile.engagement_pattern == EngagementPattern.ACTIVE_COMMENTER:
            base_conversion += 0.015
        
        return min(base_conversion, 0.1)
    
    def _calculate_optimal_posting_time(self, user_profile: UserProfile) -> datetime:
        """Calculate optimal posting time for user"""
        # Use user's active hours
        if user_profile.active_hours:
            optimal_hour = max(set(user_profile.active_hours), key=user_profile.active_hours.count)
        else:
            # Default based on engagement pattern
            pattern_hours = {
                EngagementPattern.BINGE_CONSUMER: 20,  # 8 PM
                EngagementPattern.CASUAL_BROWSER: 12,  # Noon
                EngagementPattern.ACTIVE_COMMENTER: 15,  # 3 PM
                EngagementPattern.TREND_FOLLOWER: 17,  # 5 PM
                EngagementPattern.SILENT_LURKER: 19,  # 7 PM
                EngagementPattern.NICHE_ENTHUSIAST: 21  # 9 PM
            }
            optimal_hour = pattern_hours.get(user_profile.engagement_pattern, 18)
        
        # Calculate next optimal time
        now = datetime.now()
        optimal_time = now.replace(hour=optimal_hour, minute=0, second=0, microsecond=0)
        
        if optimal_time <= now:
            optimal_time += timedelta(days=1)
        
        return optimal_time
    
    def _recommend_platform(self, user_profile: UserProfile) -> str:
        """Recommend best platform for user"""
        if user_profile.preferred_platforms:
            return user_profile.preferred_platforms[0]
        
        # Default based on personality type
        platform_preferences = {
            PersonalityType.ACHIEVER: "linkedin",
            PersonalityType.EXPLORER: "instagram",
            PersonalityType.SOCIALIZER: "facebook",
            PersonalityType.CREATOR: "tiktok",
            PersonalityType.SAGE: "twitter"
        }
        
        return platform_preferences.get(user_profile.personality_type, "instagram")
    
    async def _generate_personalized_hashtags(self, content: Dict[str, Any],
                                            user_profile: UserProfile) -> List[str]:
        """Generate personalized hashtags"""
        base_hashtags = ["#personalized", "#ai", "#content"]
        
        # Add personality-based hashtags
        personality_hashtags = {
            PersonalityType.ACHIEVER: ["#success", "#goals", "#achievement"],
            PersonalityType.EXPLORER: ["#adventure", "#discover", "#explore"],
            PersonalityType.SOCIALIZER: ["#community", "#connect", "#share"],
            PersonalityType.CREATOR: ["#create", "#inspire", "#art"],
            PersonalityType.SAGE: ["#learn", "#wisdom", "#knowledge"]
        }
        
        hashtags = base_hashtags + personality_hashtags.get(user_profile.personality_type, [])
        
        # Add interest-based hashtags
        for interest in user_profile.interests[:3]:  # Top 3 interests
            hashtags.append(f"#{interest.replace(' ', '').lower()}")
        
        return hashtags[:10]  # Limit to 10 hashtags
    
    def _generate_personalized_cta(self, user_profile: UserProfile) -> str:
        """Generate personalized call-to-action"""
        personality_ctas = {
            PersonalityType.ACHIEVER: "Start achieving your goals today!",
            PersonalityType.EXPLORER: "Discover something amazing!",
            PersonalityType.SOCIALIZER: "Join our community!",
            PersonalityType.CREATOR: "Start creating now!",
            PersonalityType.SAGE: "Learn more insights!"
        }
        
        return personality_ctas.get(user_profile.personality_type, "Take action now!")
    
    def _is_optimal_time(self, user_profile: UserProfile) -> bool:
        """Check if current time is optimal for user"""
        current_hour = datetime.now().hour
        return current_hour in user_profile.active_hours


class AdvancedPersonalizationEngine:
    """Main engine for advanced content personalization"""
    
    def __init__(self):
        self.psychographic_analyzer = PsychographicAnalyzer()
        self.content_personalizer = ContentPersonalizer()
        self.user_profiles = {}  # In production, this would be a database
        self.personalization_cache = {}
    
    async def create_user_profile(self, user_id: str, user_data: Dict[str, Any]) -> UserProfile:
        """Create comprehensive user profile"""
        
        # Analyze personality and engagement patterns
        personality_type = await self.psychographic_analyzer.analyze_user_personality(user_data)
        engagement_pattern = await self.psychographic_analyzer.analyze_engagement_pattern(user_data)
        
        # Extract user preferences
        content_preferences = self._extract_content_preferences(user_data)
        active_hours = self._extract_active_hours(user_data)
        
        # Create profile
        profile = UserProfile(
            user_id=user_id,
            personality_type=personality_type,
            engagement_pattern=engagement_pattern,
            preferred_content_personality=ContentPersonality.FRIENDLY,  # Default
            age_range=user_data.get("age_range", "25-34"),
            location=user_data.get("location", "US"),
            timezone=user_data.get("timezone", "UTC"),
            language=user_data.get("language", "en"),
            active_hours=active_hours,
            preferred_platforms=user_data.get("preferred_platforms", ["instagram"]),
            content_preferences=content_preferences,
            engagement_history=user_data.get("engagement_history", {}),
            values=user_data.get("values", ["success", "growth"]),
            interests=user_data.get("interests", ["business", "technology"]),
            pain_points=user_data.get("pain_points", ["lack of time", "information overload"]),
            aspirations=user_data.get("aspirations", ["financial freedom", "personal growth"]),
            average_session_duration=user_data.get("avg_session_duration", 300),
            content_completion_rate=user_data.get("completion_rate", 0.7),
            sharing_propensity=user_data.get("sharing_propensity", 0.1),
            comment_sentiment=user_data.get("comment_sentiment", 0.5),
            last_updated=datetime.now(),
            confidence_score=0.8
        )
        
        # Store profile
        self.user_profiles[user_id] = profile
        
        return profile
    
    async def generate_personalized_content(self, user_id: str, 
                                          base_content: Dict[str, Any]) -> PersonalizedContent:
        """Generate personalized content for specific user"""
        
        if user_id not in self.user_profiles:
            raise ValueError(f"User profile not found for user_id: {user_id}")
        
        user_profile = self.user_profiles[user_id]
        
        # Generate personalized content
        personalized_content = await self.content_personalizer.personalize_content(
            base_content, user_profile
        )
        
        # Cache for performance
        cache_key = f"{user_id}_{base_content.get('content_id', 'unknown')}"
        self.personalization_cache[cache_key] = personalized_content
        
        return personalized_content
    
    async def batch_personalize_content(self, user_ids: List[str],
                                      base_content: Dict[str, Any]) -> Dict[str, PersonalizedContent]:
        """Generate personalized content for multiple users"""
        
        results = {}
        
        # Process in batches for efficiency
        batch_size = 10
        for i in range(0, len(user_ids), batch_size):
            batch = user_ids[i:i + batch_size]
            
            # Generate personalized content for batch
            batch_tasks = [
                self.generate_personalized_content(user_id, base_content)
                for user_id in batch
                if user_id in self.user_profiles
            ]
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            # Process results
            for user_id, result in zip(batch, batch_results):
                if isinstance(result, PersonalizedContent):
                    results[user_id] = result
                else:
                    logger.error(f"Failed to personalize content for user {user_id}: {result}")
        
        return results
    
    def _extract_content_preferences(self, user_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract content preferences from user data"""
        preferences = {}
        
        # Analyze interaction history
        interactions = user_data.get("content_interactions", [])
        for interaction in interactions:
            category = interaction.get("category", "general")
            engagement_score = interaction.get("engagement_score", 0)
            
            if category in preferences:
                preferences[category] = (preferences[category] + engagement_score) / 2
            else:
                preferences[category] = engagement_score
        
        return preferences
    
    def _extract_active_hours(self, user_data: Dict[str, Any]) -> List[int]:
        """Extract user's most active hours"""
        session_data = user_data.get("session_data", [])
        
        if not session_data:
            return [9, 12, 15, 18, 21]  # Default active hours
        
        # Count activity by hour
        hour_counts = defaultdict(int)
        for session in session_data:
            if "timestamp" in session:
                hour = datetime.fromisoformat(session["timestamp"]).hour
                hour_counts[hour] += 1
        
        # Return top 5 most active hours
        sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
        return [hour for hour, count in sorted_hours[:5]]
    
    def get_personalization_insights(self, user_id: str) -> Dict[str, Any]:
        """Get personalization insights for user"""
        
        if user_id not in self.user_profiles:
            return {"error": "User profile not found"}
        
        profile = self.user_profiles[user_id]
        
        return {
            "user_id": user_id,
            "personality_type": profile.personality_type.value,
            "engagement_pattern": profile.engagement_pattern.value,
            "content_preferences": profile.content_preferences,
            "optimal_posting_times": profile.active_hours,
            "recommended_platforms": profile.preferred_platforms,
            "personalization_confidence": profile.confidence_score,
            "last_updated": profile.last_updated.isoformat()
        }


# Global personalization engine instance
personalization_engine = AdvancedPersonalizationEngine()

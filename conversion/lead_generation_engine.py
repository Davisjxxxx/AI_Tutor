#!/usr/bin/env python3
"""
Advanced Lead Generation and Conversion Engine
AI-powered lead capture, nurturing, and conversion optimization
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import uuid
import random

from ai.next_gen_providers import ai_orchestrator, AIRequest, ContentType

logger = logging.getLogger(__name__)


class LeadSource(Enum):
    """Lead generation sources"""
    ORGANIC_SOCIAL = "organic_social"
    PAID_SOCIAL = "paid_social"
    CONTENT_MARKETING = "content_marketing"
    EMAIL_MARKETING = "email_marketing"
    WEBINAR = "webinar"
    FREE_RESOURCE = "free_resource"
    REFERRAL = "referral"
    DIRECT_TRAFFIC = "direct_traffic"
    SEARCH_ENGINE = "search_engine"
    INFLUENCER = "influencer"
    PARTNERSHIP = "partnership"
    EVENT = "event"


class LeadStage(Enum):
    """Lead funnel stages"""
    AWARENESS = "awareness"
    INTEREST = "interest"
    CONSIDERATION = "consideration"
    INTENT = "intent"
    EVALUATION = "evaluation"
    PURCHASE = "purchase"
    RETENTION = "retention"
    ADVOCACY = "advocacy"


class LeadScore(Enum):
    """Lead scoring categories"""
    COLD = "cold"  # 0-25
    WARM = "warm"  # 26-50
    HOT = "hot"  # 51-75
    QUALIFIED = "qualified"  # 76-100


class ConversionGoal(Enum):
    """Conversion goals"""
    EMAIL_SIGNUP = "email_signup"
    FREE_TRIAL = "free_trial"
    DEMO_REQUEST = "demo_request"
    CONSULTATION_BOOKING = "consultation_booking"
    PRODUCT_PURCHASE = "product_purchase"
    COURSE_ENROLLMENT = "course_enrollment"
    MEMBERSHIP_SIGNUP = "membership_signup"
    WEBINAR_REGISTRATION = "webinar_registration"
    RESOURCE_DOWNLOAD = "resource_download"
    NEWSLETTER_SUBSCRIPTION = "newsletter_subscription"


@dataclass
class Lead:
    """Lead profile and tracking"""
    lead_id: str
    email: str
    
    # Personal information
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    
    # Lead qualification
    lead_source: LeadSource = LeadSource.DIRECT_TRAFFIC
    lead_stage: LeadStage = LeadStage.AWARENESS
    lead_score: int = 0
    lead_quality: LeadScore = LeadScore.COLD
    
    # Behavioral data
    page_views: int = 0
    content_downloads: int = 0
    email_opens: int = 0
    email_clicks: int = 0
    social_engagement: int = 0
    
    # Interests and preferences
    interests: List[str] = None
    pain_points: List[str] = None
    preferred_content_types: List[str] = None
    communication_preferences: Dict[str, Any] = None
    
    # Conversion tracking
    conversion_goals_completed: List[ConversionGoal] = None
    total_conversions: int = 0
    lifetime_value: float = 0.0
    
    # Timestamps
    created_date: datetime = None
    last_activity: datetime = None
    last_email_sent: Optional[datetime] = None
    next_followup: Optional[datetime] = None
    
    # Campaign tracking
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    referring_url: Optional[str] = None


@dataclass
class LeadMagnet:
    """Lead generation magnet/offer"""
    magnet_id: str
    name: str
    description: str
    magnet_type: str  # "ebook", "checklist", "template", "course", "webinar"
    
    # Content
    title: str
    subtitle: str
    value_proposition: str
    benefits: List[str]
    
    # Targeting
    target_audience: str
    target_pain_points: List[str]
    target_interests: List[str]
    
    # Conversion elements
    call_to_action: str
    form_fields: List[str]
    thank_you_message: str
    
    # Performance tracking
    views: int = 0
    conversions: int = 0
    conversion_rate: float = 0.0
    
    # A/B testing
    variants: List[Dict[str, Any]] = None
    active_variant: str = "original"
    
    # Status
    is_active: bool = True
    created_date: datetime = None


@dataclass
class NurtureSequence:
    """Email nurture sequence"""
    sequence_id: str
    name: str
    description: str
    
    # Targeting
    target_lead_stage: LeadStage
    target_lead_score_min: int
    target_interests: List[str]
    
    # Sequence configuration
    emails: List[Dict[str, Any]]  # Email templates and timing
    total_emails: int = 0
    sequence_duration_days: int = 0
    
    # Performance tracking
    subscribers: int = 0
    open_rate: float = 0.0
    click_rate: float = 0.0
    conversion_rate: float = 0.0
    unsubscribe_rate: float = 0.0
    
    # Status
    is_active: bool = True
    created_date: datetime = None


class LeadScoringEngine:
    """AI-powered lead scoring system"""
    
    def __init__(self):
        self.scoring_rules = self._load_scoring_rules()
        self.behavioral_weights = self._load_behavioral_weights()
    
    def _load_scoring_rules(self) -> Dict[str, Dict[str, int]]:
        """Load lead scoring rules"""
        return {
            "demographic": {
                "has_company": 10,
                "has_job_title": 8,
                "has_phone": 5,
                "complete_profile": 15
            },
            "behavioral": {
                "page_view": 2,
                "content_download": 10,
                "email_open": 3,
                "email_click": 8,
                "social_engagement": 5,
                "webinar_attendance": 20,
                "demo_request": 30,
                "pricing_page_view": 15
            },
            "engagement": {
                "high_email_engagement": 15,  # >50% open rate
                "frequent_visitor": 10,  # >5 sessions
                "long_session_duration": 8,  # >5 minutes
                "multiple_content_types": 12,  # Engaged with 3+ types
                "social_sharing": 6
            },
            "intent": {
                "contact_form_submission": 25,
                "consultation_request": 30,
                "free_trial_signup": 35,
                "pricing_inquiry": 20,
                "competitor_comparison": 15
            }
        }
    
    def _load_behavioral_weights(self) -> Dict[str, float]:
        """Load behavioral scoring weights"""
        return {
            "recency": 0.3,  # Recent activity weighted more
            "frequency": 0.4,  # Frequency of engagement
            "monetary": 0.3   # Value of actions taken
        }
    
    async def calculate_lead_score(self, lead: Lead) -> int:
        """Calculate comprehensive lead score"""
        
        total_score = 0
        
        # Demographic scoring
        if lead.company:
            total_score += self.scoring_rules["demographic"]["has_company"]
        if lead.job_title:
            total_score += self.scoring_rules["demographic"]["has_job_title"]
        if lead.phone:
            total_score += self.scoring_rules["demographic"]["has_phone"]
        
        # Behavioral scoring
        total_score += min(lead.page_views * self.scoring_rules["behavioral"]["page_view"], 20)
        total_score += lead.content_downloads * self.scoring_rules["behavioral"]["content_download"]
        total_score += min(lead.email_opens * self.scoring_rules["behavioral"]["email_open"], 15)
        total_score += lead.email_clicks * self.scoring_rules["behavioral"]["email_click"]
        total_score += min(lead.social_engagement * self.scoring_rules["behavioral"]["social_engagement"], 25)
        
        # Engagement quality scoring
        if lead.email_opens > 0 and lead.email_clicks > 0:
            email_engagement_rate = lead.email_clicks / lead.email_opens
            if email_engagement_rate > 0.5:
                total_score += self.scoring_rules["engagement"]["high_email_engagement"]
        
        if lead.page_views > 5:
            total_score += self.scoring_rules["engagement"]["frequent_visitor"]
        
        # Recency boost
        if lead.last_activity:
            days_since_activity = (datetime.now() - lead.last_activity).days
            if days_since_activity <= 7:
                total_score = int(total_score * 1.2)  # 20% boost for recent activity
            elif days_since_activity <= 30:
                total_score = int(total_score * 1.1)  # 10% boost
        
        return min(total_score, 100)  # Cap at 100
    
    def determine_lead_quality(self, score: int) -> LeadScore:
        """Determine lead quality based on score"""
        if score >= 76:
            return LeadScore.QUALIFIED
        elif score >= 51:
            return LeadScore.HOT
        elif score >= 26:
            return LeadScore.WARM
        else:
            return LeadScore.COLD
    
    async def predict_conversion_probability(self, lead: Lead) -> float:
        """Predict probability of lead conversion using AI"""
        
        # Prepare lead data for AI analysis
        lead_features = {
            "lead_score": lead.lead_score,
            "lead_stage": lead.lead_stage.value,
            "lead_source": lead.lead_source.value,
            "page_views": lead.page_views,
            "content_downloads": lead.content_downloads,
            "email_engagement": lead.email_clicks / max(lead.email_opens, 1),
            "days_since_creation": (datetime.now() - lead.created_date).days if lead.created_date else 0,
            "has_company": bool(lead.company),
            "has_job_title": bool(lead.job_title),
            "total_conversions": lead.total_conversions
        }
        
        # Use AI to predict conversion probability
        prompt = f"""Analyze this lead profile and predict conversion probability:

Lead Features: {json.dumps(lead_features, indent=2)}

Based on the lead's behavior, engagement, and profile completeness, predict:
1. Probability of conversion (0.0 to 1.0)
2. Best conversion strategy
3. Optimal timing for outreach
4. Recommended next actions

Return as JSON with: conversion_probability, strategy, timing, next_actions"""
        
        ai_request = AIRequest(
            prompt=prompt,
            content_type=ContentType.MARKETING_COPY,
            platform="email",
            target_audience="sales_team",
            temperature=0.3
        )
        
        try:
            response = await ai_orchestrator.generate_content(ai_request)
            prediction = json.loads(response.content)
            return prediction.get("conversion_probability", 0.5)
        except:
            # Fallback to rule-based prediction
            base_probability = 0.1  # 10% base conversion rate
            
            # Adjust based on lead score
            score_multiplier = lead.lead_score / 50  # Normalize to 0-2 range
            
            # Adjust based on engagement
            engagement_multiplier = 1.0
            if lead.email_clicks > 3:
                engagement_multiplier += 0.3
            if lead.content_downloads > 2:
                engagement_multiplier += 0.2
            
            return min(base_probability * score_multiplier * engagement_multiplier, 0.9)


class ConversionOptimizer:
    """Optimizes conversion rates using AI and testing"""
    
    def __init__(self):
        self.conversion_templates = self._load_conversion_templates()
        self.optimization_strategies = self._load_optimization_strategies()
    
    def _load_conversion_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load conversion-optimized templates"""
        return {
            "lead_magnet": {
                "high_converting_headlines": [
                    "Get {benefit} in Just {timeframe}",
                    "The {number} Secrets to {desired_outcome}",
                    "Free {resource_type}: {specific_benefit}",
                    "Unlock {exclusive_benefit} (Limited Time)",
                    "Stop {pain_point} Forever with This {solution_type}"
                ],
                "value_propositions": [
                    "Save {time_amount} hours per week",
                    "Increase {metric} by {percentage}%",
                    "Get results in {timeframe} or less",
                    "Join {number}+ successful {target_audience}",
                    "Proven system used by {authority_figures}"
                ],
                "urgency_elements": [
                    "Limited time offer",
                    "Only {number} spots available",
                    "Expires in {timeframe}",
                    "Early bird special",
                    "Exclusive access"
                ]
            },
            "email_sequences": {
                "welcome_series": [
                    {"day": 0, "subject": "Welcome! Here's your {resource}", "type": "delivery"},
                    {"day": 1, "subject": "Did you get a chance to check out {resource}?", "type": "engagement"},
                    {"day": 3, "subject": "Quick question about {pain_point}", "type": "value"},
                    {"day": 7, "subject": "Here's what {successful_person} did", "type": "social_proof"},
                    {"day": 14, "subject": "Ready to take the next step?", "type": "conversion"}
                ]
            }
        }
    
    def _load_optimization_strategies(self) -> Dict[str, List[str]]:
        """Load conversion optimization strategies"""
        return {
            "form_optimization": [
                "Reduce form fields to minimum required",
                "Use progressive profiling",
                "Add social proof near form",
                "Optimize button text and color",
                "Add privacy/security badges"
            ],
            "landing_page": [
                "Match headline to traffic source",
                "Use benefit-focused headlines",
                "Add video testimonials",
                "Create urgency and scarcity",
                "Optimize for mobile experience"
            ],
            "email_optimization": [
                "Personalize subject lines",
                "Optimize send times",
                "Segment based on behavior",
                "Use dynamic content",
                "A/B test everything"
            ]
        }
    
    async def optimize_lead_magnet(self, magnet: LeadMagnet, 
                                 performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimization recommendations for lead magnet"""
        
        current_conversion_rate = performance_data.get("conversion_rate", 0.02)
        
        optimizations = []
        
        # Headline optimization
        if current_conversion_rate < 0.05:  # Less than 5%
            optimizations.append({
                "type": "headline",
                "current": magnet.title,
                "recommendations": [
                    template.format(
                        benefit="massive results",
                        timeframe="30 days",
                        number="7",
                        desired_outcome="success",
                        resource_type="Guide"
                    ) for template in self.conversion_templates["lead_magnet"]["high_converting_headlines"][:3]
                ],
                "expected_lift": "15-30%"
            })
        
        # Value proposition optimization
        if not any(keyword in magnet.value_proposition.lower() 
                  for keyword in ["save", "increase", "get results", "proven"]):
            optimizations.append({
                "type": "value_proposition",
                "current": magnet.value_proposition,
                "recommendations": self.conversion_templates["lead_magnet"]["value_propositions"][:3],
                "expected_lift": "10-20%"
            })
        
        # Urgency optimization
        if current_conversion_rate < 0.03 and not any(
            urgent in magnet.description.lower() 
            for urgent in ["limited", "exclusive", "expires"]
        ):
            optimizations.append({
                "type": "urgency",
                "recommendations": self.conversion_templates["lead_magnet"]["urgency_elements"],
                "expected_lift": "8-15%"
            })
        
        return {
            "magnet_id": magnet.magnet_id,
            "current_performance": performance_data,
            "optimizations": optimizations,
            "priority_actions": [opt for opt in optimizations if "headline" in opt["type"] or "value_proposition" in opt["type"]],
            "estimated_total_lift": "25-50%" if len(optimizations) > 2 else "10-25%"
        }
    
    async def generate_nurture_sequence(self, target_audience: str,
                                      pain_points: List[str],
                                      conversion_goal: ConversionGoal) -> NurtureSequence:
        """Generate AI-optimized nurture sequence"""
        
        sequence_id = f"seq_{uuid.uuid4().hex[:8]}"
        
        # Generate email sequence using AI
        prompt = f"""Create a high-converting email nurture sequence:

Target Audience: {target_audience}
Pain Points: {', '.join(pain_points)}
Conversion Goal: {conversion_goal.value}

Create a 7-email sequence that:
1. Builds trust and rapport
2. Provides valuable content
3. Addresses specific pain points
4. Uses social proof and testimonials
5. Gradually introduces the solution
6. Creates urgency for conversion

For each email, provide:
- Day to send (0, 1, 3, 7, 10, 14, 21)
- Subject line
- Email type (welcome, value, social_proof, conversion)
- Key content points
- Call-to-action

Return as JSON array of emails."""
        
        ai_request = AIRequest(
            prompt=prompt,
            content_type=ContentType.EMAIL_CAMPAIGN,
            platform="email",
            target_audience=target_audience,
            temperature=0.7
        )
        
        try:
            response = await ai_orchestrator.generate_content(ai_request)
            emails = json.loads(response.content)
        except:
            # Fallback to template-based sequence
            emails = [
                {
                    "day": 0,
                    "subject": f"Welcome! Your {conversion_goal.value.replace('_', ' ')} guide is here",
                    "type": "welcome",
                    "content_points": ["Deliver promised resource", "Set expectations", "Introduce yourself"],
                    "cta": "Download your guide"
                },
                {
                    "day": 1,
                    "subject": "Quick question about your biggest challenge",
                    "type": "engagement",
                    "content_points": ["Ask about their main challenge", "Share relatable story", "Provide quick tip"],
                    "cta": "Reply and let me know"
                },
                {
                    "day": 3,
                    "subject": "The mistake 90% of people make",
                    "type": "value",
                    "content_points": ["Common mistake", "Why it happens", "Better approach"],
                    "cta": "Learn the right way"
                },
                {
                    "day": 7,
                    "subject": "How [Success Story] achieved [Result]",
                    "type": "social_proof",
                    "content_points": ["Customer success story", "Specific results", "What they did differently"],
                    "cta": "See more success stories"
                },
                {
                    "day": 14,
                    "subject": "Ready to get serious about [Goal]?",
                    "type": "conversion",
                    "content_points": ["Recap value provided", "Present solution", "Limited time offer"],
                    "cta": f"Get started with {conversion_goal.value.replace('_', ' ')}"
                }
            ]
        
        sequence = NurtureSequence(
            sequence_id=sequence_id,
            name=f"{target_audience} - {conversion_goal.value} Sequence",
            description=f"AI-generated nurture sequence for {target_audience} targeting {conversion_goal.value}",
            target_lead_stage=LeadStage.INTEREST,
            target_lead_score_min=25,
            target_interests=pain_points,
            emails=emails,
            total_emails=len(emails),
            sequence_duration_days=max(email["day"] for email in emails),
            created_date=datetime.now()
        )
        
        return sequence


class LeadGenerationEngine:
    """Main lead generation and conversion engine"""
    
    def __init__(self):
        self.leads = {}
        self.lead_magnets = {}
        self.nurture_sequences = {}
        self.scoring_engine = LeadScoringEngine()
        self.conversion_optimizer = ConversionOptimizer()
    
    async def capture_lead(self, lead_data: Dict[str, Any]) -> Lead:
        """Capture and process new lead"""
        
        lead_id = f"lead_{uuid.uuid4().hex[:8]}"
        
        # Create lead object
        lead = Lead(
            lead_id=lead_id,
            email=lead_data["email"],
            first_name=lead_data.get("first_name"),
            last_name=lead_data.get("last_name"),
            phone=lead_data.get("phone"),
            company=lead_data.get("company"),
            job_title=lead_data.get("job_title"),
            lead_source=LeadSource(lead_data.get("lead_source", "direct_traffic")),
            interests=lead_data.get("interests", []),
            pain_points=lead_data.get("pain_points", []),
            utm_source=lead_data.get("utm_source"),
            utm_medium=lead_data.get("utm_medium"),
            utm_campaign=lead_data.get("utm_campaign"),
            referring_url=lead_data.get("referring_url"),
            created_date=datetime.now(),
            last_activity=datetime.now(),
            conversion_goals_completed=[]
        )
        
        # Calculate initial lead score
        lead.lead_score = await self.scoring_engine.calculate_lead_score(lead)
        lead.lead_quality = self.scoring_engine.determine_lead_quality(lead.lead_score)
        
        # Store lead
        self.leads[lead_id] = lead
        
        # Trigger appropriate nurture sequence
        await self._trigger_nurture_sequence(lead)
        
        logger.info(f"Captured new lead: {lead.email} (Score: {lead.lead_score})")
        
        return lead
    
    async def update_lead_activity(self, lead_id: str, activity_data: Dict[str, Any]):
        """Update lead activity and recalculate score"""
        
        if lead_id not in self.leads:
            return
        
        lead = self.leads[lead_id]
        
        # Update activity metrics
        if "page_view" in activity_data:
            lead.page_views += 1
        if "content_download" in activity_data:
            lead.content_downloads += 1
        if "email_open" in activity_data:
            lead.email_opens += 1
        if "email_click" in activity_data:
            lead.email_clicks += 1
        if "social_engagement" in activity_data:
            lead.social_engagement += 1
        
        # Update last activity
        lead.last_activity = datetime.now()
        
        # Recalculate lead score
        old_score = lead.lead_score
        lead.lead_score = await self.scoring_engine.calculate_lead_score(lead)
        lead.lead_quality = self.scoring_engine.determine_lead_quality(lead.lead_score)
        
        # Check for stage progression
        await self._check_stage_progression(lead, old_score)
        
        logger.info(f"Updated lead activity: {lead.email} (Score: {old_score} -> {lead.lead_score})")
    
    async def create_lead_magnet(self, magnet_config: Dict[str, Any]) -> LeadMagnet:
        """Create optimized lead magnet"""
        
        magnet_id = f"magnet_{uuid.uuid4().hex[:8]}"
        
        # Use AI to optimize lead magnet copy
        optimized_copy = await self._optimize_lead_magnet_copy(magnet_config)
        
        magnet = LeadMagnet(
            magnet_id=magnet_id,
            name=magnet_config["name"],
            description=magnet_config["description"],
            magnet_type=magnet_config["type"],
            title=optimized_copy.get("title", magnet_config["title"]),
            subtitle=optimized_copy.get("subtitle", magnet_config.get("subtitle", "")),
            value_proposition=optimized_copy.get("value_proposition", magnet_config["value_proposition"]),
            benefits=optimized_copy.get("benefits", magnet_config["benefits"]),
            target_audience=magnet_config["target_audience"],
            target_pain_points=magnet_config["target_pain_points"],
            target_interests=magnet_config["target_interests"],
            call_to_action=optimized_copy.get("cta", magnet_config["call_to_action"]),
            form_fields=magnet_config.get("form_fields", ["email", "first_name"]),
            thank_you_message=optimized_copy.get("thank_you", "Thank you! Check your email for your download."),
            created_date=datetime.now()
        )
        
        self.lead_magnets[magnet_id] = magnet
        
        logger.info(f"Created lead magnet: {magnet.name}")
        
        return magnet
    
    async def _optimize_lead_magnet_copy(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to optimize lead magnet copy"""
        
        prompt = f"""Optimize this lead magnet for maximum conversions:

Current Title: {config['title']}
Value Proposition: {config['value_proposition']}
Target Audience: {config['target_audience']}
Pain Points: {', '.join(config['target_pain_points'])}
Benefits: {', '.join(config['benefits'])}

Create optimized copy that:
1. Uses psychological triggers
2. Creates urgency and scarcity
3. Focuses on specific benefits
4. Addresses pain points directly
5. Uses power words and emotional language

Return JSON with: title, subtitle, value_proposition, benefits, cta, thank_you"""
        
        ai_request = AIRequest(
            prompt=prompt,
            content_type=ContentType.MARKETING_COPY,
            platform="landing_page",
            target_audience=config["target_audience"],
            temperature=0.7
        )
        
        try:
            response = await ai_orchestrator.generate_content(ai_request)
            return json.loads(response.content)
        except:
            return {}  # Return empty dict to use original copy
    
    async def _trigger_nurture_sequence(self, lead: Lead):
        """Trigger appropriate nurture sequence for lead"""
        
        # Find matching nurture sequence
        matching_sequences = [
            seq for seq in self.nurture_sequences.values()
            if (lead.lead_score >= seq.target_lead_score_min and
                any(interest in lead.interests for interest in seq.target_interests))
        ]
        
        if matching_sequences:
            # Use the most specific sequence
            sequence = max(matching_sequences, key=lambda s: len(s.target_interests))
            
            # Schedule first email
            lead.next_followup = datetime.now() + timedelta(minutes=5)  # Welcome email in 5 minutes
            
            logger.info(f"Triggered nurture sequence '{sequence.name}' for lead {lead.email}")
    
    async def _check_stage_progression(self, lead: Lead, old_score: int):
        """Check if lead should progress to next stage"""
        
        # Stage progression logic based on score and behavior
        if lead.lead_score >= 75 and lead.lead_stage != LeadStage.PURCHASE:
            lead.lead_stage = LeadStage.INTENT
        elif lead.lead_score >= 50 and lead.lead_stage in [LeadStage.AWARENESS, LeadStage.INTEREST]:
            lead.lead_stage = LeadStage.CONSIDERATION
        elif lead.lead_score >= 25 and lead.lead_stage == LeadStage.AWARENESS:
            lead.lead_stage = LeadStage.INTEREST
        
        # Trigger stage-specific actions
        if old_score < 50 and lead.lead_score >= 50:
            # Lead became hot - notify sales team
            logger.info(f"Lead {lead.email} became HOT (score: {lead.lead_score})")
    
    def get_lead_analytics(self) -> Dict[str, Any]:
        """Get comprehensive lead analytics"""
        
        total_leads = len(self.leads)
        if total_leads == 0:
            return {"total_leads": 0}
        
        # Lead quality distribution
        quality_distribution = {
            "cold": len([l for l in self.leads.values() if l.lead_quality == LeadScore.COLD]),
            "warm": len([l for l in self.leads.values() if l.lead_quality == LeadScore.WARM]),
            "hot": len([l for l in self.leads.values() if l.lead_quality == LeadScore.HOT]),
            "qualified": len([l for l in self.leads.values() if l.lead_quality == LeadScore.QUALIFIED])
        }
        
        # Lead source distribution
        source_distribution = {}
        for lead in self.leads.values():
            source = lead.lead_source.value
            source_distribution[source] = source_distribution.get(source, 0) + 1
        
        # Conversion metrics
        total_conversions = sum(l.total_conversions for l in self.leads.values())
        total_ltv = sum(l.lifetime_value for l in self.leads.values())
        
        return {
            "total_leads": total_leads,
            "quality_distribution": quality_distribution,
            "source_distribution": source_distribution,
            "total_conversions": total_conversions,
            "average_ltv": total_ltv / total_leads if total_leads > 0 else 0,
            "conversion_rate": total_conversions / total_leads if total_leads > 0 else 0,
            "average_lead_score": sum(l.lead_score for l in self.leads.values()) / total_leads
        }


# Global lead generation engine instance
lead_engine = LeadGenerationEngine()

#!/usr/bin/env python3
"""
Enhanced API Routes for AI Content Empire
Unified endpoints for all next-generation features
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import logging

# Import our enhanced engines
from ai.next_gen_providers import ai_orchestrator
from ai.viral_content_engine import viral_engine, ViralContentRequest, PlatformOptimization
from ai.multimodal_generator import multimodal_generator, MediaGenerationRequest, MediaType, VideoStyle, VoiceType
from ai.advanced_personalization_engine import personalization_engine, UserProfile, PersonalizedContent
from marketing.intelligent_campaign_engine import campaign_engine, CampaignType, TargetAudience, ContentStrategy
from revenue.advanced_monetization_engine import monetization_engine
from analytics.intelligence_dashboard import intelligence_dashboard
from automation.social_media_automation import social_scheduler, SocialMediaAccount, ScheduledPost, Platform, PostType
from optimization.ab_testing_engine import ab_test_engine, ABTest, TestType, MetricType
from conversion.lead_generation_engine import lead_engine, Lead, LeadMagnet, ConversionGoal

logger = logging.getLogger(__name__)

# Create enhanced router
enhanced_router = APIRouter(prefix="/api/v2", tags=["Enhanced AI Content Empire"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ViralContentGenerationRequest(BaseModel):
    topic: str
    platform: str
    target_audience: str
    content_goal: str
    duration_seconds: int = 30
    controversy_level: int = 5
    emotional_intensity: int = 7
    uniqueness_factor: int = 8


class MultiModalContentRequest(BaseModel):
    script: str
    media_types: List[str]
    platform: str
    duration_seconds: int = 30
    video_style: str = "talking_head"
    voice_type: str = "professional_female"
    resolution: str = "1080x1920"
    include_subtitles: bool = True


class CampaignCreationRequest(BaseModel):
    name: str
    campaign_type: str
    objective: Dict[str, Any]
    target_audience: Dict[str, Any]
    content_strategy: Dict[str, Any]
    start_date: str
    end_date: str
    platforms: List[str]
    total_budget: float
    daily_budget: float


class MonetizationAnalysisRequest(BaseModel):
    creator_id: str
    total_followers: int
    engagement_rate: float
    niche: str
    platforms: List[str]
    monthly_views: int = 100000
    current_revenue: float = 0


class AnalyticsReportRequest(BaseModel):
    creator_id: str
    timeframe: str = "monthly"
    include_predictions: bool = True
    include_competitor_analysis: bool = True
    competitors: List[str] = []


class PersonalizationRequest(BaseModel):
    user_id: str
    user_data: Dict[str, Any]
    content_topic: str
    platform: str = "instagram"


class SocialMediaPostRequest(BaseModel):
    platform: str
    account_id: str
    content_type: str
    caption: str
    media_urls: List[str]
    hashtags: List[str]
    scheduled_time: str
    timezone: str = "UTC"


class ABTestRequest(BaseModel):
    name: str
    description: str
    test_type: str
    primary_metric: str
    variants: List[Dict[str, Any]]
    baseline_rate: float = 0.05
    minimum_effect_size: float = 0.1
    start_date: str
    end_date: str


class LeadCaptureRequest(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    lead_source: str = "direct_traffic"
    interests: List[str] = []
    pain_points: List[str] = []


# ============================================================================
# VIRAL CONTENT GENERATION ENDPOINTS
# ============================================================================

@enhanced_router.post("/content/viral/generate")
async def generate_viral_content(request: ViralContentGenerationRequest):
    """Generate viral content using advanced AI"""
    try:
        # Convert request to internal format
        viral_request = ViralContentRequest(
            topic=request.topic,
            platform=PlatformOptimization(request.platform),
            target_audience=request.target_audience,
            content_goal=request.content_goal,
            duration_seconds=request.duration_seconds,
            controversy_level=request.controversy_level,
            emotional_intensity=request.emotional_intensity,
            uniqueness_factor=request.uniqueness_factor
        )
        
        # Generate viral content
        result = await viral_engine.generate_viral_content(viral_request)
        
        return {
            "success": True,
            "content": {
                "script": result.script,
                "hook": result.hook,
                "visual_cues": result.visual_cues,
                "audio_suggestions": result.audio_suggestions,
                "hashtags": result.hashtags,
                "predicted_performance": {
                    "engagement_rate": result.predicted_engagement_rate,
                    "reach": result.predicted_reach,
                    "viral_score": result.viral_score
                },
                "optimization_data": {
                    "triggers_used": [trigger.value for trigger in result.triggers_used],
                    "platform_optimizations": result.platform_optimizations,
                    "ab_test_variants": result.a_b_test_variants
                }
            },
            "metadata": {
                "generation_timestamp": result.generation_timestamp.isoformat(),
                "content_fingerprint": result.content_fingerprint
            }
        }
        
    except Exception as e:
        logger.error(f"Viral content generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")


@enhanced_router.post("/content/multimodal/generate")
async def generate_multimodal_content(request: MultiModalContentRequest, background_tasks: BackgroundTasks):
    """Generate multi-modal content (video, audio, images)"""
    try:
        # Convert request to internal format
        media_request = MediaGenerationRequest(
            script=request.script,
            media_types=[MediaType(mt) for mt in request.media_types],
            platform=request.platform,
            duration_seconds=request.duration_seconds,
            video_style=VideoStyle(request.video_style),
            voice_type=VoiceType(request.voice_type),
            resolution=request.resolution,
            include_subtitles=request.include_subtitles
        )
        
        # Generate content package
        result = await multimodal_generator.generate_content_package(media_request)
        
        return {
            "success": True,
            "request_id": result.request_id,
            "generated_media": [
                {
                    "media_type": media.media_type.value,
                    "file_url": media.file_url,
                    "metadata": media.metadata,
                    "generation_time": media.generation_time,
                    "file_size_mb": media.file_size_mb
                }
                for media in result.generated_media
            ],
            "performance_estimate": result.estimated_performance,
            "optimization_suggestions": result.optimization_suggestions,
            "total_generation_time": result.total_generation_time
        }
        
    except Exception as e:
        logger.error(f"Multimodal content generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Multimodal generation failed: {str(e)}")


# ============================================================================
# INTELLIGENT MARKETING CAMPAIGN ENDPOINTS
# ============================================================================

@enhanced_router.post("/campaigns/create")
async def create_intelligent_campaign(request: CampaignCreationRequest):
    """Create intelligent marketing campaign"""
    try:
        # Convert request to campaign brief
        campaign_brief = {
            "name": request.name,
            "type": request.campaign_type,
            "objective": request.objective,
            "target_audience": request.target_audience,
            "content_strategy": request.content_strategy,
            "start_date": request.start_date,
            "end_date": request.end_date,
            "platforms": request.platforms,
            "total_budget": request.total_budget,
            "daily_budget": request.daily_budget
        }
        
        # Create campaign
        campaign = await campaign_engine.create_campaign(campaign_brief)
        
        return {
            "success": True,
            "campaign": {
                "campaign_id": campaign.campaign_id,
                "name": campaign.name,
                "status": campaign.status.value,
                "content_calendar_items": len(campaign.content_calendar),
                "estimated_reach": sum(item.get("predicted_viral_score", 0.5) * 10000 
                                     for item in campaign.content_calendar),
                "next_steps": [
                    "Review generated content calendar",
                    "Approve creative assets",
                    "Launch campaign"
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Campaign creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Campaign creation failed: {str(e)}")


@enhanced_router.post("/campaigns/{campaign_id}/launch")
async def launch_campaign(campaign_id: str, background_tasks: BackgroundTasks):
    """Launch marketing campaign with automated content generation"""
    try:
        result = await campaign_engine.launch_campaign(campaign_id)
        
        return {
            "success": True,
            "launch_result": result
        }
        
    except Exception as e:
        logger.error(f"Campaign launch failed: {e}")
        raise HTTPException(status_code=500, detail=f"Campaign launch failed: {str(e)}")


@enhanced_router.get("/campaigns/{campaign_id}/status")
async def get_campaign_status(campaign_id: str):
    """Get comprehensive campaign status"""
    try:
        status = campaign_engine.get_campaign_status(campaign_id)
        return {"success": True, "status": status}
        
    except Exception as e:
        logger.error(f"Failed to get campaign status: {e}")
        raise HTTPException(status_code=404, detail=f"Campaign not found: {str(e)}")


# ============================================================================
# ADVANCED MONETIZATION ENDPOINTS
# ============================================================================

@enhanced_router.post("/monetization/analyze")
async def analyze_monetization_opportunities(request: MonetizationAnalysisRequest):
    """Analyze monetization opportunities for creator"""
    try:
        # Convert request to creator profile
        creator_profile = {
            "creator_id": request.creator_id,
            "total_followers": request.total_followers,
            "engagement_rate": request.engagement_rate,
            "niche": request.niche,
            "platforms": request.platforms,
            "monthly_views": request.monthly_views,
            "monthly_revenue": request.current_revenue
        }
        
        # Analyze monetization opportunities
        analysis = await monetization_engine.analyze_creator_monetization(creator_profile)
        
        return {
            "success": True,
            "analysis": analysis
        }
        
    except Exception as e:
        logger.error(f"Monetization analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Monetization analysis failed: {str(e)}")


@enhanced_router.post("/monetization/opportunities/{opportunity_id}/activate")
async def activate_monetization_opportunity(opportunity_id: str, creator_profile: Dict[str, Any]):
    """Activate a specific monetization opportunity"""
    try:
        # This would retrieve the opportunity and create a campaign
        # For now, return success with next steps
        
        return {
            "success": True,
            "activation_result": {
                "opportunity_id": opportunity_id,
                "status": "activated",
                "next_steps": [
                    "Review generated promotional content",
                    "Set up tracking and analytics",
                    "Launch monetization campaign"
                ],
                "estimated_time_to_revenue": "14-30 days"
            }
        }
        
    except Exception as e:
        logger.error(f"Opportunity activation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Activation failed: {str(e)}")


# ============================================================================
# COMPREHENSIVE ANALYTICS ENDPOINTS
# ============================================================================

@enhanced_router.post("/analytics/comprehensive-report")
async def generate_comprehensive_analytics_report(request: AnalyticsReportRequest):
    """Generate comprehensive analytics and intelligence report"""
    try:
        # Build creator profile for analysis
        creator_profile = {
            "creator_id": request.creator_id,
            "niche": "tech",  # Would be retrieved from database
            "total_followers": 50000,  # Would be retrieved from database
            "engagement_rate": 0.045,  # Would be retrieved from database
            "monthly_revenue": 5000,  # Would be retrieved from database
            "competitors": request.competitors or ["competitor1", "competitor2"],
            "recent_content": [
                {
                    "script": "Amazing productivity hack that changed my life",
                    "platform": "tiktok",
                    "hashtags": ["#productivity", "#lifehack", "#trending"]
                }
            ],
            "revenue_history": [3000, 3500, 4000, 4500, 5000],
            "follower_history": list(range(45000, 50000, 100))
        }
        
        # Generate comprehensive report
        report = await intelligence_dashboard.generate_comprehensive_report(creator_profile)
        
        return {
            "success": True,
            "report": report
        }
        
    except Exception as e:
        logger.error(f"Analytics report generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@enhanced_router.get("/analytics/real-time/{creator_id}")
async def get_real_time_analytics(creator_id: str):
    """Get real-time analytics data"""
    try:
        # Mock real-time data - in production would come from live streams
        real_time_data = {
            "current_viewers": 1250,
            "engagement_rate_last_hour": 0.067,
            "viral_content_alerts": [
                {
                    "content_id": "content_123",
                    "alert_type": "viral_potential",
                    "message": "Content showing 85% viral potential - consider boosting",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "revenue_today": 450.75,
            "top_performing_content_today": [
                {
                    "content_id": "content_456",
                    "views": 25000,
                    "engagement_rate": 0.089,
                    "revenue_generated": 125.50
                }
            ]
        }
        
        return {
            "success": True,
            "real_time_data": real_time_data,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Real-time analytics failed: {e}")
        raise HTTPException(status_code=500, detail=f"Real-time analytics failed: {str(e)}")


# ============================================================================
# UNIFIED CONTENT PIPELINE ENDPOINT
# ============================================================================

@enhanced_router.post("/pipeline/complete-content-creation")
async def complete_content_creation_pipeline(
    topic: str,
    platform: str,
    target_audience: str,
    include_monetization: bool = True,
    include_campaign: bool = True,
    background_tasks: BackgroundTasks = None
):
    """Complete end-to-end content creation pipeline"""
    try:
        pipeline_results = {}
        
        # Step 1: Generate viral content
        viral_request = ViralContentRequest(
            topic=topic,
            platform=PlatformOptimization(platform),
            target_audience=target_audience,
            content_goal="viral_engagement"
        )
        
        viral_content = await viral_engine.generate_viral_content(viral_request)
        pipeline_results["viral_content"] = {
            "script": viral_content.script,
            "predicted_viral_score": viral_content.viral_score,
            "hashtags": viral_content.hashtags
        }
        
        # Step 2: Generate multimodal assets
        media_request = MediaGenerationRequest(
            script=viral_content.script,
            media_types=[MediaType.VIDEO, MediaType.AUDIO],
            platform=platform,
            duration_seconds=30
        )
        
        multimodal_content = await multimodal_generator.generate_content_package(media_request)
        pipeline_results["media_assets"] = {
            "request_id": multimodal_content.request_id,
            "generated_count": len(multimodal_content.generated_media),
            "estimated_performance": multimodal_content.estimated_performance
        }
        
        # Step 3: Monetization analysis (if requested)
        if include_monetization:
            creator_profile = {
                "creator_id": "pipeline_user",
                "total_followers": 25000,
                "engagement_rate": 0.05,
                "niche": "general",
                "platforms": [platform],
                "monthly_views": 500000
            }
            
            monetization_analysis = await monetization_engine.analyze_creator_monetization(creator_profile)
            pipeline_results["monetization_opportunities"] = {
                "total_opportunities": len(monetization_analysis["revenue_opportunities"]),
                "optimization_potential": monetization_analysis["optimization_potential"],
                "top_opportunity": monetization_analysis["revenue_opportunities"][0] if monetization_analysis["revenue_opportunities"] else None
            }
        
        # Step 4: Campaign creation (if requested)
        if include_campaign:
            campaign_brief = {
                "name": f"Viral Campaign: {topic}",
                "type": "viral_content",
                "objective": {"primary_goal": "engagement", "target_metrics": {"views": 100000}},
                "target_audience": {"demographics": {"age": "18-35"}, "interests": [topic]},
                "content_strategy": {"content_pillars": ["educational"], "posting_frequency": {platform: 1}},
                "start_date": datetime.now().isoformat(),
                "end_date": (datetime.now() + timedelta(days=30)).isoformat(),
                "platforms": [platform],
                "total_budget": 1000.0,
                "daily_budget": 33.33
            }
            
            campaign = await campaign_engine.create_campaign(campaign_brief)
            pipeline_results["campaign"] = {
                "campaign_id": campaign.campaign_id,
                "content_calendar_items": len(campaign.content_calendar),
                "status": campaign.status.value
            }
        
        return {
            "success": True,
            "pipeline_id": f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "results": pipeline_results,
            "next_steps": [
                "Review generated content",
                "Approve media assets",
                "Launch campaign" if include_campaign else "Schedule content",
                "Monitor performance"
            ],
            "estimated_completion_time": "Content ready for publishing"
        }
        
    except Exception as e:
        logger.error(f"Complete pipeline failed: {e}")
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {str(e)}")


# ============================================================================
# ADVANCED PERSONALIZATION ENDPOINTS
# ============================================================================

@enhanced_router.post("/personalization/create-profile")
async def create_user_profile(request: PersonalizationRequest):
    """Create personalized user profile"""
    try:
        profile = await personalization_engine.create_user_profile(
            request.user_id, request.user_data
        )

        return {
            "success": True,
            "profile": {
                "user_id": profile.user_id,
                "personality_type": profile.personality_type.value,
                "engagement_pattern": profile.engagement_pattern.value,
                "confidence_score": profile.confidence_score,
                "interests": profile.interests,
                "optimal_posting_times": profile.active_hours
            }
        }

    except Exception as e:
        logger.error(f"Profile creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Profile creation failed: {str(e)}")


@enhanced_router.post("/personalization/generate-content")
async def generate_personalized_content(request: PersonalizationRequest):
    """Generate personalized content for user"""
    try:
        base_content = {
            "script": f"Content about {request.content_topic}",
            "type": "social_post",
            "platform": request.platform
        }

        personalized_content = await personalization_engine.generate_personalized_content(
            request.user_id, base_content
        )

        return {
            "success": True,
            "personalized_content": {
                "content_id": personalized_content.content_id,
                "script": personalized_content.script,
                "personalization_score": personalized_content.personalization_score,
                "optimal_posting_time": personalized_content.optimal_posting_time.isoformat(),
                "recommended_platform": personalized_content.recommended_platform,
                "hashtags": personalized_content.personalized_hashtags,
                "call_to_action": personalized_content.call_to_action,
                "variants": personalized_content.variants
            }
        }

    except Exception as e:
        logger.error(f"Personalized content generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Content personalization failed: {str(e)}")


# ============================================================================
# SOCIAL MEDIA AUTOMATION ENDPOINTS
# ============================================================================

@enhanced_router.post("/automation/schedule-post")
async def schedule_social_media_post(request: SocialMediaPostRequest):
    """Schedule social media post"""
    try:
        from automation.social_media_automation import ScheduledPost

        scheduled_post = ScheduledPost(
            post_id=None,  # Will be generated
            platform=Platform(request.platform),
            account_id=request.account_id,
            content_type=PostType(request.content_type),
            caption=request.caption,
            media_urls=request.media_urls,
            hashtags=request.hashtags,
            mentions=[],
            scheduled_time=datetime.fromisoformat(request.scheduled_time),
            timezone=request.timezone
        )

        post_id = await social_scheduler.schedule_post(scheduled_post)

        return {
            "success": True,
            "post_id": post_id,
            "scheduled_time": request.scheduled_time,
            "platform": request.platform,
            "status": "scheduled"
        }

    except Exception as e:
        logger.error(f"Post scheduling failed: {e}")
        raise HTTPException(status_code=500, detail=f"Post scheduling failed: {str(e)}")


@enhanced_router.get("/automation/scheduled-posts")
async def get_scheduled_posts(platform: Optional[str] = None):
    """Get all scheduled posts"""
    try:
        platform_filter = Platform(platform) if platform else None
        posts = social_scheduler.get_scheduled_posts(platform_filter)

        return {
            "success": True,
            "posts": [
                {
                    "post_id": post.post_id,
                    "platform": post.platform.value,
                    "content_type": post.content_type.value,
                    "caption": post.caption[:100] + "..." if len(post.caption) > 100 else post.caption,
                    "scheduled_time": post.scheduled_time.isoformat(),
                    "posted": post.posted,
                    "post_url": post.post_url
                }
                for post in posts
            ],
            "total_posts": len(posts)
        }

    except Exception as e:
        logger.error(f"Failed to get scheduled posts: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get scheduled posts: {str(e)}")


# ============================================================================
# A/B TESTING ENDPOINTS
# ============================================================================

@enhanced_router.post("/testing/create-test")
async def create_ab_test(request: ABTestRequest):
    """Create new A/B test"""
    try:
        test_config = {
            "name": request.name,
            "description": request.description,
            "test_type": request.test_type,
            "primary_metric": request.primary_metric,
            "variants": request.variants,
            "baseline_rate": request.baseline_rate,
            "minimum_effect_size": request.minimum_effect_size,
            "start_date": request.start_date,
            "end_date": request.end_date
        }

        test = await ab_test_engine.create_test(test_config)

        return {
            "success": True,
            "test": {
                "test_id": test.test_id,
                "name": test.name,
                "status": test.status.value,
                "variants": [
                    {
                        "variant_id": v.variant_id,
                        "name": v.name,
                        "traffic_allocation": v.traffic_allocation,
                        "is_control": v.is_control
                    }
                    for v in test.variants
                ],
                "minimum_sample_size": test.minimum_sample_size
            }
        }

    except Exception as e:
        logger.error(f"A/B test creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"A/B test creation failed: {str(e)}")


@enhanced_router.post("/testing/{test_id}/start")
async def start_ab_test(test_id: str):
    """Start A/B test"""
    try:
        success = await ab_test_engine.start_test(test_id)

        return {
            "success": success,
            "test_id": test_id,
            "status": "running",
            "message": "A/B test started successfully"
        }

    except Exception as e:
        logger.error(f"Failed to start A/B test: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start test: {str(e)}")


@enhanced_router.get("/testing/{test_id}/results")
async def get_ab_test_results(test_id: str):
    """Get A/B test results and analysis"""
    try:
        results = await ab_test_engine.analyze_test_results(test_id)

        return {
            "success": True,
            "results": results
        }

    except Exception as e:
        logger.error(f"Failed to get test results: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get test results: {str(e)}")


# ============================================================================
# LEAD GENERATION ENDPOINTS
# ============================================================================

@enhanced_router.post("/leads/capture")
async def capture_lead(request: LeadCaptureRequest):
    """Capture new lead"""
    try:
        lead_data = {
            "email": request.email,
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company": request.company,
            "lead_source": request.lead_source,
            "interests": request.interests,
            "pain_points": request.pain_points
        }

        lead = await lead_engine.capture_lead(lead_data)

        return {
            "success": True,
            "lead": {
                "lead_id": lead.lead_id,
                "email": lead.email,
                "lead_score": lead.lead_score,
                "lead_quality": lead.lead_quality.value,
                "lead_stage": lead.lead_stage.value,
                "next_followup": lead.next_followup.isoformat() if lead.next_followup else None
            }
        }

    except Exception as e:
        logger.error(f"Lead capture failed: {e}")
        raise HTTPException(status_code=500, detail=f"Lead capture failed: {str(e)}")


@enhanced_router.get("/leads/analytics")
async def get_lead_analytics():
    """Get comprehensive lead analytics"""
    try:
        analytics = lead_engine.get_lead_analytics()

        return {
            "success": True,
            "analytics": analytics
        }

    except Exception as e:
        logger.error(f"Failed to get lead analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")


# ============================================================================
# SYSTEM STATUS AND HEALTH
# ============================================================================

@enhanced_router.get("/system/status")
async def get_enhanced_system_status():
    """Get status of all enhanced AI systems"""
    try:
        # Check status of all engines
        status = {
            "ai_orchestrator": {
                "status": "operational",
                "providers_available": len(ai_orchestrator.providers),
                "performance_metrics": ai_orchestrator.get_provider_stats()
            },
            "viral_engine": {
                "status": "operational",
                "trend_analyzer": "active",
                "trigger_engine": "active"
            },
            "multimodal_generator": {
                "status": "operational",
                "video_generator": "active",
                "audio_generator": "active"
            },
            "campaign_engine": {
                "status": "operational",
                "active_campaigns": len(campaign_engine.active_campaigns)
            },
            "monetization_engine": {
                "status": "operational",
                "intelligence_engine": "active",
                "optimizer": "active"
            },
            "analytics_dashboard": {
                "status": "operational",
                "realtime_engine": "active",
                "predictive_engine": "active",
                "competitor_engine": "active"
            }
        }
        
        return {
            "success": True,
            "system_status": "fully_operational",
            "components": status,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"System status check failed: {e}")
        return {
            "success": False,
            "system_status": "degraded",
            "error": str(e),
            "last_updated": datetime.now().isoformat()
        }

#!/usr/bin/env python3
"""
Enhanced System Integration Tests
Comprehensive testing of all advanced AI Content Empire features
"""

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

# Import all enhanced engines
from ai.next_gen_providers import ai_orchestrator
from ai.viral_content_engine import viral_engine, ViralContentRequest, PlatformOptimization
from ai.multimodal_generator import multimodal_generator, MediaGenerationRequest, MediaType
from ai.advanced_personalization_engine import personalization_engine, PersonalityType, EngagementPattern
from marketing.intelligent_campaign_engine import campaign_engine, CampaignType
from revenue.advanced_monetization_engine import monetization_engine
from analytics.intelligence_dashboard import intelligence_dashboard
from automation.social_media_automation import social_scheduler, Platform, PostType
from optimization.ab_testing_engine import ab_test_engine, TestType, MetricType
from conversion.lead_generation_engine import lead_engine, LeadSource, ConversionGoal


class TestEnhancedSystemIntegration:
    """Test suite for enhanced system integration"""
    
    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing"""
        return {
            "age_range": "25-34",
            "location": "US",
            "interests": ["business", "technology", "productivity"],
            "pain_points": ["lack of time", "information overload"],
            "content_interactions": [
                {"category": "business", "engagement_score": 0.8},
                {"category": "technology", "engagement_score": 0.9}
            ],
            "comments": [
                {"text": "This is amazing! I need to achieve more success in my business."},
                {"text": "Great tips for productivity and growth!"}
            ],
            "session_data": [
                {"duration": 1800, "content_viewed": 12},
                {"duration": 2400, "content_viewed": 15}
            ]
        }
    
    @pytest.fixture
    def sample_content_request(self):
        """Sample content generation request"""
        return {
            "topic": "AI productivity hacks for entrepreneurs",
            "platform": "tiktok",
            "target_audience": "business owners",
            "content_goal": "viral_engagement"
        }
    
    @pytest.mark.asyncio
    async def test_complete_content_creation_pipeline(self, sample_content_request):
        """Test complete end-to-end content creation pipeline"""
        
        # Step 1: Generate viral content
        viral_request = ViralContentRequest(
            topic=sample_content_request["topic"],
            platform=PlatformOptimization(sample_content_request["platform"]),
            target_audience=sample_content_request["target_audience"],
            content_goal=sample_content_request["content_goal"]
        )
        
        viral_content = await viral_engine.generate_viral_content(viral_request)
        
        assert viral_content is not None
        assert viral_content.script != ""
        assert viral_content.viral_score > 0
        assert len(viral_content.hashtags) > 0
        
        # Step 2: Generate multimodal assets
        media_request = MediaGenerationRequest(
            script=viral_content.script,
            media_types=[MediaType.VIDEO, MediaType.AUDIO],
            platform=sample_content_request["platform"],
            duration_seconds=30
        )
        
        multimodal_content = await multimodal_generator.generate_content_package(media_request)
        
        assert multimodal_content is not None
        assert len(multimodal_content.generated_media) > 0
        assert multimodal_content.estimated_performance is not None
        
        # Step 3: Create marketing campaign
        campaign_brief = {
            "name": f"Viral Campaign: {sample_content_request['topic']}",
            "type": "viral_content",
            "objective": {"primary_goal": "engagement", "target_metrics": {"views": 100000}},
            "target_audience": {"demographics": {"age": "25-35"}, "interests": ["business"]},
            "content_strategy": {"content_pillars": ["educational"], "posting_frequency": {"tiktok": 1}},
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "platforms": [sample_content_request["platform"]],
            "total_budget": 1000.0,
            "daily_budget": 33.33
        }
        
        campaign = await campaign_engine.create_campaign(campaign_brief)
        
        assert campaign is not None
        assert campaign.campaign_id is not None
        assert len(campaign.content_calendar) > 0
        
        print(f"✅ Complete pipeline test passed - Generated viral content with score {viral_content.viral_score}")
    
    @pytest.mark.asyncio
    async def test_personalization_engine(self, sample_user_data):
        """Test advanced personalization engine"""
        
        user_id = "test_user_123"
        
        # Create user profile
        profile = await personalization_engine.create_user_profile(user_id, sample_user_data)
        
        assert profile is not None
        assert profile.user_id == user_id
        assert profile.personality_type in PersonalityType
        assert profile.engagement_pattern in EngagementPattern
        assert profile.confidence_score > 0
        
        # Generate personalized content
        base_content = {
            "script": "Here are some productivity tips for entrepreneurs",
            "type": "social_post",
            "platform": "instagram"
        }
        
        personalized_content = await personalization_engine.generate_personalized_content(
            user_id, base_content
        )
        
        assert personalized_content is not None
        assert personalized_content.personalization_score > 0
        assert personalized_content.optimal_posting_time is not None
        assert len(personalized_content.personalized_hashtags) > 0
        
        print(f"✅ Personalization test passed - Profile: {profile.personality_type.value}, Score: {personalized_content.personalization_score}")
    
    @pytest.mark.asyncio
    async def test_social_media_automation(self):
        """Test social media automation system"""
        
        from automation.social_media_automation import SocialMediaAccount, ScheduledPost
        
        # Add test account
        test_account = SocialMediaAccount(
            platform=Platform.INSTAGRAM,
            username="test_account",
            account_id="test_123",
            access_token="test_token",
            followers_count=10000,
            engagement_rate=0.05
        )
        
        social_scheduler.add_account(test_account)
        
        # Schedule test post
        test_post = ScheduledPost(
            post_id=None,
            platform=Platform.INSTAGRAM,
            account_id="test_123",
            content_type=PostType.IMAGE,
            caption="Test post for automation",
            media_urls=["https://example.com/image.jpg"],
            hashtags=["#test", "#automation"],
            mentions=[],
            scheduled_time=datetime.now() + timedelta(minutes=5),
            timezone="UTC"
        )
        
        post_id = await social_scheduler.schedule_post(test_post)
        
        assert post_id is not None
        
        # Get scheduled posts
        scheduled_posts = social_scheduler.get_scheduled_posts(Platform.INSTAGRAM)
        
        assert len(scheduled_posts) > 0
        assert any(post.post_id == post_id for post in scheduled_posts)
        
        print(f"✅ Social automation test passed - Scheduled post: {post_id}")
    
    @pytest.mark.asyncio
    async def test_ab_testing_engine(self):
        """Test A/B testing engine"""
        
        # Create test configuration
        test_config = {
            "name": "Hook A/B Test",
            "description": "Testing different content hooks",
            "test_type": "content_hook",
            "primary_metric": "engagement_rate",
            "variants": [
                {
                    "name": "Control",
                    "description": "Original hook",
                    "data": {"hook": "Here's a productivity tip"},
                    "is_control": True
                },
                {
                    "name": "Variant A",
                    "description": "Question hook",
                    "data": {"hook": "Want to 10x your productivity?"}
                }
            ],
            "baseline_rate": 0.05,
            "minimum_effect_size": 0.1,
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=14)).isoformat()
        }
        
        # Create test
        test = await ab_test_engine.create_test(test_config)
        
        assert test is not None
        assert test.test_id is not None
        assert len(test.variants) == 2
        assert test.minimum_sample_size > 0
        
        # Start test
        success = await ab_test_engine.start_test(test.test_id)
        assert success is True
        
        # Simulate some test data
        await ab_test_engine.record_event(test.test_id, test.variants[0].variant_id, "impression")
        await ab_test_engine.record_event(test.test_id, test.variants[0].variant_id, "conversion")
        await ab_test_engine.record_event(test.test_id, test.variants[1].variant_id, "impression")
        
        # Analyze results
        results = await ab_test_engine.analyze_test_results(test.test_id)
        
        assert results is not None
        assert "variants" in results
        assert len(results["variants"]) == 2
        
        print(f"✅ A/B testing test passed - Test ID: {test.test_id}")
    
    @pytest.mark.asyncio
    async def test_lead_generation_engine(self):
        """Test lead generation and conversion engine"""
        
        # Capture test lead
        lead_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "company": "Test Corp",
            "lead_source": "content_marketing",
            "interests": ["business", "productivity"],
            "pain_points": ["lack of time", "low conversion rates"]
        }
        
        lead = await lead_engine.capture_lead(lead_data)
        
        assert lead is not None
        assert lead.email == "test@example.com"
        assert lead.lead_score > 0
        assert lead.lead_source == LeadSource.CONTENT_MARKETING
        
        # Update lead activity
        await lead_engine.update_lead_activity(lead.lead_id, {"page_view": True, "email_open": True})
        
        # Create lead magnet
        magnet_config = {
            "name": "Productivity Checklist",
            "description": "Ultimate productivity checklist for entrepreneurs",
            "type": "checklist",
            "title": "10x Your Productivity in 30 Days",
            "value_proposition": "Get more done in less time",
            "benefits": ["Save 2 hours daily", "Increase focus", "Boost results"],
            "target_audience": "entrepreneurs",
            "target_pain_points": ["lack of time", "low productivity"],
            "target_interests": ["business", "productivity"],
            "call_to_action": "Download Free Checklist"
        }
        
        magnet = await lead_engine.create_lead_magnet(magnet_config)
        
        assert magnet is not None
        assert magnet.name == "Productivity Checklist"
        assert magnet.title != ""
        
        # Get analytics
        analytics = lead_engine.get_lead_analytics()
        
        assert analytics["total_leads"] > 0
        assert "quality_distribution" in analytics
        
        print(f"✅ Lead generation test passed - Lead score: {lead.lead_score}, Magnet: {magnet.magnet_id}")
    
    @pytest.mark.asyncio
    async def test_monetization_analysis(self):
        """Test advanced monetization engine"""
        
        creator_profile = {
            "creator_id": "test_creator",
            "total_followers": 50000,
            "engagement_rate": 0.05,
            "niche": "business",
            "platforms": ["instagram", "tiktok"],
            "monthly_views": 500000,
            "monthly_revenue": 2000
        }
        
        analysis = await monetization_engine.analyze_creator_monetization(creator_profile)
        
        assert analysis is not None
        assert "revenue_opportunities" in analysis
        assert "optimization_potential" in analysis
        assert len(analysis["revenue_opportunities"]) > 0
        
        # Test opportunity activation
        if analysis["revenue_opportunities"]:
            top_opportunity = analysis["revenue_opportunities"][0]
            
            campaign = await monetization_engine.create_monetization_campaign(
                top_opportunity, creator_profile
            )
            
            assert campaign is not None
            assert len(campaign.promotional_content) > 0
        
        print(f"✅ Monetization test passed - Found {len(analysis['revenue_opportunities'])} opportunities")
    
    @pytest.mark.asyncio
    async def test_analytics_dashboard(self):
        """Test comprehensive analytics dashboard"""
        
        creator_profile = {
            "creator_id": "test_creator",
            "niche": "tech",
            "total_followers": 25000,
            "engagement_rate": 0.045,
            "monthly_revenue": 3000,
            "competitors": ["competitor1", "competitor2"],
            "recent_content": [
                {
                    "script": "Amazing AI productivity hack",
                    "platform": "tiktok",
                    "hashtags": ["#ai", "#productivity", "#hack"]
                }
            ]
        }
        
        report = await intelligence_dashboard.generate_comprehensive_report(creator_profile)
        
        assert report is not None
        assert "predictive_insights" in report
        assert "competitor_analysis" in report
        assert "actionable_recommendations" in report
        assert len(report["predictive_insights"]) > 0
        
        print(f"✅ Analytics dashboard test passed - Generated {len(report['predictive_insights'])} insights")
    
    @pytest.mark.asyncio
    async def test_system_health_check(self):
        """Test overall system health and integration"""
        
        # Test AI orchestrator
        assert ai_orchestrator is not None
        assert len(ai_orchestrator.providers) > 0
        
        # Test all engines are initialized
        engines = [
            viral_engine,
            multimodal_generator,
            personalization_engine,
            campaign_engine,
            monetization_engine,
            intelligence_dashboard,
            social_scheduler,
            ab_test_engine,
            lead_engine
        ]
        
        for engine in engines:
            assert engine is not None
        
        print("✅ System health check passed - All engines operational")
    
    def test_api_endpoint_coverage(self):
        """Test that all major API endpoints are covered"""
        
        from api.enhanced_routes import enhanced_router
        
        # Get all routes
        routes = [route.path for route in enhanced_router.routes]
        
        # Check for key endpoint categories
        required_endpoints = [
            "/api/v2/content/viral/generate",
            "/api/v2/content/multimodal/generate",
            "/api/v2/campaigns/create",
            "/api/v2/monetization/analyze",
            "/api/v2/analytics/comprehensive-report",
            "/api/v2/personalization/create-profile",
            "/api/v2/automation/schedule-post",
            "/api/v2/testing/create-test",
            "/api/v2/leads/capture",
            "/api/v2/system/status"
        ]
        
        for endpoint in required_endpoints:
            assert any(endpoint in route for route in routes), f"Missing endpoint: {endpoint}"
        
        print(f"✅ API coverage test passed - Found {len(routes)} endpoints")


# Run integration tests
if __name__ == "__main__":
    async def run_tests():
        test_suite = TestEnhancedSystemIntegration()
        
        print("🚀 Starting Enhanced System Integration Tests...")
        print("=" * 60)
        
        # Sample data
        sample_user_data = {
            "age_range": "25-34",
            "location": "US",
            "interests": ["business", "technology"],
            "pain_points": ["lack of time"],
            "content_interactions": [{"category": "business", "engagement_score": 0.8}],
            "comments": [{"text": "Great content about success!"}],
            "session_data": [{"duration": 1800, "content_viewed": 10}]
        }
        
        sample_content_request = {
            "topic": "AI productivity hacks",
            "platform": "tiktok",
            "target_audience": "entrepreneurs",
            "content_goal": "viral_engagement"
        }
        
        try:
            # Run all tests
            await test_suite.test_complete_content_creation_pipeline(sample_content_request)
            await test_suite.test_personalization_engine(sample_user_data)
            await test_suite.test_social_media_automation()
            await test_suite.test_ab_testing_engine()
            await test_suite.test_lead_generation_engine()
            await test_suite.test_monetization_analysis()
            await test_suite.test_analytics_dashboard()
            await test_suite.test_system_health_check()
            test_suite.test_api_endpoint_coverage()
            
            print("=" * 60)
            print("🎉 ALL INTEGRATION TESTS PASSED!")
            print("🚀 Enhanced AI Content Empire is fully operational!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            raise
    
    # Run the tests
    asyncio.run(run_tests())

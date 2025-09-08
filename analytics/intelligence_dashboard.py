#!/usr/bin/env python3
"""
Comprehensive Analytics & Intelligence Dashboard
Real-time analytics, predictive insights, and competitive intelligence
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
import pandas as pd
from collections import defaultdict

from ai.next_gen_providers import ai_orchestrator, AIRequest, ContentType

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of analytics metrics"""
    ENGAGEMENT = "engagement"
    REACH = "reach"
    CONVERSION = "conversion"
    REVENUE = "revenue"
    GROWTH = "growth"
    RETENTION = "retention"
    VIRAL = "viral"
    SENTIMENT = "sentiment"


class AnalyticsTimeframe(Enum):
    """Analytics timeframes"""
    REAL_TIME = "real_time"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class PredictionType(Enum):
    """Types of predictions"""
    VIRAL_POTENTIAL = "viral_potential"
    REVENUE_FORECAST = "revenue_forecast"
    GROWTH_PROJECTION = "growth_projection"
    ENGAGEMENT_PREDICTION = "engagement_prediction"
    TREND_PREDICTION = "trend_prediction"
    COMPETITOR_ANALYSIS = "competitor_analysis"


@dataclass
class AnalyticsMetric:
    """Individual analytics metric"""
    metric_id: str
    metric_type: MetricType
    name: str
    value: float
    previous_value: float
    change_percentage: float
    timeframe: AnalyticsTimeframe
    timestamp: datetime
    
    # Context data
    platform: str
    content_id: Optional[str] = None
    campaign_id: Optional[str] = None
    
    # Benchmarking
    industry_benchmark: Optional[float] = None
    percentile_rank: Optional[float] = None


@dataclass
class PredictiveInsight:
    """Predictive analytics insight"""
    insight_id: str
    prediction_type: PredictionType
    title: str
    description: str
    confidence_score: float
    
    # Prediction data
    predicted_value: float
    prediction_timeframe: int  # days
    factors_influencing: List[str]
    
    # Actionable recommendations
    recommendations: List[str]
    potential_impact: Dict[str, float]
    
    # Metadata
    generated_timestamp: datetime
    expires_at: datetime


@dataclass
class CompetitorIntelligence:
    """Competitor analysis data"""
    competitor_id: str
    competitor_name: str
    analysis_date: datetime
    
    # Performance metrics
    estimated_followers: int
    estimated_engagement_rate: float
    estimated_monthly_revenue: float
    content_frequency: int
    
    # Content analysis
    top_performing_content: List[Dict[str, Any]]
    content_themes: List[str]
    posting_patterns: Dict[str, Any]
    
    # Strategic insights
    competitive_advantages: List[str]
    opportunities: List[str]
    threats: List[str]


class RealTimeAnalyticsEngine:
    """Real-time analytics processing engine"""
    
    def __init__(self):
        self.metric_buffer = defaultdict(list)
        self.alert_thresholds = self._load_alert_thresholds()
        self.streaming_metrics = {}
    
    def _load_alert_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Load alert thresholds for different metrics"""
        return {
            "engagement_rate": {"low": 0.02, "high": 0.15},
            "viral_score": {"low": 0.3, "high": 0.8},
            "conversion_rate": {"low": 0.01, "high": 0.1},
            "revenue_per_day": {"low": 100, "high": 10000},
            "follower_growth_rate": {"low": 0.001, "high": 0.05}
        }
    
    async def process_real_time_data(self, data_point: Dict[str, Any]) -> List[AnalyticsMetric]:
        """Process incoming real-time data"""
        metrics = []
        
        # Extract metrics from data point
        platform = data_point.get("platform", "unknown")
        timestamp = datetime.fromisoformat(data_point.get("timestamp", datetime.now().isoformat()))
        
        # Process engagement metrics
        if "likes" in data_point and "views" in data_point:
            engagement_rate = data_point["likes"] / max(data_point["views"], 1)
            
            metric = AnalyticsMetric(
                metric_id=f"eng_{uuid.uuid4().hex[:8]}",
                metric_type=MetricType.ENGAGEMENT,
                name="engagement_rate",
                value=engagement_rate,
                previous_value=self._get_previous_value("engagement_rate", platform),
                change_percentage=self._calculate_change_percentage(
                    engagement_rate, 
                    self._get_previous_value("engagement_rate", platform)
                ),
                timeframe=AnalyticsTimeframe.REAL_TIME,
                timestamp=timestamp,
                platform=platform,
                content_id=data_point.get("content_id")
            )
            
            metrics.append(metric)
            
            # Check for alerts
            await self._check_alerts(metric)
        
        # Process reach metrics
        if "views" in data_point:
            reach_metric = AnalyticsMetric(
                metric_id=f"reach_{uuid.uuid4().hex[:8]}",
                metric_type=MetricType.REACH,
                name="views",
                value=float(data_point["views"]),
                previous_value=self._get_previous_value("views", platform),
                change_percentage=self._calculate_change_percentage(
                    float(data_point["views"]),
                    self._get_previous_value("views", platform)
                ),
                timeframe=AnalyticsTimeframe.REAL_TIME,
                timestamp=timestamp,
                platform=platform,
                content_id=data_point.get("content_id")
            )
            
            metrics.append(reach_metric)
        
        # Store metrics for trend analysis
        for metric in metrics:
            self.metric_buffer[f"{metric.name}_{metric.platform}"].append(metric)
            
            # Keep only recent metrics (last 1000 data points)
            if len(self.metric_buffer[f"{metric.name}_{metric.platform}"]) > 1000:
                self.metric_buffer[f"{metric.name}_{metric.platform}"].pop(0)
        
        return metrics
    
    def _get_previous_value(self, metric_name: str, platform: str) -> float:
        """Get previous value for comparison"""
        key = f"{metric_name}_{platform}"
        if key in self.metric_buffer and self.metric_buffer[key]:
            return self.metric_buffer[key][-1].value
        return 0.0
    
    def _calculate_change_percentage(self, current: float, previous: float) -> float:
        """Calculate percentage change"""
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return ((current - previous) / previous) * 100
    
    async def _check_alerts(self, metric: AnalyticsMetric):
        """Check if metric triggers any alerts"""
        thresholds = self.alert_thresholds.get(metric.name, {})
        
        if "low" in thresholds and metric.value < thresholds["low"]:
            await self._trigger_alert("low_performance", metric)
        elif "high" in thresholds and metric.value > thresholds["high"]:
            await self._trigger_alert("high_performance", metric)
    
    async def _trigger_alert(self, alert_type: str, metric: AnalyticsMetric):
        """Trigger performance alert"""
        logger.info(f"Alert triggered: {alert_type} for {metric.name} = {metric.value}")
        
        # In production, this would send notifications, webhooks, etc.
        alert_data = {
            "alert_type": alert_type,
            "metric": asdict(metric),
            "timestamp": datetime.now().isoformat(),
            "severity": "high" if alert_type == "low_performance" else "info"
        }
        
        # Store alert for dashboard display
        # await self.store_alert(alert_data)


class PredictiveAnalyticsEngine:
    """Advanced predictive analytics using AI"""
    
    def __init__(self):
        self.prediction_models = {}
        self.historical_data = defaultdict(list)
    
    async def generate_viral_prediction(self, content_data: Dict[str, Any]) -> PredictiveInsight:
        """Predict viral potential of content"""
        
        # Analyze content features
        content_features = await self._extract_content_features(content_data)
        
        # Calculate viral score using multiple factors
        viral_score = await self._calculate_viral_score(content_features)
        
        # Generate insight
        insight = PredictiveInsight(
            insight_id=f"viral_{uuid.uuid4().hex[:8]}",
            prediction_type=PredictionType.VIRAL_POTENTIAL,
            title=f"Viral Potential: {viral_score:.1%}",
            description=f"This content has a {viral_score:.1%} chance of going viral based on current trends and engagement patterns.",
            confidence_score=0.85,
            predicted_value=viral_score,
            prediction_timeframe=7,  # 7 days
            factors_influencing=[
                "Trending topic alignment",
                "Optimal posting time",
                "High engagement hook",
                "Platform algorithm compatibility"
            ],
            recommendations=await self._generate_viral_recommendations(content_features, viral_score),
            potential_impact={
                "estimated_views": viral_score * 1000000,
                "estimated_engagement": viral_score * 50000,
                "estimated_revenue": viral_score * 5000
            },
            generated_timestamp=datetime.now(),
            expires_at=datetime.now() + timedelta(days=7)
        )
        
        return insight
    
    async def generate_revenue_forecast(self, historical_revenue: List[float], 
                                      timeframe_days: int = 30) -> PredictiveInsight:
        """Generate revenue forecast"""
        
        if len(historical_revenue) < 7:
            # Not enough data for accurate prediction
            predicted_revenue = sum(historical_revenue) / len(historical_revenue) * timeframe_days
            confidence = 0.3
        else:
            # Use trend analysis for prediction
            predicted_revenue = await self._forecast_revenue_trend(historical_revenue, timeframe_days)
            confidence = 0.8
        
        insight = PredictiveInsight(
            insight_id=f"revenue_{uuid.uuid4().hex[:8]}",
            prediction_type=PredictionType.REVENUE_FORECAST,
            title=f"Revenue Forecast: ${predicted_revenue:,.2f}",
            description=f"Predicted revenue for the next {timeframe_days} days based on current trends.",
            confidence_score=confidence,
            predicted_value=predicted_revenue,
            prediction_timeframe=timeframe_days,
            factors_influencing=[
                "Historical performance trends",
                "Seasonal patterns",
                "Content pipeline strength",
                "Market conditions"
            ],
            recommendations=await self._generate_revenue_recommendations(predicted_revenue, historical_revenue),
            potential_impact={
                "revenue_growth": predicted_revenue - (sum(historical_revenue[-7:]) / 7 * timeframe_days),
                "confidence_interval": predicted_revenue * 0.2
            },
            generated_timestamp=datetime.now(),
            expires_at=datetime.now() + timedelta(days=timeframe_days)
        )
        
        return insight
    
    async def generate_growth_projection(self, follower_history: List[int]) -> PredictiveInsight:
        """Generate follower growth projection"""
        
        if len(follower_history) < 14:
            growth_rate = 0.02  # Default 2% weekly growth
            confidence = 0.4
        else:
            growth_rate = await self._calculate_growth_rate(follower_history)
            confidence = 0.75
        
        current_followers = follower_history[-1] if follower_history else 1000
        projected_followers = current_followers * (1 + growth_rate) ** 4  # 4 weeks
        
        insight = PredictiveInsight(
            insight_id=f"growth_{uuid.uuid4().hex[:8]}",
            prediction_type=PredictionType.GROWTH_PROJECTION,
            title=f"Growth Projection: {projected_followers:,.0f} followers",
            description=f"Projected to reach {projected_followers:,.0f} followers in 30 days at current growth rate of {growth_rate:.1%} per week.",
            confidence_score=confidence,
            predicted_value=projected_followers,
            prediction_timeframe=30,
            factors_influencing=[
                "Content consistency",
                "Engagement quality",
                "Platform algorithm changes",
                "Trending topic participation"
            ],
            recommendations=await self._generate_growth_recommendations(growth_rate, current_followers),
            potential_impact={
                "follower_increase": projected_followers - current_followers,
                "engagement_potential": (projected_followers - current_followers) * 0.03
            },
            generated_timestamp=datetime.now(),
            expires_at=datetime.now() + timedelta(days=30)
        )
        
        return insight
    
    async def _extract_content_features(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from content for analysis"""
        features = {
            "has_trending_hashtags": len([tag for tag in content_data.get("hashtags", []) if "trending" in tag.lower()]) > 0,
            "optimal_length": 15 <= len(content_data.get("script", "").split()) <= 100,
            "has_hook": content_data.get("hook", "") != "",
            "platform_optimized": content_data.get("platform") in ["tiktok", "instagram", "youtube"],
            "emotional_intensity": len([word for word in content_data.get("script", "").lower().split() 
                                      if word in ["amazing", "incredible", "shocking", "unbelievable"]]) > 0,
            "call_to_action": "follow" in content_data.get("script", "").lower() or "subscribe" in content_data.get("script", "").lower()
        }
        
        return features
    
    async def _calculate_viral_score(self, features: Dict[str, Any]) -> float:
        """Calculate viral potential score"""
        base_score = 0.1
        
        # Feature-based scoring
        if features.get("has_trending_hashtags"):
            base_score += 0.2
        if features.get("optimal_length"):
            base_score += 0.15
        if features.get("has_hook"):
            base_score += 0.25
        if features.get("platform_optimized"):
            base_score += 0.1
        if features.get("emotional_intensity"):
            base_score += 0.15
        if features.get("call_to_action"):
            base_score += 0.05
        
        return min(base_score, 0.9)  # Cap at 90%
    
    async def _forecast_revenue_trend(self, historical_revenue: List[float], days: int) -> float:
        """Forecast revenue using trend analysis"""
        # Simple linear trend analysis
        if len(historical_revenue) >= 7:
            recent_avg = sum(historical_revenue[-7:]) / 7
            older_avg = sum(historical_revenue[-14:-7]) / 7 if len(historical_revenue) >= 14 else recent_avg
            
            growth_rate = (recent_avg - older_avg) / older_avg if older_avg > 0 else 0
            
            # Project forward
            daily_revenue = recent_avg
            total_forecast = 0
            
            for day in range(days):
                daily_revenue *= (1 + growth_rate / 7)  # Weekly growth rate applied daily
                total_forecast += daily_revenue
            
            return total_forecast
        
        return sum(historical_revenue) / len(historical_revenue) * days
    
    async def _calculate_growth_rate(self, follower_history: List[int]) -> float:
        """Calculate follower growth rate"""
        if len(follower_history) < 2:
            return 0.02  # Default 2% growth
        
        # Calculate weekly growth rates
        weekly_rates = []
        for i in range(7, len(follower_history), 7):
            if i < len(follower_history):
                current_week = follower_history[i]
                previous_week = follower_history[i-7]
                if previous_week > 0:
                    rate = (current_week - previous_week) / previous_week
                    weekly_rates.append(rate)
        
        if weekly_rates:
            return sum(weekly_rates) / len(weekly_rates)
        
        # Fallback to overall growth rate
        start_followers = follower_history[0]
        end_followers = follower_history[-1]
        weeks = len(follower_history) / 7
        
        if start_followers > 0 and weeks > 0:
            return ((end_followers / start_followers) ** (1/weeks)) - 1
        
        return 0.02
    
    async def _generate_viral_recommendations(self, features: Dict[str, Any], viral_score: float) -> List[str]:
        """Generate recommendations to improve viral potential"""
        recommendations = []
        
        if not features.get("has_trending_hashtags"):
            recommendations.append("Add trending hashtags to increase discoverability")
        
        if not features.get("optimal_length"):
            recommendations.append("Optimize content length for platform algorithm")
        
        if not features.get("has_hook"):
            recommendations.append("Add a compelling hook in the first 3 seconds")
        
        if viral_score < 0.5:
            recommendations.append("Consider incorporating current trending topics")
            recommendations.append("Add more emotional triggers to increase engagement")
        
        return recommendations
    
    async def _generate_revenue_recommendations(self, predicted_revenue: float, 
                                              historical_revenue: List[float]) -> List[str]:
        """Generate revenue optimization recommendations"""
        recommendations = []
        
        if len(historical_revenue) > 7:
            recent_trend = sum(historical_revenue[-7:]) / 7 - sum(historical_revenue[-14:-7]) / 7
            
            if recent_trend < 0:
                recommendations.append("Revenue is declining - consider new monetization strategies")
                recommendations.append("Analyze top-performing content and create similar pieces")
            elif recent_trend > 0:
                recommendations.append("Revenue is growing - scale successful strategies")
                recommendations.append("Consider premium offerings for engaged audience")
        
        if predicted_revenue < 1000:
            recommendations.append("Focus on building audience before heavy monetization")
            recommendations.append("Prioritize engagement and value creation")
        
        return recommendations
    
    async def _generate_growth_recommendations(self, growth_rate: float, current_followers: int) -> List[str]:
        """Generate growth optimization recommendations"""
        recommendations = []
        
        if growth_rate < 0.01:  # Less than 1% weekly growth
            recommendations.append("Increase posting frequency to boost visibility")
            recommendations.append("Engage more actively with your community")
            recommendations.append("Collaborate with other creators in your niche")
        
        if current_followers < 10000:
            recommendations.append("Focus on niche-specific content to attract targeted followers")
            recommendations.append("Use platform-specific features (Stories, Reels, Shorts)")
        
        if growth_rate > 0.05:  # More than 5% weekly growth
            recommendations.append("Maintain current strategy - it's working well!")
            recommendations.append("Consider monetization opportunities for growing audience")
        
        return recommendations


class CompetitorAnalysisEngine:
    """Competitive intelligence and analysis"""
    
    def __init__(self):
        self.competitor_database = {}
        self.analysis_cache = {}
    
    async def analyze_competitor(self, competitor_name: str, niche: str) -> CompetitorIntelligence:
        """Analyze competitor performance and strategy"""
        
        # In production, this would scrape public data from social platforms
        # For now, we'll generate realistic mock data
        
        competitor_data = await self._gather_competitor_data(competitor_name, niche)
        
        analysis = CompetitorIntelligence(
            competitor_id=f"comp_{uuid.uuid4().hex[:8]}",
            competitor_name=competitor_name,
            analysis_date=datetime.now(),
            estimated_followers=competitor_data["followers"],
            estimated_engagement_rate=competitor_data["engagement_rate"],
            estimated_monthly_revenue=competitor_data["monthly_revenue"],
            content_frequency=competitor_data["posts_per_week"],
            top_performing_content=competitor_data["top_content"],
            content_themes=competitor_data["themes"],
            posting_patterns=competitor_data["posting_patterns"],
            competitive_advantages=await self._identify_competitive_advantages(competitor_data),
            opportunities=await self._identify_opportunities(competitor_data, niche),
            threats=await self._identify_threats(competitor_data)
        )
        
        return analysis
    
    async def _gather_competitor_data(self, competitor_name: str, niche: str) -> Dict[str, Any]:
        """Gather competitor data from various sources"""
        # Mock data generation - in production would use real APIs
        
        base_followers = {"tech": 50000, "business": 30000, "lifestyle": 80000}.get(niche, 40000)
        
        return {
            "followers": base_followers + random.randint(-10000, 20000),
            "engagement_rate": random.uniform(0.02, 0.08),
            "monthly_revenue": random.uniform(5000, 50000),
            "posts_per_week": random.randint(3, 14),
            "top_content": [
                {"title": "How I Built My Business", "views": 500000, "engagement": 0.12},
                {"title": "Daily Routine for Success", "views": 300000, "engagement": 0.08},
                {"title": "Productivity Hacks", "views": 250000, "engagement": 0.10}
            ],
            "themes": ["productivity", "entrepreneurship", "motivation", "tutorials"],
            "posting_patterns": {
                "best_times": ["09:00", "18:00", "21:00"],
                "best_days": ["Monday", "Wednesday", "Friday"],
                "content_types": {"video": 0.7, "image": 0.2, "text": 0.1}
            }
        }
    
    async def _identify_competitive_advantages(self, competitor_data: Dict[str, Any]) -> List[str]:
        """Identify competitor's competitive advantages"""
        advantages = []
        
        if competitor_data["engagement_rate"] > 0.06:
            advantages.append("High audience engagement")
        
        if competitor_data["posts_per_week"] > 10:
            advantages.append("Consistent high-frequency posting")
        
        if competitor_data["monthly_revenue"] > 20000:
            advantages.append("Strong monetization strategy")
        
        advantages.append("Established brand presence")
        advantages.append("Proven content formats")
        
        return advantages
    
    async def _identify_opportunities(self, competitor_data: Dict[str, Any], niche: str) -> List[str]:
        """Identify opportunities to compete"""
        opportunities = []
        
        if competitor_data["posts_per_week"] < 5:
            opportunities.append("Opportunity to post more frequently")
        
        if competitor_data["engagement_rate"] < 0.04:
            opportunities.append("Opportunity to create more engaging content")
        
        # Content gap analysis
        themes = competitor_data["themes"]
        potential_themes = {
            "tech": ["AI automation", "coding tutorials", "tech reviews"],
            "business": ["case studies", "industry insights", "tool reviews"],
            "lifestyle": ["wellness", "travel", "personal development"]
        }
        
        missing_themes = set(potential_themes.get(niche, [])) - set(themes)
        for theme in missing_themes:
            opportunities.append(f"Underexplored content theme: {theme}")
        
        return opportunities
    
    async def _identify_threats(self, competitor_data: Dict[str, Any]) -> List[str]:
        """Identify competitive threats"""
        threats = []
        
        if competitor_data["followers"] > 100000:
            threats.append("Large established audience")
        
        if competitor_data["monthly_revenue"] > 30000:
            threats.append("Strong financial resources for content production")
        
        if competitor_data["engagement_rate"] > 0.07:
            threats.append("Highly engaged community")
        
        threats.append("First-mover advantage in niche")
        threats.append("Established brand partnerships")
        
        return threats


class IntelligenceDashboard:
    """Main intelligence dashboard orchestrator"""
    
    def __init__(self):
        self.realtime_engine = RealTimeAnalyticsEngine()
        self.predictive_engine = PredictiveAnalyticsEngine()
        self.competitor_engine = CompetitorAnalysisEngine()
        self.dashboard_data = {}
    
    async def generate_comprehensive_report(self, creator_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        
        report_id = f"report_{uuid.uuid4().hex[:8]}"
        
        # Generate predictive insights
        insights = []
        
        # Viral prediction for recent content
        if "recent_content" in creator_profile:
            for content in creator_profile["recent_content"][:3]:
                viral_insight = await self.predictive_engine.generate_viral_prediction(content)
                insights.append(asdict(viral_insight))
        
        # Revenue forecast
        historical_revenue = creator_profile.get("revenue_history", [1000, 1200, 1100, 1300, 1500])
        revenue_insight = await self.predictive_engine.generate_revenue_forecast(historical_revenue)
        insights.append(asdict(revenue_insight))
        
        # Growth projection
        follower_history = creator_profile.get("follower_history", list(range(10000, 15000, 100)))
        growth_insight = await self.predictive_engine.generate_growth_projection(follower_history)
        insights.append(asdict(growth_insight))
        
        # Competitor analysis
        competitors = creator_profile.get("competitors", ["competitor1", "competitor2"])
        competitor_analyses = []
        
        for competitor in competitors[:2]:  # Analyze top 2 competitors
            analysis = await self.competitor_engine.analyze_competitor(
                competitor, creator_profile.get("niche", "general")
            )
            competitor_analyses.append(asdict(analysis))
        
        # Generate summary metrics
        summary_metrics = await self._generate_summary_metrics(creator_profile, insights)
        
        # Generate actionable recommendations
        recommendations = await self._generate_actionable_recommendations(insights, competitor_analyses)
        
        return {
            "report_id": report_id,
            "generated_at": datetime.now().isoformat(),
            "creator_profile": creator_profile,
            "summary_metrics": summary_metrics,
            "predictive_insights": insights,
            "competitor_analysis": competitor_analyses,
            "actionable_recommendations": recommendations,
            "next_review_date": (datetime.now() + timedelta(days=7)).isoformat()
        }
    
    async def _generate_summary_metrics(self, creator_profile: Dict[str, Any], 
                                       insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary metrics for dashboard"""
        
        # Extract key metrics from insights
        viral_scores = [insight["predicted_value"] for insight in insights 
                       if insight["prediction_type"] == "viral_potential"]
        avg_viral_score = sum(viral_scores) / len(viral_scores) if viral_scores else 0.5
        
        revenue_forecasts = [insight["predicted_value"] for insight in insights 
                           if insight["prediction_type"] == "revenue_forecast"]
        total_revenue_forecast = sum(revenue_forecasts)
        
        growth_projections = [insight["predicted_value"] for insight in insights 
                            if insight["prediction_type"] == "growth_projection"]
        projected_followers = max(growth_projections) if growth_projections else creator_profile.get("total_followers", 10000)
        
        return {
            "current_followers": creator_profile.get("total_followers", 10000),
            "projected_followers_30d": projected_followers,
            "current_monthly_revenue": creator_profile.get("monthly_revenue", 2000),
            "projected_monthly_revenue": total_revenue_forecast,
            "average_viral_score": avg_viral_score,
            "engagement_rate": creator_profile.get("engagement_rate", 0.035),
            "content_performance_score": avg_viral_score * 100,
            "growth_rate": ((projected_followers - creator_profile.get("total_followers", 10000)) / 
                          creator_profile.get("total_followers", 10000)) * 100
        }
    
    async def _generate_actionable_recommendations(self, insights: List[Dict[str, Any]], 
                                                 competitor_analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Extract recommendations from insights
        for insight in insights:
            for rec in insight.get("recommendations", []):
                recommendations.append({
                    "category": insight["prediction_type"],
                    "priority": "high" if insight["confidence_score"] > 0.8 else "medium",
                    "action": rec,
                    "expected_impact": insight.get("potential_impact", {}),
                    "timeframe": f"{insight['prediction_timeframe']} days"
                })
        
        # Add competitor-based recommendations
        for analysis in competitor_analyses:
            for opportunity in analysis.get("opportunities", []):
                recommendations.append({
                    "category": "competitive_opportunity",
                    "priority": "medium",
                    "action": opportunity,
                    "expected_impact": {"competitive_advantage": "medium"},
                    "timeframe": "30 days"
                })
        
        # Sort by priority and potential impact
        priority_order = {"high": 3, "medium": 2, "low": 1}
        recommendations.sort(key=lambda x: priority_order.get(x["priority"], 1), reverse=True)
        
        return recommendations[:10]  # Return top 10 recommendations


# Global intelligence dashboard instance
intelligence_dashboard = IntelligenceDashboard()

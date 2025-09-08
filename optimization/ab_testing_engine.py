#!/usr/bin/env python3
"""
Advanced A/B Testing and Optimization Engine
Intelligent experimentation for content, campaigns, and monetization
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
import scipy.stats as stats
from collections import defaultdict
import math

logger = logging.getLogger(__name__)


class TestType(Enum):
    """Types of A/B tests"""
    CONTENT_HOOK = "content_hook"
    CALL_TO_ACTION = "call_to_action"
    THUMBNAIL = "thumbnail"
    POSTING_TIME = "posting_time"
    HASHTAGS = "hashtags"
    CAPTION_LENGTH = "caption_length"
    CONTENT_FORMAT = "content_format"
    PRICING = "pricing"
    EMAIL_SUBJECT = "email_subject"
    LANDING_PAGE = "landing_page"
    AD_CREATIVE = "ad_creative"
    AUDIENCE_TARGETING = "audience_targeting"


class TestStatus(Enum):
    """A/B test status"""
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MetricType(Enum):
    """Types of metrics to optimize"""
    ENGAGEMENT_RATE = "engagement_rate"
    CLICK_THROUGH_RATE = "click_through_rate"
    CONVERSION_RATE = "conversion_rate"
    REVENUE_PER_VISITOR = "revenue_per_visitor"
    COST_PER_ACQUISITION = "cost_per_acquisition"
    RETENTION_RATE = "retention_rate"
    VIRAL_COEFFICIENT = "viral_coefficient"
    TIME_ON_PAGE = "time_on_page"
    BOUNCE_RATE = "bounce_rate"
    SHARE_RATE = "share_rate"


@dataclass
class TestVariant:
    """A/B test variant"""
    variant_id: str
    name: str
    description: str
    
    # Variant configuration
    variant_data: Dict[str, Any]  # The actual variant content/settings
    traffic_allocation: float  # Percentage of traffic (0.0 to 1.0)
    
    # Performance metrics
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    revenue: float = 0.0
    
    # Calculated metrics
    engagement_rate: float = 0.0
    conversion_rate: float = 0.0
    revenue_per_visitor: float = 0.0
    
    # Statistical data
    confidence_interval: Tuple[float, float] = (0.0, 0.0)
    statistical_significance: float = 0.0
    
    # Status
    is_control: bool = False
    is_winner: bool = False


@dataclass
class ABTest:
    """A/B test configuration and results"""
    test_id: str
    name: str
    description: str
    test_type: TestType
    
    # Test configuration
    primary_metric: MetricType
    secondary_metrics: List[MetricType]
    variants: List[TestVariant]
    
    # Test parameters
    minimum_sample_size: int
    minimum_effect_size: float  # Minimum detectable effect
    confidence_level: float = 0.95  # 95% confidence
    statistical_power: float = 0.8  # 80% power
    
    # Test duration
    start_date: datetime
    end_date: datetime
    max_duration_days: int = 30
    
    # Test status
    status: TestStatus = TestStatus.DRAFT
    
    # Results
    winning_variant_id: Optional[str] = None
    test_results: Dict[str, Any] = None
    recommendations: List[str] = None
    
    # Metadata
    created_by: str = "system"
    created_date: datetime = None
    last_updated: datetime = None


class StatisticalAnalyzer:
    """Statistical analysis for A/B tests"""
    
    @staticmethod
    def calculate_sample_size(baseline_rate: float, minimum_effect_size: float,
                            confidence_level: float = 0.95, power: float = 0.8) -> int:
        """Calculate required sample size for A/B test"""
        
        # Convert confidence level to alpha
        alpha = 1 - confidence_level
        beta = 1 - power
        
        # Z-scores
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)
        
        # Effect size calculation
        p1 = baseline_rate
        p2 = baseline_rate * (1 + minimum_effect_size)
        
        # Pooled proportion
        p_pooled = (p1 + p2) / 2
        
        # Sample size calculation
        numerator = (z_alpha * math.sqrt(2 * p_pooled * (1 - p_pooled)) + 
                    z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
        denominator = (p2 - p1) ** 2
        
        sample_size = math.ceil(numerator / denominator)
        
        return max(sample_size, 100)  # Minimum 100 samples
    
    @staticmethod
    def calculate_statistical_significance(variant_a: TestVariant, 
                                         variant_b: TestVariant,
                                         metric: MetricType) -> Tuple[float, bool]:
        """Calculate statistical significance between two variants"""
        
        if metric == MetricType.CONVERSION_RATE:
            # Proportion test
            n1, n2 = variant_a.impressions, variant_b.impressions
            x1, x2 = variant_a.conversions, variant_b.conversions
            
            if n1 == 0 or n2 == 0:
                return 0.0, False
            
            p1, p2 = x1/n1, x2/n2
            p_pooled = (x1 + x2) / (n1 + n2)
            
            se = math.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
            
            if se == 0:
                return 0.0, False
            
            z_score = (p2 - p1) / se
            p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
            
            return p_value, p_value < 0.05
        
        elif metric == MetricType.REVENUE_PER_VISITOR:
            # T-test for continuous variables
            if variant_a.impressions < 30 or variant_b.impressions < 30:
                return 1.0, False  # Not enough data
            
            # Simplified t-test (would need actual revenue data points)
            mean1 = variant_a.revenue_per_visitor
            mean2 = variant_b.revenue_per_visitor
            
            # Estimate standard deviations (simplified)
            std1 = mean1 * 0.5  # Assume 50% coefficient of variation
            std2 = mean2 * 0.5
            
            n1, n2 = variant_a.impressions, variant_b.impressions
            
            se = math.sqrt((std1**2 / n1) + (std2**2 / n2))
            
            if se == 0:
                return 0.0, False
            
            t_score = (mean2 - mean1) / se
            df = n1 + n2 - 2
            p_value = 2 * (1 - stats.t.cdf(abs(t_score), df))
            
            return p_value, p_value < 0.05
        
        return 1.0, False
    
    @staticmethod
    def calculate_confidence_interval(variant: TestVariant, metric: MetricType,
                                    confidence_level: float = 0.95) -> Tuple[float, float]:
        """Calculate confidence interval for variant metric"""
        
        alpha = 1 - confidence_level
        z_score = stats.norm.ppf(1 - alpha/2)
        
        if metric == MetricType.CONVERSION_RATE:
            if variant.impressions == 0:
                return (0.0, 0.0)
            
            p = variant.conversion_rate
            n = variant.impressions
            
            se = math.sqrt(p * (1 - p) / n)
            margin_error = z_score * se
            
            return (max(0, p - margin_error), min(1, p + margin_error))
        
        elif metric == MetricType.REVENUE_PER_VISITOR:
            if variant.impressions == 0:
                return (0.0, 0.0)
            
            mean = variant.revenue_per_visitor
            # Simplified standard error calculation
            se = mean * 0.1  # Assume 10% standard error
            margin_error = z_score * se
            
            return (max(0, mean - margin_error), mean + margin_error)
        
        return (0.0, 0.0)


class ABTestEngine:
    """Advanced A/B testing engine"""
    
    def __init__(self):
        self.active_tests = {}
        self.completed_tests = {}
        self.test_results_cache = {}
        self.analyzer = StatisticalAnalyzer()
    
    async def create_test(self, test_config: Dict[str, Any]) -> ABTest:
        """Create new A/B test"""
        
        test_id = f"test_{uuid.uuid4().hex[:8]}"
        
        # Create variants
        variants = []
        for i, variant_config in enumerate(test_config["variants"]):
            variant = TestVariant(
                variant_id=f"variant_{i}",
                name=variant_config["name"],
                description=variant_config["description"],
                variant_data=variant_config["data"],
                traffic_allocation=variant_config.get("traffic_allocation", 1.0 / len(test_config["variants"])),
                is_control=variant_config.get("is_control", i == 0)
            )
            variants.append(variant)
        
        # Calculate minimum sample size
        baseline_rate = test_config.get("baseline_rate", 0.05)
        minimum_effect_size = test_config.get("minimum_effect_size", 0.1)
        minimum_sample_size = self.analyzer.calculate_sample_size(
            baseline_rate, minimum_effect_size
        )
        
        # Create test
        test = ABTest(
            test_id=test_id,
            name=test_config["name"],
            description=test_config["description"],
            test_type=TestType(test_config["test_type"]),
            primary_metric=MetricType(test_config["primary_metric"]),
            secondary_metrics=[MetricType(m) for m in test_config.get("secondary_metrics", [])],
            variants=variants,
            minimum_sample_size=minimum_sample_size,
            minimum_effect_size=minimum_effect_size,
            confidence_level=test_config.get("confidence_level", 0.95),
            statistical_power=test_config.get("statistical_power", 0.8),
            start_date=datetime.fromisoformat(test_config["start_date"]),
            end_date=datetime.fromisoformat(test_config["end_date"]),
            max_duration_days=test_config.get("max_duration_days", 30),
            created_date=datetime.now(),
            last_updated=datetime.now()
        )
        
        self.active_tests[test_id] = test
        
        logger.info(f"Created A/B test: {test.name} ({test_id})")
        
        return test
    
    async def start_test(self, test_id: str) -> bool:
        """Start A/B test"""
        
        if test_id not in self.active_tests:
            raise ValueError(f"Test not found: {test_id}")
        
        test = self.active_tests[test_id]
        
        if test.status != TestStatus.DRAFT:
            raise ValueError(f"Test cannot be started. Current status: {test.status}")
        
        # Validate test configuration
        if not self._validate_test_config(test):
            raise ValueError("Invalid test configuration")
        
        test.status = TestStatus.RUNNING
        test.start_date = datetime.now()
        test.last_updated = datetime.now()
        
        logger.info(f"Started A/B test: {test.name}")
        
        return True
    
    async def record_event(self, test_id: str, variant_id: str, 
                          event_type: str, event_data: Dict[str, Any] = None):
        """Record event for A/B test variant"""
        
        if test_id not in self.active_tests:
            return  # Test not found or not active
        
        test = self.active_tests[test_id]
        
        if test.status != TestStatus.RUNNING:
            return  # Test not running
        
        # Find variant
        variant = None
        for v in test.variants:
            if v.variant_id == variant_id:
                variant = v
                break
        
        if not variant:
            return  # Variant not found
        
        # Record event
        if event_type == "impression":
            variant.impressions += 1
        elif event_type == "click":
            variant.clicks += 1
        elif event_type == "conversion":
            variant.conversions += 1
            if event_data and "revenue" in event_data:
                variant.revenue += event_data["revenue"]
        
        # Update calculated metrics
        self._update_variant_metrics(variant)
        
        # Check if test should be stopped
        await self._check_test_completion(test)
    
    async def analyze_test_results(self, test_id: str) -> Dict[str, Any]:
        """Analyze A/B test results"""
        
        if test_id not in self.active_tests and test_id not in self.completed_tests:
            raise ValueError(f"Test not found: {test_id}")
        
        test = self.active_tests.get(test_id) or self.completed_tests.get(test_id)
        
        # Update all variant metrics
        for variant in test.variants:
            self._update_variant_metrics(variant)
        
        # Statistical analysis
        control_variant = next((v for v in test.variants if v.is_control), test.variants[0])
        results = {
            "test_id": test_id,
            "test_name": test.name,
            "status": test.status.value,
            "primary_metric": test.primary_metric.value,
            "variants": [],
            "statistical_analysis": {},
            "recommendations": []
        }
        
        # Analyze each variant
        for variant in test.variants:
            # Calculate confidence interval
            ci = self.analyzer.calculate_confidence_interval(variant, test.primary_metric)
            variant.confidence_interval = ci
            
            # Calculate statistical significance vs control
            if variant != control_variant:
                p_value, is_significant = self.analyzer.calculate_statistical_significance(
                    control_variant, variant, test.primary_metric
                )
                variant.statistical_significance = 1 - p_value
            
            variant_result = {
                "variant_id": variant.variant_id,
                "name": variant.name,
                "is_control": variant.is_control,
                "impressions": variant.impressions,
                "conversions": variant.conversions,
                "conversion_rate": variant.conversion_rate,
                "revenue": variant.revenue,
                "revenue_per_visitor": variant.revenue_per_visitor,
                "confidence_interval": ci,
                "statistical_significance": variant.statistical_significance,
                "is_winner": variant.is_winner
            }
            
            results["variants"].append(variant_result)
        
        # Determine winner
        winner = self._determine_winner(test)
        if winner:
            winner.is_winner = True
            test.winning_variant_id = winner.variant_id
            results["winner"] = winner.variant_id
        
        # Generate recommendations
        recommendations = self._generate_recommendations(test)
        results["recommendations"] = recommendations
        test.recommendations = recommendations
        
        # Cache results
        self.test_results_cache[test_id] = results
        test.test_results = results
        test.last_updated = datetime.now()
        
        return results
    
    async def stop_test(self, test_id: str, reason: str = "manual_stop") -> bool:
        """Stop A/B test"""
        
        if test_id not in self.active_tests:
            raise ValueError(f"Test not found: {test_id}")
        
        test = self.active_tests[test_id]
        
        if test.status != TestStatus.RUNNING:
            raise ValueError(f"Test is not running. Current status: {test.status}")
        
        test.status = TestStatus.COMPLETED
        test.end_date = datetime.now()
        test.last_updated = datetime.now()
        
        # Analyze final results
        await self.analyze_test_results(test_id)
        
        # Move to completed tests
        self.completed_tests[test_id] = test
        del self.active_tests[test_id]
        
        logger.info(f"Stopped A/B test: {test.name} (Reason: {reason})")
        
        return True
    
    def _validate_test_config(self, test: ABTest) -> bool:
        """Validate A/B test configuration"""
        
        # Check variants
        if len(test.variants) < 2:
            return False
        
        # Check traffic allocation
        total_allocation = sum(v.traffic_allocation for v in test.variants)
        if abs(total_allocation - 1.0) > 0.01:  # Allow small rounding errors
            return False
        
        # Check dates
        if test.end_date <= test.start_date:
            return False
        
        return True
    
    def _update_variant_metrics(self, variant: TestVariant):
        """Update calculated metrics for variant"""
        
        if variant.impressions > 0:
            variant.engagement_rate = variant.clicks / variant.impressions
            variant.conversion_rate = variant.conversions / variant.impressions
            variant.revenue_per_visitor = variant.revenue / variant.impressions
    
    async def _check_test_completion(self, test: ABTest):
        """Check if test should be completed"""
        
        # Check if minimum sample size reached
        total_impressions = sum(v.impressions for v in test.variants)
        if total_impressions < test.minimum_sample_size:
            return
        
        # Check if maximum duration reached
        if datetime.now() >= test.end_date:
            await self.stop_test(test.test_id, "max_duration_reached")
            return
        
        # Check for early stopping due to statistical significance
        control_variant = next((v for v in test.variants if v.is_control), test.variants[0])
        
        for variant in test.variants:
            if variant == control_variant:
                continue
            
            p_value, is_significant = self.analyzer.calculate_statistical_significance(
                control_variant, variant, test.primary_metric
            )
            
            # Early stopping if highly significant and sufficient sample size
            if is_significant and p_value < 0.01 and total_impressions > test.minimum_sample_size * 0.5:
                await self.stop_test(test.test_id, "early_stopping_significance")
                return
    
    def _determine_winner(self, test: ABTest) -> Optional[TestVariant]:
        """Determine winning variant"""
        
        if test.primary_metric == MetricType.CONVERSION_RATE:
            return max(test.variants, key=lambda v: v.conversion_rate)
        elif test.primary_metric == MetricType.REVENUE_PER_VISITOR:
            return max(test.variants, key=lambda v: v.revenue_per_visitor)
        elif test.primary_metric == MetricType.ENGAGEMENT_RATE:
            return max(test.variants, key=lambda v: v.engagement_rate)
        
        return None
    
    def _generate_recommendations(self, test: ABTest) -> List[str]:
        """Generate recommendations based on test results"""
        
        recommendations = []
        
        winner = self._determine_winner(test)
        control = next((v for v in test.variants if v.is_control), test.variants[0])
        
        if winner and winner != control:
            improvement = 0
            if test.primary_metric == MetricType.CONVERSION_RATE:
                improvement = ((winner.conversion_rate - control.conversion_rate) / control.conversion_rate) * 100
            elif test.primary_metric == MetricType.REVENUE_PER_VISITOR:
                improvement = ((winner.revenue_per_visitor - control.revenue_per_visitor) / control.revenue_per_visitor) * 100
            
            recommendations.append(f"Implement {winner.name} - shows {improvement:.1f}% improvement over control")
            recommendations.append(f"Expected impact: {improvement:.1f}% increase in {test.primary_metric.value}")
        else:
            recommendations.append("No significant winner found - consider running longer or testing different variants")
        
        # Sample size recommendations
        total_impressions = sum(v.impressions for v in test.variants)
        if total_impressions < test.minimum_sample_size:
            recommendations.append(f"Increase sample size - need {test.minimum_sample_size - total_impressions} more impressions")
        
        return recommendations
    
    def get_active_tests(self) -> List[ABTest]:
        """Get all active tests"""
        return list(self.active_tests.values())
    
    def get_test_results(self, test_id: str) -> Optional[Dict[str, Any]]:
        """Get cached test results"""
        return self.test_results_cache.get(test_id)


# Global A/B testing engine instance
ab_test_engine = ABTestEngine()

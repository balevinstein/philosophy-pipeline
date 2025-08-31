"""
API Cost Tracking System for Philosophy Pipeline

Provides real-time cost calculation, budget monitoring, and usage analytics
for various AI API providers (Anthropic Claude, OpenAI, etc.)
"""

import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from threading import Lock
import warnings


class APIProvider(Enum):
    """Supported API providers"""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"
    CUSTOM = "custom"


@dataclass
class CostMetrics:
    """Cost metrics for tracking API usage"""
    
    # Token usage
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    
    # Request counts
    requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    
    # Cost breakdown
    input_cost: float = 0.0
    output_cost: float = 0.0
    total_cost: float = 0.0
    
    # Timing
    total_latency: float = 0.0
    avg_latency: float = 0.0
    max_latency: float = 0.0
    min_latency: float = float('inf')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CostMetrics':
        """Create from dictionary"""
        return cls(**data)
    
    def update_latency(self, latency: float):
        """Update latency statistics"""
        self.total_latency += latency
        self.max_latency = max(self.max_latency, latency)
        self.min_latency = min(self.min_latency, latency)
        
        if self.successful_requests > 0:
            self.avg_latency = self.total_latency / self.successful_requests


@dataclass
class PricingModel:
    """Pricing model for an API provider/model combination"""
    provider: APIProvider
    model: str
    input_price_per_1k: float  # Price per 1000 input tokens
    output_price_per_1k: float  # Price per 1000 output tokens
    currency: str = "USD"
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for token usage"""
        input_cost = (input_tokens / 1000) * self.input_price_per_1k
        output_cost = (output_tokens / 1000) * self.output_price_per_1k
        return input_cost + output_cost


@dataclass
class APICall:
    """Record of a single API call"""
    timestamp: float
    provider: APIProvider
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    latency: float
    success: bool
    context: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['provider'] = self.provider.value
        data['datetime'] = datetime.fromtimestamp(self.timestamp).isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'APICall':
        """Create from dictionary"""
        data['provider'] = APIProvider(data['provider'])
        if 'datetime' in data:
            del data['datetime']  # Remove derived field
        return cls(**data)


@dataclass 
class BudgetAlert:
    """Budget alert configuration"""
    threshold: float  # Alert when cost reaches this amount
    period: str  # "hour", "day", "week", "month", "total"
    alert_type: str  # "warning", "critical", "budget_exceeded"
    enabled: bool = True
    last_triggered: Optional[float] = None


class CostTracker:
    """Comprehensive cost tracking and budget monitoring system"""
    
    # Default pricing models (as of 2024 - should be updated regularly)
    DEFAULT_PRICING = {
        (APIProvider.ANTHROPIC, "claude-3-opus-20240229"): PricingModel(
            APIProvider.ANTHROPIC, "claude-3-opus-20240229", 15.0, 75.0
        ),
        (APIProvider.ANTHROPIC, "claude-3-sonnet-20240229"): PricingModel(
            APIProvider.ANTHROPIC, "claude-3-sonnet-20240229", 3.0, 15.0
        ),
        (APIProvider.ANTHROPIC, "claude-3-haiku-20240307"): PricingModel(
            APIProvider.ANTHROPIC, "claude-3-haiku-20240307", 0.25, 1.25
        ),
        (APIProvider.OPENAI, "gpt-4"): PricingModel(
            APIProvider.OPENAI, "gpt-4", 30.0, 60.0
        ),
        (APIProvider.OPENAI, "gpt-4-turbo"): PricingModel(
            APIProvider.OPENAI, "gpt-4-turbo", 10.0, 30.0
        ),
        (APIProvider.OPENAI, "gpt-3.5-turbo"): PricingModel(
            APIProvider.OPENAI, "gpt-3.5-turbo", 0.5, 1.5
        )
    }
    
    def __init__(
        self,
        save_dir: Optional[Union[str, Path]] = None,
        auto_save: bool = True,
        default_budget_limit: float = 100.0,
        currency: str = "USD"
    ):
        """
        Initialize cost tracker
        
        Args:
            save_dir: Directory to save cost data
            auto_save: Automatically save data
            default_budget_limit: Default budget limit
            currency: Currency for cost calculations
        """
        self.save_dir = Path(save_dir) if save_dir else None
        self.auto_save = auto_save
        self.default_budget_limit = default_budget_limit
        self.currency = currency
        
        # Cost tracking
        self.api_calls: List[APICall] = []
        self.metrics_by_provider: Dict[APIProvider, CostMetrics] = {}
        self.metrics_by_model: Dict[str, CostMetrics] = {}
        self.total_metrics = CostMetrics()
        
        # Pricing models
        self.pricing_models: Dict[tuple, PricingModel] = self.DEFAULT_PRICING.copy()
        
        # Budget management
        self.budget_alerts: List[BudgetAlert] = []
        self.budget_limit = default_budget_limit
        self.budget_warnings_sent = set()
        
        # Thread safety
        self._lock = Lock()
        
        # Session tracking
        self.session_metrics: Dict[str, CostMetrics] = {}
        self.current_session: Optional[str] = None
        
        # Create save directory
        if self.save_dir:
            self.save_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing data
        self._load_data()
        
        # Setup default budget alerts
        self._setup_default_alerts()
    
    def _setup_default_alerts(self):
        """Setup default budget alerts"""
        self.budget_alerts = [
            BudgetAlert(self.budget_limit * 0.5, "total", "warning"),
            BudgetAlert(self.budget_limit * 0.8, "total", "critical"),
            BudgetAlert(self.budget_limit, "total", "budget_exceeded"),
            BudgetAlert(self.budget_limit * 0.1, "day", "warning"),
            BudgetAlert(self.budget_limit * 0.25, "day", "critical")
        ]
    
    def _load_data(self):
        """Load existing cost data from disk"""
        if not self.save_dir:
            return
        
        # Load API calls
        calls_file = self.save_dir / "api_calls.json"
        if calls_file.exists():
            try:
                with open(calls_file, 'r') as f:
                    calls_data = json.load(f)
                
                self.api_calls = [APICall.from_dict(call) for call in calls_data]
                self._recalculate_metrics()
                
            except Exception as e:
                warnings.warn(f"Failed to load API calls data: {e}")
        
        # Load budget configuration
        budget_file = self.save_dir / "budget_config.json"
        if budget_file.exists():
            try:
                with open(budget_file, 'r') as f:
                    budget_data = json.load(f)
                
                self.budget_limit = budget_data.get("budget_limit", self.budget_limit)
                
                if "alerts" in budget_data:
                    self.budget_alerts = [
                        BudgetAlert(**alert) for alert in budget_data["alerts"]
                    ]
                    
            except Exception as e:
                warnings.warn(f"Failed to load budget configuration: {e}")
    
    def _save_data(self):
        """Save cost data to disk"""
        if not self.save_dir:
            return
        
        try:
            # Save API calls
            calls_file = self.save_dir / "api_calls.json"
            with open(calls_file, 'w') as f:
                json.dump([call.to_dict() for call in self.api_calls], f, indent=2)
            
            # Save budget configuration
            budget_file = self.save_dir / "budget_config.json"
            with open(budget_file, 'w') as f:
                json.dump({
                    "budget_limit": self.budget_limit,
                    "currency": self.currency,
                    "alerts": [asdict(alert) for alert in self.budget_alerts]
                }, f, indent=2)
                
        except Exception as e:
            warnings.warn(f"Failed to save cost data: {e}")
    
    def add_pricing_model(self, provider: APIProvider, model: str, pricing: PricingModel):
        """Add or update pricing model"""
        with self._lock:
            self.pricing_models[(provider, model)] = pricing
    
    def get_pricing_model(self, provider: APIProvider, model: str) -> Optional[PricingModel]:
        """Get pricing model for provider/model combination"""
        return self.pricing_models.get((provider, model))
    
    def start_session(self, session_id: str):
        """Start a new cost tracking session"""
        with self._lock:
            self.current_session = session_id
            if session_id not in self.session_metrics:
                self.session_metrics[session_id] = CostMetrics()
    
    def end_session(self, session_id: str) -> Optional[CostMetrics]:
        """End a cost tracking session"""
        with self._lock:
            if self.current_session == session_id:
                self.current_session = None
            return self.session_metrics.get(session_id)
    
    def record_api_call(
        self,
        provider: APIProvider,
        model: str,
        input_tokens: int,
        output_tokens: int,
        latency: float,
        success: bool = True,
        context: Optional[Dict[str, Any]] = None,
        custom_cost: Optional[float] = None
    ) -> float:
        """
        Record an API call and calculate cost
        
        Args:
            provider: API provider
            model: Model name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            latency: API call latency in seconds
            success: Whether the call was successful
            context: Additional context information
            custom_cost: Custom cost override
            
        Returns:
            Cost of the API call
        """
        with self._lock:
            # Calculate cost
            if custom_cost is not None:
                cost = custom_cost
            else:
                pricing = self.get_pricing_model(provider, model)
                if pricing:
                    cost = pricing.calculate_cost(input_tokens, output_tokens)
                else:
                    # Default fallback pricing
                    cost = (input_tokens * 0.001) + (output_tokens * 0.002)
                    warnings.warn(f"No pricing model for {provider.value}/{model}, using fallback")
            
            # Create API call record
            api_call = APICall(
                timestamp=time.time(),
                provider=provider,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                latency=latency,
                success=success,
                context=context
            )
            
            self.api_calls.append(api_call)
            
            # Update metrics
            self._update_metrics(api_call)
            
            # Check budget alerts
            self._check_budget_alerts()
            
            # Auto-save
            if self.auto_save:
                self._save_data()
            
            return cost
    
    def _update_metrics(self, api_call: APICall):
        """Update all relevant metrics with new API call"""
        # Initialize metrics if needed
        if api_call.provider not in self.metrics_by_provider:
            self.metrics_by_provider[api_call.provider] = CostMetrics()
        
        if api_call.model not in self.metrics_by_model:
            self.metrics_by_model[api_call.model] = CostMetrics()
        
        # List of metrics to update
        metrics_list = [
            self.total_metrics,
            self.metrics_by_provider[api_call.provider],
            self.metrics_by_model[api_call.model]
        ]
        
        # Add session metrics if active
        if self.current_session and self.current_session in self.session_metrics:
            metrics_list.append(self.session_metrics[self.current_session])
        
        # Update all metrics
        for metrics in metrics_list:
            metrics.input_tokens += api_call.input_tokens
            metrics.output_tokens += api_call.output_tokens
            metrics.total_tokens += api_call.input_tokens + api_call.output_tokens
            
            metrics.requests += 1
            if api_call.success:
                metrics.successful_requests += 1
                metrics.update_latency(api_call.latency)
            else:
                metrics.failed_requests += 1
            
            metrics.total_cost += api_call.cost
            
            # Update input/output cost breakdown
            if api_call.input_tokens > 0:
                input_ratio = api_call.input_tokens / (api_call.input_tokens + api_call.output_tokens)
                metrics.input_cost += api_call.cost * input_ratio
            
            if api_call.output_tokens > 0:
                output_ratio = api_call.output_tokens / (api_call.input_tokens + api_call.output_tokens)
                metrics.output_cost += api_call.cost * output_ratio
    
    def _recalculate_metrics(self):
        """Recalculate all metrics from API calls"""
        # Reset metrics
        self.total_metrics = CostMetrics()
        self.metrics_by_provider = {}
        self.metrics_by_model = {}
        
        # Recalculate from all API calls
        for api_call in self.api_calls:
            self._update_metrics(api_call)
    
    def _check_budget_alerts(self):
        """Check and trigger budget alerts if necessary"""
        current_time = time.time()
        
        for alert in self.budget_alerts:
            if not alert.enabled:
                continue
            
            # Calculate cost for the alert period
            if alert.period == "total":
                cost = self.total_metrics.total_cost
            else:
                period_start = self._get_period_start(alert.period)
                cost = self._get_cost_for_period(period_start, current_time)
            
            # Check if threshold is exceeded
            if cost >= alert.threshold:
                alert_key = f"{alert.period}_{alert.threshold}_{alert.alert_type}"
                
                # Don't send duplicate alerts within 1 hour
                if (alert_key not in self.budget_warnings_sent or
                    (alert.last_triggered and current_time - alert.last_triggered > 3600)):
                    
                    self._trigger_budget_alert(alert, cost)
                    alert.last_triggered = current_time
                    self.budget_warnings_sent.add(alert_key)
    
    def _get_period_start(self, period: str) -> float:
        """Get start timestamp for a period"""
        now = datetime.now()
        
        if period == "hour":
            start = now.replace(minute=0, second=0, microsecond=0)
        elif period == "day":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "week":
            days_since_monday = now.weekday()
            start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_since_monday)
        elif period == "month":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            # Default to beginning of time
            start = datetime.fromtimestamp(0)
        
        return start.timestamp()
    
    def _get_cost_for_period(self, start_time: float, end_time: float) -> float:
        """Get total cost for a time period"""
        return sum(
            call.cost for call in self.api_calls
            if start_time <= call.timestamp <= end_time
        )
    
    def _trigger_budget_alert(self, alert: BudgetAlert, current_cost: float):
        """Trigger a budget alert"""
        alert_msg = (
            f"Budget Alert ({alert.alert_type.upper()}): "
            f"{alert.period} cost ${current_cost:.2f} "
            f"has reached threshold ${alert.threshold:.2f}"
        )
        
        print(f"⚠️ {alert_msg}")
        
        # In a production system, you might also:
        # - Send email notifications
        # - Write to log files
        # - Trigger webhooks
        # - Pause API usage (for critical alerts)
    
    def get_cost_summary(self, period: Optional[str] = None) -> Dict[str, Any]:
        """
        Get cost summary for a specific period
        
        Args:
            period: Time period ("hour", "day", "week", "month", "total", or None for total)
            
        Returns:
            Cost summary dictionary
        """
        if period is None or period == "total":
            return {
                "period": "total",
                "total_cost": self.total_metrics.total_cost,
                "total_requests": self.total_metrics.requests,
                "total_tokens": self.total_metrics.total_tokens,
                "avg_cost_per_request": (
                    self.total_metrics.total_cost / self.total_metrics.requests
                    if self.total_metrics.requests > 0 else 0
                ),
                "avg_cost_per_1k_tokens": (
                    self.total_metrics.total_cost / self.total_metrics.total_tokens * 1000
                    if self.total_metrics.total_tokens > 0 else 0
                ),
                "by_provider": {
                    provider.value: metrics.to_dict()
                    for provider, metrics in self.metrics_by_provider.items()
                },
                "by_model": self.metrics_by_model.copy()
            }
        
        # Period-specific summary
        period_start = self._get_period_start(period)
        current_time = time.time()
        
        period_calls = [
            call for call in self.api_calls
            if period_start <= call.timestamp <= current_time
        ]
        
        if not period_calls:
            return {
                "period": period,
                "total_cost": 0.0,
                "total_requests": 0,
                "total_tokens": 0,
                "by_provider": {},
                "by_model": {}
            }
        
        # Calculate period metrics
        total_cost = sum(call.cost for call in period_calls)
        total_requests = len(period_calls)
        total_tokens = sum(call.input_tokens + call.output_tokens for call in period_calls)
        
        by_provider = {}
        by_model = {}
        
        for call in period_calls:
            # By provider
            if call.provider not in by_provider:
                by_provider[call.provider] = CostMetrics()
            provider_metrics = by_provider[call.provider]
            
            # By model
            if call.model not in by_model:
                by_model[call.model] = CostMetrics()
            model_metrics = by_model[call.model]
            
            # Update metrics (simplified)
            for metrics in [provider_metrics, model_metrics]:
                metrics.requests += 1
                metrics.total_cost += call.cost
                metrics.input_tokens += call.input_tokens
                metrics.output_tokens += call.output_tokens
                metrics.total_tokens += call.input_tokens + call.output_tokens
                
                if call.success:
                    metrics.successful_requests += 1
                else:
                    metrics.failed_requests += 1
        
        return {
            "period": period,
            "period_start": datetime.fromtimestamp(period_start).isoformat(),
            "total_cost": total_cost,
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "avg_cost_per_request": total_cost / total_requests if total_requests > 0 else 0,
            "avg_cost_per_1k_tokens": total_cost / total_tokens * 1000 if total_tokens > 0 else 0,
            "by_provider": {
                provider.value: metrics.to_dict()
                for provider, metrics in by_provider.items()
            },
            "by_model": {
                model: metrics.to_dict()
                for model, metrics in by_model.items()
            }
        }
    
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get cost summary for a specific session"""
        if session_id not in self.session_metrics:
            return None
        
        metrics = self.session_metrics[session_id]
        
        # Get session API calls
        session_calls = [
            call for call in self.api_calls
            if call.context and call.context.get('session_id') == session_id
        ]
        
        return {
            "session_id": session_id,
            "metrics": metrics.to_dict(),
            "call_count": len(session_calls),
            "calls": [call.to_dict() for call in session_calls[-10:]]  # Last 10 calls
        }
    
    def set_budget_limit(self, limit: float):
        """Set budget limit and update alerts"""
        with self._lock:
            self.budget_limit = limit
            
            # Update default alerts to match new budget
            for alert in self.budget_alerts:
                if alert.period == "total":
                    if alert.alert_type == "warning":
                        alert.threshold = limit * 0.5
                    elif alert.alert_type == "critical":
                        alert.threshold = limit * 0.8
                    elif alert.alert_type == "budget_exceeded":
                        alert.threshold = limit
            
            if self.auto_save:
                self._save_data()
    
    def add_budget_alert(self, alert: BudgetAlert):
        """Add a custom budget alert"""
        with self._lock:
            self.budget_alerts.append(alert)
            
            if self.auto_save:
                self._save_data()
    
    def get_budget_status(self) -> Dict[str, Any]:
        """Get current budget status"""
        total_cost = self.total_metrics.total_cost
        remaining_budget = self.budget_limit - total_cost
        budget_used_percent = (total_cost / self.budget_limit * 100) if self.budget_limit > 0 else 0
        
        # Get daily spend
        today_start = self._get_period_start("day")
        today_cost = self._get_cost_for_period(today_start, time.time())
        
        return {
            "budget_limit": self.budget_limit,
            "total_spent": total_cost,
            "remaining_budget": remaining_budget,
            "budget_used_percent": budget_used_percent,
            "today_spent": today_cost,
            "currency": self.currency,
            "status": (
                "over_budget" if total_cost > self.budget_limit else
                "critical" if budget_used_percent > 80 else
                "warning" if budget_used_percent > 50 else
                "ok"
            )
        }
    
    def generate_cost_report(self) -> Dict[str, Any]:
        """Generate comprehensive cost report"""
        return {
            "generated_at": datetime.now().isoformat(),
            "budget_status": self.get_budget_status(),
            "total_summary": self.get_cost_summary("total"),
            "today_summary": self.get_cost_summary("day"),
            "this_week_summary": self.get_cost_summary("week"),
            "this_month_summary": self.get_cost_summary("month"),
            "recent_calls": [call.to_dict() for call in self.api_calls[-20:]],
            "active_sessions": {
                session_id: metrics.to_dict()
                for session_id, metrics in self.session_metrics.items()
            },
            "pricing_models": {
                f"{provider.value}/{model}": asdict(pricing)
                for (provider, model), pricing in self.pricing_models.items()
            }
        }
    
    def save_cost_report(self, filename: Optional[str] = None):
        """Save cost report to file"""
        if not self.save_dir:
            print("Warning: No save directory configured")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cost_report_{timestamp}.json"
        
        report = self.generate_cost_report()
        
        try:
            report_file = self.save_dir / filename
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            print(f"Cost report saved to: {report_file}")
            
        except Exception as e:
            print(f"Error saving cost report: {e}")
    
    def clear_old_data(self, days: int = 30):
        """Clear API call data older than specified days"""
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        with self._lock:
            original_count = len(self.api_calls)
            self.api_calls = [
                call for call in self.api_calls
                if call.timestamp > cutoff_time
            ]
            
            removed_count = original_count - len(self.api_calls)
            
            if removed_count > 0:
                # Recalculate metrics
                self._recalculate_metrics()
                
                if self.auto_save:
                    self._save_data()
                
                print(f"Removed {removed_count} old API call records")
            
            return removed_count


# Global cost tracker instance
_global_cost_tracker: Optional[CostTracker] = None


def get_global_cost_tracker(**kwargs) -> CostTracker:
    """Get or create the global cost tracker"""
    global _global_cost_tracker
    if _global_cost_tracker is None:
        _global_cost_tracker = CostTracker(**kwargs)
    return _global_cost_tracker


def set_global_cost_tracker(tracker: CostTracker):
    """Set the global cost tracker"""
    global _global_cost_tracker
    _global_cost_tracker = tracker


def record_api_call(
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    latency: float,
    success: bool = True,
    **context
) -> float:
    """Convenience function to record API call using global tracker"""
    tracker = get_global_cost_tracker()
    provider_enum = APIProvider(provider.lower())
    return tracker.record_api_call(
        provider_enum, model, input_tokens, output_tokens, latency, success, context
    )
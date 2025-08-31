"""Performance monitoring dashboard and metrics collection."""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class PerformanceDashboard:
    """Performance monitoring dashboard for the philosophy pipeline."""
    
    def __init__(self, metrics_file: Optional[Path] = None):
        """Initialize performance dashboard.
        
        Args:
            metrics_file: File to store metrics data
        """
        self.metrics_file = metrics_file or Path.home() / ".philosophy_pipeline" / "performance_metrics.json"
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing metrics
        self.metrics = self._load_metrics()
        
        # Current session data
        self.session_start = time.time()
        self.session_id = f"session_{int(self.session_start)}"
        
    def _load_metrics(self) -> Dict[str, Any]:
        """Load metrics from disk."""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load metrics: {e}")
                
        return {
            'sessions': {},
            'total_stats': {
                'api_calls': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'total_duration': 0.0,
                'cost_saved_estimate': 0.0
            },
            'daily_stats': {}
        }
    
    def _save_metrics(self):
        """Save metrics to disk."""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save metrics: {e}")
    
    def record_api_call(self, stage: str, duration: float, cached: bool = False, 
                       model: str = None, tokens_estimated: int = None):
        """Record an API call for metrics tracking."""
        
        # Session data
        if self.session_id not in self.metrics['sessions']:
            self.metrics['sessions'][self.session_id] = {
                'start_time': self.session_start,
                'api_calls': [],
                'stats': {
                    'total_calls': 0,
                    'cache_hits': 0,
                    'total_duration': 0.0,
                    'stages_used': set(),
                    'models_used': set()
                }
            }
        
        session = self.metrics['sessions'][self.session_id]
        
        # Record call
        call_data = {
            'timestamp': time.time(),
            'stage': stage,
            'duration': duration,
            'cached': cached,
            'model': model,
            'tokens_estimated': tokens_estimated
        }
        
        session['api_calls'].append(call_data)
        
        # Update session stats
        session['stats']['total_calls'] += 1
        session['stats']['total_duration'] += duration
        session['stats']['stages_used'].add(stage)
        
        if cached:
            session['stats']['cache_hits'] += 1
            
        if model:
            session['stats']['models_used'].add(model)
        
        # Convert sets to lists for JSON serialization
        session['stats']['stages_used'] = list(session['stats']['stages_used'])
        session['stats']['models_used'] = list(session['stats']['models_used'])
        
        # Update total stats
        self.metrics['total_stats']['api_calls'] += 1
        self.metrics['total_stats']['total_duration'] += duration
        
        if cached:
            self.metrics['total_stats']['cache_hits'] += 1
            # Estimate cost savings (rough estimation)
            self.metrics['total_stats']['cost_saved_estimate'] += self._estimate_api_cost(tokens_estimated, model)
        else:
            self.metrics['total_stats']['cache_misses'] += 1
        
        # Update daily stats
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in self.metrics['daily_stats']:
            self.metrics['daily_stats'][today] = {
                'api_calls': 0,
                'cache_hits': 0,
                'total_duration': 0.0,
                'unique_stages': set(),
                'unique_models': set()
            }
        
        daily = self.metrics['daily_stats'][today]
        daily['api_calls'] += 1
        daily['total_duration'] += duration
        daily['unique_stages'].add(stage)
        
        if cached:
            daily['cache_hits'] += 1
            
        if model:
            daily['unique_models'].add(model)
            
        # Convert sets to lists
        daily['unique_stages'] = list(daily['unique_stages'])
        daily['unique_models'] = list(daily['unique_models'])
        
        # Save metrics periodically
        if session['stats']['total_calls'] % 10 == 0:
            self._save_metrics()
    
    def _estimate_api_cost(self, tokens: Optional[int], model: str) -> float:
        """Rough estimation of API cost savings."""
        if not tokens or not model:
            return 0.0
            
        # Rough cost estimates (per 1000 tokens)
        cost_per_1k = {
            'claude-3-5-sonnet': 0.003,
            'claude-3-haiku': 0.0008,
            'gpt-4': 0.03,
            'gpt-3.5-turbo': 0.002
        }
        
        base_cost = cost_per_1k.get('claude-3-5-sonnet', 0.003)  # Default
        for model_key, cost in cost_per_1k.items():
            if model_key in model.lower():
                base_cost = cost
                break
                
        return (tokens / 1000) * base_cost
    
    def get_current_session_stats(self) -> Dict[str, Any]:
        """Get statistics for the current session."""
        if self.session_id not in self.metrics['sessions']:
            return {'error': 'No current session data'}
            
        session = self.metrics['sessions'][self.session_id]
        stats = session['stats'].copy()
        
        # Calculate additional metrics
        if stats['total_calls'] > 0:
            stats['cache_hit_rate'] = stats['cache_hits'] / stats['total_calls']
            stats['avg_duration'] = stats['total_duration'] / stats['total_calls']
        else:
            stats['cache_hit_rate'] = 0.0
            stats['avg_duration'] = 0.0
            
        stats['session_duration'] = time.time() - self.session_start
        
        return stats
    
    def get_daily_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get daily statistics for the last N days."""
        daily_stats = {}
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            if date in self.metrics['daily_stats']:
                daily_data = self.metrics['daily_stats'][date].copy()
                
                # Calculate derived metrics
                if daily_data['api_calls'] > 0:
                    daily_data['cache_hit_rate'] = daily_data['cache_hits'] / daily_data['api_calls']
                    daily_data['avg_duration'] = daily_data['total_duration'] / daily_data['api_calls']
                else:
                    daily_data['cache_hit_rate'] = 0.0
                    daily_data['avg_duration'] = 0.0
                    
                daily_stats[date] = daily_data
                
        return daily_stats
    
    def get_overall_stats(self) -> Dict[str, Any]:
        """Get overall performance statistics."""
        total = self.metrics['total_stats'].copy()
        
        # Calculate derived metrics
        if total['api_calls'] > 0:
            total['cache_hit_rate'] = total['cache_hits'] / total['api_calls']
            total['avg_duration'] = total['total_duration'] / total['api_calls']
        else:
            total['cache_hit_rate'] = 0.0
            total['avg_duration'] = 0.0
            
        total['total_sessions'] = len(self.metrics['sessions'])
        
        return total
    
    def get_stage_performance(self) -> Dict[str, Dict[str, Any]]:
        """Get performance metrics by stage."""
        stage_stats = {}
        
        for session_id, session in self.metrics['sessions'].items():
            for call in session['api_calls']:
                stage = call['stage']
                
                if stage not in stage_stats:
                    stage_stats[stage] = {
                        'total_calls': 0,
                        'cache_hits': 0,
                        'total_duration': 0.0,
                        'durations': []
                    }
                
                stats = stage_stats[stage]
                stats['total_calls'] += 1
                stats['total_duration'] += call['duration']
                stats['durations'].append(call['duration'])
                
                if call['cached']:
                    stats['cache_hits'] += 1
        
        # Calculate derived metrics
        for stage, stats in stage_stats.items():
            if stats['total_calls'] > 0:
                stats['cache_hit_rate'] = stats['cache_hits'] / stats['total_calls']
                stats['avg_duration'] = stats['total_duration'] / stats['total_calls']
                
                # Calculate percentiles
                durations = sorted(stats['durations'])
                n = len(durations)
                stats['median_duration'] = durations[n//2] if n > 0 else 0.0
                stats['p95_duration'] = durations[int(n*0.95)] if n > 0 else 0.0
                
            del stats['durations']  # Remove raw data
            
        return stage_stats
    
    def generate_performance_report(self) -> str:
        """Generate a comprehensive performance report."""
        current_session = self.get_current_session_stats()
        overall = self.get_overall_stats()
        daily = self.get_daily_stats(7)
        stage_perf = self.get_stage_performance()
        
        report = f"""
Philosophy Pipeline Performance Report
=====================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Current Session Stats:
---------------------
Total API Calls: {current_session.get('total_calls', 0)}
Cache Hits: {current_session.get('cache_hits', 0)}
Cache Hit Rate: {current_session.get('cache_hit_rate', 0):.1%}
Average Duration: {current_session.get('avg_duration', 0):.2f}s
Session Duration: {current_session.get('session_duration', 0):.0f}s

Overall Performance:
------------------
Total API Calls: {overall['api_calls']}
Total Cache Hits: {overall['cache_hits']}
Overall Cache Hit Rate: {overall['cache_hit_rate']:.1%}
Total Duration: {overall['total_duration']:.2f}s
Average Call Duration: {overall['avg_duration']:.2f}s
Estimated Cost Savings: ${overall['cost_saved_estimate']:.2f}
Total Sessions: {overall['total_sessions']}

Stage Performance:
-----------------"""
        
        for stage, stats in stage_perf.items():
            report += f"""
{stage}:
  Calls: {stats['total_calls']}
  Cache Hit Rate: {stats['cache_hit_rate']:.1%}
  Avg Duration: {stats['avg_duration']:.2f}s
  Median Duration: {stats['median_duration']:.2f}s
  95th Percentile: {stats['p95_duration']:.2f}s"""

        report += f"""

Recent Daily Performance (Last 7 days):
--------------------------------------"""
        
        for date, stats in sorted(daily.items(), reverse=True):
            report += f"""
{date}:
  API Calls: {stats['api_calls']}
  Cache Hit Rate: {stats['cache_hit_rate']:.1%}
  Avg Duration: {stats['avg_duration']:.2f}s
  Unique Stages: {len(stats['unique_stages'])}
  Unique Models: {len(stats['unique_models'])}"""

        report += f"""

Performance Recommendations:
---------------------------"""
        
        # Generate recommendations based on metrics
        recommendations = self._generate_recommendations(overall, stage_perf)
        for rec in recommendations:
            report += f"\n• {rec}"
            
        return report
    
    def _generate_recommendations(self, overall: Dict[str, Any], 
                                stage_perf: Dict[str, Dict[str, Any]]) -> List[str]:
        """Generate performance recommendations based on metrics."""
        recommendations = []
        
        # Cache hit rate recommendations
        if overall['cache_hit_rate'] < 0.3:
            recommendations.append(
                f"Low cache hit rate ({overall['cache_hit_rate']:.1%}). "
                "Consider increasing cache TTL or reviewing prompt variations."
            )
        elif overall['cache_hit_rate'] > 0.8:
            recommendations.append(
                f"Excellent cache hit rate ({overall['cache_hit_rate']:.1%})! "
                "Cache optimization is working well."
            )
        
        # Stage-specific recommendations
        slow_stages = [
            stage for stage, stats in stage_perf.items() 
            if stats['avg_duration'] > 10.0
        ]
        if slow_stages:
            recommendations.append(
                f"Slow stages detected: {', '.join(slow_stages)}. "
                "Consider optimizing prompts or using faster models."
            )
        
        # Cost savings recommendations
        if overall['cost_saved_estimate'] > 10.0:
            recommendations.append(
                f"Great cost savings! Estimated ${overall['cost_saved_estimate']:.2f} "
                "saved through caching."
            )
        
        return recommendations
    
    def cleanup_old_data(self, days_to_keep: int = 30):
        """Clean up old session and daily data."""
        cutoff_time = time.time() - (days_to_keep * 24 * 3600)
        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime('%Y-%m-%d')
        
        # Clean up old sessions
        old_sessions = [
            session_id for session_id, session in self.metrics['sessions'].items()
            if session['start_time'] < cutoff_time
        ]
        
        for session_id in old_sessions:
            del self.metrics['sessions'][session_id]
        
        # Clean up old daily stats
        old_dates = [
            date for date in self.metrics['daily_stats'].keys()
            if date < cutoff_date
        ]
        
        for date in old_dates:
            del self.metrics['daily_stats'][date]
        
        logger.info(f"Cleaned up {len(old_sessions)} old sessions and {len(old_dates)} old daily records")
        self._save_metrics()
    
    def export_metrics(self, export_path: Path):
        """Export metrics to a file."""
        with open(export_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        logger.info(f"Metrics exported to {export_path}")
    
    def __del__(self):
        """Save metrics on destruction."""
        try:
            self._save_metrics()
        except:
            pass  # Ignore errors during cleanup
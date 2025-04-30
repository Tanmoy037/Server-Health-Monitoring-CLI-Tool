import psutil
from typing import Dict, Any

class CPUMetrics:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.warning_threshold = config['cpu']['warning_threshold']
        self.critical_threshold = config['cpu']['critical_threshold']
    
    def get_metrics(self) -> Dict[str, Any]:
        """Collect CPU metrics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            return {
                'usage_percent': cpu_percent,
                'core_count': cpu_count,
                'frequency': {
                    'current': cpu_freq.current if cpu_freq else None,
                    'min': cpu_freq.min if cpu_freq else None,
                    'max': cpu_freq.max if cpu_freq else None
                },
                'status': self._get_status(cpu_percent)
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'ERROR'
            }
    
    def _get_status(self, usage: float) -> str:
        """Determine status based on usage thresholds."""
        if usage >= self.critical_threshold:
            return 'CRITICAL'
        elif usage >= self.warning_threshold:
            return 'WARNING'
        return 'OK' 
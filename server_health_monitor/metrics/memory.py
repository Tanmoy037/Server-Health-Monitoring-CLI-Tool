import psutil
from typing import Dict, Any

class MemoryMetrics:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.warning_threshold = config['memory']['warning_threshold']
        self.critical_threshold = config['memory']['critical_threshold']
    
    def get_metrics(self) -> Dict[str, Any]:
        """Collect memory metrics."""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'used': memory.used,
                    'free': memory.free,
                    'percent': memory.percent,
                    'status': self._get_status(memory.percent)
                },
                'swap': {
                    'total': swap.total,
                    'used': swap.used,
                    'free': swap.free,
                    'percent': swap.percent
                }
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
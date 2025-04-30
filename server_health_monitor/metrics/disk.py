import psutil
from typing import Dict, Any, List

class DiskMetrics:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.warning_threshold = config['disk']['warning_threshold']
        self.critical_threshold = config['disk']['critical_threshold']
        self.monitored_partitions = config['disk']['monitored_partitions']
    
    def get_metrics(self) -> Dict[str, Any]:
        """Collect disk metrics for monitored partitions."""
        try:
            disk_metrics = {}
            
            for partition in self.monitored_partitions:
                usage = psutil.disk_usage(partition)
                io_counters = psutil.disk_io_counters(perdisk=True)
                
                disk_metrics[partition] = {
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent,
                    'status': self._get_status(usage.percent),
                    'io': io_counters.get(partition, {})
                }
            
            return disk_metrics
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
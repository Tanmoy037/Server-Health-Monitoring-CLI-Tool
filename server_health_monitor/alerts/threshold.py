from typing import Dict, Any, List, Callable
from datetime import datetime

class ThresholdAlert:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._callbacks: List[Callable] = []
    
    def register_callback(self, callback: Callable) -> None:
        """Register a callback function to be called when an alert is triggered."""
        self._callbacks.append(callback)
    
    def check_metrics(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check metrics against thresholds and return alerts if any."""
        alerts = []
        
        # Check CPU metrics
        if 'cpu' in metrics:
            cpu_metrics = metrics['cpu']
            if cpu_metrics['status'] in ['WARNING', 'CRITICAL']:
                alerts.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'CPU',
                    'status': cpu_metrics['status'],
                    'value': cpu_metrics['usage_percent'],
                    'message': f"CPU usage is {cpu_metrics['usage_percent']}%"
                })
        
        # Check Memory metrics
        if 'memory' in metrics:
            memory_metrics = metrics['memory']['memory']
            if memory_metrics['status'] in ['WARNING', 'CRITICAL']:
                alerts.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'Memory',
                    'status': memory_metrics['status'],
                    'value': memory_metrics['percent'],
                    'message': f"Memory usage is {memory_metrics['percent']}%"
                })
        
        # Check Disk metrics
        if 'disk' in metrics:
            for partition, disk_metrics in metrics['disk'].items():
                if disk_metrics['status'] in ['WARNING', 'CRITICAL']:
                    alerts.append({
                        'timestamp': datetime.now().isoformat(),
                        'type': 'Disk',
                        'partition': partition,
                        'status': disk_metrics['status'],
                        'value': disk_metrics['percent'],
                        'message': f"Disk usage on {partition} is {disk_metrics['percent']}%"
                    })
        
        # Check Network metrics
        if 'network' in metrics:
            network_metrics = metrics['network']
            if network_metrics['status'] in ['WARNING', 'CRITICAL']:
                alerts.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'Network',
                    'status': network_metrics['status'],
                    'value': max(network_metrics['bytes_sent_kb'], network_metrics['bytes_recv_kb']),
                    'message': f"Network traffic is {max(network_metrics['bytes_sent_kb'], network_metrics['bytes_recv_kb']):.2f} KB/s"
                })
        
        # Notify callbacks if there are alerts
        if alerts:
            for callback in self._callbacks:
                try:
                    callback(alerts)
                except Exception as e:
                    print(f"Error in alert callback: {str(e)}")
        
        return alerts 
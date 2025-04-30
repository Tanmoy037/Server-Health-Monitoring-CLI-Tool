import psutil
from typing import Dict, Any
import time

class NetworkMetrics:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.warning_threshold = config['network']['warning_threshold']
        self.critical_threshold = config['network']['critical_threshold']
        self._last_io = None
        self._last_time = None
    
    def get_metrics(self) -> Dict[str, Any]:
        """Collect network metrics."""
        try:
            current_time = time.time()
            current_io = psutil.net_io_counters()
            
            if self._last_io is not None:
                time_diff = current_time - self._last_time
                bytes_sent = (current_io.bytes_sent - self._last_io.bytes_sent) / time_diff
                bytes_recv = (current_io.bytes_recv - self._last_io.bytes_recv) / time_diff
                
                # Convert to KB/s
                bytes_sent_kb = bytes_sent / 1024
                bytes_recv_kb = bytes_recv / 1024
                
                status = self._get_status(max(bytes_sent_kb, bytes_recv_kb))
            else:
                bytes_sent_kb = 0
                bytes_recv_kb = 0
                status = 'OK'
            
            self._last_io = current_io
            self._last_time = current_time
            
            return {
                'bytes_sent_kb': bytes_sent_kb,
                'bytes_recv_kb': bytes_recv_kb,
                'packets_sent': current_io.packets_sent,
                'packets_recv': current_io.packets_recv,
                'errin': current_io.errin,
                'errout': current_io.errout,
                'dropin': current_io.dropin,
                'dropout': current_io.dropout,
                'status': status
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'ERROR'
            }
    
    def _get_status(self, rate: float) -> str:
        """Determine status based on network rate thresholds."""
        if rate >= self.critical_threshold:
            return 'CRITICAL'
        elif rate >= self.warning_threshold:
            return 'WARNING'
        return 'OK' 
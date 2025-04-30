from typing import Any, Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

class MetricFormatter:
    def __init__(self):
        self.console = Console()
    
    def format_bytes(self, bytes: int) -> str:
        """Format bytes into human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"
    
    def format_percentage(self, value: float) -> str:
        """Format percentage value."""
        return f"{value:.2f}%"
    
    def format_status(self, status: str) -> Text:
        """Format status with appropriate color."""
        if status == 'CRITICAL':
            return Text(status, style="bold red")
        elif status == 'WARNING':
            return Text(status, style="bold yellow")
        elif status == 'OK':
            return Text(status, style="bold green")
        else:
            return Text(status, style="bold white")
    
    def create_metric_panel(self, title: str, metrics: Dict[str, Any]) -> Panel:
        """Create a rich panel for displaying metrics."""
        table = Table(show_header=False, box=None)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        for key, value in metrics.items():
            if key != 'status':
                if isinstance(value, (int, float)):
                    if '%' in key.lower():
                        value_str = self.format_percentage(value)
                    else:
                        value_str = str(value)
                else:
                    value_str = str(value)
                table.add_row(key, value_str)
        
        if 'status' in metrics:
            status = self.format_status(metrics['status'])
            return Panel(table, title=title, subtitle=status)
        return Panel(table, title=title) 
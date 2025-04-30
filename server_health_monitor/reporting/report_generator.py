from typing import Dict, Any, List
from datetime import datetime, timedelta
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel

class ReportGenerator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.console = Console()
        self.layout = Layout()
        self.layout.split_column(
            Layout(name="header"),
            Layout(name="metrics"),
            Layout(name="footer")
        )
        self.layout["header"].size = 3
        self.layout["footer"].size = 3
    
    def _create_metrics_table(self, metrics: Dict[str, Any]) -> Table:
        """Create a table with current metrics."""
        table = Table(title="Server Health Summary", show_header=True, box=None)
        
        # Add columns
        table.add_column("Metric", style="cyan", width=20)
        table.add_column("Value", style="magenta", width=15)
        table.add_column("Status", style="green", width=10)
        
        # CPU metrics
        if 'cpu' in metrics:
            cpu = metrics['cpu']
            table.add_row(
                "CPU Usage",
                f"{cpu['usage_percent']}%",
                cpu['status']
            )
        
        # Memory metrics
        if 'memory' in metrics:
            memory = metrics['memory']['memory']
            table.add_row(
                "Memory Usage",
                f"{memory['percent']}%",
                memory['status']
            )
        
        # Disk metrics
        if 'disk' in metrics:
            for partition, disk in metrics['disk'].items():
                table.add_row(
                    f"Disk Usage ({partition})",
                    f"{disk['percent']}%",
                    disk['status']
                )
        
        # Network metrics
        if 'network' in metrics:
            net = metrics['network']
            table.add_row(
                "Network Traffic",
                f"{max(net['bytes_sent_kb'], net['bytes_recv_kb']):.2f} KB/s",
                net['status']
            )
        
        return table
    
    def start_live_display(self):
        """Start the live display."""
        self.layout["header"].update(Panel("[bold blue]Server Health Monitor[/bold blue]"))
        self.layout["footer"].update(Panel("[yellow]Press Ctrl+C to exit[/yellow]"))
        return Live(self.layout, refresh_per_second=1)
    
    def update_metrics(self, metrics: Dict[str, Any]):
        """Update the metrics display."""
        table = self._create_metrics_table(metrics)
        self.layout["metrics"].update(Panel(table))
    
    def generate_historical_report(self, log_file: str, hours: int = 24) -> None:
        """Generate a historical report from log data."""
        try:
            log_path = Path(log_file)
            if not log_path.exists():
                self.console.print(f"[red]Log file not found: {log_file}[/red]")
                return
            
            # Read and parse log entries
            entries = []
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue
            
            # Filter entries for the specified time period
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_entries = [
                entry for entry in entries
                if datetime.fromisoformat(entry.get('timestamp', '')) > cutoff_time
            ]
            
            if not recent_entries:
                self.console.print(f"[yellow]No data found for the last {hours} hours[/yellow]")
                return
            
            # Generate summary statistics
            self.console.print(f"\n[bold]Historical Report (Last {hours} hours)[/bold]")
            
            # CPU statistics
            cpu_entries = [e['cpu'] for e in recent_entries if 'cpu' in e]
            if cpu_entries:
                avg_cpu = sum(e['usage_percent'] for e in cpu_entries) / len(cpu_entries)
                max_cpu = max(e['usage_percent'] for e in cpu_entries)
                self.console.print(f"\n[cyan]CPU Statistics:[/cyan]")
                self.console.print(f"Average Usage: {avg_cpu:.2f}%")
                self.console.print(f"Maximum Usage: {max_cpu:.2f}%")
            
            # Memory statistics
            memory_entries = [e['memory']['memory'] for e in recent_entries if 'memory' in e]
            if memory_entries:
                avg_mem = sum(e['percent'] for e in memory_entries) / len(memory_entries)
                max_mem = max(e['percent'] for e in memory_entries)
                self.console.print(f"\n[cyan]Memory Statistics:[/cyan]")
                self.console.print(f"Average Usage: {avg_mem:.2f}%")
                self.console.print(f"Maximum Usage: {max_mem:.2f}%")
            
            # Alert statistics
            alerts = [e for e in recent_entries if 'alerts' in e]
            if alerts:
                self.console.print(f"\n[cyan]Alert Statistics:[/cyan]")
                self.console.print(f"Total Alerts: {len(alerts)}")
                critical_alerts = sum(1 for a in alerts if any(alert['status'] == 'CRITICAL' for alert in a['alerts']))
                warning_alerts = sum(1 for a in alerts if any(alert['status'] == 'WARNING' for alert in a['alerts']))
                self.console.print(f"Critical Alerts: {critical_alerts}")
                self.console.print(f"Warning Alerts: {warning_alerts}")
        
        except Exception as e:
            self.console.print(f"[red]Error generating historical report: {str(e)}[/red]") 
#!/usr/bin/env python3

import argparse
import yaml
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
import time
from datetime import datetime

# Import all the components of our monitoring system
from server_health_monitor.metrics.cpu import CPUMetrics
from server_health_monitor.metrics.memory import MemoryMetrics
from server_health_monitor.metrics.disk import DiskMetrics
from server_health_monitor.metrics.network import NetworkMetrics
from server_health_monitor.logging.metrics_logger import MetricsLogger
from server_health_monitor.alerts.threshold import ThresholdAlert
from server_health_monitor.reporting.report_generator import ReportGenerator

def load_config(config_path: str) -> dict:
    """
    Load the configuration from a YAML file.
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        dict: Configuration dictionary
        
    Raises:
        SystemExit: If the configuration file cannot be loaded
    """
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description='Server Health Monitoring Tool')
    parser.add_argument('--config', '-c', 
                      default='config/default_config.yaml',
                      help='Path to configuration file')
    parser.add_argument('--interval', '-i', 
                      type=int,
                      help='Monitoring interval in seconds')
    parser.add_argument('--log-level', '-l',
                      choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                      help='Set logging level')
    return parser.parse_args()

def main():
    """
    Main entry point for the application.
    
    This function:
    1. Loads configuration
    2. Initializes all monitoring components
    3. Sets up the live display
    4. Runs the monitoring loop
    5. Handles cleanup and errors
    """
    # Parse command line arguments
    args = parse_args()
    
    # Load configuration from file
    config = load_config(args.config)
    
    # Initialize all monitoring components
    # Each component is responsible for collecting specific metrics
    cpu_metrics = CPUMetrics(config)
    memory_metrics = MemoryMetrics(config)
    disk_metrics = DiskMetrics(config)
    network_metrics = NetworkMetrics(config)
    
    # Initialize logging and alerting systems
    metrics_logger = MetricsLogger(config)
    threshold_alert = ThresholdAlert(config)
    report_generator = ReportGenerator(config)
    
    # Define a callback function for alerts
    # This function will be called whenever an alert is generated
    def alert_callback(alerts):
        """Handle alerts by logging them."""
        for alert in alerts:
            metrics_logger.log_alert(alert['message'], alert['status'])
    
    # Register the alert callback with the alert system
    threshold_alert.register_callback(alert_callback)
    
    # Start the monitoring loop with live display
    try:
        # The Live display context manager handles the real-time updates
        with report_generator.start_live_display() as live:
            while True:
                # Collect all metrics
                metrics = {
                    'cpu': cpu_metrics.get_metrics(),
                    'memory': memory_metrics.get_metrics(),
                    'disk': disk_metrics.get_metrics(),
                    'network': network_metrics.get_metrics(),
                    'timestamp': datetime.now().isoformat()
                }
                
                # Log the collected metrics
                metrics_logger.log_metrics(metrics)
                
                # Check for any alerts based on the metrics
                alerts = threshold_alert.check_metrics(metrics)
                
                # Update the live display with new metrics
                report_generator.update_metrics(metrics)
                
                # Wait for the next monitoring interval
                time.sleep(config['cpu']['check_interval'])
    
    # Handle user interruption (Ctrl+C)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    # Handle any other errors
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

# This is the standard Python idiom for making a script both importable and executable
if __name__ == "__main__":
    main()

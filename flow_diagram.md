# Server Health Monitoring Tool - Flow Diagram

```mermaid
flowchart TD
    %% Main Entry Point
    Start[Start Application] --> ParseArgs[Parse Command Line Arguments]
    ParseArgs --> LoadConfig[Load Configuration File]
    
    %% Component Initialization
    LoadConfig --> InitMetrics[Initialize Metrics Collectors]
    LoadConfig --> InitLogger[Initialize Metrics Logger]
    LoadConfig --> InitAlerts[Initialize Alert System]
    LoadConfig --> InitReports[Initialize Report Generator]
    
    %% Alert System Setup
    InitAlerts --> DefineCallback[Define Alert Callback]
    DefineCallback --> RegisterCallback[Register Callback with Alert System]
    
    %% Main Monitoring Loop
    RegisterCallback --> StartLiveDisplay[Start Live Display]
    StartLiveDisplay --> MonitoringLoop[Monitoring Loop]
    
    %% Metrics Collection
    MonitoringLoop --> CollectCPUMetrics[Collect CPU Metrics]
    MonitoringLoop --> CollectMemoryMetrics[Collect Memory Metrics]
    MonitoringLoop --> CollectDiskMetrics[Collect Disk Metrics]
    MonitoringLoop --> CollectNetworkMetrics[Collect Network Metrics]
    
    %% Data Processing
    CollectCPUMetrics --> AggregateMetrics[Aggregate All Metrics]
    CollectMemoryMetrics --> AggregateMetrics
    CollectDiskMetrics --> AggregateMetrics
    CollectNetworkMetrics --> AggregateMetrics
    
    %% Logging and Alerting
    AggregateMetrics --> LogMetrics[Log Metrics Data]
    AggregateMetrics --> CheckAlerts[Check for Alerts]
    
    %% Alert Processing
    CheckAlerts --> |Threshold Exceeded| TriggerAlert[Trigger Alert]
    TriggerAlert --> Callback[Execute Alert Callback]
    Callback --> LogAlert[Log Alert]
    
    %% Display Update
    AggregateMetrics --> UpdateDisplay[Update Live Display]
    
    %% Loop Control
    UpdateDisplay --> Sleep[Sleep for Interval]
    Sleep --> MonitoringLoop
    
    %% Exit Conditions
    MonitoringLoop --> |Ctrl+C| KeyboardInterrupt[Handle Keyboard Interrupt]
    MonitoringLoop --> |Error| HandleError[Handle Error]
    KeyboardInterrupt --> End[End Application]
    HandleError --> End

    %% Styling
    classDef process fill:#f9f,stroke:#333,stroke-width:2px
    classDef decision fill:#bbf,stroke:#333,stroke-width:2px
    classDef start fill:#9f9,stroke:#333,stroke-width:2px
    classDef end fill:#f99,stroke:#333,stroke-width:2px
    
    class Start,End start,end
    class ParseArgs,LoadConfig,InitMetrics,InitLogger,InitAlerts,InitReports,DefineCallback,RegisterCallback,StartLiveDisplay,CollectCPUMetrics,CollectMemoryMetrics,CollectDiskMetrics,CollectNetworkMetrics,AggregateMetrics,LogMetrics,CheckAlerts,TriggerAlert,Callback,LogAlert,UpdateDisplay,Sleep process
    class MonitoringLoop decision
```

## Flow Explanation

1. **Application Start**
   - The application begins by parsing command line arguments
   - Loads configuration from the specified YAML file

2. **Component Initialization**
   - Initializes all monitoring components (CPU, Memory, Disk, Network)
   - Sets up logging system
   - Configures alert system
   - Prepares report generator

3. **Alert System Setup**
   - Defines callback function for handling alerts
   - Registers the callback with the alert system

4. **Main Monitoring Loop**
   - Starts the live display
   - Enters continuous monitoring loop

5. **Metrics Collection**
   - Collects metrics from all system components
   - Aggregates the collected data

6. **Data Processing**
   - Logs the collected metrics
   - Checks for threshold violations
   - Triggers alerts if necessary

7. **Display Update**
   - Updates the live display with new metrics
   - Sleeps for the configured interval
   - Repeats the monitoring loop

8. **Exit Conditions**
   - Handles user interruption (Ctrl+C)
   - Manages error conditions
   - Performs cleanup before exit

## Key Components

- **Metrics Collection**: Gathers system metrics using psutil
- **Alert System**: Monitors thresholds and triggers alerts
- **Logging System**: Records metrics and alerts
- **Reporting System**: Provides real-time display and historical reports
- **Configuration**: Manages settings and thresholds 
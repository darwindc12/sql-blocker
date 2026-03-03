# SQL Blocker Monitor

SQL Blocker Monitor is a lightweight Python desktop application designed to automatically detect and resolve head blocking
session in Microsoft SQL Server. It provides a GUI interface for monitoring, configuration management, configuration management, 
and controlled automatic session termination based on configurable rules.

## Features

- Detects head blocking sessions
- Configurable kill threshold (in seconds)
- Dry-run mode (no actual kills)
- Excluded database support
- Exempt hostname support
- Scheduled monitoring window
- GUI-based control panel
- Logging to file and live GUI console

## Architecture Overview

- 'run.py' - Application entry point
- 'main.py' - Initializers GUI
- 'gui.py' - User Interface
- 'scheduler.py' - Background monitoring loop
- 'monitor.py' - Core blocker detection & kill logic
- 'sql_utils.py' - SQL server database operations
- 'config.py' - Configuration management
- 'logger.py' - Logging to file and GUI

## Requirements

- Python 3.14
- Microsoft SQL Server
- ODBC Driver for SQL Server
- Python Package
  - 'pyodbc'

## Key configuration sections:

### Database
- 'conn_str' - Sql Server connection string

### Monitor
- 'kill_threshold' - Seconds before blocking SPID is eligible for kill
- 'excluded_dbs' - Comma-separated list of databases to ignore
- 'dry_run' - true or false

### Schedule
- 'start_time' - Monitoring start time (HH:MM)
- 'stop_time' - Monitoring stop time (HH:MM)

## Safety Features

- Dry-run mode for testing
- Excluded database protection
- Exempt hostname protection
- Schedule-based execution window
- Detailed logging of all actions

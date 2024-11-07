# datadog_sync

Migration Guide: Datadog Synthetic Tests from Commercial to GovCloud
Introduction

This document provides a comprehensive guide on how to migrate Datadog synthetic tests from a commercial environment to a GovCloud environment using the datadog_sync tool. The datadog_sync repository facilitates the import and export of synthetic tests between different Datadog environments.

# Installation & Usage Instructions

1. Clone the Repository

First, clone the repository to your local machine:
```
git clone https://github.com/oanantap/datadog_sync.git
cd datadog_sync
```

2. Create a Virtual Environment

Create and activate a virtual environment to manage dependencies:
```
python -m venv venv
source venv/bin/activate
```

3. Install Dependencies

Install the required dependencies listed in the requirements.txt file:
```pip install -r requirements.txt```

4. Configuration File
The configuration file can be found at config/config.py that has all the configurations required for the migration.
export all the necessary required environment variables required for config.py
example:
```
export SOURCE_API_KEY='234234234xxxxx'
export SOURCE_APPLICATION_KEY='234234234xxxxx'
```

5. Usage
Import Synthetic Tests from Commercial Environment

To import synthetic tests from the commercial environment, run the following command:
```
python main.py import-tests
```

This command will:
	•	Validate the source API.
	•	Download synthetic tests from the commercial environment.
	•	Store the downloaded tests in the import_tests directory.

6. Export Synthetic Tests to GovCloud Environment

To export the previously imported synthetic tests to the GovCloud environment, run the following command:
```python main.py export-tests```

This command will:
	•	Load the synthetic tests from the import_tests directory.
  •	Downloads the existing tests from GovCloud automatically and checks if the tests are already exists or created manually to avoid duplicates.
	•	Export the tests to the GovCloud environment.

# Code Overview

## API Client
Handles interactions with Datadog APIs.
```File: clients/api_client.py```

## Synthetic Tests
Defines the structure and behavior of synthetic tests.

Files: ```synthetic_tests/synthetic_test.py, synthetic_tests/api_synthetic_test.py, synthetic_tests/synthetic_test_factory.py```

## Handlers
Manages the logic for importing and exporting synthetic tests.

Files: ```handlers/import_handler.py, handlers/export_handler.py```

## Services
Provides a simplified interface for importing and exporting operations.

Files: ```services/import_service.py, services/export_service.py```

## Utilities
Contains utility functions for file operations.

File: ```utils/file_utils.py```

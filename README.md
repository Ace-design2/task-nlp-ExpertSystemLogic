# AI Study Planner

## Description

The AI Study Planner is a Python-based application designed to help students organize their study schedules. It takes a topic or course code and a specified number of days, generating a structured study plan distributed across the available time. The system uses a local knowledge base of courses and topics to create these plans.

## Features

- **Smart Scheduling**: Distributes study topics evenly across the specified number of days.
- **Course & Topic Filtering**: Search by course code, title, or specific keywords to find relevant study materials.
- **Difficulty-Aware**: Takes into account the difficulty level of topics.
- **CLI Interface**: Easy-to-use command-line interface for quick schedule generation.
- **REST API**: FastAPI-based backend to integrate the planner into web or mobile applications.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/Ace-design2/task-nlp-ExpertSystemLogic.git
    cd task-nlp-ExpertSystemLogic
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Command Line Interface (CLI)

To generate a schedule using the CLI:

```bash
python main.py --query "CSC416" --days 5
```

Arguments:

- `--query`: The course code (e.g., CSC416) or topic keyword to study.
- `--days`: The number of days you want to plan for.

### API Server

To run the API server:

1.  Start the server:

    ```bash
    uvicorn api:app --reload
    ```

    The server will start at `http://127.0.0.1:8000`.

2.  Access the API documentation (Swagger UI) at:
    `http://127.0.0.1:8000/docs`

3.  Generate a schedule via HTTP Request:
    ```
    GET /schedule?query=AI&days=3
    ```

## Project Structure

- `main.py`: Entry point for the CLI application.
- `api.py`: FastAPI application entry point.
- `src/`: Source code directory.
  - `study_planner.py`: Core logic for data loading and schedule generation.
- `data/`: Directory containing the knowledge base.
  - `courses.json`: JSON file with course and topic data.
- `requirements.txt`: List of Python dependencies.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request for any improvements.

# AI Study Planner

## Description

The AI Study Planner is a Python-based application designed to help students organize their study schedules. It takes a topic or course code and a specified number of days, generating a structured study plan distributed across the available time. The system uses a local knowledge base of courses and topics to create these plans, ensuring a balanced workload based on topic difficulty.

## Features

- **Smart Scheduling**: Distributes study topics evenly across the specified number of days.
- **Course & Topic Filtering**: Search by course code (e.g., CSC416), title, or keywords.
- **Difficulty-Aware**: Balances daily study load by considering the difficulty level of topics.
- **Dual Interface**:
  - **CLI**: Quick schedule generation from the terminal.
  - **REST API**: FastAPI backend for integration with web/mobile apps.
- **JSON Output**: Returns structured data easy to parse and display.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Ace-design2/task-nlp-ExpertSystemLogic.git
    cd task-nlp-ExpertSystemLogic
    ```

2.  **Create a virtual environment (Recommended):**

    ```bash
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Command Line Interface (CLI)

Generate a schedule directly from your terminal:

```bash
python main.py --query "CSC416" --days 5
```

**Arguments:**

- `--query`: The course code (e.g., `CSC416`) or topic keyword.
- `--days`: The number of days to spread the study plan over.

### API Server

Run the FastAPI server to access the REST endpoints:

1.  **Start the server:**

    ```bash
    uvicorn api:app --reload
    ```

    The server will start at `http://127.0.0.1:8000`.

2.  **API Documentation:**

    Interactive documentation is available at:
    - Swagger UI: `http://127.0.0.1:8000/docs`
    - ReDoc: `http://127.0.0.1:8000/redoc`

3.  **Generate a Schedule (HTTP Request):**

    ```
    GET /schedule?query=AI&days=3
    ```

    **Example Response:**

    ```json
    {
      "query": "CSC416",
      "days": 5,
      "total_topics": 10,
      "total_hours": 30,
      "schedule": {
        "Day 1": {
          "topics": [
            {
              "course": "CSC416",
              "topic": "Introduction to Computer Security",
              "time": 2,
              "difficulty": 1
            }
          ],
          "total_hours": 2
        }
        // ... more days
      }
    }
    ```

## Project Structure

```
.
├── api.py              # FastAPI application entry point
├── main.py             # CLI application entry point
├── Procfile            # Heroku deployment configuration
├── requirements.txt    # Project dependencies
├── data/
│   └── courses.json    # Knowledge base containing courses and topics
└── src/
    └── study_planner.py # Core logic for data loading and scheduling
```

## Deployment

The project includes a `Procfile` configured for deployment on platforms like Heroku.

**Deploy to Heroku:**

1.  Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
2.  Login and create an app:
    ```bash
    heroku login
    heroku create your-app-name
    ```
3.  Deploy the code:
    ```bash
    git push heroku main
    ```
4.  Open the app:
    ```bash
    heroku open
    ```

## Troubleshooting

- **`FileNotFoundError: Data file not found`**:
  Ensure `data/courses.json` exists. The application relies on this file for the knowledge base.
- **`ModuleNotFoundError`**:
  Make sure you have activated your virtual environment and run `pip install -r requirements.txt`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

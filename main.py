import argparse
import json
import os
from src.study_planner import CourseDataLoader, StudyPlanner

def main():
    parser = argparse.ArgumentParser(description="AI Study Planner")
    parser.add_argument("--query", type=str, required=True, help="Course code or topic to study")
    parser.add_argument("--days", type=int, required=True, help="Number of days for the study plan")
    
    args = parser.parse_args()
    
    # Path to data
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "courses.json")
    
    try:
        loader = CourseDataLoader(data_path)
        planner = StudyPlanner(loader)
        
        result = planner.generate_schedule(args.query, args.days)
        
        print(json.dumps(result, indent=2))
        
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

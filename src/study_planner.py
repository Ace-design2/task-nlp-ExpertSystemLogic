import json
import math
from typing import List, Dict, Any, Optional

class CourseDataLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def get_courses(self) -> List[Dict[str, Any]]:
        return self.data.get("courses", [])

    def get_all_topics(self) -> List[Dict[str, Any]]:
        # This might not be needed if we filter per course, but good to have
        all_topics = []
        for course in self.get_courses():
            all_topics.extend(course.get("topics", []))
        return all_topics

class StudyPlanner:
    def __init__(self, data_loader: CourseDataLoader):
        self.loader = data_loader
        self.courses = self.loader.get_courses()

    def filter_topics(self, query: str) -> List[Dict[str, Any]]:
        query = query.lower()
        filtered_topics = []
        
        # We need to preserve the context of which course a topic belongs to
        # for display purposes maybe? For now just collecting topics.
        
        for course in self.courses:
            # Check if query matches Course Level, Semester, Code, or Program
            # E.g. "400L", "Second", "CSC416"
            course_match = (
                query in course.get("code", "").lower() or
                query in course.get("level", "").lower() or
                query in course.get("semester", "").lower() or
                query in course.get("program", "").lower() or
                query in course.get("title", "").lower()
            )
            
            if course_match:
                # If course matches, include ALL its topics
                # We might want to tag them with the course code if not already
                for topic in course.get("topics", []):
                    # Add course code to topic for context if not present (modified in memory)
                    if "course_code" not in topic:
                        topic["course_code"] = course.get("code")
                    filtered_topics.append(topic)
                continue
                
            # If course didn't match broadly, check individual topics
            for topic in course.get("topics", []):
                # Check topic name
                topic_match = False
                if query in topic["topic"].lower():
                    topic_match = True
                
                # Check keywords
                if not topic_match and any(query in kw.lower() for kw in topic.get("keywords", [])):
                    topic_match = True
                    
                if topic_match:
                    if "course_code" not in topic:
                        topic["course_code"] = course.get("code")
                    filtered_topics.append(topic)

        return filtered_topics

    def generate_schedule(self, query: str, days: int) -> Dict[str, Any]:
        relevant_topics = self.filter_topics(query)
        
        if not relevant_topics:
            return {
                "error": f"No topics found for query: {query}",
                "schedule": {}
            }

        total_study_time = sum(t["estimated_study_time"] for t in relevant_topics)
        
        if days <= 0:
             return {"error": "Days must be greater than 0"}

        # Simple distribution: bin packing into days
        schedule = {}
        for i in range(1, days + 1):
            schedule[f"Day {i}"] = {"topics": [], "total_hours": 0}
        
        target_hours_per_day = total_study_time / days
        
        current_day = 1
        current_day_hours = 0
        
        for topic in relevant_topics:
            # Simple greedy fill
            if current_day > days:
                current_day = days 

            schedule[f"Day {current_day}"]["topics"].append({
                "course": topic.get("course_code", "Unknown"),
                "topic": topic["topic"],
                "time": topic["estimated_study_time"],
                "difficulty": topic["difficulty"]
            })
            schedule[f"Day {current_day}"]["total_hours"] += topic["estimated_study_time"]
            current_day_hours += topic["estimated_study_time"]

            # Use a slightly relaxed threshold to avoid pushing small topics to next day unnecessarily
            # strictly checking >= target might leave days empty if we strictly adhere.
            # But the logic "if we EXCEEDED target, move to next" makes sense.
            # Let's stick to the previous verified logic for now.
            if current_day < days and current_day_hours >= target_hours_per_day:
                current_day += 1
                current_day_hours = 0

        return {
            "query": query,
            "days": days,
            "total_topics": len(relevant_topics),
            "total_hours": total_study_time,
            "schedule": schedule
        }

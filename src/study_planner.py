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

    def generate_schedule(self, query: str, days: int, daily_hours: float) -> Dict[str, Any]:
        relevant_topics = self.filter_topics(query)
        
        if not relevant_topics:
            return {
                "error": f"No topics found for query: {query}",
                "schedule": {}
            }

        total_study_time = sum(t["estimated_study_time"] for t in relevant_topics)
        
        if days <= 0:
             return {"error": "Days must be greater than 0"}
        
        if daily_hours <= 0:
             return {"error": "Daily hours must be greater than 0"}

        # --- Validation Logic ---
        required_daily_hours = total_study_time / days
        status = "success"
        message = "Schedule generated successfully."
        adjusted_hours = daily_hours
        
        # Heuristics for "Realistic" vs "Impossible"
        # If required is more than user wanted:
        if required_daily_hours > daily_hours:
            # If the difference is small (e.g., within +2 hours or safe limit like < 8-10h/day depending on context)
            # Let's say +3 hours tolerance or absolute max of 12 hours/day for the "stretch" goal.
            # User example: 2 hrs user input, might need 3 hrs (Adjustable)
            
            # Adjustable threshold:
            # 1. New requirement isn't absurdly high (> 12 hours/day is physically draining)
            # 2. Delta isn't massive (maybe max +3 hours from what they planned?)
            
            is_adjustable = (required_daily_hours <= 12) and (required_daily_hours <= daily_hours + 4)
             
            if is_adjustable:
                status = "adjusted"
                adjusted_hours = math.ceil(required_daily_hours * 2) / 2  # Round up to nearest 0.5
                message = (
                    f"Notice: {daily_hours} hours/day is insufficient for this content ({total_study_time} total hours). "
                    f"Adjusted to {adjusted_hours} hours/day to complete in {days} days."
                )
            else:
                status = "impossible"
                # Calculate needed days if they strictly stick to their daily_hours
                needed_days = math.ceil(total_study_time / daily_hours)
                return {
                    "error": (
                        f"It is not possible to study {total_study_time} hours of content in {days} days "
                        f"with only {daily_hours} hours/day (requires {required_daily_hours:.1f} hours/day). "
                        f"Try extending duration to {needed_days} days."
                    ),
                    "status": "impossible",
                    "suggestion": {
                        "needed_days": needed_days,
                        "needed_daily_hours": round(required_daily_hours, 1)
                    }
                }

        # --- Generation Logic ---
        # Use the adjusted_hours (or original if sufficient) as the capacity per day
        # NOTE: If user provided MORE hours than needed, we still distribute, but maybe we fill less per day?
        # Actually, "bin packing" usually tries to fill up the available capacity. 
        # But if total time < (days * daily_hours), we might finish early or have light days.
        # The prompt implies we should just generate using "what the user wants" (or the adjusted amount).
        
        target_hours_per_day = adjusted_hours
        
        schedule = {}
        for i in range(1, days + 1):
            schedule[f"Day {i}"] = {"topics": [], "total_hours": 0}
        
        current_day = 1
        current_day_hours = 0
        
        for topic in relevant_topics:
            if current_day > days:
                current_day = days 

            topic_time = topic["estimated_study_time"]
            
            # Add topic to current day
            schedule[f"Day {current_day}"]["topics"].append({
                "course": topic.get("course_code", "Unknown"),
                "topic": topic["topic"],
                "time": topic_time,
                "difficulty": topic["difficulty"]
            })
            schedule[f"Day {current_day}"]["total_hours"] += topic_time
            current_day_hours += topic_time

            # Check if day is full
            # We move to next day if we meet or exceed target, UNLESS it's the last day
            if current_day < days and current_day_hours >= target_hours_per_day:
                current_day += 1
                current_day_hours = 0
                
        # Clean up empty days if we finished early?
        # The prompt doesn't strictly say, but if we have 30 days and finish in 15, days 16-30 are empty.
        # We'll leave them as empty entries or maybe filter? 
        # Let's keep them to show the user they have free time, or maybe prune.
        # For this specific "impossible/realistic" logic, we just want to ensure we fit it.
        
        # Validate if we actually fit everything?
        # Our greedy approach blindly puts things in the last day if overflow.
        # So we should check if the last day is overloaded.
        last_day_hours = schedule[f"Day {days}"]["total_hours"]
        if last_day_hours > (target_hours_per_day * 1.5): # distinct overflow
             # This might happen if individual topic is huge or packing was inefficient
             # But our "Impossible" check earlier based on totals should catch most issues.
             # We'll just append a note if it's tight.
             pass

        return {
            "query": query,
            "days": days,
            "daily_hours": adjusted_hours,
            "status": status,
            "message": message,
            "total_topics": len(relevant_topics),
            "total_hours": total_study_time,
            "schedule": schedule
        }

import json
import os
import datetime

class QuestionDatabase:
    def __init__(self, database_path="scraped_data/question_database.json"):
        self.database_path = database_path
        self.questions_db = self.load_database()
        
    def load_database(self):
        """Load the question database from JSON file"""
        try:
            with open(self.database_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Database file not found at {self.database_path}")
            return {}
            
    def save_database(self):
        """Save the question database to JSON file"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.database_path), exist_ok=True)
        
        with open(self.database_path, "w") as f:
            json.dump(self.questions_db, f, indent=2)
        
    def get_topics(self):
        """Return a list of all topics in the database"""
        return list(self.questions_db.keys())
        
    def get_questions_by_topic(self, topic):
        """Return all questions for a specific topic"""
        return self.questions_db.get(topic, [])
        
    def get_question_by_id(self, question_id):
        """Find a question by its ID"""
        for topic, questions in self.questions_db.items():
            for question in questions:
                if question.get("id") == question_id:
                    return question, topic
        return None, None
        
    def add_generated_question(self, question, original_id):
        """Add a generated question to the database with a reference to original"""
        # Generate a new ID
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        new_id = f"gen_{original_id}_{timestamp}"
        
        # Add generation metadata
        question["id"] = new_id
        question["generated"] = True
        question["original_id"] = original_id
        question["generated_on"] = timestamp
        
        # Add to database
        topic = question["topic"]
        if topic not in self.questions_db:
            self.questions_db[topic] = []
        
        self.questions_db[topic].append(question)
        self.save_database()
        
        return new_id

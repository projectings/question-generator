import sys
import os

# Add the project root to the path so we can import the existing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from question_modifier import QuestionModifier

class QuestionGenerator:
    def __init__(self):
        self.modifier = QuestionModifier()
        
    def get_topics(self):
        """Get list of available topics"""
        return self.modifier.get_topics()
        
    def generate_by_topic(self, topic):
        """Generate a new question for a specific topic"""
        return self.modifier.create_modified_question(topic=topic)
        
    def generate_by_id(self, question_id):
        """Generate a new question based on a specific question ID"""
        return self.modifier.create_modified_question(original_id=question_id)
        
    def get_question_by_id(self, question_id):
        """Retrieve a specific question by ID"""
        for topic in self.get_topics():
            for question in self.modifier.get_questions_by_topic(topic):
                if question.get("id") == question_id:
                    return question
        return None
        
    def get_questions_by_topic(self, topic):
        """Get all questions for a specific topic"""
        return self.modifier.get_questions_by_topic(topic)

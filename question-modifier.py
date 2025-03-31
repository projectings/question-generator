import json
import os
import random
import re
import copy
import math
import sympy as sp

class QuestionModifier:
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
            # Create a sample database with common further maths topics
            return {
                "Complex Numbers": [
                    {
                        "id": "sample_complex_1",
                        "topic": "Complex Numbers",
                        "question_text": "Find the modulus and argument of the complex number z = 3 + 4i.",
                        "mark_scheme": "|z| = √(3² + 4²) = √25 = 5\narg(z) = tan⁻¹(4/3) = 0.9273 radians = 53.13°",
                        "total_marks": 3
                    }
                ],
                "Matrices": [
                    {
                        "id": "sample_matrices_1",
                        "topic": "Matrices",
                        "question_text": "Find the determinant of the matrix A = [[2, 1], [3, 4]].",
                        "mark_scheme": "det(A) = 2×4 - 1×3 = 8 - 3 = 5",
                        "total_marks": 2
                    }
                ],
                "Further Calculus": [
                    {
                        "id": "sample_calculus_1",
                        "topic": "Further Calculus",
                        "question_text": "Solve the differential equation dy/dx + 2y = 3e^(-2x), given that y = 1 when x = 0.",
                        "mark_scheme": "Using integrating factor e^(∫2dx) = e^(2x)\ne^(2x)dy/dx + 2e^(2x)y = 3\nd/dx(e^(2x)y) = 3\ne^(2x)y = 3x + C\ny = 3xe^(-2x) + Ce^(-2x)\nWhen x = 0, y = 1, so 1 = 0 + C, therefore C = 1\ny = 3xe^(-2x) + e^(-2x) = e^(-2x)(3x + 1)",
                        "total_marks": 6
                    }
                ]
            }
    
    def extract_numerical_values(self, text):
        """Extract numerical values from text, ignoring common markers"""
        # Find all numbers in the text
        numbers = re.findall(r'[-+]?\d*\.\d+|\d+', text)
        # Convert to appropriate type (int or float)
        values = []
        for num in numbers:
            if '.' in num:
                values.append(float(num))
            else:
                values.append(int(num))
        return values
    
    def modify_complex_number_question(self, question):
        """Modify a complex number question"""
        modified = copy.deepcopy(question)
        
        # Extract real and imaginary parts from question
        match = re.search(r'z\s*=\s*([-+]?\d+)\s*([-+])\s*(\d+)i', question["question_text"])
        if match:
            real_part = int(match.group(1))
            sign = match.group(2)
            imag_part = int(match.group(3))
            
            # Generate new values
            new_real = random.randint(1, 8) * (1 if random.random() > 0.5 else -1)
            new_imag = random.randint(1, 8) * (1 if random.random() > 0.5 else -1)
            new_sign = "+" if new_imag >= 0 else ""
            
            # Update question
            modified["question_text"] = re.sub(
                r'z\s*=\s*([-+]?\d+)\s*([-+])\s*(\d+)i',
                f'z = {new_real} {new_sign} {abs(new_imag)}i',
                question["question_text"]
            )
            
            # Update mark scheme
            modulus = math.sqrt(new_real**2 + new_imag**2)
            argument = math.atan2(new_imag, new_real)
            degrees = argument * 180 / math.pi
            
            modified["mark_scheme"] = (
                f"|z| = √({new_real}² + {abs(new_imag)}²) = √{new_real**2 + new_imag**2} = {modulus:.2f}\n"
                f"arg(z) = tan⁻¹({new_imag}/{new_real}) = {argument:.4f} radians = {degrees:.2f}°"
            )
            
        return modified
    
    def modify_matrix_question(self, question):
        """Modify a matrix-related question"""
        modified = copy.deepcopy(question)
        
        # Check if it's a determinant question
        if "determinant" in question["question_text"].lower():
            # Extract matrix values if possible
            matrix_match = re.search(r'A\s*=\s*\[\[(.*?)\],\s*\[(.*?)\]\]', question["question_text"])
            if matrix_match:
                # Generate new 2x2 matrix with values between -5 and 5
                a = random.randint(-5, 5)
                b = random.randint(-5, 5)
                c = random.randint(-5, 5)
                d = random.randint(-5, 5)
                
                # Ensure determinant isn't zero
                while a*d - b*c == 0:
                    d = random.randint(-5, 5)
                
                # Update question
                modified["question_text"] = re.sub(
                    r'A\s*=\s*\[\[(.*?)\],\s*\[(.*?)\]\]',
                    f'A = [[{a}, {b}], [{c}, {d}]]',
                    question["question_text"]
                )
                
                # Update mark scheme
                det = a*d - b*c
                modified["mark_scheme"] = f"det(A) = {a}×{d} - {b}×{c} = {a*d} - {b*c} = {det}"
        
        return modified
    
    def modify_differential_equation(self, question):
        """Modify a differential equation question"""
        modified = copy.deepcopy(question)
        
        # Check if it's a first-order linear DE
        if "dy/dx" in question["question_text"] and "=" in question["question_text"]:
            # Try to extract the coefficient and right-hand side
            de_match = re.search(r'dy/dx\s*\+\s*(\d+)y\s*=\s*(\d+)e\^\((-?\d+)x\)', question["question_text"])
            if de_match:
                coeff = int(de_match.group(1))
                rhs_coeff = int(de_match.group(2))
                exp_coeff = int(de_match.group(3))
                
                # Generate new coefficients
                new_coeff = random.choice([1, 2, 3, 4])
                new_rhs_coeff = random.choice([2, 3, 4, 5])
                new_exp_coeff = -new_coeff  # To maintain solvability
                
                # Update question
                modified["question_text"] = re.sub(
                    r'dy/dx\s*\+\s*(\d+)y\s*=\s*(\d+)e\^\((-?\d+)x\)',
                    f'dy/dx + {new_coeff}y = {new_rhs_coeff}e^({new_exp_coeff}x)',
                    question["question_text"]
                )
                
                # Extract initial condition if present
                initial_match = re.search(r'y\s*=\s*(\d+)\s*when\s*x\s*=\s*(\d+)', question["question_text"])
                initial_y = 1
                initial_x = 0
                if initial_match:
                    initial_y = int(initial_match.group(1))
                    initial_x = int(initial_match.group(2))
                    
                    # Maybe modify initial condition
                    if random.random() > 0.5:
                        initial_y = random.choice([1, 2, 3, 4, 5])
                        modified["question_text"] = re.sub(
                            r'y\s*=\s*(\d+)\s*when\s*x\s*=\s*(\d+)',
                            f'y = {initial_y} when x = {initial_x}',
                            modified["question_text"]
                        )
                
                # Update mark scheme (simplified for brevity)
                C = initial_y
                if new_exp_coeff == -new_coeff:
                    C = initial_y - (new_rhs_coeff * initial_x)
                
                modified["mark_scheme"] = (
                    f"Using integrating factor e^(∫{new_coeff}dx) = e^({new_coeff}x)\n"
                    f"e^({new_coeff}x)dy/dx + {new_coeff}e^({new_coeff}x)y = {new_rhs_coeff}\n"
                    f"d/dx(e^({new_coeff}x)y) = {new_rhs_coeff}\n"
                    f"e^({new_coeff}x)y = {new_rhs_coeff}x + C\n"
                    f"When x = {initial_x}, y = {initial_y}, so {initial_y} = {0 if initial_x == 0 else new_rhs_coeff*initial_x} + C, therefore C = {C}\n"
                    f"y = {new_rhs_coeff}xe^({new_exp_coeff}x) + {C}e^({new_exp_coeff}x) = e^({new_exp_coeff}x)({new_rhs_coeff}x + {C})"
                )
        
        return modified
    
    def modify_question(self, question):
        """Modify a question based on its topic"""
        topic = question["topic"]
        
        if "Complex Numbers" in topic:
            return self.modify_complex_number_question(question)
        elif "Matrices" in topic:
            return self.modify_matrix_question(question)
        elif "Calculus" in topic:
            return self.modify_differential_equation(question)
        else:
            # For other topics, perform a simpler modification
            # by changing numerical values
            modified = copy.deepcopy(question)
            
            # Extract numbers from the question
            values = self.extract_numerical_values(question["question_text"])
            
            if values:
                # Create new values (±20% of original)
                new_values = [round(val * random.uniform(0.8, 1.2), 2) for val in values]
                
                # Replace values in the question
                new_text = question["question_text"]
                for i, val in enumerate(values):
                    # Replace exact value matches only
                    pattern = r'\b' + re.escape(str(val)) + r'\b'
                    new_text = re.sub(pattern, str(new_values[i]), new_text, count=1)
                
                modified["question_text"] = new_text
                
                # Note: In a real implementation, you would need to also update the mark scheme
                # This would require more sophisticated understanding of the mathematical context
                modified["mark_scheme"] += "\n[Mark scheme would need to be updated with new values]"
            
            return modified
    
    def get_questions_by_topic(self, topic=None):
        """Get questions filtered by topic"""
        if topic:
            return self.questions_db.get(topic, [])
        else:
            # Return all questions
            all_questions = []
            for topic_questions in self.questions_db.values():
                all_questions.extend(topic_questions)
            return all_questions
    
    def get_topics(self):
        """Get list of available topics"""
        return list(self.questions_db.keys())
    
    def create_modified_question(self, original_id=None, topic=None):
        """Create a modified version of a question"""
        if original_id:
            # Find question by ID
            for topic_questions in self.questions_db.values():
                for question in topic_questions:
                    if question["id"] == original_id:
                        return self.modify_question(question)
            
            print(f"Question with ID {original_id} not found")
            return None
        
        elif topic:
            # Pick a random question from the topic
            questions = self.get_questions_by_topic(topic)
            if questions:
                return self.modify_question(random.choice(questions))
            else:
                print(f"No questions found for topic: {topic}")
                return None
        
        else:
            # Pick a random question from any topic
            all_topics = self.get_topics()
            if all_topics:
                random_topic = random.choice(all_topics)
                return self.create_modified_question(topic=random_topic)
            else:
                print("No questions available in the database")
                return None

if __name__ == "__main__":
    modifier = QuestionModifier()
    
    # Test the modifier
    topics = modifier.get_topics()
    print(f"Available topics: {topics}")
    
    if topics:
        # Generate a modified question for a random topic
        topic = random.choice(topics)
        print(f"\nGenerating modified question for topic: {topic}")
        modified = modifier.create_modified_question(topic=topic)
        
        if modified:
            print("\nOriginal Question:")
            original_questions = modifier.get_questions_by_topic(topic)
            original = random.choice(original_questions)
            print(original["question_text"])
            print("\nModified Question:")
            print(modified["question_text"])

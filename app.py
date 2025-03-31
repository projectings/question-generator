from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import json
from database import QuestionDatabase
from question_generator import QuestionGenerator

os.makedirs("scraped_data", exist_ok=True)
app = Flask(__name__)
app.secret_key = os.urandom(24)  # for flash messages

# Initialize database and question generator
db = QuestionDatabase()
generator = QuestionGenerator()

@app.route('/')
def index():
    """Homepage showing all available topics"""
    topics = generator.get_topics()
    return render_template('index.html', topics=topics)

@app.route('/topic/<topic>')
def topic_questions(topic):
    """Show all questions for a specific topic"""
    questions = generator.get_questions_by_topic(topic)
    return render_template('topic.html', topic=topic, questions=questions)

@app.route('/question/<question_id>')
def view_question(question_id):
    """View a specific question"""
    question, topic = db.get_question_by_id(question_id)
    
    # If not found in the database, try getting it from the generator
    if question is None:
        question = generator.get_question_by_id(question_id)
        if question:
            topic = question.get("topic")
    
    if question is None:
        flash("Question not found!")
        return redirect(url_for('index'))
        
    return render_template('question.html', question=question, topic=topic)

@app.route('/generate', methods=['POST'])
def generate_question():
    """Generate a new question based on an existing one"""
    question_id = request.form.get('question_id')
    
    if not question_id:
        flash("No question ID provided!")
        return redirect(url_for('index'))
    
    # Generate new question
    new_question = generator.generate_by_id(question_id)
    
    if not new_question:
        flash("Failed to generate a new question!")
        return redirect(url_for('view_question', question_id=question_id))
    
    # Save to database
    new_id = db.add_generated_question(new_question, question_id)
    
    # Redirect to the new question
    return redirect(url_for('view_question', question_id=new_id))

@app.route('/api/generate/<question_id>', methods=['GET'])
def api_generate_question(question_id):
    """API endpoint to generate a new question"""
    new_question = generator.generate_by_id(question_id)
    
    if not new_question:
        return jsonify({"error": "Failed to generate question"}), 404
    
    # Save to database
    new_id = db.add_generated_question(new_question, question_id)
    
    return jsonify({
        "success": True,
        "question_id": new_id,
        "question": new_question
    })

if __name__ == '__main__':
    app.run(debug=True)

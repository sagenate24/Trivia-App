import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

# Returns categories formatted in JSON format
def format_categories(categories):
  formatted_categories = {}

  for categorie in categories:
    formatted_categories.update({ categorie.id: categorie.type })

  return formatted_categories


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {'origins': '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/api/categories')
  def get_categories():
    categories = Category.query.order_by(Category.id).all()

    if len(categories) == 0:
      abort(404)

    return jsonify({
      'categories': format_categories(categories)
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/api/questions')
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    categories = Category.query.order_by(Category.id).all()

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': format_categories(categories),
      'current_category': None
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)

      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        'success': True,
        'id': question_id
      }) 
    except:
      abort(424)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/api/questions', methods=['POST'])
  def create_questions():
    try:
      body = request.get_json()

      question = body.get('question', None)
      answer = body.get('answer', None)
      difficulty = body.get('difficulty', None)
      category = body.get('category', None)
      
      new_question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
      new_question.insert()

      return jsonify({
        'success': True,
        'id': new_question.id
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/api/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    formatted_search_term = "%{}%".format(body.get('search_term', None))
    all_questions = Question.query.filter(Question.question.ilike(formatted_search_term)).all()
    questions_paginated = paginate_questions(request, all_questions)

    return jsonify({
      'questions': questions_paginated,
      'total_questions': len(all_questions),
      'current_category': None
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/api/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    current_category = Category.query.get(category_id)

    if current_category is None:
      abort(404)

    questions_by_category = Question.query.filter_by(category=category_id).all()
    questions_paginated = paginate_questions(request, questions_by_category)

    return jsonify({
      'questions': questions_paginated,
      'total_questions': len(questions_by_category),
      'current_category': current_category.type
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/api/quizzes', methods=['POST'])
  def get_next_question():
    body = request.get_json()
    prev_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)

    # Get list of questions by the quiz category id
    questions_by_category = Question.query.filter_by(category=quiz_category['id']).all()
    # Format questions into JSON format
    formatted_questions = [question.format() for question in questions_by_category]

    # Get any random question from the list
    if len(prev_questions) == 0:
      return jsonify({
        'question': random.choice(formatted_questions)
      })
    else:
      # Get a random question that has not yet been answered
      filtered_questions = []

      # Add questions to the list when their ids are not within the list of prev_questions 
      for question in formatted_questions:
        if question['id'] not in prev_questions:
          filtered_questions.append(question)

      # No more questions to answer
      if len(filtered_questions) == 0:
        return jsonify({
          'question': None
        })
      else:
        return jsonify({
          'question': random.choice(filtered_questions)
        })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  
  return app

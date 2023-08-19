import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(req, selection):
    page = req.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,PATCH"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            categoriesDict = {}

            for category in categories:
                categoriesDict[category.id] = category.type

            return jsonify({
                'success': True,
                'categories': categoriesDict
            }), 200
        except:
            abort(404)


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=['GET'])
    def get_questions():
        try:
            selection = Question.query.all()
            total_questions = len(selection)
            pagianted_questions = paginate_questions(request, selection)
            print(len(pagianted_questions))

            if len(pagianted_questions) == 0:
                abort(404)
            
            categories = Category.query.all()
            categoriesDict = {}
            for category in categories:
                categoriesDict[category.id] = category.type

            return jsonify({
                'success': True,
                'questions': pagianted_questions,
                'total_questions': total_questions,
                'categories': categoriesDict
            }), 200
        except Exception as e:
            print(e)
            abort(400)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            currentQuestions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': True
            }), 200
        except Exception as e:
            print(e)
            abort(404)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=['POST'])
    def create_question():
        body = request.get_json()
        print(request.data)

        # get new data, none if not enterd
        newQuestion = body.get('question', None)
        newAnswer = body.get('answer', None)
        newCategory = body.get('category', None)
        newDifficulty = body.get('difficulty', None)

        if newQuestion is None or newAnswer is None or newCategory is None or newDifficulty is None:
            abort(400)

        try:
            question = Question(newQuestion, newAnswer, newCategory, newDifficulty)

            question.insert()

            selection = Question.query.all()
            currentQuestions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'question_id': question.id,
                'questions': currentQuestions,
                'total_questions': len(selection)
            }), 201
        except Exception as e:
            print(e)
            abort(404)



    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/search", methods=['POST'])
    def search():
        body = request.get_json()
        search = body.get('searchTerm')

        if search is None:
            abort(404)

        questions = Question.query.filter(
            Question.question.ilike('%'+search+'%')).all()

        if questions:
            currentQuestions = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'questions': currentQuestions,
                'total_questions': len(questions)
            }), 200
        else:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions", methods=['GET'])
    def get_question_by_category(category_id):
        category = Category.query.filter_by(id=category_id).one_or_none()
        
        if category:
            questionsInCategory = Question.query.filter_by(category=str(category_id)).all()
            print(questionsInCategory)
            currentQuestions = paginate_questions(request, questionsInCategory)

            return jsonify({
                'success': True,
                'questions': currentQuestions,
                'total_questions': len(questionsInCategory),
                'current_category': category.type
            }), 200
        else:
            abort(404)

    
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/play', methods=['POST'])
    def quiz():
        body = request.get_json()
        quizCategory = body.get('quiz_category')
        previousQuestion = body.get('previous_questions')

        try:
            if (quizCategory['id'] == 0):
                questionsQuery = Question.query.all()
            else:
                questionsQuery = Question.query.filter_by(category=quizCategory['id']).all()

            randomIndex = random.randint(0, len(questionsQuery)-1)
            nextQuestion = questionsQuery[randomIndex]

            while nextQuestion.id not in previousQuestion:
                nextQuestion = questionsQuery[randomIndex]
                return jsonify({
                    'success': True,
                    'question': {
                        "answer": nextQuestion.answer,
                        "category": nextQuestion.category,
                        "difficulty": nextQuestion.difficulty,
                        "id": nextQuestion.id,
                        "question": nextQuestion.question
                    },
                    'previousQuestion': previousQuestion
                }), 200

        except Exception as e:
            print(e)
            abort(404)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_req_err(err):
        return jsonify({
            'success': False,
            'message': 'Bad request',
            'error': 400
        }), 400
    
    @app.errorhandler(422)
    def unprocessable(err):
        return jsonify({
            'success': False,
            'message': 'Unprocessable',
            'error': 422
        }), 422
    
    @app.errorhandler(500)
    def internal_server_err(err):
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': 500
        }), 500
    
    @app.errorhandler(404)
    def not_found(err):
        return jsonify({
            'success': False,
            'message': 'Resource not found',
            'error': 404
        }), 404
    
    @app.errorhandler(405)
    def invalid_method(error):
        return jsonify({
            "success": False,
            'error': 405,
            "message": "Method not allowed"
        }), 405

    return app


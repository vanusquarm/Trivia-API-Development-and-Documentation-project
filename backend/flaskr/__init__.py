import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def retrieve_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            return jsonify({
                'categories': {category.id:category.type for category in categories},
                'success': True,
                'total_categories': len(categories)
            }) 
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
    @app.route('/questions')
    def retrieve_questions():
        page_index = request.args.get('page', 1, type=int)
        questions_selection = Question.query.order_by(Question.id).paginate(page_index, QUESTIONS_PER_PAGE).items
        categories_selection = Category.query.order_by(Category.id).all()        
        
        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions_selection],
            'categories': {category.id:category.type for category in categories_selection},
            'total_questions': 5,
            'current_category': categories_selection[0].type
        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            page_index = request.args.get('page', 1, type=int)
            questions_selection = Question.query.order_by(Question.id).paginate(page_index, QUESTIONS_PER_PAGE).items

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': [question.format() for question in questions_selection],
                'total_questions': len(questions_selection)
            })  
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        page_index = request.args.get('page', 1, type=int)

        new_question = body.get('question', '')
        new_answer = body.get('answer', '')
        new_category = body.get('category', 1)
        new_difficulty = body.get('difficulty', 1)
        search_term = body.get('searchTerm', None)

        if (new_question == '' or new_answer == '') and search_term is None:
            abort(422)

        try:
            if search_term:
                questions_selection = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search_term))).paginate(page_index,QUESTIONS_PER_PAGE).items

                return jsonify({
                    'success': True,
                    'questions': [question.format() for question in questions_selection],
                    'total_questions': len(questions_selection)
                })
            else:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()

                page_index = request.args.get('page', 1, type=int)
                questions_selection = Question.query.order_by(Question.id).paginate(page_index, QUESTIONS_PER_PAGE).items


                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': [question.format() for question in questions_selection],
                    'total_questions': len(questions_selection)
                }), 201
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def retrieve_category_questions(category_id):
        try:
            page_index = request.args.get('page', 1, type=int)
            category = Category.query.filter(Category.id == category_id).one_or_none()

            if category is None:
                abort(404)

            questions_selection = Question.query.order_by(Question.id).filter(Question.category == category_id).paginate(page_index, QUESTIONS_PER_PAGE).items
            

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions_selection],
                'total_questions': len(questions_selection),
                'current_category': category.type
            })
        except:
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

    @app.route("/quizzes", methods=["POST"])
    def retrieve_quizzes():
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')
        random_question = None

        try:
            if quiz_category is None or quiz_category['id'] == 0:
                valid_questions_selection = [question.format() for question in Question.query.all()]
            else:
                valid_questions_selection = [question.format() for question in Question.query.filter(Question.category == quiz_category['id']).all()]
                        
            valid_questions = []
            for question in valid_questions_selection:
                if question['id'] not in previous_questions:
                    valid_questions.append(question)
                
            if (len(valid_questions) > 0):
                random_question = random.choice(valid_questions)
                    
            return jsonify({
                'success': True,
                'question': random_question,
                'previous_questions': previous_questions
            })   
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    # ERROR HANDLERS
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Resource Not Found"}),
            404
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422)
    
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({"success": False, "error": 400, "message": "bad request"}), 400)

    @app.errorhandler(500)
    def bad_request(error):
        return (jsonify({"success": False, "error": 500, "message": "Internal server error"}), 500)


    return app


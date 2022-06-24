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



    return app


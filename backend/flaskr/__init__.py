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
    
    return app


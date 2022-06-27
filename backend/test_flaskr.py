import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category, database_user, database_password


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.getenv("DATABASE_NAME_TEST",'trivia_test')
        self.database_path = f"postgres://{self.database_user}:{self.database_password}@localhost:5432/{self.database_name}"
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "Test question",
            "answer": "Test answer",
            "difficulty": 1,
            "category": 1
        }
        self.question_422 = {
            "answer": "Test answer",
            "category": 7
        }

        self.quiz = {
            "quiz_category": {"id": 1, "type": "Science"},
            "previous_questions": [20, 21]
        }

        self.quiz_422 = {
            "quiz_category": {},
            "previous_questions": {}
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_retrieve_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_categories'], 6)

    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual('success', True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['total_questions'], QUESTIONS_PER_PAGE)
        self.assertTrue(data['current_category'])
    
        
    def test_delete_question(self):
        question = Question.query.first().format()
        res = self.client().delete(f"/questions/{question['id']}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], question['id'])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_create_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_search_questions(self):
            res = self.client().post("/questions", json={"searchTerm": "who"})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)
            self.assertTrue(data['questions'])
            self.assertTrue(data['total_questions'])
        
    def test_retrieve_category_questions(self):
        res = self.client.get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], "Science")
        
    def test_retrieve_quizzes(self):
        res = self.client().post("/quizzes", json=self.quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertNotEqual(data['question']['id'], 20)
        self.assertNotEqual(data['question']['id'], 21)


    '''
    Testing for expected errors 

    '''
    def test_404_not_found_retrieve_categories(self):
        res = self.client().get("/categories/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_404_not_found_retrieve_questions(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_404_not_found_delete_question(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_422_unprocessable_create_question(self):
        res = self.client().post("/questions", json=self.question_422)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], "unprocessable")
        self.assertTrue(data['error'])

    def test_404_not_found_retrieve_category_questions(self):
        res = self.client().get("/categories/1000/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_422_unprocessable_retrieving_quizzes(self):
        res = self.client().post("/quizzes", json=self.quiz_422)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], "unprocessable")
        self.assertTrue(data['error'])
    

    '''
    Alternatively, all resources can be grouped and tested under the following test cases.
    '''
    def test_404_not_found(self):
        pass
    def test_422_unprocessable(self):
        pass
    def test_400_bad_request(self):
        pass
    def test_500_server_error(self):
        pass




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
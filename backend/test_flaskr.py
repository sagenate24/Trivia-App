import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 2,
            'category': 2
        }

        self.quiz_data = {
            'previous_questions': [1],
            'quiz_category': {
                'id': 1
            }
        }

        self.quiz_data_failure = {
            'previous_questions': [1],
            'quiz_category': {
                'id': 1000
            }
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

    # Test GET all categories
    def test_get_categories (self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])
    
    def test_404_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test GET a paginated list of questions
    def test_get_paginated_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['questions']))

    def test_404_get_paginated_questions(self):
        res = self.client().get('/api/questions?page=1000', json={'rating': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test DELETE question by id
    # def test_delete_question_by_id(self):
    #     res = self.client().delete('/api/questions/5')
    #     data = json.loads(res.data)

    #     question = Question.query.get(5)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['id'], 5)
    #     self.assertEqual(question, None)
    
    # TODO find out why this isnt throwing a 404
    def test_422_delete_question_by_id(self):
        res = self.client().delete('/api/questions/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Test POST create new questions
    def test_create_questions(self):
        res = self.client().post('/api/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertTrue(data['id'])
    
    def test_400_create_questions(self):
        res = self.client().post('/api/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_search_questions(self):
        res = self.client().post('/api/questions/search', json={'search_term': 'Anne'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertFalse(data['current_category'])

    def test_404_search_questions(self):
        res = self.client().post('/api/questions/search', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_by_category(self):
        res = self.client().get('/api/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_get_questions_by_category(self):
        res = self.client().get('/api/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_next_question(self):
        res = self.client().post('/api/quizzes', json=self.quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_404_get_next_question(self):
        res = self.client().post('/api/quizzes', json=self.quiz_data_failure)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['question'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
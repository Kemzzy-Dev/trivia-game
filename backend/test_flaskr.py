import os
from unicodedata import category
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
        self.database_path = 'postgresql://{}:{}@{}/{}'.format("kemzzy","12345","localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

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
    def test_get_categories(self):
        res=self.client().get('/categories')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_questions(self):
        res=self.client().get('/questions', follow_redirects=True)
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_get_questions_by_category(self):
        res=self.client().get('/categories/5/questions', follow_redirects=True)
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_function(self):
        data=json.dumps(dict(search_term = 'what'))
        res=self.client().post('/search_questions', follow_redirects=True, data=data, content_type='application/json')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_question(self):
        jsonData=json.dumps(dict(question = 'what is my name', answer='ekemini', category='3', difficulty='8'))
        res=self.client().post('/add_question', follow_redirects=True, data=jsonData, content_type='application/json')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['Message'], 'Question added successfully')
    
    def test_delete_question(self):
        res=self.client().delete('/questions/18', follow_redirects=True)#use an already existing index so as not to get an failed test
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_questions_by_category_error(self):
        res=self.client().get('/categories/400/questions', follow_redirects=True)
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_question_error(self):
        res=self.client().delete('/questions/220', follow_redirects=True)
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_quizzes(self):
        jsonData=json.dumps(dict(previous_questions=[], quiz_category=dict(id=3)))
        res=self.client().post('/quizzes', data=jsonData, content_type='application/json', follow_redirects=True)
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
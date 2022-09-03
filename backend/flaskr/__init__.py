import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

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
        # Accepted headers for the api
        response.headers.add(
            'Access-Control-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

    # Define a function to handle the pagination of the results returned
    # The item should be a list
    def paginate(request, item):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        return item[start:end]

    # To get the current id of all the items in the items list
    # The items should be stored in a list
    def get_current_category(itemsList):
        categoryLists = []
        for item in itemsList:
            get_category = item['category']  # get a category from an item
            cat_id = Category.query.get(get_category).type
            categoryLists.append(cat_id)

        return categoryLists
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    # WORKS and test written
    # DONE
    @app.route('/categories')
    def category():
        # Get all categories
        categories = Category.query.all()
        # Make the categories and object for the frontend
        category_obj = {category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            "categories": category_obj,
        })

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
    # WORKS and test written
    # DONE
    @app.route('/questions')
    def questions():
        questions = Question.query.all()
        categories = Category.query.all()
        category_obj = {category.id: category.type for category in categories}

        format_questions = [question.format() for question in questions]
        paginated_questions = paginate(request, format_questions)

        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "categories": category_obj,
            "currentCategory": get_current_category(format_questions),
            'total_questions': len(format_questions),
        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    # """
    # WORKS and test written
    # DONE
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete(question_id):
        # Get the question to be deleted
        question = Question.query.get(question_id)
        # Check if question exists or not
        if question is not None:
            # check for errors while making changes to the database
            try:
                question.delete()
                return jsonify({
                    'success': True
                })
            except BaseException:
                question.rollback()
                abort(500)
            finally:
                question.close()
        else:
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
    # Works and test written
    # DONE
    @app.route('/add_questions', methods=['POST'])
    def new_question():
        body = request.get_json()
        # get all the data from the request body
        question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')

        if question and answer and category is not None:
            try:
                # save the question in the database
                save_question = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty)
                save_question.insert()
                return jsonify({
                    'success': True,
                })
            except BaseException:
                save_question.rollback()
                abort(500)
            finally:
                save_question.close()
        else:
            abort(400)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    # works and test written
    # DONE
    @app.route('/search_questions', methods=['POST'])
    def search_questions():
        body = request.get_json()
        searchTerm = body.get('searchTerm')
        print(searchTerm)

        if searchTerm is not None:
            # query the database with the search term
            questions = Question.query.filter(
                Question.question.ilike(
                    '%{}%'.format(searchTerm)))
            # Makes the question a list
            format_questions = [question.format() for question in questions]
            paginate_questions = paginate(request, format_questions)

            if format_questions != []:
                return jsonify({
                    'success': True,
                    'questions': paginate_questions,
                    'total_questions': len(format_questions),
                    'currentCategory': get_current_category(format_questions)
                })
            else:
                abort(404)
        else:
            abort(400)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    # WORKS and test written
    # DONE
    @app.route('/categories/<int:category_id>/questions')
    def question_by_id(category_id):
        # gets questions based on the giving category
        questions = Question.query.filter_by(category=category_id)

        # Makes the questions a list
        format_questions = [question.format() for question in questions]
        paginate_questions = paginate(request, format_questions)

        # Checks the list if it's empty and returns a response
        if paginate_questions != []:
            return jsonify({
                'success': True,
                "questions": paginate_questions,
                'currentCategory': get_current_category(format_questions),
                'total_questions': len(format_questions)
            })
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
    # WORKS AND TESTED
    # Done
    @app.route('/quizzes', methods=['POST'])
    def play():
        body = request.get_json()
        prev_question = body.get('previous_questions')
        getCategory = body.get('quiz_category')

        question = []
        try:
            # When user clicks all it returns 0 for the category
            # Since category does not have a key of 0 we instead return all the
            # questions
            getCategoryId = getCategory['id']
            if getCategoryId != 0:
                questions = Question.query.filter(
                    Question.category == getCategoryId).all()
            else:
                questions = Question.query.all()

            # formats the question to a list
            format_questions = [question.format() for question in questions]

            # getting our questions by id and checking if our questions are
            # present in the previous questions list
            for questionID in format_questions:
                if questionID['id'] not in prev_question and Question.query.filter():
                    question.append(questionID)

            # To check if they are any available questions in a category
            if question != []:
                # Get a random question from the list of available questions
                random_question = random.choice(question)
                return jsonify({
                    'success': True,
                    "question": random_question,
                })
            else:
                return jsonify({
                    "success": True,
                })
        except TypeError:
            abort(400)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unproccessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Request was received but cannot be processed by the server"
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed for this endpoint!"
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Opps! Something was wrong with that request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error! Couldn't process the request"
        }), 500

    return app

# trivia-game-for-udacity-nanodegree
The trivia game is a fun and interactive game made to test users on their knowledge in various fields of human endeavour. It was created with the intention of having fun while also learning and discovering facts.
  The trivia game is made up of two main folders:
  
  - **backend**
  
  - **frontend**
  
The backend includes the files and dependencies for running the api and databases while the frontend is a flask app responsible for serving the data from the backend to the users.
    
# Getting started

### Prerequisites & Installation

  The project requires the following to be installed:
- python version 3.7 and above
- pip
- node and npm
- virtualenv(optional)

To begin using the app, refer to the setup guidelines below:
### Backend
Navigate into the backend folder and initialize your virtual environment. Once this is done you can proceed to installing the dependencies by running `pip install -r requirements.txt` or `pip3 install -r requirements.txt`. Proceed to setup your postgres database and linking it to the app through the models.py file. 
  Running the `psql trivia < trivia.psql` command will prepopulate the database with a set of demo questions which can be deleted later. To run the application use :
  ```
  export FLASK_APP=flaskr 
  export FLASK_ENV=development
  flask run
  ```
This command will start up a localhost at port 5000 and use the ____init____.py file within our flaskr folder as the default flask app.

### Frontend
The frontend is created with the react framework and will not load successfully if the backend is not setup first. To install the frontend dependencies, navigate to the frontend directory and run:
  `npm install`
This will install the depencies and create a node_modules folder within the frontend directory. Run `npm start` to begin the frontend in developer mode.

## Test
The application has some pre-written tests in the test_flaskr.py file. Use the commands below in other to run tests:
```
  dropdb trivia_test
  createdb trivia_test
  psql trivia_test < trivia.psql
  python test_flaskr.py
```
The first command above drops the trivia_test database if it already exits. If not it can be skipped. The second command creates a new test database(this is done do that our original database items will not be tempered with). The third command prepopulates our test database with dummy data so that tests can be ran on it and the fourth command simply starts the tests.
Note: Remember to set the test database name in your test_flaskr.py file

# API REFERENCE
## Getting started
Base url: The application is hosted locally, so there is no base url for the project.

Authentication/Api keys: Both are absent for the app. 

## Errors:

Errors are given in JSON format. 

Example:
```
{
"success": False, 
"error": 405,
"message": "Method not allowed for this endpoint!"
}
  
{
  "success": False, 
  "error": 404,
  "message": "Not found"
}
```
 
Messages:

404:Not found

422:Unprocessable

405:method_not_allowed

400:Bad Request

500:Server error

## ENDPOINTS

### `GET '/categories'`

  -Returns a dictionary of which the keys are the ids and value is a string of the category
  
  -Request arguments: None
  
  -Returns an object of category type and success
  
Example: `curl http://127.0.0.1:5000/categories`
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": True
}
```

### `GET '/questions'`

-Returns an object of success, paginated questions(10 questions per page), categories (object), current categories of the returned questions(list) and total questions(integer)

-No arguments 

Example: `curl http://127.0.0.1:5000/questions`
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": [
        "Entertainment",
        "Entertainment",
        "Sports",
        "Geography",
        "Geography",
        "Geography",
        "Art",
        "Art",
        "Art",
        "Art"
    ],
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": True,
    "total_questions": 19
}
```

### `DELETE '/questions/{question_id}'`

-Deletes a particular question based on the id given

-Requires an id argument

-Returns a success key of true

Example: `curl -X DELETE http://127.0.0.1:5000/questions/12`
```
{
    "success":True
}
```

### `POST '/add_questions'`

-Adds a new question to the database 

-Body of the request should include question(string), answer(string), category(integer) and difficulty(integer).

-Returns a success value of True

Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who is ada lovelace in the world of computing?", "answer":"Ada lovelace is regarded to be the very first programmer", "difficulty":"4", "category": "5"}'`
```
{
"success":True
}
```

### `POST '/search_questions'`

-Searches for question with the search term

-Requires a 'searchTerm' body in the request

-Returns a response of success, paginated questions(10 per page), total_questions(int), current category of the response questions(list).

Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'`
```
{
    "current_category": [
        "Entertainment"
    ],
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success":True,
    "total_questions": 1
}
```

### `GET '/categories/{category id}/questions'`

-Gets the questions of a particular category

-Requires a category id argument

-Returns a success value, paginated questions(10 per page), current category of the returned questions(list) and a total questions object(int).

Example: `curl http://127.0.0.1:5000/categories/3/questions`
```
{
    "current_category": [
        "Geography",
        "Geography"
    ],
    "questions": [
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": True,
    "total_questions": 2
}
```

### `POST '/quzzies'`

-Enables users to play the game

-Requires a request body of previous_questions(list) and quiz_category(object) with key of id and value(int).

-Returns success and question(object)

Example: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category": {"id": 6}, "previous_questions": []}'`
```
{
    "category": "Sports",
    "question": {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    "success": true,
}
```

# Acknowledgements
The awesome team at Udacity and all my fellow students who helped through their hints and beautiful ideas, soon to be full stack extraordinaires!


# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Reference

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints

#### GET '/api/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with attributes, `success: True` and categories. categories contains a object of id: category_string key:value pairs.
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

#### GET '/api/questions'
- Fetches a paginated list of questions based on the page parameter passed. default questions per page is 10.
- Request Parameters: `page: Number`
- Returns: An object with 
```
{
  'success': True,
  'questions': [],
  'total_questions': Number,
  'categories': [],
  'current_category': None
}
```

#### DELETE '/api/questions/<int:question_id>'
- Removes a question from the database by id. 404 will be thrown if their is no question matching the given question_id.
- Request Parameters: question id slug.
- Returns: An object with `success: True` and the id of the deleted question
```
{
  'success': True,
  'id': Number
}
```

#### POST '/api/questions'
- Create a new question. All request arguments are required and will throw a 400 if missing.
- Request Arguments: { question: String, answer: String, difficulty: Number, category: Number}
- Returns: An object with `success: True` and the id of the deleted question
```
{
  'success': True,
  'id': Number
}
```

#### POST '/api/questions/search'
- Search for questions by a search term. the search term is only searching based on the question and not the answer. 404 will be thrown if not found.
- Request Arguments: { search_term: String }
- Returns a paginated list of questions and the total number of questions.
```
{
  'questions': [],
  'total_questions': Number,
  'current_category': None
}
```

#### GET '/api/categories/<int:category_id>/questions'
- Fetches a paginated list of questions by category id. 404 will be thrown if the id passed does not match a category in the database.
- Request Parameters: category is slug.
- Returns the current category type, paginated questions and the total number of questions
```
{
  'questions': [],
  'total_questions': Number,
  'current_category': String
}
```

#### POST '/api/quizzes'
- Fetches a random question based on the category and previous questions sent. will return a 404 if their are no questions by the category specified.
- Request Arguments: { previous_questions: [List of question ids], quiz_category: Number/category_id}.
- Returns one random question that is not specified in the `previous_questions` list argument. Returns None when the previous_questions list contains all questions for the given category.
```
{
  question: Object -OR- None
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
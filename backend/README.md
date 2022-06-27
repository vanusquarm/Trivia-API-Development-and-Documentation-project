# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Endpoints Documentation

Documentation of available API endpoints including the URL, request parameters, and the response body

<!-- ### Documentation Example -->

### `GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Sample: `curl http://localhost:3000/categories`

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### `GET '/questions'`

- Fetches a dictionary of questions.
- Request Arguments: `page` (optional and defaults to 1)
- Returns:
  - `success`: True or False.
  - `questions`: List of questions where each question is a key/value pairs object containing `id`, `question`, `category` and `diffficulty` with a max length of 10.
  - `total_questions`: the total number of quesitons in the database.
  - `current_category`: string.
  - `categories`: dictionary of the available categories.
- Sample: `curl http://localhost:3000/questions?page=1`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Science",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {...}
  ],
  "success": true,
  "total_questions": 18
}
```

### `DELETE '/questions/<int:question_id>'`

- Removes a particular question from the database.
- Request Arguments: `question_id` (required)
- Returns:
  - `success`: True or False.
  - `questions`: List of questions where each question is a key/value pairs object containing `id`, `question`, `category` and `diffficulty` with a paginated max length of 10.
  - `total_questions`: the total number of quesitons in the database.
  - `deleted`: question_id.
- Sample: `curl -X DELETE http://localhost:3000/questions/2`

```json
{
  "deleted": 2,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {...}
  ],
  "success": true,
  "total_questions": 17
}
```

### `POST '/questions'`

- Creates a question in the database and also handles the search feature.
- Request body:

  - `question`: String (required).
  - `answer`: String (required)
  - `difficulty`: Number (optional defaults to 1).
  - `category`: Number (optional defaults to 1 - `Science`).
  - `searchTerm`: String - if included it will not create a question but rather return search results

- Returns:
  - `success`: True or False.
  - `questions`: List of questions where each question is a key/value pairs object containing `id`, `question`, `category` and `diffficulty` with a paginated max length of 10.
  - `total_questions`: the total number of quesitons in the database.
  - `created`: id.
- Sample: `curl -X POST http://localhost:3000/questions -H "Content-Type: application/json" -d '{"question": "When did Nigeria gain her independence", "answer": "1960"}'`

```json
{
  "created": 21,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {...}
  ],
  "success": true,
  "total_questions": 17
}
```

### `GET '/categories/<int:category_id>/questions'`

- Fetches a dictionary of questions in a particular category.
- Request Arguments: `page` (optional and defaults to 1)
- Returns:
  - `success`: True or False.
  - `questions`: List of questions where each question is a key/value pairs object containing `id`, `question`, `category` and `diffficulty` with a max length of 10.
  - `total_questions`: the total number of quesitons in the database.
  - `current_category`: string.
  - `categories`: dictionary of the available categories.
- Sample: `curl http://localhost:3000/categories/1/questions`

```json
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {...}
  ],
  "success": true,
  "total_questions": 18
}
```

### `POST '/quizzes'`

- Fetches a random question from the database.
- Request body: `quiz_category` (optional - if not provided returns a questions from any category)
- Returns:
  - `success`: True or False.
  - `question`: A random question.
  - `previous_questions`: An arrray of IDs of previous questions.
- Sample: `curl http://localhost:3000/categories/1/questions`

```json
{
  "previous_questions": [1, 4, 11],
  "question": {
    "answer": "Apollo 13",
    "category": 5,
    "difficulty": 4,
    "id": 2,
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  },
  "success": true
}
```

## Errors handling:

The API typical will throw three major error status code `404 - Not found`, `422 - Unprocessable` or `400 - Bad request`. The will return the following key/value pairs JSON content:

- `success`: False.
- `error`: error code number.
- `message`: error message string giving a brief description of the kind of error.

Sample:

```JSON
{
    "success": false,
    "error": 404,
    "message": "Resource Not Found"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

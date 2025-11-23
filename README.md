# Late Show API

The Late Show API is a Flask-based RESTful backend application designed to manage Episodes, Guests, and Appearances for a talk show environment.

This project demonstrates practical application of backend software development concepts including:

- API design and routing
- Database modeling and relationships
- Input validation and error handling
- Test-driven development practices
- Structured project architecture

It was developed as part of a backend engineering curriculum focused on building and testing Python web applications using Flask.

---

## Installation Requirements

Before running the project, ensure the following are installed:

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment support (`venv`)
- SQLite (included with most Python installations)

Recommended environment:

- Linux or Windows Subsystem for Linux (WSL)
- Windows 10/11 or macOS

---

## Project Overview

The API enables clients to:

- Retrieve all episodes
- Retrieve a specific episode including its appearances
- Retrieve all guests
- Create guest appearance records linked to episodes
- Delete episodes and automatically remove related appearances

Data is stored using SQLite and accessed through SQLAlchemy ORM to provide a relational structure with cascade behavior.

---

## Learning Outcomes

By working on this project, the following competencies were developed:

- Setting up and configuring a Flask application
- Implementing MVC architecture in a Python project
- Designing and consuming RESTful API endpoints
- Modeling relational databases using SQLAlchemy
- Applying validations and enforcing business rules
- Handling common API errors and returning meaningful responses
- Writing automated tests using pytest
- Using fixtures and isolated test environments
- Understanding cascade delete behavior in relational models

---

## Project Structure

```
LATE-SHOW-API/
├── server/
│   ├── app.py
│   ├── models.py
│   ├── seed.py
│   └── testing/
│       ├── conftest.py
│       ├── app_test.py
│       └── models_test.py
├── requirements.txt
├── README.md
└── .gitignore
```
The structure follows the MVC pattern:

- Models: Database logic and structure
- Controllers: Route handling and request processing
- Views: JSON output returned to clients

---

## Key Features

- RESTful design principles
- Many-to-many relationship through a join model (Appearance)
- Rating validation (1–5)
- Cascade delete support
- Structured JSON responses
- Error messages for invalid requests
- Full automated test suite

---

## Setup Instructions

1. Clone the repository

git clone <repository-url>
cd LATE-SHOW-API

2. Create and activate a virtual environment

Linux / Mac:
python3 -m venv env
source env/bin/activate

Windows:
python -m venv env
env\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

---

## Running the Application

cd server
python app.py

Access the API using:

http://localhost:5555

---

## API Endpoints

GET /episodes  
Returns a list of episodes

GET /episodes/<id>  
Returns a single episode including its appearances

DELETE /episodes/<id>  
Deletes an episode and its related appearances  
Returns status 204

GET /guests  
Returns a list of guests

POST /appearances  
Creates a new appearance record

Example request body:
{
  "rating": 5,
  "episode_id": 2,
  "guest_id": 1
}

Invalid inputs return a 400 response with error details.

---

## Database and Relationships

Database: SQLite

Models:

- Episode
- Guest
- Appearance

Relationships:

- Episode has many Appearances
- Guest has many Appearances
- Appearance belongs to both Episode and Guest

Cascade rules ensure that deleting an episode automatically removes its appearances.

---

## Testing

Automated tests verify:

- Model relationships
- Validation logic
- Cascade deletes
- API endpoint behavior
- Status codes and responses

Run tests using:
```
pytest -x
```
Expected result:
```
15 passed
```
---

## Troubleshooting

If the application fails to start:

- Ensure the virtual environment is activated
- Verify dependencies are installed using `pip install -r requirements.txt`
- Confirm Python 3 is being used

If tests do not run or collect:

- Check that pytest is installed
- Ensure the `testing` folder contains test files
- Confirm `pytest.ini` is present in the project root

If database issues occur:

- Delete any existing `app.db` file
- Rerun the application or tests to recreate the database

---

## Future Improvements

Potential enhancements for future development include:

- Updating the API to support PUT/PATCH for editing records
- Adding authentication and authorization
- Implementing pagination for episode and guest lists
- Moving seed data to a CLI management script
- Adding OpenAPI/Swagger documentation
- Integrating a frontend interface
- Deploying the API to a cloud platform such as Render or Heroku

These improvements would expand the functionality and make the API suitable for production use.

---

## License

This project is licensed under the MIT License.



---

## Author

Rebecca Kibisu  

---
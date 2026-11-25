# Gather & Graze — Community Recipe Sharing Platform

A responsive full-stack recipe community application built for the CodeNova Full Stack Development Task 4.

## Features
- Create and publish recipes with title, cuisine, prep time, difficulty, ingredients and steps
- Explore recipe cards with category tags
- Search reactively by recipe title, ingredient or cuisine
- Filter by Breakfast, Lunch, Dessert and Vegan
- Recipe detail view with interactive ingredient checklist
- Like counter updates through the backend
- SQLite database persistence
- REST API, input validation and responsive mobile layout
- Sample recipes included on first run

## Technology stack
- Frontend: HTML5, CSS3, Vanilla JavaScript (Fetch API)
- Backend: Python, Flask (REST API)
- Database: SQLite

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended):
   - Windows: `py -m venv venv` then `venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the app: `python app.py`
6. Open `http://127.0.0.1:5001`

The database `recipes.db` is created automatically on first run with sample recipes.

## REST API
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/recipes` | List/search/filter recipes |
| POST | `/api/recipes` | Create a recipe |
| GET | `/api/recipes/<id>` | Get recipe details |
| POST | `/api/recipes/<id>/like` | Increment like counter |
| DELETE | `/api/recipes/<id>` | Delete a recipe |

## Database model
`recipes`: id, title, cuisine, category, prep_time, difficulty, ingredients, steps, likes, created_at.

## Before submission
- Run the app and test recipe creation, search, filters, details, ingredient checklist and likes.
- Add your own screenshots to a `screenshots/` folder and embed them here.
- Push this folder to a public GitHub repository.
- Include your own name and internship details if required.

## Note
This is a student project starter implementation. Review and understand the code, test it in your environment, and make any changes required by your internship evaluator before submitting.

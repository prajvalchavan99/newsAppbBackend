# News Search Web Application

## Description
This project is a web-based application built with Django. It allows users to search for news articles from around the world based on keywords. Users can also view the results of their previous searches, sort search results based on the date published, and filter articles by various criteria.

## Project Setup Instructions

### Backend (Django):
1. Clone the repository: `git clone <repository_url>`
2. Navigate to the backend directory: `cd backend`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
5. Install required packages: `pip install -r requirements.txt`
6. Apply database migrations: `python manage.py migrate`
7. Create a superuser for accessing the admin panel: `python manage.py createsuperuser`
8. Start the Django development server: `python manage.py runserver`

### News API
Get your API key from [News API](https://newsapi.org/) and replace `YOUR_API_KEY` in the Django project settings.

## Time Taken
The project was completed over a span of 2 days. Approximately 20 hours were spent in total, divided between backend development, frontend development, API integration, and testing.

## Overall Experience
Working on this project was a rewarding experience. It provided an opportunity to apply various technologies and implement features like API integration, user authentication, and dynamic content rendering. Debugging and problem-solving skills were honed throughout the process. Collaboration between frontend and backend teams was smooth, leading to a seamless integration of components.

## Challenges Faced
1. Storing fetched data in cache to avoid refetching of data with api
2. integrating APi with proper conditions and filters

## Screenshots
1. Home page
![Home Page](https://github.com/prajvalchavan99/newsAppbBackend/blob/main/screenshots/home.png)

2.Login Page
![Login](https://github.com/prajvalchavan99/newsAppbBackend/blob/main/screenshots/login.png)

3.Register Page
![Register](https://github.com/prajvalchavan99/newsAppbBackend/blob/main/screenshots/register.png)

4. Search News
![Search News](https://github.com/prajvalchavan99/newsAppbBackend/blob/main/screenshots/search-news.png)

5. My Searches
![My Searches](https://github.com/prajvalchavan99/newsAppbBackend/blob/main/screenshots/my-searches.png)

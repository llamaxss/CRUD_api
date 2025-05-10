# CRUD API

This project is a simple implementation of a CRUD (Create, Read, Update, Delete) API. It allows users to perform basic operations on a dataset through HTTP requests.

## Project Structure
- `src/blog_api` - Contains the API logic for managing blog posts, including endpoints for creating, reading, updating, and deleting blog posts.
- `src/chat_api` - Contains the API logic for chat api.
- `src/db` - Contains database models, services, and utilities for interacting with the database.
- `src/util` - Contains utility functions and helpers, such as database session management and data formatting.
- `src/weather_api` - Contains the API logic for fetching weather data using city names or geolocation coordinates.
- `main.py` - The main entry point for the Flask application.
- `ui/` - Contains the React-based frontend.

## Installation

- Install dependencies:
    ```bash
    cd CRUD_api
    uv sync
    cd ui
    npm install
    ```

## Usage

1. Start the backend server:
    ```bash
    uv run -m src.main
    ```

2. Access the API at `http://localhost:5055`.
3. Start frontend server in `ui/`

## API Endpoints
- **GET api/blog/post?id=<post_id>** - Get a single blog post by ID.
- **GET api/blog/posts** - Retrieve all blog posts.
- **POST api/blog/post** - Create a new blog post.
- **PUT api/blog/post** - Edit an existing blog post.
- **DELETE api/blog/post?id=<post_id>** - Delete a blog post by ID.


- **POST /api/chat/auth** - Login a user with username and password.
- **POST /api/chat/logout** - Logs out the current session.
- **POST /api/chat/register** - Register a new user account.


- **GET /api/weather/city?cityName=<cityName>** - This endpoint retrieves the weather information for a specific city based on the city name.
- **GET /api/weather/geocode?lat=<lat>&lon=<lon>** - This endpoint retrieves the weather information based on geographic coordinates.

# Flask Application for Building A Mind website.

This is a Flask-based web application for managing users, research papers, and authors. It includes features for user sign-up, sign-in, profile management, adding and listing research papers, and adding new authors.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

4. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Database Setup

1. **Create the database and tables:**

    ```sh
    python create_db.py
    ```

2. **Populate the database with sample data:**

    ```sh
    python populate_db.py
    ```

## Running the Flask App

1. **Start the Flask app:**

    ```sh
    python app.py
    ```

2. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:5000`.

## API Endpoints

### User Endpoints

- **Sign Up:**

    ```http
    POST /api/signup
    ```

    **Request Body:**

    ```json
    {
        "user_email": "string",
        "user_first_name": "string",
        "user_last_name": "string",
        "user_password": "string"
    }
    ```

    **Expected Response:**

    ```json
    {
        "message": "User created successfully",
        "token": "string"
    }
    ```

- **Sign In:**

    ```http
    POST /api/signin
    ```

    **Request Body:**

    ```json
    {
        "user_email": "string",
        "user_password": "string"
    }
    ```

    **Expected Response:**

    ```json
    {
        "message": "Signed in successfully",
        "token": "string"
    }
    ```

- **Get Profile:**

    ```http
    GET /api/profile
    ```

    **Headers:**

    ```http
    Authorization: Bearer <token>
    ```

    **Expected Response:**

    ```json
    {
        "user_id": "integer",
        "user_email": "string",
        "user_first_name": "string",
        "user_last_name": "string",
        "user_image": "string",
        "user_registration_time": "string",
        "user_access": "string",
        "university": "string",
        "collections_paper_ids": "string"
    }
    ```

- **Update Profile:**

    ```http
    PUT /api/profile
    ```

    **Headers:**

    ```http
    Authorization: Bearer <token>
    ```

    **Request Body:**

    ```json
    {
        "user_first_name": "string",
        "user_last_name": "string",
        "user_image": "string"
    }
    ```

    **Expected Response:**

    ```json
    {
        "message": "Profile updated successfully"
    }
    ```

### Research Papers Endpoints

- **List Papers:**

    ```http
    GET /api/papers
    ```

    **Expected Response:**

    ```json
    [
        {
            "paper_id": "integer",
            "paper_created_by_user_id": "integer",
            "short_paper_title": "string",
            "short_description": "string",
            "preview_image": "string",
            "authors": [
                {
                    "author_id": "integer",
                    "first_name": "string",
                    "last_name": "string",
                    "image": "string",
                    "website": "string"
                }
            ],
            "paper_pdf_link": "string"
        }
    ]
    ```

- **Get Paper by ID:**

    ```http
    GET /api/papers/<int:paper_id>
    ```

    **Expected Response:**

    ```json
    {
        "paper_id": "integer",
        "paper_created_by_user_id": "integer",
        "short_paper_title": "string",
        "short_description": "string",
        "preview_image": "string",
        "authors": [
            {
                "author_id": "integer",
                "first_name": "string",
                "last_name": "string",
                "image": "string",
                "website": "string"
            }
        ],
        "paper_pdf_link": "string",
        "paper_description": "string"
    }
    ```

- **Add Paper:**

    ```http
    POST /api/papers
    ```

    **Headers:**

    ```http
    Authorization: Bearer <token>
    ```

    **Request Body:**

    ```json
    {
        "short_paper_title": "string",
        "short_description": "string",
        "preview_image": "string",
        "authors_ids": [list of author ids],
        "paper_pdf_link": "string",
        "paper_description": "string"
    }
    ```

    **Expected Response:**

    ```json
    {
        "message": "Paper added successfully",
        "paper_id": "integer"
    }
    ```

### Authors Endpoints

- **Add Author:**

    ```http
    POST /api/authors
    ```

    **Headers:**

    ```http
    Authorization: Bearer <token>
    ```

    **Request Body:**

    ```json
    {
        "author_first_name": "string",
        "author_last_name": "string",
        "author_image": "string",
        "author_website": "string"
    }
    ```

    **Expected Response:**

    ```json
    {
        "message": "Author added successfully",
        "author_id": "integer"
    }
    ```

### Collections Endpoints

- **Get User Paper Collections:**

    ```http
    GET /api/collections
    ```

    **Headers:**

    ```http
    Authorization: Bearer <token>
    ```

    **Expected Response:**

    ```json
    {
        "collections_paper_ids": [integer]
    }
    ```

- **Get Papers from Collections:**

    ```http
    GET /api/collections/papers
    ```

    **Headers:**

    ```http
    Authorization: Bearer <token>
    ```

    **Expected Response:**

    ```json
    [
        {
            "paper_id": "integer",
            "paper_created_by_user_id": "integer",
            "short_paper_title": "string",
            "short_description": "string",
            "preview_image": "string",
            "authors": [
                {
                    "author_id": "integer",
                    "first_name": "string",
                    "last_name": "string",
                    "image": "string",
                    "website": "string"
                }
            ],
            "paper_pdf_link": "string"
        }
    ]
    ```

- **Add Paper to Collections:**

    ```http
    POST /api/collections
    ```

    **Headers:**

    ```http
    Authorization: Bearer <token>
    ```

    **Request Body:**

    ```json
    {
        "paper_id": "integer"
    }
    ```

    **Expected Response:**

    ```json
    {
        "message": "Paper added to collections successfully"
    }
    ```

- **Remove Paper from Collections:**

    ```http
    DELETE /api/collections
    ```

    **Headers:**

    ```http
    Authorization: Bearer <token>
    ```

    **Request Body:**

    ```json
    {
        "paper_id": "integer"
    }
    ```

    **Expected Response:**

    ```json
    {
        "message": "Paper removed from collections successfully"
    }
    ```

## Database Structure

The database used in this application is `bam.db`. It contains the following tables:

### Users Table

- **Table Name:** `users`
- **Description:** Stores user information.

| Column Name              | Data Type | Constraints                           | Description                           |
|--------------------------|-----------|--------------------------------------|---------------------------------------|
| `user_id`                | INTEGER   | PRIMARY KEY, AUTOINCREMENT            | Unique identifier for each user.      |
| `user_email`             | TEXT      | NOT NULL, UNIQUE                      | User's email address.                 |
| `user_first_name`        | TEXT      | NOT NULL                              | User's first name.                    |
| `user_last_name`         | TEXT      | NOT NULL                              | User's last name.                     |
| `user_password`          | TEXT      | NOT NULL                              | User's hashed password.               |
| `user_image`             | TEXT      |                                      | URL or path to user's profile image.  |
| `user_registration_time` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP             | Timestamp of user registration.       |
| `user_access`            | TEXT      | CHECK(user_access IN ('user', 'team', 'admin')), NOT NULL | User's access level (user, team, admin). |
| `university`             | TEXT      |                                      | Name of the university the user is associated with. |
| `collections_paper_ids`  | TEXT      |                                      | Comma-separated list of paper IDs in the user's collection. |

### Research Papers Table

- **Table Name:** `research_papers`
- **Description:** Stores information about research papers.

| Column Name              | Data Type | Constraints                           | Description                           |
|--------------------------|-----------|--------------------------------------|---------------------------------------|
| `paper_id`               | INTEGER   | PRIMARY KEY, AUTOINCREMENT            | Unique identifier for each paper.     |
| `paper_created_by_user_id` | INTEGER | NOT NULL, FOREIGN KEY REFERENCES `users(user_id)` | User who created the paper.           |
| `short_paper_title`      | TEXT      | NOT NULL                              | Short title of the paper.             |
| `short_description`      | TEXT      | NOT NULL                              | Short description of the paper.       |
| `preview_image`          | TEXT      |                                      | URL or path to the paper's preview image. |
| `authors_ids`            | TEXT      | NOT NULL                              | Comma-separated list of author IDs.   |
| `paper_pdf_link`         | TEXT      | NOT NULL                              | URL link to the paper's PDF.          |
| `paper_description`      | TEXT      | NOT NULL                              | Full description of the paper.        |

### Authors Table

- **Table Name:** `authors`
- **Description:** Stores information about authors.

| Column Name              | Data Type | Constraints                           | Description                           |
|--------------------------|-----------|--------------------------------------|---------------------------------------|
| `author_id`              | INTEGER   | PRIMARY KEY, AUTOINCREMENT            | Unique identifier for each author.    |
| `author_first_name`      | TEXT      | NOT NULL                              | Author's first name.                 |
| `author_last_name`       | TEXT      | NOT NULL                              | Author's last name.                  |
| `author_image`           | TEXT      |                                      | URL or path to author's image.       |
| `author_website`         | TEXT      |                                      | URL to the author's personal website. |

## Notes for database setup

- Ensure that `user_email` is unique in the `users` table.
- `paper_created_by_user_id` in `research_papers` references `user_id` in the `users` table.
- `authors_ids` in `research_papers` is a comma-separated list of `author_id` values from the `authors` table.



## General Notes

- Ensure that you update the `SECRET_KEY` in `app.py` to a secure value.
- Replace `<repository-url>` and `<repository-directory>` with the actual URL and directory name of your repository.

## Issues / Enhancements

- Add Publication date to the research papers table
- Add List of Tags to the research papers
- Add update paper method
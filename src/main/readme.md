# App Documentation

## Introduction

The app is a Flask-based web application that provides a reward program for users who make purchases on an online shopping store. It allows users to earn additional discounts and rewards when they purchase products from the store. The app also provides special discounts on the user's birthday. The main components of the app include authentication, product management, order processing, and reward handling.

## Installation and Setup

To run the app, follow these steps:

1. Clone the repository to your local machine:
   ```sh
   git clone <repository_url>
   ```
2. Create a virtual environment and activate it:
   ```sh
   cd app_directory
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up the database by running the following commands:
   ```sh
   flask db init
   flask db migrate
   flask db upgrade
   ```
5. Run the app:
   ```sh
   flask run
   ```
   The app will be accessible at `http://localhost:5000/`.

## Configuration

The app uses different configurations for development, production, and testing environments. The configuration settings are stored in the `config.py` file. To change the app's configuration, set the `FLASK_ENV` environment variable to one of the following values:

- `development`: For development mode with debug enabled.
- `production`: For production mode with debug disabled.
- `testing`: For testing mode with the TESTING flag enabled.

To set sensitive information like the secret key and database URL, use environment variables or a `.env` file (not included in version control). Here's an example of how to set environment variables:

```bash
export SECRET_KEY='your-secret-key'
export DATABASE_URL='sqlite:///your_database.db'
export FLASK_ENV=development
```

## Endpoints

1. ### User Authentication and Authorization
1. ### Product Management
1. ### Order Processing
1. ### Reward Handling

1. ## Error Handling
   The app is equipped with proper error handling for various scenarios. If an error occurs during a request, the app returns a JSON response with the error message and the corresponding HTTP status code.

## Conclusion

The app provides a seamless and user-friendly experience for managing rewards and purchases on the online shopping store. It uses Flask and SQLAlchemy to handle backend operations, and it is designed to be easily configurable for different environments. For further details on specific API endpoints and their usage, refer to the app's source code and the provided documentation.

# Configuration File Documentation

The `config.py` file contains various configuration settings for the app. The configuration classes are designed to be used with Flask's `app.config.from_object()` method to set the app's configurations based on the environment.

## Configuration Classes

### `Config` (Base Configuration)

- `SECRET_KEY`: A secure secret key used for cryptographic purposes. Default: `'your-secret-key'`.
- `SQLALCHEMY_DATABASE_URI`: The database URL. Default: `'sqlite:///your_database.db'`.
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Track modifications to database objects. Default: `False`.
- `DEBUG`: Enable/disable debug mode. Default: `False`.

### `DevelopmentConfig` (Development Configuration)

- Inherits from `Config`.
- `DEBUG`: Enable debug mode for development. Default: `True`.

### `ProductionConfig` (Production Configuration)

- Inherits from `Config`.
- `DEBUG`: Disable debug mode for production. Default: `False`.
- Add other production-specific settings here, such as database configurations and caching.

### `TestingConfig` (Testing Configuration)

- Inherits from `Config`.
- `TESTING`: Enable testing mode. Default: `True`.
- Add other testing-specific settings here, such as database configurations for testing.

## Environment Variables

To configure the app's sensitive information and environment, use environment variables or a `.env` file. The app automatically reads the environment variables set in the operating system or from the `.env` file.

- `SECRET_KEY`: Set a secure and secret key for cryptographic purposes.
- `DATABASE_URL`: Set the database URL (e.g., MySQL, PostgreSQL, SQLite).
- `FLASK_ENV`: Set the environment (e.g., `development`, `production`, `testing`).

**Note**: Make sure to avoid hardcoding sensitive information in the configuration file. Instead, use environment variables to securely manage the app's configurations.

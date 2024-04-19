# Django Login Registration API Project

This project provides a set of RESTful APIs for user authentication, including login, registration, activation, password reset, and logout. The APIs are built using Django and Django REST Framework, with authentication handled using JWT tokens.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Dependencies](#dependencies)
- [Acknowledgments](#acknowledgments)

## Installation

To run this project locally, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```
4. Change directory to the project directory:
   ```
   cd project
   ```
5. Apply migrations:
   ```
   python3 manage.py migrate
   ```
6. Start the development server:
   ```
   python3 manage.py runserver
   ```

## Usage

Once the development server is running, you can access the APIs using tools like `curl`, Postman, or any HTTP client library in your preferred programming language. Make sure to refer to the [API Endpoints](#api-endpoints) section below for details on each endpoint and their usage.

## API Endpoints
```
- **POST /register**: Endpoint for user registration. Requires user details including username, email, and password.
- **GET /activate/surl**: Endpoint to activate a user account using the activation link sent via email upon registration.
- **POST /forgot_password**: Endpoint for initiating the password reset process. Requires the user's email address.
- **GET /reset_password/surl**: Endpoint to verify the password reset link and allow the user to reset their password.
- **PUT /change_password/user_id**: Endpoint to change the user's password. Requires the user's new password.
- **POST /login**: Endpoint for user authentication. Requires a valid username and password.
- **POST /logout**: Endpoint to log out a user and invalidate their JWT token.

```

## Dependencies

- Django
- Django REST Framework
- Django REST Framework JWT
- Django Redis Caches
- Python 3
- Django Rest Framework Swagger
- Django Rest Framework Authtoken

## Acknowledgments

I would like to express my gratitude to the following:

- The Python community for creating an incredible programming language that makes development a joy.
- The Django community for developing a robust and versatile web framework that accelerates web development.
- The Django REST Framework team for providing powerful tools for building RESTful APIs with Django.
- Contributors to the open-source projects used in this project, including:
  - [django-rest-framework-jwt](https://github.com/jpadilla/django-rest-framework-jwt)
  - [django-redis](https://github.com/niwibe/django-redis)
  - [rest_framework_swagger](https://github.com/axnsan12/drf-yasg)
  - [rest_framework.authtoken](https://github.com/encode/django-rest-framework/blob/master/rest_framework/authtoken/)
- Any other individuals or communities whose resources or tutorials I've referenced during the development of this project.



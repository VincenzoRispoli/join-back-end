
# Join Backend

## Description

Join Backend is a RESTful backend built with **Django** and **Django REST Framework** to manage contacts, tasks, and subtasks. The project supports basic CRUD operations (Create, Read, Update, Delete), user authentication, and advanced data management.

---

## Technologies Used

- **Django** - A Python web framework used to build the backend.
- **Django REST Framework** - A powerful toolkit for building Web APIs with Django.
- **SQLite3** - A lightweight database engine used for development and testing.

---

## Installation Guide

To get the project up and running on your local machine, follow these steps:

### 1. Clone the Repository

Begin by cloning the repository to your local machine:

git clone https://github.com/yourusername/join-backend.git


### 2. Install Dependencies

Navigate to the project folder and install the required Python packages using **pip**:

cd join-backend
pip install -r requirements.txt


### 3. Set Up the Database

Once dependencies are installed, you need to apply migrations to set up your database:

python manage.py migrate


### 4. Create a Superuser (Optional)

To interact with the Django admin panel, you can create a superuser:

python manage.py createsuperuser


### 5. Run the Development Server

Now, you can start the development server:

python manage.py runserver


Your backend should now be running at `http://127.0.0.1:8000`.

---

## API Endpoints

Below are the available API endpoints for authentication, contacts, tasks, and subtasks:

### Authentication

- **POST** `/api/auth/login/` - User login.
- **POST** `/api/auth/registration/` - User registration.

### Contacts

- **GET** `/api/contacts/` - Get a list of all contacts.
- **GET** `/api/contacts/{id}/` - Retrieve a specific contact by ID.
- **POST** `/api/contacts/` - Create a new contact.
- **PUT** `/api/contacts/{id}/` - Update an existing contact.
- **DELETE** `/api/contacts/{id}/` - Delete a contact.

### Tasks

- **GET** `/api/tasks/` - Get a list of all tasks.
- **POST** `/api/tasks/` - Create a new task.
- **GET** `/api/tasks/{id}/` - Retrieve a specific task by ID.
- **PUT** `/api/tasks/{id}/` - Update an existing task.
- **DELETE** `/api/tasks/{id}/` - Delete a task.

### Subtasks

- **GET** `/api/subtasks/` - Get a list of all subtasks.
- **POST** `/api/subtasks/` - Create a new subtask.
- **GET** `/api/subtasks/{id}/` - Retrieve a specific subtask by ID.
- **PUT** `/api/subtasks/{id}/` - Update an existing subtask.
- **DELETE** `/api/subtasks/{id}/` - Delete a subtask.

---

## Authentication

The application supports basic authentication for user login and registration:

1. **Login**: To log in, make a `POST` request to `/api/auth/login/` with the user’s credentials (username and password).
2. **Registration**: To register a new user, make a `POST` request to `/api/auth/registration/` with the necessary user details.

---

## Testing

To run the tests, you can use Django's built-in test framework:

python manage.py test

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Notes:

- Make sure to replace `yourusername` with your actual GitHub username when cloning the repo.
- Ensure that `requirements.txt` is up to date with all the necessary packages. If it’s not available, use `pip freeze > requirements.txt` to generate it.
- If you want to deploy to a production environment, you may want to configure a production-ready database such as PostgreSQL or MySQL instead of SQLite.

---

### Final Thoughts

This project can be easily extended with more features like task deadlines, notifications, and more sophisticated user roles. Feel free to contribute or modify as needed.

Let me know if you have any questions or need further assistance!

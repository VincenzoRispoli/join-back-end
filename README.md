Name of Project: 
Join Backend

Description: 
A RESTful backend built with Django and Django REST Framework to manage contacts, tasks, and subtasks.
It supports CRUD operations, authentication, and advanced data management.

Used Tecnologies:
Django,
Django Rest Framewor,
dblite3

API Endpoints:
AUTHENTICATION
POST	/api/auth/login/	User Login,
POST	/api/auth/registration/	User Registration,

CONTACTS
GET	/api/contacts/	Get a contact list,
GET /api/contacts/{id}/ Retrieve a specific contact,
POST	/api/contacts/ Create new contact,
GET	/api/contacts/{id}/	Get specific contact,
PUT	/api/contacts/{id}/ Update a contact,
DELETE	/api/contacts/{id}/	Delete a contact,

TASKS
GET	/api/tasks/	Get a tasks list,
POST	/api/tasks/	Create a new Task,
GET	/api/tasks/{id}/	Get a specific task,
PUT	/api/tasks/{id}/	Update a task,
DELETE	/api/tasks/{id}/	Delete a task,

SUBTASKS
GET /api/subtasks/ List all subtasks,
POST /api/subtasks/ Create a new subtask,
GET /api/subtasks/{id}/ Retrieve a specific subtask,
PUT /api/subtasks/{id}/ Update a subtask,
DELETE /api/subtasks/{id}/ Delete a subtask

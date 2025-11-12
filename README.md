# 🧩 Django Project Management Backend

A RESTful backend system built using Django and Django REST Framework that allows users to manage **Projects, Tasks, and Comments** with authentication and role-based access.

---

## 🚀 Features
- User Registration & Login (Token Authentication)
- Project Management (CRUD, Add Member, Complete)
- Task Management (CRUD, Assign, Complete)
- Comment System on Tasks
- Filtering (by project, user, status)
- Authentication on all endpoints
- PEP8 + DRF Best Practices

---

## 🧱 Tech Stack
- **Python 3.10+**
- **Django 5.x**
- **Django REST Framework 3.x**
- **django-filter**
- **SQLite Database**

---

## 🗂️ Project Structure
```
project_management/
├── accounts/
├── projects/
├── tasks/
├── project_management/
└── requirements.txt
```

---

## ⚙️ Setup Instructions

1️⃣ Clone the repository:
```bash
git clone https://github.com/romilmonpara/django-project-management-backend.git
cd django-project-management-backend
```

2️⃣ Create virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

3️⃣ Run migrations and start server:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 🔐 API Endpoints

### Authentication
| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/api/accounts/register/` | POST | Register a new user |
| `/api/accounts/login/` | POST | Obtain auth token |

### Projects
| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/api/projects/` | GET, POST | List or create projects |
| `/api/projects/{id}/` | GET, PUT, PATCH, DELETE | Retrieve or modify a project |
| `/api/projects/{id}/add-member/` | POST | Add user to project |
| `/api/projects/{id}/complete/` | POST | Mark project as completed |

### Tasks & Comments
| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/api/tasks/` | GET, POST | List or create tasks |
| `/api/tasks/{id}/assign/` | POST | Assign to user |
| `/api/tasks/{id}/complete/` | POST | Complete a task |
| `/api/tasks/{id}/comments/` | GET, POST | Task comments |
| `/api/comments/` | GET | List comments |

---

## 🧠 Example Lifecycle
1. Register & Login → get token  
2. Create project  
3. Add members  
4. Create and assign tasks  
5. Add comments  
6. Mark task/project as completed

---

## 🧑‍💻 Author
**Monpara Romil Kamleshbhai**  
B.Tech Information Technology, LJIET  
📍 Ahmedabad, India

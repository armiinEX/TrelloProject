# 🗂️ Mini Trello (Django REST Framework + Celery + i18n)

A simplified Trello-like project built with **Django REST Framework**.  
It supports authentication, boards, lists, tasks, invitations via email, Celery/Redis async jobs, and internationalization (English/Farsi).

---

## 🚀 Features

- **User Authentication**
  - JWT-based auth (access/refresh tokens)
  - Register, login, logout
  - Manage profile (name, email, preferred language)

- **Boards**
  - Create, update, delete boards with max board limit
  - Membership system with invitations
  - Member role & status handling

- **Lists & Tasks**
  - Full CRUD for lists and tasks
  - Move tasks between lists
  - Support due dates & ordering

- **Invitations**
  - Send invitations via email (async with Celery + Redis)
  - Accept/reject invitations
  - List received invitations

- **Internationalization (i18n)**
  - Supports English (en) & Farsi (fa)
  - Switch language at runtime

- **UI Templates**
  - Plain HTML templates for testing APIs
  - Ready for frontend integration (React, Vue, etc.)

---

## ⚙️ Tech Stack

- **Backend:** Django 5 + Django REST Framework  
- **Auth:** JWT (SimpleJWT)  
- **Async Tasks:** Celery 5 + Redis  
- **Database:** SQLite (default) → can be switched to PostgreSQL  
- **i18n:** Django translations (`gettext`)  
- **Testing UI:** Plain HTML templates with Fetch API  

---

## 🔧 Installation

```bash
git clone https://github.com/yourname/mini-trello.git
cd TrelloProject
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run migrations and create superuser:
python manage.py migrate
python manage.py createsuperuser

# Run Redis (for Celery tasks):
docker run -d -p 6379:6379 redis

# Run Celery:
celery -A core worker -l info

# Start Django server:
python manage.py runserver

# Create and compile translations (for Farsi):
django-admin makemessages -l fa
django-admin compilemessages

# Default: http://127.0.0.1:8000
```

---

## 🌐 API Endpoints

### 1. Authentication & User

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/accounts/auth/register/` | Register new user |
| POST | `/api/accounts/auth/login/` | Login (returns access + refresh tokens) |
| POST | `/api/accounts/auth/logout/` | Logout (invalidate refresh token) |
| GET | `/api/accounts/me/` | Get current user profile |
| PATCH | `/api/accounts/me/` | Update profile (e.g. name, language) |

**Example:**
```http
PATCH /api/accounts/me/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "Armin",
  "preferred_language": "fa"
}
```

### 2. Boards

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/boards/` | List boards for current user |
| POST | `/api/boards/` | Create new board |
| GET | `/api/boards/{board_id}/` | Get board details |
| PATCH | `/api/boards/{board_id}/` | Update board |
| DELETE | `/api/boards/{board_id}/` | Delete board |
| GET | `/api/boards/{board_id}/members/` | List members of board |
| POST | `/api/boards/{board_id}/invite/` | Send invitation |

### 3. Invitations

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/invitations/` | List received invitations |
| PATCH | `/api/invitations/{invitation_id}/` | Accept/Reject invitation |

**Example:**
```http
PATCH /api/invitations/12/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "accepted"
}
```

### 4. Lists

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/boards/{board_id}/lists/` | List lists in a board |
| POST | `/api/boards/{board_id}/lists/` | Create new list |
| GET | `/api/lists/{list_id}/` | List details |
| PATCH | `/api/lists/{list_id}/` | Update list |
| DELETE | `/api/lists/{list_id}/` | Delete list |

### 5. Tasks

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/lists/{list_id}/tasks/` | List tasks in a list |
| POST | `/api/lists/{list_id}/tasks/` | Create task |
| GET | `/api/tasks/{task_id}/` | Task details |
| PATCH | `/api/tasks/{task_id}/` | Update task (move to list, set due date, reorder) |
| DELETE | `/api/tasks/{task_id}/` | Delete task |

### 6. Multi-language

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/languages/` | List supported languages |
| PATCH | `/api/accounts/me/` | Update preferred language |

---

## 🖥️ HTML Test Pages

The project includes simple test templates:

| URL | Template |
|-----|----------|
| `/` | home.html |
| `/api/accounts/auth/test-ui/` | accounts/auth_test.html |
| `/boards-ui/` | boards/board_list.html |
| `/tasksapp/tasks-test/` | tasksapp/tasks_test.html |
| `/<lang>/boards/invite-test/` | boards/invite.html |
| `/<lang>/boards/lang-test/` | boards/language_test.html |

---

## 📖 i18n

To create/compile translations:
```bash
django-admin makemessages -l fa
django-admin makemessages -l en
django-admin compilemessages
```

Switch language with header:
```http
GET /api/boards/
Accept-Language: fa
```

---

## ✅ Notes

- JWT tokens expire in 5 minutes (access) & 1 day (refresh) – configurable in settings.py under SIMPLE_JWT.
- Limits: max 5 boards per user, max 10 members per board, max 15 memberships per user.
- Email sending works via Celery & Redis.

---

## 📜 License

MIT License – free to use and modify.
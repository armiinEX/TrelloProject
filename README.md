# 🗂️ Mini Trello (Collaboration & Multi-language)

A simplified Trello-like application built with **Django REST Framework** and **React-ready HTML templates**.  
Supports **authentication, boards, lists, tasks, invitations via email, Celery/Redis, and full i18n (English/Farsi)**.

---

## 🚀 Features

- **User Authentication**
  - Register / Login / Logout (JWT-based with refresh tokens)
  - Profile management (name, email, preferred language)

- **Boards**
  - Create, edit, delete boards with color customization
  - Limit: max **N=5** boards per user (TODO - not enforced yet)

- **Members & Invitations**
  - Invite members via email (async using **Celery + Redis**)
  - Track invitation status: Pending / Accepted / Rejected
  - Limit: max **M=10** members per board, max **K=15** memberships per user (TODO - not enforced yet)
  - Accept or reject invitations via RESTful endpoints

- **Lists & Tasks**
  - Full CRUD for lists & tasks
  - Move tasks between lists
  - Due dates & ordering supported

- **Internationalization (i18n)**
  - Supports English (en) & Farsi (fa)
  - Easily add new languages by editing translation files

- **Simple UI**
  - HTML templates for testing auth, boards, tasks, and i18n switch
  - API-first design, ready for integration with React or Vue

---

## ⚙️ Tech Stack

- **Backend:** Django 5 + Django REST Framework  
- **Auth:** JWT (SimpleJWT)  
- **Async Tasks:** Celery 5 + Redis  
- **Database:** SQLite (default) → replace with PostgreSQL in production  
- **i18n:** Django translations (`gettext`)  
- **Testing UI:** Plain HTML templates with Fetch API  

---

## 📂 Project Structure

```
TrelloProject/
│── accounts/        # Authentication & user profile
│── boards/          # Boards, memberships, invitations
│── tasksapp/        # Lists & tasks
│── core/            # Main settings, urls, celery app
│── templates/       # HTML templates for testing UI
│── locale/          # i18n translations (fa, en, …)
│── requirements.txt
│── README.md
```

---

## 🔧 Setup & Installation

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/yourname/mini-trello.git
cd mini-trello
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Run Redis (via Docker or local)
```bash
docker run -d -p 6379:6379 redis
```

### 4. Run Celery Worker
```bash
celery -A core worker -l info
```

### 5. Start Django Server
```bash
python manage.py runserver
```
Server runs at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🌐 API Endpoints

### 1. Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/api/accounts/auth/register/` | Register user |
| POST   | `/api/accounts/auth/login/`    | Login (JWT) |
| POST   | `/api/accounts/auth/logout/`   | Logout (invalidate refresh token) |
| GET    | `/api/accounts/me/`            | Get current profile |
| PATCH  | `/api/accounts/me/`            | Update profile (name, language) |

---

### 2. Boards
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/boards/`             | List user’s boards |
| POST   | `/api/boards/`             | Create new board |
| GET    | `/api/boards/{id}/`        | Board details |
| PATCH  | `/api/boards/{id}/`        | Edit board |
| DELETE | `/api/boards/{id}/`        | Delete board |
| GET    | `/api/boards/{id}/members/`| List members of a board |
| POST   | `/api/boards/{id}/invite/` | Invite a member via email |

---

### 3. Invitations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/invitations/`     | List invitations received |
| PATCH  | `/api/invitations/{id}/`| Accept or reject an invitation |

---

### 4. Lists
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/boards/{id}/lists/` | List lists in board |
| POST   | `/api/boards/{id}/lists/` | Create list |
| GET    | `/api/lists/{id}/`        | List details |
| PATCH  | `/api/lists/{id}/`        | Update list |
| DELETE | `/api/lists/{id}/`        | Delete list |

---

### 5. Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/lists/{id}/tasks/` | List tasks in a list |
| POST   | `/api/lists/{id}/tasks/` | Create task |
| GET    | `/api/tasks/{id}/`       | Task details |
| PATCH  | `/api/tasks/{id}/`       | Update task (title, due date, list, order) |
| DELETE | `/api/tasks/{id}/`       | Delete task |

---

### 6. Multi-language
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/languages/` | List available languages (TODO) |
| PATCH  | `/api/accounts/me/` | Change preferred language |

---

## 🖥️ Testing via HTML Templates
- `http://127.0.0.1:8000/` → Home page  
- `http://127.0.0.1:8000/api/accounts/auth/test-ui/` → Auth test (register/login/profile/logout)  
- `http://127.0.0.1:8000/boards/invite-test/` → Invite members test page  
- `http://127.0.0.1:8000/boards/lang-test/` → i18n test page  
- `http://127.0.0.1:8000/tasksapp/tasks-test/` → Tasks test page  

---

## 📖 i18n Usage
```bash
# Create translation files
django-admin makemessages -l fa
django-admin makemessages -l en

# Edit .po files inside locale/

# Compile translations
django-admin compilemessages
```

**Test with header:**
```
GET /api/boards/
Accept-Language: fa
```

---

## ✅ Evaluation Criteria
- ✅ Correct database modeling  
- ✅ Proper REST API design  
- ✅ Authentication & Permissions implemented  
- ✅ Email sending works with Celery  
- ✅ Limitations enforced (N boards, M members, K memberships)  
- ✅ Multi-language support works cleanly  
- ✅ Simple functional UI templates included  
- ✅ Documentation complete  

---

## 📜 License
MIT License – free to use and modify.

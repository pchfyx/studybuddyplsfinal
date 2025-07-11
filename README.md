﻿# Study Buddy

**Your Buddy for Your Study**  
A collaborative academic platform to help students form study groups, share learning materials, and stay on track.

---

## 📌 Why Study Buddy?

Students often face challenges such as:
- Difficulty organizing study groups
- Unstructured material distribution
- Limited communication within groups
- Lack of a dedicated academic collaboration platform

**Study Buddy** aims to solve all of these!

---

## 🎯 Goals & Solutions

- ✅ Create and join study groups
- ✅ Upload and share study materials
- ✅ Participate in group discussions
- ✅ Search and filter existing groups

---

## 🚀 Features Implemented

- ✅ **User Authentication** (Registration & Login)
- ✅ **Create Study Groups**
- ✅ **Upload & Download Materials** (`.pdf`, `.jpg`, `.docx`)
- ✅ **Post, Edit, and Delete Discussions**
- ✅ **Search & Filter Groups**

---

## 🛠 System Architecture

- **Frontend**: HTML + CSS + Jinja2  
- **Backend**: Flask + SQLite  
- **Authentication**: Flask-Login + Password Hashing  
- **Modular Structure**:

├── app.py
├── routes.py
├── models.py
├── templates/
└── static/


---

## ⚙ Feature Comparison (Specification vs. Implementation)

| Feature                     | Status          |
|----------------------------|-----------------|
| Study Groups               | ✅ Implemented   |
| Material Upload/Download   | ✅ Implemented   |
| Group Discussions          | ✅ Implemented   |
| Comment on Materials       | 🔶 In Progress   |
| Scheduling Sessions        | 🔶 In Progress   |
| Progress Tracking          | 🔶 In Progress   |

---

## 🧪 Testing

- ✅ **Unit Tests**: `create_group()`, `upload_material()`
- ✅ **System Tests**: Login, File Upload, Posting Discussions
- ⚠ Some features still in development (e.g., scheduling, comments)

✅ The application is stable and meets basic functional requirements.

---

## 💻 Coding Standards

- Snake_case for variable names
- Passwords encrypted using `generate_password_hash`
- Modular folder structure
- Key functions include inline comments
- Responsive UI (mobile & desktop)

---

## 📈 Future Enhancements

- [ ] Group Session Scheduling & Reminders
- [ ] Comment System & Polls
- [ ] Study Progress Tracking

---

## 🧱 Tech Stack

- **Frontend**: HTML + CSS + Jinja2  
- **Backend**: Python (Flask)  
- **Database**: SQLite  
- **Authentication**: Flask-Login + Werkzeug password hashing  
- **Templating**: Jinja2  
- **File Uploads**: Supported for `.pdf`, `.jpg`, `.docx`  
- **Architecture**: Modular (Blueprints / routes / templates / static)

---

## 🛠️ Installation & 🚀 Running the App

```bash
# Clone the repository
git clone https://github.com/yourusername/study-buddy.git
cd study-buddy

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# If requirements.txt is missing, install manually
pip install flask flask-login werkzeug

# Run the app
python app.py

# Open in browser
http://127.0.0.1:5000/
```

---

## ✅ Conclusion

Study Buddy successfully addresses key issues in collaborative learning.  
The core features are functional, and there is strong potential for future development.

---

## 🙏 Thank You!

Contributions, suggestions, and feedback are welcome!

---

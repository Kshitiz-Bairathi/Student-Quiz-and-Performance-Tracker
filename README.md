# 🎓 Student Quiz and Performance Tracker

A web-based platform built using **Python** and the **Flask** framework, designed to modernize how students practice for exams. This system enables teachers (Admins) to upload and manage multiple-choice questions (MCQs), while students can register, attempt quizzes, and track their performance in an organized and efficient way.

---

## 📌 Objective

This project eliminates the need for teachers to distribute practice questions through books or unstructured assignments. It provides a centralized and user-friendly platform for conducting and managing quizzes.

---

## 💡 Features

### 👨‍🏫 Admin (Teacher)
- Login securely as admin
- Add MCQ questions for different subjects
- View all questions
- Delete questions
- View individual student scores and overall performance

### 👨‍🎓 Student
- Register and login with credentials
- Attempt quizzes by subject
- View performance after each quiz
- Track historical performance

---

## 🛠️ Technologies Used

- **Language:** Python
- **Framework:** Flask
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite
- **Tools:** VS Code, Flask Debugger, Jinja2 Templates

---

## 🚀 Getting Started

### 📁 Clone the Repository
git clone https://github.com/your-username/student-quiz-tracker.git
cd student-quiz-tracker

### 🔧 Set Up Virtual Environment
python -m venv venv
source venv/bin/activate        # On Windows use: venv\Scripts\activate

### 📦 Install Dependencies
pip install -r requirements.txt

### ▶️ Run the Application
python app.py
Now open your browser and go to: http://127.0.0.1:5000

---

## 📈 Future Improvements
- Add time-based quizzes
- Export results as PDF or Excel
- Integrate email notifications for results
- Add analytics dashboards for admins

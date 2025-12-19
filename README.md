Event Planner Application

A desktop-based Event Planner built with Python and CustomTkinter.
The application helps users manage tasks, budgets, guests, and provides a centralized dashboard for navigation and overview.

This project follows a modular MVC-inspired architecture, where each feature is developed as an independent module to improve maintainability and grading clarity.

Features

📋 Task Manager

Create and manage tasks

Mark tasks as completed

(Optional) Deadline-based countdown logic integrated into tasks

💰 Budget Manager

Track budget items

View total expenses

👥 Guest Manager

Add, remove, and view guests

Persistent storage using local files

📊 Dashboard

Central navigation hub

Aggregates information from services in a read-only manner

⏱️ Countdown Utility (Optional / In Progress)

Simple countdown timer

Designed to be isolated to avoid impacting core functionality

Tech Stack

Python 3.10+

CustomTkinter (modern Tkinter UI)

Tkinter

Each feature module follows this pattern:

UI → Controller → Service → Model

Setup Instructions (Local)
1️⃣ Clone the repository
git clone https://github.com/atrocria/EventPlanner
cd EventPlanner

2️⃣ Create a virtual environment
python -m venv .venv


Activate it:

Windows

.venv\Scripts\activate


macOS / Linux

source .venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt


If requirements.txt is missing, install manually:

pip install customtkinter

4️⃣ Run the application
python app.py

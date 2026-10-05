# Online Notes Sharing System (ONSS)

A Django-based web application that lets students and teachers upload, manage, search, and download academic study materials from one central platform.



![Python](https://img.shields.io/badge/Python-3.x-blue)




![Django](https://img.shields.io/badge/Django-Framework-green)




![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)




![License](https://img.shields.io/badge/Project-Academic-orange)



## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Screenshots](#screenshots)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Roadmap](#roadmap)
- [Authors](#authors)
- [License](#license)

## Overview

ONSS provides a single, organized space for sharing academic resources. It combines secure user authentication, note management, search, and a dashboard-driven interface so that learners can quickly find and access the materials they need.

## Features

- **Authentication:** User registration, login, and password change
- **Profile management:** View and update user details
- **Note management:** Upload, edit, and delete notes
- **Search and browse:** Find notes by keyword and explore all available materials
- **Downloads:** Access shared study materials with one click
- **Dashboard:** Central view for managing notes and account activity
- **Responsive UI:** Works across desktop and mobile screens

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Django |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| UI Framework | Bootstrap |

## Screenshots

| Home |
|------|

![Home Page](Documentation/ONSS%20img/home%20page.png)

| Login |
|-------|

![Login Page](Documentation/ONSS%20img/login%20page.png)

| Dashboard |
|-----------|

![Dashboard](Documentation/ONSS%20img/dashboard.png)
 
| Add Notes |
|-----------|

![Add Notes](Documentation/ONSS%20img/add%20notes.png)

| Manage Notes |
|--------------|

![Manage Notes](Documentation/ONSS%20img/manage%20notes.png)

| Search Notes |
|--------------|

![Search Notes](Documentation/ONSS%20img/search%20notes.png)

| Notes |
|-------|

![Notes](Documentation/ONSS%20img/notes.png)

| Profile |
|---------|

![Profile](Documentation/ONSS%20img/profile.png)


## Project Structure

```text
Online-Notes-Sharing-System/
├── Documentation/
│   ├── ONSS img/            # Screenshots
│   ├── ONSS.pptx            # Presentation
│   ├── Synopsis.pdf
│   └── Thesis.pdf
├── Installation-Guide.docx
├── SQL File/
│   └── nsspythondb.sql
└── nss/
    └── notessharing/
        ├── manage.py
        ├── db.sqlite3
        ├── nssapp/          # Main application
        ├── notessharing/    # Project settings
        ├── static/
        └── templates/
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Prayasit/Online-Notes-Sharing-System.git
   cd Online-Notes-Sharing-System/nss/notessharing
   ```

2. **(Optional) Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install django
   ```

4. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

5. **Start the development server**

   ```bash
   python manage.py runserver
   ```

6. Open **http://127.0.0.1:8000/** in your browser.

## Documentation

Additional material is available in the [`Documentation/`](Documentation/) folder:

- Project Thesis
- Project Synopsis
- Project Presentation
- Application screenshots

## Roadmap

- Cloud-based file storage
- AI-powered note recommendations
- Discussion and chat functionality
- Plagiarism detection
- Mobile application
- Institution-level user roles
- Enhanced security features

## Authors

- **Prayas Gotefode**, MCA Student
- **Shiwani Amrute**, MCA Student

## License

Developed as an academic mini project.

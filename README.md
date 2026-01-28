# 📚 Study Track

<div align="center">

**Track your learning progress and boost your productivity**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 🎯 Overview

**Study Track** is a web application built with Streamlit that helps you organize, track, and manage your online courses. Keep track of your learning progress, manage course videos, and stay organized with an intuitive dashboard.

### ✨ Features

- 🔐 **User Authentication** - Secure login and registration system
- 📊 **Dashboard** - Visual overview of your learning progress
- 📝 **Course Management** - Add, view, edit, and delete courses
- ✅ **Progress Tracking** - Mark videos as completed and track your progress
- 🎨 **Modern UI** - Clean and intuitive user interface
- 💾 **MongoDB Integration** - Robust database for data persistence

---

<details>
<summary><b>📋 Table of Contents</b></summary>

- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Features in Detail](#-features-in-detail)
- [Technologies Used](#-technologies-used)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

</details>

---

<details>
<summary><b>📦 Prerequisites</b></summary>

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **MongoDB Community Edition** - [Download MongoDB](https://www.mongodb.com/try/download/community)
- **MongoDB Compass** (Optional but recommended) - [Download Compass](https://www.mongodb.com/try/download/compass)
- **Git** - [Download Git](https://git-scm.com/downloads)

### Verify Installation

```bash
python --version
mongod --version
git --version
```

</details>

---

<details>
<summary><b>🚀 Installation</b></summary>

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/study-track.git
cd study-track
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

1. Copy the example environment file:
   ```bash
   # Windows
   copy .env.example .env
   
   # Mac/Linux
   cp .env.example .env
   ```

2. Edit `.env` and add your MongoDB connection string:
   ```env
   MONGO_URI=mongodb://localhost:27017/
   SECRET_KEY=your_secret_key_here
   ```

### Step 5: Set Up Streamlit Secrets

1. Copy the example secrets file:
   ```bash
   # Windows
   copy .streamlit\secrets.toml.example .streamlit\secrets.toml
   
   # Mac/Linux
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Edit `.streamlit/secrets.toml`:
   ```toml
   [mongo]
   uri = "mongodb://localhost:27017/"
   
   [general]
   secret_key = "your_secret_key_here"
   ```

### Step 6: Start MongoDB

**Windows:**
```bash
net start MongoDB
```

**Mac (Homebrew):**
```bash
brew services start mongodb-community
```

**Linux:**
```bash
sudo systemctl start mongod
```

### Step 7: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

</details>

---

<details>
<summary><b>⚙️ Configuration</b></summary>

### Environment Variables

Create a `.env` file in the root directory:

```env
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/          # Local MongoDB
# MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/  # MongoDB Atlas

# Database Name
DB_NAME=study_track

# Collection Names
USERS_COLLECTION=users
COURSES_COLLECTION=courses

# Secret Key (generate with: python -c "import secrets; print(secrets.token_hex(32))")
SECRET_KEY=your_secret_key_here
```

### MongoDB Atlas Setup (Cloud)

If you prefer using MongoDB Atlas instead of local MongoDB:

1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Get your connection string
4. Update `MONGO_URI` in `.env`:
   ```env
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
   ```

### Streamlit Configuration

Edit `.streamlit/secrets.toml`:

```toml
[mongo]
uri = "mongodb://localhost:27017/"

[general]
secret_key = "your_secret_key_here"
```

</details>

---

<details>
<summary><b>💻 Usage</b></summary>

### First Time Setup

1. **Start the application:**
   ```bash
   streamlit run app.py
   ```

2. **Register a new account:**
   - Click "Sign Up" on the login page
   - Enter your name, email, and password
   - Click "Create Account"

3. **Login:**
   - Enter your email and password
   - Click "Login"

### Adding a Course

1. Navigate to **"Add New Course"** from the sidebar
2. Fill in the course details:
   - Course Title
   - Course URL (optional)
   - Description
   - Sections and Videos
3. Click **"Add Course"**

### Tracking Progress

1. Go to **"My Courses"** from the sidebar
2. Click on any course to view details
3. Mark videos as completed by clicking the checkbox
4. Your progress is automatically saved

### Dashboard

The dashboard shows:
- Total courses
- Total videos
- Completed videos
- Overall progress percentage
- Recent courses

</details>

---

<details>
<summary><b>📁 Project Structure</b></summary>

```
study-track/
│
├── app.py                      # Main Streamlit application entry point
├── database.py                 # MongoDB connection and database operations
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
│
├── components/                # UI Components
│   ├── __init__.py
│   ├── auth.py               # Authentication pages (login/signup)
│   ├── dashboard.py          # Main dashboard component
│   ├── course_add.py         # Add course form
│   ├── course_view.py        # Course viewing component
│   └── course_handlers.py    # Course management functions
│
├── .streamlit/               # Streamlit configuration
│   ├── secrets.toml.example  # Secrets template
│   └── secrets.toml          # Your secrets (not in git)
│
└── README.md                 # This file
```

### Key Files

- **`app.py`** - Main application file, handles routing and page navigation
- **`database.py`** - Database operations, user management, course CRUD
- **`components/auth.py`** - User authentication (login, signup, logout)
- **`components/dashboard.py`** - Dashboard with progress statistics
- **`components/course_add.py`** - Form to add new courses
- **`components/course_view.py`** - Display and manage courses

</details>

---

<details>
<summary><b>🎨 Features in Detail</b></summary>

### Authentication System

- **Secure Password Hashing** - Uses bcrypt for password encryption
- **Session Management** - Maintains user sessions across pages
- **Email Validation** - Ensures unique email addresses
- **User Profiles** - Stores user name, email, and creation date

### Course Management

- **Add Courses** - Create courses with custom sections and videos
- **View Courses** - Browse all your courses in a clean list view
- **Edit Courses** - Update course information
- **Delete Courses** - Remove courses you no longer need
- **Progress Tracking** - Mark individual videos as completed

### Dashboard

- **Statistics Overview** - See your total courses, videos, and progress
- **Progress Visualization** - Visual progress bars and percentages
- **Recent Courses** - Quick access to your latest courses
- **Quick Navigation** - Easy access to all features

### Database Schema

**Users Collection:**
```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "password": "hashed_password",
  "name": "User Name",
  "created_at": ISODate
}
```

**Courses Collection:**
```json
{
  "_id": ObjectId,
  "user_id": "user_id_string",
  "title": "Course Title",
  "url": "course_url",
  "description": "Course description",
  "sections": [
    {
      "title": "Section Title",
      "videos": [
        {
          "title": "Video Title",
          "url": "video_url",
          "completed": false
        }
      ]
    }
  ],
  "created_at": ISODate,
  "updated_at": ISODate
}
```

</details>

---

<details>
<summary><b>🛠️ Technologies Used</b></summary>

### Core Technologies

- **[Python 3.8+](https://www.python.org/)** - Programming language
- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[MongoDB](https://www.mongodb.com/)** - NoSQL database
- **[PyMongo](https://pymongo.readthedocs.io/)** - MongoDB driver for Python

### Key Libraries

- **bcrypt** - Password hashing and verification
- **python-dotenv** - Environment variable management
- **uuid** - Unique identifier generation
- **datetime** - Date and time handling

### Development Tools

- **MongoDB Compass** - GUI for MongoDB database management
- **Git** - Version control

</details>

---

<details>
<summary><b>🤝 Contributing</b></summary>

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/study-track.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Write clean, readable code
   - Add comments where necessary
   - Test your changes thoroughly

4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**

### Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

### Reporting Issues

If you find a bug or have a suggestion:
1. Check if the issue already exists
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)

</details>

---

<details>
<summary><b>🔧 Troubleshooting</b></summary>

### Common Issues and Solutions

#### ❌ MongoDB Connection Error

**Error:** `Failed to connect to MongoDB`

**Solutions:**
- Ensure MongoDB is running:
  ```bash
  # Windows
  net start MongoDB
  
  # Mac
  brew services start mongodb-community
  
  # Linux
  sudo systemctl start mongod
  ```
- Check your `MONGO_URI` in `.env` file
- Verify MongoDB is listening on port 27017

#### ❌ ModuleNotFoundError

**Error:** `No module named 'pymongo'`

**Solution:**
```bash
pip install -r requirements.txt
```

#### ❌ Port Already in Use

**Error:** `Port 8501 is already in use`

**Solution:**
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

#### ❌ Authentication Not Working

**Error:** Can't login or signup

**Solutions:**
- Check MongoDB connection
- Verify `.env` and `secrets.toml` are configured correctly
- Check browser console for errors
- Ensure MongoDB collections are created

#### ❌ Streamlit Not Found

**Error:** `streamlit: command not found`

**Solution:**
```bash
pip install streamlit
# Or
pip install -r requirements.txt
```

### Getting Help

- Check the [MongoDB Setup Guide](MONGODB_SETUP.md)
- Review the [GitHub Setup Guide](GITHUB_SETUP.md)
- Open an issue on GitHub
- Check MongoDB and Streamlit documentation

</details>

---

<details>
<summary><b>📝 License</b></summary>

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License

```
Copyright (c) 2024 Study Track

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

</details>

---

## 📞 Support

If you have any questions or need help:

- 📧 Open an issue on [GitHub Issues](https://github.com/yourusername/study-track/issues)
- 📖 Check the documentation in `MONGODB_SETUP.md` and `GITHUB_SETUP.md`
- 💬 Reach out to the maintainers

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [MongoDB](https://www.mongodb.com/) for the robust database
- All contributors and users of this project

---

<div align="center">

**Made with ❤️ using Streamlit and MongoDB**

⭐ Star this repo if you find it helpful!

</div>

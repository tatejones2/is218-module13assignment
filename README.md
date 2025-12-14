**README file contains instructions on how to run the front-end, execute Playwright tests, and links to the Docker Hub repository.**

# IS218 Module 13 - JWT Authentication with E2E Testing

### GitHub Repository
**Repository Link:** [https://github.com/tatejones2/is218-module13assignment](https://github.com/tatejones2/is218-module13assignment)

This repository contains:
- ✅ **JWT Registration & Login Routes** - `/auth/register` and `/auth/login` endpoints with complete authentication logic
- ✅ **Front-End Forms** - HTML pages with client-side validation for registration and login flows
- ✅ **Playwright E2E Tests** - 14 comprehensive end-to-end tests for authentication flows with positive and negative scenarios
- ✅ **CI/CD Pipeline** - Automated testing, security scanning, and Docker Hub deployment on every commit

### Docker Hub Repository
**Docker Image:** [Docker Hub - is218-module13](https://hub.docker.com/r/tatejones2/is218-module13)

Pull the latest image:
```bash
docker pull tatejones2/is218-module13:latest
```

---

## 🚀 Quick Start

### Run the Application
```bash
# Using Docker Compose (recommended)
docker-compose up

# Application will be available at http://localhost:8000
# Register/Login forms: http://localhost:8000/register or http://localhost:8000/login
```

### Run Front-End (Manual Testing)
```bash
# Start the application
docker-compose up

# Open browser and navigate to:
# - http://localhost:8000/register - Registration form
# - http://localhost:8000/login - Login form
# - http://localhost:8000/dashboard - Dashboard (requires login)

# Test with valid credentials:
# Username: testuser123
# Email: testuser@example.com
# Password: ValidPass123!
```

### Run E2E Tests
```bash
# Setup Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install

# Run E2E tests with docker-compose
docker-compose up -d
sleep 10
pytest tests/e2e/ -v -m e2e --tb=short
docker-compose down

# Or run individual test class
pytest tests/e2e/test_auth_e2e.py::TestRegistrationE2E -v
pytest tests/e2e/test_auth_e2e.py::TestLoginE2E -v
pytest tests/e2e/test_auth_e2e.py::TestAuthNavigationE2E -v
```

### Test Coverage
The E2E test suite includes **14 tests** covering:

**Registration Tests (6 tests)**
- ✅ Valid registration with all required fields
- ✅ Short password validation (client-side)
- ✅ Invalid email format validation
- ✅ Mismatched password detection
- ✅ Password strength requirements (uppercase, lowercase, number)
- ✅ Duplicate email rejection (server-side)

**Login Tests (6 tests)**
- ✅ Valid login with correct credentials
- ✅ Login using email instead of username
- ✅ Wrong password error handling (401 Unauthorized)
- ✅ Nonexistent user error handling
- ✅ Empty fields validation
- ✅ Remember me checkbox functionality

**Navigation Tests (2 tests)**
- ✅ Link from register page to login page
- ✅ Link from login page to register page

---

## 📚 Project Documentation

### Key Features
- **JWT Authentication** - Secure token-based authentication with access and refresh tokens
- **Password Security** - Bcrypt hashing with strength validation (uppercase, lowercase, number, special char)
- **Client-Side Validation** - Email format and password strength checks on registration/login forms
- **Server-Side Validation** - Duplicate prevention and data integrity checks
- **E2E Testing** - Automated browser testing with Playwright for authentication workflows
- **CI/CD Pipeline** - Automated testing, security scanning, and Docker deployment via GitHub Actions

### Project Structure
```
.
├── app/
│   ├── auth/
│   │   ├── jwt.py              # JWT token creation and verification
│   │   ├── dependencies.py     # Authentication dependencies
│   │   └── redis.py            # Token blacklist management
│   ├── models/
│   │   ├── user.py             # User model with auth methods
│   │   └── calculation.py      # Calculation model
│   ├── schemas/
│   │   ├── user.py             # User validation schemas
│   │   ├── token.py            # Token response schemas
│   │   └── calculation.py      # Calculation schemas
│   └── main.py                 # FastAPI routes
├── templates/
│   ├── register.html           # Registration form with validation
│   ├── login.html              # Login form with remember me
│   ├── dashboard.html          # Dashboard (protected)
│   └── layout.html             # Base template
├── static/
│   ├── css/style.css           # Styling
│   └── js/script.js            # Form handling
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── e2e/
│       └── test_auth_e2e.py   # Playwright E2E tests
├── .github/workflows/
│   └── test.yml               # CI/CD pipeline configuration
├── docker-compose.yml         # Service orchestration
├── Dockerfile                 # Container image
├── CI_CD_PIPELINE.md          # Pipeline documentation
└── requirements.txt           # Python dependencies
```

### API Endpoints

**Authentication**
- `POST /auth/register` - Register new user with email, password, first_name, last_name
- `POST /auth/login` - Login with username/email and password, returns JWT tokens
- `POST /auth/token` - Login with form data (Swagger UI compatible)

**Calculations** (BREAD operations)
- `GET /calculations` - List all calculations
- `POST /calculations` - Create new calculation
- `GET /calculations/{id}` - Read specific calculation
- `PUT /calculations/{id}` - Update calculation
- `DELETE /calculations/{id}` - Delete calculation

---

## 🔧 Development

### Setup Local Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install
```

### Run All Tests
```bash
# Unit and integration tests
pytest tests/unit/ tests/integration/ -v

# E2E tests
pytest tests/e2e/ -v -m e2e

# All tests with coverage
pytest --cov=app --cov-report=html
```

### Access API Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:
1. **Tests** - Runs unit, integration, and E2E tests on every commit
2. **Security** - Scans Docker image for vulnerabilities with Trivy
3. **Deploys** - Pushes image to Docker Hub if all tests pass

See [CI_CD_PIPELINE.md](CI_CD_PIPELINE.md) for detailed pipeline documentation.

---

# 📦 Project Setup

---

# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You'll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

> Skip if Docker isn't used in this module.

## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

(or update this if the main script is different.)

- **With Docker**:

```bash
docker run -it --rm <image-name>
```

---

# 📝 7. Submission Instructions

After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

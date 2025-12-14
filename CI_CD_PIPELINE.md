# CI/CD Pipeline Documentation

## Overview

This project uses GitHub Actions to implement a complete CI/CD pipeline that runs on every commit to the `main` branch. The pipeline automates testing, security scanning, and deployment to Docker Hub.

## Pipeline Stages

### 1. **Test Job** (`test`)
Runs on every push to `main` and all pull requests.

**Environment Setup:**
- Python 3.12
- PostgreSQL 17 database service
- Playwright browser automation

**Steps:**
1. **Checkout code** - Gets the latest repository code
2. **Setup Python** - Configures Python 3.12 environment
3. **Cache dependencies** - Optimizes pip cache for faster builds
4. **Install dependencies** - Installs all Python requirements
5. **Install Playwright** - Downloads Chromium browser and system dependencies
6. **Run unit and integration tests** - Executes `tests/unit/` and `tests/integration/`
   - Generates coverage reports
   - Creates JUnit XML output
7. **Run E2E tests with docker-compose** - Executes end-to-end tests
   - Spins up services using `docker-compose.yml`
   - Waits for services to be healthy
   - Runs Playwright tests against running services
   - Cleans up services on completion

**Pass/Fail Criteria:**
- All tests must pass
- Code coverage reports are generated
- E2E tests validate authentication flows

### 2. **Security Job** (`security`)
Runs only after the test job succeeds.

**Steps:**
1. **Build Docker image** - Creates a Docker image from the Dockerfile
2. **Run Trivy vulnerability scanner** - Scans the image for:
   - Critical vulnerabilities
   - High-severity vulnerabilities
   - Known CVEs
   - Unfixed issues are ignored

**Pass/Fail Criteria:**
- No critical or high-severity vulnerabilities found

### 3. **Deploy Job** (`deploy`)
Runs only after security scanning passes AND only on the `main` branch.

**Requirements:**
- Production environment (requires GitHub environment approval if configured)

**Steps:**
1. **Setup Docker Buildx** - Configures multi-platform build capability
2. **Login to Docker Hub** - Authenticates using secrets
3. **Build and push Docker image** - 
   - Builds for multiple platforms (amd64, arm64)
   - Pushes to Docker Hub with tags:
     - `{DOCKERHUB_USERNAME}/is218-module13:latest`
     - `{DOCKERHUB_USERNAME}/is218-module13:{git-sha}`
   - Uses registry cache for faster builds
4. **Success notification** - Confirms successful deployment

## Environment Variables

Configured at the workflow level and available to all jobs:

```yaml
DATABASE_URL: postgresql://postgres:postgres@localhost:5432/fastapi_db
TEST_DATABASE_URL: postgresql://postgres:postgres@localhost:5432/fastapi_test_db
JWT_SECRET_KEY: "super-secret-key-for-jwt-min-32-chars"
JWT_REFRESH_SECRET_KEY: "super-refresh-secret-key-min-32-chars"
ACCESS_TOKEN_EXPIRE_MINUTES: 30
REFRESH_TOKEN_EXPIRE_DAYS: 7
BCRYPT_ROUNDS: 12
```

## Required GitHub Secrets

To enable Docker Hub deployment, configure these secrets in your GitHub repository settings:

- **`DOCKERHUB_USERNAME`** - Your Docker Hub username
- **`DOCKERHUB_TOKEN`** - Docker Hub access token (Personal Access Token)

**How to set up:**
1. Go to Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `DOCKERHUB_USERNAME` with your Docker Hub username
4. Add `DOCKERHUB_TOKEN` with your Docker Hub PAT

## Testing Strategy

### Unit Tests
Located in `tests/unit/`, these test individual functions and classes in isolation.

### Integration Tests
Located in `tests/integration/`, these test how components work together with the database.

### E2E Tests
Located in `tests/e2e/`, these run against live services:
- **Registration tests** - Valid/invalid registration flows
- **Login tests** - Authentication with valid/invalid credentials
- **Navigation tests** - Page routing and navigation
- **Token management** - JWT storage and refresh

E2E tests run with:
- PostgreSQL database
- FastAPI web server
- Playwright browser automation

## Docker Configuration

The pipeline uses docker-compose for E2E testing:

**Services:**
- `web` - FastAPI application (auto-rebuilt for tests)
- `db` - PostgreSQL 17 database
- `pgadmin` - Database management interface (optional)

**Environment:**
- Database credentials configured in `docker-compose.yml`
- JWT secrets inherited from workflow env vars
- Application runs with reload enabled for development

## Workflow Triggers

The pipeline runs on:
- **Push to main branch** - Full CI/CD pipeline
- **Pull requests to main** - Tests only (no deployment)

## Pipeline Flow Diagram

```
Code Push to main
       ↓
   Test Job
   ├─ Unit/Integration Tests
   ├─ E2E Tests (with docker-compose)
   └─ Pass/Fail
       ↓ (only on success)
   Security Job
   ├─ Build Docker image
   ├─ Trivy vulnerability scan
   └─ Pass/Fail
       ↓ (only on success & main branch)
   Deploy Job
   ├─ Build multi-platform image
   ├─ Login to Docker Hub
   ├─ Push image with tags
   └─ Success notification
```

## Troubleshooting

### Tests fail locally but pass in CI
- Ensure database is running: `docker-compose up db`
- Clear pytest cache: `pytest --cache-clear`
- Reinstall dependencies: `pip install -r requirements.txt`

### E2E tests timeout
- Increase sleep time in docker-compose startup
- Check service health: `docker-compose logs`
- Verify PostgreSQL is fully initialized

### Docker push fails
- Verify `DOCKERHUB_TOKEN` is valid (not expired)
- Check username matches Docker Hub account
- Ensure Docker image builds successfully locally

### Trivy scan fails
- Review vulnerability details in GitHub Actions output
- Update dependencies: `pip install --upgrade`
- Build image locally: `docker build -t test .`

## Local Testing

To run the same tests locally:

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install

# Unit and integration tests
pytest tests/unit/ tests/integration/ -v

# E2E tests with docker-compose
docker-compose up -d
sleep 10
pytest tests/e2e/ -v -m e2e
docker-compose down

# All tests with coverage
pytest --cov=app --cov-report=html
```

## Deployment

When tests pass on the main branch:
1. Security scanning validates no critical vulnerabilities
2. Docker image is built for amd64 and arm64 architectures
3. Image is pushed to Docker Hub:
   - Latest tag for quick reference
   - SHA tag for version tracking
4. Registry cache speeds up future builds

**Access deployed image:**
```bash
docker pull {DOCKERHUB_USERNAME}/is218-module13:latest
docker run -p 8000:8000 {DOCKERHUB_USERNAME}/is218-module13:latest
```

## Best Practices

1. **Keep tests fast** - E2E tests should complete in < 5 minutes
2. **Test isolation** - Each test should be independent
3. **Commit messages** - Use clear, descriptive messages
4. **PR reviews** - Tests must pass before merging to main
5. **Secret management** - Never commit secrets or credentials
6. **Docker cache** - Leverage buildx cache for faster deployments

## Monitoring

Check pipeline status:
- **GitHub Actions tab** - View runs, logs, and artifacts
- **Docker Hub repositories** - Monitor pushed images
- **Coverage reports** - Review code coverage metrics

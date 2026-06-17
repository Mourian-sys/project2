# Deployment Guide - Project 2

This guide explains how to deploy the Project 2 application using Jenkins with GitHub webhooks.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [GitHub Webhook Setup](#github-webhook-setup)
3. [Jenkins Configuration](#jenkins-configuration)
4. [Deployment Process](#deployment-process)
5. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software
- Jenkins (v2.300+)
- Python 3.7+
- Git
- pip (Python package manager)
- curl or similar HTTP client

### Required Jenkins Plugins
1. **GitHub plugin** - For GitHub integration
2. **GitHub Pull Request Builder** - For PR management
3. **Generic Webhook Trigger** - For flexible webhook handling
4. **Pipeline** - For pipeline support

To install plugins:
1. Go to Jenkins Dashboard → Manage Jenkins → Manage Plugins
2. Search for each plugin and click Install

## GitHub Webhook Setup

### Step 1: Generate GitHub Personal Access Token (Optional but Recommended)

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token"
3. Select scopes:
   - `repo` (full control of private repositories)
   - `admin:repo_hook` (write access to hooks)
4. Copy the token and save it securely

### Step 2: Configure GitHub Webhook

1. Go to your repository: `https://github.com/Mourian-sys/project2`
2. Navigate to Settings → Webhooks → Add webhook
3. Fill in the following:
   - **Payload URL**: `http://your-jenkins-instance:8080/github-webhook/`
   - **Content type**: Select `application/json`
   - **Events**: Select "Push events" (or choose specific events)
   - **Active**: ✓ Check this box

4. Click "Add webhook"

### Step 3: Test the Webhook

1. In your local repository, make a commit:
   ```bash
   git add .
   git commit -m "Test webhook"
   git push origin main
   ```

2. GitHub will send a webhook event
3. Check Jenkins console log to verify receipt

## Jenkins Configuration

### Step 1: Create a New Pipeline Job

1. Jenkins Dashboard → New Item
2. Name: `project2-deployment`
3. Select: **Pipeline**
4. Click OK

### Step 2: Configure Pipeline Settings

1. **Build Triggers** tab:
   - ✓ Check "GitHub hook trigger for GITScm polling"

2. **Pipeline** tab:
   - Select: "Pipeline script from SCM"
   - SCM: Select "Git"
   - Repository URL: `https://github.com/Mourian-sys/project2.git`
   - Credentials: (add your GitHub credentials if private repo)
   - Branch Specifier: `*/main`
   - Script Path: `Jenkinsfile`

3. Click Save

### Step 3: Configure Jenkins Security

If using webhooks from GitHub to your Jenkins instance:

1. Go to Manage Jenkins → Configure System
2. Find "GitHub" section
3. Click "Add GitHub Server"
4. Configure:
   - **API URL**: `https://api.github.com`
   - **Credentials**: Add your GitHub Personal Access Token
5. Test connection
6. Click Save

## Deployment Process

### Automatic Deployment (via Webhook)

1. Push code to the `main` branch:
   ```bash
   git push origin main
   ```

2. GitHub sends a webhook to Jenkins
3. Jenkins automatically triggers the `project2-deployment` job
4. Pipeline executes with stages:
   - Checkout
   - Setup Python Environment
   - Code Quality Check
   - Run Tests
   - Build Package
   - Deploy to Staging
   - Health Check

### Manual Deployment

1. Go to Jenkins Dashboard
2. Click on `project2-deployment` job
3. Click "Build Now"
4. Monitor build progress in console output

### Monitoring Deployment

1. View build logs:
   - Click on build number (e.g., #1)
   - Click "Console Output"

2. Check application status:
   ```bash
   curl http://your-jenkins-instance:5000/health
   ```

## Production Deployment Script

For production deployments, create a separate pipeline stage:

```groovy
stage('Deploy to Production') {
    when {
        branch 'main'
    }
    steps {
        echo '========== Deploying to production =========='
        sh '''
            . ${VENV_DIR}/bin/activate
            
            # Connect to production server
            ssh user@production-server << 'EOF'
                cd /opt/project2
                git pull origin main
                python -m pip install -r requirements.txt
                systemctl restart project2
            EOF
        '''
    }
}
```

## Configuration Files

### .env File

Create a `.env` file in the project root:

```env
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
LOG_LEVEL=INFO
```

### Jenkins Credentials

1. Jenkins Dashboard → Manage Jenkins → Manage Credentials
2. Add GitHub credentials:
   - Kind: Username with password
   - Username: your-github-username
   - Password: your-personal-access-token
   - ID: github-credentials

## API Endpoints

After deployment, the following endpoints are available:

- **Health Check**: `GET http://your-jenkins-instance:5000/health`
- **Process Data**: `POST http://your-jenkins-instance:5000/api/process`
- **Validate Input**: `POST http://your-jenkins-instance:5000/api/validate`
- **GitHub Webhook**: `POST http://your-jenkins-instance:5000/webhook/github`

## Troubleshooting

### Webhook Not Triggering

1. Verify webhook URL is accessible:
   ```bash
   curl http://your-jenkins-instance:8080/github-webhook/
   ```

2. Check GitHub webhook delivery logs:
   - Repository Settings → Webhooks → Click webhook → Recent Deliveries

3. Check Jenkins logs:
   - Jenkins Dashboard → Manage Jenkins → System Log

### Build Failing at Test Stage

1. Check test output in console log
2. Run tests locally:
   ```bash
   python -m pytest tests/ -v
   ```

3. Verify all dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

### Application Not Responding After Deployment

1. Check if process is running:
   ```bash
   ps aux | grep gunicorn
   ```

2. Check application logs:
   ```bash
   tail -f /path/to/project2/app.log
   ```

3. Verify port availability:
   ```bash
   lsof -i :5000
   ```

### GitHub Webhook Authentication Failures

1. Verify personal access token is valid
2. Check token has correct scopes: `repo` and `admin:repo_hook`
3. Regenerate token if needed

## Rollback Procedure

If deployment fails or issues arise:

1. Revert to previous commit:
   ```bash
   git revert <commit-hash>
   git push origin main
   ```

2. Jenkins will automatically trigger new deployment with previous version
3. Monitor health endpoint to confirm stability

## Additional Resources

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [GitHub Webhooks Guide](https://docs.github.com/en/developers/webhooks-and-events/webhooks)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Gunicorn Documentation](https://gunicorn.org/)

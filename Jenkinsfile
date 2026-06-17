// Jenkinsfile for automated deployment
// This file configures the Jenkins pipeline for continuous integration and deployment

pipeline {
    agent any
    
    environment {
        REPO_URL = 'https://github.com/Mourian-sys/project2.git'
        BRANCH = 'main'
        PYTHON_VERSION = '3.9'
        VENV_DIR = 'venv'
        APP_PORT = '5000'
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }
    
    triggers {
        // Trigger on GitHub webhook push events
        githubPush()
        
        // Optional: Poll SCM every 5 minutes
        // pollSCM('H/5 * * * *')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '========== Checking out code =========='
                git branch: "${BRANCH}", url: "${REPO_URL}"
                echo '========== Repository checked out successfully =========='
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo '========== Setting up Python environment =========='
                sh '''
                    python3 --version
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip setuptools wheel
                    pip install -r requirements.txt
                    echo "Python environment ready"
                '''
            }
        }
        
        stage('Code Quality Check') {
            steps {
                echo '========== Running code quality checks =========='
                sh '''
                    . ${VENV_DIR}/bin/activate
                    # Install flake8 for linting
                    pip install flake8 -q
                    # Run linting checks (non-blocking)
                    flake8 app/ tests/ --count --statistics || true
                    echo "Code quality checks completed"
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo '========== Running unit tests =========='
                sh '''
                    . ${VENV_DIR}/bin/activate
                    # Run tests with coverage
                    pytest tests/ -v --cov=app --cov-report=html --cov-report=term
                    echo "Tests completed successfully"
                '''
            }
        }
        
        stage('Build Package') {
            steps {
                echo '========== Building Python package =========='
                sh '''
                    . ${VENV_DIR}/bin/activate
                    python setup.py sdist bdist_wheel
                    echo "Package build completed"
                '''
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                echo '========== Deploying to staging environment =========='
                sh '''
                    . ${VENV_DIR}/bin/activate
                    # Kill existing process if running
                    pkill -f "python app/main.py" || true
                    sleep 2
                    
                    # Deploy application
                    nohup python -m gunicorn \
                        --workers 4 \
                        --worker-class sync \
                        --bind 0.0.0.0:${APP_PORT} \
                        --timeout 120 \
                        --error-logfile - \
                        --access-logfile - \
                        "app.main:create_app()" > app.log 2>&1 &
                    
                    sleep 3
                    echo "Staging deployment completed"
                '''
            }
        }
        
        stage('Health Check') {
            steps {
                echo '========== Performing health check =========='
                sh '''
                    . ${VENV_DIR}/bin/activate
                    for i in {1..10}; do
                        if curl -s http://localhost:${APP_PORT}/health | grep -q "healthy"; then
                            echo "Health check passed"
                            exit 0
                        fi
                        echo "Attempt $i/10 - waiting for service..."
                        sleep 2
                    done
                    echo "Health check failed"
                    exit 1
                '''
            }
        }
    }
    
    post {
        success {
            echo '========== Pipeline execution successful =========='
            // Optionally send success notification
            sh '''
                echo "Build successful at $(date)" | mail -s "Jenkins Build Success" your-email@example.com || true
            '''
        }
        failure {
            echo '========== Pipeline execution failed =========='
            // Optionally send failure notification
            sh '''
                echo "Build failed at $(date)" | mail -s "Jenkins Build Failed" your-email@example.com || true
            '''
        }
        always {
            echo '========== Cleaning up =========='
            // Archive test results
            junit 'test-results.xml' || true
            // Publish coverage reports
            publishHTML([
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ]) || true
            // Clean workspace
            cleanWs()
        }
    }
}

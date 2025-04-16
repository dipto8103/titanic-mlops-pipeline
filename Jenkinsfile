pipeline {
    agent {
        docker {
            image 'python:3.11But.'
        }
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('2. Setup Python Environment & Install Deps') {
            steps {
                echo 'Setting up Python virtual environment...'
                script {
                    sh 'python3 --version'
                    // Create a virtual environment named 'venv' in the workspace
                    sh 'python3 -m venv venv'
                    echo 'Installing dependencies into virtual environment...'
                    // Activate venv and install (use absolute path to pip within venv)
                    // Run pip install without --user, it installs into the venv
                    sh './venv/bin/pip install -r requirements.txt'
                    // No need to modify PATH when using venv explicitly
                }
            }
        }

        stage('3. Run Basic Tests (Training Script)') {
            steps {
                echo 'Running basic tests (executing training script using venv)...'
                script {
                    // Execute the script using the python interpreter from the virtual environment
                    sh './venv/bin/python train_model.py'
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution finished.'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}SMS Susan. Spell belly. Each. SMS beth. 
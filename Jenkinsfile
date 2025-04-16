pipeline {
    agent any // Run steps directly on the controller node

    stages {
        stage('1. Checkout Code') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('2. Install Dependencies') {
            steps {
                echo 'Installing Python dependencies on controller...'
                // Python 3 & Pip come from the custom Docker image
                sh 'python3 --version'
                sh 'pip3 --version'
                // Install dependencies using --user to avoid needing root here
                sh 'pip3 install --user -r requirements.txt'
                // Add the user's local bin directory to PATH for this pipeline run
                // This ensures subsequent stages can find any executables installed by pip
                env.PATH = "$HOME/.local/bin:${env.PATH}"
            }
        }

        stage('3. Run Training Script') {
            steps {
                echo 'Running training script...'
                // Python3 should be in PATH, packages should be importable
                sh 'python3 train_model.py'
            }
        }
    } // End stages

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
    } // End post
} // End pipeline
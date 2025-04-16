pipeline {
    // Define the agent for the entire pipeline
    agent {
        docker {
            image 'python:3.9-slim' // Use a specific Python 3.9 image (slim version is smaller)
            // args '-v /var/run/docker.sock:/var/run/docker.sock' // Uncomment if you need Docker inside Docker later
            // reuseNode true // Optional: Can speed up builds by reusing the node, but manage workspace carefully
        }
    }

    stages {
        stage('1. Checkout Code') {
            // Note: Checkout happens before the agent typically starts,
            // but the files become available in the agent's workspace.
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('2. Setup Python Environment') {
            steps {
                echo 'Setting up Python environment inside Docker container...'
                script {
                    // These should now work inside the python:3.9-slim container
                    sh 'python3 --version'
                    sh 'pip3 --version'
                    echo 'Installing dependencies from requirements.txt...'
                    // Use --user or consider virtual environments if preferred
                    sh 'pip3 install --user -r requirements.txt'
                    // Add ~/.local/bin to PATH if using --user, needed for scripts installed by pip
                    env.PATH = "$HOME/.local/bin:${env.PATH}"
                }
            }
        }

        stage('3. Run Basic Tests (Training Script)') {
            steps {
                echo 'Running basic tests (executing training script)...'
                script {
                    // This should now work as python3 and libraries are available
                    sh 'python3 train_model.py'
                }
            }
        }
        // We will add Docker build stages later
    }

    post { // Actions performed after the pipeline finishes
        always {
            echo 'Pipeline execution finished.'
            // cleanWs() // Consider cleaning workspace, especially if not reusing node
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
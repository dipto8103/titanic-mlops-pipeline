pipeline {
    agent any // Specifies that Jenkins can use any available agent (node) to run this pipeline

    // The empty environment block that caused the error has been removed

    stages {
        stage('1. Checkout Code') {
            steps {
                echo 'Checking out code from GitHub...'
                // This step checks out the code from the Git repository configured in the Jenkins job
                checkout scm
            }
        }

        stage('2. Setup Python Environment') {
            // We will refine this stage later to handle Python/pip installation if needed
            steps {
                echo 'Setting up Python environment...'
                script {
                    try {
                        // Check versions if Python/pip are found on the agent
                        sh 'python3 --version || python --version'
                        sh 'pip3 --version || pip --version'
                        // Attempt to install dependencies
                        sh 'pip3 install --user -r requirements.txt || pip install --user -r requirements.txt'
                    } catch (Exception e) {
                        echo "Warning: Potential issue setting up Python environment. Might need explicit installation. Error: ${e.getMessage()}"
                        // We won't fail the build here yet, just warn.
                    }
                }
            }
        }

        stage('3. Run Basic Tests (Placeholder)') {
            steps {
                echo 'Running basic tests...'
                // This is a placeholder. We aren't running real unit/integration tests yet.
                // Attempt to run the training script as a basic check
                script {
                   try {
                        // Try running the script - might fail if dependencies aren't correctly installed/found
                        sh 'python3 train_model.py || python train_model.py'
                   } catch (Exception e) {
                        echo "Warning: Training script execution failed. Likely due to environment issues. Error: ${e.getMessage()}"
                        // We won't fail the build here yet, just warn.
                   }
                }
            }
        }
        // We will add Docker-related stages later
    }

    post { // Actions performed after the pipeline finishes
        always {
            echo 'Pipeline execution finished.'
            // Optional: Clean up the workspace
            // cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
        unstable {
            echo 'Pipeline completed with warnings (unstable).'
        }
    }
}
pipeline {
    agent any // This tells Jenkins to run this pipeline on any available agent
    environment {
        // Append C:\Windows\System32 to the start of the PATH
        PATH = "C:\\Windows\\System32;${env.PATH}" // This PATH was explicitly added because windows has some restriction of the length of an environment
        // variable. See: https://devblogs.microsoft.com/oldnewthing/20100203-00/?p=15083
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm // Checks out the source code from the configured SCM repository
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh """
                        python -m pip install -r requirements.txt
                        """
                    } else {
                        bat """
                        python -m pip install -r requirements.txt
                        """
                    }
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh """
                        python -m unittest discover
                        """
                    } else {
                        bat """
                        python -m unittest discover
                        """
                    }
                }   
            }
        }
    }
}

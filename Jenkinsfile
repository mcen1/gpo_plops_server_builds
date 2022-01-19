@Library("shared-pipeline-library") _
@Library("shared-pipeline-library-gcdunix") __

ansiColor('xterm') {
    node (label: 'linux') {
      stage ("Checkout scm") {
        checkout scm
        currentBuild.displayName = "${SERVERFILE}"
      }
      stage ("Run tests before deploying") {
        sh "python3 tests/run.py 'server_vars/${SERVERFILE}'"
      }

      stage ("Add ansible galaxy requirements if not already there"){
        sh "ansible-galaxy install -r requirements.yml --force"
      }

      stage ("Run playbook") {
        withCredentials([file(credentialsId: "cyberark_ssl_cert_key", variable: 'CYBERARK_PKEY')]) {
          withCredentials([file(credentialsId: "cyberark_ssl_cert_public", variable: 'CYBERARK_CERT')]) {
            withCredentials([file(credentialsId: "ansbuildcreds", variable: 'ANSBUILDCREDS')]) {
              withCredentials([file(credentialsId: "sa_ansible_ssh_key", variable: 'ANSIBLEKEY'), file(credentialsId: "ansvault", variable: 'ANS_VAULT_FILE')]){
                sh "ansible-playbook --private-key='${ANSIBLEKEY}' -u sa-ansible -e 'varfile=\"server_vars/${SERVERFILE}\" credfile=\"${ANSBUILDCREDS}\"' main.yml"
              }
            }
          }
        }
      }
    }
}

######################################################################
# - First put ssh key on all remote machine                          #
# - Go in docker_swarm/vars/main.yml and change default user for shh #
######################################################################

# Check that access is allowed
# echo "Trying to ping all ip from inventory/dev/hosts..."
# ansible all -m ping -u {{ssh_remote_user}} -i ./inventory/dev/hosts


# Allow verbose mode
if [[ $1 == "-v" || $1 == "-vv" || $1 == "-vvv" ]];
then
    # Run infrastructure playbook
    echo "Running ansible-playbook infrastructure.yml $1 -i ./inventory/dev/hosts -e 'ansible_python_interpreter=/usr/bin/python3'..."
    ansible-playbook infrastructure.yml $1 -i ./inventory/dev/hosts -e 'ansible_python_interpreter=/usr/bin/python3'

    # Run gitlab playbook
    echo "Running ansible-playbook $1 -i ./inventory/dev/hosts -e 'ansible_python_interpreter=/usr/bin/python3' gitlab-playbook.yml --ask-vault-pass -e @roles/gitlab/vars/vault.yml'..."
    ansible-playbook $1 -i ./inventory/dev/hosts -e 'ansible_python_interpreter=/usr/bin/python3' gitlab-playbook.yml --ask-vault-pass -e @roles/gitlab/vars/vault.yml
else
    # Run infrastructure playbook
    # echo "Running ansible-playbook infrastructure.yml -i ./inventory/dev/hosts -e 'ansible_python_interpreter=/usr/bin/python3'..."
    # ansible-playbook infrastructure.yml -i ./inventory/dev/hosts -e 'ansible_python_interpreter=/usr/bin/python3'

    # Run gitlab playbook
    echo "Running ansible-playbook  -i ./inventory/dev/hosts -e 'ansible_python_interpreter=/usr/bin/python3' gitlab-playbook.yml --ask-vault-pass -e @roles/gitlab/vars/vault.yml'..."
    ansible-playbook  -i ./inventory/dev/hosts -e 'ansible_python_interpreter=/usr/bin/python3' gitlab-playbook.yml --ask-vault-pass -e @roles/gitlab/vars/vault.yml
fi
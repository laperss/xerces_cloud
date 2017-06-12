# Ansible

## Installation
```
sudo apt-add-repository -y ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
```
Ansible only needs to be installed on your local pc. Connection to the different VMs goes through SSH.

### Set hosts
Add VMs to the Ansible hosts file `/etc/ansible/hosts` as follows
```
[vm1_name]
129.192.XXX.XX1
[vm_group]
129.192.XXX.XX2
129.192.XXX.XX3
129.192.XXX.XX4
```
where vm1_name and vm_group are arbitrarily chosen and can be used later to refer to different VMs or collection of VMs.

#### Set private key and user
Add both your private key and default username to the Ansible config file `/etc/ansible/ansible.cfg` as follows
```
private_key_file = /path/to/keyfile
remote_user = ubuntu
```

### Run Ansible playbook
Run the Ansible playbook by running
```
ansible-playbook -s playbook.yml
```

### Debugging
Add the flag `-vvv` for more debugging information.

### Sources
- [Ansible Documentation](http://docs.ansible.com/)
- [An Ansible Tutorial](https://serversforhackers.com/an-ansible-tutorial) 
- [Get Ansible to work on bare Ubuntu 16.04 without python 2.7](https://gist.github.com/gwillem/4ba393dceb55e5ae276a87300f6b8e6f)
- [List of Ansible pre-defined variables](https://stackoverflow.com/questions/18839509/where-can-i-get-a-list-of-ansible-pre-defined-variables)

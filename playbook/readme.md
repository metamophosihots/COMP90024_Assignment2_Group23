
1.comment unwanted roles in all_in_one.yaml

  1.1 if "harvest" is one of the roles you want, you will also need to slightly modify "deploy harvest" part to choose your configuration file in roles/db-harvest/tasks/main.yaml

2.run command:

. ./unimelb-comp90024-2021-grp-23-openrc.sh; ansible-playbook -i hosts all_in_one.yaml --ask-become-pass

3.provid the following key:

NmMwOWM4ODEyNGQ2MzM5

4.provid the sudo key for your local computer

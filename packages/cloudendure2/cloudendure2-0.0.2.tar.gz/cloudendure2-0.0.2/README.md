**CloudEndure SDK**
# Python Package
**Compatability:** <br>
![Python Version 3.8](https://img.shields.io/badge/Python-3.8-blue.svg)

## Using CloudEndureSDK

<span style="color:DarkRed">**DOCUMENTATION WORK IN PROGRESS...**</span>

###### Example - Backup All Blueprints:
````python
from cloudendure import CloudendureSDK

userApiToken = "{TOKEN}"

client = CloudendureSDK(userApiToken)
client.export_all_bp_csv('blueprint_backup.csv')

````
###### Example - List All Projects
````python
from cloudendure import CloudendureSDK

userApiToken = 'token'
projectId = 'projectId'

client = CloudendureSDK(userApiToken)
projects = client.list_projects()
print(projects)

````


###### Example - List all project blueprints:
````python
from cloudendure import CloudendureSDK

userApiToken = 'token'
projectId = 'projectId'

client = CloudendureSDK(userApiToken)
blueprints = client.list_blueprint(projectId)

````

###### Example - List all machines in a project
````python
from cloudendure import CloudendureSDK

userApiToken = 'token'
projectId = 'projectId'

client = CloudendureSDK(userApiToken)
machines = client.list_machines(projectId)
print(machines)

````

###### Example - Get a machine blueprint and export to csv
````python
from cloudendure import CloudendureSDK

userApiToken = 'token'
projectId = 'projectId'
client = CloudendureSDK(userApiToken)

machine = client.get_machine_by_name(machineName='MyMachineName', projectId=projectId)
blueprint = [client.get_blueprint_by_machine(machineId=machine['id'], projectId=projectId)]
print(blueprint)
client.export_bp_csv(filename='export.csv', blueprint=blueprint)

````

###### Example - Get Machine by Name
````python
from cloudendure import CloudendureSDK

userApiToken = 'token'
projectId = 'projectId'
client = CloudendureSDK(userApiToken)

machine = client.get_machine_by_name(machineName='MyMachine', projectId=projectId)
print(machine)


````

###### Example - Mass update blueprints from csv
````python
from cloudendure import CloudendureSDK

userApiToken = 'token'
projectId = 'projectId'
client = CloudendureSDK(userApiToken)

# Backup All Blueprints
client.export_all_bp_csv('backup.csv') 

r = client.update_machine_blueprint_csv(fileName='update.csv')
print(r)


````


---

<br>





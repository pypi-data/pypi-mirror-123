# Clio
An easy to use CLI tool for running faster kubernetes and docker commands.


<h2>Usage example</h2>

For seeing the logs of a kube pod:

**$ syneto-clio logs <pod_name>**

For entering a kube pod:

**$ syneto-clio enter <pod_name>**

For getting the status of all kube pods:

**$ syneto-clio check**

For restarting a docker container:

**$ syneto-clio restart <container_name>**

For cleaning up hanging containers & images:

**$ syneto-clio cleanup docker**

For mounting giove code:

_Sidenote:_ If you ran **config** command already, you can skip name, password and ip parameters and just provie the source path.

**$ syneto-clio sync giove --name < name > --password < password > --ip < ip_address > < source_path > **




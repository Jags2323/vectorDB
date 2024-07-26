Installing MINTS:

Installing MINTS Involves multiple tools like **Docker, Kubernetes, Ansible and any Cloud Service.**

Docker for **Containerization** of MINTS Services, which **packages** each service and all its **dependencies** together in the form of containers. which is deployable unit in Kubernetes cluster.

Kubernetes for **Container Orchestration** and managing MINTS Services. Each Service will be deployed in any **Cloud Kubernetes Cluster** with the help **Ansible Playbook**.

Ansible Playbook Initially Spins the Kubernetes Cluster, later deploys each service in repected cloud kubernetes cluster. 

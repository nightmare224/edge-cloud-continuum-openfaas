# Efficient FaaS Architectures in the Edge-Cloud Continuum

## Introduction

This [repository](https://github.com/nightmare224/edge-cloud-continuum-openfaas) contains the codebase developed for my master's thesis, titled "Efficient FaaS Architectures in the Edge-Cloud Continuum," completed at the University of Amsterdam.

## Quick Started

### Prerequisite

1. Prepare at least two target machines: one for the cloud and one for the edge. The cloud machine should run **Ubuntu 20.04**, while the edge machine can be configured with either **Ubuntu 20.04** or **Raspberry Pi OS Lite (64-bit)**.
2. The target machines need to enable SSH connection.

### Install

To deploy FaaS platform in decentralized, federated, centralized architectures: 

1. **Clone the **[edge-cloud-continuum-openfaas](https://github.com/nightmare224/edge-cloud-continuum-openfaas) **repository**

   ```bash
   git clone https://github.com/nightmare224/edge-cloud-continuum-openfaas.git
   ```

2. **Install Ansible**

   Please follow the step in [Ansible documentation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) to install Ansible on the node that is able to connect with target machines.

3. **Configure the [inventroy file](https://github.com/nightmare224/edge-cloud-continuum-openfaas/tree/master/deployment/ansible/inventory)**

   Setup the IP address and username and password of the target machines.

   **IMPORTANT**: Only modify the **ansible_host** and **ansible_user** fields. Do not change other parts.

4. **Deploy the target architecture**

   ```bash
   cd deployment/ansible
   # centralized, federated, decentralized
   ARCH=centralized
   ansible-playbook -i inventory/${ARCH}.ini ${ARCH}.yaml --ask-become-pass
   ```

### Evaluation

1. **Deploy workload**

   ```bash
   cd deployment/ansible
   # centralized, federated, decentralized
   ARCH=centralized
   ansible-playbook -i inventory/${ARCH}.ini experiment.yaml
   ```

2. **Trigger workload**

   ```bash
   cd experiment/trigger
   ./trigger.sh





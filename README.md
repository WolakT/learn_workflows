# GCP Workflows to call the self hosted runner over private connection

In order to invoke a private endpoint from GCP workflows follwing setup is needed:
- GCP workflows has a `private_service_name` in the call args
- There is a service-directory endpoint registered that has the correct IP address and the port number


## Use case 1

Let's imagine we have an app that delegates long running operations to the GCP workflows.
In such scenario instead of having an async endpoint that would run for longer amount of time
and block operations, we can create an endpoint that calls the GCP workflow and returns the 
execution uuid. In such way we have the non-blocking endpoint. 
But what if we designed our workflow in such way that it making a series of calls to our app. 
Every change of the logic or endpoint would need to first deploy the newer version of the app or the 
workflow, which makes the development process ineffective. 
Ideally we would have an gcp workflows emulator where we could test new workflows in conjunction
with app changes. Unfortunatelly there is no emulator atm. 
A nice workaround would be to use the ability of workflows to call private endpoints. 
One solution would be to use the selfhosted runner (VM, GKE) and in the CI/CD pipeline that 
would trigger the e2e tests. Pipeline would deploy a test version of the GCP workflow with 
a `private_service_name` as arg in the call endpoint then spin up the app inside a docker container and start
testing. In such setup the app can call the workflow and workflow can call back different app endpoints,
allowing for testing new features. 


## Self hosted runnger on GKE

Assuming the scenario where we have a self hosted runner on GKE cluster. The following is needed to set this up.
- GKE cluste
- Self hosted runner deployment with a service account
- Runners service account requires the `Workflow invoker` role
- app needs to create docker within docker so a sidecar container with dind is needed
- internal load balancer to expose the internal IP of the runner
- directory service registered together with the endpoint
- NAT set up to enable pods access to github actions


## Self hosted runners on GKE controlled with actions-runner-controller

[Github docs](https://github.com/actions/actions-runner-controller/blob/master/docs/quickstart.md)

1. Create a cluster
2. Create a secret with github PAT
3. Remember to get the credentials:
    ```bash
    gcloud container clusters get-credentials github-runner-cluster --region=europe-central2
    ```
4. Create a k8s secret with GH token PAT(classic)
    ```bash
    kubectl create secret generic controller-manager   --from-literal=github_token=$RUNNER_TOKEN   -n actions-runner-system
    ```
5. deploy the cert-manager
    ```bash
    kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.8.2/cert-manager.yaml
    ```
    or 
    ```bash
    kubectl apply -f actions-runner-controller-legacy/cert-manager.yaml
    ```
6. Use helm to deploy the actions-runner-controller
    ```bash
    helm repo add actions-runner-controller https://actions-runner-controller.github.io/actions-runner-controller
    helm upgrade --install actions-runner-controller   actions-runner-controller/actions-runner-controller   -n actions-runner-system   -f actions-runner-controller-legacy/values.yaml
    ```


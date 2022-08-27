# Kubernetes Validating Webhook
 This repo was forked from [k-mitevski/kubernetes-validating-webhook](https://github.com/k-mitevski/kubernetes-validating-webhook). I suggest this [great article](https://kmitevski.com/writing-a-kubernetes-validating-webhook-using-python/) for a newcomer on webhooks to get basic but valuable insight about writing a simple admission webhook. 

 Even though we can limit the requested cpu using the [limitrange](https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/#create-a-limitrange-and-a-pod) on the container level, I just wanted to do the same thing using the webhook.

## How it works?
When a deployment is triggered, the request is intercepted by the webhook and forwarded to the backend. The backend checks the CPU requests of each container of the deployment. To approve the deployment request, the requested CPU values should be less than the threshold value which is given from the [environment value of the webhook container](resources/webhook-deploy.yaml).

```
env:
- name: cpu
  value: "2"
```
Threshold value can be given as core or milicores.
```
env:
- name: cpu
  value: "2500m"
```
Namespaces where our control logic is intended to be executed can be manipulated from the [configmap](resources/webhook-cm.yaml).
```
data:
  properties.yaml: |
    default
    devteam
```

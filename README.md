# flask-app Demo deployment
This repo contain some configuration file for building a secure kubernete infrastructure on cloud. this is not completed deployment repo.
you neet to change or add more configuration to deploy your application.
## Digitalocean kubernetes cluster setup

### Pre-reqs
- Custom domain in order to add subdomains
- Kubernetes cluster in digitalocean

### Install nginx ingress load balancer
- choose hostname for load balancer and set in `nginx-ingress-values.yml`, e.g. lb.example.com
- install nginx ingress controller:
  ```
  helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
  ```
  ```
  helm repo update ingress-nginx
  ```
  ```
  helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace -f nginx-ingress-values.yml
  ```
- wait for load balancer to fully setup in digitalocean
- add 2 loadbalancer hostname DNS A records: 
    - lb -> loadbalancer ip
    - www.lb -> loadbalancer ip

### Install cert manager & cluster issuer for issuing ssl certs:
- set your email in `cert-issuer.yml`, it must be a valid email.
- install manager & cert issuer:
  ```
  helm repo add jetstack https://charts.jetstack.io
  ```
  ```
  helm repo update jetstack
  ```
  ```
  helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace -f cert-manager-values.yml
  ```
  ```
  kubectl apply -f cert-issuer.yml
  ```

### Install argocd for continuous deployment

- create 2 hostname DNS CNAME records for argocd to point to your loadbalancer domain: 
    - argocd -> lb.example.com
    - www.argocd -> lb.example.com
- set actual registry hostname in `argocd-ingress-http.yml` e.g. argocd.example.com
- install argocd:
  ```
  kubectl create namespace argocd
  ```
  ```
  kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
  ```
  ```
  kubectl apply -f argocd-ingress-http.yml
  ```
- get admin password: 
  ```
  kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}"
  ```
- navigate to argocd.example.com and login with username: admin, and apssword from previous step.

# Deployment Guide

There are two supported paths: a single-VM Docker Compose deployment (fast,
suitable for demos) and a Kubernetes + Terraform deployment (production
pattern shown here as a reference AWS implementation).

## Option A — Single VM (Docker Compose)

```bash
git clone https://github.com/equidx-ai/equidx-ai.git
cd equidx-ai
cp .env.example .env   # edit with production secrets
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Put `infrastructure/nginx/nginx.conf` in front of it (or your own
reverse proxy / load balancer) for TLS termination and routing between
`app.<domain>` (web) and `api.<domain>` (backend).

## Option B — Kubernetes + Terraform (reference: AWS)

### 1. Provision cloud infrastructure

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars   # edit as needed
terraform init
terraform plan
terraform apply
```

This provisions a VPC, an EKS cluster, an RDS Postgres instance, an
ElastiCache Redis cluster, and an S3 bucket for uploads (see
`infrastructure/terraform/main.tf` and `modules/`).

### 2. Point kubectl at the new cluster

```bash
aws eks update-kubeconfig --name equidx-<environment> --region <region>
```

### 3. Create secrets

Populate `equidx-secrets` (see
`infrastructure/k8s/02-secrets.example.yaml` for the expected keys) from
your secrets manager — do not commit real secret values.

### 4. Apply manifests

```bash
kubectl apply -f infrastructure/k8s/00-namespace.yaml
kubectl apply -f infrastructure/k8s/01-configmap.yaml
kubectl apply -f infrastructure/k8s/  # secrets already created above
```

See `infrastructure/k8s/README.md` for the recommended apply order.

### 5. CI/CD

`.github/workflows/cd.yml` builds and pushes each service's image to
GHCR on every `vX.Y.Z` tag, then rolls the corresponding Kubernetes
Deployments. Configure the `KUBE_CONFIG` repository secret with a
kubeconfig scoped to the target cluster/namespace.

## Observability in production

- Prometheus + Grafana: deploy via the community `kube-prometheus-stack`
  Helm chart pointed at the same `/metrics` endpoints each service already
  exposes, or reuse `infrastructure/monitoring/prometheus.yml` as a
  starting scrape config.
- Logs: ship container stdout (already structured JSON) to OpenSearch via
  Fluent Bit/Filebeat — see `infrastructure/logging/`.

## Zero-downtime rollouts

Each Kubernetes Deployment (`infrastructure/k8s/1x-*.yaml`) uses the
default rolling-update strategy; readiness probes on `/health` ensure new
pods only receive traffic once ready. `backend` additionally has an HPA
scaling 3–10 replicas on CPU utilization.

## Database migrations in production

Run migrations as a one-off Job (or a pre-deploy CI step) rather than on
pod startup, to avoid multiple replicas racing to migrate concurrently:

```bash
kubectl -n equidx run migrate --rm -it --restart=Never \
  --image=ghcr.io/equidx-ai/backend:latest -- alembic upgrade head
```

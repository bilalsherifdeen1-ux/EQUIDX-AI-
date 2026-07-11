# Kubernetes manifests

Apply in order (or use `kubectl apply -f infrastructure/k8s/` — filenames
are numerically prefixed so `kubectl` applies them in a safe order):

```bash
kubectl apply -f 00-namespace.yaml
kubectl apply -f 01-configmap.yaml
# Create equidx-secrets from your secrets manager — do NOT apply
# 02-secrets.example.yaml as-is in production.
kubectl apply -f 30-postgres.yaml -f 31-redis.yaml
kubectl apply -f 10-backend.yaml -f 11-ai-engine.yaml -f 12-biosensor-simulator.yaml \
               -f 13-analytics.yaml -f 14-mobile-api.yaml -f 15-web.yaml
kubectl apply -f 20-ingress.yaml
```

In production, prefer managed Postgres/Redis (see `../terraform/modules`)
over the in-cluster StatefulSet/Deployment shipped here for dev/demo
clusters.

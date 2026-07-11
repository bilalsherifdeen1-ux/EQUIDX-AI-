# API Reference

## REST (OpenAPI)

The backend auto-generates an OpenAPI 3.1 spec, browsable at
`/docs` (Swagger UI) and `/redoc` (ReDoc), and machine-readable at
`/openapi.json`. Locally: <http://localhost:8000/docs>.

### Key resource groups

| Group | Base path | Notes |
|---|---|---|
| Authentication | `/api/v1/auth` | register, login (OAuth2 password flow), refresh, `me` |
| OAuth2 SSO | `/api/v1/oauth` | Google authorization-code flow scaffold |
| Patients | `/api/v1/patients` | synthetic patient CRUD, RBAC-gated |
| Samples | `/api/v1/samples` | registration, status tracking, barcode lookup |
| Reports | `/api/v1/reports` | AI report generation + review workflow |
| Files | `/api/v1/files` | S3-backed upload + presigned download URLs |
| Notifications | `/api/v1/notifications` | in-app notification feed |
| Admin | `/api/v1/admin` | user management, audit log — ADMIN only |
| Analytics | `/api/v1/analytics` | proxy to the analytics microservice |

All endpoints except `/auth/register` and `/auth/login` require a bearer
JWT (`Authorization: Bearer <access_token>`), obtained from `/auth/login`.

### AI Engine service (separate OpenAPI doc)

<http://localhost:8100/docs> — `/api/v1/infer`, `/api/v1/train`,
`/api/v1/evaluate/{sample_type}`.

### Biosensor Simulator service

<http://localhost:8200/docs> — `/api/v1/waveform` (REST pull),
`/ws/stream/{sample_type}` (WebSocket live stream).

## GraphQL

Endpoint: `/graphql` on the backend (`http://localhost:8000/graphql`),
with an interactive GraphiQL-style explorer in development.

Example query:

```graphql
query {
  patients(search: "Rivera", limit: 5) {
    id
    mrn
    firstName
    lastName
    isSynthetic
  }
  samples(patientId: "00000000-0000-0000-0000-000000000000") {
    id
    sampleType
    status
    barcode
  }
}
```

GraphQL is intentionally read-oriented in this prototype — mutations
(create/update) go through the REST API, which owns validation, RBAC, and
audit logging for writes.

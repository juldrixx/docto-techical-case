# GCP

## Requirements

### Access Management

#### Locally

Locally, to have access to GCP resource, we will use our own identity. So we just need to configure the gcloud CLI to use our identity and our project.
```sh
gcloud auth login
gcloud auth application-default login
gcloud config set project <PROJECT_ID>
```

#### GitHub Actions

In GitHub Actions, we will do the same thing that we did with AWS to impersonnate a `Service Account` without any need to store credentails.
To do that, we will use the Worload Identity Federation (WIF).

Navigate to `IAM & Admin > Workload Identity Federation` and create new pool (a new provider need to be created with it). With the following configuration:
- Name: `github-wif-pool`
- Provider Type: `OpenID Connect (OIDC)`
- Provider Name: `github`
- Provider ID: `github-provider`
- Issuer (URL): `https://token.actions.githubusercontent.com`
- Audiences: `Default audience`
- Attribute Mapping:
  - `google.subject` -> `assertion.sub`
  - `attribute.repository` -> `assertion.respository`
  - `attribute.ref` -> `assertion.ref`
- Attribute Conditions: `attribute.repository=="juldrixx/docto-technical-case" && attribute.ref=="refs/heads/main"`

After that we will create a `Service Account` with the following roles attached to it:
- roles/owner
- roles/iam.workloadIdentityUser (mandatory)
> `roles/owner` is wide, you should restrict change by smaller roles.

And now assign this `Service Account` to `Worload Identity Federation pool` by clicking on your pool and `Grant Access`. Select `Grant access using Service Account impersonation` and chose your `Service Account` and as principals set `attribute.repository` -> `juldrixx/docto-technical-case` to make sure that only our repository can impersonnate this `Service Account`.


#### Configure GitHub Action

Now, we can just configure our GitHub Action to use it.
You need to add these permissions:

```yaml
permissions:
  id-token: write # This is required for requesting the JWT
  contents: read  # This is required for actions/checkout
```

and the following action:

```yaml
- name: Configure gcp credentials
  uses: google-github-actions/auth@v2
  with:
    project_id: "<PROJECT_ID>"
    workload_identity_provider: "projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/<WIF_POOL_ID>/providers/<WIF_PROVIDER_ID>"
    service_account: <SERVICE_ACCOUNT_EMAIL>
```

### GCS Bucket for Terraform state

When using Terraform, you prefer to store your Terraform state in the same infrastructure that your working on.
So when using Terraform on GCP, you will store your state in an GCS bucket for it.

Create an GCS bucket:

```sh
gsutil mb -l \
  europe-west9 \
  gs://tf-docto-technical-case
```

> We set the region as `europe-west9` that represents Paris, because it will reduce our network costs.

Delete GCS bucket for TF State:

```sh
gcloud storage rm --recursive gs://tf-docto-technical-case
```

## Notes

The setup is pretty much the same as in AWS. Here is the replacement:
- `S3 Bucket` -> `Cloud Storage Bucket (GCS)`
- `RDS` -> `Cloud SQL`
- `EC2` -> `Google Kubernetes Engine (GKE)`

I change the `EC2` by a `GKE Autopilot` because in AWS we just deployed Docker images so to do a better setup I deployed my Docker images as `Deployment` in Kubernetes. And `Autopilot` because it allows to reduce the cost to provision only the resource (Kubernetes node) needed depending the workload present on the Kubernetes.

The `Cloud SQL` is deployed as private so it doesn't have any public ip. So, to connect to it in `Kubernetes`, we need to configure a `Cloud SQL Proxy` as `sidecar` that will run alongside the container that needs to access it.

```tf
resource "kubernetes_deployment" "fastapi" {
  ...
  spec {    
    ...
    template {      
      ...
      spec {
        ...
        container {
          name  = "cloud-sql-proxy"
          image = "gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.11.4"
          args = [
            "--structured-logs",
            "--port=3306",
            "--private-ip",
            "${data.google_sql_database_instance.sql.connection_name}"
          ]
          security_context {
            run_as_non_root = true
          }
        }
      }
    }
  }
}
```

And to give access to the different GCP resources like the `Cloud SQL` or the `GCS Bucket`, we need our API to have some rights. To do that we will create a `Service Account` that will have different roles attached to it and use `Workload Identity` to make the pods impersonates it.
```tf
resource "google_service_account" "k8s" {
  account_id   = "${local.identifier}-sa"
  display_name = "Service Account for ${local.identifier}"
}

resource "google_project_iam_member" "sql" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.k8s.email}"
}

resource "google_storage_bucket_iam_member" "gcs" {
  bucket = google_storage_bucket.gcs.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.k8s.email}"
}

resource "google_service_account_iam_binding" "k8s_bind" {
  service_account_id = google_service_account.k8s.id
  role               = "roles/iam.workloadIdentityUser"
  members = [
    "serviceAccount:${var.project_id}.svc.id.goog[${kubernetes_service_account.k8s.metadata[0].namespace}/${kubernetes_service_account.k8s.metadata[0].name}]"
  ]
}

resource "kubernetes_service_account" "k8s" {
  metadata {
    name      = "${local.identifier}-sa"
    namespace = "default"
    annotations = {
      "iam.gke.io/gcp-service-account" = "${google_service_account.k8s.email}"
    }
  }
}

resource "kubernetes_deployment" "fastapi" {
  ...
  spec {
    ...
    template {
      ...
      spec {
        service_account_name = kubernetes_service_account.k8s.metadata[0].name
      }
    }
  }
}
```

> Note that the `Service Account` as right only on the `GCS Bucket` and note on the project level. In GCP, the rights are either attached to the project or directly on a specific resource. Where AWS, the right are defined on the project level, but specified for specifec resource.s
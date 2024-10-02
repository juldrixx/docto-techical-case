resource "google_service_account" "k8s" {
  account_id   = "${local.identifier}-sa"
  display_name = "Service Account for ${local.identifier}"
}

resource "google_project_iam_member" "sql" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.k8s.email}"
}

resource "google_service_account_iam_binding" "k8s_bind" {
  service_account_id = google_service_account.k8s.id
  role               = "roles/iam.workloadIdentityUser"
  members = [
    "serviceAccount:${var.project_id}.svc.id.goog[${kubernetes_service_account.k8s.metadata[0].namespace}/${kubernetes_service_account.k8s.metadata[0].name}]"
  ]
}

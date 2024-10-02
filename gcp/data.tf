data "google_client_config" "default" {}

data "google_sql_database_instance" "sql" {
  name = google_sql_database_instance.sql.name
}

data "kubernetes_service" "fastapi" {
  metadata {
    name      = kubernetes_service.fastapi.metadata[0].name
    namespace = kubernetes_service.fastapi.metadata[0].namespace
  }
}

data "kubernetes_service" "website" {
  metadata {
    name      = kubernetes_service.website.metadata[0].name
    namespace = kubernetes_service.website.metadata[0].namespace
  }
}


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
  metadata {
    name = "${local.identifier}-fastapi"
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "fastapi"
      }
    }

    template {
      metadata {
        labels = {
          app = "fastapi"
        }
      }

      spec {
        service_account_name = kubernetes_service_account.k8s.metadata[0].name

        container {
          name              = "fastapi"
          image             = "ghcr.io/juldrixx/docto-technical-case-fastapi:latest"
          image_pull_policy = "Always"

          env {
            name  = "MYSQL_USER"
            value = google_sql_user.users.name
          }
          env {
            name  = "MYSQL_PASSWORD"
            value = google_sql_user.users.password
          }
          env {
            name  = "MYSQL_HOST"
            value = "localhost"
          }
          env {
            name  = "MYSQL_PORT"
            value = 3306
          }
          env {
            name  = "MYSQL_DB"
            value = google_sql_database.database.name
          }
          env {
            name  = "OBJECT_BUCKET"
            value = google_storage_bucket.gcs.name
          }
          env {
            name  = "OBJECT_BUCKET_TYPE"
            value = "GCS"
          }
        }

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

resource "kubernetes_service" "fastapi" {
  metadata {
    name = "${local.identifier}-fastapi-svc"
  }
  spec {
    selector = {
      app = "fastapi"
    }
    port {
      port        = 8000
      target_port = 8000
    }
    type = "LoadBalancer"
  }
}

resource "kubernetes_deployment" "website" {
  metadata {
    name = "${local.identifier}-website"
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "website"
      }
    }

    template {
      metadata {
        labels = {
          app = "website"
        }
      }

      spec {
        service_account_name = kubernetes_service_account.k8s.metadata[0].name

        container {
          name              = "website"
          image             = "ghcr.io/juldrixx/docto-technical-case-website:latest"
          image_pull_policy = "Always"

          env {
            name  = "REACT_APP_FASTAPI_URL"
            value = "http://${data.kubernetes_service.fastapi.status[0].load_balancer[0].ingress[0].ip}:8000"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "website" {
  metadata {
    name = "${local.identifier}-website-svc"
  }
  spec {
    selector = {
      app = "website"
    }
    port {
      port        = 80
      target_port = 80
    }
    type = "LoadBalancer"
  }
}

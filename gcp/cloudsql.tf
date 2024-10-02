resource "google_compute_global_address" "sql" {
  name          = "${local.identifier}-vpc-sql"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vpc.id
}

resource "google_service_networking_connection" "vpc_peering" {
  network                 = google_compute_network.vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.sql.name]
  deletion_policy         = "ABANDON"
}

#tfsec:ignore:google-sql-encrypt-in-transit-data
resource "google_sql_database_instance" "sql" {
  name             = "${local.identifier}-sql"
  region           = var.region
  database_version = "MYSQL_8_0"

  deletion_protection = false

  settings {
    tier              = "db-f1-micro"
    availability_type = "ZONAL"
    activation_policy = "ALWAYS"

    backup_configuration {
      enabled = true
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
    }
  }
  depends_on = [
    google_service_networking_connection.vpc_peering
  ]
}

resource "random_password" "sql_password" {
  length           = 20
  special          = true
  min_lower        = 2
  min_upper        = 2
  min_numeric      = 2
  min_special      = 2
  override_special = "_%@$#"
}

resource "google_sql_user" "users" {
  name     = "${local.identifier}-sql-user"
  instance = google_sql_database_instance.sql.name
  password = sensitive(random_password.sql_password.result)
}

resource "google_sql_database" "database" {
  name     = "${local.identifier}-db"
  instance = google_sql_database_instance.sql.name
}

resource "google_compute_network" "vpc" {
  name         = "${local.identifier}-vpc"
  routing_mode = "GLOBAL"
}

#tfsec:ignore:google-compute-enable-vpc-flow-logs
resource "google_compute_subnetwork" "subnetwork" {
  name          = "${local.identifier}-subnetwork"
  ip_cidr_range = "10.1.0.0/22"
  region        = var.region
  network       = google_compute_network.vpc.id

  secondary_ip_range {
    range_name    = "${local.identifier}-secondary-subnet-pods"
    ip_cidr_range = "10.4.0.0/14"
  }
  secondary_ip_range {
    range_name    = "${local.identifier}-secondary-subnet-services"
    ip_cidr_range = "10.8.0.0/16"
  }
}

#tfsec:ignore:google-compute-no-public-egress
resource "google_compute_firewall" "allow-egress" {
  name    = "${local.identifier}-allow-egress"
  network = google_compute_network.vpc.name

  allow {
    protocol = "all"
  }

  direction          = "EGRESS"
  destination_ranges = ["0.0.0.0/0"]
}

resource "google_compute_router" "router" {
  name    = "${local.identifier}-router"
  network = google_compute_network.vpc.name
  region  = var.region
}

resource "google_compute_router_nat" "nat" {
  name                               = "${local.identifier}-nat"
  router                             = google_compute_router.router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}

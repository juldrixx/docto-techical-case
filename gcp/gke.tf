provider "kubernetes" {
  host                   = "https://${module.gke.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.gke.ca_certificate)
}

module "gke" {
  source = "terraform-google-modules/kubernetes-engine/google//modules/beta-autopilot-private-cluster"

  project_id = var.project_id

  name              = "${local.identifier}-gke"
  region            = var.region
  zones             = local.zones
  network           = google_compute_network.vpc.name
  subnetwork        = google_compute_subnetwork.subnetwork.name
  ip_range_pods     = google_compute_subnetwork.subnetwork.secondary_ip_range[0].range_name
  ip_range_services = google_compute_subnetwork.subnetwork.secondary_ip_range[1].range_name

  release_channel = "REGULAR"

  horizontal_pod_autoscaling = true
  enable_private_endpoint    = false
  enable_private_nodes       = true
}
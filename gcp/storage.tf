#tfsec:ignore:google-storage-bucket-encryption-customer-key
resource "google_storage_bucket" "gcs" {
  name          = "${local.identifier}-bucket"
  location      = "EU"
  storage_class = "STANDARD"
  force_destroy = true

  uniform_bucket_level_access = true
}

output "fastapi_url" {
  description = "URL to access the FastAPI"
  value = "http://${data.kubernetes_service.fastapi.status[0].load_balancer[0].ingress[0].ip}:8000"
}

output "website_url" {
  description = "Url to access the Website"
  value = "http://${data.kubernetes_service.website.status[0].load_balancer[0].ingress[0].ip}:80"
}
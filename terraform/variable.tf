variable "pubsub_credentials" {
    description = "Google Cloud Pub/Sub Credentials"
    type = string
    default = ""
}

variable "google_project" {
  description = "Google Cloud Project ID"
  type = string
  default = ""
}

variable "google_region" {
  description = "Google Cloud region"
  type = string
  default = "us-central1"
}

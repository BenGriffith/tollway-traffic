terraform {
  required_providers {
    google = {
        source = "hashicorp/google"
        version = "4.78.0"
    }
  }
}

provider "google" {
  alias = "pubsub_provider"
  credentials = var.pubsub_credentials
  project = var.google_project
  region = var.google_region
}

module "pubsub" {
  source = "terraform-google-modules/pubsub/google"
  version = "6.0.0"

  topic = "tollway-traffic"
  project_id = var.google_project
  pull_subscriptions = [
    {
      name = "pull"
    }
  ]
}

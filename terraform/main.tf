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
  credentials = local.envs["PUBSUB_SERVICE_ACCOUNT"]
  project = local.envs["PROJECT_ID"]
  region = local.envs["GOOGLE_REGION"]
}

module "pubsub" {
  source = "terraform-google-modules/pubsub/google"
  version = "6.0.0"

  topic = local.envs["TOPIC_ID"]
  project_id = local.envs["PROJECT_ID"]
  pull_subscriptions = [
    {
      name = "pull"
    }
  ]
}

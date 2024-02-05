provider "google" {
  credentials = local.envs["PUBSUB_SERVICE_ACCOUNT"]
  project = local.envs["PROJECT_ID"]
  region = local.envs["GOOGLE_REGION"]
}

resource "google_pubsub_topic" "tollway_topic" {
  name = local.envs["TOPIC_ID"]
}

resource "google_pubsub_subscription" "pull_subscription" {
  name  = "pull_subscription"
  topic = google_pubsub_topic.tollway_topic.name
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.19.0"
    }
  }
}

provider "google" {
  credentials = var.google_credentials
  project     = var.project
  region      = var.region
}

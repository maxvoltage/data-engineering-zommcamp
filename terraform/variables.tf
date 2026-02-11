variable "google_credentials" {
  description = "Path to the Google Cloud credentials JSON file"
  type        = string
}

variable "project" {
  description = "GCP Project ID"
  type        = string
  default     = "circular-truck-487100-i2"
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-west1"
}

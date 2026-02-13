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
variable "location" {
  description = "Project Location"
  type        = string
  default     = "US"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  type        = string
  default     = "terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  type        = string
  default     = "STANDARD"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  type        = string
  default     = "demo_dataset"
}

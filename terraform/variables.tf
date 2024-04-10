variable "credentials" {
  description = "My Credentials"
  default     = "/Users/anzelam/ac/google/terraform/gcp-creds.json"
}

variable "project" {
  description = "Project"
  default     = "de-running-project"
}

variable "region" {
  description = "Region"
  default     = "europe-west3-a"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_dataset_name_stage" {
  description = "My BigQuery Dataset Name"
  default     = "stage"
}

variable "bq_dataset_name_report" {
  description = "My BigQuery Dataset Name"
  default     = "report"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "de-running-project-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}
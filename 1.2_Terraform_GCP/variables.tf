variable "bq_dataset_name" {
    description = "My BigQuery Dataset Name"
    default ="demo_dataset"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default     = "US"
}
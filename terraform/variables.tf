variable "aws_region" {
  default = "us-east-1"
}

variable "dockerhub_username" {
  description = "Your Docker Hub username"
  type        = string
}

variable "app_name" {
  default = "interview-project"
}

variable "db_password" {
  description = "RDS database password"
  type        = string
  sensitive   = true
}
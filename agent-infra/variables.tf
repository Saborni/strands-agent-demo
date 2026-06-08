variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "eu-west-1"
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "weatheragent"
}

variable "agent_name" {
  description = "Name of the AgentCore agent"
  type        = string
  default     = "weatheragent"
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "dev"
}

variable "log_retention_days" {
  description = "CloudWatch logs retention in days"
  type        = number
  default     = 7
}

variable "image_tag" {
  description = "Docker image tag for ECR"
  type        = string
  default     = "latest"
}

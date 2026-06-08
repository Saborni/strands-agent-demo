output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.agent_repo.repository_url
}

output "ecr_repository_arn" {
  description = "ECR repository ARN"
  value       = aws_ecr_repository.agent_repo.arn
}

output "agent_runtime_id" {
  description = "AgentCore runtime ID"
  value       = aws_bedrockagentcore_agent_runtime.this.agent_runtime_id
}

output "agent_runtime_arn" {
  description = "AgentCore runtime ARN"
  value       = aws_bedrockagentcore_agent_runtime.this.agent_runtime_arn
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group for AgentCore"
  value       = aws_cloudwatch_log_group.agentcore_runtime_logs.name
}

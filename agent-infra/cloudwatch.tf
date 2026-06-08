# CloudWatch Log Group for AgentCore Runtime
resource "aws_cloudwatch_log_group" "agentcore_runtime_logs" {
  name              = "/aws/bedrock/agentcore/${var.agent_name}"
  retention_in_days = var.log_retention_days

  tags = {
    Name        = "${var.agent_name}-runtime-logs"
    Environment = var.environment
  }
}

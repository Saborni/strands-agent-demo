resource "aws_bedrockagentcore_agent_runtime" "this" {
  agent_runtime_name = replace(var.agent_name, "-", "_")
  role_arn           = aws_iam_role.this.arn

  agent_runtime_artifact {
    container_configuration {
      container_uri = "${aws_ecr_repository.agent_repo.repository_url}:${var.image_tag}"
    }
  }

  network_configuration {
    network_mode = "PUBLIC"
  }

  tags = {
    Name        = var.agent_name
    Environment = var.environment
  }
}

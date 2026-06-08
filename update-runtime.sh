#!/bin/bash
set -e

AWS_REGION=${AWS_REGION:-eu-west-1}
IMAGE_TAG=${IMAGE_TAG:-latest}

echo "🐳 Building and pushing updated Docker image..."
cd agent-infra
ECR_REPO_URL=$(terraform output -raw ecr_repository_url 2>/dev/null | tr -d '\n\r')
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

cd ../agent-app
# ECR login
aws ecr get-login-password --region ${AWS_REGION} | \
  docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Check if running on macOS
if [[ "$(uname)" == "Darwin" ]]; then
  echo "Running on macOS..."
  # Check for Apple Silicon
  if [[ "$(uname -m)" == "arm64" ]]; then
    echo "Apple Silicon detected, using platform flag for Docker build..."
    PLATFORM_FLAG="--platform linux/arm64"
  else
    PLATFORM_FLAG=""
  fi
else
  PLATFORM_FLAG="--platform linux/arm64"
fi

# Build, tag and push
docker build ${PLATFORM_FLAG} -t ${ECR_REPO_URL}:${IMAGE_TAG} .
docker push ${ECR_REPO_URL}:${IMAGE_TAG}

# Step 3: Create bedrock runtime
echo "🤖 Updating bedrock runtime..."
cd ../agent-infra
terraform apply -target=aws_bedrockagentcore_agent_runtime.this -var="image_tag=${IMAGE_TAG}" -auto-approve

echo "✅ Deployment complete!"

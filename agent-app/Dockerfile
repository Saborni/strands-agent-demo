FROM python:3.13-slim

WORKDIR /app

# Copy all Python files
COPY weather.py .

# Install dependencies
RUN pip install --no-cache-dir \
    boto3 \
    botocore \
    bedrock-agentcore \
    strands-agents \
    strands-agents-tools

# Run the script
ENTRYPOINT ["python", "weather.py"]

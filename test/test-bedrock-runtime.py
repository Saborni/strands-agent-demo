import boto3
import json
import uuid
from datetime import datetime

session_id = f"test-session-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:8]}"

client = boto3.client('bedrock-agentcore', region_name='eu-west-1')

payload = json.dumps({"prompt": "What is the weather like in Boston today?"}).encode('utf-8')

response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:eu-west-1:0123456789:runtime/weatheragent-s4zS2BDGEG',
    runtimeSessionId=session_id, # Must be 33+ char. Every new SessionId will create a new MicroVM
    payload=payload
)
response_body = response['response'].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)
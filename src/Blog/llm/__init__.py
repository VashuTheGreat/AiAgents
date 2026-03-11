from langchain_aws import ChatBedrockConverse
LLM_MODEL_ID = "us.meta.llama3-3-70b-instruct-v1:0"
LLM_REGION = "us-east-1"
llm = ChatBedrockConverse(
    model_id=LLM_MODEL_ID,
    region_name=LLM_REGION
)


image_planner_llm = ChatBedrockConverse(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    region_name="us-east-1",
)
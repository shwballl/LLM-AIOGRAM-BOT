from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
import logging

load_dotenv()

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
token = os.getenv("GITHUB_API_KEY")

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

messages=[
    SystemMessage("You are a helpfull assistant."),
]


def generate_response(prompt: int) -> str:
    messages.append(
       UserMessage(str(prompt)),
    )
    try:
        response = client.complete(
            messages=messages,
            max_tokens=4096,
            model=model,
            temperature=0.4,
            top_p=1
        )
    except Exception as e:
        logging.error("Failed to recognize prompt. With error: " + str(e))
        return None
    
    logging.info("AI response content: " + str(response.choices))
    gpt_reply = response.choices[0].message.content
    logging.info("AI response successfuly generated: " + str(gpt_reply))
    
    messages.append(
        AssistantMessage(gpt_reply),
    )
    return str(gpt_reply)
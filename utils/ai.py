import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
import logging
import base64
import requests
from PIL import Image
from io import BytesIO

load_dotenv()

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
token = os.getenv("GITHUB_API_KEY")
image_endpoint = "https://models.github.ai/images/generations"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

messages = [
    SystemMessage("You are a helpful assistant."),
]

def generate_text_response(prompt: str) -> str:
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
    logging.info("AI response successfully generated: " + str(gpt_reply))
    return str(gpt_reply)

def generate_text_from_image_response(prompt: str, image_source: str, is_local_file: bool = False) -> str:
    """
    Generate a text response from an image and a text prompt
    
    Args:
        prompt (str): The text prompt to send alongside the image
        image_source (str): The URL of the image
        is_local_file (bool): Whether the image_source is a local file path
        
    Returns:
        str: Generated response text
    """
    # For the GitHub AI API, we can only use image_url
    # So if we have a local file, we need to convert it to a URL somehow
    
    if is_local_file:
        # This is a placeholder - in a real implementation, you would need to
        # upload the image to a temporary storage service and get a URL
        logging.error("Local file processing is not supported by the API")
        return "Sorry, local file processing is not currently supported. Please provide an image URL instead."
    
    # Handle image URL
    image_content = {
        "type": "image_url",
        "image_url": {
            "url": image_source
        }
    }
    
    messages.append(
        UserMessage(
            content=[
                {
                    "type": "text",
                    "text": str(prompt)
                },
                image_content
            ]
        )
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
        logging.error("Failed to process image prompt. With error: " + str(e))
        return f"Error processing image: {str(e)}"
    
    logging.info("AI response content: " + str(response.choices))
    gpt_reply = response.choices[0].message.content
    logging.info("AI response for image successfully generated: " + str(gpt_reply))
    
    messages.append(
        AssistantMessage(gpt_reply),
    )
    return str(gpt_reply)

def generate_image(prompt: str) -> dict:
    messages.clear()
    messages.append(
        SystemMessage("""You will generate only random images using my prompt with sizes of 1280x1280 maximum and return a list of image URLs. 
                      The response should be in this structure: 
                      {\"image_url\": {\"url\": \"https://example.com/image.jpg\"}}.
                      """),
    )
    messages.append(
        UserMessage(str(prompt)),
    )
    try:
        response = client.complete(
            messages=messages,
            max_tokens=4096,
            model=model,
            temperature=0.7,
            top_p=0.4
        )
    except Exception as e:
        logging.error("Failed to recognize prompt. With error: " + str(e))
        return None
    
    logging.info("AI response content: " + str(response.choices))
    gpt_reply = response.choices[0].message.content

    # Parse the JSON string into a dictionary
    try:
        image_data = json.loads(gpt_reply)
        image_urls = image_data  # This is now a proper dictionary
        logging.info("AI response successfully generated: " + str(image_urls))
        return image_urls
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response: {e}")
        raise
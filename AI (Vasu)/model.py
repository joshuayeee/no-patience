# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types
import csv


# Extracts CSV data
def extract_csv(pathname: str) -> list[str]:
    parts = [f"---START OF CSV ${pathname} ---"]
    with open(pathname, "r", newline = "") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            str = " "
            parts.append(str.join(row))

    return parts

def generate():
    client = genai.Client(
        api_key=getenv("GEMINI_API_KEY"),
    )

    model = "gemini-3-flash-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH",
        ),
        tools=tools,
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
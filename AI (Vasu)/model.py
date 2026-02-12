import base64
import os
from google import genai
from google.genai import types
from google.genai import errors
import csv
from pathlib import Path

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
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    csv_file_path = "data/VoluntaryLimitation.csv"
    csv_data_parts = extract_csv(csv_file_path)
    csv_text = "\n".join(csv_data_parts)
    user_question = input("Ask a question: ")

    full_prompt = f"Data:\n{csv_text}\n\nQuestion: {user_question}"

    model = "gemini-3-flash-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=full_prompt),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="LOW",
        ),
        tools=tools,
    )

    print("\nResponse:")
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.text:
            print(chunk.text, end="")

if __name__ == "__main__":
    generate()
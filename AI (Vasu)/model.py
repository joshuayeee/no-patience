from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import pandas as pd

tokenizer = AutoTokenizer.from_pretrained("vaishali/multitabqa-base")
model = AutoModelForSeq2SeqLM.from_pretrained("vaishali/multitabqa-base")

# Example tables
VoluntaryLimitation = pd.read_csv("data/VoluntaryLimitation.csv")

# Flatten tables into a model-readable string
def linearize_table(table_name, df):
    cols = " | ".join(df.columns)
    rows = " ".join([
        f"row {i+1} : " + " | ".join(map(str, row)) 
        for i, row in df.iterrows()
    ])
    return f" : {table_name} col : {cols} {rows}"

question = "What is the effective date of the voluntary limitation that prevents lifting of equipment over 20 lbs?"
table_context = linearize_table("Voluntary Limitation", VoluntaryLimitation)
model_input_string = f"question: {question} table: {table_context}"

inputs = tokenizer(model_input_string, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50, num_beams=4)
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Answer: ", answer)

'''
import base64
import os
from google import genai
from google.genai import types
from google.genai import errors
import csv
from pathlib import Path
import time

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
        tools=tools,
    )

    print("\nResponse:")
    
    while True:
        try:
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if chunk.text:
                    print(chunk.text, end="")

            break

        except errors.ClientError as e:
            if "429" in str(e):
                print("\n[Quota reached. Retrying in 30 seconds...]")
                time.sleep(30)
            else:
                raise e


if __name__ == "__main__":
    generate()

'''
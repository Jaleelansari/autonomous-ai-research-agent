from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)


def summarize_text(text):

    response = client.chat.completions.create(
        model="mistralai/mixtral-8x7b-instruct-v0.1",
        messages=[
            {
                "role": "system",
                "content": "You are an expert research assistant."
            },
            {
                "role": "user",
                "content": f"""
                Summarize this research paper.

                Include:
                1. Objective
                2. Methodology
                3. Key Findings
                4. Limitations
                5. Future Scope

                Research Paper:
                {text[:3000]}
                """
            }
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    extracted_folder = "data/extracted_text"

    summary_folder = "data/summaries"

    os.makedirs(summary_folder, exist_ok=True)

    for file in os.listdir(extracted_folder):

        if file.endswith(".txt"):

            file_path = os.path.join(extracted_folder, file)

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            print(f"Summarizing {file}...")

            summary = summarize_text(text)

            output_path = os.path.join(
                summary_folder,
                file.replace(".txt", "_summary.txt")
            )

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(summary)

            print(f"Saved: {output_path}")
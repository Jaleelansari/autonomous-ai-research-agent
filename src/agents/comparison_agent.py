from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)


def compare_papers(combined_text):

    response = client.chat.completions.create(
        model="mistralai/mixtral-8x7b-instruct-v0.1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert AI research analyst."
                )
            },
            {
                "role": "user",
                "content": f"""
                Compare these research papers professionally.

                Include:
                1. Common Themes
                2. Key Differences
                3. Methodologies Used
                4. Strengths
                5. Weaknesses
                6. Future Research Directions

                Research Summaries:
                {combined_text[:12000]}
                """
            }
        ],
        temperature=0.3,
        max_tokens=1200
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    summary_folder = "data/summaries"

    combined_text = ""

    for file in os.listdir(summary_folder):

        if file.endswith(".txt"):

            file_path = os.path.join(summary_folder, file)

            with open(file_path, "r", encoding="utf-8") as f:
                combined_text += f.read() + "\n\n"

    print("Comparing research papers...")

    comparison = compare_papers(combined_text)

    os.makedirs("reports", exist_ok=True)

    output_path = "reports/paper_comparison.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(comparison)

    print("Comparison report saved successfully!")
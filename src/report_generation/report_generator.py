from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)


def generate_report(comparison_text):

    response = client.chat.completions.create(
        model="mistralai/mixtral-8x7b-instruct-v0.1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional AI research report writer."
                )
            },
            {
                "role": "user",
                "content": f"""
                Generate a professional research report.

                Include:
                1. Executive Summary
                2. Introduction
                3. Research Analysis
                4. Comparative Insights
                5. Key Findings
                6. Challenges
                7. Future Research Directions
                8. Conclusion

                Research Comparison:
                {comparison_text[:12000]}
                """
            }
        ],
        temperature=0.3,
        max_tokens=1800
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    comparison_file = "reports/paper_comparison.txt"

    with open(comparison_file, "r", encoding="utf-8") as f:
        comparison_text = f.read()

    print("Generating AI research report...")

    report = generate_report(comparison_text)

    output_path = "reports/final_research_report.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print("Research report generated successfully!")
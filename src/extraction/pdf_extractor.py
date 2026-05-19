import fitz
import os


def extract_text(pdf_path):

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text


if __name__ == "__main__":

    pdf_folder = "data/papers"

    output_folder = "data/extracted_text"

    os.makedirs(output_folder, exist_ok=True)

    for pdf_file in os.listdir(pdf_folder):

        if pdf_file.endswith(".pdf"):

            pdf_path = os.path.join(pdf_folder, pdf_file)

            text = extract_text(pdf_path)

            output_path = os.path.join(
                output_folder,
                pdf_file.replace(".pdf", ".txt")
            )

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Extracted: {pdf_file}")
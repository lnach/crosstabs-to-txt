import pdfplumber
import os
import re

def clean_cell(text):
    if not text:
        return ""
    text = text.replace("\n", " ")
    text = re.sub(r"(\w+)-\s+(\w+)", r"\1\2", text)  # join hyphen-split words
    return text.strip()

def extract_all_tables(pdf_path, output_txt):
    all_blocks = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            print(f"🔍 Processing page {page_num}/{len(pdf.pages)}")
            table = page.extract_table()
            full_text = page.extract_text()

            if not table or not full_text:
                print(f"⏭️ Skipping page {page_num} (no table or text)")
                continue

            lines = full_text.split("\n")

            # --- Extract multiline question ---
            question_lines = []
            for line in lines:
                if "BANNER" in line.upper():
                    break
                if re.match(r"\d+\.\s", line.strip()) or re.match(r"\d+\.", line.strip()):
                    question_lines.append(line.strip())
                elif question_lines:
                    question_lines.append(line.strip())
            question_text = " ".join(question_lines).strip()

            # --- Extract banner ---
            banner_label = next((line.strip() for line in lines if "BANNER" in line.upper()), "")

            # --- Clean table ---
            table = [row for row in table if any(cell and cell.strip() for cell in row)]
            header_rows = table[:3]
            data_rows = table[3:]
            num_cols = max(len(row) for row in header_rows)

            full_headers = []
            value_row = []
            last_top = ""

            for col in range(num_cols):
                top = clean_cell(header_rows[0][col]) if col < len(header_rows[0]) else ""
                bottom = clean_cell(header_rows[1][col]) if col < len(header_rows[1]) else ""
                value = clean_cell(header_rows[2][col]) if col < len(header_rows[2]) else ""

                top = re.sub(r"-{2,}", "", top).strip()
                bottom = re.sub(r"-{2,}", "", bottom).strip()

                if top:
                    last_top = top
                elif not top and last_top:
                    top = last_top

                if top and bottom:
                    full_label = f"{top}: {bottom}"
                elif bottom:
                    full_label = f"{top or 'Unnamed'}: {bottom}"
                else:
                    full_label = top or "Unnamed"

                full_headers.append(full_label)
                value_row.append(value)

            all_data_rows = [value_row] + data_rows

            # Build block text
            block = [f"Page: {page_num}", f"Question: {question_text}", f"Banner: {banner_label}"]
            block.append(", ".join(full_headers))
            for row in all_data_rows:
                block.append(", ".join([str(cell) for cell in row[:len(full_headers)]]))
            all_blocks.append("\n".join(block))

    # Write final .txt file
    with open(output_txt, "w") as f:
        f.write("\n\n".join(all_blocks))

    print(f"\n📄 .txt saved to → {output_txt}")



if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(base_dir, "..", "Indiana State Senate District 8  - August 29, 2023 - Crosstabs.pdf")
    output_txt = os.path.join(base_dir, "..", "indiana_all_crosstabs_for_gpt.txt")
    extract_all_tables(pdf_path, output_txt)


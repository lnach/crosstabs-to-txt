import streamlit as st
import pdfplumber
import re
import tempfile
import os

st.set_page_config(page_title="Crosstab Extractor", layout="centered")

# --- Clean cell content ---
def clean_cell(text):
    if not text:
        return ""
    text = text.replace("\n", " ")
    text = re.sub(r"(\w+)-\s+(\w+)", r"\1\2", text)
    return text.strip()

<<<<<<< HEAD
# --- Live log placeholder ---
log_placeholder = st.empty()
log_messages = []

def log_callback(msg):
    log_messages.append(msg)
    log_placeholder.text("\n".join(log_messages))

# --- Table extraction logic ---
def extract_all_tables_to_txt(pdf_path, output_txt, log_callback=None):
=======
def extract_all_tables_to_txt(pdf_path):
>>>>>>> ce4dd66 (Fixed code so its working again)
    all_blocks = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            if log_callback:
                log_callback(f"🔍 Processing page {page_num}/{len(pdf.pages)}")

            table = page.extract_table()
            full_text = page.extract_text()

            if not table or not full_text:
                if log_callback:
                    log_callback(f"⏭️ Skipping page {page_num} (no table or text)")
                continue

            lines = full_text.split("\n")
<<<<<<< HEAD

            # Extract question and banner
=======
>>>>>>> ce4dd66 (Fixed code so its working again)
            question_lines = []

            for line in lines:
                if "BANNER" in line.upper():
                    break
                if re.match(r"\d+\.\s", line.strip()) or re.match(r"\d+\.", line.strip()):
                    question_lines.append(line.strip())
                elif question_lines:
                    question_lines.append(line.strip())

            question_text = " ".join(question_lines).strip()
            banner_label = next((line.strip() for line in lines if "BANNER" in line.upper()), "")

            # Clean and build table
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

            block = [f"Page: {page_num}", f"Question: {question_text}", f"Banner: {banner_label}"]
            block.append(", ".join(full_headers))
            for row in all_data_rows:
                block.append(", ".join([str(cell) for cell in row[:len(full_headers)]]))
            all_blocks.append("\n".join(block))

<<<<<<< HEAD
    with open(output_txt, "w") as f:
        f.write("\n\n".join(all_blocks))

    if log_callback:
        log_callback(f"\n✅ GPT-friendly .txt saved to → {output_txt}")
    return output_txt
=======
    return "\n\n".join(all_blocks)
>>>>>>> ce4dd66 (Fixed code so its working again)

# --- Streamlit UI ---
st.title("Crosstab to GPT Text Converter")
st.markdown("Upload a PDF of crosstabs, and download a cleaned `.txt` file formatted for ChatGPT.")

uploaded_file = st.file_uploader("📄 Upload your Crosstabs PDF", type=["pdf"])

if uploaded_file:
    default_filename = uploaded_file.name.replace(".pdf", "_for_gpt.txt")
    custom_filename = st.text_input("✏️ Name your .txt file (include `.txt`)", value=default_filename)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name

    with st.spinner("🔍 Extracting tables and formatting..."):
<<<<<<< HEAD
        txt_output_path = temp_pdf_path.replace(".pdf", "_for_gpt.txt")
        final_path = extract_all_tables_to_txt(temp_pdf_path, txt_output_path, log_callback=log_callback)

        with open(final_path, "r") as file:
            txt_content = file.read()
=======
        txt_content = extract_all_tables_to_txt(temp_pdf_path)
>>>>>>> ce4dd66 (Fixed code so its working again)

        st.success("✅ Done! Download your file below.")
        st.download_button(
            "⬇️ Download .txt file",
            data=txt_content,
            file_name=custom_filename,
            mime="text/plain"
        )

        st.subheader("Preview of Extracted Text")
        st.text_area("Scroll to preview:", txt_content[:2000], height=300)

        with st.expander("🔍 Show full extraction log"):
            st.text("\n".join(log_messages))

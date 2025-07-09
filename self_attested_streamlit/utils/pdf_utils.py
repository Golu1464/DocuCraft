import streamlit as st
from PyPDF2 import PdfMerger, PdfReader
import os

def merge_pdfs_ui():
    st.header("📄 Merge Aadhaar PDFs")

    uploaded_files = st.file_uploader(
        "Upload Aadhaar front and back PDFs (2 files recommended)",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.info(f"🧾 You uploaded {len(uploaded_files)} PDF file(s)")

        if st.button("🔗 Merge PDFs"):
            merger = PdfMerger()
            total_pages = 0

            for pdf in uploaded_files:
                reader = PdfReader(pdf)
                total_pages += len(reader.pages)
                merger.append(pdf)

            merged_pdf_path = "merged_output.pdf"
            with open(merged_pdf_path, "wb") as f_out:
                merger.write(f_out)

            with open(merged_pdf_path, "rb") as f:
                st.success(f"✅ Successfully merged {len(uploaded_files)} PDFs into one.")
                st.markdown(f"📄 **Total Pages in Merged PDF**: `{total_pages}`")
                st.download_button("📥 Download Merged PDF", f, file_name="merged_aadhaar.pdf")

            # Optional: Clean up file from server if not needed
            if os.path.exists(merged_pdf_path):
                os.remove(merged_pdf_path)

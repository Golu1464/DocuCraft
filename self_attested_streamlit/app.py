import streamlit as st
from utils import image_utils, pdf_utils

st.set_page_config(page_title="DocuCraft - SelfAttested Clone", layout="centered")

st.title("📎 DocuCraft — Document & Image Editor")
st.sidebar.title("🧰 Categories & Tools")

tool_category = st.sidebar.selectbox("Choose a Category", [
    "Attest",
    "Resize (Dimensions)",
    "Resize (KB)",
    "Merge",
    "Image Compression",
    "Cropping"
])

tool = None

if tool_category == "Attest":
    tool = st.sidebar.radio("Tools", ["Attest Signature", "Attest Name and Date"])

elif tool_category == "Resize (Dimensions)":
    tool = st.sidebar.radio("Tools", [
        "Resize Image (240x320px)",
        "Resize Image (3.5cm x 4.5cm)",
        "Post Card Image Resizer (4x6)",
        "Signature Editor (6cm x 2cm)",
        "Resize Signature (140x60px)"
    ])

elif tool_category == "Resize (KB)":
    tool = st.sidebar.radio("Tools", [
        "Resize Image in KB",
        "Agniveer Photo Resizer (10–20KB)",
        "Agniveer Signature Resizer (5–10KB)",
        "SSC Signature Resizer (10–20KB)"
    ])

elif tool_category == "Merge":
    tool = st.sidebar.radio("Tools", ["Merge Aadhaar Cards"])

elif tool_category == "Image Compression":
    tool = st.sidebar.radio("Tools", ["Image Compression Tool"])

elif tool_category == "Cropping":
    tool = st.sidebar.radio("Tools", ["Crop Image in cm/pixels", "Universal Image Cropper"])

# Tool → Function mapping
if tool in [
    "Resize Image (240x320px)", "Resize Image (3.5cm x 4.5cm)",
    "Post Card Image Resizer (4x6)", "Signature Editor (6cm x 2cm)",
    "Resize Signature (140x60px)"
]:
    image_utils.resize_image_ui(tool)

elif tool in [
    "Resize Image in KB", "Agniveer Photo Resizer (10–20KB)",
    "Agniveer Signature Resizer (5–10KB)", "SSC Signature Resizer (10–20KB)"
]:
    image_utils.compress_image_ui(tool)

elif tool in ["Attest Signature", "Attest Name and Date"]:
    image_utils.add_text_signature_ui(tool)

elif tool == "Merge Aadhaar Cards":
    pdf_utils.merge_pdfs_ui()

elif tool in ["Crop Image in cm/pixels", "Universal Image Cropper"]:
    image_utils.crop_image_ui(tool)

elif tool == "Image Compression Tool":
    image_utils.compress_image_ui(tool)

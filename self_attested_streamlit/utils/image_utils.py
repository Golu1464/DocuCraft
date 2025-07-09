
import streamlit as st
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import base64
import os
from streamlit_cropper import st_cropper

def resize_image_ui(tool=None):
    st.header("📐 Resize Image")

    # Define automatic resize presets
    cm_presets = {
        "Resize Image (3.5cm x 4.5cm)": (3.5, 4.5),
        "Post Card Image Resizer (4x6)": (10.16, 15.24),   # 4x6 inches in cm
        "Signature Editor (6cm x 2cm)": (6.0, 2.0),
    }
    px_presets = {
        "Resize Signature (140x60px)": (140, 60),
    }

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if not uploaded_file:
        return

    img = Image.open(uploaded_file)
    st.image(img, caption="Original Image", use_container_width=True)

    unit = st.radio("Unit", ["px", "cm", "inch"], horizontal=True)
    dpi = st.number_input("DPI (for cm/inch)", min_value=72, max_value=600, value=300)

    if tool == "Resize Image (240x320px)":
        # Manual Resize
        width = st.number_input("Width", value=img.width)
        height = st.number_input("Height", value=img.height)

    else:
        if tool in px_presets:
            width, height = px_presets[tool]
        elif tool in cm_presets:
            cm_w, cm_h = cm_presets[tool]
            if unit == "cm":
                width, height = cm_w * dpi / 2.54, cm_h * dpi / 2.54
            elif unit == "inch":
                width, height = cm_w / 2.54 * dpi, cm_h / 2.54 * dpi
            else:  # px
                width, height = int(cm_w * dpi / 2.54), int(cm_h * dpi / 2.54)
        else:
            st.error("Unsupported preset.")
            return

        st.markdown(f"🔁 **Auto Resize to:** `{int(width)} x {int(height)} px`")

    if st.button("Resize Image"):
        resized_img = img.resize((int(width), int(height)))
        st.image(resized_img, caption="Resized Image")
        save_image(resized_img)


def crop_image_ui(tool=None):
    st.header("✂️ Crop Image")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if not uploaded_file:
        return

    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Original Image", use_container_width=True)

    # Unit and DPI
    col1, col2 = st.columns(2)
    with col1:
        unit = st.radio("Choose Unit", ["pixels", "cm"])
    with col2:
        dpi = st.number_input("DPI (for cm → px)", value=300)

    # Crop size presets
    preset = st.selectbox("📏 Choose Crop Size", [
        "Free Crop",
        "Passport (3.5 x 4.5 cm)",
        "Signature (6 x 2 cm)",
        "Postcard (4 x 6 inch)",
        "Custom Size"
    ])

    aspect_ratio = None
    target_width_px, target_height_px = None, None

    if preset == "Passport (3.5 x 4.5 cm)":
        w_cm, h_cm = 3.5, 4.5
    elif preset == "Signature (6 x 2 cm)":
        w_cm, h_cm = 6, 2
    elif preset == "Postcard (4 x 6 inch)":
        # Convert inches to px manually
        w_cm, h_cm = 4 * 2.54, 6 * 2.54
    elif preset == "Custom Size":
        w_cm = st.number_input("Width", value=3.5)
        h_cm = st.number_input("Height", value=4.5)
    else:  # Free Crop
        w_cm = h_cm = None

    # Set aspect ratio and target px if available
    if w_cm and h_cm:
        aspect_ratio = (w_cm, h_cm)
        target_width_px = int(w_cm * dpi / 2.54)
        target_height_px = int(h_cm * dpi / 2.54)
        st.markdown(f"🔄 Target Crop: `{target_width_px} x {target_height_px}` px")

    # Crop
    st.markdown("**🔍 Select crop area below:**")
    cropped_img = st_cropper(img, box_color="#27ae60", aspect_ratio=aspect_ratio)

    if preset != "Free Crop" and target_width_px and target_height_px:
        cropped_img = cropped_img.resize((target_width_px, target_height_px))

    if st.button("✅ Crop & Download"):
        st.image(cropped_img, caption="🖼️ Cropped Image", use_container_width=True)
        buffer = BytesIO()
        cropped_img.save(buffer, format="PNG")
        buffer.seek(0)
        st.download_button("📥 Download Cropped Image", buffer, file_name="cropped_image.png")

def compress_image_ui(tool=None):
    st.header("🗜️ Compress Image")

    # Target size ranges in KB for auto tools
    size_targets = {
        "Agniveer Photo Resizer (10–20KB)": (10, 20),
        "Agniveer Signature Resizer (5–10KB)": (5, 10),
        "SSC Signature Resizer (10–20KB)": (10, 20)
    }

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if not uploaded_file:
        return

    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Original Image", use_container_width=True)

    if tool == "Resize Image in KB":
        # Manual compression
        quality = st.slider("Select Compression Quality", 10, 95, 60)
        if st.button("Compress Image"):
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=quality)
            buffer.seek(0)
            size_kb = len(buffer.getvalue()) / 1024
            st.success(f"✅ Final Size: {size_kb:.2f} KB")
            st.image(Image.open(buffer), caption="Compressed Image", use_column_width=True)
            st.download_button("Download Compressed Image", buffer, file_name="compressed.jpg")

    else:
        # Auto compression to range
        min_kb, max_kb = size_targets.get(tool, (10, 20))
        st.markdown(f"🎯 Target Size: **{min_kb}–{max_kb} KB**")

        if st.button("Compress Image"):
            result = compress_to_target(img, min_kb, max_kb)

            if isinstance(result, tuple) and result[0] == "RESIZED_ONLY":
                buffer = result[1]
                size_kb = len(buffer.getvalue()) / 1024
                st.warning("⚠️ Image could not be compressed within the exact range, but it was resized and compressed as much as possible.")
                st.success(f"Best Possible Size: {size_kb:.2f} KB")
                st.image(Image.open(buffer), caption="Best Compressed Image", use_container_width=True)
                st.download_button("Download Compressed Image", buffer, file_name="compressed.jpg")

            elif isinstance(result, BytesIO):
                size_kb = len(result.getvalue()) / 1024
                st.success(f"✅ Final Size: {size_kb:.2f} KB")
                st.image(Image.open(result), caption="Compressed Image", use_container_width=True)
                st.download_button("Download Compressed Image", result, file_name="compressed.jpg")

            else:
                st.error("❌ Unable to compress the image. Please try a smaller or simpler image.")

def compress_to_target(img, min_kb, max_kb):
    min_q, max_q = 5, 95
    max_attempts = 10

    # Resize large images down to max_dimension for better compression
    max_dimension = 512
    if max(img.size) > max_dimension:
        w, h = img.size
        if w > h:
            new_w = max_dimension
            new_h = int(h * max_dimension / w)
        else:
            new_h = max_dimension
            new_w = int(w * max_dimension / h)
        img = img.resize((new_w, new_h))

    attempt = 0
    best_buffer = None
    best_diff = float("inf")
    best_size = 0

    while min_q <= max_q and attempt < max_attempts:
        mid_q = (min_q + max_q) // 2
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=mid_q)
        size_kb = len(buffer.getvalue()) / 1024

        # Track best match
        diff = abs((min_kb + max_kb) / 2 - size_kb)
        if diff < best_diff:
            best_diff = diff
            best_buffer = buffer
            best_size = size_kb

        if min_kb <= size_kb <= max_kb:
            buffer.seek(0)
            return buffer
        elif size_kb > max_kb:
            min_q = mid_q + 1
        else:
            max_q = mid_q - 1
        attempt += 1

    # Best-effort return
    if best_buffer:
        best_buffer.seek(0)
        return ("RESIZED_ONLY", best_buffer)

    return None

def add_text_signature_ui(tool=None):
    st.header("✍️ Add Text / Signature / Date")

    main_image_file = st.file_uploader("Upload your main document/image", type=["jpg", "jpeg", "png"])
    if not main_image_file:
        return

    img = Image.open(main_image_file).convert("RGBA")
    draw = ImageDraw.Draw(img)

    if tool == "Attest Name and Date":
        text = st.text_input("Enter text (e.g., Name, Date)")
        font_size = st.slider("Font Size", 10, 100, 24)
        x = st.number_input("X position", 0, img.width, 50)
        y = st.number_input("Y position", 0, img.height, 50)

        if st.button("Add Text"):
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            draw.text((x, y), text, fill="black", font=font)
            st.image(img, caption="Image with Text", use_container_width=True)
            save_image(img.convert("RGB"))

    elif tool == "Attest Signature":
        signature_file = st.file_uploader("Upload Signature Image (PNG preferred)", type=["png", "jpg", "jpeg"])
        if signature_file:
            signature = Image.open(signature_file).convert("RGBA")

            # Show original signature
            st.image(signature, caption="Uploaded Signature", width=200)

            # Resize options
            st.markdown("### 🔧 Resize Signature Before Overlay")
            sig_width = st.number_input("Signature Width (px)", value=signature.width)
            sig_height = st.number_input("Signature Height (px)", value=signature.height)

            # Resize signature
            resized_signature = signature.resize((int(sig_width), int(sig_height)))

            # Position inputs
            x = st.number_input("X position", 0, img.width, 50, key="sig_x")
            y = st.number_input("Y position", 0, img.height, 50, key="sig_y")

            if st.button("Overlay Signature"):
                # Paste resized signature
                img.paste(resized_signature, (int(x), int(y)), mask=resized_signature)
                st.image(img, caption="Image with Signature", use_column_width=True)
                save_image(img.convert("RGB"))



def save_image(img, filename="edited_image.png"):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    st.download_button("Download Image", buffer, file_name=filename)

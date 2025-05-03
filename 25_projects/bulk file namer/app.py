import streamlit as st
import os
import tempfile
import shutil
import zipfile
from io import BytesIO

st.set_page_config(page_title="Bulk File Renamer", layout="centered")

st.title("📁 Bulk File Renamer")
st.write("Rename multiple uploaded files and download them as a ZIP.")

uploaded_files = st.file_uploader("Upload multiple files", accept_multiple_files=True)
new_base_name = st.text_input("Enter new base name for files (e.g., VacationPic)")
keep_extension = st.checkbox("Keep original file extensions", value=True)

if st.button("🔁 Rename Files") and uploaded_files and new_base_name:
    with tempfile.TemporaryDirectory() as temp_dir:
        renamed_files = []

        # Save uploaded files to temporary directory
        for file in uploaded_files:
            file_path = os.path.join(temp_dir, file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())

        # Rename files
        for count, filename in enumerate(os.listdir(temp_dir), start=1):
            old_path = os.path.join(temp_dir, filename)
            ext = os.path.splitext(filename)[1] if keep_extension else ""
            new_filename = f"{new_base_name}_{count}{ext}"
            new_path = os.path.join(temp_dir, new_filename)
            os.rename(old_path, new_path)
            renamed_files.append(new_path)

        # Create ZIP
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for file_path in renamed_files:
                zipf.write(file_path, os.path.basename(file_path))
        zip_buffer.seek(0)

        st.success("✅ Files renamed and zipped successfully!")
        st.download_button(
            label="📦 Download ZIP",
            data=zip_buffer,
            file_name="renamed_files.zip",
            mime="application/zip"
        )

else:
    st.info("Please upload files and enter a base name.")

st.caption("Made with ❤️ by Shayan")

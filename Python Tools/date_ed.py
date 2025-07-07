import os
import subprocess
import sys
import datetime

# ✅ Auto-install required libraries
try:
    import pikepdf
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pikepdf"])
    import pikepdf

try:
    import win32file, win32con, pywintypes
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
    subprocess.check_call([sys.executable, "-m", "pywin32_postinstall", "-install"])
    import win32file, win32con, pywintypes

# 📁 Get current folder
folder_path = os.getcwd()

# 🗂️ List PDF files
pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

# 🕒 Date for metadata and filesystem
mod_date_pdf = "D:20250701113400+05'30'"
mod_date_os = datetime.datetime(2025, 7, 1, 11, 34, 0)

# 🛠 Update PDF metadata using correct with block
def update_pdf_metadata(file_path):
    with pikepdf.Pdf.open(file_path, allow_overwriting_input=True) as pdf:
        with pdf.open_metadata() as meta:
            meta["pdf:ModDate"] = mod_date_pdf
            meta["pdf:CreationDate"] = mod_date_pdf
        pdf.save(file_path)

# 🛠 Update OS-level timestamps (Windows only)
def update_file_timestamp(file_path, dt):
    handle = win32file.CreateFile(
        file_path,
        win32con.GENERIC_WRITE,
        0,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL,
        None
    )
    wintime = pywintypes.Time(dt)
    win32file.SetFileTime(handle, wintime, wintime, wintime)
    handle.close()

# 🔁 Process each PDF
for pdf_file in pdf_files:
    full_path = os.path.join(folder_path, pdf_file)
    print(f"🔧 Processing: {pdf_file}")
    update_pdf_metadata(full_path)
    update_file_timestamp(full_path, mod_date_os)
    print(f"✅ Updated: {pdf_file}")

print("\n🎉 All PDFs updated to: 01-July-2025 11:34 AM IST (both metadata and OS timestamps)")

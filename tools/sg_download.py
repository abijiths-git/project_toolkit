import os
import time
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

# ---------- CONFIGURATION ----------
EXCEL_PATH = "part_numbers.xlsx"
DOWNLOAD_DIR = os.path.abspath("downloads")
URL = "https://catalog.speedgrip.treffertech.com/index.php?route=common/home"

# ---------- SETUP ----------
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Load the Excel file with part numbers and categories
df = pd.read_excel(EXCEL_PATH)
df = df.dropna(subset=['Part Number'])  # Remove rows without part number

for index, row in df.iterrows():
    part = str(row['Part Number']).strip()
    category = str(row['Category']).strip() if 'Category' in row else ""
    print(f"\n🔍 Searching for: {part} in category: {category}")
    
    # Create folder for this part
    part_folder = os.path.join(DOWNLOAD_DIR, str(part))
    os.makedirs(part_folder, exist_ok=True)
    
    # Set up Chrome for this part
    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": part_folder,
        "download.prompt_for_download": False,
        "directory_upgrade": True
    })
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=options)
    driver.get(URL)

    try:
        # ✅ Select the category before searching
        try:
            category_dropdown = Select(driver.find_element(By.NAME, "category_id"))
            category_found = False
            for option in category_dropdown.options:
                if option.text.strip().lower() == category.lower():
                    category_dropdown.select_by_visible_text(option.text.strip())
                    category_found = True
                    print(f"✅ Selected category: {option.text.strip()}")
                    break
            if not category_found:
                print(f"⚠️ Category '{category}' not found. Using default.")
        except NoSuchElementException:
            print("⚠️ Category dropdown not found.")

        # 🔍 Now search for the part
        search_box = driver.find_element(By.NAME, "search")
        search_box.clear()
        search_box.send_keys(part)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        # Try clicking "VIEW MORE"
        try:
            view_more = driver.find_element(By.LINK_TEXT, "VIEW MORE")
            view_more.click()
            time.sleep(2)
        except NoSuchElementException:
            print(f"⚠️  'VIEW MORE' not found for {part}, skipping...")
            driver.quit()
            continue

        # Handle file format dropdowns
        dropdowns = driver.find_elements(By.TAG_NAME, "select")
        print(f"🔧 Found {len(dropdowns)} dropdown(s) on the page after View More.")
        found = False

        for idx, dropdown in enumerate(dropdowns, start=1):
            try:
                select_element = Select(dropdown)
                options = [o.text.strip() for o in select_element.options if o.text.strip()]
                print(f" Dropdown {idx}: {options}")

                for option in select_element.options:
                    format_name = option.text.strip()
                    if not format_name or "Choose" in format_name:
                        continue

                    print(f" ⬇️ Downloading format: {format_name}")
                    select_element.select_by_visible_text(format_name)
                    time.sleep(1)

                    try:
                        download_button = dropdown.find_element(
                            By.XPATH, ".//following::a[contains(@class, 'rfq') and .//i[contains(@class, 'fa-download')]]"
                        )
                        download_button.click()
                        time.sleep(3)                        
                    except NoSuchElementException:
                        print(f" ⚠️ Download button not found after selecting {format_name}")

                found = True
                break

            except Exception as e:
                print(f" ⚠️ Skipping dropdown {idx} due to error: {e}")
                continue

        if not found:
            print(f"⚠️  No valid dropdown/download combo found for {part}")
            driver.save_screenshot(f"{part}_debug.png")
            print(f"📸 Screenshot saved for debugging: {part}_debug.png")

        # --- Try to download view images ---
        try:
            print(f"🖼️ Looking for image view download buttons for {part}...")

            view_labels = ['Isometric View', 'Front View', 'Top View', 'Side View']
            rows = driver.find_elements(By.XPATH, "//table//tr")

            for row in rows:
                try:
                    label = row.find_element(By.XPATH, ".//td[1]").text.strip()
                    if label in view_labels:
                        download_btn = row.find_element(By.XPATH, ".//td[2]//a[contains(text(), 'Download')]")
                        href = download_btn.get_attribute("href")
                        if href:
                            headers = {
                                "User-Agent": "Mozilla/5.0",
                                "Accept": "*/*",
                                "Connection": "keep-alive"
                            }

                            img_name = str(href.split("/")[-1]) or f"{label.replace(' ', '_')}.png"
                            img_path = os.path.join(part_folder, img_name)

                            try:
                                response = requests.get(href, headers=headers, stream=True)
                                if response.status_code == 200:
                                    with open(img_path, 'wb') as f:
                                        for chunk in response.iter_content(1024):
                                            f.write(chunk)
                                    print(f"📥 Downloaded {label} to {img_path}")
                                else:
                                    print(f"⚠️ Failed to download {label}. Status code: {response.status_code}")
                            except Exception as e:
                                print(f"⚠️ Error downloading {label}: {e}")
                except Exception as e:
                    print(f" ⚠️ Could not process row for {part}: {e}")
        except Exception as e:
            print(f"⚠️ Error finding view image buttons: {e}")

    except Exception as e:
        print(f"❌ Error processing part {part}: {e}")
    finally:
        driver.quit()

print("\n✅ All downloads completed. Files saved to:", DOWNLOAD_DIR)

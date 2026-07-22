import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def open_product(url):
    options = Options()
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    try:
        driver.maximize_window()
    except:
        pass

    return driver


def clean_and_parse_float(text):
    """
    Helper function to safely extract a number from strings like '32', '32-34', or '32 inches'.
    If it's a range, it takes the average or the first number.
    """
    # Find all numbers (including decimals)
    numbers = re.findall(r"\d+\.?\d*", text)
    if not numbers:
        return None
    # If it's a range like 32-34, take the average; otherwise just take the number
    floats = [float(n) for n in numbers]
    return sum(floats) / len(floats)


def extract_fit(driver):
    # First Strategy: Look for specific table/row details layout
    try:
        rows = driver.find_elements(By.XPATH, "//div[contains(@class,'index-row')]")

        for row in rows:
            try:
                key = row.find_element(By.XPATH, ".//div[1]").text.strip().upper()
                value = row.find_element(By.XPATH, ".//div[2]").text.strip()

                if key == "FIT":
                    print("PDP FIT :", value)
                    return value
            except:
                continue
    except:
        pass

    # Second Strategy: Scan through bullet points for fit keywords
    try:
        details = driver.find_elements(By.XPATH, "//li")
        for item in details:
            text = item.text.strip().upper()
            if "REGULAR FIT" in text:
                print("PDP FIT : REGULAR FIT")
                return "REGULAR FIT"
            if "SLIM FIT" in text:
                print("PDP FIT : SLIM FIT")
                return "SLIM FIT"
            if "RELAXED FIT" in text:
                print("PDP FIT : RELAXED FIT")
                return "RELAXED FIT"
            if "OVERSIZED FIT" in text:
                print("PDP FIT : OVERSIZED FIT")
                return "OVERSIZED FIT"
            if "EASY FIT" in text:
                print("PDP FIT : EASY FIT")
                return "EASY FIT"
    except:
        pass

    # Debug fallback: Capture current state when fit cannot be found
    try:
        body = driver.find_element(By.TAG_NAME, "body").text
        with open("fit_debug.txt", "w", encoding="utf-8") as f:
            f.write(body)
    except:
        pass

    print("PDP FIT : NOT FOUND")
    return ""


def extract_size_chart(driver, product_type):
    wait = WebDriverWait(driver, 8)
    size_chart_found = False

    # ---------------------------------------
    # Try Multiple Ways to Open Size Chart
    # ---------------------------------------
    button_xpaths = [
        "//button[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'SIZE CHART')]",
        "//span[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'SIZE CHART')]",
        "//a[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'SIZE CHART')]",
        "//div[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'SIZE CHART')]",
        "//*[contains(@class,'size-buttons-show-size-chart')]",
        "//*[contains(@class,'sizeChart')]",
    ]

    for xpath in button_xpaths:
        try:
            element = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].click();", element)
            size_chart_found = True
            print("Size Chart Opened via explicit button")
            break
        except:
            continue

    # Fallback: Try general 'SIZE' elements if specific chart button wasn't found
    if not size_chart_found:
        print("Trying to find clickable general Size elements...")
        try:
            all_elements = driver.find_elements(
                By.XPATH,
                "//*[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'SIZE')]",
            )
            print("Possible Size Elements Found:", len(all_elements))
            for e in all_elements:
                try:
                    if e.is_displayed():
                        driver.execute_script("arguments[0].click();", e)
                        size_chart_found = True
                        print("Size Chart Opened via fallback element")
                        break
                except:
                    pass
        except:
            pass

    # If still not found, check out-of-stock indicators
    if not size_chart_found:
        try:
            body_text = driver.find_element(By.TAG_NAME, "body").text.upper()
            if (
                "OUT OF STOCK" in body_text
                or "CURRENTLY OUT OF STOCK" in body_text
                or "SOLD OUT" in body_text
            ):
                print("Product is Out of Stock")
                return {"STATUS": "OUT_OF_STOCK"}
        except:
            pass

        print("Size Chart Not Found")
        return {}

    # ---------------------------------------
    # Wait for Table & Extract
    # ---------------------------------------
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        table = driver.find_element(By.TAG_NAME, "table")
        rows = table.find_elements(By.TAG_NAME, "tr")
    except Exception as e:
        print("Size chart clicked, but no table element appeared.", e)
        return {}

    if not rows:
        print("Table found but contains no rows.")
        return {}

    # ---------------------------------------
    # Read Headers
    # ---------------------------------------
    header_cells = rows[0].find_elements(By.XPATH, "./th|./td")
    headers = [h.text.strip().upper() for h in header_cells]
    print("Headers Found:", headers)

    size_col = 0  # Default fallback to first column if 'SIZE' isn't explicitly found
    waist_col = None
    brand_col = None

    for i, h in enumerate(headers):
        if "BRAND SIZE" in h:
            brand_col = i
        elif "SIZE" in h:
            size_col = i

        if product_type == "TOPWEAR":
            if "CHEST" in h or "BUST" in h:
                waist_col = i
        else:
            if "TO FIT WAIST" in h or "WAIST" in h or "BOTTOM" in h:
                waist_col = i

    # Fallback logic if target column keywords aren't matching perfectly
    if waist_col is None:
        # If we can't find Chest/Waist, guess the second column (index 1) as a last resort
        if len(headers) > 1:
            waist_col = 1
        else:
            print("Target measurement column (Chest/Waist) not found.")
            return {}

    # ---------------------------------------
    # Blank Header Offset
    # ---------------------------------------
    header_offset = 1 if (len(headers) > 0 and headers[0] == "") else 0

    # ---------------------------------------
    # Extract Sizes
    # ---------------------------------------
    sizes = {}

    for row in rows[1:]:
        cols = row.find_elements(By.XPATH, "./th|./td")
        values = [c.text.strip() for c in cols]

        if not values:
            continue

        try:
            # Determine correct index dynamically
            if brand_col is not None and (brand_col - header_offset) < len(values):
                target_idx = brand_col - header_offset
            else:
                target_idx = size_col - header_offset

            # Ensure index safety
            if target_idx >= len(values) or (waist_col - header_offset) >= len(
                values
            ):
                continue

            raw_size = values[target_idx].upper().strip()
            raw_waist = values[waist_col - header_offset]

            # Fixed: Typo resolved from clean_and_parse_flosat to clean_and_parse_float
            waist_val = clean_and_parse_float(raw_waist)
            if waist_val is None:
                continue

            # Normalize common size names
            if raw_size == "2XL":
                raw_size = "XXL"
            elif raw_size == "3XL":
                raw_size = "XXXL"

            sizes[raw_size] = waist_val
        except Exception as e:
            continue

    print("Extracted Waist/Chest Sizes:", sizes)
    return sizes
from extraction.size_chart_extractor import (
    extract_fit,
    extract_size_chart,
    open_product,
)
import pandas as pd
from utils.column_detector import detect_columns
from utils.reference_size_chart import get_reference_sizes
from verification.size_chart_verifier import compare_sizes

# -----------------------------------
# Report Path
# -----------------------------------
REPORT_PATH = "reports/denim_size_report.xlsx"


def generate_report(df):
    columns = detect_columns(df)

    print("Detected Columns:", columns)
    print("DF Columns List:", df.columns.tolist())

    all_results = []

    driver = open_product(df.iloc[0][columns["LINK"]])

    # -----------------------------------
    # Bottomwear Categories
    # -----------------------------------
    BOTTOMWEAR = {
        "JEANS",
        "DENIM",
        "TROUSER",
        "TROUSERS",
        "SHORTS",
        "JOGGERS",
        "TRACK PANTS",
        "TRACKPANTS",
        "CHINOS",
    }

    # -----------------------------------
    # Process Products
    # -----------------------------------
    for index, row in df.iterrows():
        print("\n===================================")
        print(f"Processing Product {index + 1}/{len(df)}")
        print("===================================")
        print("URL :", row[columns["LINK"]])

        subcategory = str(row[columns["SUBCATEGORY"]]).upper().strip()

        if subcategory in BOTTOMWEAR:
            product_type = "BOTTOMWEAR"
        else:
            product_type = "TOPWEAR"

        print("Detected Product Type :", product_type)
        gender = ""

        # ----------------------------
        # Get Gender from Excel
        # ----------------------------

        # Case 1: Dataset has a GENDER column
        if "GENDER" in columns and pd.notna(row[columns["GENDER"]]):
            gender = str(row[columns["GENDER"]]).strip().upper()
            print("Gender from GENDER column :", gender)

        # Case 2: Dataset has a LINE column
        elif "LINE" in columns and pd.notna(row[columns["LINE"]]):
            line = str(row[columns["LINE"]]).strip().upper()
            print("LINE :", line)

            if "WOMEN" in line:
                gender = "WOMEN"
            elif "MEN" in line:
                gender = "MEN"

        # Final fallback
        if gender == "":
            gender = "MEN"

        print("Using Gender :", gender)
        print("RAW PRODUCT TYPE :", product_type)
        report_row = {
            "STYLE": row[columns["STYLE"]],
            "SUB CATEGORY": row[columns["SUBCATEGORY"]],
            "LINK": row[columns["LINK"]],
            "GENDER": gender,
        }

        try:
            driver.get(row[columns["LINK"]])

            # Extract Fit
            fit = extract_fit(driver)
            print("PDP FIT :", fit)

            # Extract Size Chart
            extracted_sizes = extract_size_chart(driver, product_type)

            # --- STEP 1: Debug Log for Extracted Sizes ---
            print("Website Sizes:", extracted_sizes)
            print("Extracted Sizes :", extracted_sizes)

            reference = get_reference_sizes(
                product_type,
                gender,
                fit,
            )

            print("Reference :", reference)

            # ---------------------------------------
            # Out Of Stock
            # ---------------------------------------
            if extracted_sizes is None or (
                isinstance(extracted_sizes, dict)
                and extracted_sizes.get("STATUS") == "OUT_OF_STOCK"
            ):
                print("Product is Out of Stock")

                report_row["Extracted Size Chart"] = "OUT OF STOCK"
                report_row["Final Size Chart Verdict"] = "Not Applicable"

                all_results.append(report_row)
                continue

            # ---------------------------------------
            # Compare Sizes
            # ---------------------------------------
            result = compare_sizes(
                product_type,
                reference["SIZES"],
                extracted_sizes,
            )
            print("Reference Sizes:", reference["SIZES"])
            print("Website Sizes:", extracted_sizes)
            print("Comparison:", result)

            # ---------------------------------------
            # Extracted Size Chart Column
            # ---------------------------------------
            report_row["Extracted Size Chart"] = ", ".join(
                f"{size}-{value:g}"
                for size, value in extracted_sizes.items()
            )
            report_row["Reference Size Chart"] = ", ".join(
                f"{size}-{value:g}"
                for size, value in reference["SIZES"].items()
            )

            # ---------------------------------------
            # Final Verdict
            # Ignore NOT FOUND
            # ---------------------------------------
            incorrect = False

            for verdict in result.values():
                if verdict == "MISMATCH":
                    incorrect = True
                    break

            if incorrect:
                report_row["Final Size Chart Verdict"] = "Incorrect"
            else:
                report_row["Final Size Chart Verdict"] = "Correct"

        except Exception as e:
            print("ERROR :", e)

            report_row["Extracted Size Chart"] = "ERROR"
            report_row["Final Size Chart Verdict"] = "ERROR"

        all_results.append(report_row)

    # -----------------------------------
    # Close Browser
    # -----------------------------------
    driver.quit()

    # -----------------------------------
    # Generate Report & Return
    # -----------------------------------
    report_df = pd.DataFrame(all_results)
    report_df.to_excel(REPORT_PATH, index=False)

    print("\n===================================")
    print("REPORT GENERATED SUCCESSFULLY")
    print("Location :", REPORT_PATH)
    print("Total Products :", len(report_df))
    print("===================================")

    return report_df
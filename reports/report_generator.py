import pandas as pd
import os


def generate_report(all_results, report_path):

    # ---------------------------------------
    # Create DataFrame
    # ---------------------------------------

    report_df = pd.DataFrame(all_results)

    # ---------------------------------------
    # Check if Empty
    # ---------------------------------------

    if report_df.empty:

        print("\n===================================")
        print("NO DATA FOUND")
        print("===================================")

        return

    # ---------------------------------------
    # Create Reports Folder
    # ---------------------------------------

    os.makedirs(

        os.path.dirname(report_path),

        exist_ok=True

    )

    # ---------------------------------------
    # Save Report
    # ---------------------------------------

    report_df.to_excel(

        report_path,

        index=False

    )

    # ---------------------------------------
    # Success Message
    # ---------------------------------------

    print("\n===================================")
    print("REPORT GENERATED SUCCESSFULLY")
    print("Location :", report_path)
    print("Total Products :", len(report_df))
    print("===================================")
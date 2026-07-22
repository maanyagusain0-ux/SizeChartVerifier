def detect_columns(df):

    columns = {}

    for col in df.columns:

        name = str(col).strip().upper()

        # -------------------------------
        # LINK
        # -------------------------------

        if any(x in name for x in [

            "LINK",
            "URL",
            "PRODUCT URL",
            "MYNTRA"

        ]):

            columns["LINK"] = col

        # -------------------------------
        # STYLE
        # -------------------------------

        elif any(x in name for x in [

    "STYLE",
    "STYLE CODE",
    "FG CODE",
    "ARTICLE",
    "CODE"

]):
            columns["STYLE"] = col

        # -------------------------------
        # GENDER
        # -------------------------------

        elif any(x in name for x in [

            "GENDER",
            "A GENDER",
            "SEX"

        ]):

            columns["GENDER"] = col

        # -------------------------------
        # SUB CATEGORY
        # -------------------------------

        elif any(x in name for x in [

            "SUB CAT",
            "SUB CATEGORY",
            "CATEGORY",
            "CAT"

        ]):

            columns["SUBCATEGORY"] = col

        # -------------------------------
        # FIT
        # -------------------------------

        elif "FIT" in name:

            columns["FIT"] = col

    return columns
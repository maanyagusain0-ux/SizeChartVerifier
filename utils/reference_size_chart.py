# ==========================================
# TOPWEAR SIZE CHARTS
# ==========================================

MEN_TOP_REGULAR = {

    "XS": 36,
    "S": 38,
    "M": 40,
    "L": 42,
    "XL": 44,
    "XXL": 46

}

MEN_TOP_SLIM = {

    "XS": 36,
    "S": 38,
    "M": 40,
    "L": 42,
    "XL": 44,
    "XXL": 46

}

MEN_TOP_RELAXED = {

    "XS": 40,
    "S": 42,
    "M": 44,
    "L": 46,
    "XL": 48,
    "XXL": 50

}

WOMEN_TOP = {

    "XXS": 30,
    "XS": 32,
    "S": 34,
    "M": 36,
    "L": 38,
    "XL": 40,
    "XXL": 42

}

# ==========================================
# BOTTOMWEAR SIZE CHARTS
# ==========================================

MEN_BOTTOM = {

    "XS": 28,
    "S": 30,
    "M": 32,
    "L": 34,
    "XL": 36,
    "XXL": 38,
    "XXXL": 40

}

WOMEN_BOTTOM = {

    "XXS": 24,
    "XS": 25,
    "S": 28,
    "M": 30,
    "L": 32,
    "XL": 34

}

# ==========================================
# BELTS
# ==========================================

MEN_BELTS = {

    "85": 32,
    "90": 34,
    "95": 36,
    "105": 40

}

# ==========================================
# FITS
# ==========================================

MEN_SLIM_FITS = {

    "SLIM",
    "SLIM FIT",
    "SUPER SLIM",
    "SUPER SLIM FIT"

}

MEN_RELAXED_FITS = {

    "RELAXED",
    "RELAXED FIT",
    "OVERSIZED",
    "OVERSIZED FIT",
    "EASY",
    "EASY FIT",
    "FASHION"

}

# ==========================================
# NORMALIZE GENDER
# ==========================================

def normalize_gender(gender):

    gender = str(gender).strip().upper()

    if "WOMEN" in gender:
        return "WOMEN"

    if "FEMALE" in gender:
        return "WOMEN"

    if gender == "W":
        return "WOMEN"

    if "LADIES" in gender:
        return "WOMEN"

    if "GIRL" in gender:
        return "WOMEN"

    if "MEN" in gender:
        return "MEN"

    if "MALE" in gender:
        return "MEN"

    if gender == "M":
        return "MEN"

    if "BOY" in gender:
        return "MEN"

    return "UNKNOWN"

# ==========================================
# GET REFERENCE SIZE CHART
# ==========================================

# ==========================================
# GET REFERENCE SIZE CHART
# ==========================================

def get_reference_sizes(product_type, gender, fit=""):

    product_type = str(product_type).strip().upper()
    gender = normalize_gender(gender)
    fit = str(fit).strip().upper()

    print("\n==============================")
    print("PRODUCT TYPE :", product_type)
    print("GENDER       :", gender)
    print("FIT          :", fit)

    # ======================================
    # TOPWEAR
    # ======================================

    if product_type == "TOPWEAR":

        if gender == "MEN":

            # -------------------------------
            # SLIM FIT
            # -------------------------------

            if "SLIM" in fit:

                print("Reference : MEN TOPWEAR SLIM")

                return {

                    "TYPE": "TOPWEAR",

                    "CATEGORY": "MEN",

                    "SIZES": MEN_TOP_SLIM

                }

            # -------------------------------
            # RELAXED / EASY / OVERSIZED
            # -------------------------------

            elif (

                "RELAXED" in fit
                or "EASY" in fit
                or "OVERSIZED" in fit
                or "FASHION" in fit

            ):

                print("Reference : MEN TOPWEAR RELAXED")

                return {

                    "TYPE": "TOPWEAR",

                    "CATEGORY": "MEN",

                    "SIZES": MEN_TOP_RELAXED

                }

            # -------------------------------
            # REGULAR
            # -------------------------------

            else:

                print("Reference : MEN TOPWEAR REGULAR")

                return {

                    "TYPE": "TOPWEAR",

                    "CATEGORY": "MEN",

                    "SIZES": MEN_TOP_REGULAR

                }

        elif gender == "WOMEN":

            print("Reference : WOMEN TOPWEAR")

            return {

                "TYPE": "TOPWEAR",

                "CATEGORY": "WOMEN",

                "SIZES": WOMEN_TOP

            }

    # ======================================
    # BOTTOMWEAR
    # ======================================

    elif product_type == "BOTTOMWEAR":

        if gender == "MEN":

            print("Reference : MEN BOTTOMWEAR")

            return {

                "TYPE": "BOTTOMWEAR",

                "CATEGORY": "MEN",

                "SIZES": MEN_BOTTOM

            }

        elif gender == "WOMEN":

            print("Reference : WOMEN BOTTOMWEAR")

            return {

                "TYPE": "BOTTOMWEAR",

                "CATEGORY": "WOMEN",

                "SIZES": WOMEN_BOTTOM

            }

    # ======================================
    # BELTS
    # ======================================

    elif product_type == "BELTS":

        if gender == "MEN":

            print("Reference : MEN BELTS")

            return {

                "TYPE": "BELTS",

                "CATEGORY": "MEN",

                "SIZES": MEN_BELTS

            }

    # ======================================
    # UNKNOWN
    # ======================================

    print("Unknown Product Type or Gender")

    return {

        "TYPE": "UNKNOWN",

        "CATEGORY": "UNKNOWN",

        "SIZES": {}

    }

def compare_sizes(product_type, expected_sizes, extracted_sizes):

    results = {}

    # ---------------------------------------
    # Normalize Website Sizes
    # ---------------------------------------

    normalized_sizes = {}

    for website_size, value in extracted_sizes.items():

        key = str(website_size).strip().upper()

        if key == "2XL":
            key = "XXL"

        elif key == "3XL":
            key = "XXXL"

        normalized_sizes[key] = float(value)

    # ---------------------------------------
    # Detect Numeric Website Sizes
    # ---------------------------------------

    numeric_sizes = all(

        str(k).isdigit()

        for k in normalized_sizes.keys()

    )

    # ---------------------------------------
    # Convert Numeric Sizes using Reference
    # ---------------------------------------

    if numeric_sizes:

        converted = {}

        for alpha_size, reference_value in expected_sizes.items():

            for website_size, website_value in normalized_sizes.items():

                try:

                    if abs(float(reference_value) - float(website_value)) <= 0.01:

                        converted[alpha_size] = website_value

                except:

                    pass

        normalized_sizes = converted

    print("\n===================================")
    print("PRODUCT TYPE :", product_type)
    print("REFERENCE :", expected_sizes)
    print("WEBSITE :", normalized_sizes)
    print("===================================")

    # ---------------------------------------
    # Compare
    # ---------------------------------------

    for size, expected in expected_sizes.items():

        website = normalized_sizes.get(size)

        if website is None:

            results[size] = "NOT FOUND"

            continue

        try:

            if abs(float(expected) - float(website)) <= 0.01:

                results[size] = "MATCH"

            else:

                results[size] = "MISMATCH"

        except:

            results[size] = "ERROR"

    return results
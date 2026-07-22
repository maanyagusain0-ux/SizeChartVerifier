# Numeric Size Mapping

NUMERIC_SIZE_MAPPING = {

    "10": "S",
    "12": "M",
    "14": "L",
    "16": "XL",
    "18": "XXL"

}


def normalize_sizes(extracted_sizes):

    # If website already has letter sizes,
    # return them unchanged.

    if any(
        size in extracted_sizes
        for size in [
            "XS",
            "S",
            "M",
            "L",
            "XL",
            "XXL"
        ]
    ):

        return extracted_sizes

    normalized = {}

    for size, value in extracted_sizes.items():

        if size in NUMERIC_SIZE_MAPPING:

            normalized[
                NUMERIC_SIZE_MAPPING[size]
            ] = value

        else:

            normalized[size] = value

    return normalized
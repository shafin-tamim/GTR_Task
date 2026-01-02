# Agent 1: Data Extractor
def data_extractor(fetch_fn, query):
    return fetch_fn(query)


# Agent 2: Review Generator
def review_generator(phone1, phone2=None):
    if phone2:
        return (
            f"{phone1['model']} has a {phone1['camera']} camera and "
            f"{phone1['battery']}mAh battery. "
            f"Compared to {phone2['model']}, it offers better camera "
            f"performance and is recommended for photography."
        )

    return (
        f"{phone1['model']} features a {phone1['display']} display, "
        f"{phone1['battery']}mAh battery and {phone1['camera']} camera."
    )

def apply_filter(results, sort_by="similarity", order="desc"):
    reverse = True if order == "desc" else False
    key_func = (
        (lambda x: x.get("similarity", 0))
        if sort_by == "similarity"
        else (lambda x: x.get("price", 0))
    )
    return sorted(results, key=key_func, reverse=reverse)

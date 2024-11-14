def format_currency(value):
    """Format currency to PHP"""
    return "₱{:,.2f}".format(value)


def error_messages(form):
    error_messages = "; ".join(
        error for errors in form.errors.values() for error in errors
    )
    return error_messages


def paginate_suppliers(page, user_suppliers):
    """Paginate table values"""
    ITEMS_PER_PAGE = 10

    total_items = user_suppliers.get_total_suppliers()
    total_pages = max(1, (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)

    if total_pages <= 5:
        start_page = 1
        end_page = total_pages
    else:
        start_page = max(1, page - 2)
        end_page = min(total_pages, page + 2)

        if start_page == 1:
            end_page = 5
        elif end_page == total_pages:
            start_page = total_pages - 4

    offset = (page - 1) * ITEMS_PER_PAGE
    products = user_suppliers.get_all_paginated_suppliers(offset, ITEMS_PER_PAGE)

    return [products, start_page, end_page, total_pages]


def paginate_inventory(page, user_inventory):
    """Paginate table values"""
    ITEMS_PER_PAGE = 10

    total_items = user_inventory.get_total_items()
    total_pages = max(1, (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)

    if total_pages <= 5:
        start_page = 1
        end_page = total_pages
    else:
        start_page = max(1, page - 2)
        end_page = min(total_pages, page + 2)

        if start_page == 1:
            end_page = 5
        elif end_page == total_pages:
            start_page = total_pages - 4

    offset = (page - 1) * ITEMS_PER_PAGE
    products = user_inventory.get_all_paginated_items(offset, ITEMS_PER_PAGE)

    return [products, start_page, end_page, total_pages]

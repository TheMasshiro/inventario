def format_currency(value):
    """Format currency to PHP"""
    return "₱{:,.2f}".format(value)


def error_messages(form):
    for _, errors in form.errors.items():
        if errors:
            return errors[0]
    return ""

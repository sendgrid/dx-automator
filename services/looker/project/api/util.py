from datetime import datetime


def clean_key(key: str):
    """
    Removes caps and periods from key
    (seen in some json responses frm looker)
    """
    key_split = key.split(".")
    k = key_split[1].lower() if len(key_split) > 1 else key_split[0].lower()
    return k.replace("#", "sharp")


def clean_invoice_json(json_dict: dict, email_send_month: str,
                       total_ei_revenue: str):
    clean_dict = dict()
    for key in json_dict:
        cleaned = clean_key(key)
        if cleaned == email_send_month:
            d = datetime.strptime(json_dict[key], "%Y-%m")
            clean_dict[cleaned] = d
        elif cleaned == total_ei_revenue:
            li = list(json_dict[key].values())[0]
            for l in li:
                clean_dict[clean_key(l)] = li[l]
    return clean_dict

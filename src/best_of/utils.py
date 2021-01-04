import re
import textwrap
from datetime import datetime


def simplify_str(text: str) -> str:
    return re.compile(r"[^a-zA-Z0-9]").sub("", text.strip()).lower()


def diff_month(date1: datetime, date2: datetime) -> int:
    return (date1.year - date2.year) * 12 + date1.month - date2.month


def clean_whitespaces(text: str) -> str:
    return " ".join(text.split())


def simplify_number(num: int) -> str:
    num_converted = float("{:.2g}".format(num))
    magnitude = 0
    while abs(num_converted) >= 1000:
        magnitude += 1
        num_converted /= 1000.0
    return "{}{}".format(
        "{:f}".format(num_converted).rstrip("0").rstrip("."),
        ["", "K", "M", "B", "T"][magnitude],
    )


def remove_special_chars(text: str) -> str:
    return text.encode("ascii", "ignore").decode("ascii")


def process_description(text: str, max_lenght: int) -> str:
    if not text:
        return ""

    # Remove github emoji commands
    text = re.sub(":[a-zA-Z_]*:", "", text).strip()

    text = remove_special_chars(text).strip()
    text = text.replace('"', "")
    text = text.replace("<", "")
    text = text.replace(">", "")

    if not text:
        return text

    if not text.endswith("."):
        # make sure that the text always ends with a dot
        text += "."

    return clean_whitespaces(textwrap.shorten(text, width=max_lenght, placeholder=".."))


url_validator = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def is_valid_url(url: str) -> bool:
    return re.match(url_validator, url) is not None

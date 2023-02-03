#!/usr/bin/env python3

"""Extracts order info from Amazon order confirmation emails exported to plain text
run with -t to print results to terminal rather than outputting to file
"""

import datetime as dt
from pathlib import Path
import re
import sys

from helpers import string_to_date


def extract_data(text, target=None):
    "searches the text for the designated target data"
    match target:
        case "order_number":
            pattern = re.compile("Order #(.+)")
        case "order_date":
            pattern = re.compile("Date: (.+)")
        case "order_total":
            pattern = re.compile("[Order|Order Grand] Total:\s?\n(.+)")
        case "order_item":
            pattern = re.compile("Subject:.+order of (.+)")
        case _:
            raise ValueError
    result = re.search(pattern, text)
    if result:
        return result.group(1).strip()
    else:
        raise EOFError

def clean_date(date_string):
    "converts date string into formatted datetime object"
    date_obj = string_to_date(date_string).date()
    return date_obj.strftime("%d %b %Y")

def main():
    file_in = Path(sys.argv[1])
    text = file_in.read_text()
    onumber = extract_data(text, target="order_number")
    odate = extract_data(text, target="order_date")
    odate = clean_date(odate)
    ototal = extract_data(text, target="order_total")
    oitem = extract_data(text, target="order_item")
    output = f"- [ ] {odate}; total {ototal}; order {onumber}: {oitem}\n"
    if "-t" in sys.argv:
        print(output)
    else:
        file_out = Path("/Users/anthonygladman/Library/Mobile Documents/iCloud~md~obsidian/Documents/BibScrib/Household stuff/Amazon Purchases for YNAB.md")
        with file_out.open("a") as f:
            f.write(output)
        file_in.unlink()

if __name__ == '__main__':
    main()

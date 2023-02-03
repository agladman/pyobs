"""Extracts useful information from Virgin Media bills and squirts it into Obsidian"""

import re
import sys

from datetime import datetime as dt
from pathlib import Path
from config import VIRGIN_MEDIA_FILE, MEDIADIR
from PyPDF2 import PdfReader

from helpers import string_to_date


def get_pdf_text(filepath):
    """extracts text from the PDF at the given filepath
    more info: https://pypdf2.readthedocs.io/en/latest/modules/PageObject.html#PyPDF2._page.PageObject.extract_text"""
    reader = PdfReader(filepath)
    page = reader.pages[0]
    return page.extract_text()

def match(pattern, text):
    "find the `pattern` in the `text` if it's there"
    m = re.search(pattern, text)
    if m:
        return m.group(1)
    else:
        return False

def extract_data(text):
    "pulls out the useful bits"
    patterns = [
        re.compile("Bill date:\s+(\d{2} \w+ \d{4})"),   # bill date
        re.compile("Direct Debit date:\s+(\d{2} \w+ \d{4})"), # direct debit date
        re.compile("Amount due\s?£(\d{2,}\.\d{2})")]    # amount due
    bill_date = string_to_date(match(patterns[0], text))
    dd_date = string_to_date(match(patterns[1], text))
    amount_due = float(match(patterns[2], text))
    return (bill_date, dd_date, amount_due)

def rename_and_move_pdf(file_in, date_string):
    "renames `file_in` using the `date_string` and saves the file to the `MEDIADIR`"
    target = f"{MEDIADIR}/Virgin Media Invoice {date_string}.pdf"
    try:
        file_out = file_in.rename(target)
        return file_out.name
    except OSError as e:
        raise OSError(e)

def main():
    file_in = Path(sys.argv[1])
    text = get_pdf_text(file_in)
    bill_date, dd_date, amount_due = extract_data(text)
    pdf_file = rename_and_move_pdf(file_in, bill_date.strftime("%Y-%m-%d"))
    output = f"- [[{pdf_file}]] - £{amount_due} due {dd_date.strftime('%d %b %Y')}\n"
    if "-t" in sys.argv:
        print(output)
    else:
        with Path(VIRGIN_MEDIA_FILE).open("a") as f:
            f.write(output)

if __name__ == '__main__':
    main()

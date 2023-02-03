# PYOBS

Python scripts for automating stuff that will be useful with [Obsidian](https://obsidian.md).

## Kindle Notes
Place the exported kindle notebook in the `_kindle` folder then run `kindle.py`. Notes will be parsed into separate files and placed into the `_to Obsidian` folder where Hazel will take over and move them into the `imports` folder in that program. The script will also create a source info file and place it in there along with the notes.

## Virgin Media Bills
Have Hazel move a Virgin Media bill into the `_virgin` folder and run `virgin.py`. The script will:

- [x] Read the PDF
- [x] Extract the amount due
- [x] Extract the invoice date
- [x] Extract the payment due date
- [x] Rename the file with its invoice date
- [x] Move the file to the Obsidian media folder
- [x] Append a link to the file to `/Users/anthonygladman/Library/Mobile Documents/iCloud~md~obsidian/Documents/BibScrib/Household stuff/Virgin Media Broadband.md`, along with the amount due and when payment will be taken via direct debit
- [ ] Check for other virgin media invoices in the Media folder and keep only the 12 most recent, moving any older files to the desktop, and unlinking the relevant line in the Obsidian file

{% warning %}
**Warning:** remember to pass the PDF filename in quotes when calling this script from the terminal, e.g. `python3 virgin.py "_virgin/Virgin Media bill_2023_01_16.pdf"`
{% endwarning %}

## Amazon Orders
Save order confirmation emails as text files, have Hazel move them to the `_Amazon` folder and run `amazon.py`.
The script will:

- Extract the order date
- Extract the order number
- Extract the order amount
- Extract the item ordered
- Write this information to a file in Obsidian

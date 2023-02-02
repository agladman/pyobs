
"""cleans up kindle notebooks and create a source note and separate note files"""

from bs4 import BeautifulSoup
from pathlib import Path
import re

from helpers import timestamp, write_md


class Source:
    """source note object"""

    def __init__(self, book_title, authors):
        self.filename = Path(f"S.{timestamp()}.md")
        self.title = book_title
        self.short_title = self.get_short_title()
        self.authors = authors
        self.sort_authors()
        self.wikilink = self.get_wikilink()
        self.child_notes = []

    def __repr__(self):
        return f"{self.__class__} | {self.__dict__}"

    def __str__(self):
        return f"""---
tags: []
aliases: ["{self.authors}, {self.short_title}"]
---

Authors: {self.authors}
Title: {self.title}
ISBN:
Published:

###### Linked notes
- {self.print_child_notes()}
        """

    def sort_authors(self):
        """if name is last, first returns first last"""
        if "," not in self.authors:
            pass
        else:
            self.authors = re.sub(r"(.+), (.+)", r"\2 \1", self.authors)

    def get_short_title(self):
        """returns short version of book title"""
        m = re.match(r"(.+):", self.title)
        if m:
            return m.group(1)
        else:
            return self.title
            
    def get_wikilink(self):
        """returns wikilink string"""
        return f"[[{self.filename.stem}|{self.authors}, {self.short_title}]]"

    def add_child(self, child):
        child.source = f"{self.wikilink}, p{child.page}, loc {child.location}"
        self.child_notes.append(child)

    def print_child_notes(self):
        return "\n- ".join(n.wikilink for n in self.child_notes)

    def save(self):
        """writes note to a markdown file"""
        write_md(str(self), filename=self.filename)
        for c in self.child_notes:
            write_md(str(c), filename=c.filename)


class Note:
    """individual note taken from a source"""

    def __init__(self, soup, idx, quote=True):
        self.filename = Path(f"{timestamp()}.{str(idx + 1).zfill(3)}.md")
        self.note = None
        self.quote = None
        if quote is True:
            self.quote = self.get_note_text(soup)
        else:
            self.note = self.get_note_text(soup, quote=False)
        self.page = self.get_page(soup)
        self.location = self.get_loc(soup)
        self.source = None
        self.wikilink = self.get_wikilink()

    def __repr__(self):
        return f"{self.__class__} | {self.__dict__}"

    def __str__(self):
        return f"""---
tags: []
aliases: []
---

{self.quote if self.quote else ''}
{self.note if self.note else ''}
---

Source: {self.source}
        """

    def get_note_text(self, soup, quote=True):
        body = soup.get_text()
        text = re.match(r"(.+)", body)
        if quote is True:
            return "> " + self.multiple_replace(text.group(1)) + "\n"
        else:
            return text.group(1) + "\n"

    @staticmethod
    def multiple_replace(text):
        "see: https://stackoverflow.com/questions/15175142/how-can-i-do-multiple-substitutions-using-regex"
        dict = {
            '“ ': '"',
            ' ”': '"',
            " \u2019": "'",
            ' ,': ',',
            ' .': '.',
            ' :': ':',
            ' ;': ';',
            ' !': '!',
            ' ?': '?',
            # r"\s([.,:;!?])": r"\1", # doesn't seem to work here!
            '( ': '(',
            ' )': ')',
            ' - ': '-',
            ' • ': '\n> - '
        }
        # Create a regular expression  from the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
        # For each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)

    @staticmethod
    def get_page(soup):
        note_heading = soup.get_text()
        pmatch = re.search(r"Page (\d+)", note_heading)
        if not pmatch:
            return '000'
        else:
            return pmatch.group(1)

    @staticmethod
    def get_loc(soup):
        note_heading = soup.get_text()
        lmatch = re.search(r"Location (\d+)", note_heading)
        if not lmatch:
            return '000'
        else:
            return lmatch.group(1)

    def append_note(self, soup):
        self.note = self.get_note_text(soup, quote=False)

    def get_wikilink(self):
        """returns wikilink string"""
        return f"[[{self.filename.stem}|note from p{self.page}]]"

    def save(self):
        """writes note to a markdown file"""
        write_md(str(self), filename=self.filename)



def get_soup(path_obj):
    "parse html file with BeautifulSoup"
    # soup = BeautifulSoup.BeautifulSoup(content.decode('utf-8','ignore'))
    with path_obj.open("r", encoding="utf-8", errors="replace") as f:
        return BeautifulSoup(f, "html.parser")

def source(soup):
    "returns source note wikilink details"
    book_title = soup.find_all("div", class_="bookTitle")[0].get_text()
    authors = soup.find_all("div", class_="authors")[0].get_text() # except what if there's more than one author
    return Source(book_title.strip("\n"), authors.strip("\n"))

def check_type(soup):
    "return whether this is a note or a highlight"
    text = soup.get_text()
    if re.match(r"^Note ", text):
        return 1
    elif re.match(r"^Highlight ", text):
        return 0
    else:
        return False

def make_notes(soup, source):
    "parse soup for individual highlights and notes"
    tags = soup.find_all("h3", class_="noteHeading")
    divs = soup.find_all("div", class_="noteText")
    holding = None
    for i, (item_head, item_content) in enumerate(zip(tags, divs)):
        z = check_type(item_head)
        if z == 0:
            if holding is not None:
                source.add_child(holding)
            holding = Note(item_content, i)
        elif z == 1:
            if holding is not None:
                holding.append_note(item_content)
            else:
                holding = Note(item_content, i, quote=False)
        elif z is False:
            pass

def main():
    input_f = Path("_kindle")
    for f in input_f.iterdir():
        if f.is_file():
            html = get_soup(f)
            s = source(html)
            make_notes(html, s)
            s.save()
            print("run complete")

if __name__ == '__main__':
    main()

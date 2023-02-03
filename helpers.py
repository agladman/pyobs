"""helper functions for all"""

from datetime import datetime as dt
# from functools import wraps
# import json
# import logging.config
from pathlib import Path

from config import OUTDIR


# default_path=Path("logging.json")
# default_level=logging.DEBUG

# if default_path.exists():
#     with open(default_path, 'rt') as f:
#         config = json.load(f)
#     logging.config.dictConfig(config)
# else:
#     logging.basicConfig(level=default_level)

# logger = logging.getLogger(__name__)

# def log(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         args_repr = [repr(a) for a in args]
#         kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
#         signature = ", ".join(args_repr + kwargs_repr)
#         logger.debug(f"function {func.__name__} called with args {signature}")
#         try:
#             result = func(*args, **kwargs)
#             return result
#         except Exception as e:
#             logger.error(f"Exception raised in {func.__name__}: {type(e).__name__}", exc_info=False)
#             raise e
#     return wrapper

def timestamp(time=dt.now(), format="zk", sep=False) -> str:
    """returns a formatted timestamp string
    formats:
        zk: zettelkasten
        rd: readable
        sd: standard"""
    formats = {
        "zk": "%Y%m%d%H%M%S",
        "rd": "%a %d %B %Y, %H:%M:%S",
        "sd": "%Y-%m-%d %H:%M:%S"
        }
    timestamp = time.strftime(formats[format])
    if sep is True:
        return "".join(ch for ch in timestamp if ch not in " -,:")
    else:
        return timestamp
    
def write_md(data, filename=None):
    "write stuff to a markdown file"
    if filename is None:
        filename = Path(f"{timestamp()}.md")
    outfile = Path(OUTDIR).joinpath(filename)
    with outfile.open("w", encoding="utf-8") as f:
        f.write(data)

def get_byte_position(filename):
    "from https://stackoverflow.com/questions/21559181/how-to-find-the-byte-position-of-specific-line-in-a-file"
    # OSError: telling position disabled by next() call
    # returning, so reads whole file w/o throwing the exception. FACK.
    position = 0  # or wherever you left off last time
    try:
        with open(filename, encoding="utf-8") as file:
            file.seek(position)  # zero in base case
            for line in file:
                # position = file.tell() # current seek position in file
                # process the line
                position += len(line)
    except:
        print(f'exception occurred at position {position}')
        raise
    return position

def string_to_date(date_string):
    "converts `date_string` to a datetime object"
    for fmt in ("%d %b %Y", "%d %B %Y", "%d %B %Y at %H:%M:%S %Z"):
        try:
            return dt.strptime(date_string, fmt)
        except ValueError:
            pass
    raise ValueError("No valid date format found")

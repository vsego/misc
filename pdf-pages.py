#!/usr/bin/env python3

"""
A native Python module to get pages' sizes from PDF.

I needed this to get pages' sizes from huge PDFs (containing large images)
without big memory consumption.

Done by following [Portable Document Format – Part 1: PDF 1.7, First Edition]
(https://wwwimages2.adobe.com/content/dam/acom/en/devnet/pdf/PDF32000_2008.pdf)
found [here](https://www.adobe.com/devnet/pdf/pdf_reference.html).
"""

from math import log10
import re
from sys import argv


def _pages_tree_to_list(pages, root=None):
    """
    Return list of pages in the right order from PDF's tree.
    """
    if root is None:
        root = next(
            ref
            for ref in pages
            if not any(ref in pgs for pgs in pages.values())
        )
    result = list()
    for ref in pages[root]:
        if ref in pages:
            result.extend(_pages_tree_to_list(pages, ref))
        else:
            result.append(ref)
    return result


def _str_to_num(s):
    """
    Return string converted to `int` or `float`.
    """
    try:
        return int(s)
    except ValueError:
        return float(s)


def _ref_m_to_tuple(m):
    """
    Return reference tuple from RegEx `Match`.
    """
    return int(m.group("m")), int(m.group("n"))


def pdf_pages_sizes(fp, chunk_size=1024**2, units="px"):
    """
    Return list of sizes for PDF in stream `fp` (open file, `StringIO`, etc).

    :param chunk_size: The size of the chunks to be read from the file.
        Shouldn't be too small (at least 10 or so). Smaller will usually mean
        slower, while bigger uses more memory. The default of 1 MiB seems to
        work just fine.
    :param units: A string describing in which units should the result be
        returned. Possible values: `"px"` (the default), `"in"`, `"mm"`,
        `"cm"`.
    :return: List of `(width, height)` tuples, each corresponding to one page.
        The values are given in the unit corresponding with the `units`
        parameter.
    """
    # Debug print
    def print_data():
        print({k: v for k, v in data.items() if k != "text"})
    # Get page size for a given reference
    def get_mediabox(ref):
        supported_units = {
            "px": 1, "in": 1.0 / 72, "mm": 25.4 / 72, "cm": 2.54 / 72,
        }
        mediabox = data["mediaboxes"][ref]
        unit_factor = supported_units[units]
        while ref:
            unit_factor *= data["units"].get(ref, 1)
            ref = data["parents"].get(ref)
        return tuple(value * unit_factor for value in mediabox[2:])
    # Functions to handle recognised PDF entities
    def obj(m):
        if data["depth"] == 0:
            data["ref"] = _ref_m_to_tuple(m)
    def start(m):
        data["depth"] += 1
    def object_type(m):
        if data["depth"] == 1:
            data["type"] = m.group("type")
    def mediabox(m):
        data["mediabox"] = tuple(
            _str_to_num(d) for d in re.split(r"\s+", m.group("size"))
        )
    def end(m):
        data["depth"] -= 1
        assert data["depth"] >= 0
        if data["depth"] == 0:
            if data["ref"]:
                if data["type"] == "Page" and data["mediabox"]:
                    data["mediaboxes"][data["ref"]] = data["mediabox"]
                elif data["type"] == "Pages" and data["kids"]:
                    data["pages"][data["ref"]] = data["kids"]
            data["ref"] = None
            data["type"] = None
            data["mediabox"] = None
            data["kids"] = list()
    def stream(m):
        data["in_stream"] = True
    def endstream(m):
        data["in_stream"] = False
        data["needs_fresh_pos"] = True
    def kids(m):
        assert not data["kids"]
        kids_list = re.split(r"\s+", m.group("kids"))
        new_kids = [
            (int(m), int(n)) for m, n in zip(kids_list[0::3], kids_list[1::3])
        ]
        data["kids"].extend(new_kids)
        if data["ref"] is not None:
            data["parents"].update({kid: data["ref"] for kid in new_kids})
    def parent(m):
        assert data["ref"] is not None
        data["parents"][data["ref"]] = _ref_m_to_tuple(m)
    def userunit(m):
        if data["depth"] == 1 and data["ref"]:
            data["units"][data["ref"]] = _str_to_num(m.group("unit"))

    # Regx Strings (subexpressions to use):
    rs_one_to_list = r"{fmt}(?:\s+{fmt})*"
    rs_ref = r"\d+\s+\d+\s+R"
    rs_refs = rs_one_to_list.format(fmt=rs_ref)
    rs_nref = r"(?P<m>\d+)\s+(?P<n>\d+)\s+R"  # TODO \b
    rs_float = r"(?:\b\d+(?:\.\d*)?|\.\d+\b)"
    rs_floats = rs_one_to_list.format(fmt=rs_float)

    # What to search for -> the function to handle it.
    searches = {
        r"(?P<m>\d+)\s+(?P<n>\d+)\s+obj\b": obj,
        r"<<": start,
        r"/Type\s*/(?P<type>\w+)": object_type,
        r"/MediaBox\s*\[\s*(?P<size>" + rs_floats + r")\s*\]": mediabox,
        r">>": end,
        r"\bstream\b": stream,
        r"\bendstream\b": endstream,
        r"/Kids\s*\[\s*(?P<kids>" + rs_refs + r")\s*\]": kids,
        r"/Parent\s+" + rs_nref: parent,
        r"/UserUnit\s*(?P<unit>" + rs_float + r")": userunit,
    }
    # re has caching, but this allows us to use `pos` argument with `search`,
    # which gives a nice speed improvement over cropping the text all the time.
    compiled_searches = {restr: re.compile(restr) for restr in searches}

    # Initial data; we could use normal variables and `nonlocal` instead,
    # but this seemed neater and it is compatible with Python 2, which is
    # where I need this module (a legacy project).
    data = {
        "depth": 0,
        "in_stream": False,
        "kids": list(),
        "mediabox": None,
        "mediaboxes": dict(),
        "needs_fresh_pos": True,
        "pages": dict(),
        "parents": dict(),
        "ref": None,
        "text": "",
        "type": None,
        "units": dict(),
    }

    # Read and analyze the PDF.
    old_chunk = ""
    while True:
        # Read the next chunk and add it to the current text.
        chunk = fp.read(chunk_size)
        if not chunk:
            break
        chunk = chunk.decode("latin-1")
        data["text"] = old_chunk + chunk

        # Chip those elements away, until none are left.
        pos = dict()
        offset = 0
        data["needs_fresh_pos"] = True
        while data["needs_fresh_pos"] or pos:
            # Find all the elements that we recognise.
            if data["needs_fresh_pos"]:
                pos = {
                    restr: match
                    for restr, match in (
                        (
                            restr,
                            compiled_searches[restr].search(
                                data["text"], pos=offset,
                            ),
                        )
                        for restr in searches.keys()
                        if (
                            not data["in_stream"]
                            or searches[restr].__name__ == "endstream"
                        )
                    )
                    if match
                }
                if not pos:
                    break
                data["needs_fresh_pos"] = False

            # Get the leftmost matched element.
            restr, match = min(pos.items(), key=lambda it: it[1].start())

            # Process it...
            func = searches[restr]
            if not data["in_stream"] or func.__name__ == "endstream":
                # ...but only if not in stream or is a keyword that ends
                # streams.
                func(match)

            # Reset the offset (to ignore the processed part of the text).
            offset = match.end()

            # Find the next `restr` element and update the dictionary of
            # found elements.
            if not data["needs_fresh_pos"]:
                match = compiled_searches[restr].search(
                    data["text"], pos=offset,
                )
                if match:
                    pos[restr] = match
                else:
                    pos.pop(restr)

        # Remove unneeded text.
        # This is the reason why chunk_size shouldn't be too small. Basically,
        # it must be bigger than the length of anything (except the `/Kids`
        # element) that we can find.
        if offset:
            data["text"] = data["text"][offset:]
        old_chunk = (
            data["text"]
            if "/Kids" in data["text"] else
            data["text"] if len(data["text"]) < len(chunk) else chunk
        )

    # Order the pages, get their sizes and return those as a list.
    pages = _pages_tree_to_list(data["pages"])
    assert len(pages) == len(data["mediaboxes"])
    return [get_mediabox(ref) for ref in pages]


if __name__ == "__main__":
    try:
        fname = argv[1]
    except IndexError:
        print("Usage: {cmd} file_name.pdf [units]".format(cmd=argv[0]))
    else:
        try:
            units = argv[2]
        except IndexError:
            units = "px"
        with open(fname, "rb") as f:
            sizes = pdf_pages_sizes(f, units=units)
            if sizes:
                fmt = "  {{num:{max_len}d}}. {{size}}".format(
                    max_len=int(log10(len(sizes)) + 1),
                )
                print("Pages' sizes:")
                for num, size in enumerate(sizes, start=1):
                    print(fmt.format(
                        num=num,
                        size="{w:.2f} x {h:.2f} {units}".format(
                            w=size[0], h=size[1], units=units,
                        ),
                    ))
            else:
                print("Not a single page in this PDF?!?")

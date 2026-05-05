"""BibTeX special character encoder/decoder.

Converts between Unicode characters and LaTeX escape sequences,
e.g. ö <-> {\\"o}, é <-> {\'e}, ñ <-> {\\~n}.
"""

import re

# Mapping from Unicode char to LaTeX command
_UNICODE_TO_LATEX: dict[str, str] = {
    "à": "{\\`a}", "á": "{\\'a}", "â": "{\\^a}", "ä": '{\\"a}',
    "ã": "{\\~a}", "å": "{\\aa}", "æ": "{\\ae}",
    "è": "{\\`e}", "é": "{\\'e}", "ê": "{\\^e}", "ë": '{\\"e}',
    "ì": "{\\`i}", "í": "{\\'i}", "î": "{\\^i}", "ï": '{\\"i}',
    "ò": "{\\`o}", "ó": "{\\'o}", "ô": "{\\^o}", "ö": '{\\"o}',
    "õ": "{\\~o}", "ø": "{\\o}",
    "ù": "{\\`u}", "ú": "{\\'u}", "û": "{\\^u}", "ü": '{\\"u}',
    "ý": "{\\'y}", "ÿ": '{\\"y}',
    "ñ": "{\\~n}", "ç": "{\\c{c}}",
    "ß": "{\\ss}",
    "À": "{\\`A}", "Á": "{\\'A}", "Â": "{\\^A}", "Ä": '{\\"A}',
    "È": "{\\`E}", "É": "{\\'E}", "Ê": "{\\^E}", "Ë": '{\\"E}',
    "Ì": "{\\`I}", "Í": "{\\'I}", "Î": "{\\^I}", "Ï": '{\\"I}',
    "Ò": "{\\`O}", "Ó": "{\\'O}", "Ô": "{\\^O}", "Ö": '{\\"O}',
    "Ù": "{\\`U}", "Ú": "{\\'U}", "Û": "{\\^U}", "Ü": '{\\"U}',
    "Ñ": "{\\~N}", "Ç": "{\\c{C}}",
}

# Reverse mapping: LaTeX -> Unicode
_LATEX_TO_UNICODE: dict[str, str] = {v: k for k, v in _UNICODE_TO_LATEX.items()}

# Pattern to match LaTeX escape sequences
_LATEX_PATTERN = re.compile(
    r"\{\\[`'\"\^~cso][a-zA-Z]?(?:\{[a-zA-Z]\})?\}|\{\\(?:aa|ae|ss|o)\}"
)


def encode_unicode(text: str) -> str:
    """Replace Unicode characters with LaTeX escape sequences."""
    for char, latex in _UNICODE_TO_LATEX.items():
        text = text.replace(char, latex)
    return text


def decode_latex(text: str) -> str:
    """Replace LaTeX escape sequences with Unicode characters."""
    def replace_match(m: re.Match) -> str:
        return _LATEX_TO_UNICODE.get(m.group(0), m.group(0))
    return _LATEX_PATTERN.sub(replace_match, text)


def encode_entry(entry: dict, fields: list[str] | None = None) -> dict:
    """Encode Unicode in specified fields (or all fields) of an entry."""
    result = dict(entry)
    target = fields or [k for k in entry if k not in ("ENTRYTYPE", "ID")]
    for field in target:
        if field in result and isinstance(result[field], str):
            result[field] = encode_unicode(result[field])
    return result


def decode_entry(entry: dict, fields: list[str] | None = None) -> dict:
    """Decode LaTeX escapes in specified fields (or all fields) of an entry."""
    result = dict(entry)
    target = fields or [k for k in entry if k not in ("ENTRYTYPE", "ID")]
    for field in target:
        if field in result and isinstance(result[field], str):
            result[field] = decode_latex(result[field])
    return result

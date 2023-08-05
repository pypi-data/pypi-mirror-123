"""
Entry functions for Imoji
"""

UNICODE_ESCAPE = 'unicode_escape'
UTF_8 = 'utf-8'
UNICODE_EMOJI_PREFIX = "\\U000"


def stringify(value, debug=False):
    if debug:
        print("Emoji Debug Info:", value)
        pass
    else: pass
    return value.encode(UNICODE_ESCAPE)


def get_unicode(value, debug=False):
    """Check unicode values in text and return in array."""
    try:
        value
    except TypeError:
        quit()

    unicos = []
    if isinstance(value, str):
        if debug:
            print("Imoji [DEBUG INFO]: It's just a normal string:.", value)
            return
        else:
            print("Error: No unicode emoji founded in string.")
            return
    elif isinstance(value, bytes):
        if debug:
            print("Imoji [DEBUG INFO]: Unicode founded.")
            pass
        else:
            pass
        split_list = value.decode("utf-8").split()
        for u in split_list:
            if u.startswith('\\U'):
                if debug:
                    print("Imoji [DEBUG INFO]: Unicode in text:", u)
                    pass
                else:
                    pass
                if UNICODE_EMOJI_PREFIX in u:
                    rm_prefix = u.replace(UNICODE_EMOJI_PREFIX, "")
                    unicos.append(rm_prefix)
                    return unicos

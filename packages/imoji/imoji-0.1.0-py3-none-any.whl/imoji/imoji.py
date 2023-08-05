import os
from PIL import Image
from imoji.entry import get_unicode, stringify
from imoji.emojis.reference import path

RGBA = 'RGBA'
REPO_NAME = path  # name of folder with all emoji files in png (default of library)
ERRO_MESSAGE = "No unicode found in list"


class Imoji:
    """main class of library."""

    def __init__(self, text, debug=False):
        self.encode = stringify(value=text, debug=debug)
        self.unicodelist = get_unicode(value=self.encode, debug=debug)
        self.__find = self.find(unicodelist=self.unicodelist, debug=debug)

    def find(self, unicodelist: list, debug=False):
        count = 0
        if isinstance(unicodelist, list):
            if debug:
                print("Imoji [DEBUG INFO]: Emoji list", unicodelist)
                pass
            else:
                pass
            for root, dirs, files in os.walk(REPO_NAME):
                for name in files:
                    if debug:
                        count += 1
                        print(f"Emoji/PNG FILE [{count}]:", name)
                        pass
                    else:
                        pass
                    try:
                        for u in unicodelist:
                            emoji_file = u + ".png"
                            if name == emoji_file:
                                if debug:
                                    print("Unicode returned sucessfully:", emoji_file)
                                    pass
                                else:
                                    pass
                                return emoji_file
                    except TypeError:
                        return ERRO_MESSAGE

    def drawUnicode(self, debug=False):
        img = Image.open(REPO_NAME + "/" + self.__find).convert(RGBA)
        if debug:
            print("Emoji object:", img)
            pass
        else:
            pass
        return img

    def pasteUnicode(self, emoji_im, foreground, posX, posY):
        pasted = foreground.paste(emoji_im, (posX, posY), emoji_im)
        return pasted
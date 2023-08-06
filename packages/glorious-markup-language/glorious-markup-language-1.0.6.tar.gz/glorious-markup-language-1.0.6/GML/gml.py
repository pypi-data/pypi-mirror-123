"""
Parser for texts.
"""

__copyright__ = "Copyright Florian Briksa 2021. All rights reserved."
__author__ = "Florian Briksa"
__version__ = "1.0.6"


import os
import re
import time
from typing import Tuple, List, Dict

import pygame

pygame.init()


def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("Executed function {} in {:.4f} seconds.".format(func, time.time() - start))
        return result

    return wrapper


class PARSER:
    def __init__(self, max_width=250, side_space=10, font_path=""):
        PARSER.check_fonts(font_path)
        self.p_size = 20
        self.h1_size = 30
        self.h2_size = 25
        self.h3_size = 20
        self.li_size = 20
        self.font_path = font_path
        self.linespace = 2
        self.code = list()
        self.surface = None
        self.height = 0
        self.width = 0
        self.max_width = max_width - side_space * 2
        self.font_sizes = {"normal": dict(),
                           "italic": dict(),
                           "bold": dict(),
                           "bold-italic": dict()}
        self.side_space = side_space

    # @measure_time
    def parse(self, code: list, images: Dict[str, pygame.Surface], background: pygame.Surface = None,
              width=None, height=None) -> pygame.Surface:
        """
        Draws GML-code onto a surface.        
        """
        self.width = self.width if width is None else width
        self.height = self.height if height is None else height
        self.code = code
        # self.print_structure()
        if background is not None:
            self.surface = pygame.transform.scale(background, (self.width+self.side_space*2, self.height))
        else:
            self.surface = pygame.Surface((self.width+self.side_space*2, self.height))
            self.surface.fill((255, 255, 255))
        # self.surface.set_colorkey((255, 255, 255))
        self.blit_code(images)
        return self.surface

    def init(self, text: str, images: Dict[str, pygame.Surface]) -> Tuple[List, int, int]:
        """
        Parses lines of GML code and prepares them for rendering.
        """
        self.code = list()
        self.height = 0
        self.width = 0
        start = 0
        text = text.replace("\n", "")
        while text.find("<!--") != -1:
            start = text.find("<!--")
            end = text.find("-->")
            text = text[:start] + text[end + 3:]
        text = text.replace("  ", "")
        for exp in re.finditer(r"(?<=</)\w+", text):
            innerHTML = text[start:exp.end() - len(exp.group()) - 2].replace("</" + exp.group() + ">", "").replace(
                "<" + exp.group() + ">", "")
            styles, innerHTML = self.parse_line(innerHTML, images, exp.group())
            width = self.get_width(innerHTML.replace("|", " "), styles)
            package = [(innerHTML.split(" "), styles)]
            if width > self.max_width:
                txt = innerHTML.split(" ")
                package = self.reformulate(txt, styles, self.max_width)
                width = self.max_width
            self.width = width if width > self.width else self.width
            for line, styles in package:
                self.height += styles["size"] + self.linespace
                self.code.append((exp.group(), " ".join(line), styles))
            start = exp.end() + 1
        return self.code, self.height, self.width

    # @measure_time
    def blit_code(self, images):
        y = 0
        for kind, code, style in self.code:
            self.surface = self.anzeige(self.surface, code, style, (self.side_space, y), images)
            # if style["break"] == "True":
            y += style["size"] + self.linespace

    def print_structure(self):
        inline = 0
        for kind, code, style in self.code:
            if "h" in kind:
                inline = (int(kind[-1]) - 1) * 2
            print(("".zfill(inline) + kind).replace("0", " "), ": ", code)
            if "h" in kind:
                inline = int(kind[-1]) * 2

    # @measure_time
    def parse_line(self, line: str, images, kind) -> Tuple[dict, str]:
        """
        Parses one code-line and returns all styles as dict.
        """
        styles = {"color": "black",
                  "type": "normal",
                  "image": [],
                  "size": self[kind + "_size"],
                  "tag": kind,
                  "align": "left",
                  "antialias": True,
                  "display": "standard",
                  "marked": "None",
                  "insert": [],
                  }
        boolean = line.find("<style ")
        if boolean != -1:
            line = line.replace("<style ", "")
            end = line.find("/>")
            if line[end - 1] == " ":
                end -= 1
            settings = line[:end]
            line = line[end + 3:] if line[end] == " " else line[end + 2:]
            settings = settings.replace("\"", "").replace("'", "")
            settings = settings.split(" ")
            settings = [i.split("=") for i in settings]
            try:
                for key, value in settings:
                    styles[str(key)] = str(value)
            except ValueError:
                raise SyntaxError("Wrong style setting at element %s" % settings)
            styles["size"] = int(styles["size"])
        if styles["size"] not in self.font_sizes:
            self.font_sizes[styles["type"]][styles["size"]] = pygame.font.Font(os.path.join(self.font_path, 
                                                                               PARSER.parse_font_style(styles["type"])),
                                                                               styles["size"])
        boolean = line.find("<img ")
        while boolean != -1:
            line = line.replace("<img ", "", 1)
            end = line.find("/>")
            if line[end - 1] == " ":
                end -= 1
            settings = line[boolean:end]
            start = line[:boolean]
            # e = time.time()
            width = self.get_width(start.replace("|", " ") + " ", styles)
            # print(start, "{:.4f}".format(time.time() - e))
            sp = self.get_width(" ", styles)
            end = line[end + 3:] if line[end] == " " else line[end + 2:]
            settings = settings.replace("\"", "").replace("'", "")
            settings = settings.split(" ")
            settings = [i.split("=") for i in settings]
            img = PARSER.scale(images[settings[0][1]], styles["size"] + self.linespace)
            space = int(img // sp) + 1
            fill = "".zfill(space).replace("0", "|")
            line = start + fill + end
            new_str = 1
            if kind == "li":
                new_str = -3
                for letter in line:
                    if letter != " ":
                        break
                    new_str -= 1
            styles["image"].append([str(settings[0][1]), width - sp * new_str, int(img)])
            boolean = line.find("<img ")
        if styles["tag"] == "li":
            line = "    " + line
        return styles, line

    def get_width(self, txt, style) -> int:
        img = self.font_sizes[style["type"]][style["size"]].size(txt)
        return img[0]

    def set_max_width(self, width):
        self.max_width = width

    def reset(self):
        self.p_size = 20
        self.h1_size = 30
        self.h2_size = 25
        self.h3_size = 20
        self.li_size = 20
        self.linespace = 2
        self.code = list()
        self.surface = None
        self.height = 0
        self.width = 0

    def get_max_width(self):
        return self.max_width

    def reformulate(self, elements, style, limit, begin=0) -> List[tuple, ]:
        lists = []
        active = []
        x = begin
        on = 0
        spaces = 0
        after = False
        for element in elements:
            w = self.get_width(element.replace("|", " ") + " ", style)
            if x + w + self.side_space * 2 > limit:
                sub = len([m.group() for m in re.finditer(r'((\|)\2)+', " ".join(active))])
                new_style = style.copy()
                new_style["image"] = new_style["image"][:sub]
                for img in new_style["image"]:
                    img[1] -= limit * len(lists) - on
                    if after:
                        img[1] += after * self.get_width(" ", style)
                style["image"] = style["image"][sub:]
                new_style["break"] = "True"
                lists.append((active, new_style))
                on += (limit - x)
                x = w
                if style["tag"] == "li":
                    element = "      " + element
                    h = self.get_width("      ", style)
                    for img in style["image"]:
                        img[1] += h
                    x += h
                active = [element]
                spaces = 0
            else:
                active.append(element)
                x += w
            if len(element) == 0:
                spaces += 1
            else:
                spaces = 0
        new_style = style.copy()
        for img in new_style["image"]:
            img[1] -= limit * len(lists) - on
            if after:
                img[1] += after * self.get_width(" ", new_style)
        lists.append((active, new_style))
        return lists

    def anzeige(self, bild, wort, style, pos, images) -> pygame.Surface:
        """
        Blits a text to a surface.
        """
        pos = (pos[0], pos[1] + self.linespace * 2)
        try:
            farbe = pygame.Color(style["color"])
        except ValueError:
            farbe = eval(style["color"])
            farbe = (int(farbe[0]), int(farbe[1]), int(farbe[2]), int(farbe[3]) if len(farbe) == 4 else 255)
        bildx, positionx = PARSER.txt(wort, self.font_sizes[style["type"]][style["size"]], farbe, style)
        if style["align"] == "center":
            p = (bild.get_width() // 2, pos[1] + bildx.get_height() // 2)
        elif style["align"] == "right":
            p = (bild.get_width() - bildx.get_width() // 2, pos[1] + bildx.get_height() // 2)
        else:
            p = (pos[0] + bildx.get_width() // 2, pos[1] + bildx.get_height() // 2)
        if style["marked"] != "None":
            try:
                farbe = pygame.Color(style["marked"])
            except ValueError:
                farbe = eval(style["marked"])
                farbe = (int(farbe[0]), int(farbe[1]), int(farbe[2]), int(farbe[3]) if len(farbe) == 4 else 255)
            if style["align"] == "center":
                pygame.draw.rect(bild, farbe, [p[0] - bildx.get_width() // 2, pos[1],
                                               bildx.get_width(), bildx.get_height()])
            elif style["align"] == "right":
                pygame.draw.rect(bild, farbe, [p[0] - bildx.get_width() // 2, pos[1],
                                               bildx.get_width(), bildx.get_height()])
            else:
                pygame.draw.rect(bild, farbe, [pos[0], pos[1], bildx.get_width(),
                                               bildx.get_height()])
        old = positionx
        positionx.center = p
        bild.blit(bildx, positionx)
        if style["image"]:
            for x, y, z in style["image"]:
                obj = pygame.transform.scale(images[x], (z, style["size"] + self.linespace))
                bild.blit(obj, (y + old[0] if y > 0 else old[0], -int(self.linespace // 2) + old[1]))
        return bild

    def __getitem__(self, item):
        return getattr(self, item)

    @staticmethod
    def parse_font_style(style):
        if style == "normal":
            return "normal.ttf"
        elif style == "bold":
            return "bold.ttf"
        elif style == "bold-italic":
            return "bold-italic.ttf"
        else:
            return "italic.ttf"

    @staticmethod
    def txt(text, font, farbe, style):
        if "h" in style["tag"] or style["display"] == "underline":
            font.underline = True
        bilder = font.render(str(text).replace("|", " "), bool(style["antialias"]), farbe)
        font.underline = False
        return bilder, bilder.get_rect()

    @staticmethod
    def scale(img: pygame.Surface, height: int):
        rel = img.get_width() / img.get_height()
        return height * rel

    @staticmethod
    def check_fonts(path):
        for i in ["normal.ttf", "italic.ttf", "bold-italic.ttf", "bold.ttf"]:
            if not os.path.isfile(os.path.join(path, i)):
                raise FileNotFoundError("Invalid path to font: %s. Please put a font named %s in the given directory." % (i, i))


"""
Explanation of the code

There are seven possible types of tag names:
    - h1: The biggest headline, usually sized 30px
    - h2: The second-biggest headline, usually sized 25px
    - h3: The smallest headline, usually sized 20px
    - p: The standard text tag
    - li: Tag name for enumerations
    - img: Tag name to implement images
    - style: Tag name to modify text content

Allowed style-parameters:
    - type: Sets the displayed text to italic, normal, bold or bold-italic.
    - color: Sets the color of the displayed text. The color can either be a name
             or a tuple, optionally with an alpha value.
    - align: Sets the align of the displayed text to left, right or center
    - size: Sets the size of the displayed text in pixels
    - antialias: Sets the antialiasing property of the text
    - display: Displays the text either 'underline' or 'standard'
    - marked: Marks the text with the specified color

NOTE: To display gaps with more than three spaces you should use the character '|'.
      Else it is possible that the algorithm interprets that gap as gap for an image
      and parses it the wrong way.


Example 1:
<h1><style type='bold' />Centre</h1>" \
<p>Wild <img src='m32' /> is the first food resource in Glorious City. It is the first need of the 
    people and forms with <img src='m31' /> stone and <img src='m30' /> timber the first set of 
    essential resources of the game.</p><p>The three most important resources: <img src='m30' />
    timber, <img src='m31' /> stone and <img src='m32' /> wild.
</p>
<h2>Earnings</h2>
<li><style color='0,155,0' type='italic' />  + 10t <img src='m32' /> Wild & <img src='m31' /> Stone</li>
<h2>Costs</h2>
<li><style color='255,0,0' type='italic' />  - 10t <img src='m30' /> Timber </li>
<li><style color='255,0,0' type='italic' />  - 10t <img src='m31' /> Stone </li>

--------------------------------

<h1>Hello!</h1>
<h2>Hello!</h2>
<h3>Hello!</h3>
<p></p>
<li>- That's an enumeration </li>
<li>- And that's an enumeration on multiple lines</li>
<li>(- Also with an image: <img src='m32' /> )</li>
<p></p>
<h1><style size='20' type='bold' color=(204,51,0) />The main Feature:</h1>
<p>Images <img src='m30' /> between <img src='m31' /> text.</p>
<p>Also <img src='m32' /> images between <img src='m33' /> multiple lines as <img src='m34' /> 
    you can see here.
</p>
<p><style color=(204,51,0) />Of course <img src='m33' /> all style-attributes are also
    <img src='m32' /> available in normal text on <img src='m31' /> multiple lines.</p>
    By the way, it doesn't matter if there's a space before an image
    <img src='m30' />, after an image<img src='m31' /> , at both sides <img src='m32' /> or without
    any spaces<img src='m33' />. Play with them and enjoy.
</p>
"""

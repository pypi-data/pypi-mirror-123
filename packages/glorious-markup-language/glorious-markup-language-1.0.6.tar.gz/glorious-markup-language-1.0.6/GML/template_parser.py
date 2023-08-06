"""
Module for parsing GML-templates into dynamic valid GML-code.
"""


__copyright__ = "Copyright Florian Briksa 2021. All rights reserved."
__author__ = "Florian Briksa"
__version__ = "1.0.6"


from typing import List, Optional


class TEMPLATE_PARSER:
    """
    Class for parsing GML-templates into dynamic valid GML-code.
    """
    def __init__(self, mp):
        """
        Class for parsing GML-templates into dynamic valid GML-code.
        """
        self.dict = mp

    def parse(self, text):
        """
        Parses a given text into valid GML-code.
        """
        try:
            text = self.parse_comments(text)
            text = self.parse_if(text)
            text = self.parse_loop(text)
            text = self.parse_line(text)
        except KeyError as e:
            raise KeyError("Missing key in self.dict: %s" % e)
        while text.find(" ") == 0:
            text = text[1:]
        while text.find("\n") == 0:
            text = text[1:]
        return text

    def parse_line(self, line: str, values: Optional[List] = None):
        boolean = line.find("{{")
        index = 0
        while boolean != -1:
            end = line.find("}}")
            if values is None:
                content = line[boolean+3:end-1]
                line = line.replace("{{ " + content + " }}", str(self.dict[content]), 1)
            else:
                content = line[boolean+3:end-1]
                line = line.replace("{{ " + content + " }}", str(values[index]), 1)
                index += 1
            boolean = line.find("{{")
        return line

    def parse_loop(self, text: str):
        """
        Parse all loops found in text.
        """
        boolean = text.find("{|")
        while boolean != -1:
            end = text.find("|}")
            loop_declaration = text[boolean+3:end-1]
            loop_key = eval(loop_declaration.replace("for ", ""))
            text = text.replace(text[boolean:end+3], "", 1)
            endfor = text.find("{|")
            line = text[boolean:endfor]
            txt = ""
            for value in self.dict[loop_key]:
                row = self.parse_line(line, value)
                while row[0] == " ":
                    row = row[1:]
                txt += row
            s_index = text.find(line)
            e_index = text.find("{| endfor |}") + 13
            text = text[:s_index] + txt + text[e_index:]
            boolean = text.find("{|")
        return text

    def parse_if(self, text: str):
        boolean = text.find("{-")
        while boolean != -1:
            end = text.find("-}")
            condition = eval(text[boolean+6:end])
            endif = text.find("{- endif -}")
            if not self.dict[condition]:
                text = text[:boolean] + text[endif:]
            else:
                text = text[:boolean] + text[end+3:]
            text = text.replace("{- endif -}", "", 1)
            boolean = text.find("{-")
        return text

    @staticmethod
    def parse_comments(text):
        boolean = text.find("<!--")
        while boolean != -1:
            text = text[:boolean]+text[text.find("-->")+3:]
            boolean = text.find("<!--")
        return text

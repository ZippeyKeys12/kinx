from collections import OrderedDict
from json import load as load_json
from os.path import join as path_join
from subprocess import call
from typing import Dict, Tuple, Union

from frontmatter import load as load_fm
from jinja2 import Environment, FileSystemLoader
from lxml import etree
from lxml.html import HTMLParser
from mistune import Markdown

from .lexer import BlockLexer, InlineLexer
from .renderer import Renderer


class Builder:
    head_split = "<[$]>"

    def __init__(self, path: str, dev: bool):
        self.path = path
        self.dev = dev

        kinxfile = load_fm(self.__get_path("Kinxfile"))

        self.markdown = Markdown(
            renderer=Renderer(escape=False, hard_wrap=True),
            inline=InlineLexer,
            block=BlockLexer,
        )

        try:
            jinja_extensions = kinxfile["extensions"]["jinja"]
        except:
            jinja_extensions = ()
        try:
            self.env = Environment(
                extensions=jinja_extensions,
                loader=FileSystemLoader(self.__get_path(kinxfile["root"])),
            )
        except:
            print("Unexpected error: 'root' key not found in Kinxfile")
            raise
        del jinja_extensions

        project_dir = {}

        current_header = ()
        for i in etree.fromstring(self.markdown(kinxfile.content), HTMLParser())[0]:
            if i.tag == "ul":
                if current_header in project_dir:
                    project_dir[current_header].extend(self.__get_links_md(i))
                else:
                    project_dir[current_header] = self.__get_links_md(i)
            elif i.tag[:1] == "h" and i.tag[1:] in (str(j) for j in range(1, 7)):
                current_header = (i.text, i.tag[1:])
            else:
                project_dir[current_header].append(i.tag)
                if i.tag not in ["hr"]:
                    print("{} is not read in Kinxfile".format(etree.tostring(i)))
        del current_header

        self.kinxfile = {}
        for i in ["title", "author", "description", "url", "copyright", "theme"]:
            self.kinxfile[i] = kinxfile[i]
        del kinxfile

        self.kinxfile["content"] = OrderedDict(project_dir)
        del project_dir

        print(self.kinxfile)

    def __get_links_md(self, element):
        sets = []

        for i in element:
            tags = []

            for k in i:
                if k.tag == "ul":
                    n = self.__get_links_md(k)

                    if len(n) > 1:
                        tags.append(n)
                    else:
                        tags.extend(n)
                else:
                    tags.append((k.text, k.get("href")))
            sets.append(tags)

        return sets

    def __get_path(self, path_to: str) -> str:
        return path_join(self.path, path_to)

    def build(self):
        pass

        # if dev:
        #     call("yarn", "start")
        # else:
        #     call("yarn", "build")

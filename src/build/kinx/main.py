"""Site Builder
"""
from os.path import join as path_join
from typing import Dict, List, Tuple, Union

from frontmatter import load as load_fm
from jinja2 import Environment, FileSystemLoader
from lxml import etree
from lxml.etree import Element
from lxml.html import HTMLParser
from mistune import Markdown

from .lexer import BlockLexer, InlineLexer
from .renderer import Renderer


class Builder:
    DEFAULT_HEADER = ('DEFAULT', 1)

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
            try:
                jinja_extensions = kinxfile["extensions"]["jinja"]
            except KeyError:
                jinja_extensions = ()
            self.env = Environment(
                extensions=jinja_extensions,
                autoescape=True,
                loader=FileSystemLoader(self.__get_path(kinxfile["root"])),
            )
            del jinja_extensions
        except KeyError:
            print("Unexpected error: 'root' key not found in Kinxfile")
            raise

        project_dir: dict = {}

        self.headers: List[Union[Tuple[str, int], str]] = [self.DEFAULT_HEADER]
        for i in etree.fromstring(self.markdown(
                kinxfile.content), HTMLParser())[0]:
            if i.tag == "ul":
                project_dir[self.headers[-1]].extend(self.__get_links_md(i))
            elif (i.tag[:1] == "h" and i.tag[1:] in
                  (str(j) for j in range(1, 7))):
                self.headers.append((i.text, i.tag[1:]))
                project_dir[self.headers[-1]] = []
            else:
                project_dir[self.headers[-1]].append(i.tag)
                if i.tag not in ["hr"]:
                    print(
                        "{} is not read in Kinxfile".format(
                            etree.tostring(i)))

        self.kx: dict = {}
        for i in ["title", "author", "description",
                  "url", "copyright", "theme"]:
            self.kx[i] = kinxfile[i]
        del kinxfile

        self.kx["content"] = (project_dir)
        del project_dir

        print(self.kx)

        self.pages: Dict[str, str] = {}

    def __get_links_md(self, element: Element) -> List[Tuple[str, str]]:
        s_type = Tuple[str, str]
        sets: List[s_type] = []

        for i in element:
            tags: list = []

            for k in i:
                n: Union[s_type, List[s_type]]
                if k.tag == "ul":
                    n = self.__get_links_md(k)
                else:
                    n = (k.text, k.get("href"))

                tags.append(n)

            sets.extend(tags)

        return sets

    def __get_path(self, path_to: str) -> str:
        return path_join(self.path, path_to)

    def build(self):
        kxc = self.kx["content"]
        for i in kxc:
            for j in kxc[i]:
                if not isinstance(j, list):
                    continue
                link = j[0][1]
                self.pages[link] = self.__render_page(link)
                for k in j[1:]:
                    self.pages[k[0]] = self.__render_page(k[1])

        # if dev:
        #     call("yarn", "start")
        # else:
        #     call("yarn", "build")

    def __render_page(self, path):
        return self.markdown(self.env.get_template(path).render(
            {j: self.kx[j] for j in self.kx if j not in ["content"]}))

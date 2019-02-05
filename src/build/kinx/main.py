"""Site Builder
"""
from os.path import join as path_join

from frontmatter import load as load_fm
from jinja2 import Environment, FileSystemLoader
from lxml import etree
from lxml.html import HTMLParser
from mistune import Markdown

from .lexer import BlockLexer, InlineLexer
from .renderer import Renderer


class Builder:
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

        current_header: list = []
        for i in etree.fromstring(self.markdown(
                kinxfile.content), HTMLParser())[0]:
            if i.tag == "ul":
                project_dir[current_header[-1]].extend(self.__get_links_md(i))
            elif (i.tag[:1] == "h" and i.tag[1:] in
                  (str(j) for j in range(1, 7))):
                current_header.append((i.text, i.tag[1:]))
                project_dir[current_header[-1]] = []
            else:
                project_dir[current_header[-1]].append(i.tag)
                if i.tag not in ["hr"]:
                    print(
                        "{} is not read in Kinxfile".format(
                            etree.tostring(i)))
        del current_header

        self.kx: dict = {}
        for i in ["title", "author", "description",
                  "url", "copyright", "theme"]:
            self.kx[i] = kinxfile[i]
        del kinxfile

        self.kx["content"] = (project_dir)
        del project_dir

        print(self.kx)

        self.pages: dict = {}

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
        kxc = self.kx["content"]
        for i in kxc:
            for j in kxc[i]:
                if not isinstance(j, list):
                    continue
                link = j[0][1]
                self.pages[link] = self.__render_page(link)
                for k in j[1:]:
                    for l in k:
                        link = l[1]
                        self.pages[link] = self.__render_page(link)

        print(self.pages)

        # if dev:
        #     call("yarn", "start")
        # else:
        #     call("yarn", "build")

    def __render_page(self, path):
        return self.markdown(self.env.get_template(path).render(
            {j: self.kx[j] for j in self.kx if j not in ["content"]}))

from jinja2 import Environment, FileSystemLoader
import os

class ProjectElement:
    def __init__(self, type, name, belong_to, ref):
        self.type = type
        self.name = name
        self.belong_to = belong_to
        self.ref = ref


class Generator:
    init_out_path = ""
    elements = list()

    def __init__(self):
        self.j2_env = Environment(
            loader=FileSystemLoader("res"),
            trim_blocks=True
        )

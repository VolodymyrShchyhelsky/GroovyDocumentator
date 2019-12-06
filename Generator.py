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

    def __init__(self, output=None):
        if output:
            self.output = os.path.normpath(output)
        self.j2_env = Environment(
            loader=FileSystemLoader("res"),
            trim_blocks=True
        )

    def append_class_element(self, element, class_name):
        element.id = 1 + len(Generator.elements)
        pr_elem = ProjectElement(element.__class__.__name__, element.name,
                                 " class: " + class_name,
                                 self.output + "/" + class_name + ".html#" + str(element.id))
        Generator.elements.append(pr_elem)
    
    def append_subclass(self, element, class_name):
        pr_elem = ProjectElement(element.__class__.__name__, element.name,
                                 " class: " + class_name,
                                 self.output + "/classes/" + element.name + ".html")
        Generator.elements.append(pr_elem)

    def append_file_element(self, element, file_name, file_path):
        element.id = 1 + len(Generator.elements)
        pr_elem = ProjectElement(element.__class__.__name__, element.name,
                                 file_path,
                                 self.output + "/" + file_name + ".html#" + str(element.id))
        Generator.elements.append(pr_elem)

    def append_file_class(self, element, file_path):
        pr_elem = ProjectElement(element.__class__.__name__, element.name,
                                 file_path,
                                 self.output + "/classes/" + element.name + ".html")
        Generator.elements.append(pr_elem)
from Generator import *
import os
from FileParser import *


class ClassDocGenerator(Generator):
    def __init__(self, output, class_in, is_enum=False):
        super(ClassDocGenerator, self).__init__(output)
        self.is_enum = is_enum
        self.class_in = class_in

    def generate_structure(self):
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        if self.is_enum:
            template = self.j2_env.get_template("enum_t.html")
        else:
            template = self.j2_env.get_template("class_t.html")
        result = template.render({"obj": self.class_in,
                                  "out": Generator.init_out_path})
        with open(self.output + "/" + self.class_in.name + ".html", "w") as file:
            file.write(result)

    def generate_classes(self):
        if not os.path.exists(self.output + "/classes"):
            os.makedirs(self.output + "/classes")
        for class_in in self.class_in.classes:
            gen = ClassDocGenerator(self.output + "/classes", class_in)
            gen.generate()
        for class_in in self.class_in.enums:
            gen = ClassDocGenerator(self.output + "/classes", class_in, True)
            gen.generate()

    def generate(self):
        self.gen_alphabet()
        self.generate_structure()
        self.generate_classes()

    def gen_alphabet(self):
        for elem in self.class_in.classes:
            self.append_subclass(elem, self.class_in.name)
        for elem in self.class_in.enums:
            self.append_subclass(elem, self.class_in.name)
        for elem in self.class_in.methods:
            self.append_class_element(elem, self.class_in.name)
        for elem in self.class_in.constructors:
            self.append_class_element(elem, self.class_in.name)
        for elem in self.class_in.fields:
            self.append_class_element(elem, self.class_in.name)
        for elem in self.class_in.closures:
            self.append_class_element(elem, self.class_in.name)

from Generator import *
from FileParser import *


class AlphabetGenerator(Generator):
    def __init__(self):
        super(AlphabetGenerator, self).__init__()
        self.generate()

    def generate(self):
        for obj in Generator.elements:
            obj.ref = os.path.abspath(obj.ref)
        Generator.elements.sort(key=lambda x: x.name.lower())
        Generator.elements.sort(key=lambda x: x.type.lower())
        self.elements = list()
        previous_type = ""
        for element in Generator.elements:
            if previous_type != element.type:
                previous_type = element.type
                self.elements.append((element.type, list([element])))
            else:
                self.elements[-1][1].append(element)

        index_html = self.j2_env.get_template("alphabet.html").render({
            "obj": self.elements,
            "out": Generator.init_out_path
        })
        with open(Generator.init_out_path + "/alphabet.html", "w") as f:
            f.write(index_html)

from ClassDocGenerator import *


class DocumentGenerator(Generator):
    def __init__(self, output=None, file_path=None):
        super(DocumentGenerator, self).__init__(output)
        self.file_path = os.path.normpath(file_path)
        self.file = None
        self.generate()

    def generate(self):
        try:
            with open(self.file_path, 'r') as file:
                txt = file.read()
            txt += '\n'
            self.file = File(txt, os.path.basename(self.file_path))
            self.file.parse()
            self.gen_alphabet()
            full_path_len = len(os.path.abspath(self.output) + self.file.name)
            if full_path_len < 250:
                self.generate_file()
                self.generate_classes()
        except Exception as error:
            print(error, self.output)

    def generate_file(self):
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        template = self.j2_env.get_template("file_t.html")
        result = template.render({"obj": self.file,
                                  "out": Generator.init_out_path})
        with open(self.output + "/" + self.file.name + ".html", "w") as file:
            file.write(result)

    def generate_classes(self):
        if not os.path.exists(self.output + "/classes"):
            os.makedirs(self.output + "/classes")
        for class_in in self.file.classes:
            gen = ClassDocGenerator(self.output + "/classes", class_in)
            gen.generate()
        for class_in in self.file.enums:
            gen = ClassDocGenerator(self.output + "/classes", class_in, True)
            gen.generate()

    def gen_alphabet(self):
        for elem in self.file.classes:
            self.append_file_class(elem, self.file_path)
        for elem in self.file.enums:
            self.append_file_class(elem, self.file_path)
        for elem in self.file.methods:
            self.append_file_element(elem, self.file.name, self.file_path)
        for elem in self.file.closures:
            self.append_file_element(elem, self.file.name, self.file_path)

import glob
import os
from FileDocGenerator import *


class CatalogDocGenerator(Generator):
    def __init__(self, output=None, path=None, is_catalog_generation=False):
        super(CatalogDocGenerator, self).__init__()
        self.output_path = os.path.normpath(output)
        self.path = os.path.normpath(path)
        self.files = list()
        self.file_names = list()
        self.directories = list()
        self.dir_names = list()
        self.is_catalog_generation = is_catalog_generation
        self.description = "There is no .md files"
        if os.path.isdir(self.path):
            self.generate()

    def generate_files(self):
        self.files = sorted(glob.glob(self.path + "/*.groovy"))
        self.file_names = [os.path.basename(x) for x in self.files]
        for file in self.files:
            if not os.path.exists(self.output_path + "/files/" + os.path.basename(file)):
                os.makedirs(self.output_path + "/files/" + os.path.basename(file))
            output_path_dir = self.output_path + "/files/" + os.path.basename(file)
            DocumentGenerator(output_path_dir, file)

    def generate_dir(self):
        content = list(map(lambda x: os.path.join(self.path, x), os.listdir(self.path)))
        self.directories = list(filter(lambda x: os.path.isdir(x), content))
        self.dir_names = [os.path.basename(x) for x in self.directories]
        for module_path in self.directories:
            output_path_dir = self.output_path + "/" + os.path.basename(module_path)
            # mainly in groovy used framework's for testing with completely different syntax (example:  Spock Primer)
            if os.path.basename(module_path) not in ["test", "TEST", "Test"]:
                CatalogDocGenerator(output_path_dir, module_path)

    def get_description(self):
        md_files = glob.glob(self.path + "/*.md")
        if len(md_files) > 0:
            with open(md_files[0], 'r') as file:
                self.description = file.read()
        self.description = self.description.replace("\n", "<br>")

    def generate(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        self.get_description()
        if not self.is_catalog_generation:
            self.generate_dir()
        self.generate_files()
        index_html = self.j2_env.get_template("catalog_t.html").render({
            "description": self.description,
            "catalogs": self.dir_names,
            "files": self.file_names,
            "name": os.path.basename(self.path),
            "out": Generator.init_out_path
        })
        with open(self.output_path + "/" + os.path.basename(self.path) + ".html", "w") as f:
            f.write(index_html)

import ProjectInfo
import datetime
from AlphabetGenerator import *


class MainGenerator(Generator):
    def __init__(self, name):
        super(MainGenerator, self).__init__()
        self.name = name
        self.generate()

    def generate(self):
        index_html = self.j2_env.get_template("main.html").render({
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "out": Generator.init_out_path,
            "name": self.name,
            "version": ProjectInfo.version
        })
        with open(Generator.init_out_path + "/main.html", "w") as f:
            f.write(index_html)

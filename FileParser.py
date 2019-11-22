import re
from Keywords import *
from string import ascii_letters, digits


class Object:
    def __init__(self, name, declaration=None, documentation=""):
        self.id = 0
        self.name = name
        self.declaration = declaration
        if documentation == "":
            self.documentation = "Empty documentation"
        else:
            self.documentation = documentation
            self.documentation = self.documentation.replace(" *", '<br>')
            self.documentation = self.documentation[3:-2]


class Method(Object):
    def __init__(self, name, declaration, documentation):
        super().__init__(name, declaration, documentation)
        self.annotations = list()
        self.qualifiers = list()
        self.generic = None

    def concat(self):
        for elem in self.annotations:
            self.declaration = elem + "\n" + self.declaration
        for elem in self.qualifiers:
            self.declaration = elem + " " + self.declaration
        self.annotations.clear()
        self.qualifiers.clear()


class Field(Object):
    def __init__(self, name, declaration, documentation):
        super().__init__(name, declaration, documentation)
        self.qualifiers = list()

    def concat(self):
        for an in self.qualifiers:
            self.declaration = an + " " + self.declaration
        self.qualifiers.clear()


class Class(Object):
    def __init__(self, body, name, declaration, documentation):
        super().__init__(name, declaration, documentation)
        self.body = body
        self.classes = list()
        self.methods = list()
        self.fields = list()
        self.constructors = list()
        self.annotations = list()
        self.qualifiers = list()
        self.enums = list()

    def parse(self):
        parser = Parser(self.body, self.name)
        parser.parse()
        self.methods = parser.methods
        self.fields = parser.fields
        self.classes = parser.classes
        self.constructors = parser.constructors
        self.enums = parser.enums


class Enum(Class):
    def __init__(self, body, name, declaration, documentation):
        super().__init__(body, name, declaration, documentation)
        self.enumeration = list()

    def parse(self):
        parser = Parser(self.body, self.name)
        parser.parse_enum()
        self.enumeration = parser.enumeration
        super().parse()


class File(Object):
    def __init__(self, body, name):
        super().__init__(name)
        self.body = body
        self.imports = list()
        self.classes = list()
        self.enums = list()
        self.fields = list()
        self.methods = list()

    def parse(self):
        parser = Parser(self.body)
        self.body = self.body.lstrip()
        if self.body.startswith("/**"):
            parser.parse_documentation_comment()
            self.documentation = parser.last_comment
            parser.last_comment = ""
            self.documentation = self.documentation.replace(" *", '<br>')
            self.documentation = self.documentation[3:-2]
        parser.parse()
        self.imports = parser.imports
        self.classes = parser.classes
        self.enums = parser.enums
        self.fields = parser.fields
        self.methods = parser.methods


def is_valid_name(lexeme) -> bool:
    lexeme = lexeme.strip()
    if not len(lexeme):
        return False
    is_valid_start = re.match("[a-zA-Z_~]", lexeme[0])
    is_valid_body = all([re.match("[a-zA-Z0-9_]", x) for x in lexeme[1:]])
    is_keyword = lexeme in KEYWORDS
    return bool(is_valid_start and is_valid_body and not is_keyword)


class Parser:
    def __init__(self, text, class_name=None):
        self.text = text
        self.last_comment = ""
        self.imports = list()
        self.classes = list()
        self.annotations = list()
        self.qualifiers = list()
        self.generic = list
        self.methods = list()
        self.fields = list()
        self.constructors = list()
        self.enums = list()
        self.enumeration = list()
        self.class_name = class_name

    def parse_generic(self):
        self.generic = self.get_block('<', '>')
        self.text = self.text[len(self.generic) + 1:]

    def read_line(self) -> str:
        line_sep = self.text.find('\n')
        line = self.text[:line_sep]
        self.text = self.text[line_sep + 1:]
        return line

    def read_word(self) -> str:
        self.text = self.text.lstrip()
        tmp_text = self.text.lstrip(ascii_letters + '_' + digits)
        word_len = max(len(self.text) - len(tmp_text), 1)
        word = self.text[:word_len]
        self.text = self.text[word_len:]
        self.text = self.text.lstrip()
        return word

    def get_block(self, start_sign, finish_sign) -> str:
        start = self.text.find(start_sign)
        it = start
        level = 1
        while level != 0:
            it += 1
            if self.text[it] == start_sign:
                level += 1
            if self.text[it] == finish_sign:
                level -= 1
        return_val = self.text[start: it + 1]
        self.text = self.text[it + 1:]
        return return_val

    def parse_documentation_comment(self):
        self.last_comment = ""
        end_of_comment = self.text.find('*/')
        self.last_comment = self.text[:end_of_comment + len('*/')]
        self.text = self.text[len(self.last_comment):]
        if self.text.startswith('\n'):
            self.text = self.text[1:]

    def parse_enum(self):
        flag = True
        while flag:
            if self.text.startswith("/**"):
                self.parse_documentation_comment()
            name = self.read_word()
            value = ""
            if self.text.startswith("("):
                value = self.get_block('(', ')')
                self.text = self.text.lstrip()
            self.enumeration.append(name + value)
            if self.text.startswith(","):
                self.text = self.text[1:]
            else:
                flag = False

    def parse_class(self):
        start = self.text.find("{")
        declaration = self.text[:start]
        documentation = self.last_comment
        self.last_comment = ""
        type = self.text.split()[0]
        name = self.text.split()[1]
        class_body = self.get_block('{', '}')
        if type == "enum":
            new_class = Enum(class_body[1:-1], name, declaration, documentation)
        else:
            new_class = Class(class_body[1:-1], name, declaration, documentation)
        new_class.annotations = self.annotations
        self.annotations.clear()
        new_class.qualifiers = self.qualifiers
        new_class.parse()
        if type == "enum":
            self.enums.append(new_class)
        else:
            self.classes.append(new_class)

    def parse_object(self):
        is_method = False
        object_type = self.read_word()
        if not is_valid_name(object_type):
            return
        if object_type == self.class_name:
            object_name = object_type
            object_type = ""
        else:
            object_name = self.read_word()
            if not is_valid_name(object_name):
                return
        object_parameters = ""
        if self.text.startswith("("):
            object_parameters = self.get_block('(', ')')
            self.text = self.text.lstrip()
            if self.text.startswith("{") or self.text.startswith("throws"):
                object_parameters = object_parameters + self.text[: self.text.find('{')]
                self.get_block('{', '}')
                is_method = True
        declaration = object_type + " " + object_name + object_parameters
        if is_method:
            method = Method(object_name, declaration, self.last_comment)
            self.last_comment = ""
            method.annotations = self.annotations
            self.annotations.clear()
            method.qualifiers = self.qualifiers
            method.generic = self.generic
            method.concat()
            # print("Method ", method.declaration)
            if object_name == self.class_name:
                self.constructors.append(method)
            else:
                self.methods.append(method)
        else:
            field = Field(object_name, declaration, self.last_comment)
            field.qualifiers = self.qualifiers
            field.concat()
            self.fields.append(field)

    def parse(self):
        while len(self.text) > 1:
            self.text = self.text.lstrip()
            if self.text.startswith("/**"):
                self.parse_documentation_comment()
                continue

            if self.text.startswith("//"):
                self.read_line()
                continue

            if self.text.startswith("import") or self.text.startswith("package"):
                self.imports.append(self.read_line())
                continue

            if (self.text.startswith("class ") or
                    self.text.startswith("interface ") or
                    self.text.startswith("trait ") or
                    self.text.startswith("enum ")):
                self.parse_class()
                continue

            if self.text.startswith("@"):
                self.annotations.append(self.read_line())
                continue

            if (self.text.startswith("private ") or
                    self.text.startswith("public ") or
                    self.text.startswith("protected ") or
                    self.text.startswith("abstract ") or
                    self.text.startswith("static ") or
                    self.text.startswith("final ")):
                self.qualifiers.append(self.read_word())
                continue

            if self.text.startswith("<"):
                self.parse_generic()
                continue

            self.parse_object()


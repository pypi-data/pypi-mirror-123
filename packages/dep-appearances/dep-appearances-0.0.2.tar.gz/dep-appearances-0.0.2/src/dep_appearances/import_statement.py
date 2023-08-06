import re

class ImportStatement:
    IMPORT_REGEX = re.compile(r'^\s*import\s+(\w+)|^\s*from\s+(\w+)(\.\w+)*\s+import')

    @classmethod
    def test(cls, source_code):
        return cls.IMPORT_REGEX.match(source_code)

    def __init__(self, source_file, source_code, line_number):
        self.source_file = source_file
        self.source_code = source_code
        self.line_number = line_number

    def package_name(self):
        match = self.IMPORT_REGEX.match(self.source_code)

        if match is None:
            return None

        return match.group(1) or match.group(2)

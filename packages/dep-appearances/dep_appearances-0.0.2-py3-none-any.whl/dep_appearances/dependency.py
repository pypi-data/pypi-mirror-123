class Dependency:
    def __init__(self, name):
        self.name = name
        self.import_statements = []

    def imported_by(self, import_statement):
        if import_statement.package_name() is self.name:
            return True

        if import_statement.package_name().replace("_", "-") == self.name:
            return True

        return False

    def add_import_statement(self, import_statement):
        self.import_statements.append(import_statement)

    def unused(self):
        return len(self.import_statements) == 0

    def underused(self, usage_threshold):
        return len(self.import_statements) <= usage_threshold and not self.unused()

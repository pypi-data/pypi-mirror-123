import os
import pdb
import pipfile

from dep_appearances.dependency import Dependency
from dep_appearances.import_statement import ImportStatement

class AppearancesReport:
    def __init__(self, project_root):
        self.project_root = os.path.abspath(project_root)
        self.dependencies = []

    def compile(self):
        self.dependencies = self._dependencies_with_imports()
        return self

    def unused_dependencies(self):
        unused_deps = [dep for dep in self.dependencies if dep.unused()]
        return sorted(unused_deps, key=lambda dep: dep.name)

    def underused_dependencies(self, usage_threshold):
        deps = [dep for dep in self.dependencies if dep.underused(usage_threshold=usage_threshold)]
        return sorted(deps, key=lambda dep: dep.name)

    def _dependencies_with_imports(self):
        dependencies = self._extract_dependencies()
        import_statements = self._extract_import_statements()

        for dep in dependencies:
            for import_statement in import_statements:
                if dep.imported_by(import_statement):
                    dep.add_import_statement(import_statement)

        return dependencies

    def _extract_dependencies(self):
        dependencies = []
        pfile = pipfile.load(os.path.join(self.project_root, "Pipfile"))

        for package in pfile.data["default"].keys():
            dependencies.append(package)

        for package in pfile.data["develop"].keys():
            dependencies.append(package)

        return [Dependency(dependency) for dependency in dependencies]

    def _extract_import_statements(self):
        import_statements = []

        for root, _dirs, files in os.walk(self.project_root):
            if root.startswith(os.path.abspath(f"{self.project_root}/.venv")):
                continue

            for file in files:
                if os.path.splitext(file)[1].lower() == ".py":
                    import_statements += self._extract_imports_from_py(os.path.join(root, file))

        return import_statements

    def _extract_imports_from_py(self, file):
        imports = []

        with open(file) as f:
            line_number = 0

            for line in f:
                line_number += 1

                if ImportStatement.test(line):
                    import_statement = ImportStatement(
                        source_file=file,
                        source_code=line,
                        line_number=line_number
                    )

                    imports.append(import_statement)

        return imports

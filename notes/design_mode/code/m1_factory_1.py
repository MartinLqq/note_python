class Python:
    def print(self):
        return 'print()'

class Java:
    def print(self):
        return 'System.out.printIn()'

class Php:
    def print(self):
        return 'printf()'


class LanguageFactory:

    options = {
        'python': Python,
        'java': Java,
        'php': Php,
    }

    def create(self, language: str):
        cls = self.options.get(language)
        return cls() if cls else None


if __name__ == '__main__':
    fac = LanguageFactory()
    python = fac.create('python')
    print(python.print())

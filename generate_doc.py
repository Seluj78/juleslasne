from website import application
from flask_apidoc.commands import GenerateApiDoc
from flask_script import Manager

manager = Manager(application)
manager.add_command('apidoc', GenerateApiDoc(output_path='docs'))

if __name__ == "__main__":
    manager.run()

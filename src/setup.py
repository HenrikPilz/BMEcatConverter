from distutils.core import setup

setup(name='BMEcatConverter',
      description='This is a converter, which applies for two tasks:\n\t- converting BMEcats into Excel-Sheets' +
                  '\n\t- converting Excel-Sheets of certain form (Mapping-Master) into BMEcat Version 1.2',
      version='1.2',
      author='Henrik Pilz',
      author_email='henrik.pilz@contorion.de',
      packages=[ 'datamodel', 'exporter', 'importer', 'mapping', 'test', 'resolver', 'transformer' ],
      package_dir={'' : 'src'},
      requires=['lxml', 'regex', 'openpyxl', 'coverage(==4.3)'],
      py_modules=['main', 'converter', 'argumentParser', 'test_main'],
      data_files={'documents' : 'documents'}
      )

from distutils.core import setup
import os.path


setup(
  name = 'group7',         # How you named your package folder (MyLib)
  packages = ['group7'],   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Function Myvat',   # Give a short description about your library
  long_description='Demo Library',
  author = 'agem0008',                   # Type in your name
  author_email = '6314120008@mutacth.com',      # Type in your E-Mail
  keywords = ['group7', 'Myvat', 'vat', 'NECS1201'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)

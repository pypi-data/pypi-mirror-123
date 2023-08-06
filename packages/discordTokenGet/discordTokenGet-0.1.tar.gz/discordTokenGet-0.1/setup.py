from distutils.core import setup
setup(
  name = 'discordTokenGet',         # How you named your package folder (MyLib)
  packages = ['discordTokenGet'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='GNU AGPLv3',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Discord Token Grabbing Module',   # Give a short description about your library
  author = 'NNoGalaxy',                   # Type in your name
  author_email = 'galaxynn666@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/NNoGalaxy/discordTokenGet',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/NNoGalaxy/discordTokenGet/archive/refs/tags/v0.1.tar.gz',    # I explain this later on
  keywords = ['discord', 'token', 'module'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU Affero General Public License v3',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)
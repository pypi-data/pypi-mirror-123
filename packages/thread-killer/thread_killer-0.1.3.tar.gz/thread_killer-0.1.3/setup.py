from distutils.core import setup
setup(
  name = 'thread_killer',         # How you named your package folder (MyLib)
  packages = ['thread_killer'],   # Chose the same as "name"
  version = '0.1.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Thread killer - library for managing zombie threads',   # Give a short description about your library
  author = 'Aydar Gabdrahmanov',                   # Type in your name
  author_email = 'smith@fixmost.com',      # Type in your E-Mail
  url = 'https://bitbucket.fixmost.com/projects/PAYS/repos/thread-killer/',   # Provide either the link to your github or to your website
  download_url = 'https://bitbucket.fixmost.com/projects/PAYS/repos/thread-killer/browse?at=refs%2Ftags%2F0.1.2',    # I explain this later on
  keywords = ['Thread', 'Thread-killer'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)
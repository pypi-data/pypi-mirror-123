from distutils.core import setup
setup(
  name = 'AnimeChanQuotes',         # How you named your package folder (MyLib)
  packages = ['AnimeChanQuotes'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='GNU',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Wraps the api calls for https://animechan.vercel.app/ into an easy use function.',   # Give a short description about your library
  author = 'Chelsea Piccirilli',                   # Type in your name
  author_email = 'piccirilli115@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/cpiccirilli1/anime-quote-wrapper',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/cpiccirilli1/AnimeChanQuotes/archive/refs/tags/v_01.tar.gz',    # I explain this later on
  keywords = ['Wrapper', 'Anime', 'api', 'quotes'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',

  ],
)
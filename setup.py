from distutils.core import setup
setup(
  name = 'aiok',         # How you named your package folder (MyLib)
  packages = ['aiok'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'async vkbot module',   # Give a short description about your library
  author = '14iq',
  author_email = 'belicoff0505@gmail.com',
  url = 'https://github.com/14iq/aiok',
  download_url = 'https://github.com/14iq/aiok/archive/v_01.tar.gz',
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],
  install_requires=[
        'aiohttp',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.7',
  ],
)
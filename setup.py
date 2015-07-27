from distutils.core import setup, Command

setup(name='dryscrape',
      version='1.0',
      description='a lightweight Javascript-aware, headless web scraping library for Python',
      author='Niklas Baumstark',
      author_email='niklas.baumstark@gmail.com',
      license='MIT',
      url='https://github.com/niklasb/dryscrape',
      packages=['dryscrape', 'dryscrape.driver'],
      install_requires=['webkit_server', 'lxml', 'xvfbwrapper'],
      )

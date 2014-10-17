from distutils.core import setup, Command

setup(name='dryscrape',
      version='0.9.1',
      description='a lightweight Javascript-aware, headless web scraping library for Python',
      author='Niklas Baumstark',
      author_email='niklas.baumstark@gmail.com',
      license='MIT',
      url='https://niklasb.github.com/dryscrape',
      packages=['dryscrape', 'dryscrape.driver'],
      requires=['webkit_server', 'lxml'],
      )

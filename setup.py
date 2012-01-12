from distutils.core import setup, Command

setup(name='pyscrape',
      version='0.8',
      description='a lightweight Javascript-aware, headless web scraping library for Python',
      author='Niklas Baumstark',
      author_email='niklas.baumstark@gmail.com',
      license='MIT',
      url='https://niklasb.github.com/pyscrape',
      packages=['pyscrape', 'pyscrape.driver'],
      requires=['webkit_server', 'lxml'],
      )

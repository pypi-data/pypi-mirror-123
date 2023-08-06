from setuptools import setup

setup(name='crypto_stocks',
      version='0.1.4',
      description='Get current price of crypto from most popular stock exchanges',
      packages=['crypto_stocks'],
      author_email='1mgavura@gmail.com',
      long_description = 'README.md',
      long_description_content_type = 'text/markdown',
      install_requires=[            # I get to this in a second
          'requests',
      ],
      url = 'https://github.com/mishagavura',
      zip_safe=False)

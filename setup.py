from setuptools import setup

setup(
      name='recpy',
      version='0.1',
      description="RecPy is an API wrapper built in Python for pulling data from RecNet.",
      url='https://github.com/RecNetBot-Development/RecPy/',
      license='MIT',
      packages=['src'],
      install_requires=[
            "aiohttp==3.8.0"
      ]
)
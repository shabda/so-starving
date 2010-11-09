VERSION = '0.0.1'

from setuptools import setup, find_packages

setup(
      name = 'so_starving',
      version = VERSION,
      author = 'Vincent Rialland',
      author_email = 'vincent.rialland@gmail.com',
      description = 'The "I am so starving example with the Nagare framework (http://agiliq.com/blog/2010/11/i-am-so-starving-same-web-app-in-various-python-we/)',
      license = '',
      keywords = '',
      url = '',
      packages = find_packages(),
      include_package_data = True,
      package_data = {'' : ['*.cfg']},
      zip_safe = False,
      install_requires = ('nagare', 'simplejson', 'werkzeug'),
      entry_points = """
      [nagare.applications]
      so_starving = so_starving.app:app
      """
     )

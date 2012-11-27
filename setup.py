from setuptools import find_packages, setup

version='0.1'

setup(name='WikiCookieAuth',
      version=version,
      description="Share cookies between MediaWiki and trac.",
      author='Christoph Schindler',
      author_email='hop@30hopsmax.at',
      maintainer='Christoph Schindler',
      maintainer_email='hop@30hopsmax.at',
      url='https://github.com/Metalab/WikiCookieAuthTracPlugin',
      keywords='trac plugin',
      license="GPL",
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests*']),
      include_package_data=True,
      package_data={ 'wikicookieauth': ['templates/*', 'htdocs/*'] },
      zip_safe=False,
      entry_points = """
      [trac.plugins]
      wikicookieauth = wikicookieauth
      """,
      )


from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='islay.auth',
      version=version,
      description="An unobtrusive authentication framework for WSGI stacks.",
      long_description=open(os.path.join('src', 'islay', 'auth', 'README.txt')).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Matthew Wilkes',
      author_email='wilkes@jarn.com',
      url='',
      license='',
      package_dir = {'':'src'},
      packages=find_packages('src', exclude=['ez_setup']),
      namespace_packages=['islay'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'distribute',
          'WebOb',
          'zope.interface',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
            [paste.filter_factory]
            auth = islay.auth.auth:AuthFactory
      """,
      )

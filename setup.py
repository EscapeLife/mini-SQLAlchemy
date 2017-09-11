from distutils.core import setup

setup(name='m',
      version='0.1.0',
      packages=['mini-orm', 'mini-orm.security', 'mini-orm.extensions', 'mini-orm.extensions.sqlalchemy'],
      install_requires=[
          'WebOb>=1.6.1',
          'sqlalchemy>=1.0.0',
          'pyhocon>=0.3.0',
      ],
      author="Escape",
      author_email="wenpanhappy@126.com",
      description="This is a very mini SQLAlchemy",
      license="Apache-2",
      )

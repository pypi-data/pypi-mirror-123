#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['fastapi_users',
 'fastapi_users.authentication',
 'fastapi_users.db',
 'fastapi_users.router']

package_data = \
{'': ['*']}

install_requires = \
['fastapi >=0.65.2,<0.71.0',
 'passlib[bcrypt] ==1.7.4',
 'email-validator >=1.1.0,<1.2',
 'pyjwt ==2.2.0',
 'python-multipart ==0.0.5',
 'makefun >=1.9.2,<1.13']

extras_require = \
{'mongodb': ['fastapi-users-db-mongodb >=1.0.0'],
 'oauth': ['httpx-oauth >=0.3,<0.4'],
 'ormar': ['fastapi-users-db-ormar >=1.0.0'],
 'sqlalchemy': ['fastapi-users-db-sqlalchemy >=1.0.0'],
 'tortoise-orm': ['fastapi-users-db-tortoise >=1.0.0']}

setup(name='fastapi-users',
      version='8.1.1',
      description='Ready-to-use and customizable users management for FastAPI.',
      author='François Voron',
      author_email='fvoron@gmail.com',
      url='https://github.com/fastapi-users/fastapi-users',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
      python_requires='>=3.7',
     )

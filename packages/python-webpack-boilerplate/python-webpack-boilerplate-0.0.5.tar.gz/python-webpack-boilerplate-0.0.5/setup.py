# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webpack_boilerplate',
 'webpack_boilerplate.contrib',
 'webpack_boilerplate.management',
 'webpack_boilerplate.management.commands',
 'webpack_boilerplate.templatetags']

package_data = \
{'': ['*'],
 'webpack_boilerplate': ['frontend_template/*',
                         'frontend_template/{{cookiecutter.project_slug}}/*',
                         'frontend_template/{{cookiecutter.project_slug}}/src/application/*',
                         'frontend_template/{{cookiecutter.project_slug}}/src/components/*',
                         'frontend_template/{{cookiecutter.project_slug}}/src/styles/*',
                         'frontend_template/{{cookiecutter.project_slug}}/vendors/*',
                         'frontend_template/{{cookiecutter.project_slug}}/vendors/images/*',
                         'frontend_template/{{cookiecutter.project_slug}}/webpack/*']}

install_requires = \
['cookiecutter>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'python-webpack-boilerplate',
    'version': '0.0.5',
    'description': 'Jump start frontend project bundled by Webpack',
    'long_description': '# README\n\n[![Build Status](https://github.com/AccordBox/python-webpack-boilerplate/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/AccordBox/python-webpack-boilerplate/actions/workflows/ci.yml)\n[![PyPI version](https://badge.fury.io/py/python-webpack-boilerplate.svg)](https://badge.fury.io/py/python-webpack-boilerplate)\n[![Documentation](https://img.shields.io/badge/Documentation-link-green.svg)](https://python-webpack-boilerplate.rtfd.io/)\n\n## Goal\n\n**Jump start frontend project bundled by Webpack with Django, Flask quickly**\n\n## What is included.\n\n1. A `frontend project template` which has good structure, easy to use and customize. You can create the frontend project with just **ONE** command, and use it even you have no idea how to config Webpack.\n1. Custom template tags which can help load Webpack bundle file in the templates transparently.\n\n## Features\n\n- **Supports Django and Flask** (will support more framework in the future)\n- Automatic multiple entry points\n- Automatic code splitting\n- Hot Module Replacement (HMR) (auto reload web page if you edit JS or SCSS)\n- Easy to config and customize\n- ES6 Support via [babel](https://babeljs.io/) (v7)\n- JavaScript Linting via [eslint](https://eslint.org/)\n- SCSS Support via [sass-loader](https://github.com/jtangelder/sass-loader)\n- Autoprefixing of browserspecific CSS rules via [postcss](https://postcss.org/) and [postcss-preset-env](https://github.com/csstools/postcss-preset-env)\n- Style Linting via [stylelint](https://stylelint.io/)\n\n## Optional support\n\n*Need install extra packages*\n\n- React\n- Vue\n\n## Documentation\n\n1. [Setup With Django](https://python-webpack-boilerplate.readthedocs.io/en/latest/setup_with_django/)\n1. [Setup With Flask](https://python-webpack-boilerplate.readthedocs.io/en/latest/setup_with_flask/)\n1. [Frontend Workflow](https://python-webpack-boilerplate.readthedocs.io/en/latest/frontend/)\n1. [Tailwind CSS](https://python-webpack-boilerplate.readthedocs.io/en/latest/setup_with_tailwind/)\n1. [Import React](https://python-webpack-boilerplate.readthedocs.io/en/latest/react/)\n1. [Import Vue](https://python-webpack-boilerplate.readthedocs.io/en/latest/vue/)\n\n## If you want to know more about Webpack and Django\n\n1. [Setup Webpack Project with Django](http://www.accordbox.com/blog/setup-webpack-project-django)\n1. [Load Webpack bundles in Django](http://www.accordbox.com/blog/load-webpack-bundles-django)\n1. [Linting in Webpack](http://www.accordbox.com/blog/code-linting-webpack)\n1. [Load Webpack hash bundle in Django](http://www.accordbox.com/blog/load-webpack-hash-bundle-django)\n1. [Code splitting with Webpack](http://www.accordbox.com/blog/code-splitting-webpack)\n1. [How to config HMR with Webpack and Django](http://www.accordbox.com/blog/how-config-hmr-webpack-and-django)\n\n## Special Thanks\n\n* [django-webpack-loader](https://github.com/owais/django-webpack-loader)\n* [rails/webpacker](https://github.com/rails/webpacker)\n* [wbkd/webpack-starter](https://github.com/wbkd/webpack-starter)\n',
    'author': 'Michael Yin',
    'author_email': 'michaelyin@accordbox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AccordBox/python-webpack-boilerplate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

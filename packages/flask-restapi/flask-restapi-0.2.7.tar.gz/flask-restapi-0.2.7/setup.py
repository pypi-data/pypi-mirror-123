# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_restapi', 'flask_restapi.spec']

package_data = \
{'': ['*'], 'flask_restapi': ['templates/*']}

install_requires = \
['Flask[async]>=2.0.1,<3.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'flask-restapi',
    'version': '0.2.7',
    'description': 'Flask-RESTAPI is an extension for validate and make OpenAPI docs.',
    'long_description': '# Flask-RESTAPI\n\n[![license](https://img.shields.io/github/license/jonarsli/flask-restapi.svg)](https://github.com/jonarsli/flask-restapi/blob/master/LICENSE)\n[![pypi](https://img.shields.io/pypi/v/flask-restapi.svg)](https://pypi.python.org/pypi/flask-restapi)\n\n\n[Flask-RESTAPI document](https://jonarsli.github.io/flask-restapi/)\n\nFlask-RESTAPI is an extension for Flask that is a database-agnostic framework library for creating REST APIs. It is a lightweight abstraction that works with your existing ORM/libraries.\n\nIt use pydantic to validate and serialize data. OpenAPI document can be automatically generated through the python decorator and it supports swagger ui display.\n\nPydantic are used to validate and serialize parameters. For details, please refer to the [pydantic documentation](https://pydantic-docs.helpmanual.io/).\n\n## Installation\n```bash\npip install flask-restapi\n```\n\n## Example\n```python\nfrom flask import Flask\nfrom flask.views import MethodView\nfrom pydantic import BaseModel\n\nfrom flask_restapi import Api, RequestParametersType\n\napp = Flask(__name__)\napi = Api(app)\n\n\nclass UserGetSpec(BaseModel):\n    name: str\n\n\nclass UserResponseSpec(BaseModel):\n    id: int\n    name: str\n\n\nclass User(MethodView):\n    @api.query(UserGetSpec)\n    @api.response(UserResponseSpec)\n    def get(self, parameters: RequestParametersType):\n        """Get a user name and id"""\n        user_name = parameters.query.name\n        return UserResponseSpec(id=1, name=user_name)\n\n\napp.add_url_rule("/user", view_func=User.as_view("user"))\n\n```\n\n## Swagger API docs\nNow go to http://localhost:5000/docs\n![](docs/images/example.png)',
    'author': 'jonars',
    'author_email': 'jonarsli13@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JonarsLi/flask-restapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataconf']

package_data = \
{'': ['*']}

install_requires = \
['pyhocon>=0.3.54,<0.4.0', 'python-dateutil>=2.8.1,<3.0.0']

entry_points = \
{'console_scripts': ['dataconf = dataconf.cli:run']}

setup_kwargs = {
    'name': 'dataconf',
    'version': '0.3.0',
    'description': 'Lightweight configuration with automatic dataclasses parsing (HOCON/JSON/YAML/PROPERTIES)',
    'long_description': '# Dataconf\n\n[![Actions Status](https://github.com/zifeo/dataconf/workflows/CI/badge.svg)](https://github.com/zifeo/dataconf/actions)\n[![PyPI version](https://badge.fury.io/py/dataconf.svg)](https://badge.fury.io/py/dataconf)\n\nLightweight configuration with automatic dataclasses parsing (hocon/json/yaml/properties files).\n\n## Getting started\n\nRequires at least Python 3.8.\n\n```bash\n# pypi\npip install dataconf\npoetry add dataconf\n\n# master\npip install --upgrade git+https://github.com/zifeo/dataconf.git\npoetry add git+https://github.com/zifeo/dataconf.git\n\n# dev\npoetry install\npre-commit install\n```\n\n## Usage\n\n```python\nfrom dataclasses import dataclass, field\nfrom typing import List, Dict, Text, Union\nfrom dateutil.relativedelta import relativedelta\nimport dataconf\n\nconf = """\nstr_name = test\nstr_name = ${?HOSTNAME}\ndash-to-underscore = true\nfloat_num = 2.2\n# this is a comment\nlist_data = [\n    a\n    b\n]\nnested {\n    a = test\n}\nnested_list = [\n    {\n        a = test1\n    }\n]\nduration = 2s\nunion = 1\n"""\n\n@dataclass\nclass Nested:\n    a: Text\n\n@dataclass\nclass Config:\n    str_name: Text\n    dash_to_underscore: bool\n    float_num: float\n    list_data: List[Text]\n    nested: Nested\n    nested_list: List[Nested]\n    duration: relativedelta\n    union: Union[Text, int]\n    default: Text = \'hello\'\n    default_factory: Dict[Text, Text] = field(default_factory=dict)\n\nprint(dataconf.loads(conf, Config))\n# Config(str_name=\'/users/root\', dash_to_underscore=True, float_num=2.2, list_data=[\'a\', \'b\'], nested=Nested(a=\'test\'), nested_list=[Nested(a=\'test1\')], duration=relativedelta(seconds=+2), union=1, default=\'hello\', default_factory={})\n\n# Replicating pureconfig Scala sealed trait case class behavior\n# https://pureconfig.github.io/docs/overriding-behavior-for-sealed-families.html\nclass InputType:\n    """\n    Abstract base class\n    """\n    pass\n    \n    \n@dataclass(init=True, repr=True)\nclass StringImpl(InputType):\n    name: Text\n    age: Text\n\n    def test_method(self):\n        print(f"{self.name} is {self.age} years old.")\n\n        \n@dataclass(init=True, repr=True)\nclass IntImpl(InputType):\n    area_code: int\n    phone_num: Text\n\n    def test_method(self):\n        print(f"The area code for {self.phone_num} is {str(self.area_code)}")\n\n        \n@dataclass\nclass Base:\n    location: Text\n    input_source: InputType\n\nstr_conf = """\n{\n    location: Europe\n    input_source {\n        name: Thailand\n        age: "12"\n    }\n}\n"""\n\nconf = dataconf.loads(str_conf, Base)\n```\n\n```python\nimport dataconf\n\nconf = dataconf.string(\'{ name: Test }\', Config)\nconf = dataconf.env(\'PREFIX_\', Config)\nconf = dataconf.url(\'https://github.com/zifeo/dataconf/blob/master/.pre-commit-config.yaml\', Config)\nconf = dataconf.file(\'confs/test.{hocon,json,yaml,properties}\', Config)\n\nconf = dataconf.loads(\'confs/test.hocon\', Config)\nconf = dataconf.loads(\'confs/test.json\', Config)\nconf = dataconf.loads(\'confs/test.yaml\', Config)\nconf = dataconf.loads(\'confs/test.properties\', Config)\n\ndataconf.dumps(\'confs/test.hocon\', out=\'hocon\')\ndataconf.dumps(\'confs/test.json\', out=\'json\')\ndataconf.dumps(\'confs/test.yaml\', out=\'yaml\')\ndataconf.dumps(\'confs/test.properties\', out=\'properties\')\n```\n\nFollows same api as python JSON package (e.g. `load`, `loads`, `dump`, `dumps`). \nFor full HOCON capabilities see [here](https://github.com/chimpler/pyhocon/#example-of-hocon-file).\n\n## Env dict/list parsing\n\n```\nPREFIX_VAR=a\nPREFIX_VAR_NAME=b\nPREFIX_TEST__NAME=c\nPREFIX_LS_0=d\nPREFIX_LS_1=e\nPREFIX_LSLS_0_0=f\nPREFIX_LSOB_0__NAME=g\nPREFIX_NESTED="{ name: Test }"\nPREFIX_SUB="{ value: ${PREFIX_VAR} }"\n```\n\nis equivalent to\n\n```\n{\n    var = a\n    var_name = b\n    test {\n        name = c\n    }\n    ls = [\n        d\n        e\n    ]\n    lsls = [\n        [\n            f\n        ]\n    ]\n    lsob = [\n        {\n            name = g\n        }\n    ]\n    nested {\n        name: Test\n    }\n    sub {\n        # will have value "a" at parsing, useful for aliases\n        value = ${PREFIX_VAR}\n    }\n}\n```\n\n## CI\n\n```shell\ndataconf -c confs/test.hocon -m tests.configs -d TestConf -o hocon\n# dataconf.exceptions.TypeConfigException: expected type <class \'datetime.timedelta\'> at .duration, got <class \'int\'>\n```\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zifeo/dataconf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

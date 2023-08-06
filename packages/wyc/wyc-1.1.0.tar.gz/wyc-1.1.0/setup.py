# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['wyc']
install_requires = \
['pscript>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'wyc',
    'version': '1.1.0',
    'description': 'Create WebComponent (Custom Element) from a python file',
    'long_description': '# wyc\nCreate a Web Component (a Custom Element) from a python file (transpile python code to javascript (es2015)).\n\n[![Test](https://github.com/manatlan/wyc/actions/workflows/tests.yml/badge.svg)](https://github.com/manatlan/wyc/actions/workflows/tests.yml)\n\n## Features\n\n * Use python to define your custom element (the important one ;-))\n * Use @react decorator to auto declare js methods (avoid `observedAttributes` and `attributeChangedCallback`)\n * can generate multiple custom elements from a single python file\n * auto register component\'s names in the page, based on classnames (_customElements.define("my-component", MyComponent)_)\n * include javascript code (in module _docstring_)\n * generate es2015 javascript, for a maximum of compatibilities\n * 100% unittest coverage\n * should work with py2 too\n\n## Changelog\n\n    [see changelog](changelog.md)\n\n## Install\n\n**wyc** is on [pypi](https://pypi.org/project/wyc/) :\n\n```pip install wyc```\n\n## Usecase\n\nOn server side ... just declare a http endpoint (`/generate/<py_file>`), get the content of the `<py_file>` and just `return wyc.build(content)`.\n\nSo, your python file is automatically transpiled to JS, and directly usable in your html page, by adding a `<script src=\'/generate/file.py\' ></script>`.\n\nIf your component class is named "MyComponent" (in `file.py`), it will be usable as `<my-component ...> ... </my-component>`\n\n## Documentation\n\nA minimal python custom element could be:\n\n```python\nclass HelloWorld(HTMLElement):\n    """<div>Hello World</div>"""\n```\n\nWhen it\'s linked in your html page, you can start to use `<hello-world/>`.\n\nYour class must inherit from `HTMLElement`, so you will have access to *shadow dom* thru `self.shadowRoot`. And your class will work exactly like `HTMLElement` in js side, so there are special methods which are usable nativly:\n\n * `def connectedCallback(self)`: Invoked each time the custom element is appended into a document-connected element. This will happen each time the node is moved, and may happen before the element\'s contents have been fully parsed.\n * `def disconnectedCallback(self)`: Invoked each time the custom element is disconnected from the document\'s DOM.\n * `def adoptedCallback(self)`: Invoked each time the custom element is moved to a new document.\n\nthe others methods (`observedAttributes` and `attributeChangedCallback`) should not be used, because **wyc** generate them automatically depending on the usage of the `@react()` decorator.\n\n### Declare react\'s attributes\nBy using the `@react(*attributes)`, you can declare method which will be invoked when an attribute change.\n\n```python\nclass HelloWorld(HTMLElement):\n    """<div>Hello World</div>"""\n\n    @react("nb")\n    def method(self):\n        ...\n```\n\nWhen "nb" attribute change, the method is invoked ... simple!\n\n### Initialize things at constructor phase\nYour component can use an `init(self)` instance method, to initialize things at constructor phase.\n\n```python\nclass HelloWorld(HTMLElement):\n    """<div>Hello World</div>"""\n    def init(self):\n        self.root = self.shadowRoot.querySelector("div")\n```\n\n### Declare js code in py component\nSometimes you\'ll need to use external js, you can declare them in module docstrings.\n\n```python\n"""\nvar myExternalJs=function() { ... }\n"""\n\nclass HelloWorld(HTMLElement):\n    """<div>Hello World</div>"""\n\n    def a_method(self):\n        myExternalJs()\n```\n\n### Demos and examples\n\nSee [examples](examples/), for real examples and more tips ...\n\n## History\nAt the beginning, I\'ve built the same kind of things for [brython](https://brython.info/) ... but it was not a good idea, because brython would have been mandatory to use them.\n\nBased on my experience with [vbuild](https://github.com/manatlan/vbuild), I had made a POC with the marvelous [pscript](https://pscript.readthedocs.io/en/latest/)... And the POC comes to a real life module, which is pretty usable, in production too.\n\nThus, **wyc** components are usable in html/js, brython, angular, vuejs, react, svelte ...etc... it\'s the power of standards.\n\n\n',
    'author': 'manatlan',
    'author_email': 'manatlan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/manatlan/wyc',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)

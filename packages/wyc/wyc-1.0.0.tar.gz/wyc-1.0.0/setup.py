# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['wyc']
install_requires = \
['pscript>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'wyc',
    'version': '1.0.0',
    'description': 'Create WebCompoent (Custom Element) from a python file',
    'long_description': '# wyc\nCreate a Web Component (a Custom Element) from a python file (transpile python code to javascript (es2015)).\n\n## features\n\n * Use python to define your custom element (the important one ;-))\n * Use @react decorator to auto declare js methods (avoid `observedAttributes` and `attributeChangedCallback`)\n * can generate multiple custom elements from a single python file\n * auto register component\'s names in the page, based on classnames (_customElements.define("my-component", MyComponent)_)\n * include javascript code (in module _docstring_)\n * generate es2015 javascript, for a maximum of compatibilities\n * 100% unittest coverage\n * should work with py2 too\n\n## install\n\n```pip install wyc```\n\n## usecase\n\nOn server side ... just declare a http endpoint (`/generate/<py_file>`), get the content of the `<py_file>` and just `return wyc.build(content)`.\n\nSo, your python file is automatically transpiled to JS, and directly usable in your html page, by adding a `<script src=\'/generate/file.py\' ></script>`.\n\nIf your component class is named "MyComponent", it will be usable as `<my-component ...> ... </my-component>`\n\n## documentation\n\nA minimal python custom element could be:\n\n```python\nclass HelloWorld(HTMLElement):\n    """<div>Hello World</div>"""\n    pass\n```\n\nWhen it\'s linked in your html page, you can start to use `<hello-world/>`.\n\nYour class must inherit from `HTMLElement`, so you will have access to *shadow dom* thru `self.shadowRoot`. And your class will work exactly like `HTMLElement` in js side.\n\n\n### Initialize things at constructor phase\nYour component can use an `init(self)` instance method, to initialize things in the constructor phase.\n\n```python\nclass HelloWorld(HTMLElement):\n    """<div>Hello World</div>"""\n    def init(self):\n        self.root = self.shadowRoot.querySelector("div")\n```\n\n### Declare react\'s attributes\nBy using the `@react(*attributes)`, you can declare method which will be called when an attribute change (no need to use the `observedAttributes` and `attributeChangedCallback`)\n\n```python\nclass HelloWorld(HTMLElement):\n    """<div>Hello World</div>"""\n\n    @react("nb")\n    def method(self):\n        ...\n```\n\nWhen attribute "nb" change, the method is called ... simple!\n\n### Declare js code in py component\nSometimes you\'ll need to use external js, you can declare them in module docstrings.\n\n```python\n"""\nvar myExternalJs=function() { ... }\n"""\n\nclass HelloWorld(HTMLElement):\n    """<div>Hello World</div>"""\n\n    def a_method(self):\n        myExternalJs()\n```\n\nsee [examples](examples/), for real examples and more tips ...\n\n## history\nAt the beginning, I wanted to build the same kind of things for [brython](https://brython.info/) ... but it was not a good idea, because brython would have been mandatory to use them.\n\nBased on my experience with [vbuild](https://github.com/manatlan/vbuild), I had made a POC ... And the POC comes to a real life module, which is pretty usable, in production too.\n\nLike that, *wyc* components are usable in html/js, brython, angular, react, svelte ...etc... it\'s the power of standards.\n\n\n',
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

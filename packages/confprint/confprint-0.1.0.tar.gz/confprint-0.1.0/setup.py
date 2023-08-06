# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confprint']

package_data = \
{'': ['*']}

install_requires = \
['click==7.1.2']

entry_points = \
{'console_scripts': ['vinc = vinc:cli']}

setup_kwargs = {
    'name': 'confprint',
    'version': '0.1.0',
    'description': 'Python printer configurations.',
    'long_description': '<!-- \n![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)\n\n\n# Data Science Template\n\n**Data Science Template** is a template repository for data science projects.\n## Badges\n\nAdd badges from somewhere like: [shields.io](https://shields.io/)\n\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)\n[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)\n[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)\n\n\n## Features\n\n- Light/dark mode toggle\n- Live previews\n- Fullscreen mode\n- Cross platform\n\n\n## Tech Stack\n\n**Client:** React, Redux, TailwindCSS\n\n**Server:** Node, Express\n\n\n## Demo\n\nInsert gif or link to demo\n\n\n## Screenshots\n\n![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)\n\n\n## Installation\n\nInstall my-project with pip\n\n```bash\n  pip install my-project\n  cd my-project\n```\n\n## Environment Variables\n\nTo run this project, you will need to add the following environment variables to your .env file\n\n`API_KEY`\n\n`ANOTHER_API_KEY`\n\n\n## Deployment\n\nTo deploy this project run\n\n```bash\n  npm run deploy\n```\n\n  \n## Run Locally\n\nClone the project\n\n```bash\n  git clone https://link-to-project\n```\n\nGo to the project directory\n\n```bash\n  cd my-project\n```\n\nInstall dependencies\n\n```bash\n  poetry install\n```\n\nStart the server\n\n```bash\n  flask run\n```\n\n\n## Usage/Examples\n\n```python\nfrom automata.fa.dfa import DFA\n\nfrom visual_automata.fa.dfa import VisualDFA\n\ndfa = VisualDFA(\n    states={"q0", "q1", "q2", "q3", "q4"},\n    input_symbols={"0", "1"},\n    transitions={\n        "q0": {"0": "q3", "1": "q1"},\n        "q1": {"0": "q3", "1": "q2"},\n        "q2": {"0": "q3", "1": "q2"},\n        "q3": {"0": "q4", "1": "q1"},\n        "q4": {"0": "q4", "1": "q1"},\n    },\n    initial_state="q0",\n    final_states={"q2", "q4"},\n)\n```\n\n\n## Running Tests\n\nTo run tests, run the following command\n\n```bash\n  pytest -vs\n```\n\n\n## API Reference\n\n#### Get all items\n\n```http\n  GET /api/items\n```\n\n| Parameter | Type     | Description                |\n| :-------- | :------- | :------------------------- |\n| `api_key` | `string` | **Required**. Your API key |\n\n#### Get item\n\n```http\n  GET /api/items/${id}\n```\n\n| Parameter | Type     | Description                       |\n| :-------- | :------- | :-------------------------------- |\n| `id`      | `string` | **Required**. Id of item to fetch |\n\n#### add(num1, num2)\n\nTakes two numbers and returns the sum.\n\n  ## Color Reference\n\n| Color         | Hex                                                              |\n| ------------- | ---------------------------------------------------------------- |\n| Example Color | ![#0a192f](https://via.placeholder.com/10/0a192f?text=+) #0a192f |\n| Example Color | ![#f8f8f8](https://via.placeholder.com/10/f8f8f8?text=+) #f8f8f8 |\n| Example Color | ![#00b48a](https://via.placeholder.com/10/00b48a?text=+) #00b48a |\n| Example Color | ![#00d1a0](https://via.placeholder.com/10/00b48a?text=+) #00d1a0 |\n\n\n## Documentation\n\n[Documentation](https://linktodocumentation)\n\n\n## Appendix\n\nAny additional information goes here\n\n\n## Optimizations\n\nWhat optimizations did you make in your code? E.g. refactors, performance improvements, accessibility\n\n\n## Roadmap\n\n- Additional browser support\n\n- Add more integrations\n\n\n## Related\n\nHere are some related projects\n\n[Awesome README](https://github.com/matiassingers/awesome-readme)\n\n\n## Lessons Learned\n\nWhat did you learn while building this project? What challenges did you face and how did you overcome them?\n\n\n## FAQ\n\n#### Question 1\n\nAnswer 1\n\n#### Question 2\n\nAnswer 2\n\n\n## Feedback\n\nIf you have any feedback, please reach out to us at fake@fake.com\n\n\n## Support\n\nFor support, email fake@fake.com or join our Slack channel.\n\n\n## Used By\n\nThis project is used by the following companies:\n\n- Company 1\n- Company 2\n\n\n## Authors\n\n- [@lewiuberg](https://www.github.com/lewiuberg)\n\n\n## Acknowledgements\n\n - [Data Science Simplified](https://mathdatasimplified.com) for all her amazing tips.\n - [The realpython community](https://realpython.com/community/) for all their great feedback and help.\n - [readme.so](https://readme.so/editor) for helping in making amazing readme\'s.\n\n## Contributing\n\nContributions are always welcome!\n\nSee `contributing.md` for ways to get started.\n\nPlease adhere to this project\'s `code of conduct`.\n\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n -->\n\n # In development\n',
    'author': 'Lewi Lie Uberg',
    'author_email': 'lewi@uberg.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lewiuberg/confprint',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

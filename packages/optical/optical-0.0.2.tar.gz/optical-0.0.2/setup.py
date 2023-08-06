# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['optical', 'optical.converter', 'optical.visualizer']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'altair>=4.1.0,<5.0.0',
 'bounding-box>=0.1.3,<0.2.0',
 'imagesize>=1.2.0,<2.0.0',
 'joblib>=1.0.1,<2.0.0',
 'lxml>=4.6.3,<5.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'mediapy>=0.2.2,<0.3.0',
 'pandas>=1.2.3,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'scikit-multilearn>=0.2.0,<0.3.0',
 'tqdm>=4.59.0,<5.0.0']

extras_require = \
{'docs': ['Sphinx>=3.5.3,<4.0.0',
          'sphinx-panels>=0.5.2,<0.6.0',
          'sphinx-rtd-theme>=0.5.1,<0.6.0'],
 'tensorflow': ['tensorflow-cpu>=2.4.1,<3.0.0']}

setup_kwargs = {
    'name': 'optical',
    'version': '0.0.2',
    'description': 'Utilities for vision related tasks',
    'long_description': '<div align="center">\n\n# Optical\n![ci build](https://github.com/hashtagml/optical/actions/workflows/build.yaml/badge.svg)\n[![codecov](https://codecov.io/gh/hashtagml/optical/branch/main/graph/badge.svg?token=EC26I5HFQH)](https://codecov.io/gh/hashtagml/optical)\n![Python Version](https://img.shields.io/pypi/pyversions/optical)\n[![Documentation Status](https://readthedocs.org/projects/optical/badge/?version=latest)](https://optical.readthedocs.io/en/latest/?badge=latest)\n![GitHub all releases](https://img.shields.io/github/downloads/hashtagml/optical/total)\n![PyPI - License](https://img.shields.io/pypi/l/optical)\n[![PyPI version](https://badge.fury.io/py/optical.svg)](https://badge.fury.io/py/optical)\n<!-- [![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat)](#contributors-) -->\n\n<p align="center"><img align="centre" src="assets/optical_b.png" alt="logo" width = "650"></p>\n\nA collection of utilities for ML vision related tasks.\n\n</div>\n\n## What is optical?\n\nObject detection is one of the mainstream computer vision tasks. However, when it comes to training an object detection model, there is a variety of formats that one has to deal with for different models e.g. `COCO`, `PASCAL VOC`, `Yolo` and so on. `optical` provides a simple interface to convert back and forth between these annotation formats and also perform a bunch of exploratory data analysis (EDA) on these datasets regardless of their source format.\n\n:star2: At present we support the following formats:\n- [COCO](https://cocodataset.org/#format-data)\n- [PASCAL VOC](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html#data)\n- [Yolo](https://github.com/AlexeyAB/darknet)\n- [TFrecord](https://www.tensorflow.org/tutorials/load_data/tfrecord)\n- [SageMaker Manifest](https://docs.aws.amazon.com/sagemaker/latest/dg/augmented-manifest.html)\n- CSV\n\n\n## Installation\n\n`optical` could be installed from `pip`:\n\n```sh\npip install optical\n```\n\nFor conversion to (or from) `TFrecord`, please install the `tensorflow` extra:\n```sh\npip install `optical[tensorflow]`\n```\n\nfor visualisation of images in [mediapy](https://github.com/google/mediapy) format, you need to have [ffmpeg](https://ffmpeg.org/download.html) installed in your system.\n\n\n## Getting Started\n\n### declare the imports\n```python\nfrom optical import Annotation\n```\n\n### read the annotations\n```python\nannotation = Annotation(root = "/path/to/dataset", format="coco")\n```\n\noptical expects the data to be organised in either of the following layouts:\n\n```sh\nroot\n├── images\n│ ├── train\n│ ├── val\n│ └── test\n└── annotations\n  ├── train.json\n  ├── val.json\n  └── test.json\n```\n\nNote that for annotation formats which require individual annotations for each images (e.g., `PASCAL VOC` or `Yolo`), \nthe `annotations` directory should also contain the same sub-directories as in `images`. The splits that do not have an annotation will be ignored.\n\nIf your data does not have a split to begin with, that\'s acceptable too. In that case the directory layout should be like below:\n\n```sh\nroot\n├── images\n│ ├── 1.jpg\n│ ├── 2.jpg\n│ ├── ...\n│ │\n│ └── 100.jpg\n│\n└── annotations\n  └── label.json\n```\n\nTha name of the annotation file is not important in this case. But, if your format requires individual formats, the annotation files must have the identical name with that of the image.\n\n### EDA\n#### Check data distribution\n\n```python\n>>> annotation.describe()\n\n| split | images | annotations | categories |\n| ----- | ------ | ----------- | ---------- |\n| train | 729    | 1121        | 3          |\n| valid | 250    | 322         | 3          |\n\n```\n#### Plot label distribution\n\n```python\n>>> annotation.show_distribition()\n```\n<p align="left"><img align="centre" src="assets/show_dist.png" alt="logo" width = "300"></p>\n\n\n#### Scatter bounding box width and height\n\n```python\n>>> annotation.bbox_scatter()\n```\n<p align="left"><img align="centre" src="assets/bbox_scatter.png" alt="logo" width = "500"></p>\n\n### Visualize images\n```python\n>>> vis = annotation.visualizer(img_size=256)\n>>> vis.show_batch()\n```\n\n<p align="left"><img align="centre" src="assets/vis_batch.png" alt="logo" width = "500"></p>\n\n### Split the data if required\n```python\n>>> splits = annotation.train_test_split(test_size = 0.2, stratified = True)\n>>> splits.save("/path/to/output/dir")\n```\n\n#### Export to other formats\n```python\n>>> annotation.export(to = "yolo")\n```\n\n## Contributing\n\n### Work in local environment:\n\n1. Fork the repo\n2. install poetry:\n    ```sh\n    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n    ```\n\n3. work on virtual environment:\n   ```sh\n   conda create -n optical python=3.8 pip\n   ```\n\n4. install the dependencies and the project in editable mode\n   ```sh\n   poetry install\n   ```\n5. Make your changes as required. Please use appropriate use of docstrings (we follow [Google style docstring](https://google.github.io/styleguide/pyguide.html)) and try to keep your code clean.\n\n6. Raise a pull request.\n\n### Work inside the dev container:\nIf you are a Visual Studio Code user, you may choose to develop inside a container. The benefit is the container comes with all necessary settings and dependencies configured. You will need [Docker](https://www.docker.com/) installed in your system. You also need to have the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension enabled.\n\n1. Open the project in Visual Studio Code. in the status bar, select open in remote container.\n\nIt will perhaps take a few minutes the first time you build the container.\n',
    'author': 'Bishwarup B',
    'author_email': 'write2bishwarup@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hashtagml/optical',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

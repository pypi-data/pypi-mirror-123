# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygpseq', 'pygpseq.anim', 'pygpseq.fish', 'pygpseq.scripts', 'pygpseq.tools']

package_data = \
{'': ['*'], 'pygpseq': ['static/*']}

install_requires = \
['Cython==0.29.5',
 'Jinja2==2.11.3',
 'czifile==0.1.5',
 'ggc==0.0.3',
 'joblib==0.11',
 'matplotlib==2.2.2',
 'nd2reader==3.1.0',
 'numpy==1.16.1',
 'pandas==0.24.1',
 'scikit-image==0.14.2',
 'scipy==1.2.1',
 'seaborn==0.9.0',
 'tifffile==2019.2.10',
 'tqdm==4.31.1',
 'weasyprint==45']

entry_points = \
{'console_scripts': ['czi_to_tiff = pygpseq.scripts.czi_to_tiff:run',
                     'gpseq_anim = pygpseq.scripts.gpseq_anim:run',
                     'gpseq_fromfish = pygpseq.scripts.gpseq_fromfish:run',
                     'gpseq_fromfish_merge = '
                     'pygpseq.scripts.gpseq_fromfish_merge:run',
                     'nd2_to_tiff = pygpseq.scripts.nd2_to_tiff:run',
                     'tiff_auto3dseg = pygpseq.scripts.tiff_auto3dseg:run',
                     'tiff_desplit = pygpseq.scripts.tiff_desplit:run',
                     'tiff_findoof = pygpseq.scripts.tiff_findoof:run',
                     'tiff_split = pygpseq.scripts.tiff_split:run',
                     'tiffcu = pygpseq.scripts.tiffcu:run']}

setup_kwargs = {
    'name': 'pygpseq',
    'version': '3.4.1',
    'description': 'A GPSeq image analysis package',
    'long_description': "# !DISCLAIMER!\n\n1. **This package is not currently maintained. A new package that will include all `pygpseq` features is being implemented at [`radiantkit`](https://github.com/ggirelli/radiantkit).**\n2. **This package has been developed and tested ONLY for Python3.6, which will reach its end of life On December 23rd, 2021.**\n3. **Versions 3.4.\\* of this package only change package dependencies to fix an issue due to incorrect dependency declaration.**\n\n---\n---\n---\n\npyGPSeq\n===\n\nA Python3.6 package that provides tools to analyze images of GPSeq samples.\nRead the Wiki [documentation](https://github.com/ggirelli/pygpseq/wiki) for more details.  \n\nRequirements\n-------------\n\nPython3.6 and compatible `tkinter` package are required to run `pygpseq`.\nOn Ubuntu 20.04, you can install them with:\n```bash\nsudo add-apt-repository ppa:deadsnakes/ppa\nsudo apt install python3.6\nsudo apt install python3.6-tk\n```\n\nInstallation\n-------------\n\nWe recommend installing `pygpseq` using [`poetry`](https://github.com/python-poetry/poetry).\nCheck how to install `poetry` [here](https://github.com/python-poetry/poetry#installation)\nif you don't have it yet! Once you have `poetry` ready on your system, you can install the\npackage in its own virtual environment with:\n```bash\ngit clone https://github.com/ggirelli/pygpseq.git\ncd pygpseq\npoetry install\n```\nAnd then enter the environment with `poetry shell`.\n\nAlternatively, if you prefer to use `conda` , you can setup an environment with:\n```bash\nconda create -n pygpseq python=3.6\nconda activate pygpseq\nconda install pip\nconda install -c anaconda libtiff \n```\n\nUsage\n----------\n\n### Analyze a GPSeq image dataset\n\nThe `gpseq_anim` (**GPSeq** **an**alysis of **im**ages) analyzes a multi-condition GPSeq image dataset. Run `gpseq_anim -h` for more details.\n\n### Calculate lamin distance of FISH signals\n\nThe `gpseq_fromfish` script characterizes FISH signals identified with `DOTTER` (or similar tools) by calculating: absolute/normalized distance from lamina and central region, nuclear compartment, allele status,... Run `gpseq_fromfish -h` for more details.\n\n### Merge multiple FISH analyses using a metadata table\n\nUse the `gpseq_fromfish_merge` script to merge multiple FISH analysis output (generated with `gpseq_fromfish`). For more details run `gpseq_fromfish_merge -h`.\n\n### Perform automatic 3D nuclei segmentation\n\nRun `tiff_auto3dseg -h` for more details on how to produce binary/labeled (compressed) masks of your nuclei staining channels\n\n### Identify out of focus (OOF) fields of view\n\nRun `tiff_findoof -h` for more details on how to quickly identify out of focus fields of view. Also, the `tiff_plotoof` script (in R, requires `argparser` and `ggplot2`) can be used to produce an informative plot with the signal location over the Z stack.\n\n### Split a tiff in smaller images\n\nTo split a large tiff to smaller square images of size N x N pixels, run `tiff_split input_image output_folder N`. Use the `--enlarge` option to avoid pixel loss. If the input image is a 3D stack, then the output images will be of N x N x N voxels, use the `--2d` to apply the split only to the first slice of the stack. For more details, run `tiff_split -h`.\n\n### (Un)compress a tiff\n\nTo uncompress a set of tiff, use the `tiffcu -u` command. To compress them use the `tiffcu -c` command instead. Use `tiffcu -h` for more details.\n\n### Convert a nd2 file into single-channel tiff images\n\nUse the `nd2_to_tiff` tool to convert images bundled into a nd2 file into separate single-channel tiff images. Use `nd2_to_tiff -h` for the documentation.\n\nContributing\n---\n\nWe welcome any contributions to `pygpseq`. Please, refer to the [contribution guidelines](https://ggirelli.github.io/pygpseq/contributing) if this is your first time contributing! Also, check out our [code of conduct](https://ggirelli.github.io/pygpseq/code_of_conduct).\n\nLicense\n---\n\n```\nMIT License\nCopyright (c) 2017-21 Gabriele Girelli\n```\n",
    'author': 'Gabriele Girelli',
    'author_email': 'gigi.ga90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ggirelli/pygpseq',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)

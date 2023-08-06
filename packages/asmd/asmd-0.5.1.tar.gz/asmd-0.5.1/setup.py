# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asmd', 'asmd.eita']

package_data = \
{'': ['*'],
 'asmd': ['definitions/*', 'my_scores/*'],
 'asmd.eita': ['Programs/*']}

install_requires = \
['alive-progress>=1.3.3,<2.0.0',
 'beautifulsoup4>=4.8.2,<5.0.0',
 'decorator>=4.4.1,<5.0.0',
 'essentia>=2.1b6.dev374,<3.0',
 'hmmlearn>=0.2.5,<0.3.0',
 'joblib>=0.14.1,<0.15.0',
 'mega.py>=1.0.6,<2.0.0',
 'numpy>=1.18.1,<2.0.0',
 'plotly>=4.4.1,<5.0.0',
 'pretty_midi>=0.2.8,<0.3.0',
 'prompt_toolkit>=3.0.3,<4.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'requests>=2.22.0,<3.0.0',
 'scikit_learn>=0.22.1,<0.23.0',
 'setuptools>=45.2.0,<46.0.0',
 'tqdm>=4.43.0,<5.0.0']

setup_kwargs = {
    'name': 'asmd',
    'version': '0.5.1',
    'description': 'Audio-Score Meta-Dataset',
    'long_description': "Audio-Score Meta-Dataset\n========================\n\nASMD is a framework for installing, using and creating music multimodal\ndatasets including (for now) audio and scores.\n\nThis is the repository for paper [1] \n\nRead more in the docs_.\n\n* To install: ``pip install asmd``\n* To install datasets: ``python -m asmd.install``\n* To import API: ``from asmd import asmd``\n\nOther examples in the paper!\n\n.. _docs: https://asmd.readthedocs.org\n\nChangelog\n=========\n\nVersion 0.5\n^^^^^^^^^^^\n\n#. Improved inference of misalignments\n#. Improved the reproducibility of artificial data\n#. Improved the documentation\n#. Added `ASAP` group in **Maestro: broken backward compatibility**\n#. Added `score` for the original score\n#. Added midi note matching based on EITA method\n#. Added missing and extra notes\n#. General refactoring\n#. Added functions for set operations among datasets (union, intersections,\n   complement and subsampling)\n#. Various fixes\n\nVersion 0.4\n^^^^^^^^^^^\n# Skipped\n\nVersion 0.3\n^^^^^^^^^^^\n\n#. Fixed MIDI values ([0, 128) for control changes and pitches)\n#. Fixed metadata error while reading audio files\n#. Fixed pedaling for tracks that have no pedaling\n#. Fixed group selection\n#. Added `get_songs`\n#. Improved initialization of `Dataset` objects\n#. Improved documentation\n\nVersion 0.2.2-2\n^^^^^^^^^^^^^^^\n\n#. Fixed major bug in install script\n#. Fixed bug in conversion tool\n#. Removed TRIOS dataset because no longer available\n#. Updated ground_truth\n\nVersion 0.2.2\n^^^^^^^^^^^^^\n\n#. Improved ``parallel`` function\n#. Improved documentation\n#. Various fixings in ``get_pedaling``\n\nVersion 0.2.1\n^^^^^^^^^^^^^\n\n#. Added ``nframes`` utility to compute the number of frames in a given time lapse\n#. Added ``group`` attribute to each track to create splits in a dataset\n   (supported in only Maestro for now)\n#. Changed ``.pyx`` to ``.py`` with cython in pure-python mode\n\nVersion 0.2\n^^^^^^^^^^^\n\n#. Added ``parallel`` utility to run code in parallel over a while dataset\n#. Added ``get_pianoroll`` utility to get score as pianoroll\n#. Added ``sustain``, ``sostenuto``, and ``soft`` to model pedaling information\n#. Added utilities ``frame2time`` and ``time2frame`` to ease the development\n#. Added ``get_audio_data`` to get data about audio without loading it\n#. Added ``get_score_duration`` to get the full duration of a score without\n   loading it\n#. Added another name for the API: ``from asmd import asmd``\n#. Deprecated ``from asmd import audioscoredataset``\n#. Changed the ``generate_ground_truth`` command line options\n#. Easier to generate misaligned data\n#. Improved documentation\n\nRoadmap\n=======\n\n#. Add matching of same music piece among different datasets\n#. Added `torch.DatasetDump` for preprocessing datasets and use them in pytorch\n#. Add new modalities (video, images)\n#. Add other datasets\n#. Refactoring of the `filter` function (it's a bit long now...)\n\nCite us\n=======\n\n[1]  Simonetta, Federico ; Ntalampiras, Stavros ; Avanzini, Federico: *ASMD: an automatic framework for compiling multimodal datasets with audio and scores*. In: Proceedings of the 17th Sound and Music Computing Conference. Torino, 2020 arXiv:2003.01958_\n\n.. _arXiv:2003.01958: https://arxiv.org/abs/2003.01958\n\n---\n\nFederico Simonetta \n\n#. https://federicosimonetta.eu.org\n#. https://lim.di.unimi.it\n",
    'author': 'Federico Simonetta',
    'author_email': 'federico.simonetta@unimi.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://asmd.readthedocs.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)

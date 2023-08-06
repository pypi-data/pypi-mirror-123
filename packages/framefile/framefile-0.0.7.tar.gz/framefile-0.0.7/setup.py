from pathlib import Path

from setuptools import setup, find_packages


def load_module_dict(filename: str) -> dict:
    import importlib.util as ilu
    filename = Path(__file__).parent / filename
    spec = ilu.spec_from_file_location('', filename)
    module = ilu.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__dict__


name = "framefile"

constants = load_module_dict(f'{name}/_constants.py')

readme = (Path(__file__).parent / 'README.md').read_text(encoding="utf-8")
readme = "# "+readme.partition('# ')[-1]

setup(
    name=name,
    version=constants['__version__'],

    author="Artёm IG",
    author_email="ortemeo@gmail.com",
    url='https://github.com/rtmigo/framefile_py',

    packages=find_packages(include=[name, f'{name}.*']),

    python_requires='>=3.7',
    install_requires=[],

    description="Matching and parsing file names "
                "like IMG_####.JPG or IMG_%04d.JPG",
    long_description=readme,
    long_description_content_type='text/markdown',

    license=constants['__license__'],

    keywords="text string pattern regex parsing integer "
             "glob hash digit number".split(),

    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows"
    ],

    test_suite="test_unit.suite"
)

from setuptools import setup
import versioneer

requirements = [
    "panel", "param", "holoviews", "bokeh", "pandas", "numpy", "scipy", "matplotlib", "adtk", "tqdm", "pyyaml",
    "scipy", "scikit-learn", "statsmodels"
]

setup(
    name='adtkui',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="ADTK UI",
    license="MIT",
    author="Nicky Sandhu",
    author_email='psandhu@water.ca.gov',
    url='https://github.com/dwr-psandhu/adtkui',
    packages=['adtkui'],
    entry_points={
        'console_scripts': [
            'adtkui=adtkui.cli:cli'
        ]
    },
    install_requires=requirements,
    keywords='adtkui',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)

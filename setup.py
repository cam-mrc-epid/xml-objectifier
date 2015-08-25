from setuptools import setup, find_packages
setup(
    name = "xml-objectifier-0.1",
    version = "0.1",
    packages = find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['lxml==3.3.5', 'bunch==1.0.1'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.md', ],
        # And include any *.msg files found in the 'hello' package, too:
        'xml_objectifier': ['*.md'],
    },

    # metadata for upload to PyPI
    author = "David Gillies",
    author_email = "dg467@cam.ac.uk",
    description = "This turns forms system XML into objects",
    license = "",
    keywords = "Forms System XML",
    url = "http://github.com/davidgillies/xml-objectifier",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
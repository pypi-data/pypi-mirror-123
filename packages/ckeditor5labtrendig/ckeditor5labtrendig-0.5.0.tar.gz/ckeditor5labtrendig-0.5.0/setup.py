from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ckeditor5labtrendig',
    version='0.5.0',
    description='CKEditor 5 for django labtrendig to s3.',
    url='https://github.com/LabTrendig/django_ckeditor_5',
    author='josuedjh',
    author_email='josuedjhcayola@outlook.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["*example*"]),
    license='BSD 2-clause',
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
)
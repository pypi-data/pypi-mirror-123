import setuptools  # , Extension

try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setuptools.setup(
    name='mongonow',
    packages=['mongonow'],
    version='0.0.16',
    license='MIT',
    description='MongoNow is the equivalent of sqlite for MongoDB. It\'s a local in-memory mongo-like database.',
    author='Alexandre Mahdhaoui',
    author_email='alexandre.mahdhaoui@gmail.com',
    url='https://github.com/AlexandreMahdhaoui/MongoNow',
    download_url='https://github.com/AlexandreMahdhaoui/MongoNow.git',
    keywords=['mongodb', 'nosql'],
    classifiers=['License :: OSI Approved :: MIT License'],
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
)

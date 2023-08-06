import setuptools


setuptools.setup(
    name='easyquiz',
    version='0.2',
    author='Pablo Lapeña Mañero',
    author_email='plapenamanero@gmail.com',
    description='Module to create quick quizzes for IPython',
    long_description_content_type='text/markdown',
    package_data={'': ['langs.json']},
    url='https://github.com/plapenamanero/easyquiz',
    download_url='https://github.com/plapenamanero/easyquiz/archive/refs/tags/v0.2.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=['ipywidgets>=7.6.5'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: IPython',
        'Framework :: Jupyter',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
)

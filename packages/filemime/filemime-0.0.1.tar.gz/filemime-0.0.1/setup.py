import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="filemime",
    version="0.0.1",
    author="T.THAVASI",
    license="MIT",
    author_email="ganeshanthavasigti1032000@gmail.com",
    description="this pkg use find file mime type get to use pkg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source":"https://github.com/THAVASIGTI/filemime.git",
        "Tracker":"https://github.com/THAVASIGTI/filemime/issues",
    },
    zip_safe=True,
    # data_files=[('', ['filemime/usr/bin/*.exe','filemime/usr/bin/*.dll','filemime/usr/share/misc/*.mgc'])],
    package_data={"filemime":['filemime/usr/bin/*.exe','filemime/usr/bin/*.dll','filemime/usr/share/misc/*.mgc']},
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities'],
    install_requires=[],
    python_requires='>=3',
)
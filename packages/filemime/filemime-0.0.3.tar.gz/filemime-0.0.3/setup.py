import setuptools


from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="filemime",
    version="0.0.3",
    author="T.THAVASI",
    license="MIT",
    author_email="ganeshanthavasigti1032000@gmail.com",
    description="this package use finds all types of file extension or mime types.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source":"https://github.com/THAVASIGTI/filemime.git",
        "Tracker":"https://github.com/THAVASIGTI/filemime/issues",
    },
    zip_safe=True,
    data_files=[('', ['filemime/usr/bin/file.exe','filemime/usr/bin/msys-2.0.dll',
            'filemime/usr/bin/msys-bz2-1.dll','filemime/usr/bin/msys-magic-1.dll',
            'filemime/usr/bin/msys-z.dll','filemime/usr/share/misc/magic.mgc'
    ])],
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
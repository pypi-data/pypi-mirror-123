
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nested-multipart-parser",
    version="0.0.3",
    author="Example Author",
    license='MIT',
    author_email='contact@germainremi.fr',
    description="A parser for nested data in multipart form",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/remigermain/nested-multipart-parser",
    project_urls={
        "Bug Tracker": "https://github.com/remigermain/nested-multipart-parser/issues",
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=["nested_multipart_parser"],
    python_requires=">=3.6",
)

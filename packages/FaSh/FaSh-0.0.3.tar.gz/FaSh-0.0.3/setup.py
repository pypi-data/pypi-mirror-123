import setuptools

# with open('README.md','r') as fh:
#     long_description = fh.read()

setuptools.setup(
    name='FaSh',
    version='0.0.3',
    author='HK.xu',
    author_email='xhkdwyyx@163.com',
    description='Easy tools helping build iSpace programs',
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    url='https://github.com/Loveinwei/FaSh',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0'
)

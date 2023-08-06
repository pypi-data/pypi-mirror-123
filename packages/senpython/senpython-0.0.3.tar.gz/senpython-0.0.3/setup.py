from setuptools import setup, find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='senpython',  # How you named your package folder (MyLib)
    packages=find_packages(),  # Choose the same as "name"
    version='0.0.3',  # Start with a small number and increase it with every change you make
    license='mit',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Senpai is an esoteric programming language that is inspired by anime girls. Don\'t ask why I made this.',  # Give a short description about your library
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='4gboframram',  # Type in your name
    # author_email='no',  # Type in your E-Mail
    url='https://github.com/4gboframram/Senpython',  # Provide either the link to your github or to your website
  
    keywords=['programming_language', 'esolang', 'senpai'],  # Keywords that define your package best
    install_requires=[
		'lark'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.8'
    ],
	zip_safe=False,
	include_package_data=True 
)
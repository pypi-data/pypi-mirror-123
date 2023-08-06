from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup_args = dict(
    name='fumoAPI',
    version='1.3',
    description='Simple API wrapper for https://fumos.live',
    long_description_content_type="text/markdown",
    long_description=long_description,
    license='MIT',
    packages=find_packages(),
    author='Adobee',
    author_email='Adobe@katsumi.cf',
    keywords=['fumoAPI'],
    url='https://github.com/Airiuwu/fumoAPI',
    download_url='https://pypi.org/project/fumoAPI/'
)

install_requires = [
    'aiohttp',
    'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
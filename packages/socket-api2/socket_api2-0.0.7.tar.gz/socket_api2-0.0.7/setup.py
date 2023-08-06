from setuptools import setup, find_packages, version

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name="socket_api2",
    version="0.0.7",
    description="This is make easier to create servers and clients with socket, and its compatible with ngrok (pyngrok)",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Da4ndo',
    author_email = 'vrgdnl20@gmail.com',
    License="MIT",
    classifiers=classifiers,
    keywords=['socket_api2', 'socket', 'socket_api', 'socket api', 'socket api 2'],
    packages=find_packages(),
    install_requires=['pyngrok', 'colorama']
)
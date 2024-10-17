from setuptools import setup, find_packages
setup(
  name = 'llmservice',
  version = '0.1.0',
  packages=['llmservice'],
  install_requires = [
    'llama-cpp-python==0.3.1',
    'Flask==3.0.3',
    'Flask-Cors==3.0.10',
    'pymupdf==1.24.11',
    'easyocr==1.7.2',
    'pytest==6.2.4',
    ],
)
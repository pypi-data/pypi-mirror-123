from setuptools import setup, find_packages

setup(name='print_debugging',
      version='0.0.1',
      url=' https://github.com/benjamin-jin/debugger',
      author='Benjamin Jin',
      author_email='jinrudals135@naver.com',
      description='Load module, function from string',
      packages=find_packages(exclude=['']),
      long_description=open('README.rst').read(),
      install_requires=['ansicolors', 'dynamic-load'],
)
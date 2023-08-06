from setuptools import setup

setup(name='terra-2.0',
      version='0.2',
      description='Script to simulate planet formation or engulfment',
      url='https://github.com/ramstojh/terra',
      author='Jhon Yana',
      author_email='ramstojh@alumni.usp.br',
      license='MIT',
      packages=['terra'],
      #package_dir={'terra':'terra'},
      package_data={'terra': ['data/*.txt'], 'terra': ['data/*']},
      include_package_data=True,
      install_requires=['numpy', 'pandas', 'tqdm', 'astropy', 'matplotlib'],
      zip_safe=False)

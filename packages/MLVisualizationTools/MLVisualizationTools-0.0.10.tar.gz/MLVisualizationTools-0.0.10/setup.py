from setuptools import setup

#TODO - fix model packaging

setup(
    name='MLVisualizationTools',
    url='https://github.com/RobertJN64/MLVisualizationTools',
    author='Robert Nies',
    author_email='robertjnies@gamil.com',
    # Needed to actually package something
    packages=['MLVisualizationTools'],
    include_package_data=True,
    install_requires=['pandas'],
    extras_require={'dash': ['dash', 'plotly', 'dash_bootstrap_components>=1.0.0'],
                    'dash-notebook': ['dash', 'plotly', 'dash_bootstrap_components>=1.0.0', 'jupyter-dash']},
    # *strongly* suggested for sharing
    version='0.0.10',
    # The license can be anything you like
    license='MIT',
    description='A set of functions and demos to make machine learning projects easier to understand.',
    long_description=open('README.md').read(),
)
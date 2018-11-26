from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='gigmapr-processor',
    python_requires='>3.5.0',
    version='0.4.0',
    packages=['gigmapr_processor'],
    description='Celery task definition for gigmapr',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Sam Kleiner',
    author_email='sam@skleiner.com',
    license='MIT',
    install_requires=[
        'redis~=2.10.6', 'celery>=4.0.0', 'requests', 'beautifulsoup4'
    ],
)

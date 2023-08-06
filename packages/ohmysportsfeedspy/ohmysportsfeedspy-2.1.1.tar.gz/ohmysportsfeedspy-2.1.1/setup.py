from distutils.core import setup

setup(
    name='ohmysportsfeedspy',
    packages=['ohmysportsfeedspy'],
    version='2.1.1',
    author = ['Brad Barkhouse', 'MySportsFeeds'],
    author_email='brad.barkhouse@mysportsfeeds.com',
    url='https://github.com/MySportsFeeds/mysportsfeeds-python',
    license='MIT',
    description='A Python wrapper for the MySportsFeeds Sports Data API',
    install_requires=[
        'requests>=2,<3',
        'simplejson>=3,<4',
        'python-dateutil>=2,<3',
    ]
)

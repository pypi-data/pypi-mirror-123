from setuptools import find_packages, setup

setup(
    name='notifierbot',
    packages=find_packages(include=['notifierbot']),
    version='1.1.0',
    description='Python Library for different Notification Bots',
    author='Sakshay Mahna',
    author_email='sakshum19@gmail.com',
    url='https://github.com/SakshayMahna/Notifier-Bot/archive/refs/tags/v1.0.0.tar.gz',
    keywords=['bot', 'notification', 'notifier'],
    license='MIT',
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'requests'],
    test_suite='tests',
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.8',
  ],
)
from distutils.core import setup
setup(
  name = 'packages_load',
  packages = ['packages_load'],
  version = '0.1.2',
  license='MIT',
  description = 'Read/Download files from s3 bucket , authentication',
  author = 'Aravind',
  author_email = '',
  url = 'https://github.com/aravindalbert/packages.git',
  download_url = '',
  keywords = ['load download files s3 bucket preprocess authentication'],
  install_requires=[
    'boto3',
    'fastapi',
    'python-jose[cryptography]',
    'Authlib',
    'starlette-authlib'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
  ],
)
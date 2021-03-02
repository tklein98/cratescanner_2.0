from setuptools import find_packages
from setuptools import setup
import cloudinary
import os

cloudinary.config(cloud_name=os.environ.get('CLOUDINARY_NAME'),
                  api_key=os.environ.get('CLOUDINARY_API_KEY'),
                  api_secret=os.environ.get('CLOUDINARY_API_SECRET'))

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content if 'git+' not in x]

setup(name='crate_scanner',
      version="1.0",
      description="Project Description",
      packages=find_packages(),
      install_requires=requirements,
      test_suite='tests',
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      scripts=['scripts/crate_scanner-run'],
      zip_safe=False)

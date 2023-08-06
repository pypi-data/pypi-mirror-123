#from distutils.core import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'organization_map',
  packages = ['organization_map'], # this must be the same as the name above
  version = '1.0.2',
  description = 'Creates an organization map image',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'snuids',
  author_email = 'snuids@mannekentech.com',
  url = 'https://github.com/snuids/organization_map', 
  download_url = 'https://github.com/snuids/organization_map/archive/1.0.2.tar.gz',
  keywords = ['Python', 'image', 'hierarchical','tree','diagram'], # arbitrary keywords
  classifiers = [],
)

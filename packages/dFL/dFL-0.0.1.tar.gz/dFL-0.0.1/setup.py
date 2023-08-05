from setuptools import setup, find_packages

setup(
  name='dFL', 
  version='0.0.1',  
  license='MIT',  
  description='This project aims to build a decentralized federated learning library',  
  author='Ahmed Mukhtar Dirir',                   
  author_email='ahmed.m.dirir@gmail.com',      
  url='https://github.com/a-dirir/decentralized_FL',  
  keywords=['Federated Learning', 'Decentralized'], 
  install_requires=[     
        "cryptography",
        "Flask",
        "mongoengine",
        "numpy",
        "pymongo",
        "requests",
        "colorlog",
      ],
  extras_require = {
        "dev": [
        "pytest>=3.7",
        ],
    },
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.5',      
    'Programming Language :: Python :: 3.6',      
    'Programming Language :: Python :: 3.7',      
    'Programming Language :: Python :: 3.8',     
  ],
  packages= find_packages(), 
  package_data={'dFL': ['MainServer/keys/*.pem']},
  include_package_data=True,
)
from setuptools import setup, find_packages
setup(name='blurredface_sts_test',
      version='0.1.9',
      description='Blurred face',
      author='Leesudong',
      author_email='905412718@qq.com',
      requires= ['numpy','matplotlib'],
      packages=find_packages(),
      package_data={
         "blurredface_sts_test": ["haarcascade/*.xml"],
     },
      license="apache 3.0"
      )

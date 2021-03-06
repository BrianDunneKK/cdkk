import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='cdkk',  
     version='0.6',
     author="Brian Dunne",
     author_email="Hidden@gmail.com",
     description="Python wrappers created by CoderDojo Kilkenny",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/BrianDunneKK/pygame-cdkk",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
 
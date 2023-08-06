import setuptools

setuptools.setup(name='ewconfig',
                 packages=setuptools.find_packages(),
                 version='0.1.4',
                 author='andrew cooke',
                 author_email='andrewcooke@isti.com',
                 description='Create EW config from Station XML',
                 long_description='''
# ewconfig

Create EW config from Station XML
                 ''',
                 long_description_content_type='text/markdown',
                 include_package_data=True,
                 setup_requires=[
                     # this is required by obspy for install
                     'numpy'
                 ],
                 install_requires=[
                     'obspy'
                 ],
                 entry_points={
                     'console_scripts': [
                         'sacpz2ew = ewconfig.sacpz2ew:main_args',
                         'stationxml2ew = ewconfig.stationxml2ew:main_args',
                         'ewmerge = ewconfig.ewmerge:main_args',
                     ],
                 },
                 classifiers=(
                     "Programming Language :: Python :: 3.9",
                     "Operating System :: OS Independent",
                     "Development Status :: 4 - Beta",
                 ),
                 )

from setuptools import setup

dependencies = ['asttokens==2.0.5', 'certifi==2021.10.8', 'charset-normalizer==2.0.7', 'colorama==0.4.4', 'executing==0.8.2', 'halo==0.0.31', 'icecream==2.1.1', 'idna==3.3', 'log-symbols==0.0.14', 'pause==0.3', 'prettytable==2.2.1', 'Pygments==2.10.0', 'PyJWT==2.3.0', 'requests==2.26.0', 'six==1.16.0', 'spinners==0.0.24', 'termcolor==1.1.0', 'urllib3==1.26.7', 'wcwidth==0.2.5']
setup(
	name="waveradio-0.3", 
	version="0.0.1", 
	description="serius ini deskripsi", 
	url="", 
	author="Muhammad Al Fajri", 
	author_email="fajrim228@gmail.com", 
	license="unlicensed", 
	packages=["waveradio"],
	install_requires=dependencies,
	scripts=['bin/wave'], 
	zip_safe=False
)
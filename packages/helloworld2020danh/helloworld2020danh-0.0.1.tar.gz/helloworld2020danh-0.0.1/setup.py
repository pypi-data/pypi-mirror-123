from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name="helloworld2020danh",
	version='0.0.1',
	description="Say Hello",
	py_modules=["helloworld"],
	package_dir={'': 'src'},
	classifiers=[
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
			],
	long_description=long_description,
	long_description_content_type="text/markdown",
	install_requires = [
		"numpy ~=1.20",
			],
	extras_require = {
		"dev": [
			"pytest>=3.7",
			],
			},
)

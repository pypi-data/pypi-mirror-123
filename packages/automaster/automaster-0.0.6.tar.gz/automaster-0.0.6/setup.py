import setuptools
package_data={
    'autotk': ['*.pyd', '*.dll'],
}
setuptools.setup(include_package_data=True,packages=setuptools.find_packages("whl"),package_data=package_data,install_requires=[
    'requests>=1.0',
])

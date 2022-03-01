from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

setup_args = generate_distutils_setup(
    packages=['driver'],
    package_dir={'':'BMI160_i2c'}
)

setup(**setup_args)
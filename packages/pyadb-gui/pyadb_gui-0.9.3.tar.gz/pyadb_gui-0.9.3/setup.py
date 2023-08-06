from setuptools import setup, find_packages

# with open("README.md", "r", encoding="utf-8") as rd:
#     readme = rd.read()

setup(
    name='pyadb_gui',
    version="0.9.3",
    author='Pilchark',
    author_email='xq_work@outlook.com',
    # license='GNU General Public License v2.0',
    description='Operate Android devices with a GUI tool producted by Python.',
    # long_description = readme,
    # long_description_content_type="text/markdown",
    url='https://gitee.com/pilchark/',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'pyadb=pyadb_gui.main:main',
        ]
    }


)

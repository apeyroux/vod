from setuptools import setup

setup(
    name='vod',
    packages=['vod'],
    include_package_data=True,
    package_dir={'vod': 'src'},
    zip_safe=False,
    entry_points={'console_scripts': ['vod = vod.__main__:main']}
)

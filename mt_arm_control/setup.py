from setuptools import find_packages, setup

package_name = 'mt_arm_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rudra',
    maintainer_email='hironmoy.roy.rudra@g.bracu.ac.bd',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "test_arm = mt_arm_control.test_arm:main",
        ],
    },
)

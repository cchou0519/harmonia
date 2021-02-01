from setuptools import setup
setup(
    name='blurnn',
    version='0.1',
    description='BlurNN is a pytorch privacy preserving module',
    packages=['/app/blurnn', '/app/blurnn.optim'],
    author='AILabs',
    license='MIT License',
    requires=['torch'],
)

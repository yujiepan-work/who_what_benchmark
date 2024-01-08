from setuptools import setup, find_packages

setup(
    name='whowhatbench',
    version='1.0.0',
    url='https://github.com/andreyanufr/who_what_benchmark.git',
    author='Intel',
    author_email='',
    description='Short test for LLMs',
    packages=find_packages(),
    install_requires=[
        'transformers>=4.35.2',
        'sentence-transformers>=2.2.2',
        'openvino-nightly',
        'openvino-telemetry',
        'optimum>=1.14.1',
        'optimum-intel @ git+https://github.com/huggingface/optimum-intel.git@03e1fa6742acc1852e64c636646e2ce486bb9fbd',
        'pandas>=2.0.3',
        'numpy>=1.23.5',
        'tqdm>=4.66.1'
    ],
)

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
      name='work_stream',
      version='0.0.1',
      author='fengqing',
      author_email='fq20210602@gmail.com',
      url="https://github.com/fengqing2021/work-stream",
      description='这是一个运维工作流模块',
      packages=find_packages(),
      long_description=long_description,
      long_description_content_type="text/markdown",
      zip_safe=True,
      python_requires=">=3.6",
)

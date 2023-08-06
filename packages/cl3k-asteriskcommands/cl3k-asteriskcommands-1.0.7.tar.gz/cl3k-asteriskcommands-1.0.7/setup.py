from setuptools import setup, find_packages
import subprocess

git_command_result: subprocess.CompletedProcess = subprocess.run(
    ["git", "describe", "--tags"], capture_output=True, encoding="utf-8"
)
actual_version: str = git_command_result.stdout.strip("\n")

setup(
    name="cl3k-asteriskcommands",
    version=actual_version,
    packages=find_packages(),
    author="Juares Vermelho Diaz (CL3k)",
    author_email="jvermelho@cl3k.com",
    description="API for share asterisk commands beetween the micro services",
    keywords="Asterisk commands",
    install_requires=[],
)

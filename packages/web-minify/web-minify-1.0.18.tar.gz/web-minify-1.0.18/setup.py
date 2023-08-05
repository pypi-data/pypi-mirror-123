#!/usr/bin/env python

import os
import pprint
from setuptools import setup, find_packages, find_namespace_packages

# from pathlib import Path
# from shutil import copytree, which
# from tempfile import TemporaryDirectory
# from zipapp import create_archive

import logging

logger = logging.getLogger(__name__)

setup_requirements = ["pytest-runner", "setuptools_scm"]

version_file = "./VERSION"
readme_file = "./README.md"


def read_file(fname, strip=True):
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    data = ""
    if os.path.exists(fn):
        with open(fn) as f:
            data = f.read()
            data = data.strip() if strip else data
            # logger.info(f"Got data '{data}' from '{fn}'")
    else:
        logger.error(f"Could not find file {fn}")
        logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
    return data


def write_file(fname, data, do_overwrite=False):
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    if not os.path.exists(fn) or do_overwrite:
        with open(fn, "w") as f:
            f.write(data)
    else:
        logger.warning(f"File {fn} already exists")
        logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
    return data


def remove_comment(line, sep="#"):
    i = line.find(sep)
    if i >= 0:
        line = line[:i]
    return line.strip()


def read_requirements_file(fname: str, do_strip: bool = True):
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    print(f"Reading requirements from {fn} with do_strip = {do_strip}")
    lines = []
    if os.path.exists(fn):
        with open(fn) as f:
            for r in f.readlines():
                r = r.strip()
                if len(r) < 1:
                    continue
                r = remove_comment(r)
                if len(r) < 1:
                    continue
                lines.append(r)
    else:
        logger.error(f"Could not find requirements file {fn}")
        logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
    # logger.warning(f"Full content of '{fname}' was: \n{lines}")
    if not do_strip:
        return lines
    out = []
    for line in lines:
        if line and not line.startswith("-"):
            out.append(line)
    return out


def debug_repo(repo):
    if not repo:
        print(f"No repo")
        return
    print(f"Repository head commit: {repo.head.commit}")
    print(f"Found {len(repo.branches)} branches:")
    for branch in repo.branches:
        print(f" + {branch}({branch.commit})")
    remote = repo.remote()
    print(f"Found {len(remote.refs)} remote refs:")
    for ref in remote.refs:
        print(f" + {ref}({ref.commit})")


def get_git_branch_from_env():
    branch_env = "FK_GIT_ACTUAL_BRANCH"
    branch = os.environ.get(branch_env, None)
    if branch is not None:
        print(f"Using {branch_env} = {branch} from environment")
    else:
        print(f"No value for {branch_env} found")
    return branch


def generate_version_string(version=None, branch=None):
    version = read_file(version_file) if version is None else version
    branch = get_git_branch_from_env() if branch is None else branch
    full_version = ""

    if branch == "production":
        full_version = version
    elif branch == "beta":
        full_version = f"{version}-beta"
    elif branch.startswith("stage-") and len(branch) > 6:
        full_version = f"{version}-{branch[6:]}"
    else:
        full_version = f"{version}-test-{branch.replace(' ','_').replace('	','_')}"
    print(f"Using full version = {full_version}")
    return full_version


def get_version_string():
    # Not viable
    # return generate_version_string();
    return read_file(version_file)


##############################################################################
# Dont touch below


# class ZipApp(Command):
#    description, user_options = "Creates a ZipApp.", []
#    def initialize_options(self):
#        pass  # Dont needed, but required.
#    def finalize_options(self):
#        pass  # Dont needed, but required.
#    def run(self):
#        with TemporaryDirectory() as tmpdir:
#            copytree(".", Path(tmpdir) / "web-minify")
#            (Path(tmpdir) / "__main__.py").write_text("import runpy\nrunpy.run_module('web-minify')")
#            create_archive(tmpdir, "web-minify.pyz", which("python3"))


##############################################################################

package = {
    "name": "web-minify",
    "version": get_version_string(),
    "author": "Lennart Rolland",
    "author_email": "lennart@octomy.org",
    "maintainer": "Lennart Rolland",
    "maintainer_email": "lennart@octomy.org",
    "description": ("CSS HTML JS SVG PNG JPEG Minifier"),
    "license": "GPL-3 LGPL-3 MIT",
    "platforms": ["Linux"],
    "keywords": "python3, CSS, HTML, JS, SVG, PNG, JPEG, Compressor, CSS3, HTML5, Web, Javascript, Minifier, Minify, Uglify, Obfuscator",
    "url": "https://gitlab.com/octomy/web-minifier",
    "download_url": "https://gitlab.com/octomy/web-minify",
    "project_urls": {"Docs": "https://gitlab.com/octomy/web-minify/README.md", "Bugs": "https://gitlab.com/octomy/web-minify/-/issues", "C.I.": "https://gitlab.com/octomy/web-minify/pipelines"},
    "packages": find_packages(),
    "scripts": ["web-minify.py"],
    "zip_safe": True,
    "long_description": read_file("README.md"),
    "long_description_content_type": "text/markdown",
    "setup_requires": setup_requirements,
    "install_requires": read_requirements_file("requirements/requirements.in"),  # Allow flexible deps for install
    "tests_require": read_requirements_file("requirements/test_requirements.txt"),  # Use rigid deps for testing
    "test_suite": "../tests",
    "python_requires": ">=3.7.4",
    "data_files": [("web-minify", [version_file])],
    "include_package_data": True,
    # scripts=['css-html-js-minify.py'],  # uncomment if want install as script
    "entry_points": {"console_scripts": ["web-minify = web_minify.minify:main"]},
    # "cmdclass": {"zipapp": ZipApp},
    # From https://pypi.org/pypi?%3Aaction=list_classifiers
    "classifiers": ["Development Status :: 3 - Alpha", "Intended Audience :: Developers", "Intended Audience :: Other Audience", "Topic :: Utilities", "Natural Language :: English", "Operating System :: POSIX :: Linux", "Programming Language :: Python :: 3.7", "Topic :: Other/Nonlisted Topic"],
}


# pprint.pprint(package)
setup(**package)

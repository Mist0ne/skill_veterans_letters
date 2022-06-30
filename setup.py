#!/usr/bin/env python

import os

from setuptools import find_packages, setup

VERSION = os.getenv("CI_COMMIT_TAG")
if not VERSION:
    VERSION = "0.0.1"

# --- >
setup(
    name="skill-veterans-letters",
    version=VERSION,
    package_dir={'skill_veterans_letters': 'src/skill_veterans_letters'},
    python_requires=">=3.6.8",
    packages=find_packages(where='src', include=['skill_veterans_letters']),
    url="https://gitlab.com/mailru-voice/external_skills/skill_veterans_letters",
    license="MIT",
    author="n.orgeev",
    author_email="n.orgeev@corp.mail.ru",
    description="skill-veterans-letters",
)


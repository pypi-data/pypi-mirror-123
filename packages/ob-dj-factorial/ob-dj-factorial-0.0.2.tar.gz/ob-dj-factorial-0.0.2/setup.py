from setuptools import setup

setup(
    install_requires=["django", "celery", "djangorestframework",],
    packages=[
        "ob_dj_factorial.apis.factorial",
        "ob_dj_factorial.core.factorial",
        "ob_dj_factorial.core.factorial.admin",
        "ob_dj_factorial.core.factorial.migrations",
        "ob_dj_factorial.core.factorial.templates",
    ],
    tests_require=["pytest"],
    use_scm_version={"write_to": "version.py",},
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.html",],
    },
)

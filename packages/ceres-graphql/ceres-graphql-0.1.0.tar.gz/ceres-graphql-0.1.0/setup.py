from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="ceres-graphql",
    install_requires=("graphql-core >= 3.0",),
    extras_require={
        "relay": ("graphql-relay >= 3.0",),
    },
)

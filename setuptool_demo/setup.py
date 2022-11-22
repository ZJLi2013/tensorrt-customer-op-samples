from setuptools import Extension, setup

setup(
        name="cppextension",
        ext_modules=[
            Extension(
                name="cppextension",
                sources=["src/add.cpp"],
                include_dirs=["/opt/conda/lib/python3.8/site-packages/pybind11/include"],
            ),
        ],
    )



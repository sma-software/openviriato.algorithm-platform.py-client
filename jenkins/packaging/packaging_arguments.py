import os


def assemble_packaging_arguments(name_of_requirements: str, py_client_build_number: str, output_file_path: str) -> dict:
    with open(name_of_requirements, 'r') as f:
        required_modules = f.read().splitlines()

    absolute_output_path = os.path.abspath(output_file_path)

    return dict(
        install_requires=required_modules,
        name='algorithmplatform',
        version='0.0.{0}'.format(py_client_build_number),
        packages=['py_client.aidm', 'py_client.Conversion', 'py_client.Communication', 'py_client.algorithm_interface'],
        url='https://www.sma-partner.com',
        license='',
        author='',
        author_email='',
        description='',
        script_args=["bdist_wheel",  "-d", absolute_output_path]
    )

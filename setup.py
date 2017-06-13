from distutils.core import setup

setup(
     name="umsamples",
     version='0.1',
     install_requires =[
            "asn1crypto >=0.22.0"
            "certifi>=2017.4.17"
            "cffi>=1.10.0"
            "chardet>=3.0.4"
            "cryptography>=1.9"
            "enum34>=1.1.6"
            "idna>=2.5"
            "ipaddress>=1.0.18"
            "logging>=0.4.9.6"
            "pycparser>=2.17"
            "pyOpenSSL>=17.0.0"
            "requests>=2.17.3"
            "six>=1.10.0"
            "urllib3>=1.21.1"
            "xmltodict>=0.11.0"
               ],
     author='Bob Webster',
     license='MIT',
     url = 'https://github.com/rdbwebster/umsamples',
     description = 'VMware Usage Meter API Samples.',
)

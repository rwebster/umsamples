



### umtools runtime Installation ###

1. Create a python virtual environment

```
   virtualenv venv
   cd venv
   source bin/activate
```

2. Check out the code from github

```
   git clone https://www.github.com:/rdbwebster/umtools.git
   cd umtools
```

3. Install the package and dependencies

``` 
   pip install -U setuptools
   pip install .
```


### Installation for umtools Development Environment ###

umtools should be installed and executed in a Python 2 Virtual Environment.

#### umtool Prerequisites ####

* Python 2.7
* Pip 9.0.1

Verify the python and pip versions on the development workstation


```
$ python --version
Python 2.7.10

$ pip --version
pip 9.0.1 from /Users/bwebster/python/virtualEnvs/umtools/lib/python2.7/site-packages (python 2.7)

// upgrade pip if needed - Mac OSX

sudo pip install --upgrade pip

```


####  SSL Handshake failure on Mac OSX 10
http.requests ssl error: [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure

Requires an updated OpenSSL library

Two Choices
*     Install OpenSSL from Homebrew, then install a new version of Python 2 from Homebrew which will automatically link against the Homebrew-provided OpenSSL.

*     Install OpenSSL from Homebrew, and then install PyOpenSSL against that new version by running 
```env ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install PyOpenSSL.

```

pip install PyOpenSSL

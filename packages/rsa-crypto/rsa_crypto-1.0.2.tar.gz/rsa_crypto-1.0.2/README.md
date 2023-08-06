# rsa_crypto

A Python 3 library for encrypting and decrypting files and/or key/value pairs in a particular section of a configuration file (.ini file).

This library uses public/private RSA keys to perform the encryption.


## Installation

Download or clone this repository, cd to the directory and type:

```
python3 setup.py install
```


## Usage

This script can be used to:
- manage private (encryption), public (decryption) and the password-protected private/public keys (`create` `extract` or `clear`)
- encrypt and decrypt files (`encrypt` or `decrypt`)
- store and retrieve encrypted values stored in a configuration file (`get` or `set`)


```
rsa_crypto -h
usage: rsa_crypto [-h]  ...

optional arguments:
  -h, --help  show this help message and exit

commands:

    encrypt   Encrypt a file using an RSA certificate
    decrypt   Decrypt a file using an RSA certificate
    extract   Extract public and private keys
    create    Create new keys
    set       Encrypt a value in a configuration file using an RSA certificate
    get       Decrypt a value in a configuration file using an RSA certificate
    clear     Delete the unencrypted private key
```

### Create a new RSA key

The `create` parameter is used to create a new RSA 4096-bit public/private key pair. The default name is `.rsa_key.bin` but an alternate prefix can be specified by using the `-k <prefix>` parameter. This allows users to create and use several keys to further protect their data. Users are required to set a password to protect this public/private key pair. This key is created in the user's home directory by default.

> This key can be used both for encryption and decryption of your data, but will require users to enter the key password with each use. Keep this file private and do not distribute to anyone.

```
rsa_crypto create -k dev
Enter key password:
Re-enter key password:
Creating key...
Created password-protected private/public keys file /Users/me/dev_key.bin
Use the "extract" keyword to create public and private key files.
```

### Extract the public and private keys from the RSA key pair

The private and public keys can be extracted from the key pair by using the `extract` parameter. This allows users to distribute the public (encryption) key to other users to allow them to encrypt files and/or values. This key is *not* password protected and *cannot* be used for decrypting the data.

If the `-k` option is not used, all key files will have the default `.rsa_` prefix. Key files are created in the user's home directory by default.

The private key will allow anyone in its possession to decrypt files and data, *be extremely careful with who can access it because it is no longer password protected*. This file can be used for feeding decrypted values to automation tools without having to provide a password. *Make sure to delete (`clear`) this file when automated decryption is no longer needed.*

```
rsa_crypto extract -k dev
Using key: /Users/me/dev_key.bin
Opening encrypted key.
Enter key password:
Created private key file /Users/me/dev_private.pem (File can decrypt data and is not password-protected, keep it safe!)
Created public key file /Users/me/dev_public.pem (distribute this one to anyone who needs to encrypt data, it cannot be used for decryption!)
```

The encryption and decryption options will look for these 2 files first and only use the password-protected key pair file if they are not present.

 *Make sure to delete (`clear`) the unprotected private key file when passwordless decryption is no longer needed. This will only delete the private key file, the public key and the password-protected key-pair files will remain on your system.*

```
rsa_crypto clear -k dev
Using key: /Users/me/dev_private.pem
Private key deleted: /Users/me/dev_private.pem
```

> These files can be moved to a different directory if needed, the script will look for them in the user's home directory, and the current directory where the command is executed by default. You can also specify an absolute path when using the `-k` parameter.

> While the private and public keys can always be extracted from the password-protected key-pair file `dev_key.bin`, the key-pair file cannot be recreated. *If you delete both the private key and the key-pair file then you will no longer be able to decrypt your files or data.*

#### Environment Variables

The public and private keys don't have to exist as files, they can also be set as environment variables. For example:

```bash
export rsa_private=$(cat /Users/me/rsa_private.pem)
export rsa_public=$(cat /Users/me/rsa_public.pem)
```

The script will let you know that the environment variable was used:
...
```
Using Environment Variable rsa_public
...
```

### Encrypt and decrypt a file

The `encrypt` parameter can be used to encrypt a file, and the `decrypt` parameter can be used to decrypt a file. Encrypted files will have a `.enc` extension added to the file name. At this time, this script cannot be used to encrypt/decrypt directories, only single files.

> These parameters can be used to encrypt/decrypt binary files as well. Make sure to test appropriately, the author of this script is not responsible for data loss or any misuse of these scripts.


```
touch my_file.txt
encrypt -k dev -f my_file.txt
Using key: /Users/me/dev_public.pem
/Users/me/Documents/my_file.txt.enc
```

The file can then be decrypted using:

```
rsa_crypto decrypt -k dev -f my_file.txt.enc
Using key: /Users/me/dev_key.bin
Opening encrypted key.
Enter key password:
```
> If the private key file is present, the decryption will not prompt users for the password and the decryption will occur automatically.

If the wrong private key file is used or an invalid password is entered, the file will fail to be decrypted.

```
rsa_crypto decrypt -f my_file.txt.enc
Using key: /Users/me/.rsa_key.bin
Opening encrypted key.
Enter key password:
Failed to decrypt file
```

### Encrypt and decrypt values

This `get` and `set` parameters of the script can also be used to store and retrieve encrypted values in a configuration file. By default, the file will be stored is the user's home directory and named `.rsa_values.conf` regardless of the key prefix used. This allows for different values in this file to be encrypted using different public encryption keys, maybe by different people.

The structure of the file is fairly simple, it contains sections delimited by brackets `[MY_SECTION]`. Note that the section name is case-sensitive. The `[DEFAULT]` section is used by default.

Each section will then contain several "options" and values (key/value pairs). Only the value will be encrypted, the option name will remain in clear text.

> This structure is very well suited for keeping track of values that need to be different by environment, such as to keep track of database passwords in a DEV, TEST and PRODUCTION environments.


To save a value of an option named `database_password` in the `DEV` section using the default encryption key:

```
rsa_crypto set -s DEV -o database_password
Using key: /Users/me/Documents/rsa_public.pem
Enter value:
DEV my_password
set
Updated /Users/me/.rsa_values.conf
```

If you don't specify a value, the script will prompt you for the value so that it is not visible in the command line history. Optionally, if you prefer, you can also specify the value as a command line parameter by using the `-v` parameter.


```
rsa_crypto set -s DEV -o database_password -v my_secret_password
Using key: /Users/me/Documents/rsa_public.pem
DEV my_secret_password
set
Updated /Users/me/.rsa_values.conf
```

To decrypt the value:


```
rsa_crypto get -s DEV -o database_password
Using key: /Users/me/rsa_private.pem
get
Reading from /Users/me/.rsa_values.conf
DEV database_password my_secret_password
my_secret_password
```

> Note that in the above example the `rsa_private.pem` private key allowed us to decrypt the data without prompting for a password. Once again, *be extremely careful because anyone with that file can decrypt the data*. If the private key is not present, the script would then be prompting for a password to open the protected key-pair file `rsa_key.bin`.


```
rsa_crypto clear
Using key: /Users/me/rsa_private.pem
Private key deleted: /Users/me/rsa_private.pem
```

```
rsa_crypto get -s DEV -o database_password
Using key: /Users/me/rsa_key.bin
Opening encrypted key.
Enter key password:
get
Reading from /Users/me/.rsa_values.conf
DEV database_password my_secret_password
my_secret_password
```


Now let's set and get the PROD password:

```
rsa_crypto set -s PROD -o database_password -v super-secret
Using key: /Users/me/Documents/workspaces/khan/rsa_public.pem
PROD super-secret
set
Updated /Users/me/.rsa_values.conf
```

```
rsa_crypto get -s PROD -o database_password
Using key: /Users/me/rsa_key.bin
Opening encrypted key.
Enter key password:
get
Reading from /Users/me/.rsa_values.conf
PROD database_password super-secret
super-secret
```


The content of the `.rsa_values.conf` configuration file will look something like:


```
cat ~/.rsa_values.conf
[DEFAULT]
test = VvXy8NcqL94lBDYS56EnQm03vq9Kvg17VNU1Tu0T1j_hn-OxOTmXv_NoQHWcvWZuJto4awbq1Y_yvi_MKYE5uXOv15iVBZAuHO_xlUmujrL9pdUfxnBe8SAzH7sy2GTx42tLkb2MB9E-49GmKYqbx9dBzTNRDJj8D8LDZku6CJeSDPGy9l6UzG2vl53V3GY97an4Gb4UJ7XYEeEqMsZFRqaxgdWd_IMA_L5FtAlEaU3j4SYvqq-9QDxuab0vv8ZgzP6KuR05jXcLTrEZdrfmy_zRHuLiThu5_-ofsUNoXGNByGWAdBuuMONQj1s2QiI7qsqbFw66RBh0zUMzF2XFtSHY4AklF6uiDkieAhjBldbIjGEhrt3eMVBRBtRIDQ-LlYMcP8HnMPjBe-FBn8rYNscDrOWJIcqyTXwspfnyI6iSjEfTNQilMG6V17NXaJNipbJpoFm0aiKokZXawgav9yWWXAjRitMBtCGbqeEXVw704uY2s2K0m8XQhBLuwtCSS2Q616e4CgBxhEZOHNC0FPDpLWgvUwSFJ9vLphYSEQXeak3GRPDUfzxnjIUi8uLtifJGVEUycyRf8PV_Zf-0i8SAxFbB9OYawAKBpwwTGt4B8Pir351AcID4-s-9TG7LwrOxDvDiGxTH6Kho0SnMubXdpfDESFlwb61KzD3Yap0=

[dev]
test = Nfe5yc-FegHyEODNAX-ndIs8kf6Tjn1V3fjy7PSZ4J4NuOq7bOHCfooVb2mK4KS7Q0U8MSIIo_JmAZVqY__CvWR4zaczr4Es1d64YNX8CyVKvfIK7sPVSfv-v54-edcdtKHEj6dJRo1Pdbvc8ESgMxEUK9J64lS0FloZoXJGE1NVdkgf19IX4ZlHm2XjhyQ1pgfEg0cJPqDukM6cHfXwqexVjWGGF9-eYw6jeUFm59O3_D5Z44ull9HCdEtG85Hv99R4lpQJWYRLF1b7-HPPnyAoXwnCuR-mKi7KdiZw4q_bTruuKYltTKIYbMxXzW5m-kjNUcHSaYdOxSGVbOYdhMiBOnvTRZS5KVVpJCfS5fkQG2HLRlkRhW2PWwaG8ieP-bXvK7jvImKqRbGryPNHtdNBSv3yIXhQKqHfs6JxVXg_pBJywv7q-oymxw4hk3jf11CyZaDmAS-XQQU0KxnnkJ7Cm1h1KYVSfFMZWw9teEd3fRsiBktqPaIOnw0U5liK5WG52uBN_hdoAM73aOpsuDLPy1fYEL5Wuw3nuSZt48Gf7q6AFWS8WRCwIXa0oJJjudObfkeCw7jA0-ufIEHa4wBk2X93D2Mjr-nLOSayLM71UOdT94B4-2oVV-44Djuo-iY3iKQQkllFvuQmZr2Ozs68knOA70qbIYewVBcO4fY=

[DEV]
database_password = YrUidTfrK3w-y2KneYUSWugR0IVjmPvBpjqlBZ_5Oic5td0rO2aeWOuyeiujSe7G9YoBnKLxtIkGGzeOs0EQ6kEJCmLCq2MVNOECj4__majFlmp3De_ypebwq0SbRn4UGRzrGSV6oO93jnoHpH8Rky2L5yeJMAqjwsMAgOQBrfdpdcgqLRATUumoaRkvfMafdTYKjhJj5m6EUB9-la8YPK9kxMKu2-l9GlEnqug5S91xAOXb2laX2b3T5KCeQxxAZ2L9KtUG0NJulmaEtUFoRNWSVyBLsAvDdRkXoYXuHLSIhD-8x1RwxOjPyJ-t4cc7uNJF8ZfCsLHuesQj4jauXSmiVe5wI718rC4PS9kYH5Z5IKgl19d7jRaUI2jx-lPs4Rues1SZpHQKpH8GG3Id7z5RAtJ3OdlCrx7b3uOPL5GinlG4QdyiF7ROIsShAZPTdrQybRDDCU8ju-6R0RkMO8Qds7VNRANSwXYQAn2D62IQx3cAr40TMOHy697QgklomfT-k52GCQsfyJqFASYJ4DDhnjZB8uXzx1eHLhmVTikVt1yYXjoPOD0HPX0uYTd8L-TNwU9OnU36Q8m9dTez9rUHrX2xKapkYf0SIRPeSiLRbey_h9tnynoQYXtKsca-jxdBUDZvw2t_KbU__z_zuRWv65CrJpkcBGMvYkqeXj4=

[PROD]
database_password = g1G_zRij0D6nerTHn1bJ7fr_HiWLFv4Qi-a2Y9QfjeWy5lRCO4L_9ENuiG4hbqyJj2NtbLJ7-NCpN3wd_i8djTGcY2yTcgsFZQEceco-n1bK9yX3Fq8Go1r2D82ccdlNSASeFwA5XDEiBbjpDmsgeawYQNJJUC84oAdv52cFIqTVHecYXGp8cr93eUI3Cpj8Q67zoMH3bJNXkF1KIcFCdrlFfwOQA3RsVuoYdw_JXztVAGaUBWfnBKWjDuTcM9WJyB2-Zfw8Pv0W4Dd2YkJvjvMcCJakxoVEz1OGFBlLyBwleTXBQVKLxGBkK7Xfr7s0FArM6yBAe5BFOfd-vfNeoR38X-Rc00ojUTpbsforLKTWuvHGx1tXi8F5b7TAhNKsICptmBn52ZZmYQjCyIktgL_v0Trngk0Y3uYiaAZpFJyvNHcebjSJ445c_knbcFdn158tud9WX8dHOcXcx5LXFrfh-hU1Vc0U6MUVXgja7T_-O5N59Hob4DIyb4sHF8x-FGFiBvZK-dvIY_FDt82Z0Bk-AETPCykdkmtTx4eg-_o2eEb9ewKHlgLpnBjUs1FajMcfGYiQnaRQNfubBRHY34nmdJtfqQVqVIcQkD0N19qI-8Mg0RSwLaxKSDPlK06JdZew1Nrli-l7U5wYZV4zLdIzXG4tqy6qIb_8Y5yMXm0=
```

## Python example

As mentioned, one of the main purposes of this script is to allow automation scripts to securely access secured information.

See the file `example.py` for use as a Python library.


## Releases

MacOS, Linux and Windows self-contained command-line binary versions of this software are available at:

https://github.com/Christophe-Gauge/rsa_crypto/releases/tag/PROD
# Sigmod Fingerprinting
Python implementation of the algorithm defined in [Winnowing: Local Algorithms for Document Fingerprinting](https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf).

## Installation 

```bash 
git clone https://github.com/mattstruble/sigmod-fingerprinting.git
cd sigmod-fingerprinting && python setup.py install
```

## Usage 

```python 
>>> from sigmod_fingerprinting.fingerprint import Fingerprint


>>> fingerprint = Fingerprint(kgram_len=5, window_len=4)
>>> fingerprint.generate("A do run run run, a do run run")
[[639355869, 0], [2552422548, 1], [8796342234, 5], [8796342217, 8], [8728864700, 11], [639355869, 12], [2552422548, 13]]
```

Results are an array of pairs representing [hash, index].

## Variables

The variables that can be passed into the `Fingerprint` class are as follows:

| name | purpose |
| --- | --- |
| kgram_len | Defines the length of kgrams to generate. The example above generates ['adoru', 'dorun', ...] |
| window_len | Defines the size of the window when comparing the kgram hashes for fingerprint selection. The larger the window the fewer fingerprints that are returned. | 
| modulo | The value to modulo the hashes by, defaults to `sys.maxsize`. |
| base | The base in which to use for hashing, defaults to 158 to accomodate all alphanumeric characters uniquely. |
| allow_space | Determines whether the sanitizer will allow spaces in the final kgrams. Defaults to False. |

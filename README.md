# Z-Hunt

website for online version - http://zhunt.bmb.colostate.edu

An algorithm for predicting the propensity of DNA to flip from the B-form to the Z-form.

## Quick Start

```bash
./bin/zhunt
```

## Compiling from Source

Compile using `gcc` compiler:

```bash
make all
```

## Python Code

Within [scripts](https://github.com/Ho-Lab-Colostate/zhunt/tree/master/scripts), zhunt.py is compatible with Python2.7. Future development will make it Python3 compatable. 
After zhunt compilation as described above, create a directory and place the python script with the target .fasta file. 

```python zhunt.py```

A GUI will pop-up for you to select your desired .fasta file as well as a section for your email address (future developmet). Select submit. The run will output a file <yourfilename.fasta.Z-score> that can be read in a text editor or imported into Excel.  

## Authors

* **Shing Ho** - *Initial work* - [original publication](./)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

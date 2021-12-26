# BioTable

**Contents**
1. [Fundamentals](#Fundamentals)
    1. [Python](#Python)
    1. [pandas](#pandas)
1. [Applications](#Applications)
    1. [How to obtain ClinVar variation data in tsv format?](#q1)
    1. [How to convert XML to JSON?](#q2)


## Fundamentals

### Python

If you're new to this, I highly recommend reading books and watching videos. Socratica's video tutorials were extremely helpful to me at first, and I now recommend them to you.

[link](https://www.socratica.com/subject/python)

### pandas

pandas is a powerful tool for data analysis and manipulation. 

This tutorial introduces essentials of pandas and some tips related to processing biological data.

[link](src/pandas_tutorial.ipynb)



## Applications

###  How to obtain ClinVar variation data in tsv format?<a name="q1"></a>

Run in terminal:
```shell
wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/clinvar_variation/ClinVarVariationRelease_00-latest.xml.gz
pypy3 parse_clinvar_v.py clinvar_variation/ClinVarVariationRelease_00-latest.xml.gz True
# or replace pypy to python if you prefer, but Cpython is more time comsuming that ~18 hours are needed
```
after a long wait(~3h), you will get a `.tsv.gz` file.

[link](src/parse_clinvar_v.py)

### How to convert XML to JSON?<a name="q2"></a>

[link](src/clinvar_xml2json.ipynb)

Hi!👋

This is about biological data, especially tabulars which can be processed in Python and pandas in most cases. Some examples are given, I hope there is one that happens to be useful to you.

**Contents**
1. [Fundamentals](#Fundamentals)
    1. [Python](#Python)
    2. [pandas](#pandas)
1. [Applications](#Applications)
    1. [How to obtain ClinVar variation data in tsv format?](#q1)
    2. [How to convert XML to JSON?](#q2)
    3. [How to get OMIM's full data of tsv format?](#q3)


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
# or replace pypy to python if you prefer, but CPython is more time comsuming that ~18 hours are needed
```
After a long wait(~3h), you will get a `.tsv.gz` file.

[link](src/parse_clinvar_v.py)

### How to convert XML to JSON?<a name="q2"></a>

There are many XML files shared by NCBI on its FTP server, but how to convert them quickly to JSON? This is a way, not always the best, but easy.

[link](src/clinvar_xml2json.ipynb)

### How to get OMIM's full data of tsv format?<a name="q3"></a>

`omim` is an open source tool developed by [suqingdong](https://github.com/suqingdong). It provides data from OMIM web and saves in SQLite. Some of the fields are JSON strings and are then flatten as shown in the following link. 

Due to the long wait while updating, the result file will be shared as a [release](https://github.com/chunribu/biotable/releases) to avoid duplication of work.

[link](src/omim_db_full_data_sqlite3_to_tsv.ipynb)

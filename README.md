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
    4. [How to download SRA data from EBI's FTP?](#q4)


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

### How to download SRA data from EBI's FTP?<a name="q4"></a>

国内下载NCBI数据越来越痛苦，因为NCBI数据逐渐迁移到谷歌和亚马逊的云服务。但EBI与NCBI共享数据，EBI仍然直接提供FTP服务，对国内网络相对更加友好。下面我将介绍如何利用aspera（相对）高速和稳定地下载SRA数据。

1. 请保证您已经安装conda。如果没有，请到[这里](https://docs.conda.io/en/latest/miniconda.html)下载安装。
2. 在你的`base`环境中安装aspera-cli。

```shell
conda install -c hcc aspera-cli
```

设置过conda镜像的话，可能会安装失败，可以先暂时把配置文件改名`mv ~/.condarc ~/.condarc_bak`，等安装成功后再改回去即可`mv ~/.condarc_bak ~/.condarc`。

3. 根据Accession下载FTP文件。

```shell
acc="SRR000004"
outdir="./"
ascp -QT -l 300m -P 33001 -i ~/miniconda3/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:vol1/fastq/${acc:0:6}/${acc}/${acc}_1.fastq.gz ${outdir}
ascp -QT -l 300m -P 33001 -i ~/miniconda3/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:vol1/fastq/${acc:0:6}/${acc}/${acc}_2.fastq.gz ${outdir}
```

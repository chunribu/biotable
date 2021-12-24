#!/usr/bin/env python

######################################################################
#  This script is used for parsing and converting ClinVar variation  #
#  dataset in `xml` format to a plain text tabular file.             #
#  Datasets are avilable on NCBI FTP server. Link is below 👇        #
#  https://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/clinvar_variation/   #
#                                         Author: @chunribu[GitHub]  #
######################################################################

from bs4 import BeautifulSoup
# import pandas as pd
import json
import gzip
import sys

def parse_clinvar_v(fgz, save_xml=False):
    with gzip.open(fgz, 'rt') as f:
        fo = gzip.open(fgz+'.tsv.gz', 'at')
        if save_xml:
            fxml = gzip.open(fgz+'.lined_xml.gz', 'at')

        record_count = 0
        raw_record = ''
        writable, write_header = False, True
        for i in f:
            line = i.rstrip('\n').strip()
            if line.startswith('<VariationArchive '):
                writable = True
                record_count += 1
                if record_count % 10000 == 0:
                    print('Parsing record: ', record_count)
            if writable:
                raw_record += line
            if line.startswith('</VariationArchive>'):
                writable = False
                header, record = parse(raw_record)
                if write_header: 
                    fo.write('\t'.join(header)+'\n')
                    write_header = False
                fo.write('\t'.join(['-' if i==None else i for i in record])+'\n')
                if save_xml:
                    fxml.write(raw_record+'\n')
                del header, record
                raw_record = ''
        fo.close()
        if save_xml: fxml.close()
    return record_count
                
def parse(rec):
    soup = BeautifulSoup(rec, 'xml')
    header , record = access_info(soup)
    return header, record

def access_info(soup):
    VariationName = get_attr(soup, 'VariationArchive', 'VariationName')
    RecordStatus = get_text(soup,'InterpretedRecord > ReviewStatus','mono')
    VariationAccession = get_attr(soup, 'VariationArchive', 'Accession')
    Version = get_attr(soup, 'VariationArchive', 'Version')
    Interpretation = get_text(soup, 'Interpretations Interpretation Description', 'poly')
    DateCreated = get_attr(soup, 'VariationArchive', 'DateCreated')
    DateLastUpdated = get_attr(soup, 'VariationArchive', 'DateLastUpdated')
    VariationID = get_attr(soup, 'VariationArchive', 'VariationID')
    VariationType = get_attr(soup, 'VariationArchive', 'VariationType')
    VariantLength = get_attr(soup, 'InterpretedRecord > SimpleAllele > Location > SequenceLocation', 'variantLength')
    CanonicalSPDI = get_text(soup, 'CanonicalSPDI')
    RecordType = get_attr(soup, 'VariationArchive', 'RecordType')
    NumberOfSubmissions = get_attr(soup, 'VariationArchive', 'NumberOfSubmissions')
    NumberOfSubmitters = get_attr(soup, 'VariationArchive', 'NumberOfSubmitters')
    AlleleID = get_attr(soup, 'SimpleAllele', 'AlleleID')
    CytogeneticLocation = get_text(soup, 'InterpretedRecord > SimpleAllele > Location > CytogeneticLocation', 'mono')
    OtherNames = get_text(soup, 'InterpretedRecord > SimpleAllele > OtherNameList > Name', 'poly')
    GeneID = get_attr(soup, 'InterpretedRecord > SimpleAllele > GeneList > Gene', 'GeneID', 'poly')
    GeneFullName = get_attr(soup, 'InterpretedRecord > SimpleAllele > GeneList > Gene', 'FullName', 'poly')
    GeneHGNC_ID = get_attr(soup, 'InterpretedRecord > SimpleAllele > GeneList > Gene', 'HGNC_ID', 'poly')
    GeneRelationshipType = get_attr(soup, 'InterpretedRecord > SimpleAllele > GeneList > Gene', 'RelationshipType', 'poly')
    GeneSymbol = get_attr(soup, 'InterpretedRecord > SimpleAllele > GeneList > Gene', 'Symbol', 'poly')
    GeneSource = get_attr(soup, 'InterpretedRecord > SimpleAllele > GeneList > Gene', 'Source', 'poly')
    SequenceLocation = get_attr(soup, 'InterpretedRecord > SimpleAllele > GeneList > Gene SequenceLocation', method='json')
    Xref = get_attr(soup, 'InterpretedRecord > SimpleAllele > XRefList > XRef', method='json')
    InterpretedCondition = get_text(soup, 'InterpretedRecord ConditionList ElementValue', 'poly')
    RCVAccession = get_attr(soup, 'InterpretedRecord RCVAccession', 'Accession', 'poly')
    RCVAccessionVersion = get_attr(soup, 'InterpretedRecord RCVAccession', 'Version', 'poly')
    Citation = get_text(soup, 'Interpretations Interpretation Citation ID', 'poly')
    ClinicalAssertionInterpretation = get_text(soup, 'ClinicalAssertion Interpretation Description', 'poly')
    ClinicalAssertionReviewStatus = get_text(soup, 'ClinicalAssertion ReviewStatus', 'poly')
    ClinicalAssertionAssertion = get_text(soup, 'ClinicalAssertion Assertion', 'poly')
    ClinicalAssertionMethodType = get_text(soup, 'ClinicalAssertion MethodType', 'poly')
    ClinicalAssertionAlleleOrigin = get_text(soup, 'ClinicalAssertion Sample Origin', 'poly')
    ClinicalAssertionAffectedStatus = get_text(soup, 'ClinicalAssertion Sample AffectedStatus', 'poly')
    ClinicalAssertionCommentOnEvidence = get_text(soup, 'ClinicalAssertion ObservedData Attribute[Type=Description]', 'poly')
    ClinicalAssertionCitation = get_text(soup, 'ClinicalAssertion Citation ID', 'poly')
    ClinicalAssertionSubmitter = get_attr(soup, 'ClinVarAccession ', 'SubmitterName', 'poly')
    ClinicalAssertionSubmission = get_attr(soup, 'ClinicalAssertion ClinVarSubmissionID', 'localKey', 'poly')
    ClinicalAssertionSubmissionAccession = get_attr(soup, 'ClinicalAssertion ClinVarAccession', 'Accession', 'poly')
    ClinicalAssertionSubmissionAccessionVersion = get_attr(soup, 'ClinicalAssertion ClinVarAccession', 'Version', 'poly')
    HGVS_Type = get_attr(soup, 'InterpretedRecord HGVS', 'Type', 'poly')
    HGVS_Assembly = get_attr(soup, 'InterpretedRecord HGVS', 'Assembly', 'poly')
    HGVS_NucleotideExpression = get_text(soup, 'InterpretedRecord HGVS NucleotideExpression Expression', 'poly')
    HGVS_ProteinExpression = get_text(soup, 'InterpretedRecord HGVS', 'poly', 'ProteinExpression Expression')
    MANESelect = get_attr(soup, 'InterpretedRecord HGVS NucleotideExpression', 'MANESelect', 'poly')
    
    names = 'VariationName RecordStatus VariationAccession Version Interpretation DateCreated DateLastUpdated \
VariationID VariationType VariantLength CanonicalSPDI RecordType NumberOfSubmissions NumberOfSubmitters AlleleID \
CytogeneticLocation OtherNames GeneID GeneFullName GeneHGNC_ID GeneRelationshipType GeneSymbol GeneSource SequenceLocation \
Xref InterpretedCondition RCVAccession RCVAccessionVersion Citation ClinicalAssertionInterpretation ClinicalAssertionReviewStatus \
ClinicalAssertionAssertion ClinicalAssertionMethodType ClinicalAssertionAlleleOrigin ClinicalAssertionAffectedStatus \
ClinicalAssertionCommentOnEvidence ClinicalAssertionCitation ClinicalAssertionSubmitter ClinicalAssertionSubmission \
ClinicalAssertionSubmissionAccession ClinicalAssertionSubmissionAccessionVersion HGVS_Type HGVS_Assembly \
HGVS_NucleotideExpression HGVS_ProteinExpression MANESelect'.split()
    values = eval(','.join(names))
    return names, values

def get_text(soup, query, method='mono', second_query=None):
    res = soup.select(query)
    if len(res)==0: return None
    if method=='mono': return res[0].text.strip()
    if method=='poly': 
        if second_query:
            r = [i.select(second_query) for i in res]
            return '|'.join([i[0].text if len(i)==1 else '-' for i in r])
        return '|'.join([i.text.strip() for i in res])
    return None

def get_attr(soup, query, attr='none', method='mono'):
    res = soup.select(query)
    if method=='mono':
        try: return res[0].attrs[attr]
        except: return None
    if method=='poly':
        if len(res)==0:
            return None
        r = []
        for i in res:
            if i.has_attr(attr): 
                r.append(i.attrs[attr])
            else: r.append('-')
        return '|'.join(r)
    if method=='json':
        return json.dumps([i.attrs for i in res])

if __name__ == '__main__':
    if len(sys.argv)==3:
        parse_clinvar_v(sys.argv[1], sys.argv[2])
    else: 
        parse_clinvar_v(sys.argv[1])

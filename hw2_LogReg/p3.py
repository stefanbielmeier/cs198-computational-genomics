#pysam version: 0.17.0
from pysam import VariantFile
import numpy as np
import matplotlib.pyplot as plt

#using pysam to analyze the vcf.gz file, https://pysam.readthedocs.io/en/latest/index.html
#according to https://github.com/pysam-developers/pysam/issues/536, psyam can only use bgzipped vcf files, not gzipped vcf files (like the one provided)

#Resolution:
# 1. gzip -d chr21_filtered_vcf.gz
# 2. Dowload Mac Gui for bgzip / Tabix https://vcf.iobio.io/help.html
# 3. Compress chr21_filtered_vcf with bgzip

vcf_in = VariantFile("chr21_filtered.vcf.gz")  # auto-detect input format
#vcf_out = VariantFile('-', 'w', header=vcf_in.header)

snps = 0
samples = []
allele_frequencies = []
distinct_variant_occurances = 0
allele_counts = []
dbSNPS = []

for rec in vcf_in.fetch():
    #reference is one nucleotide
    allele_frequencies.extend(rec.info["AF"])
    samples.append(rec.info["NS"])
    allele_counts.extend(rec.info["AC"])

    #extract allele genotype data into a list
    genotype_data_list = str(rec).split('\n')[0].split("\t")[9:]
    """
    for combination in genotype_data_list:
        #single distinct variant for both alleles that is not 0
        if combination[0] == "0" and combination[2] == "0":
            #both are zero, do nothing
            pass
        #same variant on both
        elif combination[0] == combination[2] and combination[0] != "0":
            distinct_variant_occurances += 1
        #one or two distinct variants
        elif combination[0] != combination[2]:
            if combination[0] == "0" or combination[2] == "0":
                distinct_variant_occurances += 1
            else: 
                distinct_variant_occurances += 2
        else:
            print("error – unreachable")
            
    """
    #count db_snips
    if rec.id != None:
        dbSNPS.append(rec.id)
    
    #Single nucleotide
    if len(rec.alleles[0]) == 1:
        #alt is one or more single nucleotides (comma separated)
        if max(len(x) for x in rec.alts) == 1:    
            snps += len(rec.alts)

number_of_samples = max(samples)

#_________________________________________
#Problem 3a) Number of single-nucleotide polymorphisms (SNPs)
# results in 190896 SNPS
print("3a) Number of SNPs", snps)

#_________________________________________
#Problem 3b)
#rareish_variants = np.len(np.array(allele_frequencies) < 0.01)
rareish_variants = np.array(allele_frequencies)

"""
Q: How many variants have an allele frequency less than 1%?
"""
print("3b) There are exactly {} variants that have an allele frequency less than 1%".format(len(rareish_variants[rareish_variants < 0.01])))

#_________________________________________
#Problem 3c)
print('3c) number of samples', number_of_samples)
# Number of distinct variants summed over all samples have per variant row / total_number_of_samples
print('3c) The average individual contains approx. {} many distinct variants (occurances)'.format(distinct_variant_occurances / number_of_samples))
print("Check: sum of all ACs didivded by number_of_samples should be >= average distinct variant occurance (above):", sum(allele_counts) / number_of_samples)

#_________________________________________
#Problem 3d)
print("3d) A dbSNP is a known SNP / genetic variation in the free public archive for known genetic variations for different species by National Center for Biotechnology Information (NCBI). \n It has an rs number, e.g. rs328 which is without clinical significance (C => (A, G))")
print("3d) Number of variants in VCF file with dbSNP ID: {}".format(len(dbSNPS)))
print("No variant has an entry in the ID column. All ID column entries put in a list:", dbSNPS)

#_________________________________________
#Problem 3e)
print("3e) A Phred quality score is a measure of the quality of the identification of the nucleobases generated by automated DNA sequencing")
print("3e) With a Phred score of 45, what is the error probability? P = 10^(-45/10) = 0.0000316227766. The accuracy is thus 1-P, which is 99.99683772")


#_________________________________________
#Problem 3b) – PLOT at the end...
plt.hist(allele_frequencies, 10)
plt.ylabel('Number of variants with allele frequency')
plt.xlabel('Variant allele frequency')
plt.title('Histogram of variant allele frequencies')
plt.show()


# VCF_SNP_analysis
Compare two vcf files and obtain common or alternate and/or unique to first vcf file or/and unique to second vcf file snp positions with respect to the reference sequence.

## Requirement:
python v2.7.6+
natsort module for python

## Usage:
```
python get_alternate_common_snps.py [-h] [-1 VCF1] [-2 VCF2] [--common]
                                    [--alternate] [--12] [--21] [--common12]
                                    [--common21] [--alternate12]
                                    [--alternate21] [--homo] [--hetero]
                                    [--out OUTPUT]

Program to get common or alternate SNPs between two VCFs

optional arguments:
  -h, --help            show this help message and exit
  
  -1 VCF1, --vcf1 VCF1  First VCF input file
  -2 VCF2, --vcf2 VCF2  Second VCF input file
  --common              Gets positions with common SNPs
  --alternate           Gets positions with alternate SNPs
  --12                  Gets positions with SNPS in first VCF but not in
                        second
  --21                  Gets positions with SNPS in second VCF but not in
                        first
  --common12            Gets positions with SNPs that are common in both VCFs
                        and those that are unique to VCF1
  --common21            Gets positons with SNPs that are common in both VCFs
                        and those that are unique ot VCF2
  --alternate12         Gets positions with SNPs that are alternate in both
                        VCFs and those that are unique to VCF1
  --alternate21         Gets positions with SNPs that are alternate in both
                        VCFs and those that are unique to VCF2
  --homo                Consider only the homozygous SNPs
  --hetero              Consider only the heterozygous SNPs
  --out OUTPUT          Output file name

```
### Finds positions where alternate snps are different
python get_alternate_common_snps.py --vcf1 VCF1.vcf -2 VCF2.vcf --alternate

### Finds positions where alternate snps are different and are heterozygous
python get_alternate_common_snps.py --vcf1 VCF1.vcf -2 VCF2.vcf --alternate --hetero

### Finds positions where alternate snps are common
python get_alternate_common_snps.py --vcf1 VCF1.vcf -2 VCF2.vcf --common

### Finds positions where alternate snps are common and are homozygous
python get_alternate_common_snps.py --vcf1 VCF1.vcf -2 VCF2.vcf --common --homo

### Finds positions in VCF1 that are not present in VCF2
python get_alternate_common_snps.py --vcf1 VCF1.vcf -2 VCF2.vcf --12

### Finds positions in VCF2 that are not present in VCF1
python get_alternate_common_snps.py --vcf1 VCF1.vcf -2 VCF2.vcf --21


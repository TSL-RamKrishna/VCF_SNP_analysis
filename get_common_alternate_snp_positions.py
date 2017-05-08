#!/usr/bin/env python

import os, sys
import argparse
from natsort import natsorted

Description="Program to get common or alternate SNPs between two VCFs"
usage="""
python {script} --vcf1 VCF1.vcf -2 VCF2.vcf --alternate #finds positions where alternate snps are different
python {script} --vcf1 VCF1.vcf -2 VCF2.vcf --common    #finds positions where alternate snps are common
python {script} --vcf1 VCF1.vcf -2 VCF2.vcf --12        #finds positions in VCF1 that are not present in VCF2
python {script} --vcf1 VCF1.vcf -2 VCF2.vcf --21        #finds positions in VCF2 that are not present in VCF1
python {script} --vcf1 VCF1.vcf -2 VCF2.vcf --common12
python {script} --vcf1 VCF1.vcf -2 VCF2.vcf --common21
python {script} --vcf1 VCF1.vcf -2 VCF2.vcf --alternate12
python {script} --vcf1 VCF1.vcf -2 VCF2.vcf --alternate21
""".format(script=sys.argv[0])

parser=argparse.ArgumentParser(description=Description, epilog=usage)
parser.add_argument("-1", "--vcf1", action="store", dest="vcf1", help="First VCF input file")
parser.add_argument("-2", "--vcf2", action="store", dest="vcf2", help="Second VCF input file")
parser.add_argument("--common", action="store_true", dest="common", help="Gets positions with common SNPs")
parser.add_argument("--alternate", action="store_true", dest="alternate", help="Gets positions with alternate SNPs")
parser.add_argument("--12", action="store_true", dest="onetwo", help="Gets positions with SNPS in first VCF but not in second")
parser.add_argument("--21", action="store_true", dest="twoone", help="Gets positions with SNPS in second VCF but not in first")
parser.add_argument("--common12", action="store_true", dest="common12", help="Gets positions with SNPs that are common in both VCFs and those that are unique to VCF1")
parser.add_argument("--common21", action="store_true", dest="common21", help="Gets positons with SNPs that are common in both VCFs and those that are unique ot VCF2")
parser.add_argument("--alternate12", action="store_true", dest="alternate12", help="Gets positions with SNPs that are alternate in both VCFs and those that are unique to VCF1")
parser.add_argument("--alternate21", action="store_true", dest="alternate21", help="Gets positions with SNPs that are alternate in both VCFs and those that are unique to VCF2")
parser.add_argument("--homo", action="store_true", dest="homozygous", help="Consider only the homozygous SNPs")
parser.add_argument("--hetero", action="store_true", dest="heterozygous", help="Consider only the heterozygous SNPs")
parser.add_argument("--out", action="store", dest="output", default="output.txt", help="Output file name")

options=parser.parse_args()


def sort_2_chromosomes(vcf1chr, vcf2chr):
    return natsorted([vcf1chr, vcf2chr])

class get_snps_positions():


    def __init__(self, vcf1, vcf2, mode):

        self.vcf1=vcf1
        self.vcf2=vcf2
        self.mode=mode

    def open_input_files(self):
        self.vcf1fh=open(self.vcf1)
        self.vcf2fh=open(self.vcf2)

    def close_input_files(self):
        self.vcf1fh.close()
        self.vcf2fh.close()

    def read_vcf1_line(self):
        return self.vcf1fh.readline()

    def read_vcf2_line(self):
        return self.vcf2fh.readline()

    def get_line_data(self, line):
        linearray=line.rstrip().split()
        chromosome=linearray[0]
        position=linearray[1]
        ref=linearray[3]
        alt=linearray[4]

        return chromosome, position, ref, alt

    def get_vcf1_linearray(self):

        while True:
            vcf1line=self.read_vcf1_line().rstrip()

            if vcf1line.startswith("#"):
                continue
            elif not vcf1line:
                return None, None, None, None
            elif vcf1line == '':
                continue
            elif options.heterozygous == True:
                if vcf1line.split()[7].split(";")[2] == "HET=1":
                    return self.get_line_data(vcf1line)
                else:
                    continue
            elif options.homozygous == True:
                if vcf1line.split()[7].split(";")[3] == "HOM=1":
                    return self.get_line_data(vcf1line)
                else:
                    continue

            else:
                return self.get_line_data(vcf1line)


    def get_vcf2_linearray(self):
        while True:
            vcf2line=self.read_vcf2_line().rstrip()
            if vcf2line.startswith("#"):
                continue
            elif not vcf2line:
                return None, None, None, None
            elif vcf2line == '':
                continue
            elif options.heterozygous == True:
                if vcf2line.split()[7].split(";")[2] == "HET=1":
                    return self.get_line_data(vcf2line)
                else:
                    continue
            elif options.homozygous == True:
                if vcf2line.split()[7].split(";")[3] == "HOM=1":
                    return self.get_line_data(vcf2line)
                else:
                    continue

            else:
                return self.get_line_data(vcf2line)

    def get_snps_positions(self):
        self.open_input_files()
        vcf1chr, vcf1pos, vcf1ref, vcf1alt = self.get_vcf1_linearray()
        vcf2chr, vcf2pos, vcf2ref, vcf2alt = self.get_vcf2_linearray()

        while True:

            #print vcf1chr, vcf1pos, vcf1alt, vcf2chr, vcf2pos, vcf2alt
            if vcf1chr == None and vcf2chr == None:
                break
            elif vcf1chr and vcf2chr and vcf1chr == vcf2chr:
                if int(vcf1pos) > int(vcf2pos):
                    if self.mode == "twoone" or self.mode == "common21" or self.mode == "alternate21":
                        print vcf2chr + " " + str(vcf2pos) + " " + vcf2ref + " " + vcf2alt
                    vcf2chr, vcf2pos, vcf2ref, vcf2alt = self.get_vcf2_linearray()

                elif int(vcf1pos) == int(vcf2pos):
                    if vcf1alt != vcf2alt and (self.mode == "alternate" or self.mode == "alternate12" or self.mode == "alternate21") :
                        print vcf2chr + " " + str(vcf2pos) + " " + vcf2ref + " " + vcf1alt + " " + vcf2alt
                        #output.write(vcf2chr + " " + str(vcf2pos) + " " + vcf2ref + " " + vcf1alt + " " + vcf2alt + "\n")
                    elif vcf1alt == vcf2alt and (self.mode == "common" or self.mode == "common12" or self.mode == "common21") :
                        print vcf2chr + " " + str(vcf2pos) + " " + vcf2ref + " " + vcf2alt
                        #output.write(vcf2chr + " " + str(vcf2pos) + " " + vcf2ref + " " + vcf1alt + " " + vcf2alt + "\n")

                    else:
                        pass

                    vcf1chr, vcf1pos, vcf1ref, vcf1alt = self.get_vcf1_linearray()
                    vcf2chr, vcf2pos, vcf2ref, vcf2alt = self.get_vcf2_linearray()

                elif int(vcf1pos) < int(vcf2pos):

                    if self.mode == "onetwo" or self.mode == "common12" or self.mode == "alternate12":
                        print vcf1chr + " " + str(vcf1pos) + " " + vcf1ref + " " + vcf1alt
                    vcf1chr, vcf1pos, vcf1ref, vcf1alt = self.get_vcf1_linearray()


            else:
                chr_sorted=sort_2_chromosomes(vcf1chr, vcf2chr)
                #print chr_sorted, vcf1chr, vcf2chr, vcf1pos, vcf1alt, vcf2pos, vcf2alt

                if vcf1chr == None and vcf2chr != None:
                    if self.mode == "twoone" or self.mode=="common21" or self.mode == "alternate21":
                        print vcf2chr + " " + str(vcf2pos) + " " + vcf2ref + " " + vcf2alt
                    vcf2chr, vcf2pos, vcf2ref, vcf2alt = self.get_vcf2_linearray()
                elif vcf1chr != None and vcf2chr == None:
                    if self.mode == "onetwo" or self.mode == "common12" or self.mode == "alternate12":
                        print vcf1chr + " " + str(vcf1pos) + " " + vcf1ref + " " + vcf1alt
                    vcf1chr, vcf1pos, vcf1ref, vcf1alt = self.get_vcf1_linearray()
                elif vcf1chr != None and vcf2chr != None:
                    if vcf1chr == chr_sorted[0]:
                        if self.mode == "onetwo" or self.mode == "common12" or self.mode == "alternate12":
                            print vcf1chr + " " + str(vcf1pos) + " " + vcf1ref + " " + vcf1alt
                        vcf1chr, vcf1pos, vcf1ref, vcf1alt = self.get_vcf1_linearray()
                    elif vcf2chr == chr_sorted[0]:
                        if self.mode == "twoone" or self.mode == "common21" or self.mode == "alternate21":
                            print vcf2chr + " " + str(vcf2pos) + " " + vcf2ref + " " + vcf2alt
                        vcf2chr, vcf2pos, vcf2ref, vcf2alt = self.get_vcf2_linearray()

                else:
                    pass

        self.close_input_files()

if not options.vcf1:
    print "You must supply first VCF file. Use option -1 or --vcf1 to provide first vcf file"
    exit(1)
elif not options.vcf2:
    print "You must supply second VCF file. Use option -2 or --vcf2 to provide second vcf file"
    exit(1)
elif not options.common and not options.alternate and not options.onetwo and not options.twoone and not options.common12 and not options.common21 and not options.alternate12 and not options.alternate21:
    print "You must specify at least one mode. The valid modes are common, alternate, onetwo, twoone, common12, common21, alternate12, alternate21"
    print "Please check the help page using --help option"
    exit(1)
else:
    if options.common == True:
        print "Chromosome Position Ref Alt"
        result = get_snps_positions(options.vcf1, options.vcf2, "common")
    elif options.alternate == True:
        print "Chromosome Position Ref Alt-1 Alt-2"
        result = get_snps_positions(options.vcf1, options.vcf2, "alternate")
    elif options.onetwo == True:
        print "Chromosome Position Ref Alt"
        result= get_snps_positions(options.vcf1, options.vcf2, "onetwo")
    elif options.twoone == True:
        print "Chromosome Position Ref Alt"
        result = get_snps_positions(options.vcf1, options.vcf2, "twoone")
    elif options.common12:
        print "Chromosome Position Ref Alt"
        result = get_snps_positions(options.vcf1, options.vcf2, "common12")
    elif options.common21:
        print "Chromosome Position Ref Alt"
        result = get_snps_positions(options.vcf1, options.vcf2, "common21")
    elif options.alternate12:
        print "Chromosome Position Ref Alt-1 Alt-2"
        result = get_snps_positions(options.vcf1, options.vcf2, "alternate12")
    elif options.alternate21:
        print "Chromosome Position Ref Alt-1 Alt-2"
        result = get_snps_positions(options.vcf1, options.vcf2, "alternate21")
    else:
        pass

    result.get_snps_positions()
    result.close_input_files()

exit(0)

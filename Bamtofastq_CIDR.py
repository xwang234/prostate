#!/usr/bin/python
#SBATCH -t 0-10
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=xwang234@fhcrc.org
#using picard because it orders reads in paired end files 
import sys
sys.path.append('/home/xwang234/python2')
import xlrd
import subprocess
from subprocess import call

#tools and folder settings
java="/app/easybuild/software/Java/1.8.0_92/bin/java"
java_opts="-Xmx2g"
picard_opts1="VALIDATION_STRINGENCY=LENIENT"
picard_opts2="MAX_RECORDS_IN_RAM=1000000"
#picard2.13.2
picard="/fh/fast/stanford_j/Xiaoyu/Tools/picard/build/libs/picard.jar"
bamfolder="/fh/fast/stanford_j/CIDR/CIDR_Seq/05-11-2011/BAM"
outfolder="/fh/fast/stanford_j/Xiaoyu/HPC/data/CIDR"

#read individual,GR_ID info
samplefile="/fh/fast/stanford_j/Xiaoyu/HPC/data/MasterList_PROGRESS_2017OCT03.xlsx"
#open excel file
workbook = xlrd.open_workbook(samplefile)
sheet_names = workbook.sheet_names()
#read the 4th sheet of CIDR info
CIDR_sheet = workbook.sheet_by_name(sheet_names[3])
STUDYID=CIDR_sheet.col_values(0)
#remove none numeric ones
uniq_STUDYID=[x for x in STUDYID if isinstance(x,float)]

#find the unique ids
uniq_STUDYID=set(uniq_STUDYID)
uniq_STUDYID=list(uniq_STUDYID)

RG_IDs=CIDR_sheet.col_values(3)
SM_tags=CIDR_sheet.col_values(4)
#the input entry
i=int(sys.argv[1])
print i
indid=uniq_STUDYID[i]

#check which rows match indid
idxrows=[j for j,x in enumerate(STUDYID) if x==indid]
for idx in idxrows:
	individual=str(SM_tags[idx]) #"200366231@1047560304"
	RG_ID=str(RG_IDs[idx]) #"81BJLABXX_1_CGATGT"
	#bam file
	bam=bamfolder+"/"+individual+".bam"
	#bam2fastq,split based on RG_ID
	command=[java,java_opts,"-jar",picard,"SamToFastq",picard_opts1,picard_opts2,"I="+bam,"F="+outfolder+"/"+individual+"_"+RG_ID+"_1.fastq","F2="+outfolder+"/"+individual+"_"+RG_ID+"_2.fastq","RG_TAG="+RG_ID]
	print command
	call(command)
	#gzip
	command=["gzip",outfolder+"/"+individual+"_"+RG_ID+"_1.fastq"]
	print command
	call(command)
	command=["gzip",outfolder+"/"+individual+"_"+RG_ID+"_2.fastq"]
	print command
	call(command)
	print "done"

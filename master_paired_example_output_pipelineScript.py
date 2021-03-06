
#  Pipeline Script generated by cox1kb on Thu 01/26/17 at 16:57:41.
#  Input files are:
#      tC1_R1.trimmed.fastq  -- a fastq file
#      tC1_R2.trimmed.fastq  -- a fastq file
#  Script commands are:
#      bowtie mouse | -p 8
#      removeN
#      blat mouse | -threads=8
#      blast mouse maxEval=1e-15 | -word_size 24 -num_threads 8
#      blast mouse maxEval=1e-8 | -num_threads 8
#

# generic python modules
import os
import sys

# Arron Lab modules
sys.path.append("/data/aplab/cox1kb/")
from imsa2 import pipelineUtils
from imsa2 import listener

# create a log file for this run
logFile = pipelineUtils.getLogListener()


# Bowtie vs. '/database/bowtie2/index/Mus_musculus/UCSC/mm9/Sequence/BowtieIndex/genome'.  Hits are removed from the read set.
# Bowtie parameters: ' -p 8'
# filter parameters: 'delimiter='#0/', pairedHits=True, pairedMisses=False, printHits1=None, printHits2=None, printMisses1='tC1_R1.trimmed_cmus.temp.fq', printMisses2='tC1_R2.trimmed_cmus.temp.fq''
if not os.path.exists("tC1_R1.trimmed_cmus.bwt"):
    pipelineUtils.runBowtie("tC1_R1.trimmed.fastq", "tC1_R2.trimmed.fastq", "/database/bowtie2/index/Mus_musculus/UCSC/mm9/Sequence/BowtieIndex/genome", "tC1_R1.trimmed_cmus.temp.bwt", " -p 8", "/data/aplab/cox1kb/2017-01-new-mice/tC1", 12, "tC1_R1.trimmed_cmus.bowtieLog.txt", logFile)
    os.rename("tC1_R1.trimmed_cmus.temp.bwt", "tC1_R1.trimmed_cmus.bwt")
if not os.path.exists("tC1_R1.trimmed_cmus.fq"):
    pipelineUtils.filterUsingBowtie("tC1_R1.trimmed.fastq", "tC1_R2.trimmed.fastq", "tC1_R1.trimmed_cmus.bwt", inputType="fastq", delimiter='#0/', pairedHits=True, pairedMisses=False, printHits1=None, printHits2=None, printMisses1='tC1_R1.trimmed_cmus.temp.fq', printMisses2='tC1_R2.trimmed_cmus.temp.fq', divideHalf=False, mylistener=logFile)
    os.rename("tC1_R1.trimmed_cmus.temp.fq", "tC1_R1.trimmed_cmus.fq")

    os.rename("tC1_R2.trimmed_cmus.temp.fq", "tC1_R2.trimmed_cmus.fq")


# combine the two pairs into one file for easier blast/blat alignment and filtering.
if not os.path.exists("tC1_R1.trimmed_cmus.combined.fq"):
    pipelineUtils.combineFiles(["tC1_R1.trimmed_cmus.fq", "tC1_R2.trimmed_cmus.fq"], "tC1_R1.trimmed_cmus.temp.fq")
    os.rename("tC1_R1.trimmed_cmus.temp.fq", "tC1_R1.trimmed_cmus.combined.fq")

# converting FASTQ file 'tC1_R1.trimmed_cmus.combined.fq' to FASTA file 'tC1_R1.trimmed_cmus.combined.fa'
if not os.path.exists("tC1_R1.trimmed_cmus.combined.fa"):
    pipelineUtils.convertToFasta("tC1_R1.trimmed_cmus.combined.fq", "tC1_R1.trimmed_cmus.combined.temp.fa", logFile)
    os.rename("tC1_R1.trimmed_cmus.combined.temp.fa", "tC1_R1.trimmed_cmus.combined.fa")

# removing reads with more than 5 N's from 'tC1_R1.trimmed_cmus.combined.fa' and more than 15 homopolymer repeats to create 'tC1_R1.trimmed_cmus.combined_n5.fa'
if not os.path.exists("tC1_R1.trimmed_cmus.combined_n5.fa"):
    pipelineUtils.removeNs("tC1_R1.trimmed_cmus.combined.fa", "tC1_R1.trimmed_cmus.combined_n5.temp.fa", 5, 15, logFile)
    os.rename("tC1_R1.trimmed_cmus.combined_n5.temp.fa", "tC1_R1.trimmed_cmus.combined_n5.fa")


# BLAT vs. '/database/ncbi/2015/mus_musculus/MusMusculus.2bit'.  Hits are removed from the read set.
# BLAT parameters: ' -threads=8 -minIdentity=80'
# filter parameters: 'minPercent=None, minCoverage=None, minTotalPercent=0.8, delimiter='#0/', pairedHits=True, pairedMisses=False, printHits=None, printMisses='tC1_R1.trimmed_cmus.combined_n5_cmus.temp.fa''
if not os.path.exists("tC1_R1.trimmed_cmus.combined_n5_cmus.psl"):
    pipelineUtils.runBlat("tC1_R1.trimmed_cmus.combined_n5.fa", "/database/ncbi/2015/mus_musculus/MusMusculus.2bit", "tC1_R1.trimmed_cmus.combined_n5_cmus.temp.psl", " -threads=8 -minIdentity=80", "/database/ncbi/2015/mus_musculus/MusMusculus.11.ooc", "/data/aplab/cox1kb/2017-01-new-mice/tC1", 12, "tC1_R1.trimmed_cmus.combined_n5_cmus.blatLog.txt", logFile)
    os.rename("tC1_R1.trimmed_cmus.combined_n5_cmus.temp.psl", "tC1_R1.trimmed_cmus.combined_n5_cmus.psl")
if not os.path.exists("tC1_R1.trimmed_cmus.combined_n5_cmus.fa"):
    pipelineUtils.filterUsingBlat("tC1_R1.trimmed_cmus.combined_n5.fa", "tC1_R1.trimmed_cmus.combined_n5_cmus.psl", minPercent=None, minCoverage=None, minTotalPercent=0.8, delimiter='#0/', pairedHits=True, pairedMisses=False, printHits=None, printMisses='tC1_R1.trimmed_cmus.combined_n5_cmus.temp.fa', divideHalf=False, mylistener=logFile)
    os.rename("tC1_R1.trimmed_cmus.combined_n5_cmus.temp.fa", "tC1_R1.trimmed_cmus.combined_n5_cmus.fa")


# BLAST vs '/database/ncbi/2015/mus_musculus/MusMusculus'.  Hits are removed from the read set.
# BLAST parameters: ' -word_size 24 -num_threads 8 -evalue 1e-15 -max_target_seqs 5'
# Filter paremeters: 'minPercent=None, minLength=None, minNumIds=None, maxEval=1e-15, minBitScore=None, delimiter='#0/', pairedHits=True, pairedMisses=False, printHits=None, printMisses='tC1_R1.trimmed_cmus.combined_n5_cmus_cmus.temp.fa''
if not os.path.exists("tC1_R1.trimmed_cmus.combined_n5_cmus_cmus.bln"):
    pipelineUtils.runBlast("tC1_R1.trimmed_cmus.combined_n5_cmus.fa", "/database/ncbi/2015/mus_musculus/MusMusculus", "tC1_R1.trimmed_cmus.combined_n5_cmus_cmus.temp.bln", " -word_size 24 -num_threads 8 -evalue 1e-15 -max_target_seqs 5", "/data/aplab/cox1kb/2017-01-new-mice/tC1", 12, "tC1_R1.trimmed_cmus.combined_n5_cmus_cmus.blastLog.txt", logFile)
    os.rename("tC1_R1.trimmed_cmus.combined_n5_cmus_cmus.temp.bln", "tC1_R1.trimmed_cmus.combined_n5_cmus_cmus.bln")
if not os.path.exists("tC1_R1.trimmed_cmus.combined_n5_cmus_cmus.fa"):
    pipelineUtils.filterUsingBlast("tC1_R1.trimmed_cmus.combined_n5_cmus.fa", "tC1_R1.trimmed_cmus.combined_n5_cmus_cmus.bln", minPercent=None, minLength=None, minNumIds=None, maxEval=1e-15, minBitScore=None, delimiter='#0/', pairedHits=True, pairedMisses=False, printHits=None, printMisses='tC1_R1.trimmed_cmus.combined_n5_cmus_cmus.temp.fa', mylistener=logFile)
    os.rename("tC1_R1.trimmed_cmus.combined_n5_cmus_cmus.temp.fa", "tC1_R1.trimmed_cmus.combined_n5_cmus_cmus.fa")
    

# BLAST vs '/database/ncbi/2015/mus_musculus/MusMusculus'.  Hits are removed from the read set.
# BLAST parameters: ' -num_threads 8 -evalue 1e-8 -max_target_seqs 5'
# Filter paremeters: 'minPercent=None, minLength=None, minNumIds=None, maxEval=1e-08, minBitScore=None, delimiter='#0/', pairedHits=True, pairedMisses=False, printHits=None, printMisses='tC1_R1.trimmed_cmus.combined_n5_cmus_cmus_cmus.temp.fa''
if not os.path.exists("tC1_R1.trimmed_cmus.combined_n5_cmus_cmus_cmus.bln"):
    pipelineUtils.runBlast("tC1_R1.trimmed_cmus.combined_n5_cmus_cmus.fa", "/database/ncbi/2015/mus_musculus/MusMusculus", "tC1_R1.trimmed_cmus.combined_n5_cmus_cmus_cmus.temp.bln", " -num_threads 8 -evalue 1e-8 -max_target_seqs 5", "/data/aplab/cox1kb/2017-01-new-mice/tC1", 12, "tC1_R1.trimmed_cmus.combined_n5_cmus_cmus_cmus.blastLog.txt", logFile)
    os.rename("tC1_R1.trimmed_cmus.combined_n5_cmus_cmus_cmus.temp.bln", "tC1_R1.trimmed_cmus.combined_n5_cmus_cmus_cmus.bln")
if not os.path.exists("tC1_R1.trimmed_cmus.combined_n5_cmus_cmus_cmus.fa"):
    pipelineUtils.filterUsingBlast("tC1_R1.trimmed_cmus.combined_n5_cmus_cmus.fa", "tC1_R1.trimmed_cmus.combined_n5_cmus_cmus_cmus.bln", minPercent=None, minLength=None, minNumIds=None, maxEval=1e-08, minBitScore=None, delimiter='#0/', pairedHits=True, pairedMisses=False, printHits=None, printMisses='tC1_R1.trimmed_cmus.combined_n5_cmus_cmus_cmus.temp.fa', mylistener=logFile)
    os.rename("tC1_R1.trimmed_cmus.combined_n5_cmus_cmus_cmus.temp.fa", "tC1_R1.trimmed_cmus.combined_n5_cmus_cmus_cmus.fa")
    

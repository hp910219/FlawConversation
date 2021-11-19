args=commandArgs(TRUE)
inputf<-args[1]
outf<-args[2]


library(maftools)
mut_maf <- read.maf(maf=inputf)
pdf(outf)
oncoplot(maf=mut_maf,top=10,showTumorSampleBarcodes=TRUE,SampleNamefontSize=0.6)
dev.off()


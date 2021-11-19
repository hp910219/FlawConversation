##eg:Rscript surv_group.R T1.merge.txt surv_group_result.pdf  class
# install.packages("ggplot2")
# install.packages("survival")
# install.packages("ggpubr")
# install.packages("survminer")

library(ggplot2)
library(survival)
library(ggpubr)
library(survminer)

args=commandArgs(TRUE)
inf<-args[1]
outf<-args[2]
variable<-"class"
matri<-read.table(inf,header=T,sep="\t",quote="",check.names=F,stringsAsFactors=F)
matri$OS[which(matri$OS=="-")]<-0
matri$OS.time[which(matri$OS.time=="-")]<-0
matri$OS<-as.numeric(matri$OS)
matri$OS.time<-as.numeric(matri$OS.time)
res.cox<-survfit(as.formula(paste('Surv(OS.time,OS)~',variable)),data=matri)
gg=ggsurvplot(res.cox,conf.int = F,pval = T,data=matri)
pdf(outf)
print(gg)
dev.off()

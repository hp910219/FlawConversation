##eg:Rscript cox.R  T3.gene.0519.tsv T1.v2.RFI.txt cox.test.gene.tsv merge.gene.tsv
# install.packages("survival")
# install.packages("plyr")

library(survival)
library(plyr)
args=commandArgs(TRUE)
input_data_file=args[1]
input_RFI_file=args[2]
output_file=args[3]
output_merge_file=args[4]
dataX <- read.table(input_data_file,sep="\t",header=T,row.names=1,check.names=F,quote="")
RFI=read.table(input_RFI_file,sep="\t",header=T,row.names=1,check.names=F,quote="")
dataX[dataX[,]>0]=1
data=data.frame(t(dataX))
outdata<-merge(data,RFI,by.x = 0,by.y=0)
outdata2=outdata[,2:ncol(outdata)]
row.names(outdata2)=outdata[,1]

unicox<-function(x){
  print(x)
  FML=as.formula(paste0("Surv(time,cens)~",x))
  coxreg=survdiff(FML,data=outdata2)
  O=coxreg$obs[2]
  E=coxreg$exp[2]
  V=coxreg$var[1,1]
  L=(O-E)/V
  HR=round(exp(L),2)
  pvalue=round((1 - pchisq(coxreg$chisq, length(coxreg$n) -1)),3)
  pvalue_logtest="NA"
  pvalue_waldtest="NA"
  pvalue_sctest="NA"
  CI1=round(exp(L-1.96/sqrt(V)),2)
  CI2=round(exp(L+1.96/sqrt(V)),2)
  coxdata=data.frame('gene'=x,'HR'=HR,'CI1'=CI1,'CI2'=CI2,
                     'pvalue'=pvalue,'logtest'=pvalue_logtest,
                     'waldtest'=pvalue_waldtest,'sctest'=pvalue_sctest)
  return(coxdata)
}
genelist=colnames(outdata2)
out=lapply(genelist, unicox)

out=ldply(out,data.frame)
write.table(out,file=output_file,sep="\t",row.names = TRUE,col.names = NA)
write.table(outdata2,file=output_merge_file,sep="\t",row.names = TRUE,col.names = NA)

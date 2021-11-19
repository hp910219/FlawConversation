##Rscript surv_cox.R exp_file.tsv surv_file.tsv surv_cox_result.tsv time cens
# install.packages("tableone")
# install.packages("survival")
# install.packages("survminer")
# install.packages("forestplot")


library(survival)
library(survminer)
library(forestplot)
library(tableone)
args=commandArgs(TRUE)
exp_file<-args[1]
surv_file<-args[2]
out_file<-args[3]
Time<-args[4]
status<-args[5]

rna<-read.table(exp_file,header=TRUE,row.names=1,sep = "\t",quote = "",stringsAsFactors = F,check.names = F)
clinical<-read.table(surv_file,header=TRUE,sep = "\t",quote = "",stringsAsFactors = F,check.names = F,row.names=1)
data_exp<-rna[,colnames(rna) %in% rownames(clinical)]
data_phe<-clinical[rownames(clinical) %in% colnames(rna),]
data_phe_order<-data_phe[colnames(data_exp),]
colnames(data_phe_order)[which(colnames(data_phe_order)==Time)]<-"Ztime"
colnames(data_phe_order)[which(colnames(data_phe_order)==status)]<-"Zstatus"
mySurv=with(data_phe_order,Surv(Ztime, Zstatus))
identical(colnames(data_exp),rownames(data_phe_order))

cox_2 <-apply(data_exp , 1 , function(gene){
  x=coxph(mySurv ~ log(gene+2) )
  x <- summary(x)
  p.value<-signif(x$wald["pvalue"], digits=2)
  wald.test<-signif(x$wald["test"], digits=2)
  beta<-signif(x$coef[1], digits=2);#coeficient beta
  HR <-signif(x$coef[2], digits=2);#exp(beta)
  HR.confint.lower <- signif(x$conf.int[,"lower .95"], 2)
  HR.confint.upper <- signif(x$conf.int[,"upper .95"],2)
  HRm <- paste0(HR, " (",
                HR.confint.lower, "-", HR.confint.upper, ")")
  res<-c(beta, HR,HR.confint.lower,HR.confint.upper, wald.test, p.value)
  names(res)<-c("beta",'HR','HR.confint.lower','HR.confint.upper', "wald.test",
                "p.value")
  res
})
cox_2=as.data.frame(t(cox_2))
cox_r<-cbind(rownames(cox_2),cox_2)
colnames(cox_r)[1]<-"Gene"
write.table(cox_r,out_file,sep="\t",quote=F,row.names=F)





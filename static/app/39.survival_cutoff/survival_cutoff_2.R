##eg:Rscript survival_cutoff_2.R 207.signature.tsv time cens Sig.6 output_cutoff.tsv
#library(cutoff)
library(survminer)
library(survival)
# # 0. Load some data
# setwd("D:\\postgraduate\\STAD\\Signature")
# mydata <- tmb_h_sig_os
# head(mydata)
args=commandArgs(TRUE)
input_file <- args[1]
time = args[2]
event = args[3]
variables = args[4]
outf =args[5]

mydata <- read.table(file = input_file, header = T, sep = "\t", row.names = 1, check.names = F)
# mydata <- mydata[mydata$`TMB-H` == "TMB-H",]
# 1. Determine the optimal cutpoint of variables
res.cut <- surv_cutpoint(mydata, time = time, event = event, variables = variables)

summary(res.cut)
write.table(summary(res.cut),outf,sep="\t",na=" ",quote=F,col.names=T,row.names=T)

# # 2. Plot cutpoint for IDB
# # palette = "npg" (nature publishing group), see ?ggpubr::ggpar
# plot(res.cut, "Signature.6", palette = "npg")

# # 3. Categorize variables
# res.cat <- surv_categorize(res.cut)
# head(res.cat)
# #write.csv(res.cat,"group_AllType_MUT=.csv",row.names = F)
# 
# # 4. Fit survival curves and visualize
# 
# #res.cat$futime=res.cat$futime/365 
# fit <- survfit(Surv(futime, fustat) ~Signature.1, data = res.cat)
# #pdf(file="prop_IFdel_os.pdf",width=5,height=4.5)
# ggsurvplot(fit, data = res.cat, 
#            risk.table = F, 
#            fun = "pct",
#            size = 1,
#            conf.int = F,
#            palette = c("#BB4444", "#4477AA"),
#            pval = TRUE,
#            legend = c(0.75, 1),     # ?ı?legend??λ??
#            #surv.median.line = "hv",
#            legend.labs = c( "sig1 high","sig1 low"),
#            legend.title = "",
#            xlab="Time (month)")
# dev.off()

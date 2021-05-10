##多组间差异分析：ANOVA,kruskal.test
#eg:Rscript multGroups_diff.R inf_exp.tsv inf_phe.tsv out_anova.tsv

anova<-function(inf_exp,inf_phe,outfile){
  dataExp<-read.table(inf_exp,sep="\t",quote = "",stringsAsFactors = FALSE,check.names=FALSE)
  dataPhe<-read.table(inf_phe,sep="\t",quote = "",stringsAsFactors = FALSE,header = FALSE,check.names=FALSE)
  data<-as.data.frame(t(dataExp))
  data<-cbind(data[,1],dataPhe,data[,2:ncol(data)])
  data_target<-as.data.frame(data[2:nrow(data),])
  colnames(data_target)<-data[1,]
  data_target$group<-as.factor(data_target$group)
  
  l<-list()
  for(k in 3:ncol(data_target)){
    genename=colnames(data_target)[k]
    data_target1<-data_target[,c(1,2,k)]
    colnames(data_target1)[3]<-"TargetGene"
    ##检测是否符合正态分布;由于一组数据如果完全相同会报错，故重新定义函数，如果一组数据完全相同，则会在p_value显示"No significance",只有既符合正态分布又满足方差齐性的数据才能用anova进行分析，其他情况用kruskal.test分析，鉴于该检验没有F_value,故标注“No”
    
    f <- function(x) {
      if (diff(range(x)) == 0) list() else shapiro.test(x)
    }
    nortest<-f(as.numeric(data_target1$TargetGene))
    if(length(nortest)==0){
      F_value="No"
      p_value="No significance" ##所有分组数值相同
      
    }else{
      ##方差齐性检测
      barttest<-bartlett.test(TargetGene~group, data = data_target1)
      if(nortest$p.value>0.05 && barttest$p.value>0.05){
        fit<-aov(TargetGene~group,data = data_target1)
        F_value=summary(fit)[[1]][["F value"]][1]
        p_value=summary(fit)[[1]][["Pr(>F)"]][1]
      }else{
        fit1<-kruskal.test(TargetGene~group, data = data_target1)
        F_value="No"
        p_value=fit1$p.value
      }
    }
    
    l[[k-2]]=c(genename,F_value,p_value)
    }
    
  df = data.frame(l)
  dft = t(df)
  dftf = as.data.frame(dft)
  colnames(dftf)=c("gene","F_value","p_value")
  rownames(dftf)<-1:nrow(dftf)
  merge<-cbind(dataExp[2:nrow(dataExp),],dftf[,2:ncol(dftf)])
  colnames(merge)[1:ncol(dataExp)]<-dataExp[1,]
  
  write.table(merge,outfile,col.names = TRUE,row.names = FALSE,quote=FALSE,sep="\t")
}

args<-commandArgs(TRUE)
inf_exp=args[1]
inf_phe=args[2]
outfile=args[3]

anova(inf_exp,inf_phe,outfile)





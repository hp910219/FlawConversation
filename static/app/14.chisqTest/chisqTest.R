chisqTest<-function(inf,outf){
  #data<-read.table(inf,sep = "\t",quote = "",header = T,stringsAsFactors = F,check.names = F)
  data_inf<-read.table(inf,sep = "\t",quote = "",header = F,stringsAsFactors = F,check.names = F)
  data1<-as.data.frame(t(data_inf))
  data2<-data1[2:nrow(data1),]
  colnames(data2)<-data1[1,]
  rownames(data2)<-1:nrow(data2)
  data<-data2
  result<-c("Gene","Group","groupI_mut","groupI_wt","groupII_mut","groupII_wt","p.value")
  geneN<-colnames(data)
  data[,2:ncol(data)]<-sapply(data[,2:ncol(data)],as.numeric)
  for(i in (2:ncol(data))){
    dataG<-matrix(c(data[1,i],data[2,i],data[3,i],data[4,i]),nrow = 2)
    chisqT<-chisq.test(dataG)
    p.result<-chisqT$p.value
    result_n<-cbind(geneN[i],"groupI vs groupII",data[1,i],data[2,i],data[3,i],data[4,i],p.result)
    result<-rbind(result,result_n)
  }
  write.table(result,outf,sep="\t",quote=F,row.names = F,col.names = F)
  
}

args <- commandArgs(TRUE)
inf<-args[1]
outf<-args[2]

chisqTest(inf,outf)

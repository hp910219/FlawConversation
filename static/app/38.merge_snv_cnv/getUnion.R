args=commandArgs(TRUE)
snvf=args[1]
cnvf=args[2]
mergef=args[3]

data_snv<-read.table(snvf,sep="\t",quote="",check.names=F,stringsAsFactors=F,,header=T)
data_cnv<-read.table(cnvf,sep="\t",quote="",check.names=F,stringsAsFactors=F,,header=T)
colnames(data_snv)[1]="Gene"
colnames(data_cnv)[1]="Gene"
data_snv[is.na(data_snv)]=0
data_cnv[is.na(data_cnv)]=0


getUnion<-function(d1,d2){
  dM=merge(d1,d2,by="Gene",all=T)
  dR1=dM[,1:(ncol(d1))]
  dR2=dM[,c(1,(ncol(d1)+1):ncol(dM))]
  colnames(dR1)=colnames(d1)
  colnames(dR2)=colnames(d2)
  rownames(dR1)=dR1[,1]
  dR1f=dR1[,-1]
  dR1t<-as.data.frame(t(dR1f))
  dR1t=as.data.frame(cbind(rownames(dR1t),dR1t[,]))
  colnames(dR1t)[1]="Sample"
  rownames(dR2)=dR2[,1]
  dR2f=dR2[,-1]
  dR2t<-as.data.frame(t(dR2f))
  dR2t=as.data.frame(cbind(rownames(dR2t),dR2t[,]))
  colnames(dR2t)[1]="Sample"
  dM1=rbind(dR1t,dR2t)
  dM1[is.na(dM1)]=0
  df<-aggregate(dM1[2:ncol(dM1)],by=dM1[1],sum)
  dft=as.data.frame(t(df))
  rownames(dft)[1]="Gene"
  return(dft)
}

dft=getUnion(data_snv,data_cnv)
write.table(dft,mergef,sep="\t",quote=F,col.names=F,row.names=T)


#docker run -it -v /mnt/dechao/hbv/:/data bio_r
#eg:Rscript getFa.R input.tsv out.fasta input_len.tsv


#获取反向互补的序列

args=commandArgs(TRUE)
inf=args[1]
outf=args[2]
outf1=args[3]

library(mgsub)
library(stringi)
dt<-read.table(inf,sep="\t",quote = "",stringsAsFactors = FALSE,check.names=FALSE,comment.char="",header=T)
get_rev<-function(seq){
  complementary_seq= mgsub(seq,c("A","T","G","C","a","g","t","c","N","n","U","u"),c("T","A","C","G","t","c","a","g","N","n","A","a"))
  rev_complementary_seq=stri_reverse(complementary_seq)
  return(rev_complementary_seq)}
d=as.data.frame(get_rev(dt[,2]))
d1=as.data.frame(cbind(dt[,1],d))
colnames(d1)<-c("Name","revCseq")
#生成fasta文件
library(seqinr)
sname=d1[,1]
seq=as.list(d1[,2])
write.fasta(seq,names=sname,file=outf,open="w",nbchar=60,as.string=FALSE)

d1$length<-nchar(d1[,2])
d2=as.data.frame(cbind(d1,dt[,2]))
colnames(d2)[4]<-"ASseq"
write.table(d2,outf1,sep="\t",quote=F,col.names=T,row.names=F)


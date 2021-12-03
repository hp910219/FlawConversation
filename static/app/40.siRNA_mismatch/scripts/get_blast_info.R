library("dplyr")
args<-commandArgs(TRUE)
inf_siRNA<-args[1]
inf_blastall<-args[2]
inf_subject<-args[3]
outf<-args[4]
outf_filter<-args[5]

data_siRNA<-read.table(inf_siRNA,header=T,check.names=F)
data_blast<-read.table(inf_blastall,sep="\t",quote = "",stringsAsFactors = FALSE,check.names=FALSE,comment.char="")
colnames(data_blast)<-c("Name","Subject_id","%_identity","Alignment_length","Mismatches","Gaps","Q.start","Q.end","S.start","S.end","E-value","Score")
data_merge<-merge(data_blast,data_siRNA,by="Name")
data_seq<-read.table(inf_subject,header=T,check.names=F)
data_filter<-data_merge[data_merge[,6]==0,] ##获取没有插入缺失匹配的
data_filter<-data_filter[data_filter[,9]<data_filter[,10],] ##获取正向匹配的序列
##format to all match
data_filter[,9]=data_filter[,9]-data_filter[,7]+1
data_filter[,10]=data_filter[,10]+data_filter[,14]-data_filter[,8]
data_filter[,7]=1
data_filter[,8]=data_filter[,14]
data_filter$subject_target_seq<-substring(data_seq[1,1],data_filter[,9],data_filter[,10]) ##获取匹配的目标序列
data_filter$tag<-paste(data_filter[,1],data_filter[,9],data_filter[,10],sep="_")
data_filter_uniq=dplyr::distinct(data_filter, tag, .keep_all = TRUE)
colnames(data_filter_uniq)[13]<-"siRNA_target_seq"
list_string_diff = function(a, b, exclude = c("-", "?"), ignore.case = TRUE, show.excluded = FALSE, only.position = TRUE){
  if(nchar(a)!=nchar(b)) stop("Lengths of input strings differ")
  if(ignore.case){
    a = toupper(a)
    b = toupper(b)
  }
  
  split_seqs = strsplit(c(a, b), split = "")
  only.diff = split_seqs[[1]] != split_seqs[[2]]
  only.diff[
    (split_seqs[[1]] %in% exclude) |
      (split_seqs[[2]] %in% exclude)
  ] = NA
  
  diff.info = data.frame(which(is.na(only.diff)|only.diff),
                         split_seqs[[1]][only.diff], split_seqs[[2]][only.diff])
  names(diff.info) = c("position", "seq.a", "seq.b")
  
  if(!show.excluded) diff.info = na.omit(diff.info)
  if(only.position){
    diff.info$position
  }else diff.info
}

df=data.frame()
for(i in 1:nrow(data_filter_uniq)){
    a=list_string_diff(data_filter_uniq$siRNA_target_seq[i],data_filter_uniq$subject_target_seq[i],only.position = FALSE)
    if(nrow(a)==0){df1=data_filter_uniq[i,c(1,13,15,9,10,16)]
       df1$mis_type="All-match"
       df=dplyr::bind_rows(df,df1)}
    if(nrow(a)>3){df1=data_filter_uniq[i,c(1,13,15,9,10,16)]
       df1$mis_type=">3mis"
       df=dplyr::bind_rows(df,df1)}
    if(nrow(a)==1 || nrow(a)==2 || nrow(a)==3){
    a$siRNA_site<-(data_filter_uniq[i,"length"]-a[,1]+1)
    a$siRAN_base<-substring(data_filter$ASseq[i],a[,4],a[,4])
    a$target_site<-(data_filter[i,9]+a[,1]-1)
    a$mis<-paste(a$siRNA_site,a$siRAN_base,a$target_site,a$seq.b,sep="_")
    b<-t(a$mis)
    if(ncol(b)==1){colnames(b)=1}
    df1=cbind(data_filter_uniq[i,c(1,13,15,9,10,16)],b)
    if(ncol(b)==1){df1$mis_type=paste("AS",strsplit(df1[,7],"_")[[1]][1],sep=",")}
    if(ncol(b)==2){df1$mis_type=paste("AS",strsplit(df1[,7],"_")[[1]][1],strsplit(df1[,8],"_")[[1]][1],sep=",")}
    if(ncol(b)==3){df1$mis_type=paste("AS",strsplit(df1[,7],"_")[[1]][1],strsplit(df1[,8],"_")[[1]][1],strsplit(df1[,9],"_")[[1]][1],sep=",")}
    
    df=dplyr::bind_rows(df,df1)
  }
}

df_final=df[,-2]
if(ncol(df_final)==6){ colnames(df_final)<-c("Name","AS seq. 5'-3'","Target_Start","Target_End","Target seq. 5'-3'","Mismatch type")}
if(ncol(df_final)==7){df_final1=df_final[,c("Name","ASseq","S.start","S.end","subject_target_seq","mis_type","1")];colnames(df_final1)<-c("Name","AS seq. 5'-3'","Target_Start","Target_End","Target seq. 5'-3'","Mismatch type","1mis")}
if(ncol(df_final)==8){df_final1=df_final[,c("Name","ASseq","S.start","S.end","subject_target_seq","mis_type","1","2")];colnames(df_final1)<-c("Name","AS seq. 5'-3'","Target_Start","Target_End","Target seq. 5'-3'","Mismatch type","1mis","2mis")}
if(ncol(df_final)==9){df_final1=df_final[,c("Name","ASseq","S.start","S.end","subject_target_seq","mis_type","1","2","3")];colnames(df_final1)<-c("Name","AS seq. 5'-3'","Target_Start","Target_End","Target seq. 5'-3'","Mismatch type","1mis","2mis","3mis")}
df_final1[is.na(df_final1)]<-""
write.table(df_final1,outf,sep="\t",quote=F,col.names=T,row.names=F)

##filter
df_final1$tag=ifelse(df_final1[,6]==">3mis",0,1)
data_mark=aggregate(df_final1$tag,df_final1[1],max) #判断序列是否有最佳匹配，无最佳匹配的第二列为0
getseq0=data_mark[data_mark[,2]==0,1] #获取无最佳匹配的序列名
data0=df_final1[df_final1[,1] %in% getseq0,] #获取无最佳匹配的序列信息
data0format=dplyr::distinct(data0, Name, .keep_all = TRUE) #序列去重，只保留一条信息
data0format[3:5]=""
data1=df_final1[!(df_final1[,1] %in% getseq0),] #获取有最佳匹配测序列信息
data1format=data1[data1$tag==1,]
dataMerge=rbind(data1format,data0format) ##合并报出所有的序列

dataMerge=dataMerge[order(dataMerge$Name),] #order
name=table(dataMerge$Name)
name=name[order(names(name))] #order
l=c()
for(i in 1:length(name)){
  if(name[i][[1]] ==1){l=c(l,"")}else{l=c(l,seq(1:name[i][[1]]))}
}
dataM=as.data.frame(cbind(dataMerge,as.data.frame(l)))
#colnames(dataM)[11]="Numb"
dataM$Name_new[dataM$l==""]<-paste(dataM$Name,dataM$l,sep="")
dataM$Name_new[dataM$l!=""]=paste(dataM$Name,dataM$l,sep="_")
dataM_filter=dataM[,c(12,2:9)]
write.table(dataM_filter,outf_filter,sep="\t",quote=F,col.names=T,row.names=F)

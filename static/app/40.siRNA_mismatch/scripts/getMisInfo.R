library("dplyr")
df=data.frame()
for(i in 1:nrow(data_filter)){
  if(data_filter[i,5]==0 ||data_filter[i,5]>3){df=dplyr::bind_rows(df,data_filter[i,c(1,5,15,9,10,17)])
    }else{
     a=list_string_diff(data_filter$siRNA_target_seq[i],data_filter$subject_target_seq[i],only.position = FALSE)
     a$siRNA_site<-(21-a[,1]+1)
     a$siRAN_base<-substring(data_filter$ASseq[i],a[,4],a[,4])
     a$target_site<-(data_filter[i,9]+a[,1]-1)
     a$mis<-paste(a$siRNA_site,a$siRAN_base,a$target_site,a$seq.b,sep="_")
     b<-t(a$mis)
     df1=cbind(data_filter[i,c(1,5,15,9,10,17)],b)  
     df=dplyr::bind_rows(df,df1)
      }
}

library(rpart)
dctree<-function(test_file,output_predict_test_prune,work_dir){
  data<-load(paste(work_dir,"dctree_train.RData",sep="/"))
  train_data<-eval(parse(text=data))
  test_data<-read.table(test_file, sep="\t", header=T,row.names = 1,check.names = F)
  test_data$TMB=apply(test_data,1,sum)/0.47
  test_data$cluster=NA
  test_data=cbind(test_data$cluster,test_data[,-ncol(test_data)])
  colnames(test_data)[1]<-"cluster"
  
  dtree<-rpart(cluster~.,data=train_data,method="class", parms=list(split="information"),
               control = rpart.control(minsplit = 1, minbucket = 1, cp = 0.0001))
 # write.table(dtree$cptable,out_cp_table,col.names = TRUE,row.names = FALSE,sep = "\t",quote=F)
 # printcp(dtree)
  cp_value=0.015
  prune_tree<-prune(dtree,cp=as.numeric(cp_value))

  
  ##using the prune tree to cluster test data
  predtree<-predict(prune_tree,newdata=test_data,type="class") 
  predict_test=data.frame(ID=row.names(test_data),ID2=names(predtree),cluster=test_data$cluster,predtree=predtree)
  predtree_prob<-predict(prune_tree,newdata=test_data,type="prob") 
  data_f=cbind(predict_test[,-c(2,3)],predtree_prob)
  colnames(data_f)[2:5]<-c("cluster","score_S_I","score_S_II","score_S_III")
  write.table(data_f,output_predict_test_prune,sep="\t",quote=F,col.names = T,row.names = F)
#  write.table(data_f,output_predict_test_prune,sep="\t",quote=F,col.names = T,row.names = F)
}

args <- commandArgs(TRUE)
test_file<-args[1]
output_predict_test_prune<-args[2]
work_dir=args[3]
dctree(test_file,output_predict_test_prune,work_dir)



#Rscript dcTree.R 197.v3.txt test.v3.txt train.pd.prune.txt train.pd.nopr.txt test.pd.prune.txt test.pd.nopr.txt tree_nopr.png tree_prune2.png roc_nopr.png roc_prune.png test_roc_nopr.png test_roc_prune.png
library(rpart)
library(rpart.plot)
library(pROC)
dctree<-function(train_file,test_file,output_predict_train_prune,output_predict_train_nopr,output_predict_test_prune,output_predict_test_nopr,tree_nopr_png,tree_prune_png,roc_nopr_png,roc_prune_png,test_roc_nopr_png,test_roc_prune_png){
  train_data<-read.table(train_file, sep="\t", header=T,row.names = 1,check.names = F)
  test_data<-read.table(test_file, sep="\t", header=T,row.names = 1,check.names = F)
  dtree<-rpart(cluster~.,data=train_data,method="class", parms=list(split="information"),
               control = rpart.control(minsplit = 1, minbucket = 1, cp = 0.0001))
  printcp(dtree)
  prune_tree<-prune(dtree,cp=0.015)
  opar<-par(no.readonly = T)
  png(file = tree_nopr_png,width = 3000, height = 2000)
  rpart.plot(dtree,branch=1,type=4,fallen.leaves=T,cex=2, sub="剪枝前")
  dev.off()
  png(file = tree_prune_png,width = 3000, height = 2000)
  rpart.plot(prune_tree,branch=1, type=4,fallen.leaves=T,cex=2, sub="剪枝后")
  par(opar)
  dev.off()
  
  ##using the prune tree to cluster train data
  predtree<-predict(prune_tree,newdata=train_data,type="class")   #利用预测集进行预测table(vdata$cluster0816,predtree,dnn=c("真实值","预测值"))    #输出混淆矩阵
  table(train_data$cluster,predtree,dnn=c("真实值","预测值"))    #输出混淆矩阵table(test_data$等级,pre_xgb,dnn=c("真实值","预测值"))
  xgboost_roc <- roc(train_data$cluster,as.numeric(predtree))
  predtree_prob<-predict(prune_tree,newdata=train_data,type="prob") 
  predict_train=data.frame(ID=row.names(train_data),ID2=names(predtree),cluster=train_data$cluster,predtree=predtree)
  write.table(cbind(predict_train,predtree_prob),output_predict_train_prune,sep="\t",col.names = T,row.names = F)
  #绘制ROC曲线和AUC值
  png(file = roc_prune_png)
  plot(xgboost_roc, print.auc=TRUE, auc.polygon=TRUE, grid=c(0.1, 0.2),
       grid.col=c("green", "red"), max.auc.polygon=TRUE,auc.polygon.col="skyblue", 
       print.thres=TRUE,main='xgboost模型ROC曲线')
  dev.off()
  
  
  ##using the no-prune tree to cluster train data
  predtree<-predict(dtree,newdata=train_data,type="class")   #利用预测集进行预测table(vdata$cluster0816,predtree,dnn=c("真实值","预测值"))    #输出混淆矩阵
  table(train_data$cluster,predtree,dnn=c("真实值","预测值"))    #输出混淆矩阵table(test_data$等级,pre_xgb,dnn=c("真实值","预测值"))
  xgboost_roc <- roc(train_data$cluster,as.numeric(predtree))
  predict_train=data.frame(ID=row.names(train_data),ID2=names(predtree),cluster=train_data$cluster,predtree=predtree)
  write.table(predict_train,output_predict_train_nopr,sep="\t",col.names = T,row.names = F)
  #绘制ROC曲线和AUC值
  png(file = roc_nopr_png)
  plot(xgboost_roc, print.auc=TRUE, auc.polygon=TRUE, grid=c(0.1, 0.2),
       grid.col=c("green", "red"), max.auc.polygon=TRUE,auc.polygon.col="skyblue", 
       print.thres=TRUE,main='xgboost模型ROC曲线')
  dev.off()
  
  
  ##using the prune tree to cluster test data
  predtree<-predict(prune_tree,newdata=test_data,type="class") 
  predict_test=data.frame(ID=row.names(test_data),ID2=names(predtree),cluster=test_data$cluster,predtree=predtree)
  predtree_prob<-predict(prune_tree,newdata=test_data,type="prob") 
  write.table(cbind(predict_test,predtree_prob),output_predict_test_prune,sep="\t",col.names = T,row.names = F)
  table(test_data$cluster,predtree,dnn=c("真实值","预测值")) 
  xgboost_roc <- roc(test_data$cluster,as.numeric(predtree))
  #绘制ROC曲线和AUC值
  png(file = test_roc_prune_png)
  plot(xgboost_roc, print.auc=TRUE, auc.polygon=TRUE, grid=c(0.1, 0.2),
       grid.col=c("green", "red"), max.auc.polygon=TRUE,auc.polygon.col="skyblue", 
       print.thres=TRUE,main='xgboost模型ROC曲线')
  dev.off()
  
  
  ##using the no-prune tree to cluster test data
  predtree<-predict(dtree,newdata=test_data,type="class") 
  predict_test=data.frame(ID=names(predtree),predtree=predtree)
  write.table(predict_test,output_predict_test_nopr,sep="\t",col.names = T,row.names = F)
  table(test_data$cluster,predtree,dnn=c("真实值","预测值")) 
  xgboost_roc <- roc(test_data$cluster,as.numeric(predtree))
  #绘制ROC曲线和AUC值
  png(file = test_roc_nopr_png)
  plot(xgboost_roc, print.auc=TRUE, auc.polygon=TRUE, grid=c(0.1, 0.2),
       grid.col=c("green", "red"), max.auc.polygon=TRUE,auc.polygon.col="skyblue", 
       print.thres=TRUE,main='xgboost模型ROC曲线')
  dev.off()
  
}

args <- commandArgs(TRUE)
train_file<-args[1]
test_file<-args[2]
output_predict_train_prune<-args[3]
output_predict_train_nopr<-args[4]
output_predict_test_prune<-args[5]
output_predict_test_nopr<-args[6]
tree_nopr_png<-args[7]
tree_prune_png<-args[8]
roc_nopr_png<-args[9]
roc_prune_png<-args[10]
test_roc_nopr_png<-args[11]
test_roc_prune_png<-args[12]
dctree(train_file,test_file,output_predict_train_prune,output_predict_train_nopr,output_predict_test_prune,output_predict_test_nopr,tree_nopr_png,tree_prune_png,roc_nopr_png,roc_prune_png,test_roc_nopr_png,test_roc_prune_png)


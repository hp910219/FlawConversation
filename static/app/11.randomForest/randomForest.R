##eg:Rscript randomForest.R 197-G1-G2-G3.txt TCGA_242.txt train_pd.txt test_pd.txt weights.txt output.pdf

library("randomForest")
RandomForest<-function(input1,input2,output_pd_train,output_pd_test,output_weight,output_pdf){
  traindata <- read.table(input1,header=TRUE,check.names = FALSE,stringsAsFactors=FALSE,row.names=1)
  testdata <-  read.table(input2,header=TRUE,check.names = FALSE,stringsAsFactors=FALSE,row.names=1)
  traindata$cluster = as.factor(traindata$cluster)
  testdata$cluster = as.factor(testdata$cluster)
  #d_randomforest <- randomForest(cluster~.,data=traindata,na.action=na.omit,ntree =500,mtry=3,importance=TRUE,proximity=TRUE)
  d_randomforest <- randomForest(cluster~.,data=traindata,na.action=na.omit,ntree =500,mtry=3,importance=TRUE,proximity=TRUE)
  pdf(output_pdf)
  table(predict(d_randomforest),traindata$cluster) #查看频数表
  print(d_randomforest) #查看规则
  hist(treesize(d_randomforest))   #展示随机森林模型中每棵决策树的节点数
  max(treesize(d_randomforest));min(treesize(d_randomforest))
  plot(d_randomforest)  #根据随机森林生成的不同的树绘制误差率
  #展示数据集在二维情况下各类别的具体分布情况
  MDSplot(d_randomforest,traindata$cluster,palette=rep(1,2),pch=as.numeric(traindata$cluster))    
  ####每个变量的重要性 d_randomforest$importance
  weight=importance(d_randomforest)
  write.table(weight, output_weight, sep = "\t", quote = F, row.names = T,col.names = NA)
  varImpPlot(x=d_randomforest,sort=TRUE,n.var=nrow(d_randomforest$importance),main="变量重要性测度散点图")
  barplot(d_randomforest$importance[,1],main="变量重要性测度指标柱形图")
  box()
  
  #####测试
  data.pred=predict(d_randomforest,testdata,type="class")
  pred_out_1<-predict(object=d_randomforest,newdata=testdata,type="prob")  #输出概率
  pred_out_1
  plot(margin(d_randomforest,testdata$cluster),main="观测值被判断正确的概率图")  #可视化 MDSplot(d_randomforest)
  data.pred <- as.vector(data.pred)# 输出预测与观测对应表
  ID <- row.names(testdata)
  pred_result <- data.frame(ID=ID,cluster=data.pred)
  pred_result<-cbind(pred_result,data.frame(pred_out_1),testdata)
  write.table(pred_result, output_pd_test, sep = "\t", quote = F, row.names = F,col.names = T)
  
  
  #####训练集输出
  data.pred=predict(d_randomforest,traindata,type="class")
  #data.pred
  pred_out_1<-predict(object=d_randomforest,newdata=traindata,type="prob")  #输出概率
  
  plot(margin(d_randomforest,testdata$cluster),main="观测值被判断正确的概率图")  #可视化 MDSplot(d_randomforest)
  data.pred <- as.vector(data.pred)# 输出预测与观测对应表
  ID <- row.names(traindata)
  pred_result <- data.frame(ID=ID,cluster=data.pred)
  pred_result2<-cbind(pred_result,data.frame(pred_out_1),traindata)
  write.table(pred_result2, output_pd_train, sep = "\t", quote = F, row.names = F,col.names = T)
  dev.off()
}  

args <- commandArgs(TRUE)
input1<-args[1]
input2<-args[2]
output_pd_train<-args[3]
output_pd_test<-args[4]
output_weight<-args[5]
output_pdf<-args[6]
RandomForest(input1,input2,output_pd_train,output_pd_test,output_weight,output_pdf)

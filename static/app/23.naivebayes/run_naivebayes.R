library(naivebayes)
run_naivebayes<-function(input1,input2,output_train_pd,ouput_test_pd,laplace){
  traindata=read.table(input1,sep = '\t',header=T,row.names=1)
  train=as.matrix(traindata[,-1])
  train[train[,]>0]=1
  y=factor(traindata$cluster)
#  laplace <- 1
  if(is.na(laplace)){laplace=1}
  mnb <- multinomial_naive_bayes(x =train, y = y, laplace = laplace)
  pd_prob_train=predict(mnb, newdata = train, type = "prob")
  pd_class_train=predict(mnb, newdata = train, type = "class")
  pred_train<-cbind(pd_class_train,pd_prob_train,traindata)
  write.table(pred_train,output_train_pd,sep="\t",col.names=NA,row.names=T,quote=F)
  
  
  testdata=read.table(input2,sep = '\t',header=T,row.names=1)
  test=as.matrix(testdata[,-1])
  test[test[,]>0]=1
  y=factor(testdata$cluster)
  pd_prob_test=predict(mnb, newdata = test, type = "prob")
  pd_class_test=predict(mnb, newdata = test, type = "class")
  pred_test<-cbind(pd_class_test,pd_prob_test,testdata)
  write.table(pred_test,output_test_pd,sep="\t",col.names=NA,row.names=T,quote=F)
}

args=commandArgs(TRUE)
input1<-args[1]
input2<-args[2]
output_train_pd<-args[3]
output_test_pd<-args[4]
laplace<-as.numeric(args[5])
run_naivebayes(input1,input2,output_train_pd,ouput_test_pd,laplace)

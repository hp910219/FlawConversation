#eg:Rscript RankGeneCluster.R LUAD.T8.bu.tsv LUAD.T1.tsv key_genes.txt /data/RankGeneCluster/result/ LUAD
args=commandArgs(TRUE)
input_T8_fpkm <-args[1]
input_T1_file <-args[2]
input_gene_file <-args[3]
output_dir<-args[4]
pre_name<-args[5]
# 将循环产生的表写到一个文档中
sink(paste(output_dir,pre_name,".row.log.A.csv",sep=""))

input.gene.A <- read.table(file = input_gene_file,header = T,sep = '\t',quote = '',row.names = 1,check.names = F)
# input.sample <- read.table(file = input_sample_file,header = T,sep = '\t',quote = '',row.names = 1,check.names = F)

# 提取sample以备后用
T8 <- read.table(file = input_T8_fpkm,header = T,sep = '\t',quote = '',row.names = 1,check.names = F)
# T8.A <- T8[,intersect(x = row.names(input.sample),y = colnames(T8))]
T8.A <- T8[intersect(x = rownames(input.gene.A),y = rownames(T8)),]

#### 49个gene热图 ####
## 提取相关gene及sample
for(i in 3:nrow(T8.A)){
  gene.49 <- T8.A[rownames(T8.A)[1:i],]
  
  # 将写出的文件根据不同的序号分别命名
  output_49gene_file <- paste(output_dir,pre_name,".",i,'.heatmap.pdf',sep = '')
  output_49gene.Pvalue_file <- paste(output_dir,pre_name,".",i,'.gene.Pvalue.tsv',sep = '')
  output_T1_file <- paste(output_dir,pre_name,".",i,'.T1.merge.tsv',sep = '')
  output_survival_file <- paste(output_dir,pre_name,".",i,'.survival.pdf',sep = '')
  
  ## 将其进行可视化
  library(pheatmap)
  gene.49.pmap <- pheatmap(mat = gene.49,
                           border_color = NA,
                           filename = output_49gene_file,
                           width = 8,height = 8,
                           scale = 'row',
                           cluster_rows = F,cluster_cols = T,
                           treeheight_row = 15,treeheight_col = 30,
                           fontsize = 10,fontsize_row = 8,fontsize_col = 2,
                           cutree_cols = 3,  ## 当cluster_cols = F 时，此参数无效
                           clustering_method = 'ward.D2')
  
  ## 将新的到的列顺序放到原来的表中 ##
  T8.A.new <- T8.A[,gene.49.pmap$tree_col$order]
  
  ## 得到排序后的顺序及分类
  gene49.col_cluster <- cutree(gene.49.pmap$tree_col,k = 3)
  gene49.col_cluster <- data.frame(ID = names(gene49.col_cluster), cluster = gene49.col_cluster)
  gene49.col_cluster <- gene49.col_cluster[gene.49.pmap$tree_col$order,]
  gene49.col_cluster.data <- data.frame(cluster = gene49.col_cluster$cluster)
  row.names(gene49.col_cluster.data) <- row.names(gene49.col_cluster)
  
  #### 检测生存状况 ####
  T1 <- read.table(file = input_T1_file,header = T,sep = '\t',quote = '',row.names = 1,check.names = F)
  T1.sample <- T1[row.names(gene49.col_cluster.data),]
  
  ## 得到cluster及T1表后，计算P值
  library(survival)
  library(plyr)
  
  input_data_file <- gene49.col_cluster.data
  input_RFI_file <- T1.sample
  
  dataX <- t(input_data_file)
  RFI <- input_RFI_file
  dataX[dataX[,] == 1] <- 0
  dataX[dataX[,] == 2] <- 1
  data <- data.frame(t(dataX))
  outdata <- merge(data,RFI,by.x = 0,by.y=0)
  outdata2 <- outdata[,2:ncol(outdata)]
  row.names(outdata2) <- outdata[,1]
  
  unicox<-function(x){
    print(x)
    FML=as.formula(paste0("Surv(time,cens)~",x))
    coxreg=survdiff(FML,data=outdata2)
    O=coxreg$obs[2]
    E=coxreg$exp[2]
    V=coxreg$var[1,1]
    L=(O-E)/V
    HR=round(exp(L),2)
    pvalue=round((1 - pchisq(coxreg$chisq, length(coxreg$n) -1)),3)
    pvalue_logtest="NA"
    pvalue_waldtest="NA"
    pvalue_sctest="NA"
    CI1=round(exp(L-1.96/sqrt(V)),2)
    CI2=round(exp(L+1.96/sqrt(V)),2)
    coxdata=data.frame('gene'=x,'HR'=HR,'CI1'=CI1,'CI2'=CI2,
                       'pvalue'=pvalue,'logtest'=pvalue_logtest,
                       'waldtest'=pvalue_waldtest,'sctest'=pvalue_sctest)
    return(coxdata)
  }
  
  genelist <- colnames(outdata2)
  out <- lapply(genelist, unicox)
  
  out <- ldply(out,data.frame)
  table(dataX[1,])
  
  
  for(a in 1:nrow(out)){
    print(paste(i,out[a,1],out[a,2],out[a,3],out[a,4],out[a,5],out[a,6],out[a,7],out[a,8],out[a,9],out[a,10],sep=","))
    print("\n")
  }
  
  write.table(x = out,file = output_49gene.Pvalue_file,sep="\t",row.names = TRUE,col.names = NA)
  write.table(x = outdata2,file = output_T1_file,sep="\t",row.names = TRUE,col.names = NA)
  
  #### 根据已得到的数据看生存 ####
  library(ggplot2)
  library(survival)
  library(ggpubr)
  library(survminer)
  
  res.cox <- survfit(Surv(time,cens)~cluster,  # 创建生存对象
                     data = outdata2)  # 数据集来源
  gg <- ggsurvplot(fit = res.cox,
                   data = outdata2,   #指定变量数据来源
                   pval = T,  # 添加P值
                   surv.median.line = 'hv',  # 添加中位生存时间
                   conf.int = F,  # 显示置信区间
                   risk.table = T,  # 添加风险表
                   legend.title = "", #设置图例标题
                   legend.labs = c("cluster1", "cluster2","cluster3"),  # 指定图例分组标签
                   palette = c(cluster1 = '#3468BB',cluster2 = '#FE0200',cluster3 = "#FAAE01"),
                   break.x.by = 2000,  # 设置x轴刻度间距
                   tables.height = 0.3,  # 设置曲线图下的生存表的高度
                   legend = c(0.85,0.9)  # 指定图例在图中的位置，"top"(默认),"bottom","left","right","none"等
  )
 # ggsave(output_survival_file,plot = print(gg), onefile = F, width = 5, height = 5, units = "in")
  pdf(output_survival_file)
  print(gg)
  dev.off()

}

sink()




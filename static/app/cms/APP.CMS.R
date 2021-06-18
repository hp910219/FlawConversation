
library(pheatmap)
run_cms<-function(input_alterations_file,input_clinic_info_file,output_cms_clustering_figure,output_alterations_pheatmap_figure,output_cms_clustering_tsv){
  alterations <- read.table(file = input_alterations_file,
                            header = T,row.names = 1,check.names = F,sep = '\t')
  clinic_info <- read.table(file = input_clinic_info_file,
                            header = T,row.names = 1,check.names = F,sep = '\t')
  
  
  cor_total <- matrix(data = NA,nrow = ncol(alterations),ncol = ncol(alterations),
                      dimnames = list(colnames(alterations),colnames(alterations)))
  for(i in colnames(alterations)){
    for(j in colnames(alterations)){
      count=length(which(alterations[,i] > 0 & alterations[,j] > 0))
      if(i==j){
        cor_total[i,j]=0
      }
      else{
        cor_total[i,j] = 1/(1+count)
      }
    }
  }
  
  
  # clustering
  ph <- pheatmap(mat = 1-cor_total,
                 color = c('#F5FDF1','#E0F3D8','#CDEAC4','#ACDCB8',
                           '#7BCBC1','#4EB3D3'),
                 #filename = output_cms_clustering_figure,
                 # cellwidth = 12,cellheight = 12,
                 width = 12,height = 12,
                 scale = 'none',
                 cluster_rows = T,cluster_cols = T,
                 #annotation_col = clinic_info,
                 treeheight_row = 0,treeheight_col = 50,
                 fontsize = 3,fontsize_row = 2,fontsize_col = 2,
                 cutree_cols = 3,
                 clustering_distance_cols = as.dist(cor_total),
                 clustering_distance_rows = as.dist(cor_total),
                 clustering_method = 'ward.D2')
  
  col_order<-ph$tree_col$order
  alterations<-alterations[,col_order]
  #write.table(alterations,output_alterations_ordered_tsv,sep="\t",row.names = T,col.names = NA)
  
  col_cluster <- cutree(ph$tree_col,k=3)
  clinic_info$cluster=col_cluster[row.names(clinic_info)]
  write.table(clinic_info,output_cms_clustering_tsv,sep="\t",row.names = T,col.names = NA)
  
  # clustering save to file
  ph <- pheatmap(mat = 1-cor_total,
                 color = c('#F5FDF1','#E0F3D8','#CDEAC4','#ACDCB8',
                           '#7BCBC1','#4EB3D3'),
                 filename = output_cms_clustering_figure,
                 # cellwidth = 12,cellheight = 12,
                 width = 12,height = 12,
                 scale = 'none',
                 cluster_rows = T,cluster_cols = T,
                 annotation_col = clinic_info,
                 treeheight_row = 0,treeheight_col = 50,
                 fontsize = 8,
                 fontsize_row = 4,fontsize_col =4,
                 cutree_cols = 3,
                 clustering_distance_cols = as.dist(cor_total),
                 clustering_distance_rows = as.dist(cor_total),
                 clustering_method = 'ward.D2')
  
  
  ph2 <- pheatmap(mat = alterations,
                  cluster_rows=F,cluster_cols=F,
                  width = 12,height = 12,
                  treeheight_col=50,
                  fontsize_row=4,fontsize_col=4,
                  fontsize=5,
                  scale = "none",
                  clustering_distance_cols = as.dist(data),
                  annotation_col=clinic_info,
                  filename = output_alterations_pheatmap_figure,
                  clustering_method="ward.D2")
}

args=commandArgs(TRUE)
input_alterations_file<-args[1]
input_clinic_info_file<-args[2]
output_cms_clustering_figure<-args[3]
output_alterations_pheatmap_figure<-args[4]
output_cms_clustering_tsv<-args[5]
run_cms(input_alterations_file,input_clinic_info_file,output_cms_clustering_figure,output_alterations_pheatmap_figure,output_cms_clustering_tsv)



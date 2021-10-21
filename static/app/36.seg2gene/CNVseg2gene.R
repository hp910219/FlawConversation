#### 循环 ####
seg2gene<-function(SNP6,gene.69,output_69gene.CNV_file,amp_fold,del_fold){
  #SNP6 <- read.table(file = input_SNP6_file,header = T,sep = "\t",quote = "",check.names = F)
  #gene.69 <- read.table(file = input_gene_file,header = T,sep = "\t",quote = "",row.names = 1,check.names = F)
  
  
  sink(output_69gene.CNV_file)
  cat("sample\tgene\tvalue\n")
  
  for(i in 1:nrow(gene.69)){
    gene <- rownames(gene.69)[i]
    chr <- gene.69[i,1]
    start.1 <- gene.69[i,2]
    end.1 <- gene.69[i,3]
    SNP6.A <- SNP6[SNP6$chr == chr & SNP6$start < start.1 & SNP6$end > end.1 & SNP6$value > amp_fold,] ##Amp.100时用此行代码
    SNP6.B <- SNP6[SNP6$chr == chr & SNP6$start < start.1 & SNP6$end > end.1 & SNP6$value < del_fold,] ##Amp.100时用此行代码
    # SNP6.A <- SNP6[SNP6$chr == chr & SNP6$start < start.1 & SNP6$end > end.1 & SNP6$value < -1,] ##Del.200时用此行代码
    if(nrow(SNP6.A) != 0){
      cat(paste(SNP6.A$sample,gene,"100",sep="\t",collapse = "\n"))
      cat('\n')
      
    }
    
    if(nrow(SNP6.B) != 0){
      cat(paste(SNP6.B$sample,gene,"200",sep="\t",collapse = "\n"))
      # cat(paste(SNP6.A$sample,gene,"200",sep="\t",collapse = "\n"))
      cat('\n')
    }
    
  }
  sink()
}

args<-commandArgs(TRUE)

input_SNP6_file <- args[1]
input_gene_file <- args[2]
output_69gene.CNV_file <- args[3]
amp_fold<-args[4]
del_fold<-args[5]

#input_SNP6_file <- "C:/R/radio/SNP6_nocnv_genomicSegment.txt"
#input_gene_file <- "C:/R/radio/69gene.T4.txt"
#output_69gene.CNV_file <- "C:/R/radio/tmp/69gene.Amp.T4+CNV.tsv"
#amp_fold<-1
#del_fold<--1

SNP6 <- read.table(file = input_SNP6_file,header = T,sep = "\t",quote = "",check.names = F)
gene.69 <- read.table(file = input_gene_file,header = T,sep = "\t",quote = "",row.names = 1,check.names = F)

seg2gene(SNP6,gene.69,output_69gene.CNV_file,amp_fold,del_fold)

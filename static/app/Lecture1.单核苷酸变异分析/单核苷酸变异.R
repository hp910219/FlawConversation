####  T2 to T3  ######
args=commandArgs(TRUE)
input_snv_file <- args[1]
output_snv_file <- args[2]

snv <- read.table(input_snv_file, sep = "\t", header = T, check.names = F, quote = "")
# cnv <- read.table(input_cnv_file, sep = "\t", header = T, check.names = F,quote = "")

# install.packages(plyr)
library(plyr)
## 1.1 filter the variants, keep the meaningful variants
snv_filter <- snv[(snv$effect == "Missense_Mutation" 
                   | snv$effect == "Nonsense_Mutation" 
                   | snv$effect == "Nonstop_Mutation" 
                   | snv$effect == "Frame_Shift_Del" 
                   | snv$effect == "Frame_Shift_Ins" 
                   | snv$effect == "In_Frame_Del"
                   | snv$effect == "In_Frame_Ins" ),]

snv_filter[snv_filter$effect == "Missense_Mutation","DNA_VAF"] = snv_filter[snv_filter$effect == "Missense_Mutation","DNA_VAF"]+10
snv_filter[snv_filter$effect == "In_Frame_Ins","DNA_VAF"] = snv_filter[snv_filter$effect == "In_Frame_Ins","DNA_VAF"]+20
snv_filter[snv_filter$effect == "In_Frame_Del","DNA_VAF"] = snv_filter[snv_filter$effect == "In_Frame_Del","DNA_VAF"]+20
snv_filter[snv_filter$effect == "Nonsense_Mutation","DNA_VAF"] = snv_filter[snv_filter$effect == "Nonsense_Mutation","DNA_VAF"]+40
snv_filter[snv_filter$effect == "Nonstop_Mutation","DNA_VAF"] = snv_filter[snv_filter$effect == "Nonstop_Mutation","DNA_VAF"]+40
snv_filter[snv_filter$effect == "Frame_Shift_Del","DNA_VAF"] = snv_filter[snv_filter$effect == "Frame_Shift_Del","DNA_VAF"]+40
snv_filter[snv_filter$effect == "Frame_Shift_Ins","DNA_VAF"] = snv_filter[snv_filter$effect == "Frame_Shift_Ins","DNA_VAF"]+40
snv_filter[snv_filter$effect == "Splice_Site","DNA_VAF"] = snv_filter[snv_filter$effect == "Splice_Site","DNA_VAF"]+30
snv_filter[snv_filter$effect == "Splice_Region","DNA_VAF"] = snv_filter[snv_filter$effect == "Splice_Region","DNA_VAF"]+0

O <- data.frame(gene = snv_filter$gene, sample = snv_filter$sample, vaf = snv_filter$DNA_VAF)

# 1.2 change to gene-sample matrix
colA <- 1
colB <- 2
colC <- 3
X <- unique(O[,colA])
Y <- unique(O[,colB])
snv_matrix <- matrix(NA, nrow = length(X), ncol = length(Y),  dimnames=list(X,Y))
for (i in 1:nrow(O)){
  source_node = O[i,colA]
  target_node = O[i,colB]
  value = O[i,colC]
  snv_matrix[source_node,target_node] = value
}

write.table(snv_matrix, file = output_snv_file, sep = "\t", quote = FALSE, row.names = TRUE, col.names = NA)

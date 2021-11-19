
args=commandArgs(TRUE)
sample_mut_path=args[1]
outdir=args[2]
BSg_type=args[3]


# install.packages('deconstructSigs')
# install.packages("BSgenome.Hsapiens.UCSC.hg19")
# install.packages("BSgenome.Hsapiens.UCSC.hg38")

library(deconstructSigs)
library(BSgenome.Hsapiens.UCSC.hg19)
library(BSgenome.Hsapiens.UCSC.hg38)

sample.mut.ref <- read.table(sample_mut_path, header=TRUE, sep="\t")
sample.mut.ref$chr<-as.character(sample.mut.ref$chr)
sample.mut.ref$sample<-as.character(sample.mut.ref$sample)
sample.mut.ref$pos<-as.numeric(sample.mut.ref$pos)
setwd(outdir)
if(BSg_type=="BSgenome.Hsapiens.UCSC.hg19"){
              sigs.input<-mut.to.sigs.input(mut.ref=sample.mut.ref, 
                                sample.id="sample",
                                chr="chr",
                                pos="pos",
                                ref="ref",
                                alt="alt",
                                bsg=BSgenome.Hsapiens.UCSC.hg19)}
if(BSg_type=="BSgenome.Hsapiens.UCSC.hg38"){
              sigs.input<-mut.to.sigs.input(mut.ref=sample.mut.ref,
                                sample.id="sample",
                                chr="chr",
                                pos="pos",
                                ref="ref",
                                alt="alt",
                                bsg=BSgenome.Hsapiens.UCSC.hg38)}


sample_id_list = unlist(unique(sample.mut.ref[,1]))
weights_list<-list()

#pdf("out.pdf")
for(i in 1:length(sample_id_list))
{
sample_id<-sample_id_list[[i]]
one_sample = whichSignatures(tumor.ref = sigs.input, 
                           signatures.ref = signatures.cosmic,                      
                           sample.id = sample_id, 
                           contexts.needed = TRUE,
                           tri.counts.method = 'default')
write.table(one_sample$weights, file.path(outdir, paste(sample_id, ".tsv", sep="")), quote = F, row.names = F, col.names = T, sep="\t")

plotSignatures(one_sample, sub = "result")
weights_list[[i]]<-one_sample$weights
i#weights_list<-append(weights_list, one_sample$weights)
makePie(one_sample, sub = "result")
}
weight_data<-Reduce(function(...) rbind(...), weights_list)
write.table(weight_data, file.path(outdir, "weights.tsv"), quote = F, row.names = T, col.names = T, sep="\t")
dev.off()


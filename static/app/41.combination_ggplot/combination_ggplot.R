library(tidyverse)
library(ggpubr) 

args<-commandArgs(TRUE)
inf<-args[1]
outf<-args[2]

MMR<- read.csv(inf)
ggplot(MMR,aes(group,TMB,col=group)) + 
  geom_violin(width=.7)+ 
  geom_jitter(width = .2,alpha=.6)+
  geom_boxplot(width=.1,fill="white") +
  scale_color_brewer(palette = "Set1", guide = "none") +
  # scale_color_manual(values = c("#3468BB","#FE0200"), guide = "none")
  ylab("TMB")+
  xlab("MMR genes")+
  ylim(0,100)+
  theme_classic()+
  stat_compare_means(label = "p.format")

ggsave(filename = outf,width = 5,height = 5)


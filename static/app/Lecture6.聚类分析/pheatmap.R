#### 聚类代码详解 ####
args=commandArgs(TRUE)
input_signature=args[1]
input_zhushitiao=args[2]
output_pdf=args[3]

data <- read.table(file =input_signature ,header = T,sep = "\t",row.names = 1,check.names = F)
data.new <- data[1:15,1:50]
zhushitiao <- read.table(file =input_zhushitiao ,header = T,sep = "\t",row.names = 1,check.names = F)

ann_colors <- list(cluster = c(I = "#3468BB", II = "#FAAE01", III = "#FE0200"),
                   Time = c('#EEEEEE',"CornflowerBlue"))

library(pheatmap)
pmap <- pheatmap(mat = data.new, #载入数据�?
                 filename = output_pdf,

                 #设定颜色
                 color = c("#F7FCF0","#E0F3DB","#CCEBC5","#A8DDB5","#7BCCC4","#4EB3D3","#2B8CBE","#0868AC","#084081"),
                 # color = colorRampPalette(c("SteelBlue","LightYellow","red"))((50)),
                 border_color = NA, #控制每个单元格之间线条，此参数可设置"NA"，或是十六进制颜�?,默认是”grey"

                 # 设定聚类
                 clustering_method = "ward.D2", #参数设定不同聚类方法，默认为“complete",可设定”ward",
                 # "ward.D","ward.D2","single","complete","average","mcquitty","median","centroid"
                 scale = "none", #矩阵是否进行标准化处理，可�?"none","row","column"
                 cluster_rows = F,cluster_col = T, #默认是对行列均进行聚类，可单独设置行或列不进行聚�?
                 treeheight_row = 20,treeheight_col = 20, #控制tree的高度，默认高度�?50.上一行为False时，此参数无�?
                 cutree_cols = 3,
                
                 # 设定图例及字�?
                 # legend = T, #图例，可设置legend = F 不显示图�?,默认为T
                 # display_numbers = T, #在热图格子里展示文本
                 # number_color = "red", #设置格子字体颜色
                 # number_format = "%.1f", #保留小数点后1�?
                 # fontsize = 12,
                 fontsize_row = 8,fontsize_col = 8,

                 # 图的大小
                 # cellwidth = 10,cellheight = 10, #设置单元格大�?
                 width = 10,height = 5,
                 # main = "Pheatmap.test", #设置标题

                 # 注释�?
                 annotation_col = zhushitiao, #参数添加列注释信�?
                 annotaton_legend = T, #去掉注释图例
                 annotation_colors = ann_colors, #设定注释信息颜色
                 )

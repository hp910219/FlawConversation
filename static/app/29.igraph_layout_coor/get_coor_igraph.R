library(igraph)

get_coor<-function(edges,nodes,method){
  g <- graph_from_data_frame(edges, directed=T, vertices=nodes$Herb)
  if(method=="fr"){
    co<-layout_with_fr(g)
  }else if(method=="kk"){
    co<-layout_with_kk(g)
  }else if(method=="dh"){
    co<-layout_with_dh(g)
  }else if(method=="gem"){
    co<-layout_with_gem(g)
  }else if(method=="graphopt"){
    co<-layout_with_graphopt(g)
  }else if(method=="lgl"){
    co<-layout_with_lgl(g)
  }else if(method=="mds"){
    co<-layout_with_mds(g)
  }else if(method=="drl"){
    co<-layout_with_drl(g)
  }else if(method=="star"){
    co<-layout_as_star(g)
  }else if(method=="circle"){
    co<-layout_in_circle(g)
  }else if(method=="nicely"){
    co<-layout_nicely(g)
  }else if(method=="grid"){
    co<-layout_on_grid(g)
  }else if(method=="sphere"){
    co<-layout_on_sphere(g)
  }else if(method=="randomly"){
    co<-layout_randomly(g)
  }
  return(co)
}

args<-commandArgs(TRUE)
input_nodes<-args[1]
input_edges<-args[2]
method<-args[3]
outf<-args[4]

nodes <- read.table(input_nodes, sep = "\t", quote="",header = T,  stringsAsFactors = F,check.names = F,fill = T)
edges <- read.table(input_edges, sep = "\t", row.names = NULL, header = T, fill = T, stringsAsFactors = F)
edges <- edges[edges[, 3] != 0, ]
co<-get_coor(edges,nodes,method)

nodes_final<-cbind(nodes,co)
if(method=="sphere"){
  colnames(nodes_final)[4:6]<-c("x","y","z")
}else{colnames(nodes_final)[4:5]<-c("x","y")}

write.table(nodes_final,outf,row.names = F,col.names = T,sep = "\t",quote = F)



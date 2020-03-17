##Rscript merge_demo.R patient.gene.txt patient  patient.survival.txt 1  output.txt AB
##	patient.gene.txt : inputA
##	patient : the key column of inputA, either column header or column id is OK
##  patient.survival.txt : inputB
##	1 : the key column of inputB, either column header or column id is OK
##	output.txt : output file
##	AB: could be A/B/AB, keep all A or keep all B or keep all AB



args<-commandArgs(TRUE)
inputA=args[1]
colA=args[2]
inputB=args[3]
colB=args[4]
ouputC=args[5]
all=args[6]



if(!is.na(as.numeric(colA))){
	colA=as.numeric(colA)
}	
if(!is.na(as.numeric(colB))){
	colB=as.numeric(colB)
}
print(colA)
print(colB)	

allA=T
allB=F
if(all=="A"){
	allA=T
}else if(all=="B"){
	allB=T
}else if(all=="AB"){
	allA=T
	allB=T
}

A<-read.table(file = inputA, header = T,sep = "\t",stringsAsFactors = F)
B<-read.table(file = inputB, header = T,sep = "\t",stringsAsFactors = F)
outdata<-merge(A,B,by.x = colA,by.y=colB,all.x=allA,all.y=allB)
write.table(outdata,file = ouputC,sep = "\t",row.names = F,quote=F)

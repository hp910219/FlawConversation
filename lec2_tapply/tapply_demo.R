##Rscript tapply_demo.R chengji.txt 1 2 30 output.txt max
##	chengji.txt : inputfile
##	1 : the key column of inputfile, only column id is OK
##  	2 : the start column of inputfile, only column id is OK
##	30 : the end column of inputfile, only column id is OK 
##	output.txt : output file
##      max: the applied method, could be max, min, sum, length, mean, median, sd



args<-commandArgs(TRUE)
inputfile=args[1]
key_col=args[2]
start_col=args[3]
end_col=args[4]
outputfile=args[5]
method=args[6]

if(!is.na(as.numeric(key_col))){
	key_col=as.numeric(key_col)
}	
if(!is.na(as.numeric(start_col))){
	start_col=as.numeric(start_col)
}
if(!is.na(as.numeric(end_col))){
	end_col=as.numeric(end_col)
}


data<-read.table(file=inputfile,header = T,sep = "\t",stringsAsFactors = F)


first_colname<-colnames(data)[start_col]
first<-tapply(data[,start_col],data[,key_col],method)

output<-data.frame(first)
print(row.names(output))
print(colnames(output))
colnames(output)<-c(first_colname)
print(row.names(output))
print(colnames(output))


for (col in c((start_col+1):end_col)) {
    col_name<-colnames(data)[col]
    output[,col_name]<-tapply(data[,col],data[,key_col],method)
}
print(output)
write.table(output,file = outputfile, sep = "\t",row.names = TRUE,col.names = NA,quote=FALSE)

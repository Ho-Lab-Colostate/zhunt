#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
library(ggplot2)

  
x <- scan(args[1], what="", sep="")
df <- t(as.data.frame(matrix(unlist(strsplit(x, "")), nrow = 1, byrow = T)))

nts <- df

df2 <- read.csv(args[2], sep="", skip=1, header=F)

zscore <- df2$V3
zscore <- as.numeric(zscore)

cmb <- data.frame(nts,zscore)

newtable <- table(nts)
t(t(newtable))
plottable <- data.frame(newtable,aggregate(cmb[, 2], list(cmb$nts), mean))

nts_sum <- plottable$nts
nts_sum = factor(nts_sum)
zscore_sum <- plottable$x
count_sum <- plottable$Freq


pdf("NTS_&_Sum_Zscore.pdf")
ggplot(plottable, aes(x = nts_sum)) + 
geom_col(aes(y = zscore_sum), size = 1, color = "darkblue", fill = "white") +   
geom_point(aes(y = 0.01*count_sum), size = 1.5, color="red")+                        
scale_y_continuous(sec.axis=sec_axis(~./0.01,name="Counts"),name="Average Z-score")


pdf("Z-score_across_Sequence.pdf")
barplot(zscore, ylab="Z-score",xlab="Sequence", main="Z-score Across Sequence")
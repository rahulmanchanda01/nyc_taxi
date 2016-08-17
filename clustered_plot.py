#load data
amtrac <- read.csv("C:/Users/../AmtrakPassengersMonthYear.csv")

#create t, tsquare, and factor month

amtrac$t <- seq(1,159)
amtrac$tsquare <- amtrac$t^2
amtrac$monthFactor <- factor(amtrac$Month)

#addlagged variable as a new column
#lag a variable by 1 time unit using package "DataCombine" that should be installed
#install.packages("DataCombine")
#library(DataCombine)

#create a new data frame that will have 'Ridership-1' as an additional column
newLaggedAmtrac <- slide(amtrac, Var = "Ridership", slideBy = -1)
#change name of new column from 'Ridership-1' to lag1Ridership
names(newLaggedAmtrac)[7]<-"lag1Ridership"

#save dataframe in file
write.table(newLaggedAmtrac, file = "C:/Users/rbapna/Dropbox/____msba6250-summer2016/class 3 - forecasting/datasets/laggedAmtrac.csv", sep = ",")
            
#create new training dataframe called 'trnSet' using rows 141 to 159
trnSet<-newLaggedAmtrac[1:140,]

#create new validation dataframe called 'valSet' using rows 141 to 159
valSet<-newLaggedAmtrac[141:159,]

#fit 'full' regression model with lag, seasonality, trend and quadratic trend on training
#use first 140 rows
rTrn2<- lm(Ridership~lag1Ridership+t+tsquare+monthFactor, data=trnSet)
summary(rTrn2)

#predict on training and test set, latter being key
predTrn <- predict(rTrn2, newdata=trnSet )
predTst <- predict(rTrn2, newdata=valSet )

predTrn
predTst

#plot original ridership data
plot(amtrac$t, amtrac$Ridership, type="l")


#plot predcited training set values
yvalauesToDdisplay <- predTrn
xyvalauesToDdisplay <- 1:140
lines(xyvalauesToDdisplay,yvalauesToDdisplay,  type="l" , col="purple" )

#plot predicted test set value
yvalauesToDdisplay <- predTst
xyvalauesToDdisplay <- 141:159
lines(xyvalauesToDdisplay,yvalauesToDdisplay,  type="l" , col="green" )

#compute RMSE
regTrn2.rmse <- sqrt(mean((amtrac$Ridership[141:159]-predTst)^2,  na.rm=TRUE))
regTrn2.rmse
#eureka -- this is a great model -- RMSE is 48!

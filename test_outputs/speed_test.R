library(ggplot2)

df <- read.csv('speed_test.csv')

ggplot(df, aes(x=as.factor(cnt), y=time_avg*1000)) + 
geom_boxplot() + 
theme_minimal() + 
xlab('bulk_endpoint_document_count') +
ylab('average_time_per_document (in ms)') 
ggsave('bulk_speed_per_doc.png', width=4, height=3)


ggplot(df, aes(x=as.factor(cnt), y=time_tot*1000)) + 
geom_boxplot() + 
theme_minimal() + 
xlab('bulk_endpoint_document_count') +
ylab('tot_time (in ms)') 
ggsave('bulk_speed_tot.png', width=4, height=3)


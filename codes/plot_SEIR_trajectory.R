library("ggplot2")

log_path <- args[1]
savefig_path <- args[1]

seir_data <- read.csv(log_path, header = F, sep = ",")

colnames(seir_data) <- c("Susceptible", "Exposed", "Infected", "Recovered")


if (any(seir_data$Exposed) > 0)
{
  p <- ggplot(data=sir_data1, aes(x=1:nrow(seir_data))) + geom_line(y=sir_data1$Susceptible, aes(color="susceptible")) + 
    geom_line(y=sir_data1$Exposed, aes(color="exposed")) + 
    geom_line(y=sir_data1$Infected, aes(color="infected")) + geom_line(y=sir_data1$Recovered, aes(color="recovered")) +
    ylim(0,sum(seir_data[1,])) + labs(x="Generations",y="Inidividuals") +
    ggtitle("SEIR trajectory") +
    scale_color_manual(name='States',
                       breaks=c('susceptible', 'exposed', 'infected', 'recovered'),
                       values=c('susceptible'='steelblue2','exposed'='#FFD700', 'infected'='tomato', 'recovered'='springgreen')) +
    theme_bw() + theme(panel.grid=element_blank())
  picname = "SEIR.png"
} else
{
  p <- ggplot(data=sir_data1, aes(x=1:nrow(seir_data))) + geom_line(y=sir_data1$Susceptible, aes(color="susceptible")) + 
    geom_line(y=sir_data1$Infected, aes(color="infected")) + geom_line(y=sir_data1$Recovered, aes(color="recovered")) +
    ylim(0,sum(seir_data[1,])) + labs(x="Generations",y="Inidividuals") +
    ggtitle("SIR trajectory") +
    scale_color_manual(name='States',
                       breaks=c('susceptible', 'infected', 'recovered'),
                       values=c('susceptible'='steelblue2', 'infected'='tomato', 'recovered'='springgreen')) +
    theme_bw() + theme(panel.grid=element_blank())
  picname = "SIR.png"
}

ggsave(paste0(savefig_path, picname))

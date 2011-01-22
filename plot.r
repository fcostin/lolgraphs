df <- read.csv('data.csv', row.names = 1)

colnames(df) <- c(
	'religion',
	'iq',
	'poverty',
	'murder',
	'theft',
	'divorce',
	'generosity',
	'conservative',
	'health.contentment'
)
# we need to flip this (it was originally defined so that higher values meant less generous...
df$generosity <- max(df$generosity) - df$generosity

library(lattice)
png('us-states.png', width = 800, height = 800)
plot(df, pch = 16)
dev.off()

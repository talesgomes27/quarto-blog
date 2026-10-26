# Reconcile archived aggregates; never load or simulate raw trip records.
suppressPackageStartupMessages({
  library(jsonlite)
  library(ggplot2)
})
args <- commandArgs(trailingOnly = FALSE)
script <- normalizePath(sub('^--file=', '', args[grepl('^--file=', args)]))
root <- dirname(dirname(script))
source <- 'docs/reviews/evidence/bike-share-audit.json'
a <- fromJSON(file.path(root, source), simplifyVector = TRUE)
frozen <- file.path(root, a$source)
stopifnot(identical(digest::digest(file = frozen, algo = 'sha256'), a$sha256))
n <- a$retained_trip_rows
counts <- lapply(a$counts, unlist)
stopifnot(all(vapply(counts, sum, numeric(1)) == n), n == 4335006)
bikes <- data.frame(type = names(counts$bikes), trips = as.numeric(counts$bikes))
bikes$percent <- 100 * bikes$trips / n
member <- a$duration_table[2, ]; casual <- a$duration_table[3, ]
duration <- data.frame(group = c('member', 'casual'), trips = as.numeric(counts$groups[c('member','casual')]),
  mean_minutes = as.numeric(c(member[5], casual[5])),
  q1_minutes = as.numeric(c(member[8], casual[8])),
  median_minutes = as.numeric(c(member[9], casual[9])),
  q3_minutes = as.numeric(c(member[10], casual[10])),
  maximum_minutes = as.numeric(c(member[11], casual[11])))
duration$iqr_minutes <- duration$q3_minutes - duration$q1_minutes
duration$percent <- 100 * duration$trips / n
mean_ratio <- duration$mean_minutes[2] / duration$mean_minutes[1]
median_ratio <- duration$median_minutes[2] / duration$median_minutes[1]
weighted <- weighted.mean(duration$mean_minutes, duration$trips)
stopifnot(round(mean_ratio,2)==2.68, round(median_ratio,2)==1.77, round(weighted,2)==26.97,
          all(duration$q1_minutes < duration$median_minutes), all(duration$median_minutes < duration$q3_minutes))
months <- c('jul','ago','set','out','nov','dez','jan','fev','mar','abr','mai','jun')
monthly <- data.frame(month = c(paste0('2020-',sprintf('%02d',7:12)),paste0('2021-',sprintf('%02d',1:6))),
                      trips = as.numeric(counts$months[months]))
quarter <- data.frame(period = c('2020-Q3','2020-Q4','2021-Q1','2021-Q2'),
                      trips = as.numeric(counts$quarter_labels[c('summer','fall','winter','spring')]))
stopifnot(all(c(sum(monthly$trips), sum(quarter$trips)) == n), monthly$month[which.max(monthly$trips)]=='2021-06')
# Counts transcribed from the same archived group summary; conservation checks bind their denominators.
by_group <- data.frame(group = rep(c('member','casual'), each=3),
  type = rep(c('docked_bike','electric_bike','classic_bike'),2),
  trips = c(1043233,602335,801776,955394,486882,445386))
by_group$percent_within_group <- 100 * by_group$trips / rep(duration$trips,each=3)
weekend <- data.frame(group=c('member','casual'),weekend_trips=c(676393,789897),
                      weekday_trips=c(1770951,1097765))
weekend$percent_within_group <- 100 * weekend$weekend_trips / duration$trips
stopifnot(identical(as.numeric(tapply(by_group$trips,by_group$group,sum)[c('member','casual')]),duration$trips),
          all(weekend$weekend_trips+weekend$weekday_trips == duration$trips),
          sum(weekend$weekend_trips)==counts$weekend['yes'])
out <- file.path(root,'posts/bike-share-navigate/revision-2026-10-26')
dir.create(out, recursive=TRUE,showWarnings=FALSE)
ink <- '#172f3f'; accent <- '#136c65'
base <- theme_minimal(base_size=13) + theme(plot.title=element_text(face='bold',color=ink),
  axis.title=element_text(color=ink), panel.grid.minor=element_blank(),plot.caption=element_text(hjust=0))
files <- character()
for (lang in c('pt','en')) {
  pt <- lang=='pt'
  caption <- if(pt) 'Fonte: agregados arquivados do estudo. Reconciliação de 26/10/2026; sem reexecução dos CSVs.' else
    'Source: archived study aggregates. Reconciled October 26, 2026; raw CSV files were not rerun.'
  p1 <- ggplot(monthly,aes(x=factor(month,levels=month), y=trips/1000))+
    geom_col(fill=accent,width=.72)+labs(title=if(pt)'Viagens por mês no registro arquivado'else'Archived trip counts by month',
      x=if(pt)'Mês de início da viagem'else'Trip start month', y=if(pt)'Viagens (milhares)'else'Trips (thousands)',caption=caption)+base+
    theme(axis.text.x=element_text(angle=45,hjust=1))
  p2 <- ggplot(bikes,aes(x=reorder(type,percent), y=percent))+
    geom_col(fill=accent,width=.6)+coord_flip()+labs(title=if(pt)'Participação dos tipos de bicicleta'else'Share of trips by bicycle type',
      x=NULL,y=if(pt)'Percentual das 4.335.006 viagens (%)'else'Percentage of 4,335,006 trips (%)',caption=caption)+base
  d <- rbind(data.frame(group=duration$group,statistic=if(pt)'Média'else'Mean',minutes=duration$mean_minutes),
             data.frame(group=duration$group,statistic=if(pt)'Mediana'else'Median',minutes=duration$median_minutes))
  d$group <- factor(d$group,levels=c('member','casual'),labels=if(pt)c('Membros','Casuais')else c('Members','Casual'))
  p3 <- ggplot(d,aes(group,minutes,fill=statistic))+geom_col(position='dodge',width=.65)+
    scale_fill_manual(values=c(ink,accent))+labs(title=if(pt)'Médias e medianas de duração por grupo'else'Mean and median trip duration by group',
      x=NULL,y=if(pt)'Duração (minutos por viagem)'else'Duration (minutes per trip)',fill=NULL,caption=caption)+base+
    theme(legend.position='bottom')
  for(name in c('monthly-trips','bike-types','duration-summary')) {
    p <- switch(name,'monthly-trips'=p1,'bike-types'=p2,'duration-summary'=p3)
    filename <- paste0(name,'-',lang,'.png')
    ggsave(file.path(out,filename),p,width=9,height=4.8,dpi=160,bg='white')
    files <- c(files,filename)
  }
}
result <- list(revised='2026-10-26',method='Reconciliation of archived aggregates; raw CSVs and the historical R analysis were not rerun.',
  source=list(audit_json=source,audit_sha256=digest::digest(file=file.path(root,source),algo='sha256'),
    frozen=a$source,frozen_sha256=a$sha256),
  script=list(path='scripts/reconcile_bikeshare.R',sha256=digest::digest(file=script,algo='sha256')),
  versions=list(R=R.version.string,ggplot2=as.character(packageVersion('ggplot2')),jsonlite=as.character(packageVersion('jsonlite'))),
  retained_trip_rows=n,bikes=bikes,duration=duration,monthly=monthly,calendar_quarters=quarter,
  bikes_by_group=by_group,weekend_by_group=weekend,
  weighted_mean_from_rounded_group_means=weighted,mean_ratio=mean_ratio,median_ratio=median_ratio,
  figures=lapply(files,function(f) list(file=f,sha256=digest::digest(file=file.path(out,f),algo='sha256'))))
write_json(result,file.path(out,'results.json'),pretty=TRUE,auto_unbox=TRUE,digits=10)
cat('Reconciled',n,'archived trips; six localized figures; assertions passed.\n')

library("Biostrings")
library("lubridate")
library("parallel")
require("data.table")


args <- commandArgs(trailingOnly = TRUE)
wk_dir <- args[1]
num_samps <- as.integer(args[2])

get_date <- function(current_tick, start_tick, days_per_tick, time_start_tick)
{
  return( (current_tick - start_tick) * days_per_tick + time_start_tick )
}

each_tick_days = 365/120
start_date_sim = get_date(2040, 0, each_tick_days, as.Date("1995-01-01"))
start_sampling_date = as.Date("2012-01-01")

set.seed(123)
sample_csv = fread(file.path(wk_dir, "sample.csv.gz"), header=FALSE, sep=" ", col.names = c("generation", "host_id", "seed_id"))

sample_csv$time = rep(start_date_sim, nrow(sample_csv))
sample_csv[, time:= (sample_csv[,generation] - sample_csv[1,generation]) * (365 / 120) + start_date_sim]

eligible_samps = sample_csv[time>=start_sampling_date]

eligible_samps[,name := paste0(eligible_samps[,generation], ".", eligible_samps[,host_id])]

first_samp_df = eligible_samps[, .SD[1], by = "host_id"]

names2filter_downsampled = sample(first_samp_df[,name], num_samps)

vcf_path = file.path(wk_dir, "sampled_pathogen_sequences.vcf")

vcf <- fread(vcf_path)
new_table = vcf[, ..names2filter_downsampled]

sampled_info_csv = eligible_samps[name %in% names2filter_downsampled]

selected_cols = c(c("POS", "REF", "ALT"), names2filter_downsampled)
new_table = vcf[, ..selected_cols]

row_condition <- apply(new_table[, ..names2filter_downsampled], 1, function(row) all(row == row[1]))
selected_rows <- new_table[row_condition==FALSE, ]


vcf2fasta <- function(vcf_ind, vcf_info)
{
  real_alt = c()
  for (i in 1:nrow(vcf_info))
  {
    alts = strsplit(vcf_info[i,]$ALT, ",")[[1]]
    if (vcf_ind[i]==0)
    {
      real_alt = c(real_alt, vcf_info[i,]$REF)
    }
    else
    {
      real_alt = c(real_alt, alts[vcf_ind[i]])
    }
  }
  return(DNAString(paste(real_alt, collapse="")))
}

vcf_lists = as.list(selected_rows[, ..names2filter_downsampled])

vcf_info_ = selected_rows[, c("POS", "REF", "ALT")]
total_cores <- detectCores()
sampled_genomes <- DNAStringSet(mclapply(vcf_lists, vcf2fasta, vcf_info=vcf_info_, mc.cores = total_cores))
all_names_current = names(sampled_genomes)

write.csv(data.frame(id = 1:nrow(vcf_info_), position = vcf_info_[,"POS"]),
        file.path(wk_dir, "final_samples_snp_pos.csv"), quote=F, row.names=F)

fas_out_path = file.path(wk_dir, "sample.SNPs_only.fasta")

writeXStringSet(sampled_genomes, filepath=fas_out_path, format="fasta", append=TRUE)
write.csv(sampled_info_csv, file.path(wk_dir, "final_samples_info.csv"), quote=F, row.names=F)


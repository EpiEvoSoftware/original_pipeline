library("Biostrings")

args <- commandArgs(trailingOnly = TRUE)
wk_dir <- args[1]  

real_header = as.list(strsplit(readLines(paste0(wk_dir, "samples.merged.modified.vcf"))[1], "\t"))

vcf <- read.table(paste0(wk_dir, "samples.merged.modified.vcf"), sep="\t", col.names=real_header[[1]])
new_table = vcf[,10:ncol(vcf)]

row_condition <- apply(new_table, 1, function(row) all(row == row[1]))
selected_rows <- new_table[row_condition==FALSE, ]

vcf_info_ = vcf[,c("POS", "REF", "ALT")]

vcf_lists <- as.list(selected_rows)
vcf_info_ = vcf_info_[row_condition==FALSE,]

a = ""
for (i in vcf_info_$REF)
{
    a = paste0(a, i)
}
dna_string = DNAString(a)
writeXStringSet(DNAStringSet(dna_string), filepath=paste0(wk_dir, "reference.snpsonly.fasta"), format="fasta")


vcf2fasta <- function(vcf_ind, vcf_info)
{
  # vcf_info_needed <- vcf_info[which(vcf_ind[[1]] != 0),]
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


sampled_genomes <- DNAStringSet(sapply(vcf_lists, vcf2fasta, vcf_info=vcf_info_))

writeXStringSet(sampled_genomes, filepath=paste0(opts$working_directory, "sample.SNPs_only.fasta"), format="fasta")
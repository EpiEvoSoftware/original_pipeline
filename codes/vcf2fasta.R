library("Biostrings")

args <- commandArgs(trailingOnly = TRUE)
wk_dir <- args[1]          ## wk_dir: the working directory (read from command line)
ref_path <- args[2]   ## Reference genome path


ref <- DNAString(paste(readLines(ref_path), collapse=""))

snps_fas <- readBStringSet(paste0(wk_dir, "all_snps.fasta"))


real_header = as.list(strsplit(readLines(paste0(wk_dir, "samples.merged.modified.vcf"))[1], "\t"))

vcf <- read.table(paste0(wk_dir, "samples.merged.modified.vcf"), sep="\t", col.names=real_header[[1]])
vcf_lists <- as.list(vcf[,10:ncol(vcf)])

vcf2fasta <- function(vcf_ind, vcf_info, ref)
{
  # vcf_info_needed <- vcf_info[which(vcf_ind[[1]] != 0),]
  new_fasta = ref
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
  return(replaceLetterAt(ref, vcf_info$POS, letter=real_alt))
}


sampled_genomes <- DNAStringSet(sapply(vcf_lists, vcf2fasta, vcf_info=vcf[,c("POS", "REF", "ALT")], ref=ref))

writeXStringSet(sampled_genomes, filepath=paste0(wk_dir, "sample.fasta"), format="fasta")




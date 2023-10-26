library("optparse")
library("Biostrings")

option_list = list(
  make_option(c("-wk_dir", "--working_directory"), type="character", default="User", help="Working directory", metavar="character"),
  make_option(c("-ref_path", "--ref_path"), type="character", default="User", help="Reference genome path", metavar="character")
)

opts = parse_args(OptionParser(option_list=option_list))

ref <- DNAString(paste(readLines(opts$ref_path), collapse=""))

snps_fas <- readBStringSet(paste0(opts$wk_dir, "all_snps.fasta"))


real_header = as.list(strsplit(readLines(paste0(opts$wk_dir, "samples.merged.modified.vcf"))[1], "\t"))

vcf <- read.table(paste0(opts$wk_dir, "samples.merged.modified.vcf"), sep="\t", col.names=real_header[[1]])
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

writeXStringSet(sampled_genomes, filepath=paste0(opts$wk_dir, "sample.fasta"), format="fasta")




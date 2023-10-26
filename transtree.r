library("ape")
require(data.table)

args <- commandArgs(trailingOnly = TRUE)
wk_dir <- args[1]


configs_file = read.delim(paste0(wk_dir, "/params.config"), header = FALSE, sep = ":")
n_gen = as.integer(configs_file[configs_file$V1=="n_generation",]$V2)


sample_txt <- read.table(paste0(wk_dir, "/final_n_samples.txt"), sep=" ")
colnames(sample_txt) <- c("tick", "sampled_hosts")

recover_txt <- read.table(paste0(wk_dir, "/recovery.renamed.txt"), sep=" ")
colnames(recover_txt) <- c("tick", "recovered_hosts")

infection_txt <- read.table(paste0(wk_dir, "/infection.renamed.txt"), sep=" ")
colnames(infection_txt) <- c("tick", "infector", "infected")



## A function to compress the infection txt and recover txt to only include samples-related information
compress_info <- function(samp, infectors, infecteds, inds_w)
{
  for (i in samp)
  {
    if (i %in% inds_w == F)
    {
      inds_w = c(inds_w, i)
      chain_up = infectors[which(infecteds == i)[1]]
      if (chain_up %in% inds_w == F)
      {
        inds_w = compress_info(chain_up, infectors, infecteds, inds_w)
      }
    }
  }
  return(inds_w)
}



inds_needed <- compress_info(sample_txt$sampled_hosts, infection_txt$infector, infection_txt$infected, c())

recover_txt = recover_txt[recover_txt$recovered_hosts %in% inds_needed,]

infection_txt = infection_txt[(infection_txt$infector %in% inds_needed) & (infection_txt$infected %in% inds_needed),]

tree <- read.tree(paste0(wk_dir, "/seeds.renamed.nwk"))
already_recovered <- c()

#paste_p_2_number <- function(host_number)
#{
#  return(paste0("p", host_number))
#}

decide_host_status <- function(hosts_label, already_recovered_hosts, sample_txt_all, tick_number, infectors_future)
{
  #number_host = as.integer(strsplit(hosts_label, "p")[[1]][2])
  number_host = hosts_label
  if (number_host %in% sample_txt_all$sampled_hosts) ## Sampled, never irrelevent
  {
    if (number_host %in% already_recovered_hosts)
    {
      return("sampled")
    }
    else
    {
      return("alive")
    }
  }
  else
  {
    if (number_host %in% infectors_future)
    {
      return("alive")
    }
    else
    {
      return("irrelevent")
    }
  }
}


already_recovered = c()
# For each generation, Decide whether each host recovers
for (i in 2:n_gen)
{
  print(i)
  ## Host names and states in the last generation
  all_hosts_in_tree = tree$tip.label
  host_status = sapply(all_hosts_in_tree, decide_host_status, already_recovered_hosts=already_recovered, sample_txt_all=sample_txt, tick_number=i, infectors_future=infection_txt[infection_txt$tick>=i-1,]$infector)
  alive_hosts_in_tree = all_hosts_in_tree[which(host_status=="alive")]
  irrelevent_hosts_in_tree = all_hosts_in_tree[which(host_status=="irrelevent")]
  already_recovered = recover_txt[recover_txt$tick<=i-1,]$recovered_hosts
  infection_list = unique(infection_txt[infection_txt$tick==i-1,]$infector)
  infection_lastgen = infection_txt[infection_txt$tick==i-1,]
  
  
  ## For each existing host on the tree, decide if it infected others last generation
  for (j in alive_hosts_in_tree)
  {
    if (j %in% infection_list)
    {
      edge_dt = as.data.frame(tree$edge)
      setDT(edge_dt)
      edge_dt[, edge_idx := as.integer(rownames(edge_dt))]
      tip_dt = data.table(tip_label = tree$tip, 
                          edge_idx = sapply(tree$tip.label, function(tip_label) which.edge(tree, tip_label)))
      tip_dt <- tip_dt[edge_dt, on = .(edge_idx)]
      
      infected_names = infection_lastgen[infection_lastgen$infector==j,]$infected
      if (length(infected_names)==1)
      {
        newtree = read.tree(text = paste0("(", infected_names, ":1);"))
        tree <- bind.tree(tree, newtree, where=tip_dt[tip_dt$tip_label==j]$V2, 0)
        first_infected = infected_names[1]
      }
      else
      {
        c = 0
        first_infected = infected_names[1]
        for (infected_name in infected_names)
        {
          if (c==0)
          {
            newtree = read.tree(text = paste0("(", infected_name, ":1);"))
            tree <- bind.tree(tree, newtree, where=tip_dt[tip_dt$tip_label==j]$V2, 0)
            c = c + 1
          }
          else
          {
            edge_dt = as.data.frame(tree$edge)
            setDT(edge_dt)
            edge_dt[, edge_idx := as.integer(rownames(edge_dt))]
            tip_dt = data.table(tip_label = tree$tip, 
                                edge_idx = sapply(tree$tip.label, function(tip_label) which.edge(tree, tip_label)))
            tip_dt <- tip_dt[edge_dt, on = .(edge_idx)]
            newtree = read.tree(text = paste0("(", infected_name, ":1);"))
            tree <- bind.tree(tree, newtree, where=tip_dt[tip_dt$tip_label==paste0("", first_infected)]$V2, 1)
          }
        }
      }
      # Infected individual added, decide whether the infector recovered
      edge_dt = as.data.frame(tree$edge)
      setDT(edge_dt)
      edge_dt[, edge_idx := as.integer(rownames(edge_dt))]
      tip_dt = data.table(tip_label = tree$tip, 
                          edge_idx = sapply(tree$tip.label, function(tip_label) which.edge(tree, tip_label)))
      tip_dt <- tip_dt[edge_dt, on = .(edge_idx)]
      if (j %in% already_recovered)
      {
        newtree = read.tree(text = paste0("(", j, ":0);"))
        tree <- bind.tree(tree, newtree, where=tip_dt[tip_dt$tip_label==first_infected]$V2, 1)
      }
      else
      {
        newtree = read.tree(text = paste0("(", j, ":1);"))
        tree <- bind.tree(tree, newtree, where=tip_dt[tip_dt$tip_label==first_infected]$V2, 1)
      }
    }
    else
    {
      if (j %in% already_recovered == F)
      {
        edge_dt = as.data.frame(tree$edge)
        setDT(edge_dt)
        edge_dt[, edge_idx := as.integer(rownames(edge_dt))]
        tip_dt = data.table(tip_label = tree$tip, 
                            edge_idx = sapply(tree$tip.label, function(tip_label) which.edge(tree, tip_label)))
        tip_dt <- tip_dt[edge_dt, on = .(edge_idx)]
        newtree = read.tree(text = paste0("(", j, ":1);"))
        tree <- bind.tree(tree, newtree, where=tip_dt[tip_dt$tip_label==j]$V2, 0)
      }
    }
  }
  tree = drop.tip(tree, irrelevent_hosts_in_tree)
}


write.tree(tree, paste0(wk_dir, "/transmission_tree.nwk"))




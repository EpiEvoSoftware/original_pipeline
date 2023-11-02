library("ape")
library("parallel")
require(data.table)


#######################################
## A function to find out hosts' ids that are needed in the transmission tree reconstruction
## Information of the events that doesn't affect the reconstruction of the tree don't need to be processed
compress_info <- function(samp, infectors, infecteds, inds_w)
{
  ## samp is the ids of hosts that are sampled (they are the tips/leaves of the tree)
  ## infectors is the ids of all infectors 
  ## infecteds is the ids of all infecteeds
  ## inds_w stores the ids of hosts that are needed (starting with an empty vector, accumulating through each iteration)
  for (i in samp)
  {
    if (i %in% inds_w == F)
    {
      ## The samples must be included in the <inds_w>, bc they are the leaves/tips
      inds_w = c(inds_w, i)
      ## Find the host who infected the sample, the infector also needs to be included
      chain_up = infectors[which(infecteds == i)[1]]
      if ((is.na(chain_up)==F) & (chain_up %in% inds_w == F))
      {
        ## Iterate the function, but using the infector as "sample" to find the infector of the infector and add it to inds_w
        inds_w = compress_info(chain_up, infectors, infecteds, inds_w)
      }
    }
  }
  ## After iterating over all samples, inds_w should include all individuals needed to reconstruct the tree
  return(inds_w)
}

## A function to find out which seed does the given sample (samp) come from
find_ori <- function(samp, infection)
{
  if (samp %in% infection$infected)
  {
    return(find_ori(infection_txt[infection_txt$infected == samp,]$infector, infection))
  }
  else
  {
    return(samp)
  }
}


## A function to decide at this current tick (generation), what's the state of the given host (hosts_label)
decide_host_status <- function(hosts_label, already_recovered_hosts, sample_txt_all, tick_number, infectors_future)
{
  number_host = hosts_label
  if (number_host %in% sample_txt_all$sampled_hosts) 
  {
    if (number_host %in% already_recovered_hosts) ## Already sampled
    {
      return("sampled")
    }
    else  ## Will be sampled in the future
    {
      return("alive")
    }
  }
  else
  {
    if (number_host %in% infectors_future) ## Never sampled, but will infect others in the future
    {
      return("alive")
    }
    else  ## Never sampled and won't infect others, thus will not play a role in the transmission tree
    {
      return("irrelevent")
    }
  }
}


## A function to reconstruct the transmission tree
reconstruct_tree <- function(n_gen, seeds_id, recover_txt, infection_txt, cores_avail)
{
  ## Starting with a tree with one single leaf (the seed) at the first generation
  tree = read.tree(text = paste0("(", seeds_id, ":1);"))
  ## Filter recover_txt and infection_txt to only include information related to this current seed
  recover_txt = recover_txt[which(sapply(recover_txt$recovered_hosts, find_ori, infection=infection_txt)==seeds_id),]
  infection_txt = infection_txt[which(sapply(infection_txt$infector, find_ori, infection=infection_txt)==seeds_id),]
  
  already_recovered = c()
  # For each generation, Decide whether each host recovers
  for (i in 2:n_gen)
  {
    ## Host names and states in the last generation
    all_hosts_in_tree = tree$tip.label
    host_status = mclapply(all_hosts_in_tree, decide_host_status, already_recovered_hosts=already_recovered, 
                         sample_txt_all=sample_txt, tick_number=i, infectors_future=infection_txt[infection_txt$tick>=i-1,]$infector, 
                         mc.cores=cores_avail)
    alive_hosts_in_tree = all_hosts_in_tree[which(host_status=="alive")]
    irrelevent_hosts_in_tree = all_hosts_in_tree[which(host_status=="irrelevent")]
    already_recovered = recover_txt[recover_txt$tick<=i-1,]$recovered_hosts
    infection_list = unique(infection_txt[infection_txt$tick==i-1,]$infector)
    infection_lastgen = infection_txt[infection_txt$tick==i-1,]
  
  
  ## For each "alive" host on the tree, decide if it infected others last generation
    for (j in alive_hosts_in_tree)
    {
      ## If the alive host is an infector
      if (j %in% infection_list)
      {
        ## Decide the id of each node and edge (not the same as their names in samples)
        edge_dt = as.data.frame(tree$edge)
        setDT(edge_dt)
        edge_dt[, edge_idx := as.integer(rownames(edge_dt))]
        tip_dt = data.table(tip_label = tree$tip, 
                            edge_idx = sapply(tree$tip.label, function(tip_label) which.edge(tree, tip_label)))
        tip_dt <- tip_dt[edge_dt, on = .(edge_idx)]
        
        ## Infecteds of infector j at last generation
        infected_names = infection_lastgen[infection_lastgen$infector==j,]$infected
        ## If there's only one infection event for this infector at last generation
        if (length(infected_names)==1)
        {
          ## Concatenate the new branch to the transmission tree
          newtree = read.tree(text = paste0("(", infected_names, ":1);"))
          tree <- bind.tree(tree, newtree, where=tip_dt[tip_dt$tip_label==j]$V2, 0)
          first_infected = infected_names[1]
        }
        else
        {
          ## Subsequently add each new branch to the transmission tree (they are all added to the first infection event branch)
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
        # New infections' branches added, decide whether the infector recovered
        edge_dt = as.data.frame(tree$edge)
        setDT(edge_dt)
        edge_dt[, edge_idx := as.integer(rownames(edge_dt))]
        tip_dt = data.table(tip_label = tree$tip, 
                            edge_idx = sapply(tree$tip.label, function(tip_label) which.edge(tree, tip_label)))
        tip_dt <- tip_dt[edge_dt, on = .(edge_idx)]
        # If the infector recovers in this generation
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
        ## Not a infector, decide whether it recovers at last generation. If doesn't recover
        if (j %in% already_recovered == F)
        {
          ## Add a pseudobranch (Add a new branch to the former branch, i.e. make the branch 1 unit longer)
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
  return(write.tree(tree))
}

#######################################

args <- commandArgs(trailingOnly = TRUE)
wk_dir <- args[1]          ## wk_dir: the working directory (read from command line)
seeds_tree_path <- args[2]       ## seeds_tree_path, a tree for the phylogeny of the seeds (doesn't necessarily exist)
n_cores <- detectCores()         ## Number of cores that are available

## Read the config file
configs_file = read.delim(paste0(wk_dir, "/params.config"), header = FALSE, sep = ":")
n_gen = as.integer(configs_file[configs_file$V1=="n_generation",]$V2)           ## n_gen: How many generations does the simulation run for

## Read the renamed final samples.txt
sample_txt <- read.table(paste0(wk_dir, "/final_n_samples.txt"), sep=" ")
colnames(sample_txt) <- c("tick", "sampled_hosts")

## Read the renamed final recovery.txt
recover_txt <- read.table(paste0(wk_dir, "/recovery.renamed.txt"), sep=" ")
colnames(recover_txt) <- c("tick", "recovered_hosts")

## Read the renamed final infection.txt
infection_txt <- read.table(paste0(wk_dir, "/infection.renamed.txt"), sep=" ")
colnames(infection_txt) <- c("tick", "infector", "infected")

## Filter the information for <recover_txt> and <infection_txt>, only keep those that will play a role in final tree
inds_needed <- compress_info(sample_txt$sampled_hosts, infection_txt$infector, infection_txt$infected, c())
recover_txt = recover_txt[recover_txt$recovered_hosts %in% inds_needed,]
infection_txt = infection_txt[(infection_txt$infector %in% inds_needed) & (infection_txt$infected %in% inds_needed),]

## Reconstruct transmission tree for each seed
seeds_4_indsw = sapply(inds_needed, find_ori, infection=infection_txt)  ## Find which seed does each tip/sample come from
seeds_id = unique(seeds_4_indsw)        ## The id of seeds
trees_reconstructed <- sapply(seeds_id, reconstruct_tree, n_gen=n_gen, 
                              recover_txt=recover_txt, infection=infection_txt, n_cores)

## Write the .nwk tree file for each transmission tree in a separate file
for (tree_id in 1:length(trees_reconstructed))
{
  write(trees_reconstructed[tree_id], file = paste0(wk_dir, "/transmission_tree/", names(trees_reconstructed)[tree_id], ".nwk"))
}

## If the seeds' phylogeny is provided, we can construct a whole tree
if (file.exists(seeds_tree_path))
{
  seeds_tree <- read.tree(seeds_tree_path)
  for (tree_id in 1:length(trees_reconstructed))
  {
    edge_dt = as.data.frame(seeds_tree$edge)
    setDT(edge_dt)
    edge_dt[, edge_idx := as.integer(rownames(edge_dt))]
    tip_dt = data.table(tip_label = seeds_tree$tip, 
                        edge_idx = sapply(seeds_tree$tip.label, function(tip_label) which.edge(seeds_tree, tip_label)))
    tip_dt <- tip_dt[edge_dt, on = .(edge_idx)]
    newtree = read.tree(text = trees_reconstructed[tree_id])
    print(names(trees_reconstructed)[tree_id])
    print(write.tree(seeds_tree))
    seeds_tree <- bind.tree(seeds_tree, newtree, where=tip_dt[tip_dt$tip_label==names(trees_reconstructed)[tree_id]]$V2, 0)
  }
  write.tree(seeds_tree, file = paste0(wk_dir, "/transmission_tree/whole_transmission_tree.nwk"))
}







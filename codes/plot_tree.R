## Producing transmission tree plot
library("ape")
library("phylobase")
library("ggtree")
library("ggplot2")
library("gridExtra")
library("grid")

assign_id <- function(meta_df, g1, id_value, new_layer) {
  nodes_num = length(nodeId(g1))
  which_root = 0
  ancestor_ids = c()
  for (i in 1:nodes_num) {
    ancestor_id = ancestor(g1, i)
    ancestor_ids = c(ancestor_ids, ancestor_id)
  }
  new_new_layer = c()
  for (i in new_layer) {
    #print(i)
    ancestor_id = ancestor(g1, i)
    
    if (is.na(ancestor_id)) {
      child_id = max(which(ancestor_ids==i))
      id_value[i,]$ori_id = meta_df[which(meta_df$node_id %in% id_value[child_id,]$ori_id),]$parent_id
      #return(id_value)
    }
    else {
      new_new_layer = c(new_new_layer, ancestor_id)
      if (i > nTips(g1)) {
        child_id = which(ancestor_ids==i)
        id_value[i,]$ori_id = unique(meta_df[which(meta_df$node_id %in% id_value[child_id,]$ori_id),]$parent_id)
      }
      else {
        name = labels(g1)[i]
        id_value[i,]$ori_id = meta_df[which(meta_df$name==name),]$node_id
      }
    }
  }
  new_new_layer = unique(new_new_layer)
  if (any(is.na(id_value$ori_id))) {
    return(assign_id(meta_df, g1, id_value, new_new_layer))
  }
  else {
    return(id_value)
  }
}

assign_color <- function(meta_df, id_value) {
  nodes_num = length(nodeId(g1))
  for (i in 1:nodes_num) {
    id_value[i,]$color = meta_df[which(meta_df$node_id==id_value[i,]$ori_id),]$color_by_t1
  }
  return(id_value)
}

assign_dr <- function(meta_df, id_value) {
  nodes_num = length(nodeId(g1))
  for (i in 1:nodes_num) {
    id_value[i,]$dr = meta_df[which(meta_df$node_id==id_value[i,]$ori_id),]$drug_resistance
    id_value[i,]$label_nm = meta_df[which(meta_df$node_id==id_value[i,]$ori_id),]$name
  }
  return(id_value)
}


args <- commandArgs(trailingOnly = TRUE)
wk_dir <- args[1]

tree_path = list.files(path = file.path(wk_dir, "transmission_tree"), full.names = T)
mt_path = file.path(wk_dir, "transmission_tree_metadata.csv")

configs_file = read.delim(file.path(wk_dir, "params.config"), header = FALSE, sep = ":")
n_gen = as.integer(configs_file[configs_file$V1=="n_generation",]$V2)
sim_start_y = as.integer(configs_file[configs_file$V1=="sim_start_y",]$V2)
sim_start_m = as.integer(configs_file[configs_file$V1=="sim_start_m",]$V2)
sim_start_d = as.integer(configs_file[configs_file$V1=="sim_start_d",]$V2)
sim_time_grid = as.character(configs_file[configs_file$V1=="sim_time_grid",]$V2)

sampled_dt = read.table(file.path(wk_dir, "sample.txt"), sep = " ",
                      header = F, col.names = c("tick", "host_id", "strain", "state"))

meta_df = read.csv(mt_path, header=T)s

for (tr in tree_path)
{
  tree = read.tree(tr)
  labs_tr = strsplit(tree$tip.label[[1]], split="")[[1]]
  dot_index = which(labs_tr==".")
  end = dot_index - 1
  start = dot_index + 1
  tick = paste0(labs_tr[1:end], collapse="")
  host = paste0(labs_tr[start:length(labs_tr)], collapse="")
}





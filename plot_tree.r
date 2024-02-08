library("ape")
library("phylobase")
library("ggtree")
library("ggplot2")
library("gridExtra")
library("grid")
require("data.table")


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
    ancestor_id = ancestor(g1, i)
    
    if (is.na(ancestor_id)) {
      child_ids = which(ancestor_ids==i)
      id_value[i,]$ori_id = meta_df[which(meta_df$node_id %in% id_value[child_ids,]$ori_id),]$parent_id[1]
      #return(id_value)
    }
    else {
      new_new_layer = c(new_new_layer, ancestor_id)
      if (i > nTips(g1)) {
        child_ids = which(ancestor_ids==i)
        id_value[i,]$ori_id = meta_df[which(meta_df$node_id %in% id_value[child_ids,]$ori_id),]$parent_id[1]
      }
      else {
        name = labels(g1)[i]
        id_value[i,]$ori_id = meta_df[which(meta_df$name==name),]$node_id
      }
    }
  }
  new_new_layer = unique(new_new_layer)
  if (any(is.na(id_value$ori_id))) {
    if (is.null(new_new_layer))
    {
      id_value[which(is.na(id_value$ori_id)),]$ori_id = -1
    }
    return(assign_id(meta_df, g1, id_value, new_new_layer))
  }
  else {
    return(id_value)
  }
}


assign_color <- function(meta_df, id_value) {
  nodes_num = length(nodeId(g1))
  #trans_df = data.frame(dr = rep(NA, nodes_num))
  for (i in 1:nodes_num) {
    if (id_value[i,]$ori_id==-1)
    {
      id_value[i,]$color = "grey"
      #trans_df[i,1] = "grey"
    }
    else
    {
      #trans_df[i,1] = meta_df[which(meta_df$node_id==id_value[i,]$ori_id),]$color_trait 
      id_value[i,]$color = meta_df[which(meta_df$node_id==id_value[i,]$ori_id),]$color_trait 
      id_value[i,]$label_nm = meta_df[which(meta_df$node_id==id_value[i,]$ori_id),]$name 
    }
  }
  return(id_value)
}


assign_dr <- function(meta_df, id_value, dr_id, n_trans) {
  col_id = i + 6 + n_trans
  nodes_num = length(nodeId(g1))
  dr_df = data.frame(dr = rep(NA, nodes_num))
  colnames(dr_df) = paste0("dr", dr_id)
  for (i in 1:nodes_num) {
    #dr_df[i,1] = meta_df[which(meta_df$node_id==id_value[i,]$ori_id),col_id]
    if (length(which(meta_df$node_id==id_value[i,]$ori_id))>0){
      dr_df[i,1] = meta_df[which(meta_df$node_id==id_value[i,]$ori_id),col_id]
    }
    else {
      dr_df[i,1] = 0
    }
  }
  id_value = cbind(id_value, dr_df)
  return(id_value)
}




## Input tree metadata file
args <- commandArgs(trailingOnly = TRUE)
wk_dir <- args[1]
seed_size <- as.integer(args[2])
configs_file <- args[3]
n_trans <- as.integer(args[4])
n_dr <- as.integer(args[5])
seed_tree <- args[6]
meta_df = read.csv(file.path(wk_dir, "transmission_tree_metadata.csv"), header=T, sep=",")
colnames(meta_df)[6] <- "color_trait"
slim_config = read.delim(configs_file, header = FALSE, sep = ":")
n_gen = as.integer(slim_config[slim_config$V1=="n_generation",]$V2)
meta_df$name = as.character(meta_df$name)

whole_phylo_output = FALSE
if (file.exists(seed_tree))
{
	seed_phylo = read.tree(seed_tree)
	whole_phylo_output = TRUE
}

for (seed_id in 1:seed_size)
{
  trans_tree_file = file.path(wk_dir, "transmission_tree", paste0(seed_id - 1, ".nwk"))
  tree_str <- paste(readLines(trans_tree_file), collapse="\n")
  if (startsWith(tree_str, "("))
  {
    ## Read tree into tree object if exists
    tree = read.tree(trans_tree_file)
    if (length(tree$tip.label)==1)
    {
      print("Doesn't support visualizing single branch tree.")
      if (whole_phylo_output) 
      {
        seed_phylo <- drop.tip(seed_phylo, as.character(seed_id - 1))
      }
    }
    else
    {
      g1 = as(tree, 'phylo4')
      nodes_num = length(nodeId(g1))
      
      color_value = data.frame(color = rep("grey", nodes_num), ori_id = rep(NA, nodes_num), 
                               label_nm = rep(NA, nodes_num),
                               row.names = nodeId(g1))
      
      start_id = nTips(g1) + 1
      
      color_value_df = assign_color(meta_df, assign_id(meta_df, g1, color_value, 1:nTips(g1)))
      
      rNodeData <- data.frame(color = color_value_df[start_id:nodes_num,]$color,
                              row.names = nodeId(g1, "internal"))
      rTipData <- data.frame(color = color_value_df[1:nTips(g1),]$color)
      
      
      for (i in 1:n_dr)
      {
        color_value_df = assign_dr(meta_df, color_value_df, i, n_trans)
        dr_df = data.frame(dr = color_value_df[start_id:nodes_num, ncol(color_value_df)])
        colnames(dr_df) = paste0("dr", i)
        rNodeData <- cbind(rNodeData, dr_df)
        rTipData <- cbind(rTipData, color_value_df[1:nTips(g1), ncol(color_value_df)])
        if (ncol(color_value_df)>4)
        {
          df_heatmap <- color_value_df[1:nTips(g1), 4:ncol(color_value_df)]
        }
        else
        {
          df_heatmap <- data.frame(dr1=color_value_df[1:nTips(g1), 4])
        }
        rownames(df_heatmap) <- color_value_df[1:nTips(g1),]$label_nm
      }
      
      g2 = phylo4d(g1)
      nodeData(g2) <- rNodeData
      tipData(g2) <- rTipData
      p2 <- ggtree(g2, aes(color=I(color)), ladderize = TRUE)

      if (n_dr>0)
      {
        p3 <- gheatmap(p2, df_heatmap, offset=5, width=0.1) + 
            theme(plot.margin = margin(0,0,0.5,1, "cm")) +
            scale_fill_gradient(low="white", high="orange")
      }
      else
      {
        p3 <- p2
      }
      
      p3 <- gheatmap(p2, df_heatmap, offset=5, width=0.1) + 
        theme(plot.margin = margin(0,0,0.5,1, "cm")) +
        scale_fill_gradient(low="white", high="orange") 
    
      ggsave(file.path(wk_dir, "transmission_tree", paste0("tree.", seed_id - 1, ".pdf")), plot = p3, width = 5, height = 10, dpi = 300)
      
      if (whole_phylo_output) 
      {
        edge_dt = as.data.frame(seed_phylo$edge)
        setDT(edge_dt)
        edge_dt[, edge_idx := as.integer(rownames(edge_dt))]
        tip_dt = data.table(tip_label = seed_phylo$tip, 
                            edge_idx = sapply(seed_phylo$tip.label, function(tip_label) which.edge(seed_phylo, tip_label)))
        tip_dt <- tip_dt[edge_dt, on = .(edge_idx)]
        seed_phylo <- bind.tree(seed_phylo, tree, where=tip_dt[tip_dt$tip_label==seed_id - 1]$V2, 0)
      }
    }
  }
  else
  {
    print("No samples for this seed's progeny.")
    if (length(seed_phylo$tip.label)==1)
    {
      whole_phylo_output = FALSE
    }
    if (whole_phylo_output) 
    {
      seed_phylo <- drop.tip(seed_phylo, as.character(seed_id - 1))
    }
  }
}


if (whole_phylo_output) 
{
	write.tree(seed_phylo, file=file.path(wk_dir, "whole_transmission_tree.nwk"))
	meta_df$name = as.character(meta_df$name)
	g1 = as(seed_phylo, 'phylo4')
	nodes_num = length(nodeId(g1))

	color_value = data.frame(color = rep("grey", nodes_num), ori_id = rep(NA, nodes_num), 
                       label_nm = rep(NA, nodes_num),
                       row.names = nodeId(g1))

	start_id = nTips(g1) + 1

	color_value_df = assign_color(meta_df, assign_id(meta_df, g1, color_value, 1:nTips(g1)))
  
  rNodeData <- data.frame(color = color_value_df[start_id:nodes_num,]$color,
                          row.names = nodeId(g1, "internal"))
	rTipData <- data.frame(color = color_value_df[1:nTips(g1),]$color)

  	
	if (n_dr>0)
 	{
 		for (i in 1:n_dr)
  	{
    	color_value_df = assign_dr(meta_df, color_value_df, i, n_trans)
    	dr_df = data.frame(dr = color_value_df[start_id:nodes_num, ncol(color_value_df)])
    	colnames(dr_df) = paste0("dr", i)
    	rNodeData <- cbind(rNodeData, dr_df)
    	rTipData <- cbind(rTipData, color_value_df[1:nTips(g1), ncol(color_value_df)])
  	}
    if (ncol(color_value_df)>4)
    {
      df_heatmap <- color_value_df[1:nTips(g1), 4:ncol(color_value_df)]
    }
    else
    {
      df_heatmap <- data.frame(dr1=color_value_df[1:nTips(g1), 4])
    }
    rownames(df_heatmap) <- color_value_df[1:nTips(g1),]$label_nm
 	}
  
  g2 = phylo4d(g1)
 	nodeData(g2) <- rNodeData
 	tipData(g2) <- rTipData
 	p2 <- ggtree(g2, aes(color=I(color)), ladderize = TRUE)

  if (n_dr>0)
  {
    p3 <- gheatmap(p2, df_heatmap, offset=5, width=0.1) + 
        theme(plot.margin = margin(0,0,0.5,1, "cm")) +
        scale_fill_gradient(low="white", high="orange")
  }
  else
  {
    p3 <- p2
  }

	ggsave(file.path(wk_dir, "whole_transmission_tree.pdf"), plot = p3, width = 5, height = 10, dpi = 300)
}




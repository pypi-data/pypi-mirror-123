import numba as nb
import numpy as np
import pandas as pd
import lsdnumbatools as lsdnb


@nb.njit()
def get_max_in_window(iteratool, array, starting_node, distance):
	print("StARTING NODE IS", starting_node)
	print("Which IS", iteratool.node2rowcol(starting_node))

	mahQ = lsdnb.fifo(array.shape[0])
	mahQ.push(starting_node)
	argval = starting_node
	val = array[starting_node]
	cumdist = np.zeros(array.shape[0])
	is_in_Q = np.zeros_like(array,dtype = np.int8)
	is_in_Q[starting_node] = 1
	nnodes = 0
	cumdist[starting_node] = 0

	while(mahQ.size != 0):
		nnodes += 1
		next_node = mahQ.pop()
		neight = iteratool.get_neighbouring_nodes(next_node)
		for i in range(neight.shape[0]):
			if(neight[i] < 0):
				continue
			if(is_in_Q[neight[i]] == 1):
				continue
			cumdist[neight[i]] = cumdist[next_node] + iteratool.lengthener[i]
			if(cumdist[neight[i]] > distance):
				continue

			mahQ.push(neight[i])

			is_in_Q[neight[i]] = 1

			if(array[neight[i]] > val):
				val = array[neight[i]]
				argval = neight[i]
	# print("Found after", nnodes, ":",argval,val)
	return argval, val

@nb.njit()
def _get_quick_river_network_from_mask(rec, stack, arrth, th, mask):
	iz_visited = np.zeros_like(stack, dtype = nb.int8)
	iz_visited[mask == 0] = 1
	nodes = np.full_like(stack,-1)

	nnodes = -1
	for inode in stack[::-1]:
		if(iz_visited[inode] == 1):
			continue
		if(arrth[inode] < th):
			continue
		nnodes += 1
		nodes[nnodes] = inode
		iz_visited[inode] = 1
		cnode = inode
		while(rec[cnode] != cnode and iz_visited[rec[cnode]] != 1):
			cnode = rec[cnode]
			nnodes += 1
			nodes[nnodes] = cnode
			iz_visited[cnode] = 1

	nnodes += 1
	return nodes[:nnodes]

@nb.njit()
def label_down_from_node_D8(node, rec):
	output = np.zeros_like(rec)
	output[node] = 1
	cnode = node
	tn = 1
	while(rec[cnode] != cnode):
		cnode = rec[cnode]
		output[cnode] = 1
		tn += 1

	return output

def get_quick_river_network_from_mask(dem, mask = None, threshold_array = None, threshold = 1e6):

	rivernodes = _get_quick_river_network_from_mask(dem.graph.ds["D8Srec"].values, 
		dem.graph.ds["SStack"].values, dem.ds[threshold_array].values.ravel(), threshold, dem.ds[mask].values.ravel())
	rows,cols = dem.graph.iterator_tool.node2rowcol(rivernodes)
	dist = dem.graph.compute_distance_from_outlet()
	dist[dem.ds[mask].values.ravel()==False] = 0
	maine = label_down_from_node_D8(np.argmax(dist), dem.graph.ds["D8Srec"].values)
	df = pd.DataFrame({
		"node": rivernodes,
		"row": rows,
		"col": cols,
		"elevation": dem.graph.ds["topography"].values[rivernodes],
		"distance_from_outlet" : dist[rivernodes],
		"main_stem": maine[rivernodes]
		})
	return df



















































# end of file



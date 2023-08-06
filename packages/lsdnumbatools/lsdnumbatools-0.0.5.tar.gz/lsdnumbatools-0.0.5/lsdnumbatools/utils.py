import numba as nb
import numpy as np

@nb.jit(nopython = True, cache = True)
def rectangle_compartimentor( nrows, ncols, nodes):
	"""
	returns rows and cols indices arrays from am array of node indices
	"""
	# pregenerating node, row, cols
	cols = np.mod(nodes,ncols)
	rows = ((nodes - cols) / ncols).astype(np.int16)
	return rows, cols

def combine_masks(xalsd,masks, intersect = True):
	omask = np.zeros(xalsd.graph.ds["nxy"].values,dtype = np.int8)
	func = np.logical_and if intersect else np.logical_or
	for tm in masks:
		if(is_instance(tm,str)):
			omask = func(omask , xalsd.ds[tm].values)
		elif(is_instance(tm,np.ndarray)):
			omask = func(omask , tm)
	return omask





@nb.jit(nopython = True, cache = True)
def rectangle_compartimentor( nrows, ncols, nrcomp, nccomp):
	arr2D = np.zeros((nrows,ncols), dtype = np.intc)
	current_ID = -1
	base_row = 0
	base_col = 0
	while(True):
		current_ID +=1
		for r in range(nrcomp):
			nr = base_row + r
			for c in range(nccomp):
				nc = base_col + c
				if(nr >= nrows or nc >= ncols):
					continue
				arr2D[nr,nc] = current_ID
			
		base_col += nccomp
		if(base_col >= ncols):
			base_col = 0
			base_row += nrcomp
			
		if(base_row >= nrows):
			break
		
	return arr2D.ravel()
	
@nb.jit(nopython = True, cache = True)
def fill_array_from_index( arr, index_array, index2val):
	for i in range(arr.shape[0]):
		arr[i] = index2val[index_array[i]]
	

@nb.jit(nopython = True, cache = True)
def average_amongst_donors_and_recs(arr,Srec,Sdons, Sndons):
	
	intermediate = np.zeros_like(arr)
	for inode in range(Srec.shape[0]):
		values = 0
		N = 0
		if(Srec[inode] == inode):
			continue
		for i in range(Sndons[inode]):
			values += arr[Sdons[inode,i]]
			N +=1
		values += arr[Srec[inode]]
		N += 1

		intermediate[inode] = values/N
		
	return intermediate



_fifo_specs = [
	('array', nb.int64[:]),
	('size', nb.int64),
	('capacity', nb.int64),
	('reading_id', nb.int64),
	('inserting_id', nb.int64),

]


@nb.experimental.jitclass(_fifo_specs)
class fifo(object):
	"""docstring for BasicQueue"""
	def __init__(self, capacity):
		self.capacity = capacity
		self.size = 0
		self.reading_id = -1
		self.inserting_id = -1
		self.array = np.full(self.capacity,-1)

	def push(self, val):
		self.inserting_id += 1
		self.size += 1
		if(self.capacity == self.inserting_id):
			temp = np.full(self.capacity * 2,-1 )
			temp[:self.capacity] = self.array 
			self.capacity = self.capacity * 2
			self.array = temp
		self.array[self.inserting_id] = val

	def pop(self):
		self.reading_id += 1
		if(self.reading_id > self.inserting_id):
			print("Returning -9999, fifo out of bounds")
			self.reading_id -= 1
			return -9999
		self.size -= 1
		return self.array[self.reading_id]









































# End of file


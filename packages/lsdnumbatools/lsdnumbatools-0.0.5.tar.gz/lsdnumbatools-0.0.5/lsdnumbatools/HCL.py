import numpy as np
import numba as nb
import math

@nb.njit()
def flow_route(elev, hw, iteratool, qx, qy, local_time_factor, hflow_threshold, mannings, gravity, edgeslope, froude_limit):

	#temp storage of t-1
	# qout_beef = np.copy(qout)

	# Looping thorugh all thingy
	for i in range(iteratool.nxy):
		# ignoring nodata:
		if(iteratool.node_type[i] <= 0):
			continue

		# lengthener increment
		neb = iteratool.get_neighbouring_nodes(i)
		recx = neb[3]
		recy = neb[1]

		for rec in [recx,recy]:

			if(rec == iteratool.not_a_neightbour or iteratool.node_type[rec] < 0):
				continue

			# Ignoring nowater
			if(hw[i] <= 0 and hw[rec] <= 0):
				continue

			# Calculating hflow
			hflow = max(elev[i] + hw[i], elev[rec] + hw[rec]) - max(elev[rec], elev[i])

			# If bellow flow threshold: pass
			if (hflow <= hflow_threshold):
				# qout[i,lenghtener_i] = 0
				if(rec == recx):
					qx[i] = 0
				else:
					qy[i] = 0

				continue

			# Getting the distance to the next node
			if(rec == recx):
				DX = iteratool.dx 
			else:
				DX = iteratool.dy

			# Calculating the hydraulic slope
			tempslope = (((elev[rec] + hw[rec])) - (elev[i] + hw[i])) / DX;
			
			# If border condition:
			if(iteratool.node_type[rec] <= 0):
				# if()
				tempslope = edgeslope

			# Equation 1 of Caesar Lisflood paper
			if(rec == recx):
				qx[i] = ((qx[i] - (gravity * hflow * local_time_factor * tempslope)) /
			                        (1 + gravity * hflow * local_time_factor * (mannings * mannings) * abs(qx[i]) /
			                         math.pow(hflow, (10 / 3))));
			else:
				qy[i] = ((qy[i] - (gravity * hflow * local_time_factor * tempslope)) /
			                        (1 + gravity * hflow * local_time_factor * (mannings * mannings) * abs(qy[i]) /
			                         math.pow(hflow, (10 / 3)))); 


			# This comment is from Declan Valters' implementation:
			# need to have these lines to stop too much water moving from one cell to another - resulting in -ve discharges
   #    which causes a large instability to develop - only in steep catchments really
			if(rec == recx):
				if(qx[i] > 0 and (qx[i] / hflow)/math.sqrt(gravity*hflow) > froude_limit ):
					qx[i] = hflow * (math.sqrt(gravity*hflow) * froude_limit );

				if (qx[i] < 0 and abs(qx[i] / hflow) / math.sqrt(gravity * hflow) > froude_limit ):
					qx[i] = 0 - (hflow * (math.sqrt(gravity * hflow) * froude_limit ));

				if (qx[i] > 0 and (qx[i] * local_time_factor / DX) > (hw[i] / 4)):
					qx[i] = ((hw[i] * DX) / 5) / local_time_factor;

				if (qx[i] < 0 and abs(qx[i] * local_time_factor / DX) > (hw[rec] / 4)):
					qx[i] = 0 - ((hw[rec] * DX) / 5) / local_time_factor;
			else:
				if(qy[i] > 0 and (qy[i] / hflow)/math.sqrt(gravity*hflow) > froude_limit ):
					qy[i] = hflow * (math.sqrt(gravity*hflow) * froude_limit );

				if (qy[i] < 0 and abs(qy[i] / hflow) / math.sqrt(gravity * hflow) > froude_limit ):
					qy[i] = 0 - (hflow * (math.sqrt(gravity * hflow) * froude_limit ));

				if (qy[i] > 0 and (qy[i] * local_time_factor / DX) > (hw[i] / 4)):
					qy[i] = ((hw[i] * DX) / 5) / local_time_factor;

				if (qy[i] < 0 and abs(qy[i] * local_time_factor / DX) > (hw[rec] / 4)):
					qy[i] = 0 - ((hw[rec] * DX) / 5) / local_time_factor;



@nb.njit()
def calculate_dt(previousdt, iteratool, hw, courant_number, gravity) :
	# Equation 3 of the paper
	hwmax =  hw.max()
	if(hwmax > 0): # and (previousdt > (courant_number * (min(iteratool.dx,iteratool.dy) / math.sqrt(gravity * (hwmax)))))):
		local_time_factor = courant_number * ( min(iteratool.dx,iteratool.dy) / math.sqrt( gravity * ( hwmax ) ) );
	else:
		local_time_factor = previousdt

	return local_time_factor;      


@nb.njit()
def depth_update(hw, qx, qy, iteratool, local_time_factor):

	for i in range(iteratool.nxy):

		if(iteratool.node_type[i] <=0):
			continue

		neb = iteratool.get_neighbouring_nodes(i)
		recx = neb[4]
		recy = neb[6]

		# if(iteratool.node_type[recx] >= 0 and recx != iteratool.not_a_neightbour):
		dqx = qx[recx] - qx[i]
		# else:
			# dqx = qx[i]
		# if(iteratool.node_type[recy] >= 0 and recy != iteratool.not_a_neightbour):
		dqy = qy[recy] - qy[i]
		# else:
			# dqy = qy[i]

		hw[i] += local_time_factor * (dqx + dqy) / (iteratool.dx * iteratool.dy);

def flow_route_parallel(elev, hw, iteratool, qx, qy, local_time_factor, hflow_threshold, mannings, gravity, edgeslope, froude_limit, n_threads):
	oldth = nb.get_num_threads()
	nb.set_num_threads(n_threads)
	_flow_route_parallel(elev, hw, iteratool, qx, qy, local_time_factor, hflow_threshold, mannings, gravity, edgeslope, froude_limit, n_threads)
	nb.set_num_threads(oldth)

nb.njit(parallel = True, nogil = True)
def _flow_route_parallel(elev, hw, iteratool, qx, qy, local_time_factor, hflow_threshold, mannings, gravity, edgeslope, froude_limit, n_threads):

	# setting the number of threads
	down_lim = np.zeros(n_threads, dtype = np.int32)
	upper_lim = np.zeros(n_threads, dtype = np.int32)
	limiter = np.int32(math.ceil(iteratool.ny/n_threads))
	for i in range(n_threads):
		down_lim[i] = i*limiter
		upper_lim[i] = (i+1) * limiter
		if(i>=1):
			down_lim[i] = upper_lim[i-1] + 1
		# print(down_lim[i], upper_lim[i])

	upper_lim[-1] = iteratool.ny-1
	# for i in range(n_threads):
	down_lim = down_lim * iteratool.nx
	upper_lim = upper_lim * iteratool.nx



	# Looping thorugh all thingy
	for i in nb.prange(n_threads):
		# print("from",down_lim[i], "to" ,upper_lim[i])
		nodes = np.arange(down_lim[i],upper_lim[i])
		__flow_route_parallel(elev, hw, iteratool, qx, qy, local_time_factor, hflow_threshold, mannings, gravity, edgeslope, froude_limit, nodes)

	for i in range(n_threads - 1):
		nodes = np.arange(upper_lim[i], upper_lim[i] + iteratool.nx)
		__flow_route_parallel(elev, hw, iteratool, qx, qy, local_time_factor, hflow_threshold, mannings, gravity, edgeslope, froude_limit, nodes)

@nb.njit( nogil = True)
def __flow_route_parallel(elev, hw, iteratool, qx, qy, local_time_factor, hflow_threshold, mannings, gravity, edgeslope, froude_limit, nodes):

	#temp storage of t-1
	# qout_beef = np.copy(qout)

	# Looping thorugh all thingy
	for i in nodes:
		# ignoring nodata:
		if(iteratool.node_type[i] <= 0):
			continue

		# lengthener increment
		neb = iteratool.get_neighbouring_nodes(i)
		recx = neb[3]
		recy = neb[1]

		for rec in [recx,recy]:

			if(rec == iteratool.not_a_neightbour or iteratool.node_type[rec] < 0):
				continue

			# Ignoring nowater
			if(hw[i] <= 0 and hw[rec] <= 0):
				continue

			# Calculating hflow
			hflow = max(elev[i] + hw[i], elev[rec] + hw[rec]) - max(elev[rec], elev[i])

			# If bellow flow threshold: pass
			if (hflow <= hflow_threshold):
				# qout[i,lenghtener_i] = 0
				if(rec == recx):
					qx[i] = 0
				else:
					qy[i] = 0

				continue

			# Getting the distance to the next node
			if(rec == recx):
				DX = iteratool.dx 
			else:
				DX = iteratool.dy

			# Calculating the hydraulic slope
			tempslope = (((elev[rec] + hw[rec])) - (elev[i] + hw[i])) / DX;
			
			# If border condition:
			if(iteratool.node_type[rec] <= 0):
				# if()
				tempslope = edgeslope

			# Equation 1 of Caesar Lisflood paper
			if(rec == recx):
				qx[i] = ((qx[i] - (gravity * hflow * local_time_factor * tempslope)) /
			                        (1 + gravity * hflow * local_time_factor * (mannings * mannings) * abs(qx[i]) /
			                         math.pow(hflow, (10 / 3))));
			else:
				qy[i] = ((qy[i] - (gravity * hflow * local_time_factor * tempslope)) /
			                        (1 + gravity * hflow * local_time_factor * (mannings * mannings) * abs(qy[i]) /
			                         math.pow(hflow, (10 / 3)))); 


			# This comment is from Declan Valters' implementation:
			# need to have these lines to stop too much water moving from one cell to another - resulting in -ve discharges
   #    which causes a large instability to develop - only in steep catchments really
			if(rec == recx):
				if(qx[i] > 0 and (qx[i] / hflow)/math.sqrt(gravity*hflow) > froude_limit ):
					qx[i] = hflow * (math.sqrt(gravity*hflow) * froude_limit );

				if (qx[i] < 0 and abs(qx[i] / hflow) / math.sqrt(gravity * hflow) > froude_limit ):
					qx[i] = 0 - (hflow * (math.sqrt(gravity * hflow) * froude_limit ));

				if (qx[i] > 0 and (qx[i] * local_time_factor / DX) > (hw[i] / 4)):
					qx[i] = ((hw[i] * DX) / 5) / local_time_factor;

				if (qx[i] < 0 and abs(qx[i] * local_time_factor / DX) > (hw[rec] / 4)):
					qx[i] = 0 - ((hw[rec] * DX) / 5) / local_time_factor;
			else:
				if(qy[i] > 0 and (qy[i] / hflow)/math.sqrt(gravity*hflow) > froude_limit ):
					qy[i] = hflow * (math.sqrt(gravity*hflow) * froude_limit );

				if (qy[i] < 0 and abs(qy[i] / hflow) / math.sqrt(gravity * hflow) > froude_limit ):
					qy[i] = 0 - (hflow * (math.sqrt(gravity * hflow) * froude_limit ));

				if (qy[i] > 0 and (qy[i] * local_time_factor / DX) > (hw[i] / 4)):
					qy[i] = ((hw[i] * DX) / 5) / local_time_factor;

				if (qy[i] < 0 and abs(qy[i] * local_time_factor / DX) > (hw[rec] / 4)):
					qy[i] = 0 - ((hw[rec] * DX) / 5) / local_time_factor;


#####
##### Old test
#####





# import numpy as np
# import numba as nb
# import math

# @nb.njit()
# def flow_route(elev, hw, iteratool, qout, local_time_factor, hflow_threshold, mannings, gravity, edgeslope, froude_limit):

# 	#temp storage of t-1
# 	# qout_beef = np.copy(qout)

# 	# Looping thorugh all thingy
# 	for i in range(iteratool.nxy):
# 		# ignoring nodata:
# 		if(iteratool.node_type[i] <= 0):
# 			continue

# 		# Ignoring nowater
# 		if(hw[i] <= 0):
# 			continue

# 		# lengthener increment
# 		lenghtener_i = -1
# 		for rec in iteratool.get_neighbouring_nodes(i):
# 			lenghtener_i += 1
# 			# If the receiver is not a valid node
# 			if(iteratool.node_type[rec] < 0):
# 				qout[i,lenghtener_i] = 0
# 				continue
# 			if(elev[rec] + hw[rec] > elev[i] + hw[i]):
# 				qout[i,lenghtener_i] = 0
# 				continue

# 			# Calculating hflow
# 			hflow = max(elev[i] + hw[i], elev[rec] + hw[rec]) - max(elev[rec], elev[i])

# 			# If bellow flow threshold: pass
# 			if (hflow <= hflow_threshold):
# 				qout[i,lenghtener_i] = 0
# 				continue

# 			# Getting the distance to the next node
# 			DX = iteratool.lengthener[lenghtener_i]

# 			# Calculating the hydraulic slope
# 			tempslope = (((elev[rec] + hw[rec])) - (elev[i] + hw[i])) / DX;
			
# 			# If border condition:
# 			if(iteratool.node_type[rec] == 0):
# 				tempslope = edgeslope

# 			# Equation 1 of Caesar Lisflood paper
# 			qout[i,lenghtener_i] = ((qout[i,lenghtener_i] - (gravity * hflow * local_time_factor * tempslope)) /
# 			                        (1 + gravity * hflow * local_time_factor * (mannings * mannings) * abs(qout[i,lenghtener_i]) /
# 			                         math.pow(hflow, (10 / 3))));

# 			# Testing something here
# 			if(qout[i,lenghtener_i] < 0):
# 				qout[i,lenghtener_i] = 0
			


# 			# This comment is from Declan Valters' implementation:
# 			# need to have these lines to stop too much water moving from one cell to another - resulting in -ve discharges
#       # which causes a large instability to develop - only in steep catchments really
# 			# if (qout[i,lenghtener_i] > 0 and (qout[i,lenghtener_i] / hflow)/math.sqrt(gravity*hflow) > froude_limit ):
# 			# 	qout[i,lenghtener_i] = hflow * (math.sqrt(gravity*hflow) * froude_limit );

# 			# if (qout[i,lenghtener_i] < 0 and abs(qout[i,lenghtener_i] / hflow) / math.sqrt(gravity * hflow) > froude_limit ):
# 			# 	qout[i,lenghtener_i] = 0 - (hflow * (math.sqrt(gravity * hflow) * froude_limit ));

# 			# if (qout[i,lenghtener_i] > 0 and (qout[i,lenghtener_i] * local_time_factor / DX) > (hw[i] / 4)):
# 			# 	qout[i,lenghtener_i] = ((hw[i] * DX) / 5) / local_time_factor;

# 			# if (qout[i,lenghtener_i] < 0 and abs(qout[i,lenghtener_i] * local_time_factor / DX) > (hw[rec] / 4)):
# 			# 	qout[i,lenghtener_i] = 0 - ((hw[rec] * DX) / 5) / local_time_factor;

# @nb.njit()
# def calculate_dt(previousdt, iteratool, hw, courant_number, gravity) :
# 	# Equation 3 of the paper
# 	hwmax =  hw.max()
# 	if(hwmax > 0): # and (previousdt > (courant_number * (min(iteratool.dx,iteratool.dy) / math.sqrt(gravity * (hwmax)))))):
# 		local_time_factor = courant_number * ( min(iteratool.dx,iteratool.dy) / math.sqrt( gravity * ( hwmax ) ) );
# 	else:
# 		local_time_factor = previousdt

# 	return local_time_factor;      


# @nb.njit()
# def depth_update(hw, qout, iteratool, local_time_factor, TO, elev):


# 	# Initialising a qin to 0
# 	qin = np.zeros(iteratool.nxy)
# 	hwitp1 = np.copy(hw)

# 	# First loop to calculate qin
# 	for i in TO:
# 		# ignoring nodata:
# 		if(iteratool.node_type[i] <= 0):
# 			continue

# 		sumQout = np.sum(qout[i])
# 		# This is a generalisation of Equation 2 in the caesar lisflood paper -> see equation 1 from bates et al 2010 (delta water depth is the divergence of water fluxes)
# 		hwitp1[i] += local_time_factor * (qin[i] - sumQout) / (iteratool.dx * iteratool.dy);

# 		if(hwitp1[i] < 0):
# 			extra_q = abs(hwitp1[i]) * (iteratool.dx * iteratool.dy);
# 			hwitp1[i] = 0
# 			n_extra = 0
# 			lenghtener_i = -1
# 			for rec in iteratool.get_neighbouring_nodes(i):
# 				lenghtener_i += 1
# 				if(elev[rec] + hw[rec] > elev[i] + hw[i]):
# 					continue

# 				# If the receiver is not a valid node
# 				if(iteratool.node_type[rec] < 0):
# 					continue
# 				n_extra += 1
# 			for rec in iteratool.get_neighbouring_nodes(i):
# 				lenghtener_i += 1
# 				if(elev[rec] + hw[rec] > elev[i] + hw[i]):
# 					continue

# 				# If the receiver is not a valid node
# 				if(iteratool.node_type[rec] < 0):
# 					continue

# 				qout[i,lenghtener_i] -= extra_q/n_extra;
# 				if(qout[i,lenghtener_i]<0):
# 					qout[i,lenghtener_i] = 0 #PROBABLY MASS BALANCE ISSUE THERE

# 		lenghtener_i = -1
# 		for rec in iteratool.get_neighbouring_nodes(i):
# 			lenghtener_i += 1
# 			if(elev[rec] + hw[rec] > elev[i] + hw[i]):
# 				continue

# 			# If the receiver is not a valid node
# 			if(iteratool.node_type[rec] < 0):
# 				qout[i,lenghtener_i] = 0
# 				continue

# 			# else:
# 			qin[rec] += qout[i,lenghtener_i]


# 	hw[:] = hwitp1[:]

# 	# # second loop to calculate hw (water depths)
# 	# for i in range(iteratool.nxy):
# 	# 	# ignoring nodata:
# 	# 	if(iteratool.node_type[i] <= 0):
# 	# 		continue

# 	# 	# This is a generalisation of Equation 2 in the caesar lisflood paper -> see equation 1 from bates et al 2010 (delta water depth is the divergence of water fluxes)
# 	# 	hw[i] += local_time_factor * (qin[i] - np.sum(qout[i])) / (iteratool.dx * iteratool.dy);









# @nb.njit()
# def depth_update_old(hw, qout, iteratool, local_time_factor):

# 	# Initialising a qin to 0
# 	qin = np.zeros(iteratool.nxy)

# 	# First loop to calculate qin
# 	for i in range(iteratool.nxy):
# 		# ignoring nodata:
# 		if(iteratool.node_type[i] <= 0):
# 			continue

# 		lenghtener_i = -1
# 		for rec in iteratool.get_neighbouring_nodes(i):
# 			lenghtener_i += 1
# 			# If the receiver is not a valid node
# 			if(iteratool.node_type[rec] < 0):
# 				hw[i] = 0
# 				continue

# 			# else:
# 			qin[rec] += qout[i,lenghtener_i]

# 	# second loop to calculate hw (water depths)
# 	for i in range(iteratool.nxy):
# 		# ignoring nodata:
# 		if(iteratool.node_type[i] <= 0):
# 			continue

# 		# This is a generalisation of Equation 2 in the caesar lisflood paper -> see equation 1 from bates et al 2010 (delta water depth is the divergence of water fluxes)
# 		hw[i] += local_time_factor * (qin[i] - np.sum(qout[i])) / (iteratool.dx * iteratool.dy);













# model.register(
# 	"drainage_area", 
# 	transmissible_downstream = True, 
# 	dimension = 2,
# 	)



# def SPL():
# 	receiver_node = graph.get_receiver_node()
# 	slope = graph.get_slope_to_receiver()
# 	this_erosion = slope**model.n * model.K * model.drainage_area**m
# 	model.fluvial_erosion[current_node].add(this_erosion)
# model.define_function("SPL", SPL)

# model.define_phase("continental", ["water_routing","SPL","Hillslope"], track_provenance = True)
# model.define_phase("Marine", ["water_routing","SPL","Hillslope"], spatial_limits = ["define_sea"])


# model.














import math
import itertools
import os
class prefixLengthBS():
	def __init__(self,max_length,table):
		self.hash_table = {}
		self.expand_table={}
		for i in range(max_length+1):
			self.hash_table[i] = {}
		self.max_length = max_length
		self.set_hash_table(table)
		depth = int(math.ceil(math.log(self.max_length+2,2)))
		max_bound = int(math.pow(2,depth))
		root = int(math.floor( max_bound - 1)/2)
		self.put_markers(root,0,max_bound-2)
	
	def set_hash_table(self,table):
		for pref in table:
			self.hash_table[len(pref)][pref] = table[pref]

	def right_children(self,index,prev_bound,next_bound):
		#print "prev = {0}\nindex = {1}\nnext = {2}\n".format(prev_bound,index,next_bound)
		if index==next_bound or index == prev_bound:
			return [index]
		right_index = int(index+math.ceil(float(next_bound-index)/2))
		if prev_bound != 0:
			left_index = int(index-math.floor(float(index-prev_bound)/2))
		else:
   			left_index = int(index-math.floor(float(index-prev_bound+1)/2))
   		return self.right_children(right_index,index,next_bound) + self.right_children(left_index,prev_bound,index)

	def put_markers(self,index,prev_bound,next_bound):
		#print "putting markers"
		#print "prev = {0}\nindex = {1}\nnext = {2}\n".format(prev_bound,index,next_bound)
		if index>=next_bound or index <= prev_bound or index == 0:
			return 
		right_index = int(index+math.ceil(float(next_bound-index)/2))
		right_children = self.right_children(right_index,index,next_bound)
		#print right_children
		for i in right_children:
			if i <= len(self.hash_table)-1:
				for ip in self.hash_table[i]:
					if self.hash_table[index].get(ip[0:index]) == None:
						self.hash_table[index][ip[0:index]] = "Mark"#self.hash_table[i][ip]
		self.put_markers(right_index,index,next_bound)
		if prev_bound != 0:
			left_index = int(index-math.floor(float(index-prev_bound)/2))
			right_of_left_index = int(left_index+math.ceil(float(index-left_index)/2))
		else:
			left_index = int(index-math.floor(float(index-prev_bound+1)/2))
			right_of_left_index = int(left_index+math.ceil(float(index-1-left_index)/2))
		#print "putting right of "+str(left_index)
		self.put_markers(right_of_left_index,left_index,index-1)
		self.put_markers(left_index,prev_bound,index-1)
	def search(self,ip):
		depth = int(math.ceil(math.log(self.max_length+2,2)))
		max_bound = int(math.pow(2,depth))
		root = int(math.floor( max_bound - 1)/2)
		return self.inner_search(root,0,max_bound-2,ip)
   	def inner_search(self,index, prev_bound, next_bound, ip):
		#print "prev = {0}\nindex = {1}\nnext = {2}\n".format(prev_bound,index,next_bound)
   		sub_ip = ip[0:index]
   		if index==next_bound or index == prev_bound:
   			return self.hash_table[index].get(sub_ip)
   		if self.hash_table[index].get(sub_ip) != None: #to right
   			right_index = int(index+math.ceil(float(next_bound-index)/2))
   			nexthop = self.inner_search(right_index,index,next_bound,ip)
   			print nexthop
   			if nexthop == None and self.hash_table[index].get(sub_ip) !="Mark":
   				nexthop = self.hash_table[index].get(sub_ip)

   		if self.hash_table[index].get(sub_ip) == None: #to left
   			if prev_bound != 0:
   				left_index = int(index-math.floor(float(index-prev_bound)/2))
   			else:
   				left_index = int(index-math.floor(float(index-prev_bound+1)/2))
   			return self.inner_search(left_index,prev_bound,index,ip)

   		return nexthop

   	
class prefixLengthExpandBS(prefixLengthBS):
	def __init__(self,max_length,table):
		prefixLengthBS.__init__(self,max_length,table)
		self.expand_table[2]={}
		self.expand_table[int(math.ceil(float(self.max_length) / 2) + 1)]={}
		self.expand_table[self.max_length]={}
		self.set_expand_table()
	def set_expand_table(self):
		mid_index = int(math.ceil(float(self.max_length) / 2) + 1)
		for i in range(self.max_length+1):
			for ip in self.hash_table[i]:
				if i <= 2:
					expand_str = ["".join(seq) for seq in itertools.product("01", repeat=2-i)]
					for str in expand_str:
						self.expand_table[2][ip + str] = self.hash_table[i][ip]
					self.expand_table[2].update(self.hash_table[2])
				else :
					if i <= mid_index:
						expand_str = ["".join(seq) for seq in itertools.product("01", repeat= mid_index - i)]
						for str in expand_str:
							self.expand_table[mid_index][ip + str] = self.hash_table[i][ip]
						self.expand_table[mid_index].update(self.hash_table[mid_index])
					else :
						if i <= self.max_length:
							expand_str = ["".join(seq) for seq in itertools.product("01", repeat=self.max_length - i)]
							for str in expand_str:
								self.expand_table[self.max_length][ip + str] = self.hash_table[i][ip]
							self.expand_table[self.max_length].update(self.hash_table[self.max_length])
		for ip in self.expand_table[self.max_length]:
			if self.expand_table[mid_index].get(ip[0:mid_index]) == None:
				self.expand_table[mid_index][ip[0:mid_index]] = self.expand_table[self.max_length][ip]

	def search(self,ip):
   		index=int(math.ceil(float(self.max_length) / 2) + 1)
   		sub_ip = ip[0:index]
   		if self.expand_table[index].get(sub_ip) != None:
   			print sub_ip
			if self.expand_table[self.max_length].get(ip[0:self.max_length]):
				return self.expand_table[self.max_length][ip[0:self.max_length]]
			if self.expand_table[index].get(sub_ip) != None:
				return self.expand_table[index][sub_ip]
   		if self.expand_table[index].get(sub_ip) == None: #to left
   			if self.expand_table[2].get(ip[0:2]) != None:
   				return self.expand_table[2][ip[0:2]];
   		return None
class prefixRangeBS():
	def __init__(self,max_length,table):
		#self.table = {"1":"p1","101":"p2","10101":"p3","1011":"p4"}
		#self.table = {"1":"p1","101":"p2","101010":"p3","1011":"p4","11":"p5","110":"p6"}
		self.ranges = {}
		self.labels = {}
		self.nexthops = {}
		self.max_length = max_length+1
		self.table = table
		self.make_ranges()
		self.precomputation()

	def make_ranges(self):
		for ip in self.table:
			startip = ip+"0"*(self.max_length-len(ip))
			self.ranges[startip] = self.table[ip]
			self.labels[startip] = "L"
			endip = ip+"1"*(self.max_length-len(ip))
			if self.max_length - len(ip) == 0:
				print endip
				endip = ''.join(format(int(int(startip,2)+1),str(self.max_length)+'b'))
				print endip
				self.ranges[endip] = self.table[ip]
				self.labels[endip] = "H"
			else:
				if self.ranges.get(endip) and self.labels[endip] =="H":
					endip = ''.join(format(int(int(startip,2)+1),str(self.max_length)+'b'))
					self.ranges[endip] = self.table[ip]
					self.labels[endip] = "H"
				else:
					self.ranges[endip] = self.table[ip]
					self.labels[endip] = "H"
		
	def precomputation(self):
		print "precomputation"
		s = list()
		ips = sorted(self.ranges)
		i = 0 		
		while(i < len(ips)):
			if self.labels[ips[i]] == "L":
				s.append(self.ranges[ips[i]])
				#self.nexthops[ips[i]]["="] = self.ranges[ips[i]]
				#self.nexthops[ips[i]][">"] = self.ranges[ips[i]]
				self.nexthops[ips[i]] = {">":self.ranges[ips[i]]}
				self.nexthops[ips[i]].update({"=":self.ranges[ips[i]]})
			if self.labels[ips[i]] == "H":
				nexthop = s.pop()
				self.nexthops[ips[i]] = {"=": nexthop}
				if len(s):
					self.nexthops[ips[i]].update({">": s[-1]})
				else :
					self.nexthops[ips[i]].update({">": nexthop})
			i += 1
		#print self.nexthops
	def search(self,ip):
		return self.inner_search(int(math.ceil(len(self.ranges))/2),0,len(self.ranges),ip)

	def inner_search(self,index,prev_bound,next_bound,ip):
		#print "prev = {0}\nindex = {1}\nnext = {2}\n".format(prev_bound,index,next_bound)
		ip = ip[0:self.max_length]
		ips = self.ranges.keys()
		ips.sort()
		if ip == ips[index]: 
			return  self.nexthops[ips[index]]["="]
		if index == prev_bound or index == next_bound or next_bound-index <= 1:
			if ip == ips[index]: 
				return  self.nexthops[ips[index]]["="]
			if ip > ips[index] : 
				return  self.nexthops[ips[index]][">"]
			return None
		if ip > ips[index]:
			#print "up"
			nexthop = self.inner_search(int(math.ceil(float(next_bound-index)/2)),prev_bound,index,ip)
			if nexthop == None:
				nexthop = self.nexthops[ips[index]][">"]
		if ip <= ips[index]:
			#print "down"
			return self.inner_search(int(index-math.floor(float(index-prev_bound)/2)),index,next_bound,ip)
		return nexthop
'''
def main():
	print "start"
	max_length = 6
	
	bs = prefixLengthBS(max_length,{})
	#bs.generate()
	depth = int(math.ceil(math.log(max_length+2,2)))
	max_bound = int(math.pow(2,depth))
	root = int(math.floor( max_bound - 1)/2)
	bs.put_markers(root,0,max_bound-2)
	print bs.hash_table
	print "bs :{0} ".format(bs.search(""))
	expand_bs = prefixLengthExpandBS(max_length,{})
	expand_bs.set_expand_table()
	print expand_bs.expand_table
	print "ebs : {0}".format(expand_bs.search(""))
	filepath = os.path.dirname(__file__)+"/routingtable.txt"
	bspr = BSPrefixRange(filepath)
	bspr.make_ranges()
	bspr.precomputation()
	print bspr.search(int(math.ceil(len(bspr.ranges))/2),0,len(bspr.ranges),"10110000000")
if __name__ == '__main__':
    main()
'''
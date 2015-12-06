class Leaf:
	
	def __init__(self,label):
		self.data = label
	
	def label(self):
		return self.data
	
	def is_leaf(self):
		return True
	
	def height(self):
		return 0
			

class BinNode:
	
	def __init__(self,left,right):
		self.l = left
		self.r = right
	
	def is_leaf(self):
		return False
	
	def son(self,which):
	
		'''which - 'L' lub 'R'''
		
		if which == 'L':
			return self.l
		elif which == 'R':
			return self.r
	
	def graft(self,first,second):
		
		'''(first,second)-> None
		
		first, second -> 'L' lub 'R'
		Przeksztalca aktualne drzewo w drzewo do niego podobne wykonujac przeszczep w okreslonych w argumentach 
		first i second miejscach
		'''
		
		if first == 'L':
			if second == 'R':
				var = BinNode(self.son('R').son('R'),BinNode(self.son('R').son('L'),self.son('L')))
				self.l = var.l
				self.r = var.r
			elif second == 'L':
				var = BinNode(self.son('R').son('L'),BinNode(self.son('L'),self.son('R').son('R')))
				self.l = var.l
				self.r = var.r
		elif first == 'R':
			if second == 'R':
				var = BinNode(BinNode(self.son('L').son('L'),self.son('R')),self.son('L').son('R'))
				self.l = var.l
				self.r = var.r
			elif second == 'L':
				var = BinNode(BinNode(self.son('R'),self.son('L').son('R')),self.son('L').son('L'))
				self.l = var.l
				self.r = var.r
	
	
	def similar(self):
		'''similar od wierzcholka, wywoluje przeszczep na danym drzewie, pozniej przywraca je do stanu
		poczatkowego;
		zmienna var do zapamietania self.l i self.r aktualnie modyfikowanego drzewa
		'''
		var=BinNode(self.l,self.r)
		if not self.is_leaf():
			if not self.son('L').is_leaf():
				'''jesli lewy syn nie jest lisciem to mozna w nim dokonac przeszczepu zmieniajac drzewo
				'''
				for x in self.son('L').similar():
					yield self
				
				self.graft('R','L')
				yield self
				self.l=var.l
				self.r=var.r
				self.graft('R','R')
				yield self
				self.l=var.l
				self.r=var.r
			
			elif not self.son('R').is_leaf():
				'''przeszczep w prawym synie, ktory nie jest lisciem
				'''
				for x in self.son('R').similar():
					yield self
				
				self.graft('L','L')
				yield self
				self.l=var.l
				self.r=var.r
				self.graft('L','R')
				yield self
				self.l=var.l
				self.r=var.r
	
	def height(self):
		'''metoda height od wierzcholka
		'''
		if self.is_leaf():
			return 0
		else:
			return 1 + max(self.son('L').height(),self.son('R').height())

	
class BinTree:
	
	def __init__(self,node):
		self.n = node
	
	def root(self):
		return self.n
	
	def similar(self):
		'''similar od drzewa wypisuje drzewa podobne do aktualnego korzystajac z metody similar od wierzcholka
		'''
		for x in self.root().similar():
			print BinTree(x)
	
	def height(self):
		'''metoda height od drzewa
		'''
		return self.height1(self.root())
	
	def height1(self, node):
		if node.is_leaf():
			return 0
		else:
			return 1 + max(self.height1(node.son('L')),self.height1(node.son('R')))
	
	def max_height(self):
		'''przeksztalcenie drzewa w drzewo podobne o maksymalnej wysokosci;
		obiekt v jako zmienna do zapamietania x.l i x.r dla drzewa od wierzcholka x o wiekszej wysokosci
		'''
		max=self.height()
		v=BinNode(None,None)
		for x in self.root().similar():
			var=BinTree(x).height()
			if var>max:
				max=var
				v.l=x.l
				v.r=x.r
		self.n=v
		
	def min_height(self):
		'''przeksztalcenie drzewa w drzewo podobne o minimalnej wysokosci;
		obiekt v jako zmienna do zapamietania x.l i x.r dla drzewa od wierzcholka x o mniejszej wysokosci
		'''
		min=self.height()
		v=BinNode(None,None)
		for x in self.root().similar():
			var=BinTree(x).height()
			if var<min:
				min=var
				v.l=x.l
				v.r=x.r
		self.n=v

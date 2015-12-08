import copy
inf = float('inf')
#Znalezienie dla danego drzewa wszystkich drzew podobnych poprzez nni
#Policzenie dla kazdego z nich srednicy i wybranie tego o najmniejszej srednicy

class Leaf:

    def __init__(self,label):
        self.label = label

    def get_label(self):
        return self.label

    def is_leaf(self):
        return True

    def height(self):
        return 0

    def diameter(self):
        return 0


class BinNode:

    def __init__(self,left,right):
        self.l = left
        self.r = right
        self.parent = None

    def is_leaf(self):
        return False

    def son(self,which):

        if which == 'L':
            return self.l
        elif which == 'R':
            return self.r

    def height(self):
        if self.is_leaf():
            return 0
        else:
            return 1 + max(self.son('L').height(),self.son('R').height())

    def diameter(self):

        left_height = self.son("L").height()
        right_height = self.son("R").height()

        left_diameter = self.son("L").diameter()
        right_diameter = self.son("R").diameter()

        return max(left_height + right_height + 1, left_diameter, right_diameter)

    def nni(self,which):
        #przeksztalca aktualne drzewo w drzewo do niego podobne
        #which - trzy rodzaje zmiany
        if which != 1:
            if not self.son("L").is_leaf():
                #nni na krawedzi od self do jego lewego dziecka
                a = self.son("L").son("L")
                b = self.son("L").son("R")
                c = self.son("R")
                if which == 2:
                    var = BinNode(BinNode(a,c),b)
                    self.l = var.l
                    self.r = var.r
                else:
                    var = BinNode(BinNode(c,b),a)
                    self.l = var.l
                    self.r = var.r
            if not self.son("R").is_leaf():
                #nni na krawedzi od self do jego prawego dziecka
                a = self.son("R").son("R")
                b = self.son("R").son("L")
                c = self.son("L")
                if which == 2:
                    var = BinNode(b,BinNode(c,a))
                    self.l = var.l
                    self.r = var.r
                else:
                    var = BinNode(a,BinNode(b,c))
                    self.l = var.l
                    self.r = var.r

    def similar(self):
        #dla kazdej krawedzi w drzewie o korzeniu self znajduje nni
        #aktualne drzewo
        var=BinNode(self.l,self.r)
        for i in range(1,4):
            self.nni(i)
            yield self
            self.l=var.l
            self.r=var.r
        if not self.son("L").is_leaf():
            for x in self.son("L").similar():
                yield self
        if not self.son("R").is_leaf():
            for x in self.son("R").similar():
                yield self


class BinTree:

    def __init__(self,node):
        self.n = node

    def root(self):
        return self.n

    def get_cost(self):
        return self.root().get_cost()

    def height(self):
        return self.height1(self.root())

    def height1(self, node):
        if node.is_leaf():
            return 0
        else:
            return 1 + max(self.height1(node.son('L')),self.height1(node.son('R')))

    def diameter(self):
        self.root().diameter()

    def similar(self):
        min_tree_diameter = inf
        for x in self.root().similar():
            diameter = self.root().diameter()
            #print show(BinTree(x))
            #print diameter
            if diameter < min_tree_diameter:
                min_tree = copy.deepcopy(x)
                min_tree_diameter = diameter
        return BinTree(min_tree), min_tree_diameter

#print tree
def showR(node, prefix=''):
    if node.is_leaf():
        return prefix + '-' + node.get_label() + '\n'
    else:
        return showR(node.son('L'),prefix+'   ') + prefix + '-<' + '\n' + showR(node.son('R'),prefix+'   ')

def show(tree):
    return showR(tree.root())


#Przykladowe drzewo

t4 = BinTree(BinNode(BinNode(Leaf('A'),Leaf('B')),BinNode(Leaf('C'),BinNode(Leaf('D'),BinNode(Leaf('E'),Leaf('F'))))))
print 'Drzewo t4:'
print show(t4)
diameter = t4.root().diameter()
print diameter

print "NNI"
new_diameter = inf

while diameter < new_diameter:
    t, new_diameter = t4.similar()
print show(t)
print new_diameter


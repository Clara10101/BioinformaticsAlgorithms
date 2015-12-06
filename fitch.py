from Bio import SeqIO
records = list(SeqIO.parse("sekwencje.przyrownane.fasta", "fasta"))

sequences_length = len(records[0])

class Leaf:

    def __init__(self,label,sequence):
        self.label = label
        self.sequence = sequence
        self.minimal_residues = [[] for i in range(sequences_length)]
        self.cost = []

    def get_label(self):
        return self.label

    def is_leaf(self):
        return True

    def get_minimal_residues(self):
        return self.minimal_residues

    def get_cost(self):
        return self.cost

    def fitch(self):
        #dodanie aminokwasow znajdujacych sie na danych pozycjach w sekwencji
        for i in range(sequences_length):
            r = self.sequence[i]
            self.minimal_residues[i].append(r)
            self.cost.append(0)


class BinNode:

    def __init__(self,left,right):
        self.l = left
        self.r = right
        self.cost = []
        self.minimal_residues = [[] for i in range(sequences_length)]
        self.sequence = None

    def is_leaf(self):
        return False

    def son(self,which):

        '''which - 'L' lub 'R'''

        if which == 'L':
            return self.l
        elif which == 'R':
            return self.r

    def get_cost(self):
        return self.cost

    def get_minimal_residues(self):
        return self.minimal_residues

    def fitch(self):
        #wyznaczamy etykiety dla lewego i prawego dziecka
        left = self.son("L")
        right = self.son("R")
        left.fitch()
        right.fitch()
        r_left = left.get_minimal_residues()
        r_right = right.get_minimal_residues()
        c_left = left.get_cost()
        c_right = right.get_cost()
        for i in range(sequences_length):
            if set(r_left[i]).intersection(set(r_right[i])):
                #maja wspolne przeciecie
                r = list(set(r_left[i]).intersection(set(r_right[i])))
                cost = c_left[i] + c_right[i]
                self.minimal_residues[i].extend(r)
                self.cost.append(cost)
            else:
                r = list(set(r_left[i]).union(set(r_right[i])))
                cost = c_left[i] + c_right[i] + 1
                self.minimal_residues[i].extend(r)
                self.cost.append(cost)



class BinTree:

    def __init__(self,node):
        self.n = node

    def root(self):
        return self.n

    def get_cost(self):
        return self.root().get_cost()

    def fitch(self):
        return self.root().fitch()


#print tree
def showR(node, prefix=''):
    if node.is_leaf():
        return prefix + '-' + node.get_label() + '\n'
    else:
        return showR(node.son('L'),prefix+'   ') + prefix + '-<' + '\n' + showR(node.son('R'),prefix+'   ')

def show(tree):
    return showR(tree.root())

#trzy drzewa i policzenie dla nich kosztu algorytmem fitcha
#pierwsze drzewo
t1 = BinTree(BinNode(BinNode(Leaf(records[0].id,records[0].seq),Leaf(records[1].id,records[1].seq)),BinNode(Leaf(records[2].id,records[2].seq),Leaf(records[3].id,records[3].seq))))
print 'Drzewo t1:'
print show(t1)
print 'Koszt dla drzewa t1:'
t1.fitch()
print t1.get_cost()

#drugie drzewo
t2 = BinTree(BinNode(BinNode(Leaf(records[0].id,records[0].seq),Leaf(records[2].id,records[2].seq)),BinNode(Leaf(records[1].id,records[1].seq),Leaf(records[3].id,records[3].seq))))
print 'Drzewo t2:'
print show(t2)
print 'Koszt dla drzewa t2:'
t2.fitch()
print t2.get_cost()

#trzecie drzewo
t3 = BinTree(BinNode(BinNode(Leaf(records[0].id,records[0].seq),Leaf(records[3].id,records[3].seq)),BinNode(Leaf(records[1].id,records[1].seq),Leaf(records[2].id,records[2].seq))))
print 'Drzewo t3:'
print show(t3)
print 'Koszt dla drzewa t3:'
t3.fitch()
print t3.get_cost()
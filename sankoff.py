from Bio import SeqIO
records = list(SeqIO.parse("sekwencje.przyrownane.fasta", "fasta"))
import pam_matrix

sequences_length = len(records[0])
#zakladamy ze wszystkie sekwencje pochodza z multiuliniowienia i maja rowna dlugosc

inf = float('inf')

#klasa reprezentujaca drzewo binarne
class Leaf:

    def __init__(self,label,sequence):
        self.label = label
        self.sequence = sequence
        self.states = [[inf, inf, inf, inf] for i in range(sequences_length)]
        for i in range(sequences_length):
            aminoacid_index = ["A","C","T","G"].index(self.sequence[i])
            self.states[i][aminoacid_index] = 0

    def get_label(self):
        return self.label

    def is_leaf(self):
        return True

    def height(self):
        return 0


class BinNode:

    def __init__(self,left,right):
        self.l = left
        self.r = right
        self.states = [[0, 0, 0, 0] for i in range(sequences_length)]
        #podczas tworzenia wierzcholka obliczamy koszt dla czterech stanow

        for i in range(sequences_length):
            #dla kazdej kolumny uliniowienia
            for k in range(0,4):
                #dla kazdego z 4 stanow
                min_left = inf
                for j in range(0, 4):
                    #zamiana moze byc na 4 aminokwasy
                    cost = pam_matrix.macierz_pam[k][j] + left.states[i][j]
                    min_left = min(min_left, cost)
                min_right = inf
                for j in range(0, 4):
                    cost = pam_matrix.macierz_pam[k][j] + right.states[i][j]
                    min_right = min(min_right, cost)
                self.states[i][k] = min_left + min_right

    def is_leaf(self):
        return False

    def son(self,which):

        '''which - 'L' lub 'R'''

        if which == 'L':
            return self.l
        elif which == 'R':
            return self.r

    def get_cost(self):
        cost = 0
        for i in range(len(self.states)):
            #minimalny element w wierszu czyli koszt dla najlepszego stanu
            cost += min(self.states[i])
        return cost

class BinTree:

    def __init__(self,node):
        self.n = node

    def root(self):
        return self.n

    def get_cost(self):
        return self.root().get_cost()


#print tree
def showR(node, prefix=''):
    if node.is_leaf():
        return prefix + '-' + node.get_label() + '\n'
    else:
        return showR(node.son('L'),prefix+'   ') + prefix + '-<' + '\n' + showR(node.son('R'),prefix+'   ')

def show(tree):
    return showR(tree.root())

#trzy drzewa i policzenie dla nich kosztu algorytmem sankoffa
#pierwsze drzewo
t1 = BinTree(BinNode(BinNode(Leaf(records[0].id,records[0].seq),Leaf(records[1].id,records[1].seq)),BinNode(Leaf(records[2].id,records[2].seq),Leaf(records[3].id,records[3].seq))))
print 'Drzewo t1:'
print show(t1)
print 'Koszt dla drzewa t1:'
print t1.get_cost()

#drugie drzewo
t2 = BinTree(BinNode(BinNode(Leaf(records[0].id,records[0].seq),Leaf(records[2].id,records[2].seq)),BinNode(Leaf(records[1].id,records[1].seq),Leaf(records[3].id,records[3].seq))))
print 'Drzewo t2:'
print show(t2)
print 'Koszt dla drzewa t2:'
print t2.get_cost()

#trzecie drzewo
t3 = BinTree(BinNode(BinNode(Leaf(records[0].id,records[0].seq),Leaf(records[3].id,records[3].seq)),BinNode(Leaf(records[1].id,records[1].seq),Leaf(records[2].id,records[2].seq))))
print 'Drzewo t3:'
print show(t3)
print 'Koszt dla drzewa t3:'
print t3.get_cost()

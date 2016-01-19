class Leaf:

    def __init__(self,label):
        self.label = label

    def get_label(self):
        return self.label

    def is_leaf(self):
        return True

class BinNode:

    def __init__(self,left,right):
        self.l = left
        self.r = right
        self.label = None

    def is_leaf(self):
        return False

    def get_label(self):
        return self.label

    def son(self,which):

        if which == 'L':
            return self.l
        elif which == 'R':
            return self.r

    def get_leafs_labels(self):

        labels = []

        if self.son("R").is_leaf():
            labels.append(self.son("R").get_label())
        else:
            labels.extend(self.son("R").get_leafs_labels())

        if self.son("L").is_leaf():
            labels.append(self.son("L").get_label())
        else:
            labels.extend(self.son("L").get_leafs_labels())

        return labels

    def set_labels(self):

        self.label = self.get_leafs_labels()

        if not self.son("L").is_leaf():
            self.son("L").set_labels()

        if not self.son("R").is_leaf():
            self.son("R").set_labels()

    def lca_node(self,list,species_tree_node):

        if set(list).issubset(species_tree_node.get_label()):

            if species_tree_node.is_leaf():
                return species_tree_node

            if set(list).issubset(species_tree_node.son("L").get_label()):
                return self.lca_node(list,species_tree_node.son("L"))
            elif set(list).issubset(species_tree_node.son("R").get_label()):
                return self.lca_node(list,species_tree_node.son("R"))
            else:
                return species_tree_node
        else:
            return None

    def lca_mapping(self,species_tree):

        return self.lca_node(self.get_label(),species_tree.root())

    def duplication(self,species_tree):

        duplications = 0

        lca = self.lca_mapping(species_tree)
        lca_left = None; lca_right = None

        if not self.son("L").is_leaf():
            lca_left = self.son("L").lca_mapping(species_tree)
            duplications += self.son("L").duplication(species_tree)

        if not self.son("R").is_leaf():
            lca_right = self.son("R").lca_mapping(species_tree)
            duplications += self.son("R").duplication(species_tree)

        if lca == lca_left:
            duplications += 1

        if lca == lca_right:
            duplications += 1

        return duplications


class BinTree:

    def __init__(self,node):
        self.n = node

    def root(self):
        return self.n

    def set_labels(self):
        self.root().set_labels()

    def duplication(self,species_tree):
        return self.root().duplication(species_tree)


g = BinTree(BinNode(BinNode(BinNode(Leaf("A"),Leaf("B")),BinNode(Leaf("C"),Leaf("D"))),Leaf("E")))
g.set_labels()
s = BinTree(BinNode(BinNode(BinNode(Leaf("A"),BinNode(Leaf("B"),Leaf("D"))),Leaf("C")),Leaf("E")))
s.set_labels()

#print g.root().son("L").son("R").get_label()
#print g.root().son("L").son("R").lca_mapping(s).get_label()
print g.duplication(s)

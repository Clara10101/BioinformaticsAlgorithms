from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio import AlignIO
from Bio.Phylo.Consensus import *
from Bio import Phylo

clusters = 508
consensus_trees = []
#drzewa konsensusowe dla wszystkich klastrow

for i in [x for x in range(100,clusters) if x != 354]:
    msa = AlignIO.read('msa_klaster' + str(i) + '_s.fasta', 'fasta')
    calculator = DistanceCalculator('identity')
    dm = calculator.get_distance(msa)
    constructor = DistanceTreeConstructor(calculator, 'nj')
    trees = bootstrap_trees(msa, 50, constructor)

    trees_list = list(trees)
    not_included = set([])

    for j in range(len(trees_list)):
        target_tree = trees_list[j]
        support_tree = get_support(target_tree, trees_list)

        for node in support_tree.get_nonterminals():
            if node.confidence < 50:
                not_included.add(j)

    trees = [trees_list[k] for k in range(len(trees_list)) if k not in not_included]

    if len(trees) > 0:
        consensus_trees.append(majority_consensus(trees))

Phylo.write(consensus_trees,"drzewa_klastry","newick")



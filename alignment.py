__author__ = 'Klara'
inf = float('inf')

def scoring(residue1,residue2, gap_penalty = 2):

    if residue1 == residue2:
        return 1
    elif residue1 == '_' or residue2 == '_':
        return -1*gap_penalty
    else:
        return -1

def GlobalAlignmentNeedlemanWunsch(sequence1, sequence2, gap_penalty):

    n = len(sequence1)
    m = len(sequence2)
    M = [[0 for col in range(m+1)] for row in range(n+1)] #score of the alignment
    T = [[0 for col in range(m+1)] for row in range(n+1)] #to be used in traceback procedure

    for i in range(1,m+1):#boundary conditions
        M[0][i] = -1*i*gap_penalty
        T[0][i] = 'l'
    for j in range(1,n+1):
        M[j][0] = -1*j*gap_penalty
        T[j][0] = 'u'

    for i in range(1,n+1):
        for j in range(1,m+1):

            diagonal = M[i-1][j-1] + scoring(sequence1[i-1],sequence2[j-1],gap_penalty)
            left = M[i-1][j] - gap_penalty
            up = M[i][j-1] - gap_penalty
            max_value = max(diagonal,left,up)
            M[i][j] = max_value

            #pointers
            if diagonal == max_value:
                T[i][j] = 'd'
            elif left == max_value:
                T[i][j] = 'l'
            else:
                T[i][j] = 'u'

    score = M[n][m]

    #Traceback
    j,i = m,n
    AS1 = ''
    AS2 = ''
    while i > 0 and j > 0:
        if T[i][j] == 'd':
            AS1 = sequence1[i-1] + AS1
            AS2 = sequence2[j-1] + AS2
            i-=1
            j-=1
        elif T[i][j] == 'u':
            AS1 = '_' + AS1
            AS2 = sequence2[j-1] + AS2
            j -= 1
        else:
            AS2 = '_' + AS2
            AS1 = sequence1[i-1] + AS1
            i -=1

    while i > 0:
        AS1 = sequence1[i-1] + AS1
        AS2 = '_' + AS2
        i-=1
    while j > 0:
        AS1 = '_' + AS1
        AS2 = sequence2[j-1] + AS2
        j-=1

    return score, (AS1,AS2)

def LocalAlignmentSmithWaterman(sequence1, sequence2, gap_penalty):

    n = len(sequence1)
    m = len(sequence2)
    M = [[0 for col in range(m+1)] for row in range(n+1)]
    T = [[0 for col in range(m+1)] for row in range(n+1)]

    for i in range(1,m+1):
        T[0][i] = 'l'
    for j in range(1,n+1):
        T[j][0] = 'u'

    for i in range(1,n+1):
        for j in range(1,m+1):

            diagonal = M[i-1][j-1] + scoring(sequence1[i-1],sequence2[j-1],gap_penalty)
            left = M[i-1][j] - gap_penalty
            up = M[i][j-1] - gap_penalty
            max_value = max(diagonal,left,up,0)
            M[i][j] = max_value

            #pointers
            if diagonal == max_value:
                T[i][j] = 'd'
            elif left == max_value:
                T[i][j] = 'l'
            elif up == max_value:
                T[i][j] = 'u'

    score = 0
    score_row = 0
    score_column = 0

    for i in range(n+1):
        max_score = max(M[i])
        if score < max_score:
            score = max_score
            score_row = i
            score_column = M[i].index(max_score)

    #Traceback
    j,i = score_column,score_row
    AS1 = ''
    AS2 = ''
    while i > 0 and j > 0 and M[i][j] > 0:
        if T[i][j] == 'd':
            AS1 = sequence1[i-1] + AS1
            AS2 = sequence2[j-1] + AS2
            i-=1
            j-=1
        elif T[i][j] == 'u':
            AS1 = '_' + AS1
            AS2 = sequence2[j-1] + AS2
            j -= 1
        else:
            AS2 = '_' + AS2
            AS1 = sequence1[i-1] + AS1
            i -=1

    return score, (AS1,AS2)

#Alignment with affine gap model, score without traceback
def AffineGapModel(sequence1, sequence2, gap_opening_penalty, gap_extension_penalty):

    n = len(sequence1)
    m = len(sequence2)

    M = [[0 for col in range(m+1)] for row in range(n+1)]
    Ix = [[0 for col in range(m+1)] for row in range(n+1)]
    Iy = [[0 for col in range(m+1)] for row in range(n+1)]

    T = [[['',0] for col in range(m+1)] for row in range(n+1)]
    Tx = [[['',0] for col in range(m+1)] for row in range(n+1)]
    Ty = [[['',0] for col in range(m+1)] for row in range(n+1)]

    for i in range(1,m+1):
        M[0][i] = gap_opening_penalty + i*gap_extension_penalty
        T[0][i][0] = 'l'
        Ix[0][i] = -inf
        Iy[0][i] = -inf
    for j in range(1,n+1):
        M[j][0] = gap_opening_penalty + j*gap_extension_penalty
        T[j][0][0] = 'u'
        Ix[j][0] = -inf
        Iy[j][0] = -inf

    for i in range(1,n+1):
        for j in range(1,m+1):

            M_M = M[i-1][j-1] + scoring(sequence1[i-1],sequence2[j-1])
            M_Ix = Ix[i-1][j-1] + scoring(sequence1[i-1],sequence2[j-1])
            M_Iy = Iy[i-1][j-1] + scoring(sequence1[i-1],sequence2[j-1])
            max_M = max(M_M,M_Ix,M_Iy)

            #from which matrice
            if max_M == M_M:
                T[i][j][1] = 'M'
            elif max_M == M_Ix:
                T[i][j][1] = 'Ix'
            else:
                T[i][j][1] = 'Iy'

            M[i][j] = max_M
            if M_M == max_M:
                T[i][j][0] = 'd'

            I_M = M[i-1][j] - gap_opening_penalty
            I_Ix = Ix[i-1][j] - gap_extension_penalty
            max_Ix = max(I_M,I_Ix)

            if max_Ix == I_M:
                Tx[i][j][1] = 'M'
            else:
                Tx[i][j][1] = 'Ix'

            Ix[i][j] = max_Ix
            if I_Ix == max_Ix:
                Tx[i][j][0] = 'u'

            I_M = M[i][j-1] - gap_opening_penalty
            I_Iy = Iy[i][j-1] - gap_extension_penalty
            max_Iy = max(I_M,I_Iy)

            if max_Iy == I_M:
                Ty[i][j][1] = 'M'
            else:
                Ty[i][j][1] = 'Iy'

            Iy[i][j] = max_Iy
            if I_Iy == max_Iy:
                Ty[i][j][0] = 'd'

    score = max(M[n][m],Ix[n][m],Iy[n][m])
    print M
    print Ix
    print Iy
    print T
    print Tx
    print Ty

    j,i = m,n
    AS1 = ''
    AS2 = ''
    #while i > 0 and j > 0:

    return score

if __name__ == "__main__":

    seq1 = 'CTTAGA'
    seq2 = 'GTAA'
    gap_penalty = 2

    score, alignment = GlobalAlignmentNeedlemanWunsch(seq1,seq2,gap_penalty)
    print 'Global alignment of two sequences: ' + seq1 + ', ' + seq2
    print 'Score: ' + str(score)
    print 'Optimal alignment:\n' + alignment[0] + '\n' + alignment[1]

    score, alignment = LocalAlignmentSmithWaterman(seq1, seq2, gap_penalty)
    print 'Local alignment of two sequences: ' + seq1 + ', ' + seq2
    print 'Score: ' + str(score)
    print 'Optimal alignment:\n' + alignment[0] + '\n' + alignment[1]

    seq3 = 'HEAGAWGHEE'
    seq4 = 'PAWHEAE'

    score, alignment = LocalAlignmentSmithWaterman(seq3, seq4, gap_penalty)
    print 'Local alignment of two sequences: ' + seq3 + ', ' + seq4
    print 'Score: ' + str(score)
    print 'Optimal alignment:\n' + alignment[0] + '\n' + alignment[1]

    seq5 = 'ACGGTAC'
    seq6 = 'GAGGT'

    score = AffineGapModel(seq5,seq6,3,2)
    print score
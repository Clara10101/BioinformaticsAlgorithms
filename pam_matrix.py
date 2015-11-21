from Bio import SeqIO
records = list(SeqIO.parse("sekwencje.przyrownane.fasta", "fasta"))

wystapienia = [0,0,0,0]
dlugosc = len(records[0])
macierz_podstawien = [[0 for col in range(4)] for row in range(4)]

#zliczenie wystapien kazdego z aminokwasow we wszystkich sekwencjach
for i in range(len(records)):
	for p,j in enumerate(["A","C","T","G"]):
		wystapienia[p] += records[i].seq.count(j)

#zliczanie liczby wystapien pary (x,y) we wszystkich uliniowieniach		
for i in range(len(records)):	
	for j in range(len(records)):
		if i != j:
			for k in range(dlugosc):
				n_i = records[i].seq[k]
				n_j = records[j].seq[k]
				macierz_podstawien[["A","C","T","G"].index(n_i)][["A","C","T","G"].index(n_j)] += 1
				
#wzor do wyliczenia wartosci lambda
c = sum(float(wystapienia[x]) / sum(wystapienia) for x in range(4)) * sum(float(macierz_podstawien[x][y]) / sum(macierz_podstawien[x][z] for z in range(4)) for x in range(4) for y in range(4) if x != y)
#1pam - wymiana srednio 1% lacznej liczby reszt aminokwasowych
l = 0.01 / c

macierz_pam = [[0 for col in range(4)] for row in range(4)]

#macierz pam na podstawie wyliczonej wartosci lambda (l)
for i in range(4):
	for j in range(4):
		if i != j:
			macierz_pam[i][j] = l * macierz_podstawien[i][j] / sum(macierz_podstawien[i][x] for x in range(4))
#przekatne czyli prawdop ze aminokwas nie bedzie zastapiony zadnym innym w czasie 1pam
for i in range(4):
	for j in range(4):
		if i == j:
			macierz_pam[i][j] = 1 - sum(macierz_pam[i][x] for x in range(4) if x != i)
	


import subprocess
import multiprocessing

def runMuscle(muscle_num):
    seq_fasta = "sekwencje_klaster_" + str(muscle_num) + ".fasta"
    out_name = "msa_klaster" + str(muscle_num) + ".fasta"

    exec_muscle = "muscle3.8.31_i86win32" + " -in " + seq_fasta + " -fastaout " + out_name
    p = subprocess.Popen(exec_muscle, shell=True, stderr=subprocess.PIPE)
    p.communicate()

    return muscle_num

if __name__ == '__main__':

    numProcessors = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(numProcessors)

    cluster_num = 508 #liczba klastrow

    muscle_num = 0
    tasks = []

    while muscle_num <= cluster_num:
        tasks.append( (muscle_num, ) )
        muscle_num += 1

    # Run tasks
    results = [pool.apply_async( runMuscle, t ) for t in tasks]

    # Process results
    for result in results:
        m_num = result.get()
        print("Result for cluster %d written to phyi file" % (m_num))

    pool.close()
    pool.join()

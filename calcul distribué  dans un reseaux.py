import psutil,os,sys,time,numpy as np,ipyparallel


arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]
arg4 = sys.argv[4]


aFile = open(arg1, 'r+')
bFile = open(arg2, 'r+')
aN = int(aFile.readline())
bN = int(bFile.readline())
counter = 0


def find_process(name):
    for proc in psutil.process_iter():
        try: pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess: pass
        else:
            if name in pinfo["name"]:
                return pinfo, proc
    return None, None

if hasattr(sys, 'real_prefix'):
    exe = sys.real_prefix
else:
    exe = sys.base_exec_prefix
f = os.path.join(exe, "Scripts")



if find_process("ipcluster")[0] is None:
    print("start ipcluster")
    from pyquickhelper.loghelper import run_cmd
    if sys.platform.startswith("win"):
        cmd = os.path.join(f, "ipcluster")
    else:
        cmd = "ipcluster"
    cmd += " start -n 7"
    run_cmd(cmd, wait=False)
else:
    print("déjà démarré", find_process("ipcluster"))


time.sleep(5)



from ipyparallel import Client
clients = Client()
clients.block = True
print(clients.ids)







def genMatrix(inFile, d):
    datalines = inFile
    newMatrix = []

    for x in range(0,d):
        dataline = datalines.readline().split()
        for y in range(0,d):
            yVals = list(map(float, dataline))

        newMatrix.append(yVals)
    return newMatrix

def partitionMatrix(matrix):
    length = len(matrix)
    if(length % 2 is not 0):
        stack = []
        for x in range(length + 1):
            stack.append(float(0))
        length += 1
        matrix = np.insert(matrix, len(matrix), values=0, axis=1)
        matrix = np.vstack([matrix, stack])
    d = (length // 2)
    matrix = matrix.reshape(length, length)
    completedPartition = [matrix[:d, :d], matrix[d:, :d], matrix[:d, d:], matrix[d:, d:]]
    return completedPartition

def strassen(mA, mB):
    n1 = len(mA)
    n2 = len(mB)
    global aN
    if(n1 and n2 <= aN):
        return (mA * mB)
    else:
        print(mA)
        A = partitionMatrix(mA)
        B = partitionMatrix(mB)
        mc = np.matrix([0 for i in range(len(mA))]for j in range(len(mB)))
        C = partitionMatrix(mc)


        a11 = np.array(A[0])
        a12 = np.array(A[2])
        a21 = np.array(A[1])
        a22 = np.array(A[3])
        b11 = np.array(B[0])
        b12 = np.array(B[2])
        b21 = np.array(B[1])
        b22 = np.array(B[3])

        mone = clients[1].apply_sync (np.array(strassen((a11 + a22), (b11 + b22))))
        mtwo = clients[2].apply_sync(np.array(strassen((a21 + a22), b11)))
        mthree = clients[3].apply_sync(np.array(strassen(a11, (b12 - b22))))
        mfour = clients[4].apply_sync(np.array(strassen(a22, (b21 - b11))))
        mfive = clients[5].apply_sync(np.array(strassen((a11 + a12), b22)))
        msix = clients[6].apply_sync(np.array(strassen((a21 - a11), (b11 + b12))))
        mseven = clients[7].apply_sync(np.array(strassen((a12 - a22), (b21 + b22))))

        C[0] = np.array((mone + mfour - mfive + mseven))
        C[2] = np.array((mthree + mfive))
        C[1] = np.array((mtwo + mfour))
        C[3] = np.array((mone - mtwo + mthree + msix))

        return np.array(C)

matrixA = genMatrix(aFile, aN)
matrixB = genMatrix(bFile, bN)
matrixA = np.matrix(matrixA)
matrixB = np.matrix(matrixB)

matrixC = [[0 for i in range(len(matrixA))]for j in range(len(matrixA))]







if find_process("ipcluster")[0] is not None:
    print("stop ipcluster")
    from pyquickhelper.loghelper import run_cmd
    if sys.platform.startswith("win"):
        cmd = os.path.join(f, "ipcluster")
    else:
        cmd = "ipcluster"
    cmd += " stop"
    out, err = run_cmd(cmd, wait=True)
    print(out.replace(os.environ["USERNAME"], "USERNAME"))
else:
    print("aucun processus ipcluster trouvé")
import sys

string = str(open(sys.argv[1], "r").read().strip())
arr = string.split()
s = []
ending = ""
count = 0
empty = False


def printRule(count):
    if not(empty):
        print("p[0] = (", end='')
        for j in range(count):
            print("p[" + str(j+1) + "]", end='')
            if j+1!=count:
                print(", ", end='')
            else:
                print(")\n")
    else:
        print("p[0] = None\n")


for i,word in enumerate(arr):
    if word==":":
        if len(s)>0 and s[-1][0]==arr[i-1]:
            ending = "_" + str(s[-1][1]+1)
            s[-1][1]+=1
        else:
            ending = ""
            if len(s)>0:
                s.pop()
            s.append([arr[i-1],0])
        print("def p_" + arr[i-1] + ending + "(p):\n\t\'\'\'\n\t" + arr[i-1] + " : ",end ='')
        count = -1
    elif i+1<len(arr) and arr[i+1]!=":":
        if word=="~":
            word=" "
            empty = True
        else:
            empty = False
        print(word, end=' ')
    elif i+1==len(arr):
        count+=1
        print(word, end=' ')
        print("\n\t\'\'\'\n\t", end='')
        printRule(count)
    elif i!=0:
        print("\n\t\'\'\'\n\t", end='')
        printRule(count)
    count+=1
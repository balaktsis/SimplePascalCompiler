import sys

string = str(open(sys.argv[1],"r").read().strip())
arr = string.split()
s = []
ending = ""
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
    elif i+1<len(arr) and arr[i+1]!=":":
        if word=="~":
            word=" "
        print(word, end=' ')
    elif i!=0:
        print("\n\t\'\'\'\n\t" + "pass\n")

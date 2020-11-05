import sys
import time

filename=sys.argv[1]                # First Argument- Filename
min_sup=float(sys.argv[2])            # Second Argument-Minimum Support(in decimal)
min_conf =float(sys.argv[3])        #Third Argument-Minimum Confidence(in decimal)

with open("allcombinations.csv") as f:
    B_items = f.read().replace("\n", "").split(",")
    B_items.sort()

#Reading data from the file name and printing the data to the users
filedata=open(filename,"r")
data=filedata.readlines()
data=[l.replace("\n","").split(",") for l in data]
print("-------------------INPUT DATA------------------")
for d in data:
    print(d)

#Class for Apriori alogorithm
class A_Rule:
    def __init__(self,A_left,A_right,A_all):
        self.A_left=list(A_left)
        self.A_left.sort()
        self.A_right=list(A_right)
        self.A_right.sort()
        self.A_all=A_all

    def __str__(self):
        return ",".join(self.A_left)+" => "+",".join(self.A_right)


#Class for Brute Force alogorithm
class B_Rule:

    def __init__(self,B_left,B_right,B_all):
        self.B_left = list(B_left)
        self.B_left.sort()
        self.B_right = list(B_right)
        self.B_right.sort()
        self.B_all = B_all

    def __str__(self):
        return ",".join(self.B_left)+ " => "+",".join(self.B_right)

#generating all possible Sub-combinations for a rule
def A_generating_sub_rule(fs,r,result,support):
    r_size=len(r[0])
    t_size=len(fs)
    if t_size-r_size>0:
        r=B_generate_itemset(r)
        new_r=[]
        for i in r:
            l=fs-i
            if(len(l)==0):
                continue
            conf=support[fs]/support[l]
            if(conf>=min_conf):
                result.append([A_Rule(l,i,fs),support[fs],conf])
                new_r.append(i)

        if(len(new_r)>1):
            A_generating_sub_rule(fs,new_r,result,support)

#Generating Combinations for Itemset for Apriori
def B_generate_itemset(dk):
    res=[]
    for i in range(len(dk)):
        for j in range(i+1,len(dk)):
            l,r=dk[i],dk[j]
            ll,rr=list(l),list(r)
            ll.sort()
            rr.sort()
            if ll[:len(l)-1] == rr[:len(r)-1]:
                res.append(l | r)
    return res


#Generating Combinations for Itemset for Brute Force
def B_generate(items, k):

    if k == 1:
        return [[x] for x in items]

    all_res = []
    for i in range(len(items)-(k-1)):
        for sub in B_generate(items[i+1:], k-1):
            temp = [items[i]]
            temp.extend(sub)
            all_res.append(temp)
    return all_res


#Function used to scan the database to count frequency for Apriori
def A_scan(data,f1):
    count = {s:0 for s in f1}
    for i in data:
        for freqset in f1:
            if(freqset.issubset(i)):
                count[freqset]+=1
    n=len(data)
    return{freqset: support/n for freqset, support in count.items() if support/n>=min_sup}

#Function used to scan the database to count frequency for Brute Force
def B_scan(db,s):
    count = 0
    for t in db:
        if set(s).issubset(t):
            count += 1
    return count

##Start for Apriori alogorithm
print("-------------------------start Apriori---------------------------")
A_start_time = time.time()
support={}
item=[[]]
dk=[[]]
f1=set() #creating a set to hold all the data for scanning the data from the dictionary
for i in data:
    for items in i:
        f1.add(frozenset([items]))
item.append(f1)
count=A_scan(data,f1)
dk.append(list(count.keys()))
support.update(count)

t=1
while len(dk[t]) > 0:
    item.append(B_generate_itemset(dk[t]))
    count=A_scan(data,item[t+1])
    support.update(count)
    dk.append(list(count.keys()))
    t+=1


#generating the rules for Apriori Alogorithm
result=[]
for i in range(2,len(dk)):
    if(len(dk[i])==0):
        break
    frequent_set=dk[i]

    for fs in frequent_set:
        for r in [frozenset([x]) for x in fs]:
            l=fs-r
            conf=support[fs]/support[l]
            if conf>=min_conf:
                result.append([A_Rule(l,r,fs),support[fs],conf])
    if(len(frequent_set[0])!=2):
        for fs in frequent_set:
            r=[frozenset([x]) for x in fs]
            A_generating_sub_rule(fs,r,result,support)

result.sort(key=lambda x: str(x[0]))
A_end_time=time.time()
for k in result:
    print(k[0],k[1],k[2])
A_time=A_end_time - A_start_time


print("-------------------------start Brute force---------------------------")
#start for brute force algorithm
B_start_time = time.time()
B_frequent = []
B_support = {}
for k in range(1, len(B_items)+1):
    B_current = []
    for comb in B_generate(B_items, k):
        count = B_scan(data, comb)
        if count/len(data) >= min_sup:
            B_support[frozenset(comb)] = count/len(data)
            B_current.append(comb)
    if len(B_current) == 0:
        break
    B_frequent.append(B_current)


#generating all rules for Brute Force
all_rule = set()
B_all_result = []
for k_freq in B_frequent:
    if len(k_freq) == 0:
        continue
    if len(k_freq[0]) < 2:
        continue
    for freq in k_freq:
        for i in range(1, len(freq)):
            for left in B_generate(freq, i):
                tmp = freq.copy()
                right = [x for x in tmp if x not in left]
                all_rule.add(B_Rule(left, right, freq))
for rule in all_rule:
    B_confidence = B_support[frozenset(rule.B_all)] / B_support[frozenset(rule.B_left)]
    if B_confidence >= min_conf:
        B_all_result.append([rule, B_support[frozenset(rule.B_all)], B_confidence])

B_all_result.sort(key=lambda x: str(x[0]))
B_end_time = time.time()

for r in B_all_result:
    print(r[0], r[1], r[2])
print("\n---------------------------------- RUNNING TIME:----------------------------------")

#displaying the time calculated
B_time=B_end_time - B_start_time
print("Apriori took ",str(A_end_time - A_start_time) + "s")
print("Brute force took ",str(B_end_time - B_start_time) + "s")
print("Apriori Algorithm is ",str(B_time-A_time)," seconds faster than Brute Force Algorithm")

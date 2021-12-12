import csv
 
f = open('./HandInfo.csv','r')
rdr = csv.reader(f)

count = 0
entire = 0
for line in rdr:
  entire += 1
  if(line[9]==''):
    break
  if "palmar" in line[6] and line[9]=="1":
    count+=1
  if "dorsal" in line[6] and line[9]=="0":
    count+=1
f.close()

print(count / entire)
print(entire)
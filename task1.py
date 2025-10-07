
dict1 = {}
n1 = int(input("Enter number of elements in first dictionary: "))

for i in range(n1):
    key = input("Enter key: ")
    value = input("Enter value: ")
    dict1[key] = value
 
dict2 = {}
n2 = int(input("Enter number of elements in second dictionary: "))

for i in range(n2):
    key = input("Enter key: ")
    value = input("Enter value: ")
    dict2[key] = value
 
merged_dict = dict1.copy()    
merged_dict.update(dict2)    
print("Merged Dictionary:", merged_dict)

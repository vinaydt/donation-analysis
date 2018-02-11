
# coding: utf-8

# In[680]:

import pandas as pd
import numpy as np
import sys


# In[681]:

name = ['CMTE_ID','AMNDT_IND','RPT_TP','TRANSACTION_PGI','IMAGE_NUM','TRANSACTION_TP','ENTITY_TP','NAME','CITY','STATE',
         'ZIP_CODE','EMPLOYER','OCCUPATION','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID','TRAN_ID','FILE_NUM','MEMO_CD','MEMO_TEXT',
         'SUB_ID']


# In[683]:

dataset=pd.read_csv(sys.argv[1],delimiter="|",names=name, dtype=str)


# In[684]:

theFile = open(sys.argv[2], "r")
percentile = []
for val in theFile.read().split():
    percentile.append(float(val))
theFile.close()


# In[685]:

kthpercentile = percentile[0]


# In[686]:

reatainNames = ['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID']


# In[687]:

dataset = dataset[reatainNames]


# In[692]:

def processDataSet(data):
    data = data[data['OTHER_ID'].isnull()]
    data = data[data['CMTE_ID'].notnull()]
    data = data[data['TRANSACTION_AMT'].notnull()]
    data = data[data['ZIP_CODE'].str.len() >= 5]
    data = data[data['TRANSACTION_DT'].notnull()]
    data = data[data['TRANSACTION_DT'].str.len() == 8]
    data = data[data['NAME'].notnull()]
    data['ZIP_CODE_5'] =  data['ZIP_CODE'].str[:5]
    data['YEAR'] = data['TRANSACTION_DT'].str[4:]
    return data


# In[693]:

dataset = processDataSet(dataset)


# In[694]:

#dataset.head(15)


# In[695]:

def percentile(contributions):
    return np.percentile(contributions, kthpercentile, interpolation='nearest')


# In[696]:

def assignCurrentVariables(row):
    currentYear = row['YEAR']
    currentZipCode = row['ZIP_CODE_5']
    currentRecepient = row['CMTE_ID']
    assigned = True;
    return currentYear, currentZipCode, currentRecepient, assigned


# In[698]:

currentYear = None
currentZipCode = None
currentRecepient = None
assigned = False;

totalNoOfTransactionsReceived = 0;
totalAmountContributions = 0;
contributions =[]

dictionary = dict()

file = open(sys.argv[3],"w") 

for index, row in dataset.iterrows():
    key = row['NAME'] + row['ZIP_CODE_5']
    if key in dictionary:
        if(int(row['YEAR'])> dictionary[key] and assigned==False):
            currentYear, currentZipCode, currentRecepient,assigned =  assignCurrentVariables(row)
        if(row['YEAR']==currentYear and row['ZIP_CODE_5']==currentZipCode and row['CMTE_ID']==currentRecepient):
            totalNoOfTransactionsReceived += 1;
            totalAmountContributions +=  int(row['TRANSACTION_AMT'])
            contributions.append(int(row['TRANSACTION_AMT']))
            file.write(row['CMTE_ID']+"|"+row['ZIP_CODE_5']+"|"+row['YEAR']+"|"+str(percentile(contributions))+"|"+
                      str(totalAmountContributions)+"|"+str(totalNoOfTransactionsReceived)+"\n")
    else:
        dictionary[key] = int(row['YEAR'])
file.close()
    
        
        
    


# In[ ]:




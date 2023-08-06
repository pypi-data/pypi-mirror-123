# Import library
from revamp.functions import report

# Initiate object
descr = report(df=train)

# Call the object method
print(descr.summary())
print(descr.descriptive_analysis())
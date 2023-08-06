# KEEP IT

This is a **WORK IN PROGRESS**.

`keepit` provides advanced memoization to disk for functions.
In other words, it records the results of important functions between executions.

`keepit` saves the results of calling a function to disk, so calling the function with the exact same parameters will re-use the stored copy of the results, leading to much faster times.


Example usage:

```
import pandas as pd
from keepit import keepit

@keepit('myresults.tsv')
def expensive_function(number=1):
    df = pd.DataFrame()
    # Perform a really expensive operation, maybe access to disk?
    return df

# When a results file for the function does not exist
# this may take a long time
expensive_function(number=1)
# Now a myresults.tsv_{some hash) has been generated

# This is almost instantaneous:
expensive_function(number=1)

# Files are specific to each parameter execution, 
# so this will again take a long time:
expensive_function(number=42)
# After this, we should have two files, one for number=1, 
# and another one for number=42.

```





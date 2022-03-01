# price-list-comparison

Python script that compares pricing of quarterly catalog pricing and finds errors with customer pricing. 

Specific templates will be adhered to for this project. 

### Output

## Two Files
- US_MASTER_ANALYSIS: This file will contain the quarterly process for contracts team that compares the current quarterly market price compared to the last quarters market price
    - Will Require upload of both current quarters US Master from SNOW ticket AND last quarters file
- YYYYQQ_Customer_Price_List: This file will compare all customer specific pricing against the current quarters market price. This is only to be used identifying price errors done with in legacy system
    - Will Require upload of all customer specific pricing (no changes to output from legacy system)
    

### Possible enhancements

- GUI application will be created to allow users to upload excel documents required for script to run
    - Will include validation errors for user error feedback
    - Will run by an executable 
    - Will use PyQt5 


FILES FOR ORIGINAL PROJECT WILL NOT BE PROVIDED, BUT TEMPLATE WILL BE OUTSIDE PARTY WOULD LIKE TO USE THIS PROGRAM
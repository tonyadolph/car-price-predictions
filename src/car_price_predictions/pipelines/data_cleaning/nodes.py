"""
This is a boilerplate pipeline 'data_cleaning'
generated using Kedro 0.18.3
"""
import pandas as pd

def _getAdjustedMileage(row, verbose=False):

    """ 
        based upon stats: age, fueltype return adjusted average mileage
                
            fuelType	year => Avg Mileage / per year
            Petrol - 2020 => 5900
            Diesel - 2020 => 8400
            Petrol - 2019 => 6300
            Diesel - 2019 => 9400
            Other - 2019 => 7400
            Other - 2020 => 6800
            
        If a vehicle was 2020 (dataset age) - i.e. its new or almost new, I left mileage un-adjusted
        If a vehicle was older than 2020:
        if mileage <= 160: adjust mileage = mileage * 1000 making my example Passat above have an adjusted mileage of 80,000
        else if mileage > 160 < 1% of national average for the age / fuelType - delete the record

    """
    averages = {}
    averages["petrol"]={"2020": 5900, "2019": 6300}
    averages["diesel"]={"2020": 8400, "2019": 9400}
    averages["other"]={"2020": 6800, "2019": 7400}
    
    fuelType = None
    if row["fuelType"].lower() not in ["petrol","diesel"]:
        fuelType = "other"
    else:
        fuelType = row["fuelType"].lower()
        
    yearAvg = None
    if int(row["year"]) >= 2020:
        #yearAvg="2020"
        #age = 1
        return row["mileage"]
    else:
        yearAvg="2019"
        age = 2020 - int(row["year"])
     
    avg = averages[fuelType][yearAvg]
    expectedMileage = age * int(avg)

    
    if verbose:
        print(f"avg {avg} age {age} expectedMileage {expectedMileage}")
    if int(row["mileage"]) <= 160:
        return int(row["mileage"]) * 1000
    if int(row["mileage"]) < (expectedMileage * 0.01):
        # mark for deletion
        return 0
    # no need to adjust  
    return int(row["mileage"])

def clean_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """
    cleans ford.csv
    """
    sales.drop(sales[sales["engineSize"] == 0].index, inplace=True)

    sales["adjustedMileage"]=sales.apply(_getAdjustedMileage, axis = "columns")
    sales.drop(sales[sales["adjustedMileage"] == 0].index, inplace=True)
    sales.drop(["mileage"],axis=1,inplace=True)
    sales['model']=sales['model'].apply(lambda x: x.strip())
    
    return sales
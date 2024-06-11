import pickle #I actually learned this from stack overflow
import pandas as pd #the typical lybrary for machine learning

#head start: I am not an expert with python, so I did look up some dumb questions online, I sourced everything next to or before the code, with the keyword "SOURCE:"

class DataExtractor():

    def __init__(self, dataFile):
        #SOURCE: https://stackoverflow.com/questions/24906126/how-to-unpack-pkl-file
        #open the data (.pkl file) and name it f, then "unpickle" (load) the data and assign it to a variable named "data"
        with open(dataFile, "rb") as f:
            data = pickle.load(f)

        #turn the data into a dataframe, as it's easier to work with this way
        self.dataframe = pd.DataFrame(data)


    def clean_data(self):
        #read the expired_invoices text file and turn it into an array, for efficiency, to not read and create a list each time
        f = open("expired_invoices.txt")
        expired_invoices = list(f.read().split(","))
        #turn the list of strings into a list of integers
        expired_invoices = [eval(i) for i in expired_invoices] #SOURCE: https://www.geeksforgeeks.org/python-converting-all-strings-in-list-to-integers/
        #create a new dataframe variable to then turn into .csv file, I chose to do it like this, as I find it more convenient
        final_data = {"invoice_id" : [],
                        "created_on" : [],
                        "invoiceitem_id" : [],
                        "invoiceitem_name" : [], 
                        "type" : [], 
                        "unit_price": [],
                        "total_price" : [],
                         "percentage_in_invoice": [],
                         "is_expired" : []
        }

        #current row of the final df, as it will have more rows than 100 (given by the data), as each "items" column holds more than 1 item
        final_df_row = 0

        #an array of column names that should be added for the .csv file
        list_of_new_columns = ["invoiceitem_id", "invoiceitem_name", "type", "unit_price", "total_price", "percentage_in_invoice", "is_expired"]
        
        for row in range(len(self.dataframe)):
            for column in self.dataframe:

                if column == "id":
                    id = self.dataframe[column][row]
                    #I have noticed that some id's have an "O" at the end, it needs to get removed for the id to become an integer
                    if isinstance(id, str): #found this function online, SOURCE: https://www.geeksforgeeks.org/check-if-a-variable-is-string-python/
                        #remove the last element (which is the "O")
                        id = int(id[:-1])


                elif column == "items":
                    items = self.dataframe[column][row]
                    
                    #we have to do a check, as there is some missing data on some rows
                    if isinstance(items, list):

                        #the total cost of all items in this invoice
                        invoice_total = 0
                        for item in items:
                            invoice_total += item["item"]["unit_price"] * self.fix_quantity(item["quantity"])

                        #iterate through each item dictionary
                        for item in items:
                            final_data["created_on"].append(self.dataframe["created_on"][row])
                            final_data["invoice_id"].append(id)

                            



                            #iterate through each item's attributes, but it could be the quality attribute, so we must check
                            for i in list(item.values()):
                                if isinstance(i, dict):
                                    for k in list(i.keys()):

                                        if k == "id":
                                            final_data["invoiceitem_id"].append(i[k])
                                        elif k == "name":
                                            final_data["invoiceitem_name"].append(i[k])
                                        elif k == "unit_price":
                                            final_data[k].append(i[k])
                                        else : # type
                                            if i[k] == 0 or i[k] == 'O': #there is some data that is "O" insttead of 0
                                                final_data[k].append("Material")
                                            elif i[k] == 1:
                                                final_data[k].append("Equipment")
                                            elif i[k] == 2:
                                                final_data[k].append("Service")
                                            else:
                                                final_data[k].append('Other')
                                else:
                                    quantity = self.fix_quantity(i)

                                    #some quantities are strings and "magic numbers", which are < 0
                                    #in the case where the quantity is < 0, I turned it into 0
                                    
                                    
                                    
                                    final_data["total_price"].append(item["item"]["unit_price"] * quantity)
                                    final_data["percentage_in_invoice"].append(item["item"]["unit_price"] * quantity / invoice_total)
                                    
                                    is_expired = False
                                    if id in expired_invoices:
                                        is_expired = True

                                    final_data["is_expired"].append(is_expired)
                                    
                


        #FINALLY, create the final dataframe, sort it by the invoice id and the item id and return it to get turned into a csv file later
        #These were the most stressful 2 hours of my life (I may have used an extra 5-10 minutes without noticing the time, hopefully that's not a big deal :) )
        final_dataframe = pd.DataFrame(final_data)
        final_dataframe = final_dataframe.sort_values(["invoice_id", "invoiceitem_id"]) #SOURCE: https://stackoverflow.com/questions/17141558/how-to-sort-a-pandas-dataframe-by-two-or-more-columns
        return final_dataframe


    #creates a new .csv file named "invoices.csv" after cleaning the data
    def convert_data_to_csv(self):
        df = self.clean_data()
        df.to_csv("invoices.csv")
        print("Successfully converted to csv!")

    
    #helper functions
    def fix_quantity(self, quantity):
        if isinstance(quantity, str):
            if quantity.lower() == "zero":
                quantity = 0
            elif quantity.lower() == "one":
                quantity = 1
            elif quantity.lower() == "two":
                quantity = 2
            elif quantity.lower() == "three":
                quantity = 3
            elif quantity.lower() == "four":
                quantity = 4
            elif quantity.lower() == "five":
                quantity = 5
            elif quantity.lower() == "six":
                quantity = 6
            elif quantity.lower() == "seven":
                quantity = 7
            elif quantity.lower() == "eight":
                quantity = 8
            elif quantity.lower() == "nine":
                quantity = 9
            elif quantity.lower() == "ten":
                quantity = 10
        elif quantity < 0:
            quantity = 0

        return quantity


#create a data extractor class
dataExtractor = DataExtractor("invoices_new.pkl")

#create a csv file with the data
dataExtractor.convert_data_to_csv()
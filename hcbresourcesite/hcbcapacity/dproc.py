from .models import api_proj_list, summaryTable
from  datetime  import datetime as dt

class dProcess:    
       
    def apiDataPreProcessor(self, dset, dic_index):                
        cn = 0
        data_loader = list()     

    
        for values in dset[dic_index]:
            
            d = (dset[dic_index][values])
            if values == "Key":
            #validate if this value already exists in the db and then execute break.                   
                if api_proj_list.objects.filter(project_key=d).exists(): 
                    return 
                else: 
                    data_loader.append(d)                        
            elif cn in range(10, 27) and d != 'None':
                    date_fixer = d[:10]
                    final_date = dt.strptime(date_fixer, '%Y-%m-%d')
                    data_loader.append(final_date)
            elif cn in range(10, 27) and d == 'None':
                    d = None
                    data_loader.append(d)
            else:                    
                    data_loader.append(d)            
                
            cn += 1

        return data_loader 


    def summaryDataPreProcessor(self, dset, dic_index):                
        cn = 0
        data_loader = list()
        nonecntr = 0        


        for values2 in dset[dic_index]:
                    d2 = (dset[dic_index][values2])
                    
                    if values2 == 'Survey Setup Start Date' and d2 == 'None':
                        nonecntr += 1
                    elif values2 == 'Admin_Start' and d2 == 'None':
                        nonecntr += 1
                    elif values2 == 'Admin_End' and d2 == 'None':
                        nonecntr += 1
                    elif values2 == 'EES Start Date' and d2 == 'None':
                        nonecntr += 1
                    elif values2 == 'EES Submission End Date' and d2 == 'None':
                        nonecntr += 1
                    elif values2 == 'EES First Results Release Date' and d2 == 'None':
                        nonecntr += 1              

        if nonecntr >= 4:
            return
        else:             
    
            for values in dset[dic_index]:
                
                d = (dset[dic_index][values])
                if values == "Key":
                #validate if this value already exists in the db and then execute break.                   
                                      
                    if summaryTable.objects.filter(project_key_forecast_id=d).exists():
                        return
                    else: 
                        data_loader.append(d)                        
                elif cn in range(10, 27) and d != 'None':
                        date_fixer = d[:10]
                        final_date = dt.strptime(date_fixer, '%Y-%m-%d')
                        data_loader.append(final_date)
                elif cn in range(10, 27) and d == 'None':
                        d = None
                        data_loader.append(d)
                else:                    
                        data_loader.append(d)            
                    
                cn += 1

            return data_loader               
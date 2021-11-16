from collections import OrderedDict
from  datetime  import datetime as dt, timedelta
from .models import api_proj_list, da_list
from .dbsave import dbStore


class forecastTblPreProcess:
    
    def hoursDistributor(self, n, r, k, h, s, e):
            dbstorer = dbStore()
            i = 0            
            d = [str(s)[:10],str(e)[:10]]            


            proj_yr_extract = int(str(s)[:4])
            proj_yr_extract_2 = int(str(e)[:4])

            #extract month names based on the date range provided.
            start, end = [dt.strptime(_, "%Y-%m-%d") for _ in d]
            mon_extract = OrderedDict(((start + timedelta(_)).strftime(r"%b"), None) for _ in range((end - start).days)).keys()
            print("this is month extract:", mon_extract)
        
            print("This is the type of s and e", type(s))

            while proj_yr_extract < proj_yr_extract_2:
                
               
                data_loader2 = {}
                data_loader2['project_key_forecast_id'] = n            
                data_loader2['sub_region'] = da_list.objects.values_list('region', flat=True).get(da_name=k)
                print(data_loader2['sub_region'])
                data_loader2['delivery_analyst'] = k               
                data_loader2['project_year'] = proj_yr_extract
                #distributes the hours based on the dates specified.
                
                while i < len(mon_extract):
                    
                    
                    xtractor = (list(mon_extract)[i]) 
                    if xtractor != 'Jan':                   
                        data_loader2[xtractor] = (h/len(mon_extract))
                    else:
                     break            
                    i+=1
                
                dbstorer.summaryTblUpdate(data_loader2)
                proj_yr_extract +=1
                
            else:
                data_loader2 = {}
                data_loader2['project_key_forecast_id'] = n            
                data_loader2['sub_region'] = da_list.objects.values_list('region', flat=True).get(da_name=k)
                print(data_loader2['sub_region'])
                data_loader2['delivery_analyst'] = k    

                data_loader2['project_year'] = proj_yr_extract_2

                while i < len(mon_extract):
                    xtractor = (list(mon_extract)[i])
                    data_loader2[xtractor] = (h/len(mon_extract))
                    
                    i += 1 
                dbstorer.summaryTblUpdate(data_loader2)

            
            
            #return data_loader2 
   
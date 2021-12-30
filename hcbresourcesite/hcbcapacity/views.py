from os import error, terminal_size
from django.db.models.aggregates import Avg
from django.db.models.expressions import F, Subquery
from django.db.models.fields import IntegerField
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Sum, Count, Q, FloatField
from django.http import HttpResponse, HttpResponseRedirect
from .models import api_proj_list, summaryTable, std_hours, daProdByMonth, daAverageProd
from django.template import loader
from django.core.exceptions import ValidationError
from .forms import UpdateApiProjectList
from .preprocess import forecastTblPreProcess
from .dbsave import dbStore
from .dproc import dProcess
from jira import JIRA, JIRAError
from collections import OrderedDict
import random
from  datetime  import datetime as dt, timedelta
import json
import psycopg2

# Create your views here.
def index(request):
    latest_project_list = api_proj_list.objects.exclude(Q(proj_status__exact='Completed') | Q(proj_status__exact='On Hold')).order_by('admin_start')
    
    print(type(latest_project_list))
    
    context = {
        'latest_project_list' : latest_project_list,
    }
    
    return render(request,'hcbcapacity/index.html', context)

def pie_chart(request):
    
    print("This is a request.", request)    

    if request.method == 'GET':
       projyr = request.GET["project_yr"]
       daProd = daProdByMonth.objects.filter(project_year__exact = projyr)
   
       
    print("This is the daprod", daProd)
  
    #for pie chart.
    labels_pie = []
    data_pie = []

    #for projstat data.
    labels_stat_pie = []
    data_stat_pie = []

    #for bar chart
    labels_bar = []
    data_bar = []

    #for area chart. Plotting data for the area chart.
    data_area = []

    #create queries for the specific areas in the dashboard.
    queryset_pie = api_proj_list.objects.filter(project_year__exact=projyr).values('sub_region').exclude(Q(proj_status__exact='Completed') | Q(proj_status__exact='On Hold')).annotate(da_hours=Sum('da_hours'))    

    queryset_bar = api_proj_list.objects.values('delivery_analyst').exclude(Q(proj_status__exact='Completed') | Q(proj_status__exact='On Hold')).annotate(proj_per_da=Count('project_key'))

    #Get anticipated prod percentage from the team based on the number of hours and the standard hours.
    queryset_std_hours = std_hours.objects.annotate(stdhours=(Sum('no_of_hours')*0.75)).values()
    print("These are the total hours for the year.", queryset_std_hours) 

    #query_avg_prod = daProdByMonth.objects.filter(project_year__exact=projyr).aggregate(avr_prod=((Avg(F('jan')), Avg(F('feb')), Avg(F('mar')), Avg(F('apr')), Avg(F('may')), #Avg(F('jun')), Avg(F('jul')), Avg(F('aug')), Avg(F('sep')), Avg(F('oct')), Avg(F('nov')), Avg(F('dece')))))
    
    #print('This is average prod', query_avg_prod)

    queryset_area_da_hours = daAverageProd.objects.filter(project_year=projyr).values()
    
    print("This is the average prod of the DAs", queryset_area_da_hours)
   

    #Create a query for the specific month

    
    query_average_jan = daProdByMonth.objects.filter(project_year__exact=projyr).exclude(Q(jan__exact = 0)).aggregate(jan=Avg('jan'))
    query_average_feb = daProdByMonth.objects.filter(project_year__exact=projyr).exclude(Q(feb__exact = 0)).aggregate(feb=Avg('feb'))
    query_average_mar = daProdByMonth.objects.filter(project_year__exact=projyr).exclude(Q(mar__exact = 0)).aggregate(mar=Avg('mar'))
    query_average_apr = daProdByMonth.objects.filter(project_year__exact=projyr).exclude(Q(apr__exact = 0)).aggregate(apr=Avg('apr'))
    query_average_may = daProdByMonth.objects.filter(project_year__exact=projyr).exclude(Q(may__exact = 0)).aggregate(may=Avg('may'))
    query_average_jun = daProdByMonth.objects.filter(project_year__exact=projyr).exclude(Q(jun__exact = 0)).aggregate(jun=Avg('jun'))
    query_average_jul = daProdByMonth.objects.filter(project_year__exact=projyr).exclude(Q(jul__exact = 0)).aggregate(jul=Avg('jul'))
    query_average_aug = daProdByMonth.objects.filter(project_year__exact=projyr).exclude(Q(aug__exact = 0)).aggregate(aug=Avg('aug'))
    query_average_sep = daProdByMonth.objects.filter(project_year__exact=projyr).exclude(Q(sep__exact = 0)).aggregate(sep=Avg('sep'))
    query_average_oct = daProdByMonth.objects.filter(project_year__exact=projyr).exclude(Q(oct__exact = 0)).aggregate(oct=Avg('oct'))
    query_average_nov = daProdByMonth.objects.filter(project_year__exact=projyr).exclude(Q(nov__exact = 0)).aggregate(nov=Avg('nov'))
    query_average_dec = daProdByMonth.objects.filter(project_year__exact=projyr).exclude(Q(dece__exact = 0)).aggregate(dece=Avg('dece'))
 
    print('This is the average for Jan', query_average_jan.get("jan"))
       

    data_area.append((query_average_jan.get("jan")))
    data_area.append((query_average_feb.get("feb")))
    data_area.append((query_average_mar.get("mar")))
    data_area.append((query_average_apr.get("apr")))
    data_area.append((query_average_may.get("may")))
    data_area.append((query_average_jun.get("jun")))
    data_area.append((query_average_jul.get("jul")))
    data_area.append((query_average_aug.get("aug")))
    data_area.append((query_average_sep.get("sep")))
    data_area.append((query_average_oct.get("oct")))
    data_area.append((query_average_nov.get("nov")))
    data_area.append((query_average_dec.get("dece")))

    data_area_final = [0 if n == None else round(n) for n in data_area ]

    print('This is the consolidated data_area', data_area)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    
    #This is for the project counts by DA.
    project_count = api_proj_list.objects.exclude(Q(proj_status__exact='Completed') | Q(proj_status__exact='On Hold')).aggregate(proj_count=Count('project_key'))
    
    #count of projects based on project status.
    proj_stat = api_proj_list.objects.filter(project_year__exact=projyr).values('proj_status').annotate(proj_count=Count('proj_status'))    
    
    proj_wo_da = api_proj_list.objects.filter(Q(delivery_analyst__exact='None') & Q(project_year__exact=projyr)).exclude(Q(proj_status__exact='Completed') | Q(proj_status__exact='On Hold')).count()

    proj_w_da = api_proj_list.objects.exclude(delivery_analyst__exact='None').exclude(Q(proj_status__exact='Completed') | Q(proj_status__exact='On Hold')).count()
    
    #This is for the project status pie chart:
    for case_pie_proj_stat in proj_stat:
        for stat_key, stat_value in case_pie_proj_stat.items():
            if stat_key == 'proj_status':
                labels_stat_pie.append(stat_value)                
            else:
                data_stat_pie.append(stat_value)             


    #This is for the pie chart.
    for case_pie in queryset_pie:
        for da_key, da_value in case_pie.items():
            if da_key == 'sub_region' and da_value != None:
                labels_pie.append(da_value)                
            elif da_value != None:
                data_pie.append(da_value)
    
    #This is for the bar chart.
    for case_bar in queryset_area_da_hours:
        for da_key, da_value in case_bar.items():
            if da_key == 'delivery_analyst' and da_value != None:
                labels_bar.append(da_value)                
            elif da_key == 'average_prod':
                data_bar.append(round(da_value))



    context = {
        'labels_pie' : labels_pie,
        'data_pie' : data_pie,
        'labels_stat_pie': labels_stat_pie,
        'data_stat_pie':data_stat_pie,
        'labels_bar': labels_bar,
        'data_bar' : data_bar,
        'labels_area': months,
        'data_area' : data_area_final,
        'proj_count' : project_count['proj_count'],
        'proj_wo_da' : proj_wo_da,
        'proj_w_da' : proj_w_da,
        'daProd' : daProd,
    }

    return render(request, 'hcbcapacity/pie_chart.html', context)

def proj_without_da(request):

   
    list_projects_wo_da = api_proj_list.objects.filter(delivery_analyst__exact='None').exclude(Q(proj_status__exact='Completed') | Q(proj_status__exact='On Hold') | 
    Q(complexity__exact='2b. License + support for managed project (Lite/Base + Premium)')).order_by('admin_start')

    
    context = {
        'list_projects_wo_da' : list_projects_wo_da,
    }

    return render(request, 'hcbcapacity/projwoda.html', context)


def daProjects(request, prod_id):

    if request.method == 'GET':
        da_prod = daProdByMonth.objects.filter(prod_id__exact=prod_id).values('delivery_analyst')
       
        dafilter = da_prod[0]['delivery_analyst']
        print(dafilter)      

    list_projects_w_da = api_proj_list.objects.filter(delivery_analyst__contains=dafilter).order_by('admin_start')
   
    context = {
        'list_projects_w_da' : list_projects_w_da,
    }

    return render(request,'hcbcapacity/projwda.html', context)


def enter_info(request):
    
    #first, create and initiate a form instance of the API project.
    #form = UpdateApiProjectList()

    #Generate a project key for from the entry form.
    forkey_gen = (random.random()*1000)
    forkey = int(forkey_gen)
    x=(f'A1-{forkey}')
    
    preProc = forecastTblPreProcess()
    dbStorer = dbStore()

    if request.method == 'POST':
       
        # this is used to check if the request.POST is indeed passing off work in the post
        #print('This is the POST:', request.POST)
        
        #pass on the POST request back to the initialized form. 
        form = UpdateApiProjectList(request.POST)        #print('this is the type of form:', type(form))

        print('This is the summary value', form['summary'].value())
        
        # Create a form instance and populate it with data from the request (binding):
        if form.is_valid():
            
            form.save()        
            project_key = form['project_key'].value()
            delivery_analyst = form['delivery_analyst'].value()
            created = form['created'].value()
            sub_reg = form['sub_region'].value()
            
            survey_start_dt = form['survey_setup_start_date'].value()
            ad_start_dt = form['admin_start'].value()
            ad_end_dt = form['admin_end'].value()
            ees_start_dt = form['ees_start_date'].value()
            ees_submission_dt = form['ees_submission_end_date'].value()
            ees_first_res_dt = form['ees_first_results_release_date'].value()
            hours = float(form['da_hours'].value())
                
            #Project Management
            pm = preProc.hoursDistributor(project_key, sub_reg, delivery_analyst, (hours * 0.3), created, ees_first_res_dt)
            print("This is for project management", pm)
            dbStorer.summaryTblUpdate(pm)
            #survey design and production
            sdp = preProc.hoursDistributor(project_key, sub_reg, delivery_analyst,(hours*0.25),survey_start_dt,ad_start_dt)
            dbStorer.summaryTblUpdate(sdp)
            #survey admin
            adm = preProc.hoursDistributor(project_key, sub_reg, delivery_analyst,(hours*0.10),ad_start_dt,ad_end_dt)
            dbStorer.summaryTblUpdate(adm)
            #Data Processing
            dProc = preProc.hoursDistributor(project_key,sub_reg, delivery_analyst,(hours*0.25),ees_start_dt,ees_submission_dt)
            dbStorer.summaryTblUpdate(dProc)
            #results rollout
            resRollout = preProc.hoursDistributor(project_key,sub_reg, delivery_analyst,(hours*0.10),ees_submission_dt,ees_first_res_dt)
            dbStorer.summaryTblUpdate(resRollout)
        else:
            form = UpdateApiProjectList()
            #Look at all of the keys in the api project list and create a list of it.       
           
        return HttpResponseRedirect(reverse('hcbcapacity:index'))   
        
    else:
        
       form = UpdateApiProjectList(initial={'project_key': x})


    return render(request,'hcbcapacity/enterinfo.html', {'form': form})
   

def update_api_table(request):

    

    if request.method == 'POST':

       """ #first connect the JIRA api.
        jira_connect = JIRA('http://jira.ehr.com/',basic_auth=('MICHA557', 'Mike&Rose22'))

        #store the JQL in a request variable.
        jql_request = 'issuetype in ("Survey Request", "Project Initiation") AND summary !~ test AND summary !~ "pulse product" AND created >= startOfYear() AND created <= endOfYear() AND ("Project Type" in ("Traditional Survey (Confirmit)", "Managed EES / Pulse License / Pulse License + Additional Services") OR "Contract Type" in ("2b. License + support for managed project (Lite/Base + Premium)", "3. Managed projects on EES")) AND status not in (Closed, Cancelled, Completed) ORDER BY created DESC'

        #load all the fileds and map the respective custom field to the namefields.
        allfields = jira_connect.fields()
        nameMap = {field['name'] : field['id'] for field in allfields}


        #list down the custom columns that you'd like to display. Then pass the list to the getattr method.
        custom_name = ['Project Type','Contract Type','Summary','Sub-Region','Status','Complexity','Delivery Analyst','Configuration Analyst','Production Analyst','Created','Hierarchy Setup Start Date','Hierarchy Setup Submission Date','Survey Setup Start Date','Survey Setup Submission to CSD Date','Tech Pretest Start Date','Tech Pretest End Date','Survey Lockdown Start Date','Survey Lockdown End Date','Admin Start','Admin End','MDB Setup Start Date','MDB Setup Submission Date','EES Start Date','EES Submission End Date','EES First Results Release Date','EES Second Results Release Date','DA Hours','CA Hours','PA Hours']

        #Initialize a main list where the data is stored.
        dt_main = []


        #a function which builds the list together with the equivalent custom names.
        def get_fields(issue_key):
            dt2=[]
            issue_val = jira_connect.issue(issue_key)
            dt2.append('Key')
            dt2.append(str(issue_val))
            cn = 0
            while cn < len(custom_name):
                custom_names = custom_name[cn]                
                
                get_val=getattr(issue_val.fields , nameMap[custom_names])  


                dt2.append(custom_names)
                
                if cn == 6 and get_val != None:           
                    info = issue_val.fields.customfield_25433
                    da = ','.join(str(v) for v in info)
                    dt2.append(da)
                elif cn == 7 and get_val != None:
                    info = issue_val.fields.customfield_25434
                    ca = ','.join(str(v) for v in info)
                    dt2.append(ca)
                elif cn == 8 and get_val != None:
                    info = issue_val.fields.customfield_25435
                    pa = ','.join(str(v) for v in info)
                    dt2.append(pa)
            
                else:
                
                    dt2.append(str(get_val))               
                
                cn += 1
                
            dt2_merge = iter(dt2)
            dt2_dict = dict(zip(dt2_merge, dt2_merge))

            dt_main.append(dt2_dict)
        
            return dt_main

        print(dt_main)

        #Return list of issues from the JQL request.
        block_size = 100
        block_num =0
        while True:
            start_idx=block_num*block_size
            issues = jira_connect.search_issues(jql_request, start_idx, block_size)
            
            if len(issues) == 0:
                break
            block_num += 1
            #loop through the list of loaded issues and make changes in the 
            for issue in issues:        
                get_fields(str(issue.key))
            

        with open("sample.json", 'w') as outfile:
            json.dump(dt_main, outfile) """

        #open JSON file containing JIRA extract:
        with open('sample.json','r') as f:
             dataset = json.load(f)

        preProc = forecastTblPreProcess()
        dpreProc = dProcess()
        dataframe = list()
        dbStorer = dbStore()

        def summaryTblExtractor(x):
            
            projkey = (x[0])
            sr = (x[4])
            da = (x[7])
            da_list = da.split(",")                      
            #created placeholder.
            cr = (x[10])
            #survey setup start date placeholder.
            survey_start_dt = (x[13])
            #admin start placeholder
            ad_start_dt = (x[19])
            #admin end placeholder
            ad_end_dt = (x[20])
            #ees start placeholder
            ees_start_dt = (x[23])
            #ees submission placeholder
            ees_submission_dt = (x[24])
            #ees first results date
            ees_first_res_dt = (x[25])
            print(ees_first_res_dt is None)
            #da hours
            if len(da_list) > 1:
                hours = (float(x[27]))/len(da_list)
            else:
                hours = (float(x[27]))          
            

        
            cnt = 0
            da_cnt = 0
            while da_cnt < len(da_list):
                cnt = 0 
                if da_list[da_cnt] != "None":          
                    while cnt <= 4:                        
                            if cnt == 0:
                                if ees_first_res_dt is not None:                               
                                    summary = preProc.hoursDistributor(projkey, sr, da_list[da_cnt], (hours * 0.30), cr, ees_first_res_dt)                                    
                                    #dbStorer.summaryTblUpdate(summary)
                                elif ees_submission_dt is not None:
                                    summary = preProc.hoursDistributor(projkey , sr, da_list[da_cnt], (hours * 0.40), cr, ees_submission_dt)
                                    #dbStorer.summaryTblUpdate(summary)
                                elif ad_end_dt is not None:
                                    summary = preProc.hoursDistributor(projkey, sr, da_list[da_cnt], (hours * 0.65), cr, ad_end_dt)
                                    #dbStorer.summaryTblUpdate(summary)                           
                                else:
                                    summary = None
                                    break
                            elif cnt == 1:
                                if survey_start_dt is not None and ad_start_dt is not None:
                                    summary = preProc.hoursDistributor(projkey, sr,  da_list[da_cnt], (hours * 0.25), survey_start_dt, ad_start_dt)
                                    #dbStorer.summaryTblUpdate(summary)
                                else:
                                    break
                            elif cnt == 2:
                                if ad_start_dt is not None and ad_end_dt is not None:
                                    summary = preProc.hoursDistributor(projkey , sr, da_list[da_cnt], (hours * 0.10), ad_start_dt, ad_end_dt )
                                    #dbStorer.summaryTblUpdate(summary)
                                else:
                                    break
                            elif cnt == 3:
                                if ees_start_dt is not None and ees_submission_dt is not None:
                                    summary = preProc.hoursDistributor(projkey, sr, da_list[da_cnt], (hours * 0.25), ees_start_dt, ees_submission_dt)
                                    #dbStorer.summaryTblUpdate(summary)
                                else:
                                    break
                            elif cnt == 4:
                                if ees_submission_dt is not None and ees_first_res_dt is not None:
                                    summary = preProc.hoursDistributor(projkey, sr, da_list[da_cnt], (hours * 0.10) , ees_submission_dt, ees_first_res_dt)
                                    #dbStorer.summaryTblUpdate(summary)
                                else:
                                    break
                            cnt+=1                
                else:
                    break
                print("This is the summary", summary)
                da_cnt+=1
                
            
                 
        
        

             
        
        dic_index = 0            
        while dic_index < len(dataset):
                       
                apiDtPreproc = (dpreProc.apiDataPreProcessor(dataset, dic_index)
                )             
                print("This is the api data after preprocessing:", apiDtPreproc)
                
                if apiDtPreproc is not None:
                    dataframe.append(tuple(apiDtPreproc))
                    dic_index += 1
                else:                                           
                    dic_index += 1                                    
        else:
            print('This is the dataframe after all the processing.', dataframe)           
            dbStorer.apiTblUpdate(dataframe)
            dic_index = 0
            
        
        while dic_index < len(dataset):                       
               
                summaryDtPreproc = dpreProc.summaryDataPreProcessor(dataset, dic_index)
                if summaryDtPreproc is not None:
                    print('This is the data_loader:', summaryDtPreproc)
                    summaryTblExtractor(summaryDtPreproc)
                    dic_index += 1  
                else:
                    dic_index += 1       
                
        

    return HttpResponseRedirect(reverse('hcbcapacity:index'))

import psycopg2

class dbStore:    

    def summaryTblUpdate(self, t):
            try:
                db = psycopg2.connect("dbname='proj_list2' user='postgres' password='WillisTowersWatsonEI2020' host='localhost' port='5432'")
                cursor = db.cursor()
                columns = ', '.join(t.keys())
                
                myTuple=("%s",)
                placeholders = ', '.join(myTuple * len(t))
               
                sql = 'INSERT INTO hcbcapacity_summarytable ({}) VALUES ({})'.format(columns, placeholders)
                values = [int(x) if isinstance(x, bool) else x for x in t.values()]
                cursor.execute(sql, values)
            except (Exception, psycopg2.Error) as E:
                print('Error : ', E)
            else:
                db.commit()
                db.close()
                print('Data Successfully Inserted!')

    def apiTblUpdate(self, api):
            try:
                db = psycopg2.connect("dbname='proj_list2' user='postgres' password='WillisTowersWatsonEI2020' host='localhost' port='5432'")
                cursor = db.cursor()
                #cursor.execute('DELETE FROM hcbcapacity_api_proj_list WHERE project_key LIKE "%E4-%";')
            
                sql_insert_query = """INSERT INTO hcbcapacity_api_proj_list ("project_key","project_type","contract_type","summary","sub_region","proj_status","complexity","delivery_analyst","configuration_analyst","production_analyst","created","hierarchy_setup_start_date","hierarchy_setup_end_date","survey_setup_start_date","survey_setup_submission_CSD","tech_prestest_start_date","tech_pretest_end_date","survey_lockdown_start_date","survey_lockdown_end_date","admin_start","admin_end","mdb_setup_start","mdb_submission_date","ees_start_date","ees_submission_end_date","ees_first_results_release_date","ees_second_results_release_date","da_hours","ca_hours","pa_hours") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" 

                cursor.executemany(sql_insert_query, api)

                cursor.execute('UPDATE hcbcapacity_api_proj_list SET project_year = EXTRACT(YEAR FROM created) WHERE project_key = project_key;')                       

            except (Exception, psycopg2.Error) as E:
                print('Error : ', E)
            else:
                db.commit()
                db.close()
                print('Data Successfully Inserted!')   
    

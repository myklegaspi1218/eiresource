from django.forms import ModelForm, TextInput, Select, DateInput, NumberInput, HiddenInput, CharField, DateField,forms
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import api_proj_list
import random
from datetime import date, datetime

class UpdateApiProjectList(ModelForm):        
      
      class Meta:
      
          PROJ_TYPE = [('Managed EES / Pulse License / Pulse License + Additional Services' , 'Managed EES / Pulse License / Pulse License + Additional Services'),('Traditional Survey (Confirmit, TRO, CAT,TRP)','Traditional Survey (Confirmit, TRO, CAT, TRP)'),('None','None')]
      
          CONT_TYPE = [('2b. License + support (incl. support for a managed project)','2b. License + support (incl. support for a managed project)'),('3. Managed projects on EES','3. Managed projects on EES'),('None','None')]

          SUB_REG = [('Asia Pacific', 'Asia Pacific'),('CEMEA', 'CEMEA'),('North America', 'North America'), ('Western Europe', 'Western Europe'), ('Great Britain', 'Great Britain')]

          DEL_ANA = [('None','None'),('Yang Xu','Yang Xu'), ('Waldy Capule','Waldy Capule'), ('Ronald Macalipay','Ronald Macalipay'), ('Maricar Garzon','Maricar Garzon'), ('Louie John Diaz','Louie John Diaz'), ('Leslie Aubrey Igaharas','Leslie Aubrey Igaharas'), ('Khumille Lopez','Khumille Lopez'), ('Justine Carmel Tayag','Justine Carmel Tayag'), ('Joy Angelie Baltazar','Joy Angelie Baltazar'), ('Joey Alvarado','Joey Alvarado'),('Joel Juatchon','Joel Juatchon'), ('Finella Francesca Panganiban','Finella Francesca Panganiban'), ('Eileen Faye Placido','Eileen Faye Placido') ,('Diana Asis','Diana Asis'),  ('Wilbur Dionglay','Wilbur Dionglay'), ('Jui Hsia Liu','Jui Hsia Liu'), ('Shara Dyan Escobido','Shara Dyan Escobido'), ('Jasmine Jake Halili','Jasmine Jake Halili'), ('Sharisse Perez','Sharisse Perez'), ('James Domogma','James Domogma'), ('John Mer Giray','John Mer Giray')]

          model = api_proj_list

          fields = ['project_key','project_type','sub_region', 'contract_type','summary','created','proj_status','survey_setup_start_date','admin_start','admin_end','ees_start_date','ees_submission_end_date','ees_first_results_release_date','delivery_analyst','da_hours']
          
          widgets = {
              
              'project_key' : HiddenInput(),
              'project_type' : Select(attrs={'class':'form-control'}, choices=PROJ_TYPE),
              'contract_type': Select(attrs={'class' : 'form-control'}, choices=CONT_TYPE),
              'sub_region': Select(attrs={'class' : 'form-control'}, choices=SUB_REG),
              'proj_status': HiddenInput(attrs={'value' : 'Preparation'}),
              'summary': TextInput(attrs={'class' : 'form-control', 'required': True}),
              'created': DateInput(format='%Y-%m-%d',attrs={'class' : 'form-control', 'value':datetime.now()}),
              'survey_setup_start_date': DateInput(format='%Y-%m-%d',attrs={'class' : 'form-control','required' : True}),                   
              'admin_start' : DateInput(format='%Y-%m-%d',attrs={'class' : 'form-control','required' : True}),               
              'admin_end' : DateInput(format='%Y-%m-%d',attrs={'class' : 'form-control','required' : True}),
              'ees_start_date': DateInput(format='%Y-%m-%d',attrs={'class' : 'form-control','required' : True}),
              'ees_submission_end_date': DateInput(format='%Y-%m-%d',attrs={'class' : 'form-control', ' required' : True}),
              'ees_first_results_release_date' : DateInput(format='%Y-%m-%d',attrs={'class' : 'form-control', 'required' : True}),                 
              'delivery_analyst' : Select(attrs={'class' : 'form-control', 'required' : True}, choices=DEL_ANA),              
              'da_hours' : NumberInput(attrs={'class':'form-control', 'required' : True})           
              

          }
        
          error_messages = {
             'summary' : {'required': 'Please enter the name of the project.'}
          }
            
          
          
          

       


      

          
              

          

from os import truncate
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import manager
from django.utils.translation import gettext_lazy as _

# Create your models here.

class api_proj_list(models.Model):
      
      project_key = models.CharField(primary_key=True, max_length=80)
      project_type = models.CharField(blank=True,null=True,max_length=255)
      contract_type = models.CharField(blank=True,null=True,max_length=100)
      summary = models.TextField(blank=True,null=True)      
      sub_region = models.TextField(blank=True,null=True)
      proj_status = models.TextField(blank=True,null=True)
      complexity = models.TextField(blank=True,null=True)
      delivery_analyst = models.TextField(blank=True,null=True)
      configuration_analyst = models.TextField(blank=True,null=True)
      production_analyst = models.TextField(blank=True,null=True)
      created = models.DateTimeField(blank=True,null=True)
      hierarchy_setup_start_date = models.DateTimeField(blank=True,null=True)
      hierarchy_setup_end_date = models.DateTimeField(blank=True,null=True)
      survey_setup_start_date = models.DateTimeField(blank=True,null=True)
      survey_setup_submission_CSD = models.DateTimeField(blank=True,null=True)
      tech_prestest_start_date = models.DateTimeField(blank=True,null=True)
      tech_pretest_end_date = models.DateTimeField(blank=True,null=True)
      survey_lockdown_start_date = models.DateTimeField(blank=True,null=True)
      survey_lockdown_end_date = models.DateTimeField(blank=True,null=True)
      admin_start = models.DateTimeField(blank=True,null=True)
      admin_end = models.DateTimeField(blank=True,null=True)
      mdb_setup_start = models.DateTimeField(blank=True,null=True)
      mdb_submission_date = models.DateTimeField(blank=True,null=True)
      ees_start_date = models.DateTimeField(blank=True,null=True)
      ees_submission_end_date = models.DateTimeField(blank=True,null=True)
      ees_first_results_release_date = models.DateTimeField(blank=True,null=True)
      ees_second_results_release_date = models.DateTimeField(blank=True,null=True)
      da_hours = models.FloatField(blank=True, null=True)
      ca_hours = models.FloatField(blank=True, null=True)
      pa_hours = models.FloatField(blank=True, null=True)
      project_year = models.IntegerField(blank=True, null=True)
      month = models.CharField(blank=True, null=True,max_length=30)
      standard_hours = models.FloatField(blank=True, null=True)
      
      # def save(self, *args, **kwargs):
      #       if self.admin_start:
      #             self.month = self.admin_start.strftime("%B")
      #       super(api_proj_list, self).save(*args,**kwargs)

      def __str__(self):
            return self.summary
     
      


class summaryTable(models.Model):
      project_key_forecast = models.ForeignKey(api_proj_list, on_delete=models.CASCADE, null= True)
      delivery_analyst = models.TextField(null=True,blank=True)
      project_year= models.IntegerField(null=True,blank=True)      
      sub_region = models.TextField(blank=True,null=True)
      jan = models.FloatField(null=True,blank=True)
      feb = models.FloatField(null=True,blank=True)
      mar = models.FloatField(null=True,blank=True)
      apr = models.FloatField(null=True, blank=True)
      may = models.FloatField(null=True,blank=True)
      jun = models.FloatField(null=True,blank=True)
      jul = models.FloatField(null=True, blank=True)
      aug = models.FloatField(null=True,blank=True)
      sep = models.FloatField(null=True,blank=True)
      oct = models.FloatField(null=True,blank=True)
      nov = models.FloatField(null=True,blank=True)
      dec = models.FloatField(null=True,blank=True)
      

class std_hours(models.Model):
      month_nm = models.TextField(null=False,blank=False)
      yr = models.IntegerField(null=False,blank=False)
      no_of_hours = models.FloatField(null=False,blank=False)


class da_list(models.Model):
      da_name = models.TextField(null=False, blank=False)
      region = models.TextField(null=False, blank=False)

class daProdByMonth(models.Model):
      prod_id = models.IntegerField(primary_key=True)
      delivery_analyst = models.CharField(max_length=100)
      sub_region = models.TextField()
      project_year = models.IntegerField()
      jan = models.FloatField()
      feb = models.FloatField()
      mar = models.FloatField()
      apr = models.FloatField()
      may = models.FloatField()
      jun = models.FloatField()
      jul = models.FloatField()
      aug = models.FloatField()
      sep = models.FloatField()
      oct = models.FloatField()
      nov = models.FloatField()
      dece = models.FloatField()
      class Meta:
            db_table = u'da_prod_by_month'
            managed = False

class daAverageProd(models.Model):
      prod_id = models.IntegerField(primary_key=True)
      delivery_analyst = models.CharField(max_length=100)
      project_year = models.IntegerField()
      average_prod = models.FloatField()
      class Meta:
            db_table=u'da_average_prod'
            managed = False
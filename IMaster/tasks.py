from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import *
from celery import shared_task
import os
import xlrd
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
import logging
from django.contrib.auth.models import User
from django.contrib import messages
from openpyxl import load_workbook
from django.core.files.base import ContentFile


@shared_task
def process_excel_file(id):
    try:
        file_obj = File.objects.get(id=id)
        df = pd.read_excel(file_obj.file)

        for index, row in df.iterrows():
            created_by, _ = User.objects.get_or_create(username=row['created_by'])

            Course.objects.create(
                course_name=row['Course_name'],
                description=row['Description'],
                credit=row['Credit'],
                created_by=created_by
            )

        return "Success"
    except Exception as e:
        return f"An error occurred: {e}"
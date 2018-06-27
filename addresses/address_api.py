from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.db import connection
from itertools import *
from psycopg2.extras import NamedTupleCursor

def get_address_details(request):
    if request.method == 'GET':
        address_query = request.GET.get('address','')
        cursor = connection.cursor()
        cursor.execute("select transaction_hash_id, output_no, output_type, output_value, size, address from bitcoin_data_app_output_table where address= %s",[address_query])
        col_names = [desc[0] for desc in cursor.description]
        address_db= cursor.fetchone()
        row_dict = dict(zip(col_names, address_db))
        return JsonResponse({"result":row_dict})


def test(request):
    if request.method == 'GET':
        address_query = request.GET.get('address','')
        cursor = connection.cursor()
        cursor.execute("select output_no, output_type, output_value, size, address from bitcoin_data_app_output_table where address= %s",[address_query])
        col_names = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        row_dict = dict(zip(col_names, row))
        return JsonResponse({"result":row_dict})



def get_full_address_details(request):
    if request.method == 'GET':
        full_address_query = request.GET.get('address','')

        address_details = []
        cursor = connection.cursor()
        cursor.execute("select  output_no, output_type, output_value, size, address from bitcoin_data_app_output_table where address= %s",[full_address_query])
        col_names = [desc[0] for desc in cursor.description]
        # for address_db in cursor.fetchall():
        #     address_details.append(dict(zip(col_names, address_db)))
        #print(address_details)
        full_address_db = cursor.fetchone()
        address_details = dict(zip(col_names, full_address_db))
        all_transaction_details = []
        cursor.execute("select transaction_hash_id from bitcoin_data_app_output_table where address=%s",[full_address_query])
        transaction_db = cursor.fetchall()
        print(transaction_db)
        for transaction in transaction_db:
            transaction_details = []
            cursor.execute('select * from bitcoin_data_app_transaction_table where transaction_hash = %s', [transaction])
            col_names = [desc[0] for desc in cursor.description]
            for transaction_info in cursor.fetchall():
                #print(transaction_info)
                transaction_details.append(dict(zip(col_names, transaction_info)))
            all_transaction_details.append(transaction_details)
            print(all_transaction_details)





        return JsonResponse({'final':address_details,
                              'txids':full_transaction_details,
                             })
        # cursor = connection.cursor()
        # cursor.execute('select * from bitcoin_data_app_output_table where address=%s',[full_address_query])

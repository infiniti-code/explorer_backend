from django.http import JsonResponse
from django.db import connection

def get_block_details(request):
    if request.method == 'GET':
        block_query = request.GET.get('block_hash','')

        # Connection to database established
        cursor = connection.cursor()
        cursor.execute('select * from bitcoin_data_app_block_table where block_hash = %s', [block_query])
        col_names = [desc[0] for desc in cursor.description]
        block_db = cursor.fetchone()


        if not block_db:
            return JsonResponse({"search":"wrong query is searched"})
        else:
            block_details = dict(zip(col_names,block_db))
            transaction_list = []
            cursor.execute("select transaction_hash from bitcoin_data_app_transaction_table where block_height_id=%s",[block_details['block_height']])
            transaction_db = cursor.fetchall()
            for transacton in transaction_db:
                transaction_list.append(transacton)

            return JsonResponse({'block':block_details,
                                'txids':transaction_list,
                                
                                 })

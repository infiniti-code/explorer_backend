from django.http import JsonResponse
from django.db import connection

# Create your views here.



def get_transaction_details(request):
    if request.method == 'GET':

        transaction_query = request.GET.get('transaction','')


        # Connection to database established
        # Multiple cursor connections should not be created due to anomaly caused in data
        # commits at different times may make them to clash
        cursor = connection.cursor()
        cursor.execute("select * from bitcoin_data_app_transaction_table where transaction_hash = %s", [transaction_query])
        col_names = [desc[0] for desc in cursor.description]
        transaction_db = cursor.fetchone()

        if not transaction_db:
            return JsonResponse({"search":"Wrong query is searched"})
        else:
            transaction_details = dict(zip(col_names,transaction_db))


            cursor.execute("select address from bitcoin_data_app_output_table where transaction_hash_id = %s", [transaction_query])
            output_db = cursor.fetchall()
            cursor.execute("select input_address from bitcoin_data_app_input_table where transaction_hash_id =%s", [transaction_query])
            input_db = cursor.fetchall()


            output_details = []
            cursor.execute("select output_type, output_value, size, address, output_script_value  from bitcoin_data_app_output_table where transaction_hash_id =%s", [transaction_query])
            col_names = [desc[0] for desc in cursor.description]
            for output_info in cursor.fetchall():
                output_details.append(dict(zip(col_names,output_info)))


            input_details = []
            cursor.execute("select input_sequence_number, input_size, input_address, input_value, input_script_type, input_script_value from bitcoin_data_app_input_table where transaction_hash_id =%s", [transaction_query])
            col_names = [desc[0] for desc in cursor.description]
            for input_info in cursor.fetchall():
                input_details.append(dict(zip(col_names,input_info)))


            address_list = []
            for output in output_db:
                address_list.append(output)
            for _input in input_db:
                address_list.append(_input)


            result = [{"addresses":list(set(address_list)),
                    "transaction":transaction_details,
                     'input_details':input_details,
                     'output_details':output_details,
                                 }]
            return JsonResponse({'result':result})

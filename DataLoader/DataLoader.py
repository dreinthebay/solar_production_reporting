import psycopg2
import psycopg2.extras
import os
from config import config

class DataLoader(object):
	"""docstring for DataLoader"""
	def __init__(self, column_names, table_name, company_name='NCS',file_path=None, folder_path=None, dictionary_of_files=None):

		self.company_name = company_name

		self.table_name = table_name

		self.columns = column_names
	
	def get_connection(self):
	    
	    params = self.connect_to_postgres()

	    conn = psycopg2.connect(**params)

	    return conn

	def connect_to_postgres(self, cloud_connect=True):
	    
	    print('testing cloud connect = ', cloud_connect)
	    
	    if cloud_connect:

	        print('Connection type: Cloud')

	        return config(section='postgresql')

	    else:

	        print('Connection type: Localhost')

	        return config(section='localhost')

	def make_sql_string(self, table_name, list_of_column_names):
	    
	    column_values = ','.join(list_of_column_names)
	    
	    values = ','.join(['%('+str(x)+')s' for x in list_of_column_names])
	    
	    s = """INSERT INTO {table_name} ({column_values}) VALUES ({values})""".format(
	    table_name=table_name,
	    column_values=column_values,
	    values=values
	    )
	    
	    print(s)
	    
	    return s

	def sql_query(self, conn, sql_string, list_of_dict):
	    
	    with conn.cursor() as cursor:
	    
	        iter_data = (d for d in list_of_dict)
	    
	        print(type(iter_data))
	    
	        psycopg2.extras.execute_batch(
	    
	            cursor,
	    
	            sql_string,
	    
	            iter_data
	        )
	    
	    conn.commit()

	    return True

	def load_single_file(self, file_path):

		with self.get_connection() as conn:

			#conn = get_connection()
			self.load_file_to_db(file_path, conn)

			#self.close_connection(conn)

		return True

	def load_folder_to_db(self, folder=None):
	
		if folder:

			with self.get_connection() as conn:

				#folder = file_path = os.path.join(self.app_folder, 'raw_data', self.company_name, self.equipment_company_name, sub_directory, file_name)

				for file in os.listdir(folder):

					file_path = folder + os.sep + file

					print(file_path)

					self.load_file_to_db(file_path, conn)

				#self.close_connection(conn)

		else:
			print('incorrect parameters passed')

		return 1

	def load_filelist_to_db(self, file_list=None):
		# if file list passed
		if file_list:
		
			with self.get_connection() as conn:
		
				for file in file_list:
			
					self.load_file_to_db(file, conn)
				
				#self.close_connection(conn)
		
		else:
		
			print('incorrect parameters passed')

		return 1

	def close_connection(self,conn):
		conn.close()
		return 1


from dotenv import load_dotenv
load_dotenv()
import requests
import os
import json

"""
Estou utilizando um arquivo .ENV para armazenar as credenciais de acesso à API da Agenda Edu.
"""

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SCHOOL_TOKEN = os.getenv('SCHOOL_TOKEN')
API_PRODUCAO = os.getenv('API_PRODUCAO')
API_SANDBOX = os.getenv('API_SANDBOX ')

def get_token():
	response = requests.post(
		url=f'{API_PRODUCAO}/oauth/v2/token',
		headers={
			'Accept': 'application/json',
			'Content-Type':'application/x-www-form-urlencoded'
		},
		data={
			'grant_type':'client_credentials',
			'client_id':CLIENT_ID,
			'client_secret':CLIENT_SECRET
		}
	)
	
	if response.status_code == 200:
		return response.json()
	return False

def get_student_list(token):
	headers = {
		'Accept': 'application/json',
		'Authorization':f'Bearer {token["access_token"]}',
	}

	params = {
		'page':1
	}

	student_list = []

	while True:

		response = requests.get(
			url=f'{API_PRODUCAO}/v2/student_profiles/',
			headers=headers,
			params=params
		)

		current_student_list = response.json()['data']

		current_student_list = [{'id':student['id'], 'name':student['attributes']['name'], 'legacy_id':student['attributes']['legacy_id'], 'period':student['attributes']['period'], 'classroom_ids':[classroom['id'] for classroom in student['relationships']['classrooms']['data']]} for student in current_student_list]
		
		student_list.extend(current_student_list)

		params['page']+=1

		if not response.json()['meta']['next']:
			break		


	return student_list

def student_add_classroom(token, student, classroom_id):
	current_student = student.copy()
	current_student.pop('legacy_id')
	current_student.pop('id')
	current_student['confirm'] = True
	current_student['classroom_ids'].append(classroom_id)

	headers = {
		'Content-Type': 'application/json',
		'Authorization':f'Bearer {token["access_token"]}',
	}

	data = {
	"student_profile": current_student
	}

	data = json.dumps(data)

	if current_student:
		response = requests.put(
			url=f'{API_PRODUCAO}/v2/student_profiles/{student["id"]}/',
			headers=headers,
			data=data
		)

		if response.status_code == 200:
			return response.json()

def set_classrom_students(token, student_list, student_list_name, classroom_id):
	for student_list_name_i in student_list_name:
		for student_list_i in student_list:
			if student_list_i['name'].lower().strip() == student_list_name_i.lower().strip():
				student_add_classroom(token, student_list_i, classroom_id)
				break
		else:
			print(f"Não foi encontrado correlação: {student_list_name_i} - {classroom_id}")


def main():
	token = get_token()

	input = open('input.json')
	input_data = json.load(input)

	if token:
		student_list = get_student_list(token)

		for i, i_data in enumerate(input_data['input']):
			set_classrom_students(token, student_list, i_data['alunos'], i_data['classroom_id'])
main()

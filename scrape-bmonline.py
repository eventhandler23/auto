#!/usr/bin/python

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://www.bmonline.ph"
USERNAME = "bmonlinetest009@outlook.ph"
PASS = "1234"

def login(**kwargs):
	login_url = BASE_URL + "/signin"
	session_request = kwargs.get('session')

	payload = {
		'email' 	: kwargs.get('email'),
		'password' 	: kwargs.get('password'),
		'_token' 	: kwargs.get('token')
	}

	session_request.post(
		login_url,
		data=payload
	)

	r = session_request.get(BASE_URL)

	s = BeautifulSoup(r.text, 'html.parser')
	info = s.find(id='personal-info')
	print info


if __name__ == '__main__':
	session_request = requests.session()
	r = session_request.get(BASE_URL)
	s = BeautifulSoup(r.text, 'html.parser')

	csrf_token = s.find('input', {'name' : '_token'})['value']

	login(
		session=session_request,
		email=USERNAME,
		password=PASS,
		token=csrf_token
	)

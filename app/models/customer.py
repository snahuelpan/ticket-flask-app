from app import db
from flask import current_app
import requests
from sqlalchemy import Column, Integer, text

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(300), index= True, unique=True)
    name = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    id_number = db.Column(db.String(20), index=True, unique=True)
    cost_center = db.Column(db.Integer)
    job_title = db.Column(db.String(300))
    email = db.Column(db.String(120))
    active = db.Column(db.Integer , server_default=text("1"))

    def __repr__(self):
        return f'<Customer {self.name} {self.lastname}>'
    
     # Flask-Login requiere estos métodos:
    def get_id(self):
        return str(self.uuid)
    
    def get_access_token(self):
        url = f"https://login.microsoftonline.com/{current_app.config["AZURE_TENANT_ID"]}/oauth2/v2.0/token"
        params = {
            'client_id': current_app.config["AZURE_CLIENT_ID"],
            'client_secret': current_app.config["AZURE_CLIENT_SECRET"],
            'scope': "https://graph.microsoft.com/.default",
            'grant_type': 'client_credentials',
        }
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        response = requests.post(url, data=params, headers=headers)
        
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            raise Exception(f"Error al obtener el token: {response.status_code} - {response.text}")
        
    def get_user_details(self, user_id: str, access_token: str):
        url = f"https://graph.microsoft.com/v1.0/users/{user_id}?$select=companyName,department,jobTitle"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al obtener detalles del usuario: {response.status_code} - {response.text}")


    def get_user_licenses(self, user_id: str, access_token: str):
        url = f"https://graph.microsoft.com/v1.0/users/{user_id}/licenseDetails"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            licenses = response.json().get('value', [])
            return [license.get('skuPartNumber') for license in licenses if license.get('skuPartNumber')]
        else:
            raise Exception(f"Error al obtener las licencias del usuario: {response.status_code} - {response.text}")
        

    def get_all_users(self):
        access_token = self.get_access_token()
        users = []
        next_link = f"https://graph.microsoft.com/v1.0/users?$top=999"  # Obtener hasta 999 usuarios por petición

        while next_link:
            response = requests.get(next_link, headers={'Authorization': f'Bearer {access_token}'})
            
            if response.status_code == 200:
                data = response.json()
                user_emails = [user['id'] for user in data.get('value', [])]
                
                # Aquí puedes realizar la lógica para obtener los usuarios desde tu base de datos
                # Supón que `existing_users` es una lista de usuarios existentes en tu base de datos
                existing_users = []  # Lógica para obtener los usuarios de la base de datos
                
                new_users = [
                    user for user in data.get('value', []) 
                    if user['id'] not in [existing_user['id'] for existing_user in existing_users]
                ]
                
                for user in new_users:
                    licenses = self.get_user_licenses(user['id'], access_token)
                    if licenses:
                        user_details = self.get_user_details(user['id'], access_token)
                        user['licenses'] = licenses
                        user['companyName'] = user_details.get('companyName')
                        user['department'] = user_details.get('department')
                        user['jobTitle'] = user_details.get('jobTitle')
                        users.append(user)
                
                next_link = data.get('@odata.nextLink')
            else:
                raise Exception(f"Error al obtener usuarios: {response.status_code} - {response.text}")

        # Aquí puedes insertar los usuarios nuevos con licencias en tu base de datos
        # Ejemplo: insert_users_to_db(users)
        
        return users

    @property
    def is_active(self):
        return self.active
    
    
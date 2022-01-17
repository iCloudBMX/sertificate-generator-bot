from .models import RegisteredUser
import pandas as pd
import string

def locate_users():
    # delete all users
    # RegisteredUser.objects.all().delete()
    
    # Load the xlsx file
    excel_data = pd.read_excel('<excel file path>')

    # Read the values of the file in the dataframe
    data = pd.DataFrame(excel_data, columns=['<colum name>'])

    users = data.values.tolist()

    for user in users:
        RegisteredUser.objects.create(name=f'{user[0]} {user[1]}', email=user[2].translate({ord(c): None for c in string.whitespace}), address=user[3], phone=user[4])


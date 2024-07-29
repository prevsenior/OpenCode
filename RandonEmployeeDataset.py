# Dataset aleatorio para nome de funcionario
# name,birthdate,sex,phonenumber,email,id,hiredate,status
# O status pode ser A or I e os outros dados aleatorios. Preciso de 120 arquivos. Preciso que faça download automaticamente

import random
import string
import os
import zipfile

def generate_employee_file(filename):
    with open(filename, 'w') as f:
        f.write('name,birthdate,sex,phonenumber,email,id,hiredate,status\n')
        for _ in range(10):
            name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
            birthdate = f"{random.randint(1950, 2000)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            sex = random.choice(['M', 'F'])
            phonenumber = str(random.randint(100000000, 999999999))
            email = f"{name}@{''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))}.com"
            emp_id = str(random.randint(100000, 999999))
            hiredate = f"{random.randint(2000, 2022)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            status = random.choice(['A', 'I'])
            f.write(','.join([name, birthdate, sex, phonenumber, email, emp_id, hiredate, status]) + '\n')

# Gerar os arquivos CSV
for i in range(5):
    filename = f'employee_data_{i}.csv'
    generate_employee_file(filename)

# Compactar os arquivos CSV em um arquivo ZIP
with zipfile.ZipFile('employee_data.zip', 'w') as zipf:
    for i in range(120):
        filename = f'employee_data_{i}.csv'
        zipf.write(filename)
        os.remove(filename)

print("Arquivo 'employee_data.zip' criado com sucesso.")


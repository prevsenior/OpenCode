# Dataset aleatorio para nome de funcionario
# name,birthdate,sex,phonenumber,email,id,hiredate,status
# O status pode ser A or I e os outros dados aleatorios. Preciso de 120 arquivos. Preciso que faça download automaticamente

import random
import string
import os

def generate_employee_file(filename):
  with open(filename, 'w') as f:
    f.write('name,birthdate,sex,phonenumber,email,id,hiredate,status\n')
    for _ in range(10):
      name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
      birthdate = str(random.randint(1950, 2000)) + '-' + str(random.randint(1, 12)) + '-' + str(random.randint(1, 28))
      sex = random.choice(['M', 'F'])
      phonenumber = str(random.randint(100000000, 999999999))
      email = name + '@' + ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10))) + '.com'
      id = str(random.randint(100000, 999999))
      hiredate = str(random.randint(2000, 2022)) + '-' + str(random.randint(1, 12)) + '-' + str(random.randint(1, 28))
      status = random.choice(['A', 'I'])
      f.write(','.join([name, birthdate, sex, phonenumber, email, id, hiredate, status]) + '\n')

for i in range(120):
  filename = 'employee_data_{}.csv'.format(i)
  generate_employee_file(filename)

!zip -r employee_data.zip *.csv
!rm *.csv
!echo "Download the employee_data.zip file by clicking on the link below."
!echo "<a href='employee_data.zip' download>Download</a>"

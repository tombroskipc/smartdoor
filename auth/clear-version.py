filename = 'requirements.txt'

with open(filename, 'r') as file:
    requirements = [line.split('==')[0] + '\n' for line in file.readlines()]
    
with open(filename, 'w') as file:
    file.writelines(requirements)
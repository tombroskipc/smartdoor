filenames = [
    'bulkdata/apc221211/apc221211.xml',
    'bulkdata/apc221212/apc221212.xml'
]

filenames = [filename.replace('.xml', '').split('/')[-1] for filename in filenames]

print(filenames)
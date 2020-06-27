import csv
import json

f = open('spiders/data.json')
jsonData = json.load(f)
f.close

with open('out.csv', 'w',encoding='utf-8') as f:
    JsonToCSV = csv.writer(f)
    JsonToCSV.writerow(["Name", "Job", 'Link',"Birthplace", "AGE", "BIRTH SIGN", "BIRTHDAY", "About", "Before Fame", "Trivia", "Family Life", "Associated With"])

    title = ["name", "job","link", "Birthplace", "Age ", "Birth Sign", " Birthday ", "About", "Before Fame", "Trivia", "Family Life", "Associated With"]

    for item in jsonData:
        keys1 = list(item['quick_info'].keys())
        keys2 = list(item['detail_info'].keys())

        values = []

        for i in title:
            if i!= 'link':
                if i not in  keys1 and i not in keys2:
                    values.append(" ")
                
                else:
                    if i in keys1:
                        values.append(item['quick_info'][i])
                    else:
                        values.append(item['detail_info'][i])
            
            else:
                if i not in  keys1 and i not in keys2:
                    values.append("no-name")
                else:
                    temp_link = item['quick_info'][i]
                    temp_link = temp_link.replace(".","-")
                    values.append(temp_link)

        JsonToCSV.writerow(values)
        
          
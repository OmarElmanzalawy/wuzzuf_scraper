import requests
import bs4
import csv
import sys

target = input('What is your target search?: ')

#Title of the job
job_titles = []

#Locaction of work
locations = []

#Fulltime, Part-time etc....
type = []

requirements = []

#Pages to scrape data from
pages = {}


#Scrapes the given page 
def scrape(page):
    soup = bs4.BeautifulSoup(page,'lxml')
    #Title & requirements
    for job in soup.find_all('h2',class_='css-m604qf'):
        is_requirements_available = True
        req_paragraph = []
        link = job.find('a').attrs['href']
        detailed = requests.get(link).text
        external_source = bs4.BeautifulSoup(detailed,'lxml')
        full_list = external_source.find('div',class_='css-1t5f0fr').find('ul')
        try:
            for line in full_list.find_all('li'):
                req_paragraph.append(line.text)
        except AttributeError:
            is_requirements_available = False
            print('Empty Requirements')
        if(is_requirements_available):
            joined = [' -- '.join(x) for x in zip(req_paragraph[0:2],req_paragraph[1::2])]
            formatted_req = '\n'.join(joined)
            requirements.append(formatted_req)
            print(formatted_req)
            print('------------\n')
        else:
            requirements.append('No Requirements')    
        job_titles.append(job.text)

    #print('-----------------\n')
    #print('Location:\n')
    #Location
    for location in soup.find_all('span',class_='css-5wys0k'):
        locations.append(location.text)
        #print(location.text)
    #print('-----------------\n')
    #print('Description:\n')

    #Type    
    for feature in soup.find_all('div',class_='css-1lh32fc'):
        type.append(feature.a.text)
        #print(feature.a.text)

    make_csv(job_titles,locations,type,requirements)


#Prints result into a csv file
def make_csv(title,loc,types,requirement):
    csv_file = open(f'{target}_scraper.csv','w',newline='',encoding="utf-8")
    writer = csv.writer(csv_file)
    writer.writerow(['Title','Location','Type','Requirements'])
    result = []    
    for x in range(0,len(job_titles)):
        instnace = []
        instnace.append(title[x])
        instnace.append(loc[x])
        try:
            instnace.append(types[x])
        except IndexError:
            types[x] = ''
        try:
            instnace.append(requirement[x])
        except IndexError:
            requirement[x] = ''
        except UnicodeEncodeError:
            instnace.append('ARABIC TEXT IS NOT SUPPORTED')      
        result.append(instnace)
        writer.writerow(instnace)

    csv_file.close()
    return result


#gets links of first three pages
def assign_pages():
    pages['main'] = source
    for pageno in range(1,3):
        pages[f'page{pageno}'] = requests.get(f'https://wuzzuf.net/search/jobs/?a=navbg&q={target}%20&start={pageno}').text
            
#Gets Source page
if (' ' not in target):
    source = requests.get(f'https://wuzzuf.net/search/jobs/?q={target}&a=navbg').text
    try:
        source.raise_for_status()
    except:
        print('Error Donloading the page')
else:
    target = target.replace(' ','+')
    source = requests.get(f'https://wuzzuf.net/search/jobs/?q={target}&a=navbg').text
    try:
        source.raise_for_status()
    except:
        print('Error Donloading the page')
assign_pages()

#Main Program
for page in pages.values():
    
    scrape(page)
    print('Exiting page')

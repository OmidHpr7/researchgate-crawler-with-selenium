# -*- coding: utf-8 -*-

""" **************************************************************************
                           Created on 2021

                        @author: Omid Hajipoor
                    Email: hajipoor.omid@aut.ac.ir
                  Gmail: omid.hajipoor0770@Gmail.com
************************************************************************** """


from selenium import webdriver
from bs4  import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())



# =============================================================================
# Get information
# =============================================================================
def get_inf_page(url):
    information_of_page = {}
    information_of_page['id'] = ''
    information_of_page['title'] = ''
    information_of_page['abstract'] = ''
    information_of_page['date'] = ''
    information_of_page['authers'] = []
    information_of_page['refrences'] = []
    
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content)
    temp = url.split('/')
    
    ## id
    id_name = temp[len(temp)-1]
    id = id_name.split('_')[0]
    print('id of paper is: ', id)
    information_of_page['id'] = id
    
    ## title
    name_part = id_name.split('_')[1:len(id_name.split('_'))]
    name = ' '.join(name_part)
    print('name of paper is: ', name)
    information_of_page['title'] = name
    
    ## abstract
    try:
        abstract_tag = soup.find('div' , attrs={'class':'nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-800 research-detail-middle-section__abstract'})
        abstract = abstract_tag.getText()

        information_of_page['abstract'] = abstract
    except:
        information_of_page['abstract'] = ''
        pass

    
    
    ## year
    try:
        ac_year = soup.find('div', attrs = {'class':'nova-legacy-e-text'}) 
        year = ac_year.getText()
        information_of_page['date'] = year.split(' ')[1]
    except:
        information_of_page['date'] = ''
        pass
    
    main = soup.findAll('div', attrs={'class':'nova-legacy-l-flex__item research-detail-author-list__item research-detail-author-list__item--has-image'})
    all_auther = []
    for line in main:
        temp = line.find('a', attrs={'class':'nova-legacy-e-link nova-legacy-e-link--color-inherit nova-legacy-e-link--theme-bare'})
        all_auther.append(temp.getText())
    
    print('Authers are: ' , all_auther)
    information_of_page['authers'] = all_auther
    
    ## refrences
    main = soup.find('div', attrs={'class': 'js-target-reference'})
    my_div_ref = main.findAll('div' , attrs={'class': 'nova-legacy-e-text nova-legacy-e-text--size-l nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-inherit nova-legacy-e-text--clamp-2 nova-legacy-v-publication-item__title'})
    allref = []
    count_url = 0
    for line in my_div_ref:
        try:
            allref.append('https://www.researchgate.net/' + line.a['href'])
            count_url += 1
            if count_url==10:
                break
        except:
            continue


    information_of_page['refrences'] = allref
    
    return information_of_page
    
    
    
import json
import time
# =============================================================================
# Crawling
# =============================================================================
def crawling(start_file_name, json_file_name, _numOf_paper):
    time.sleep(5)
    
    try:
        with open(json_file_name + '.json', mode='r', encoding='utf-8') as feedsjson:
            dict1 = json.load(feedsjson)
            
        counter = len(dict1)
    except:
        dict1 = {}
        counter = 0
        
    urls_txt = open(start_file_name + '.txt', 'r', encoding='utf8').readlines()
    urls = [url.replace('\n', '') for url in urls_txt]

    proc_url = []
    flag=False
    while flag==False:
        url = urls[counter]
        counter +=1
        sno ='paper'+str(counter)
              
        print(sno)
        inf_page = get_inf_page(url)
            
        
        dict1[sno]= inf_page
        
        for item in inf_page['refrences']:
            if (item in urls) :
                continue
            elif len(urls) == _numOf_paper:
                flag = True
                break
            else:
                urls.append(item)
                with open(start_file_name + '.txt', 'a+') as tf:
                    tf.write(item + '\n')

        
        proc_url.append(url)
        if counter == _numOf_paper:
            flag = True
            break
        elif counter%5 == 0:
            with open(json_file_name + '.json', mode='w', encoding='utf-8') as feedsjson:
                json.dump(dict1, feedsjson, indent = 4)
        else:
            print('\n')
            
            

    with open(json_file_name + '.json', mode='w', encoding='utf-8') as feedsjson:
        json.dump(dict1, feedsjson, indent = 4)
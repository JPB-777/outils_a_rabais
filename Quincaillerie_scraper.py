from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

#TODO Faire suivre le nom du magasin
#TODO trouver moyen de scroller la page pour la rendre active et permettre le scan de tous les produits pas seulement ceux de la premiere page
# Obtenir le lien des items de chaque circulaire Via Reebee

def getFlyersLinks():
    #Obtenir le lien des circulaire selon leur categories (ex: outils ou chaussures)
    #Peut-etre creer fonction permettant d<obtenir le titre et le lien de chaque categorie et passer ce parametre comme argument de cette fonction
    url = 'https://www.reebee.com/flyers?categoryID=5'

    driver = webdriver.Chrome()

    #Agrandir la fenetre
    driver.maximize_window()

    #Ouvrir le lieu url
    driver.get(url)

    #Attendre quelques secondes
    driver.implicitly_wait(3)

    #Wait
    wait = WebDriverWait(driver, 10)

    #Verifier la presence d'un popup/modal
    modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'inner-modal')))

    if modal:
        close_btn = driver.find_element_by_class_name('close-modal')
        close_btn.click()

    flyers = driver.find_elements_by_class_name('flyer-link')

    urls = []

    for flyer in flyers:
        
        full_url = flyer.get_attribute('href')
        store_name = flyer.get_attribute('title')
        urls.append((full_url, store_name))

    with open('flyerslinks_1.txt', 'w') as f:
        for url, storename in urls:
            f.write(storename)
            f.write('\n')
            f.write(url)
            f.write('\n')

    driver.quit()

    return True

#def getFlyersItemsLinks():

    # Obtenir les liens des circulaires a scraper
    #urls = getFlyersLinks()

    #Tester la fonction en silo
    with open('flyerslinks.txt', 'r') as f:
        lines = f.readlines()
        urls = [line.strip('\n') for line in lines]

    #url = "https://flyers.canadiantire.ca/flyers/canadiantire-flyer?type=1&locale=fr&store_code=101&is_store_selection=true#!/flyers/canadiantire-flyer?flyer_run_id=617768"
    # Lien de la semaine en cours######IMPORTANT######IMPORTANT####IMPORTANT####
    #Probleme pour obtenir lien de la semaine en cours

    #url = 'https://www.reebee.com/flyers/10028/1382501'
    x = 1
    for url in urls:

        driver = webdriver.Chrome()

        #Agrandir la fenetre
        driver.maximize_window()

        #Ouvrir le lieu url
        driver.get(url)

        #Attendre quelques secondes
        driver.implicitly_wait(3)

        #Wait
        wait = WebDriverWait(driver, 10)

        #Identifier les pages de la circulaire
        pages = driver.find_elements_by_class_name('vertical-scroller')

        #Creer varialbe pour nommer les nouveaux urls produits
        split_url = url.split('/')
        flyer_id = split_url[-2]
        flyer_week = split_url[-1]

        products_urls = []
        #Creer une boucle pour capturer tous les liens de chaque page de la circulaire
        for page in pages:
                       
            #Trouver tous les items sur la page
            items = driver.find_elements_by_class_name('item-region')
            

            for item in items:
                item_id = item.get_attribute('data-item-id')
                new_url = f'https://www.reebee.com/flyers/{flyer_id}/{flyer_week}?itemId={item_id}'
                products_urls.append(new_url)
                #print(f'Page: {x}')
       
        with open(f'products_urls{x}.txt', 'w') as f:
            for item in products_urls:
                f.write(item)
                f.write('\n')

        x += 1
        driver.quit()

    #return products_urls
    return True 

def getFlyersPagesLinks(links):

    pages_urls_full_list = []

    for url, storename in links:

        driver = webdriver.Chrome()

        #Agrandir la fenetre
        driver.maximize_window()

        #Ouvrir le lieu url
        driver.get(url)

        #Attendre quelques secondes
        driver.implicitly_wait(3)

        #Wait
        wait = WebDriverWait(driver, 10)
        
        #Obtenir le nombre de pages de la circulaire
        scroll_pages = driver.find_elements_by_class_name('bar-snap-point')
        num_pages = len(scroll_pages)

        #Creer variable pour nommer les nouveaux urls produits
        split_url = url.split('/')
        flyer_id = split_url[-2]
        flyer_week = split_url[-1]
        
        #Sauvegarder le lien de chaque page dans une liste
        pages_urls = [f'https://www.reebee.com/flyers/{flyer_id}/{flyer_week}?page={i+1}' for i in range(num_pages)]
        
        pages_urls_full_list.append((pages_urls, storename)) 

        driver.quit()
        
        with open(f'{storename}.txt', 'w') as f:
            for page_url in pages_urls:
                f.write(page_url)
                f.write('\n')

    #return pages_urls_full_list
    #return True 

def getFlyersItemsLinks(pages_urls_full_list):
    #with open('Pages_urls1.txt', 'r') as f:
    #    lines = f.readlines()
    #    pages_urls = [line.strip('\n') for line in lines]

    
        
    for pages, storename in pages_urls_full_list:
        
        allpages_products_urls = []

        for page in pages:
        
            driver = webdriver.Chrome()

            #Agrandir la fenetre
            driver.maximize_window()

            #Ouvrir le lieu url
            driver.get(page)

            #Attendre quelques secondes
            driver.implicitly_wait(3)

            #Wait
            wait = WebDriverWait(driver, 10)

            #Printer le url de la page
            #print(page)

            #Trouver tous les items sur la page
            items = driver.find_elements_by_class_name('item-region')
            #print(len(items))
            #print('++++++++++++++++++++++++++++++++++')

            #Creer variable pour nommer les nouveaux urls produits
            split_url = page.split('/')
            flyer_id = split_url[-2]
            flyer_week_temp = split_url[-1]
            flyer_week = flyer_week_temp.split('?')[0]

            singlepage_products_urls = []
            
            for item in items:
                item_id = item.get_attribute('data-item-id')
                new_url = f'https://www.reebee.com/flyers/{flyer_id}/{flyer_week}?itemId={item_id}'
                singlepage_products_urls.append(new_url)
                #print(f'Page: {x}')
            
            allpages_products_urls.append(singlepage_products_urls)
        
            driver.quit()
        
    with open(f'products_urls_30.txt', 'w') as f:
        for singlepage_urls in allpages_products_urls:
            for product in singlepage_urls:
                f.write(product)
                f.write('\n')
    #return 
#TODO Preciser le xpath de l'image du produit et attendte qu'elle soit visible

def getItemsDetail():
    import datetime
    from datetime import date

    #Scraper items fonctionnne voir cellule d'en haut
    #Scraper item individuel doit etre perfectionner
    #Ajouter facon de continuer meme quand un produit a un element manquant
    #Probleme avec le titre

    #products_urls = getFlyersItemsLinks()

    #Tester la fonction en mode silo
    


    with open('products_urls2.txt', 'r') as f:
        lines = f.readlines()
        products_urls = [line.strip('\n') for line in lines]

    items_details_list = []

    for i, product in enumerate(products_urls):

        driver = webdriver.Chrome()

        #Agrandir la fenetre
        driver.maximize_window()

        #Ouvrir le lieu url
        driver.get(product)

        #Attendre quelques secondes
        driver.implicitly_wait(3)

        #print(f'Product: {x}')
        keys = ('image_url', 'title', 'price', 'duration', 'description', 'item_url')
        temp_values = 'ND'

        item_details = dict.fromkeys(keys, temp_values)
        
        #Item url
        item_details.update(item_url = product)
        #Image
        try:
            img = driver.find_element_by_class_name('image')
            if img:
                img_raw_url = img.get_attribute('style')
                #print(img_raw_url)

                img_raw_url_half = img_raw_url.split('url(')
                #print(img_raw_url_half)
                full_url = img_raw_url_half[1].split(');')
                #print(full_url[1])
                item_details.update(image_url = full_url[0])
            else:
                pass
        except:
            pass
        
        #Titre
        try:
            #title = driver.find_element_by_class_name('item-details.title')
            title = driver.find_element_by_xpath("//div[@class='item-details']/div[2]/div[@class='title']")
            if title:
                #print(title.text)
                item_details.update(title = title.text)
            else:
                pass
        
        #Price
            price = driver.find_element_by_class_name('main-price')
            if price:
                #print(price.text)
                item_details.update(price = price.text)
            else:
                pass
        except:
            pass
        
        #Duration
        try:
            time = driver.find_element_by_class_name('remaining-days ')
            if time:
                #print(time.text)
                item_details.update(duration = time.text)
            else:
                pass
        except:
            pass
        
        #Description
        try:
            description = driver.find_element_by_class_name('description-text')
            if description:
                #print(description.text)
                item_details.update(description = description.text)
            else:
                pass
        except:
            pass
        
        print(i)
        items_details_list.append(item_details)
        driver.quit()

    the_date = datetime.date.today()
    new_date = the_date.strftime('%x')
    current_date = new_date.replace('/', '_')   
    with open(f'scrapeditems-{current_date}.txt', 'w') as f:
        for item in items_details_list:
            f.write(str(item))
            f.write('\n')

    return True


#1 Obtenir les liens des ciruclaires outils
#flyerslinks = getFlyersLinks()
#ok fonctionnel

#TODO Rendre la fonction fonctionnelle sans sauvergader dans fichier
#2 Obtenir le lien de chaque page de chaque circulaire
#getFlyersPagesLinks(links)
#ok fonctionnel

#Obtenir les liens des items de chaque circulaire
#urls = getFlyersLinks()
#getFlyersItemsLinks()
#ok fonctionnel

#Obtenir les infos des liens de chaque circulaire
#getItemsDetail()
#probleme de boucle infini, trop lent
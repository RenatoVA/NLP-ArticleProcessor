from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import re

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import inch
import os

def setup_driver(download_dir):
    chrome_options = Options()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

download_dir = os.path.dirname(os.path.abspath(__file__))
download_dir=download_dir+"\downloaded_documents2"
driver = setup_driver(download_dir)

def pass_captcha():
    driver.get('https://scholar.google.com/')
    time.sleep(4)
    input_element = driver.find_element(By.ID, 'gs_hdr_tsi')
    input_element.send_keys('Some docuement title')
    button_element = driver.find_element(By.ID, 'gs_hdr_tsb')
    button_element.click()
    time.sleep(20)
def replace_colons_with_underscores(text):
    invalid_characters = r'[<>:"/\\|?*]'
    return re.sub(invalid_characters, '_', text)

def save_string_to_pdf(text, filename):
    file_path = os.path.join(download_dir, filename)
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    style = styles['Normal']
    flowables = []
    paragraphs = text.split('\n')
    for paragraph in paragraphs:
        p = Paragraph(paragraph, style)
        flowables.append(p)
    
    # Construye el documento PDF
    doc.build(flowables)
    print("PDF file saved successfully.")

def verifiy_download_isstarted(download_dir, initial_files, timeout=5):
    time.sleep(1)
    seconds = 0
    while seconds < timeout:
        new_files = set(os.listdir(download_dir)) - initial_files
        if new_files:
            return new_files.pop()
        time.sleep(1)
        seconds += 1
    return None
def extract_doi(text):
    doi_pattern = r'10.\d{4,9}/[-._;()/:A-Z0-9]+'
    match = re.search(doi_pattern, text, re.IGNORECASE)
    if match:
        return match.group(0)
    else:
        return None
def extract_doi_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return extract_doi(text)
def is_download_complete(download_dir, filename, timeout=30):
    file_path = os.path.join(download_dir, filename)
    crdownload_path = file_path + ".crdownload"
    
    seconds = 0
    while seconds < timeout:
        if os.path.exists(file_path) and not os.path.exists(crdownload_path):
            return True
        time.sleep(1)
        seconds += 1
    return False

def rename_downloaded_file(download_dir, old_filename, new_filename):
    old_file_path = os.path.join(download_dir, old_filename)
    new_file_path = os.path.join(download_dir, replace_colons_with_underscores(new_filename))
    os.rename(old_file_path, new_file_path)

def check_for_error():
    try:
        # Intentar encontrar el elemento por su clase
        error_element = driver.find_element(By.CSS_SELECTOR,"div.page-meta.entry-meta")
        # Verificar si el texto del elemento contiene el mensaje de error
        if "We could not find any results for your search" in error_element.text:
            raise Exception("Could not find the document on Harvard Site")
    except NoSuchElementException:
        # Si el elemento no se encuentra, no hay error
        pass


def search_onlibgen(title,doi):
    driver.get("https://libgen.is/scimag/")
    time.sleep(3)
    search_box = driver.find_element(By.XPATH,'//input[@type="text"]')
    search_box.send_keys(title)
    search_button=driver.find_element(By.XPATH,'//input[@type="submit"]')
    search_button.click()
    time.sleep(5)
    try:
       sci_hub_link = driver.find_element(By.LINK_TEXT, "Sci-Hub")
       sci_hub_link.click()
    except NoSuchElementException:
        if doi:
           try:
               search_box = driver.find_element(By.XPATH,'//input[@type="text"]')
               search_box.send_keys(title)
               search_button=driver.find_element(By.XPATH,'//input[@type="submit"]')
               search_button.click(doi)
               time.sleep(5)
               sci_hub_link = driver.find_element(By.LINK_TEXT, "Sci-Hub")
               sci_hub_link.click()
           except NoSuchElementException:
               raise Exception("Could not find the document on LibGen Doi")
        else:
            raise Exception("Could not find the document on LibGen Title")
    before_downloads = set(os.listdir(download_dir))
    time.sleep(3)
    buttons_div = driver.find_element(By.ID, "buttons")
    download_button = buttons_div.find_element(By.XPATH, ".//button[contains(text(), '↓ save')]")
    download_button.click()
    isdownloading = verifiy_download_isstarted(download_dir, before_downloads)
    if isdownloading:
       print("the document is downloading")
       if is_download_complete(download_dir,isdownloading):
           rename_downloaded_file(download_dir, isdownloading, f"{title}.pdf")
           print("Document has been downloaded from libgen")
       else:
           raise Exception("Could not download the pdf file from libgen")
    else:
       raise Exception("Could not download the pdf file from libgen")   

def search_on_harvard_site(title):
    driver.get("https://bsc.hks.harvard.edu/")
    time.sleep(3)
    search_box_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-secondary.nav-link.has-styling[data-toggle='modal'][data-target='#modal-search']")
    search_box_button.click()
    time.sleep(2)
    search_box=driver.find_element(By.ID, "searchform-s")
    search_box.send_keys(title)
    time.sleep(2)
    search_button=driver.find_element(By.ID, "searchform-submit")
    search_button.click()
    time.sleep(3)
    check_for_error()
    xpath = f"//a[contains(text(), '{title}')]"
    try:
       link = driver.find_element(By.XPATH, xpath)
       link.click()
    except NoSuchElementException:
        raise Exception("Could not find the document on Harvard Site")        
    time.sleep(3)
    before_downloads = set(os.listdir(download_dir))
    xpath2 = "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'download')]"
    download_button = driver.find_element(By.XPATH, xpath2)
    download_button.click()
    isdownloading = verifiy_download_isstarted(download_dir, before_downloads)
    if isdownloading:
       print("the document is downloading")
       if is_download_complete(download_dir,isdownloading):
           rename_downloaded_file(download_dir, isdownloading, f"{title}.pdf")
           print("Document has been downloaded from Harvard site")
       else:
           raise Exception("Could not download the pdf file from Harvard site")
    else:
       raise Exception("Could not download the pdf file from Harvard site")
def download_from_pubmed(title):
    link_list_element = driver.find_element(By.CLASS_NAME, 'full-text-links-list')
    link_list=link_list_element.find_elements(By.TAG_NAME, 'a')
    if len(link_list)>0:
        pmc_links = [link for link in link_list if link.get_attribute('data-ga-action') == 'PMC']
        if len(pmc_links) > 0:
            
            driver.execute_script("arguments[0].setAttribute('target', '_self')", pmc_links[0])
            driver.execute_script("arguments[0].click();", pmc_links[0])
            time.sleep(3)
            section_element = driver.find_element(By.XPATH, '//section[h6[text()="Other Formats"]]')
            try:
               before_downloads = set(os.listdir(download_dir))
               pdf_link = section_element.find_element(By.XPATH, './/a[contains(text(), "PDF") or contains(text(), "pdf")]')
               driver.execute_script("arguments[0].click();", pdf_link)
               isdownloading = verifiy_download_isstarted(download_dir, before_downloads)
               if isdownloading:
                   print("the document is downloading")
                   if is_download_complete(download_dir,isdownloading):
                       rename_downloaded_file(download_dir, isdownloading, f"{title}.pdf")
                       print("Document has been downloaded from link site - pubmed")
                   else:
                       raise Exception("Could not download the pdf file from link-site pubmed")
               else:
                   raise Exception("Could not download the pdf file from link-site pubmed")
            except NoSuchElementException:
                try:
                   friendly_link = section_element.find_element(By.XPATH, './/a[contains(text(), "Printer") or contains(text(), "printer")]')
                   driver.execute_script("arguments[0].click();", friendly_link)
                   time.sleep(3)
                   content_element = driver.find_element(By.ID, 'mc')
                   text = content_element.get_attribute('innerHTML')
                   soup = BeautifulSoup(text, 'html.parser')
                   text_content = soup.get_text(separator=' ')
                   save_string_to_pdf(text_content, f"{title}.pdf")
                except NoSuchElementException:
                   raise Exception("Could not find PDF link on the page")
        else:
            raise Exception("Could not find PMC link on the page")

def download_from_link(title,link):
    if "pubmed" in driver.current_url:
        download_from_pubmed(title)
    else:
       links = driver.find_elements(By.TAG_NAME, 'a')
       download_links = []
       for link in links:
           if "download" in link.text.lower():
               download_links.append(link)
           else:
           # Busca elementos hijos con la palabra "download"
               child_elements = link.find_elements(By.XPATH, './/*[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "download") or contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "pdf")]')
               if child_elements:
                   download_links.append(link)
       if len(download_links) > 0:
           before_downloads = set(os.listdir(download_dir))
           driver.execute_script("arguments[0].click();", download_links[0])
           isdownloading = verifiy_download_isstarted(download_dir, before_downloads)
           if isdownloading:
                print("the document is downloading")
                if is_download_complete(download_dir,isdownloading):
                     rename_downloaded_file(download_dir, isdownloading, f"{title}.pdf")
                     print("Document has been downloaded from link site")
                else:
                     raise Exception("Could not download the pdf file from link-site")
           else:
               try:
                   input_element = driver.find_element(By.XPATH, '//input[contains(@value, "Download")]')
                   driver.execute_script("arguments[0].click();", input_element)
                   isdownloading = verifiy_download_isstarted(download_dir, before_downloads)
                   if isdownloading:
                        print("the document is downloading")
                        if is_download_complete(download_dir,isdownloading):
                            rename_downloaded_file(download_dir, isdownloading, f"{title}.pdf")
                            print("Document has been downloaded from link site")
                        else:
                            raise Exception("Could not download the pdf file from link-site")
                   else:
                            raise Exception("Could not download the pdf file from link-site")
               except NoSuchElementException:
                   raise Exception("Could not found download link on the page")
       else:
            raise Exception("Could not found any download link on the page")
               
def search_on_google_schoolar(title):
    google_schoolar = driver.find_element(By.XPATH, '//a[text()="Google Scholar"]')
    google_schoolar.click()
    time.sleep(3)
    try:
        link_element = driver.find_element(By.XPATH, f'//a[contains(text(),"{title}")]')
        before_downloads = set(os.listdir(download_dir))
        link_element.click()
        isdownloading = verifiy_download_isstarted(download_dir, before_downloads)
        if isdownloading:
            print("the document is downloading")
            if is_download_complete(download_dir,isdownloading):
                rename_downloaded_file(download_dir, isdownloading, f"{title}.pdf")
                print("Document has been downloaded from google schoolar")
                return
            else:
                raise Exception("Could not download the pdf file from google schoolar")
    except NoSuchElementException:
        raise Exception("Could not find the document on Google Schoolar")
    time.sleep(3)
    links = driver.find_elements(By.TAG_NAME, 'a')
    download_links = []
    for link in links:
        if "download" in link.text.lower():
            download_links.append(link)
        else:
        # Busca elementos hijos con la palabra "download"
            child_elements = link.find_elements(By.XPATH, './/*[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "download") or contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "pdf")]')
            if child_elements:
                download_links.append(link)
    if len(download_links) > 0:
        before_downloads = set(os.listdir(download_dir))
        driver.execute_script("arguments[0].click();", download_links[0])
        isdownloading = verifiy_download_isstarted(download_dir, before_downloads)
        if isdownloading:
            print("the document is downloading")
            if is_download_complete(download_dir,isdownloading):
                rename_downloaded_file(download_dir, isdownloading, f"{title}.pdf")
                print("Document has been downloaded from google schoolar")
            else:
                raise Exception("Could not download the pdf file from google schoolar")
    else:
        raise Exception("Could not found download link on google schoolar page")
def use_abstract_as_text(title,link):
    driver.get(link)
    time.sleep(3)
    if "pubmed" in driver.current_url:
        try:
           header_element = driver.find_element(By.XPATH, '//h1[contains(text(), "Abstract")] | //h2[contains(text(), "Abstract")] | //h3[contains(text(), "Abstract")] | //h4[contains(text(), "Abstract")] | //h5[contains(text(), "Abstract")] | //h6[contains(text(), "Abstract")] | //h1[contains(text(), "abstract")] | //h2[contains(text(), "abstract")] | //h3[contains(text(), "abstract")] | //h4[contains(text(), "abstract")] | //h5[contains(text(), "abstract")] | //h6[contains(text(), "abstract")]')
           parent_element = header_element.find_element(By.XPATH, './..')
           parent_html = parent_element.get_attribute('outerHTML')
           soup = BeautifulSoup(parent_html, 'html.parser')
           text_content = soup.get_text(separator=' ')
           save_string_to_pdf(text_content, f"{title}.pdf")
           print("Document-Absctract has been extracted from pubmed-link")
        except NoSuchElementException:
            raise Exception("Could not find abstract on the page")
    else:
        try:
           header_element = driver.find_element(By.XPATH, '//h1[contains(text(), "Abstract")] | //h2[contains(text(), "Abstract")] | //h3[contains(text(), "Abstract")] | //h4[contains(text(), "Abstract")] | //h5[contains(text(), "Abstract")] | //h6[contains(text(), "Abstract")] | //h1[contains(text(), "abstract")] | //h2[contains(text(), "abstract")] | //h3[contains(text(), "abstract")] | //h4[contains(text(), "abstract")] | //h5[contains(text(), "abstract")] | //h6[contains(text(), "abstract")]')
           grandparent_element = header_element.find_element(By.XPATH, './../../..')
           grandparent_html = grandparent_element.get_attribute('outerHTML')
           soup = BeautifulSoup(parent_html, 'html.parser')
           text_content = soup.get_text(separator=' ')
           save_string_to_pdf(text_content, f"{title}.pdf")
           print("Document-Absctract has been extracted from link-site")
        except NoSuchElementException:
            raise Exception("Could not find abstract on the page")


def donwload_raw_text(title,link):
    driver.get(link)
    time.sleep(3)
    doi=extract_doi_from_html(driver.page_source)
    try:
        print("Trying on link site......")
        download_from_link(title,link)
    except Exception as e:
        print(e)
        try:
           print("Trying on Harvard site......")
           search_on_harvard_site(title)
        except Exception as a:
           print(a)
           try:
               print("Trying on LibGen site......")
               search_onlibgen(title,doi)
           except Exception as b:
               print(b)
               try:
                     print("Trying on Google Schoolar......")
                     search_on_google_schoolar(title)
               except Exception as c:
                     print(c)
                     try:
                            print("Trying to use abstract as text......")
                            use_abstract_as_text(title,link)
                     except Exception as d:
                            print(d)
    finally:
        print("Scraping is done")

def download_raw_text_from_title(title):
    try:
        print("Trying on Harvard site......")
        search_on_harvard_site(title)
    except Exception as a:
        print(a)
        try:
            print("Trying on LibGen site......")
            search_onlibgen(title)
        except Exception as b:
            print(b)
            try:
                print("Trying on Google Schoolar......")
                search_on_google_schoolar(title)
            except Exception as c:
                print(c)
    finally:
        print("Scraping is done")


    



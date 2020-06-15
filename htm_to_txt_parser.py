# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 17:21:03 2020

@author: LukaszMalucha
"""

from pathlib import Path
import bs4 as bs
import re
import shutil

import operator
import pandas as pd

BRANDS = []

FOLDERS = []
for brand in BRANDS:
    try:
        CURRENT_PATH = Path(Path.cwd(), "EXTRACTED_FILES", brand)
        BRAND_FOLDERS = [str(x) for x in CURRENT_PATH.iterdir() if x.is_dir()]  
        for element in BRAND_FOLDERS:      
            FOLDERS.append(element)
    except:
        pass

    


def sort_strings(l):
    """Group strings by their page location in order to keep row together"""
    sorted_strings = {}
    for string in l:
        if string[0] not in sorted_strings:
            sorted_strings[string[0]] = []
        sorted_strings[string[0]].append(string[1]) 
               
    
    sorted_values = sorted(sorted_strings.items(), key=operator.itemgetter(0))
    
    sorts = []
    for element in sorted_values:
        sorts.append(list(reversed(element[1]))) 
        
        
    # SIGNAL POSSIBLE TABLE ROW 
    sorted_string_list = []     
    for element in sorts:
        " ".join(element)
        row_string = element[0]
        row_string = row_string.replace("\n", " ")
        sorted_string_list.append(row_string)             
        
    return sorted_string_list


# Get Page count and page frames 

def document_pages(soup):
    """Get Page count and page frames in order to sort strings by page"""
    page_frames = [ data for data in soup.select('div') if "<a name=" in str(data)]    
    
    pages_list= []
    for count,page in enumerate(page_frames):
        tup = ()
        top = int(re.search(r'(?is)(top:)(.*?)(px)',str(page.get('style'))).group(2))
        bottom = top + 842
        tup = (count+1, top, bottom)
        pages_list.append(tup)
    
    return pages_list    
        
    


def text_per_page(soup, pages):
    """Return dictionary of {page<n> : "[ Strings per page n ]"} """    
    pages_list = []
    header_spans = []
    
    divs = [ data for data in soup.select('div') if 'top' in str(data)]
    
    for page in pages:
        page_text = []  
        for div in divs:
            page_location = re.search(r'(?is)(top:)(.*?)(px)',str(div.get('style'))).group(2)
            
            # Get a header area to identify potential title(between 0 - 285px, roughly 33%)            
            if int(page_location) < 285:
                spans = [ data for data in div.select('span') if 'font-size' in str(data)]
                for span in spans:
                    font_size = re.search(r'(?is)(font-size:)(.*?)(px)',str(span.get('style'))).group(2)
                    tup = [str(span.text).strip(), int(font_size.strip())]
                    header_spans.append(tup)
        
            # Sort text by page
            if page[1] < int(page_location) < page[2]:
                page_text.append((int(page_location), str(div.text).strip()))
                
                  
        page_text_sorted = sort_strings(page_text)
        pages_list.append(page_text_sorted)
              
    
    return pages_list    



  

def extract_text(filename):  
    input_file_name = Path(filename).stem
    brand = str(filename).split("\\")[-3]
    file_path = Path(Path.cwd(), "EXTRACTED_FILES", brand, input_file_name, filename)
    
# Turn html into bs.soup
    with open(str(file_path), "r", encoding="UTF-8") as f:        
        soup = bs.BeautifulSoup(f, "lxml")   
        pages = document_pages(soup)
        pages_text = text_per_page(soup, pages)
  
# Save data as json
        output_txt_path = Path(Path.cwd(), "EXTRACTED_FILES", brand, input_file_name, "pages")
        output_txt_path.mkdir(parents=True, exist_ok=True) 
        for i, page in enumerate(pages_text):
            input_file_name = input_file_name.replace(" ", "_")
            text_file_path = Path(output_txt_path, input_file_name + "-page-" + str(i+1) + ".csv")  
            df = pd.DataFrame({f"PAGE {i+1}" : page})
            df.to_csv(text_file_path, encoding='utf-8-sig', index=False)

    
    return pages_text

    


def text_extractor():
    """Compiler for html text extraction"""
    for i, folder in enumerate(FOLDERS):
        print(i)
        htmls = list(Path(folder).glob('*.html'))
        tables = list(Path(folder).glob('*-table-*.csv'))
        tables_folder = Path(folder, "tables")
        tables_folder.mkdir(parents=True, exist_ok=True)     
            
        for element in tables:
            shutil.copy(str(element), str(tables_folder))
            element.unlink()
            
        for element in htmls:
            extract_text(str(element))    
            
            

        


text_extractor()

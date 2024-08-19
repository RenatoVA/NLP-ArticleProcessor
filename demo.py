from distilbert_model_fintuned import DistilBERTClass,Classifier
import procesing_pdf as ppdf
import pandas as pd
import os
import numpy as np
import locations_model as lm
import extractkeywords as ek
import re
import citations_model as cm
classifier= Classifier()
categories = {
    0: "Business, Firms, and Finance",
    1: "Conflict, Peace, and Security",
    2: "Education and Human Development",
    3: "Climate and Energy",
    4: "Gender and Inclusion",
    5: "Health and Wellbeing",
    6: "Culture, Institutions, and History",
    7: "Labor and Urban Economics",
    8: "Governance, Political Economy, and Public Management",
    9: "Social Welfare and Public Finance",
    10: "Technology and Data Science",
    11: "Trade, Growth, and Regional Economics"
}
def replace_colons_with_underscores(text):
    invalid_characters = r'[<>:"/\\|?*]'
    return re.sub(invalid_characters, '_', text)
def predict_labels(text):
    exceptions=""
    predictions=classifier.predict(text)
    indices = np.where((predictions >= 0.1) & (predictions <= 0.5))[0]
    predictions=np.where(predictions >= 0.1, 1, 0)
    if len(indices) >= 0:
       exceptions+=";".join([categories[i] for i in indices])
    return predictions, exceptions
def contains_working(text):
    pattern = r'\bworking\b|\bWorking\b'
    if re.search(pattern, text):
        return True
    else:
        return False
def start_scraping():
    download_dir="c:\proyectos\scraping\downloaded_documents"
    df=pd.read_excel('data.xlsx',index_col=False)
    for index, row in df.iterrows():
        pdf_filename = f"{row['Title']}.pdf"
        pdf_filename=replace_colons_with_underscores(pdf_filename)
        pdf_path = os.path.join(download_dir, pdf_filename)
        if os.path.exists(pdf_path):
            print("procesando: ",index)
            print(row['Title'])
            #Extract text from pdf
            text=ppdf.get_clean_text(replace_colons_with_underscores(row['Title']))
            #Predict labels for the text
            labels, label_exceptions = predict_labels(text)
            #Update the dataframe with the labels and exceptions
            df.iloc[index, 19:31] = ['Yes' if value == 1 else '' for value in labels]
            print("labels",labels,label_exceptions)
            #Extract regions and countries from the text
            regions, countries,locations_comments = lm.get_locations(text)
            print("regions",regions,countries,locations_comments)
            if regions==[0,0,0,0,0,0]:
                locations_comments='locations_empty'
                row["NOT Int'l Dev?"]='Posible'
            df.iloc[index, 31:38] = ['Yes' if value == 1 else '' for value in regions]
            df.iloc[index,39:40]=countries
            #Extract keywords from the text
            #df.iloc[index,38:39]=ek.extract_keywords(text)
            #Extract citations from the text
            if contains_working(row['Type']):
                if row['External Link (URL)']=='':
                   row['Citation is correct?']='No'
                else:
                   citation=cm.verify_citations(row['External Link (URL)'],row['Title'],row['Citation'])
                   if citation=='no':
                      row['Citation is correct?']='No'
                   else:
                      row['Citation is correct?']='Yes'
            else:
                    row['Citation is correct?']='Yes'
            row['Labels_comments'] = label_exceptions
            row['Locations_comments']=locations_comments
            
        else:
           pass
    return df
df=start_scraping()
df.to_excel('new_procesed_data.xlsx',index=False)
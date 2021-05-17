#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import pandas as pd
import requests
from stat import S_IREAD, S_IRGRP, S_IROTH
from styleframe import StyleFrame, Styler, utils


# ### Funciones

# In[ ]:


def no_pag_x_genero(genero):
    ### No. de paginas en cada genero
    url = 'https://repelishd.me/genero/' + genero
    source=requests.get(url).text
    soup=BeautifulSoup(source, 'lxml')
    try:
        paginas=soup.find(class_='pagination')
        total_paginas = int(paginas.span.text.split(' ')[3])
    except Exception as e:
        total_paginas = 1
    return total_paginas


# In[ ]:


def peli_x_genero(genero, pagina):
    ### Busqueda de peliculas en cada genero
    url = 'https://repelishd.me/genero/'+genero + '/' + 'page' +  '/' + str(pagina+1)
    source=requests.get(url).text
    soup=BeautifulSoup(source, 'lxml')    
    print(genero)
    print(pagina + 1, 'de', total_paginas, url)
    print()
    return soup 


# In[ ]:


def datos_peliculas(pelicula):
    #datos de las peliculas
    nombre = pelicula.h3.text
    try:
        rating = float(pelicula.find('div', class_='rating').text)
    except Exception as e:
        rating=None
    try:
        año=pelicula.find_all('span')[2].text
    except Exception as e:
        año=None
    audio=pelicula.find('div', class_='audio')
    audio_latino = 'Si'if "latino" in str(audio) else 'No'
    
    # Ir a https://repelishd.me/pelicula/erase-una-vez-en-queens-2021/ y tomar la informacion de la SINOPSIS
    url=str(pelicula.h3.a).split('"')[1]
    try:
        source=requests.get(url).text
        soup=BeautifulSoup(source, 'lxml')          
        informacion = soup.find(class_="wp-content sinopxs")
        lista_sinopsis = informacion.find_all('p')
        sinopsis = lista_sinopsis[1].text if len(lista_sinopsis[1].text) > len(lista_sinopsis[0].text) else lista_sinopsis[0].text
        
    except Exception as e:
        sinopsis = None
        
    return nombre, año, rating, año, audio_latino, url, sinopsis


# ### Hacer Catalogo de Peliculas (https://repelishd.me/)

# In[ ]:


### Dataframe
df=pd.DataFrame(columns=('Pelicula', 'Genero', 'Rating', 'Año', 'Doblada', 'Sinopsis', 'Url'))

### Requests
generos=['clasicas', 'drama', 'misterio', 'belica', 'accion', 'aventura', 'suspense', 'crimen', 'documental', 'animacion', 'historia', 'comedia']

for genero in generos:
    total_paginas = no_pag_x_genero(genero)
    
    for pagina in range(total_paginas):
        soup = peli_x_genero(genero, pagina)
 
        for pelicula in soup.find_all(class_='item movies'):
            nombre, año, rating, año, audio_latino, url, sinopsis = datos_peliculas(pelicula)
            df=df.append({'Pelicula':nombre, 'Genero':genero,'Rating':rating, 'Año':año, 'Doblada':audio_latino, 'Url':url, 'Sinopsis':sinopsis}, ignore_index=True)


# ### Guardar en Excel Catalogo

# In[ ]:


df.drop_duplicates(subset=['Pelicula', 'Rating'], keep='first', inplace=True, ignore_index=False)
df.sort_values(by=['Rating', 'Año'],  ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)
df.index += 1 
df.head(20)

sf=StyleFrame(df)
sf=sf.set_column_width(columns=['Pelicula'], width=45.00)
sf=sf.set_column_width(columns=['Url'], width=71.00)
sf=sf.set_column_width(columns=['Genero'], width=15.00)
sf=sf.set_column_width(columns=['Rating'], width=15.00)
sf=sf.set_column_width(columns=['Año'], width=15.00)
sf=sf.set_column_width(columns=['Doblada'], width=15.00)
sf=sf.set_column_width(columns=['Sinopsis'], width=90.00)
sf.to_excel(excel_writer='catalogo de peliculas.xlsx', index=True).save()


# In[ ]:





# In[ ]:





# In[ ]:





# ### Codigo deshechado

# In[ ]:


# url = 'https://repelishd.me/pelicula/el-libro-negro-online/'
# source=requests.get(url).text
# soup=BeautifulSoup(source, 'lxml')    

# informacion = soup.find(class_="wp-content sinopxs")
# lista_sinopsis = soup.find_all('p')
# sinopsis = lista_sinopsis[1].text if len(lista_sinopsis[1].text) > len(lista_sinopsis[0].text) else lista_sinopsis[0].text
# lista_sinopsis[0].text


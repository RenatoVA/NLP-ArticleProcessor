phrases = ["access educational","literacy software","technologyaided instruction","education technology","education tools","education technology","learning technology","innovations edtech","edtech innovations","innovations edtech","edtech innovations"]

# Crear un conjunto para almacenar los pares de palabras ordenados
unique_phrases = set()

# Iterar sobre la lista y añadir los pares de palabras ordenados al conjunto
for phrase in phrases:
    # Dividir la frase en palabras y ordenarlas
    words = tuple(sorted(phrase.split()))
    unique_phrases.add(words)

# Convertir el conjunto de nuevo a una lista de cadenas
result = [" ".join(words) for words in unique_phrases]

# Imprimir el resultado
print(result)
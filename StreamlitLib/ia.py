# import pytesseract
# from PIL import Image
# import cv2
# import re

# # Chemin vers l'exécutable de Tesseract (assurez-vous d'avoir installé Tesseract)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # Fonction pour prétraiter l'image
# def preprocess_image(image_path):
#     # Charger l'image
#     image = cv2.imread(image_path)

#     # Convertir en niveaux de gris
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Appliquer un seuil pour binariser l'image
#     _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

#     # Redressement de l'image (optionnel)
#     # Utiliser des techniques de redressement si nécessaire

#     return binary

# # Fonction pour extraire et analyser le texte
# def extract_prices(image_path):
#     # Prétraiter l'image
#     processed_image = preprocess_image(image_path)

#     # Utiliser Tesseract pour l'OCR
#     text = pytesseract.image_to_string(processed_image)

#     # Analyse du texte pour extraire les prix
#     lines = text.split('\n')
#     price_pattern = re.compile(r'\d+,\d{2}|\d+\.\d{2}')  # Adapté pour des prix avec virgule ou point

#     products = []
#     for line in lines:
#         match = price_pattern.search(line)
#         if match:
#             product_name = line[:match.start()].strip()
#             price = match.group()
#             products.append((product_name, price))

#     return products

# # Chemin de l'image du ticket de caisse
# image_path = '/workspaces/Streamlit/StreamlitLib/truc.jpeg'  # Remplacez par le chemin de votre image

# # Extraire les prix
# products = extract_prices(image_path)

# # Vérifier les résultats
# for product in products:
#     product_name, price = product
#     if not product_name or not price:
#         print(f"Erreur de reconnaissance pour le produit: {product}")
#     else:
#         print(f"Produit: {product_name}, Prix: {price}")

# if not products:
#     print("Aucun produit reconnu. Veuillez vérifier l'image du ticket de caisse.")

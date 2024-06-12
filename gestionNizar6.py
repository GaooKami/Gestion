import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from tkcalendar import Calendar, DateEntry

# Variable globale pour stocker les données
donnees = []

# Fonction pour vérifier l'existence du fichier CSV et le créer s'il n'existe pas
def verifier_et_creer_fichier(fichier_csv):
    if not os.path.exists(fichier_csv):
        with open(fichier_csv, 'w', newline='') as csvfile:
            fieldnames = ['Date', 'Description', 'Montant']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        messagebox.showinfo("Information", f"Le fichier {fichier_csv} n'a pas été trouvé et a été créé.")

# Fonction pour charger les données à partir du fichier CSV
def charger_donnees(fichier_csv):
    global donnees
    donnees = []
    verifier_et_creer_fichier(fichier_csv)
    with open(fichier_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            donnees.append({
                'Date': row['Date'],
                'description': row['Description'],
                'montant': float(row['Montant'])
            })

# Fonction pour sauvegarder les données dans le fichier CSV
def sauvegarder_donnees(fichier_csv):
    with open(fichier_csv, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Description', 'Montant']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for donnee in donnees:
            writer.writerow({'Date': donnee['date'], 'Description': donnee['description'], 'Montant': donnee['montant']})

# Fonction pour ajouter un produit au stock
def ajouter_produit():
    global donnees
    date_achat = calendrier_achat.get_date().strftime('%d/%m/%Y')
    nom_produit = entry_nom_produit.get()
    quantite_achetee = int(entry_quantite.get())
    prix_achat_unitaire = float(entry_prix_achat.get())
    prix_vente_unitaire = float(entry_prix_vente.get())
    
    donnees.append({
        'date_achat': date_achat,
        'nom_produit': nom_produit,
        'quantite_achetee': quantite_achetee,
        'prix_achat_unitaire': prix_achat_unitaire,
        'prix_vente_unitaire': prix_vente_unitaire
    })
    sauvegarder_donnees('stock.csv')
    messagebox.showinfo("Produit ajouté", "Le produit a été ajouté au stock avec succès.")

# Fonction pour vendre un produit
def vendre_produit():
    global donnees
    produit_selectionne = combo_produits.get()
    quantite_vendue = int(entry_quantite_vendue.get())

    for produit in donnees:
        if produit['nom_produit'] == produit_selectionne:
            if produit['quantite_achetee'] >= quantite_vendue:
                produit['quantite_achetee'] -= quantite_vendue
                sauvegarder_donnees('stock.csv')
                messagebox.showinfo("Vente réussie", "La vente a été effectuée avec succès.")
            else:
                messagebox.showerror("Erreur", "La quantité demandée est supérieure à la quantité disponible en stock.")
            break
    else:
        messagebox.showerror("Erreur", "Produit non trouvé dans le stock.")

# Fonction de validation pour les entrées numériques
def valider_entree(champ, action, contenu):
    if action == '1':  # Si c'est une insertion
        if champ == 'int':  # Si le champ attend un entier
            return contenu.isdigit()
        elif champ == 'float':  # Si le champ attend un flottant
            try:
                float(contenu)
                return True
            except ValueError:
                return False
    return True  # Si c'est une suppression, toujours autoriser

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Gestion de Stock et Finances")

# Validation des entrées numériques
validation_int = fenetre.register(lambda action, contenu: valider_entree('int', action, contenu))
validation_float = fenetre.register(lambda action, contenu: valider_entree('float', action, contenu))

# Chargement des données
charger_donnees('stock.csv')

# Cadre pour l'ajout de produits au stock
cadre_ajout_produit = tk.LabelFrame(fenetre, text="Ajouter un Produit au Stock")
cadre_ajout_produit.grid(row=0, column=0, padx=10, pady=5, sticky="w")

label_date_achat = tk.Label(cadre_ajout_produit, text="Date d'achat du produit :")
label_date_achat.grid(row=0, column=0, padx=5, pady=5)
calendrier_achat = DateEntry(cadre_ajout_produit, date_pattern='dd/mm/yyyy')
calendrier_achat.grid(row=0, column=1, padx=5, pady=5)

label_nom_produit = tk.Label(cadre_ajout_produit, text="Nom du produit :")
label_nom_produit.grid(row=1, column=0, padx=5, pady=5)
entry_nom_produit = tk.Entry(cadre_ajout_produit)
entry_nom_produit.grid(row=1, column=1, padx=5, pady=5)

label_quantite = tk.Label(cadre_ajout_produit, text="Quantité achetée :")
label_quantite.grid(row=2, column=0, padx=5, pady=5)
entry_quantite = tk.Entry(cadre_ajout_produit, validate="key", validatecommand=(validation_int, '%d', '%P'))
entry_quantite.grid(row=2, column=1, padx=5, pady=5)

label_prix_achat = tk.Label(cadre_ajout_produit, text="Prix d'achat unitaire (€) :")
label_prix_achat.grid(row=3, column=0, padx=5, pady=5)
entry_prix_achat = tk.Entry(cadre_ajout_produit, validate="key", validatecommand=(validation_float, '%d', '%P'))
entry_prix_achat.grid(row=3, column=1, padx=5, pady=5)

label_prix_vente = tk.Label(cadre_ajout_produit, text="Prix de vente unitaire (€) :")
label_prix_vente.grid(row=4, column=0, padx=5, pady=5)
entry_prix_vente = tk.Entry(cadre_ajout_produit, validate="key", validatecommand=(validation_float, '%d', '%P'))
entry_prix_vente.grid(row=4, column=1, padx=5, pady=5)

bouton_ajouter_produit = tk.Button(cadre_ajout_produit, text="Ajouter Produit", command=ajouter_produit)
bouton_ajouter_produit.grid(row=5, columnspan=2, padx=5, pady=5)

# Cadre pour la vente de produits
cadre_vente_produit = tk.LabelFrame(fenetre, text="Vendre un Produit")
cadre_vente_produit.grid(row=1, column=0, padx=10, pady=5, sticky="w")

label_produit = tk.Label(cadre_vente_produit, text="Produit à vendre :")
label_produit.grid(row=0, column=0, padx=5, pady=5)
combo_produits = ttk.Combobox(cadre_vente_produit, values=[produit['nom_produit'] for produit in donnees])
combo_produits.grid(row=0, column=1, padx=5, pady=5)

label_quantite_vendue = tk.Label(cadre_vente_produit, text="Quantité à vendre :")
label_quantite_vendue.grid(row=1, column=0, padx=5, pady=5)
entry_quantite_vendue = tk.Entry(cadre_vente_produit, validate="key", validatecommand=(validation_int, '%d', '%P'))
entry_quantite_vendue.grid(row=1, column=1, padx=5, pady=5)

bouton_vendre_produit = tk.Button(cadre_vente_produit, text="Vendre Produit", command=vendre_produit)
bouton_vendre_produit.grid(row=2, columnspan=2, padx=5, pady=5)

# Cadre pour l'affichage de la valeur totale du stock
cadre_valeur_stock = tk.LabelFrame(fenetre, text="Valeur Totale du Stock")
cadre_valeur_stock.grid(row=0, column=1, padx=10, pady=5, sticky="n")

label_valeur_stock = tk.Label(cadre_valeur_stock, text="Valeur totale du stock :")
label_valeur_stock.grid(row=0, column=0, padx=5, pady=5)
valeur_stock = tk.Label(cadre_valeur_stock, text="0 €")
valeur_stock.grid(row=0, column=1, padx=5, pady=5)

# Cadre pour l'affichage de l'argent en banque
cadre_argent_banque = tk.LabelFrame(fenetre, text="Argent en Banque")
cadre_argent_banque.grid(row=1, column=1, padx=10, pady=5, sticky="n")

label_argent_banque = tk.Label(cadre_argent_banque, text="Argent en Banque :")
label_argent_banque.grid(row=0, column=0, padx=5, pady=5)
argent_banque = tk.Label(cadre_argent_banque, text="0 €")
argent_banque.grid(row=0, column=1, padx=5, pady=5)

# Cadre pour l'affichage de l'historique
cadre_historique = tk.LabelFrame(fenetre, text="Historique")
cadre_historique.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

# Données
donnees = []
charger_donnees('stock.csv')

# Calcul de la valeur totale du stock
def calculer_valeur_stock():
    global donnees
    valeur_totale = sum(produit['quantite_achetee'] * produit['prix_achat_unitaire'] for produit in donnees)
    valeur_stock.config(text=f"{valeur_totale} €")

# Calcul de l'argent en banque
def calculer_argent_banque():
    global donnees
    argent_total = sum(donnee['montant'] for donnee in donnees)
    argent_banque.config(text=f"{argent_total} €")

# Mise à jour de la valeur totale du stock et de l'argent en banque
calculer_valeur_stock()
calculer_argent_banque()

# Lancement de la boucle principale
fenetre.mainloop()

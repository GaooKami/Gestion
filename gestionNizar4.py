import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import re
from tkcalendar import Calendar, DateEntry

# Variable globale pour stocker la valeur totale du stock
valeur_stock = 0

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
    donnees = []
    verifier_et_creer_fichier(fichier_csv)
    with open(fichier_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            donnees.append({
                'date': row['Date'],
                'description': row['Description'],
                'montant': float(row['Montant'])
            })
    return donnees

# Fonction pour sauvegarder les données dans le fichier CSV
def sauvegarder_donnees(fichier_csv, donnees):
    with open(fichier_csv, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Description', 'Montant']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for donnee in donnees:
            writer.writerow({'Date': donnee['date'], 'Description': donnee['description'], 'Montant': donnee['montant']})

# Fonction pour afficher le solde de compte bancaire et les transactions récentes
def afficher_transactions():
    transactions = charger_donnees('transactions.csv')
    if transactions:
        messagebox.showinfo("Transactions Récentes", "Transactions Récentes :\n\n" +
                            "\n".join([f"{transaction['date']}: {transaction['description']} ({transaction['montant']} €)" for transaction in transactions]))
    else:
        messagebox.showinfo("Transactions Récentes", "Aucune transaction trouvée.")

# Fonction pour valider le format de la date (jjmmaaaa)
def valider_date(date):
    pattern = re.compile(r"^\d{8}$")
    if not pattern.match(date):
        return False
    
    day = int(date[:2])
    month = int(date[2:4])
    year = int(date[4:])
    
    if day < 1 or day > 31:
        return False
    if month < 1 or month > 12:
        return False
    if year < 1000 or year > 9999:
        return False
    
    return True

# Fonction pour valider le format du montant
def valider_montant(montant):
    try:
        float(montant)
        return True
    except ValueError:
        return False

# Fonction pour formater automatiquement la date saisie
def formater_date(event):
    contenu = entry_date.get().replace("/", "")
    if len(contenu) > 8:
        contenu = contenu[:8]
    if len(contenu) > 4:
        contenu = f"{contenu[:2]}/{contenu[2:4]}/{contenu[4:]}"
    elif len(contenu) > 2:
        contenu = f"{contenu[:2]}/{contenu[2:]}"
    entry_date.delete(0, tk.END)
    entry_date.insert(0, contenu)

# Fonction pour saisir manuellement les dépenses en espèces
def saisir_depenses():
    global donnees
    date_depense = entry_date.get().replace("/", "")
    description_depense = entry_description.get()
    montant_depense = entry_depense.get()

    if not valider_date(date_depense):
        messagebox.showerror("Erreur", "Veuillez entrer une date valide au format jjmmaaaa.")
        return

    if not valider_montant(montant_depense):
        messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")
        return

    date_depense = f"{date_depense[:2]}/{date_depense[2:4]}/{date_depense[4:]}"  # Formater la date correctement
    montant_depense = -float(montant_depense)  # Modification pour soustraire le montant
    donnees.append({'date': date_depense, 'description': description_depense, 'montant': montant_depense})  # Modification pour soustraire le montant
    sauvegarder_donnees('transactions.csv', donnees)
    messagebox.showinfo("Dépense ajoutée", "Dépense ajoutée avec succès.")

# Fonction pour afficher les dépenses existantes
def afficher_depenses():
    depenses = [f"{depense['date']}: {depense['description']} ({-depense['montant']} €)" for depense in donnees if depense['montant'] < 0]
    if depenses:
        messagebox.showinfo("Dépenses", "Liste des Dépenses :\n\n" + "\n".join(depenses))
    else:
        messagebox.showinfo("Dépenses", "Aucune dépense trouvée.")

# Fonction pour calculer la valeur totale du stock
def calculer_valeur_stock():
    global valeur_stock
    valeur_stock = 0
    messagebox.showinfo("Valeur Totale du Stock", f"Valeur totale du stock : {valeur_stock} €")

# Fonction pour soustraire les dépenses au solde total
def soustraire_depenses(solde_total):
    total_depenses = sum(depense['montant'] for depense in donnees if depense['montant'] < 0)
    solde_total += total_depenses  # Correction pour soustraire les dépenses
    return solde_total

# Fonction pour afficher le solde total en combinant l'argent en banque et la valeur du stock
def afficher_solde_total():
    global valeur_stock
    try:
        argent_banque = float(entry_argent_banque.get())
        solde_total = argent_banque + valeur_stock
        solde_total = soustraire_depenses(solde_total)
        messagebox.showinfo("Solde Total", f"Solde total : {solde_total} €")
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Gestion de Finances")

# Création des libellés et des champs de saisie pour afficher le solde de compte bancaire et les transactions récentes
bouton_afficher_transactions = tk.Button(fenetre, text="Afficher Transactions Récentes", command=afficher_transactions)
bouton_afficher_transactions.grid(row=0, columnspan=2, padx=10, pady=5)

# Création des libellés et des champs de saisie pour saisir manuellement les dépenses en espèces
label_date = tk.Label(fenetre, text="Date de la dépense (jjmmaaaa) :")
label_date.grid(row=1, column=0, padx=10, pady=5)

entry_date = tk.Entry(fenetre)
entry_date.grid(row=1, column=1, padx=10, pady=5)
entry_date.bind("<KeyRelease>", formater_date)

label_description = tk.Label(fenetre, text="Description de la dépense :")
label_description.grid(row=2, column=0, padx=10, pady=5)
entry_description = tk.Entry(fenetre)
entry_description.grid(row=2, column=1, padx=10, pady=5)

label_depense = tk.Label(fenetre, text="Montant de la dépense (€) :")
label_depense.grid(row=3, column=0, padx=10, pady=5)
entry_depense = tk.Entry(fenetre)
entry_depense.grid(row=3, column=1, padx=10, pady=5)

# Ajouter un widget calendrier pour sélectionner la date de dépense
label_calendrier = tk.Label(fenetre, text="Ou sélectionnez une date :")
label_calendrier.grid(row=4, column=0, padx=10, pady=5)
calendrier = DateEntry(fenetre, date_pattern='dd/mm/yyyy')
calendrier.grid(row=4, column=1, padx=10, pady=5)

# Bouton pour saisir la dépense
def ajouter_depense_via_calendrier():
    global donnees
    date_depense = calendrier.get_date().strftime('%d/%m/%Y')
    description_depense = entry_description.get()
    montant_depense = entry_depense.get()

    if not valider_montant(montant_depense):
        messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")
        return

    montant_depense = -float(montant_depense)  # Modification pour soustraire le montant
    donnees.append({'date': date_depense, 'description': description_depense, 'montant': montant_depense})  # Modification pour soustraire le montant
    sauvegarder_donnees('transactions.csv', donnees)
    messagebox.showinfo("Dépense ajoutée", "Dépense ajoutée avec succès.")

bouton_saisir_depense = tk.Button(fenetre, text="Saisir Dépense", command=saisir_depenses)
bouton_saisir_depense.grid(row=5, columnspan=2, padx=10, pady=5)

bouton_saisir_depense_calendrier = tk.Button(fenetre, text="Ajouter Dépense via Calendrier", command=ajouter_depense_via_calendrier)
bouton_saisir_depense_calendrier.grid(row=6, columnspan=2, padx=10, pady=5)

# Création des libellés et des champs de saisie pour gérer les stocks
bouton_calculer_valeur_stock = tk.Button(fenetre, text="Calculer Valeur Stock", command=calculer_valeur_stock)
bouton_calculer_valeur_stock.grid(row=7, columnspan=2, padx=10, pady=5)

# Création des libellés et des champs de saisie pour afficher le solde total
label_argent_banque = tk.Label(fenetre, text="Argent en Banque (€) :")
label_argent_banque.grid(row=8, column=0, padx=10, pady=5)
entry_argent_banque = tk.Entry(fenetre)
entry_argent_banque.grid(row=8, column=1, padx=10, pady=5)

bouton_afficher_solde_total = tk.Button(fenetre, text="Afficher Solde Total", command=afficher_solde_total)
bouton_afficher_solde_total.grid(row=9, columnspan=2, padx=10, pady=5)

# Création des boutons pour afficher les dépenses
bouton_afficher_depenses = tk.Button(fenetre, text="Afficher Dépenses", command=afficher_depenses)
bouton_afficher_depenses.grid(row=10, columnspan=2, padx=10, pady=5)

# Données
donnees = charger_donnees('transactions.csv')

# Lancement de la boucle principale
fenetre.mainloop()

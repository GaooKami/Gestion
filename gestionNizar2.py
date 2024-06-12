import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

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

# Fonction pour saisir manuellement les dépenses en espèces
def saisir_depenses():
    global donnees
    try:
        montant_depense = float(entry_depense.get())
        description_depense = entry_description.get()
        date_depense = entry_date.get()
        donnees.append({'date': date_depense, 'description': description_depense, 'montant': -montant_depense})
        sauvegarder_donnees('transactions.csv', donnees)
        messagebox.showinfo("Dépense ajoutée", "Dépense ajoutée avec succès.")
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")

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
    solde_total -= total_depenses
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
label_date = tk.Label(fenetre, text="Date de la dépense :")
label_date.grid(row=1, column=0, padx=10, pady=5)
entry_date = tk.Entry(fenetre)
entry_date.grid(row=1, column=1, padx=10, pady=5)

label_description = tk.Label(fenetre, text="Description de la dépense :")
label_description.grid(row=2, column=0, padx=10, pady=5)
entry_description = tk.Entry(fenetre)
entry_description.grid(row=2, column=1, padx=10, pady=5)

label_depense = tk.Label(fenetre, text="Montant de la dépense :")
label_depense.grid(row=3, column=0, padx=10, pady=5)
entry_depense = tk.Entry(fenetre)
entry_depense.grid(row=3, column=1, padx=10, pady=5)

bouton_saisir_depense = tk.Button(fenetre, text="Saisir Dépense", command=saisir_depenses)
bouton_saisir_depense.grid(row=4, columnspan=2, padx=10, pady=5)

# Création des libellés et des champs de saisie pour gérer les stocks
bouton_calculer_valeur_stock = tk.Button(fenetre, text="Calculer Valeur Stock", command=calculer_valeur_stock)
bouton_calculer_valeur_stock.grid(row=5, columnspan=2, padx=10, pady=5)

# Création des libellés et des champs de saisie pour afficher le solde total
label_argent_banque = tk.Label(fenetre, text="Argent en Banque (€) :")
label_argent_banque.grid(row=6, column=0, padx=10, pady=5)
entry_argent_banque = tk.Entry(fenetre)
entry_argent_banque.grid(row=6, column=1, padx=10, pady=5)

bouton_afficher_solde_total = tk.Button(fenetre, text="Afficher Solde Total", command=afficher_solde_total)
bouton_afficher_solde_total.grid(row=7, columnspan=2, padx=10, pady=5)

# Création des boutons pour afficher les dépenses
bouton_afficher_depenses = tk.Button(fenetre, text="Afficher Dépenses", command=afficher_depenses)
bouton_afficher_depenses.grid(row=8, columnspan=2, padx=10, pady=5)

# Données
donnees = charger_donnees('transactions.csv')

# Lancement de la boucle principale
fenetre.mainloop()

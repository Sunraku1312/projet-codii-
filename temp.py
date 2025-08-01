import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import math

def calculer():
    try:
        jour = int(entry_jour.get())
        mois = int(entry_mois.get())
        annee = int(entry_annee.get())

        date_naissance = datetime(annee, mois, jour)
        aujourd_hui = datetime.now()
        difference = aujourd_hui - date_naissance
        jours = difference.days
        mois_vie = jours // 30
        annees_vie = jours // 365
        semaines_vie = jours // 7
        heures_vie = jours * 24
        minutes_vie = heures_vie * 60

        battements_coeur = jours * 86400 * 70 / 60 / 60
        clignements_yeux = jours * 86400 * 22
        sommeil = jours * 86400 * 0.33
        naissance_humains = jours * 86400 * 0.003
        distance_terre_soleil = jours * 940000000
        age_biologique = annees_vie / 2  # Estimation très approximative

        resultats = f"Jours depuis votre naissance: {jours}\n" \
                    f"Années depuis votre naissance: {annees_vie}\n" \
                    f"Mois depuis votre naissance: {mois_vie}\n" \
                    f"Semaine depuis votre naissance: {semaines_vie}\n" \
                    f"Heures de vie totales: {heures_vie}\n" \
                    f"Minutes de vie totales: {minutes_vie}\n" \
                    f"Battements de cœur approximatifs: {int(battements_coeur)}\n" \
                    f"Clignements d'yeux approximatifs: {int(clignements_yeux)}\n" \
                    f"Sommeil approximatif (en heures): {int(sommeil / 3600)}\n" \
                    f"Humains nés depuis votre naissance: {int(naissance_humains)}\n" \
                    f"Distance parcourue par la Terre autour du Soleil (en km): {int(distance_terre_soleil)}\n" \
                    f"Age biologique estimé (en années): {age_biologique}\n"

        resultats += f"Calories brûlées approximativement (au repos, en kcal): {int(jours * 1800)}\n" \
                     f"Nombre de pas approximatif (en moyenne 7000 pas/jour): {int(jours * 7000)}\n" \
                     f"Nombre de respirations approximatives (en moyenne 16 respirations/minute): {int(jours * 86400 * 16)}\n" \
                     f"Nombre de sourires approximatifs (1 sourire toutes les 10 minutes): {int(jours * 8640)}\n" \
                     f"Calories consommées (en moyenne 2500 kcal/jour): {int(jours * 2500)}\n" \
                     f"Nombre de repas pris (3 repas par jour en moyenne): {int(jours * 3)}\n" \
                     f"Nombre de fois que vous avez ri (en moyenne 15 rires par jour): {int(jours * 15)}\n" \
                     f"Nombre de fois que vous avez mangé de la nourriture sucrée (en moyenne 2 fois/jour): {int(jours * 2)}\n" \
                     f"Nombre de cheveux perdus (en moyenne 50 cheveux par jour): {int(jours * 50)}\n" \
                     f"Nombre de fois où vous avez cligné des yeux (en moyenne 22 clignements/minute): {int(jours * 86400 * 22)}\n" \
                     f"Nombre de litres d'eau consommés (en moyenne 2 litres/jour): {int(jours * 2)}\n" \
                     f"Nombre de fois que vous avez marché (en moyenne 5000 pas/jour): {int(jours * 5000)}\n" \
                     f"Nombre de fois que vous avez bu du café (en moyenne 1 tasse/jour): {int(jours)}\n" \
                     f"Nombre de fois que vous avez fait du sport (en moyenne 3 fois/semaine): {int(jours // 7 * 3)}\n" \
                     f"Nombre de fois où vous avez regardé un film (en moyenne 1 film par semaine): {int(jours // 7)}\n" \
                     f"Nombre de livres lus (en moyenne 1 livre par mois): {int(jours // 30)}\n" \
                     f"Nombre de fois où vous avez visité un nouveau lieu (en moyenne 1 fois par an): {int(annees_vie)}\n" \
                     f"Nombre de fois où vous avez fait un voyage en avion (en moyenne 1 voyage tous les 2 ans): {int(annees_vie / 2)}\n" \
                     f"Nombre de fois où vous avez mangé au restaurant (en moyenne 1 fois par semaine): {int(jours // 7)}\n" \
                     f"Nombre de fois où vous avez consulté un médecin (en moyenne 1 fois par an): {int(annees_vie)}\n" \
                     f"Nombre de films regardés (en moyenne 3 films par mois): {int(jours // 10)}"

        messagebox.showinfo("Résultats", resultats)
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer une date valide.")

root = tk.Tk()
root.title("Calculs de votre vie")

label_jour = tk.Label(root, text="Jour :")
label_jour.pack(pady=5)
entry_jour = tk.Entry(root)
entry_jour.pack(pady=5)

label_mois = tk.Label(root, text="Mois :")
label_mois.pack(pady=5)
entry_mois = tk.Entry(root)
entry_mois.pack(pady=5)

label_annee = tk.Label(root, text="Année :")
label_annee.pack(pady=5)
entry_annee = tk.Entry(root)
entry_annee.pack(pady=5)

button_calculer = tk.Button(root, text="Calculer", command=calculer)
button_calculer.pack(pady=20)

root.mainloop()

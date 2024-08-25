from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        revenu_felix = round(float(request.form['revenu_felix']), 2)
        revenu_myriam = round(float(request.form['revenu_myriam']), 2)
        compte_epargne_initial = round(float(request.form['compte_epargne_initial']), 2)
        compte_commun = round(float(request.form['compte_commun']), 2)

        # Calculs
        somme_depart = round(revenu_felix + revenu_myriam + compte_commun, 2)
        depenses_communes = round(float(request.form['depenses_communes']), 2)
        depenses_perso_felix = round(float(request.form['depenses_perso_felix']), 2)
        depenses_perso_myriam = round(float(request.form['depenses_perso_myriam']), 2)

        transactions = []
        contribution_totale = 0
        contribution_epargne = 0
        compte_epargne = compte_epargne_initial
        contribution_compte_commun = round(min(compte_commun, depenses_communes), 2)

        contribution_totale += contribution_compte_commun
        manque = round(depenses_communes - contribution_totale, 2)

        total_fonds_disponibles = round(revenu_felix + revenu_myriam, 2)
        part_felix = part_myriam = 0

        if total_fonds_disponibles > 0:
            part_felix = round(min(revenu_felix, manque * (revenu_felix / total_fonds_disponibles)), 2)
            part_myriam = round(min(revenu_myriam, manque * (revenu_myriam / total_fonds_disponibles)), 2)

        if part_felix > 0:
            transactions.append(f"Félix doit transférer {part_felix:.2f} EUR au compte commun.")
            revenu_felix = round(revenu_felix - part_felix, 2)
            contribution_totale += part_felix

        if part_myriam > 0:
            transactions.append(f"Myriam doit transférer {part_myriam:.2f} EUR au compte commun.")
            revenu_myriam = round(revenu_myriam - part_myriam, 2)
            contribution_totale += part_myriam

        manque = round(depenses_communes - contribution_totale, 2)

        if manque > 0:
            if compte_epargne >= manque:
                transactions.append(f"Transférer {manque:.2f} EUR du compte d'épargne au compte commun pour couvrir les dépenses communes.")
                compte_epargne = round(compte_epargne - manque, 2)
                contribution_epargne += manque
                contribution_totale += manque
            else:
                transactions.append(f"Transférer {compte_epargne:.2f} EUR du compte d'épargne au compte commun (fonds insuffisants pour couvrir toutes les dépenses communes).")
                contribution_epargne += compte_epargne
                contribution_totale += compte_epargne
                compte_epargne = 0

        revenu_felix = round(max(revenu_felix, 0), 2)
        revenu_myriam = round(max(revenu_myriam, 0), 2)

        total_revenu = round(revenu_felix + revenu_myriam, 2)
        total_fonds_disponibles = round(revenu_felix + revenu_myriam, 2)
        total_depenses_perso = depenses_perso_felix + depenses_perso_myriam

        if total_depenses_perso > 0:
            pourcentage_satisfaction_total = round(min(total_fonds_disponibles / total_depenses_perso, 1), 2)
        else:
            pourcentage_satisfaction_total = 0

        satisfaction_felix = round(pourcentage_satisfaction_total * depenses_perso_felix, 2)
        satisfaction_myriam = round(pourcentage_satisfaction_total * depenses_perso_myriam, 2)

        manque_felix = round(satisfaction_felix - revenu_felix, 2)
        manque_myriam = round(satisfaction_myriam - revenu_myriam, 2)

        if manque_felix > 0:
            transactions.append(f"Myriam doit transférer {manque_felix:.2f} EUR à Félix pour équilibrer les dépenses personnelles.")
            revenu_myriam = round(revenu_myriam - manque_felix, 2)
            revenu_felix = round(revenu_felix + manque_felix, 2)
        elif manque_myriam > 0:
            transactions.append(f"Félix doit transférer {manque_myriam:.2f} EUR à Myriam pour équilibrer les dépenses personnelles.")
            revenu_felix = round(revenu_felix - manque_myriam, 2)
            revenu_myriam = round(revenu_myriam + manque_myriam, 2)

        revenu_felix = round(revenu_felix - satisfaction_felix, 2)
        revenu_myriam = round(revenu_myriam - satisfaction_myriam, 2)

        # Utiliser pourcentage_satisfaction_total pour calculer les pourcentages individuels
        pourcentage_satisfaction_felix = round(pourcentage_satisfaction_total * 100, 2)
        pourcentage_satisfaction_myriam = round(pourcentage_satisfaction_total * 100, 2)

        excedent_felix = round(max(revenu_felix, 0), 2)
        excedent_myriam = round(max(revenu_myriam, 0), 2)

        total_epargne_ce_mois = 0

        if excedent_felix > 0:
            transactions.append(f"Félix doit transférer {excedent_felix:.2f} EUR au compte d'épargne.")
            compte_epargne = round(compte_epargne + excedent_felix, 2)
            total_epargne_ce_mois += excedent_felix

        if excedent_myriam > 0:
            transactions.append(f"Myriam doit transférer {excedent_myriam:.2f} EUR au compte d'épargne.")
            compte_epargne = round(compte_epargne + excedent_myriam, 2)
            total_epargne_ce_mois += excedent_myriam

        pourcentage_epargne_ce_mois = round((total_epargne_ce_mois / somme_depart) * 100, 2) if somme_depart > 0 else 0
        progression_epargne = round(((compte_epargne - compte_epargne_initial) / compte_epargne_initial) * 100, 2) if compte_epargne_initial > 0 else 0

        pourcentage_contribution_felix = round((part_felix / depenses_communes) * 100, 2) if depenses_communes > 0 else 0
        pourcentage_contribution_myriam = round((part_myriam / depenses_communes) * 100, 2) if depenses_communes > 0 else 0
        pourcentage_contribution_epargne = round((contribution_epargne / depenses_communes) * 100, 2) if depenses_communes > 0 else 0
        pourcentage_contribution_compte_commun = round((contribution_compte_commun / depenses_communes) * 100, 2) if depenses_communes > 0 else 0

        return render_template('index.html', 
                               transactions=transactions, 
                               somme_depart=somme_depart, 
                               contribution_compte_commun=contribution_compte_commun, 
                               pourcentage_contribution_compte_commun=pourcentage_contribution_compte_commun, 
                               part_felix=part_felix, 
                               pourcentage_contribution_felix=pourcentage_contribution_felix, 
                               part_myriam=part_myriam, 
                               pourcentage_contribution_myriam=pourcentage_contribution_myriam, 
                               contribution_epargne=contribution_epargne, 
                               pourcentage_contribution_epargne=pourcentage_contribution_epargne, 
                               satisfaction_felix=satisfaction_felix, 
                               depenses_perso_felix=depenses_perso_felix, 
                               pourcentage_satisfaction_felix=pourcentage_satisfaction_felix, 
                               satisfaction_myriam=satisfaction_myriam, 
                               depenses_perso_myriam=depenses_perso_myriam, 
                               pourcentage_satisfaction_myriam=pourcentage_satisfaction_myriam, 
                               total_epargne_ce_mois=total_epargne_ce_mois, 
                               pourcentage_epargne_ce_mois=pourcentage_epargne_ce_mois, 
                               compte_epargne_initial=compte_epargne_initial, 
                               compte_epargne=compte_epargne, 
                               progression_epargne=progression_epargne)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

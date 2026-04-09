import tkinter as tk
from tkinter import messagebox
import database # On importe ton fichier database.py

def ouvrir_page_principale(pseudo, id_user):
    for widget in root.winfo_children():
        widget.destroy()
        
    root.geometry("1200x750")

    # --- HEADER ---
    header_container = tk.Frame(root, pady=10)
    header_container.pack(fill="x", padx=20)

    top_row = tk.Frame(header_container)
    top_row.pack(fill="x")

    tk.Label(top_row, text="BOOKSHARE", font=("Helvetica", 24, "bold")).pack(side="left")

    # Frame à droite pour Profil et Déconnexion
    right_actions = tk.Frame(top_row)
    right_actions.pack(side="right")

    sub_row_top = tk.Frame(right_actions)
    sub_row_top.pack(fill="x")
    
    tk.Button(sub_row_top, text=f"👤 {pseudo}", command=lambda: ouvrir_profil(pseudo), 
              relief="flat", font=("Arial", 9, "bold")).pack(side="left", padx=5)
    
    tk.Button(sub_row_top, text="🚪 Déconnexion", command=creer_interface_connexion, 
              fg="red", relief="flat", font=("Arial", 9)).pack(side="left")

    # Ligne du bas : Emprunter et Ajouter
    sub_row_bottom = tk.Frame(right_actions)
    sub_row_bottom.pack(pady=5)
    
    tk.Button(sub_row_bottom, text="🤝 Emprunter", bg="#3498db", fg="white", width=12,
              command=lambda: ouvrir_page_emprunt(id_user, pseudo)).pack(side="left", padx=2)
              
    tk.Button(sub_row_bottom, text="➕ Ajouter", bg="#27ae60", fg="white", width=12,
              command=lambda: ouvrir_formulaire_livre(id_user, pseudo)).pack(side="left", padx=2)

    # Ligne 2 : Barre de recherche (Attention : header_container ici !)
    search_row = tk.Frame(header_container, pady=15)
    search_row.pack()
    ent_search = tk.Entry(search_row, width=50)
    ent_search.pack(side="left", padx=5)
    tk.Button(search_row, text="🔍", command=lambda: afficher_resultats_recherche(ent_search.get(), pseudo, id_user)).pack(side="left")

    # --- CONTENEUR DES COLONNES ---
    main_container = tk.Frame(root)
    main_container.pack(fill="both", expand=True, padx=20)

    # 1. COLONNE GAUCHE : Top 5 Livres
    col_gauche = tk.LabelFrame(main_container, text="🏆 Top 5 Livres", padx=10, pady=10)
    col_gauche.pack(side="left", fill="both", expand=True, padx=10)
    
    top_livres = database.recuperer_top_livres() # On récupère les données
    for livre in top_livres:
        moyenne = float(livre['moyenne'])
        tk.Label(col_gauche, text=f"⭐ {moyenne:.1f} - {livre['titre']}", 
                 anchor="w", font=("Arial", 10)).pack(fill="x", pady=2)

    # 2. COLONNE CENTRE : Derniers Avis
    col_centre = tk.LabelFrame(main_container, text="💬 Derniers Avis", padx=10, pady=10)
    col_centre.pack(side="left", fill="both", expand=True, padx=10)

    col_centre.columnconfigure(0, weight=1)
    col_centre.columnconfigure(1, weight=2)
    col_centre.columnconfigure(2, weight=1)

    tk.Label(col_centre, text="Utilisateur / Livre", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="nsew")
    tk.Label(col_centre, text="Avis", font=("Arial", 9, "bold")).grid(row=0, column=1, sticky="nsew")
    tk.Label(col_centre, text="Note", font=("Arial", 9, "bold")).grid(row=0, column=2, sticky="nsew")

    avis_data = database.recuperer_derniers_avis_complets()
    for i, a in enumerate(avis_data):
        tk.Label(col_centre, text=f"{a['pseudo']}\nsur {a['titre']}", fg="blue", anchor="w", justify="left", font=("Arial", 8)).grid(row=i+1, column=0, sticky="nsew", pady=5)
        tk.Label(col_centre, text=a['commentaire'], wraplength=180, anchor="w", justify="left", font=("Arial", 8)).grid(row=i+1, column=1, sticky="nsew")
        tk.Label(col_centre, text="★" * int(a['note']), fg="orange").grid(row=i+1, column=2, sticky="nsew")

    # 3. COLONNE DROITE : Mes Emprunts
    col_droite = tk.LabelFrame(main_container, text="📑 Mes Emprunts", padx=10, pady=10)
    col_droite.pack(side="left", fill="both", expand=True, padx=10)

    emprunts = database.recuperer_emprunts_utilisateur(id_user)
    if not emprunts:
        tk.Label(col_droite, text="Aucun emprunt en cours.", fg="gray", font=("Arial", 9, "italic")).pack(pady=30)
    else:
        for emp in emprunts:
            date_txt = emp['date_fin'].strftime("%d/%m/%Y") if emp['date_fin'] else "??"
            cadre_emp = tk.Frame(col_droite, pady=5)
            cadre_emp.pack(fill="x")
            tk.Label(cadre_emp, text=f"• {emp['titre']}", font=("Arial", 9, "bold"), anchor="w").pack(fill="x")
            tk.Label(cadre_emp, text=f"  Echéance : {date_txt}", fg="#e67e22", font=("Arial", 8)).pack(fill="x")

    tk.Button(col_droite, text="Voir bibliothèque", command=lambda: voir_bibliotheque(pseudo, id_user),
              bg="#3498db", fg="white").pack(side="bottom", fill="x", pady=5)


def ouvrir_profil(pseudo):
    messagebox.showinfo("Profil", f"Affichage du profil de {pseudo} (en cours de construction)")

def retour_inscription():
    # Fonction simple pour relancer l'interface d'inscription
    for widget in root.winfo_children():
        widget.destroy()
    creer_interface_inscription()

def valider_inscription():
    # On récupère les textes des Entry globales
    pseudo = entry_pseudo.get()
    mdp = entry_mdp.get()
    
    if pseudo == "" or mdp == "":
        messagebox.showwarning("Erreur", "Tous les champs sont obligatoires")
        return

    # Utilisation de la fonction inscrire_utilisateur présente dans ton database.py
    succes, msg = database.inscrire_utilisateur(pseudo, mdp)
    
    if succes:
        messagebox.showinfo("Succès", msg)
        creer_interface_connexion() # On redirige vers la connexion
    else:
        messagebox.showerror("Erreur", msg)

def creer_interface_inscription():
    for widget in root.winfo_children():
        widget.destroy()
        
    root.title("Inscription - BookShare")
    root.geometry("300x300")
    
    # On définit les variables en global pour que valider_inscription les voit
    global entry_pseudo, entry_mdp
    
    tk.Label(root, text="INSCRIPTION", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(root, text="Pseudo").pack()
    entry_pseudo = tk.Entry(root)
    entry_pseudo.pack(pady=5)

    tk.Label(root, text="Mot de passe").pack()
    entry_mdp = tk.Entry(root, show="*")
    entry_mdp.pack(pady=5)

    # Note : Pas de parenthèses après valider_inscription ici
    tk.Button(root, text="Créer mon compte", command=valider_inscription, 
              bg="#2196F3", fg="white").pack(pady=10)
    
    tk.Button(root, text="Déjà inscrit ? Se connecter", borderwidth=0, 
              fg="blue", command=creer_interface_connexion).pack()

def valider_connexion():
    pseudo = entry_pseudo.get()
    mdp = entry_mdp.get()

    succes, resultat = database.connecter_utilisateur(pseudo, mdp)
    
    if succes:
        # resultat est le dictionnaire renvoyé par fetchone()
        user_id = resultat['id_user'] # On récupère l'ID de la table
        messagebox.showinfo("Succès", f"Ravi de vous revoir {pseudo} !")
        ouvrir_page_principale(pseudo, user_id) # On passe l'ID à la page d'accueil
    else:
        messagebox.showerror("Erreur", resultat)

def creer_interface_connexion():
    for widget in root.winfo_children():
        widget.destroy()
        
    root.title("Connexion - BookShare")
    root.geometry("300x300")
    
    global entry_pseudo, entry_mdp
    
    tk.Label(root, text="CONNEXION", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(root, text="Pseudo").pack()
    entry_pseudo = tk.Entry(root)
    entry_pseudo.pack(pady=5)

    tk.Label(root, text="Mot de passe").pack()
    entry_mdp = tk.Entry(root, show="*")
    entry_mdp.pack(pady=5)

    tk.Button(root, text="Se connecter", command=valider_connexion, bg="#4CAF50", fg="white").pack(pady=10)
    
    # Lien pour aller vers l'inscription si on n'a pas de compte
    tk.Button(root, text="Pas encore de compte ? S'inscrire", borderwidth=0, fg="blue", command=creer_interface_inscription).pack()

def creer_interface_inscription():
    for widget in root.winfo_children():
        widget.destroy()
        
    root.title("Inscription - BookShare")
    root.geometry("300x300")
    
    global entry_pseudo, entry_mdp
    
    tk.Label(root, text="INSCRIPTION", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(root, text="Pseudo").pack()
    entry_pseudo = tk.Entry(root)
    entry_pseudo.pack(pady=5)

    tk.Label(root, text="Mot de passe").pack()
    entry_mdp = tk.Entry(root, show="*")
    entry_mdp.pack(pady=5)

    tk.Button(root, text="Creer mon compte", command=valider_inscription, bg="#2196F3", fg="white").pack(pady=10)
    
    tk.Button(root, text="Deja inscrit ? Se connecter", borderwidth=0, fg="blue", command=creer_interface_connexion).pack()


def ouvrir_formulaire_livre(id_user, pseudo_user):
    for widget in root.winfo_children():
        widget.destroy()

    # Barre de navigation haute pour le retour
    nav_frame = tk.Frame(root)
    nav_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Button(nav_frame, text="< Retour à l'accueil", 
              command=lambda: ouvrir_page_principale(pseudo_user, id_user),
              relief="flat", fg="blue").pack(side="left")

    tk.Label(root, text="AJOUTER UN LIVRE", font=("Helvetica", 18, "bold")).pack(pady=10)
    
    # ... (Le reste du formulaire reste le même que précédemment)

    # Formulaire
    container = tk.Frame(root)
    container.pack(pady=10)

    tk.Label(container, text="Titre :").grid(row=0, column=0, sticky="e", pady=5)
    ent_titre = tk.Entry(container, width=30)
    ent_titre.grid(row=0, column=1, pady=5)

    tk.Label(container, text="Auteur :").grid(row=1, column=0, sticky="e", pady=5)
    ent_auteur = tk.Entry(container, width=30)
    ent_auteur.grid(row=1, column=1, pady=5)

    tk.Label(container, text="Date (AAAA-MM-DD) :").grid(row=2, column=0, sticky="e", pady=5)
    ent_date = tk.Entry(container, width=30)
    ent_date.grid(row=2, column=1, pady=5)

    tk.Label(container, text="Note (1 a 5) :").grid(row=3, column=0, sticky="e", pady=5)
    spin_note = tk.Spinbox(container, from_=1, to=5, width=5)
    spin_note.grid(row=3, column=1, sticky="w", pady=5)

    tk.Label(container, text="Avis :").grid(row=4, column=0, sticky="ne", pady=5)
    txt_avis = tk.Text(container, width=30, height=5)
    txt_avis.grid(row=4, column=1, pady=5)

    def sauvegarder():
        titre = ent_titre.get()
        auteur = ent_auteur.get()
        date = ent_date.get()
        note = spin_note.get()
        avis = txt_avis.get("1.0", "end-1c") # Recupere tout le texte

        if not titre or not auteur:
            messagebox.showwarning("Attention", "Le titre et l'auteur sont obligatoires.")
            return

        succes, msg = database.ajouter_livre_avec_avis(id_user, titre, auteur, date, note, avis)
        if succes:
            messagebox.showinfo("Succès", msg)
            # IL FAUT PASSER id_user ICI AUSSI
            ouvrir_page_principale(pseudo_user, id_user) 
        else:
            messagebox.showerror("Erreur", msg)

    tk.Button(root, text="Enregistrer le livre", bg="#27ae60", fg="white", 
              command=sauvegarder, pady=10).pack(pady=20)
    
    tk.Button(root, text="Annuler", command=lambda: ouvrir_page_principale(pseudo_user)).pack()

def voir_bibliotheque(pseudo_user, id_user):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Button(root, text="< Retour", command=lambda: ouvrir_page_principale(pseudo_user, id_user)).pack(anchor="w", padx=10)
    tk.Label(root, text="BIBLIOTHÈQUE COMPLÈTE", font=("Arial", 16, "bold")).pack(pady=10)

    # Conteneur pour la liste
    liste_frame = tk.Frame(root)
    liste_frame.pack(fill="both", expand=True, padx=20)

    tous_les_livres = database.recuperer_tous_les_livres()

    for livre in tous_les_livres:
        cadre_livre = tk.Frame(liste_frame, pady=5, bd=1, relief="groove")
        cadre_livre.pack(fill="x", pady=2)

        # Affichage des infos à gauche
        info_txt = f"📖 {livre['titre']} - {livre['auteur']}"
        tk.Label(cadre_livre, text=info_txt, font=("Arial", 10)).pack(side="left", padx=10)

        # CONDITION : Si l'ID du proprio en base == ID de l'utilisateur actuel
        if livre['id_proprietaire'] == id_user:
            tk.Button(cadre_livre, text="📝 Modifier", bg="#f1c40f", fg="black",
                      command=lambda l=livre: ouvrir_formulaire_edition(l, id_user, pseudo_user)).pack(side="right", padx=10)
        else:
            # Petit indicateur visuel pour les livres des autres
            tk.Label(cadre_livre, text="(Lecture seule)", fg="gray", font=("Arial", 8)).pack(side="right", padx=10)


def afficher_resultats_recherche(terme, pseudo_user, id_user):
    for widget in root.winfo_children():
        widget.destroy()
    
    root.title(f"Résultats pour '{terme}'")
    
    tk.Button(root, text="< Retour", command=lambda: ouvrir_page_principale(pseudo_user, id_user)).pack(anchor="w", padx=10)
    
    tk.Label(root, text=f"Résultats de recherche pour : {terme}", font=("Arial", 14, "bold")).pack(pady=20)
    
    resultats = database.rechercher_livres(terme)
    
    container = tk.Frame(root)
    container.pack(fill="x", padx=50)

    if not resultats:
        tk.Label(container, text="Aucun livre trouvé.", fg="red").pack()
    else:
        for livre in resultats:
            note = f"{livre['moyenne']:.1f}/5" if livre['moyenne'] else "N/A"
            cadre = tk.Frame(container, bd=1, relief="groove", pady=10, padx=10)
            cadre.pack(pady=5, fill="x")
            tk.Label(cadre, text=f"📖 {livre['titre']} - {livre['auteur']}", font=("Arial", 11, "bold")).pack(side="left")
            tk.Label(cadre, text=f" ⭐ {note} | Ajouté par {livre['pseudo']}", fg="gray").pack(side="right")

def ouvrir_page_emprunt(id_user, pseudo_user):
    for widget in root.winfo_children():
        widget.destroy()
    
    # --- HEADER ---
    header = tk.Frame(root, bg="#f8f9fa", pady=10)
    header.pack(fill="x")
    tk.Button(header, text="← Retour", command=lambda: ouvrir_page_principale(pseudo_user, id_user), 
              bg="#6c757d", fg="white", relief="flat").pack(side="left", padx=20)
    tk.Label(header, text="Catalogue de prêt", font=("Helvetica", 18, "bold"), bg="#f8f9fa").pack(side="left", padx=20)

    # --- RECHERCHE ---
    search_frame = tk.Frame(root, pady=20)
    search_frame.pack()
    ent_search = tk.Entry(search_row := tk.Frame(search_frame), width=40, font=("Arial", 12))
    ent_search.pack(side="left", padx=5)
    
    # --- ZONE DE LISTE (Tableau) ---
    table_container = tk.Frame(root, bd=1, relief="solid")
    table_container.pack(fill="both", expand=True, padx=50, pady=10)

    # En-tête du tableau
    thead = tk.Frame(table_container, bg="#34495e")
    thead.pack(fill="x")
    tk.Label(thead, text="Titre du livre", fg="white", bg="#34495e", width=40, anchor="w", padx=10).pack(side="left")
    tk.Label(thead, text="Auteur", fg="white", bg="#34495e", width=25, anchor="w").pack(side="left")
    tk.Label(thead, text="Action", fg="white", bg="#34495e", width=15).pack(side="right")

    # Zone défilante
    canvas = tk.Canvas(table_container)
    scrollbar = tk.Scrollbar(table_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Variable pour stocker le livre choisi
    var_livre_selectionne = tk.StringVar()
    lbl_confirmation = tk.Label(root, text="Aucun livre sélectionné", font=("Arial", 10, "italic"), fg="gray")

    def selectionner(id_l, titre):
        var_livre_selectionne.set(id_l)
        lbl_confirmation.config(text=f"Prêt choisi : {titre}", fg="#27ae60", font=("Arial", 10, "bold"))

    def actualiser():
        for w in scrollable_frame.winfo_children():
            w.destroy()
        
        livres = database.rechercher_livres_disponibles(ent_search.get())
        for i, l in enumerate(livres):
            bg_color = "#ffffff" if i % 2 == 0 else "#f2f2f2"
            row = tk.Frame(scrollable_frame, bg=bg_color, pady=5)
            row.pack(fill="x")
            
            tk.Label(row, text=l['titre'], bg=bg_color, width=45, anchor="w", padx=10).pack(side="left")
            tk.Label(row, text=l['auteur'], bg=bg_color, width=30, anchor="w").pack(side="left")
            tk.Button(row, text="Choisir", command=lambda id_l=l['id_livre'], t=l['titre']: selectionner(id_l, t),
                      bg="#ecf0f1", relief="groove", font=("Arial", 8)).pack(side="right", padx=10)

    # Liaison recherche automatique
    ent_search.bind("<KeyRelease>", lambda e: actualiser())
    actualiser()

    # --- FOOTER (DURÉE ET VALIDATION) ---
    footer = tk.Frame(root, pady=20)
    footer.pack(fill="x")
    
    lbl_confirmation.pack()
    
    tk.Label(footer, text="Durée du prêt (jours) :").pack(side="left", padx=(100, 5))
    spin_jours = tk.Spinbox(footer, from_=1, to=90, width=5)
    spin_jours.pack(side="left")

    def valider():
        if not var_livre_selectionne.get():
            messagebox.showwarning("Attention", "Veuillez choisir un livre dans la liste.")
            return
        
        succes, msg = database.enregistrer_emprunt(id_user, var_livre_selectionne.get(), spin_jours.get())
        if succes:
            messagebox.showinfo("Succès", msg)
            ouvrir_page_principale(pseudo_user, id_user)
        else:
            messagebox.showerror("Erreur", msg)

    tk.Button(footer, text="Confirmer l'emprunt", bg="#2ecc71", fg="white", font=("Arial", 11, "bold"),
              padx=20, command=valider).pack(side="right", padx=100)
def ouvrir_formulaire_edition(livre, id_user, pseudo_user):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Modifier : {livre['titre']}", font=("Arial", 14, "bold")).pack(pady=20)

    # Champs pré-remplis
    tk.Label(root, text="Titre").pack()
    ent_titre = tk.Entry(root)
    ent_titre.insert(0, livre['titre'])
    ent_titre.pack()

    tk.Label(root, text="Auteur").pack()
    ent_auteur = tk.Entry(root)
    ent_auteur.insert(0, livre['auteur'])
    ent_auteur.pack()

    def sauvegarder_modif():
        # Appel à une fonction SQL que nous allons créer
        succes = database.modifier_livre(livre['id_livre'], ent_titre.get(), ent_auteur.get())
        if succes:
            messagebox.showinfo("Succès", "Livre mis à jour !")
            ouvrir_page_principale(pseudo_user, id_user)
        else:
            messagebox.showerror("Erreur", "La modification a échoué.")

    tk.Button(root, text="Enregistrer les modifications", bg="#f1c40f", command=sauvegarder_modif).pack(pady=20)
    tk.Button(root, text="Annuler", command=lambda: voir_bibliotheque(pseudo_user, id_user)).pack()




root = tk.Tk()
creer_interface_inscription()
root.mainloop()
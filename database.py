import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Erreur de connexion : {e}")
        return None

def ajouter_utilisateur(pseudo, mot_de_passe):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO Utilisateur (pseudo, mot_de_passe) VALUES (%s, %s)"
        try:
            cursor.execute(query, (pseudo, mot_de_passe))
            conn.commit()
            print("Utilisateur ajoute avec succes !")
        except Error as e:
            print(f"Erreur: {e}")
        finally:
            conn.close()

def rechercher_livres(critere):
    conn = create_connection()
    resultats = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Livre WHERE titre LIKE %s OR auteur LIKE %s"
        search_val = f"%{critere}%"
        cursor.execute(query, (search_val, search_val))
        resultats = cursor.fetchall()
        conn.close()
    return resultats

def verifier_emprunts_en_retard():
    conn = create_connection()
    retards = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT Livre.titre, Utilisateur.pseudo, Emprunt.date_fin 
        FROM Emprunt 
        JOIN Livre ON Emprunt.id_livre = Livre.id_livre
        JOIN Utilisateur ON Emprunt.id_emprunteur = Utilisateur.id_user
        WHERE Emprunt.rendu = FALSE AND Emprunt.date_fin < CURDATE()
        """
        cursor.execute(query)
        retards = cursor.fetchall()
        conn.close()
    return retards

def inscrire_utilisateur(pseudo, mot_de_passe):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        check_query = "SELECT id_user FROM Utilisateur WHERE pseudo = %s"
        cursor.execute(check_query, (pseudo,))
        
        if cursor.fetchone():
            conn.close()
            return False, "Ce pseudo est deja utilise."
        
        insert_query = "INSERT INTO Utilisateur (pseudo, mot_de_passe) VALUES (%s, %s)"
        try:
            cursor.execute(insert_query, (pseudo, mot_de_passe))
            conn.commit()
            return True, "Inscription reussie !"
        except Error as e:
            return False, f"Erreur lors de l'inscription : {e}"
        finally:
            conn.close()
    return False, "Connexion a la base de donnees impossible."


def connecter_utilisateur(pseudo, mot_de_passe):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Utilisateur WHERE pseudo = %s AND mot_de_passe = %s"
        try:
            cursor.execute(query, (pseudo, mot_de_passe))
            user = cursor.fetchone()
            if user:
                return True, user 
            else:
                return False, "Pseudo ou mot de passe incorrect."
        except Error as e:
            return False, f"Erreur de base de donnees : {e}"
        finally:
            conn.close()
    return False, "Connexion impossible."

def ajouter_livre_avec_avis(id_proprietaire, titre, auteur, date_publication, note, commentaire):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            query_livre = """
            INSERT INTO Livre (titre, auteur, date_publication, id_proprietaire) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_livre, (titre, auteur, date_publication, id_proprietaire))
            id_livre_cree = cursor.lastrowid
            query_avis = """
            INSERT INTO Avis (id_livre, id_user, note, commentaire) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_avis, (id_livre_cree, id_proprietaire, note, commentaire))
            
            conn.commit() 
            return True, "Livre et avis ajoutés !"
            
        except Error as e:
            conn.rollback() 
            return False, f"Erreur : {e}"
        finally:
            conn.close()
    return False, "Connexion impossible."

def recuperer_tous_les_livres():
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        # On récupère tout, y compris l'id_proprietaire pour le test du bouton
        query = "SELECT id_livre, titre, auteur, id_proprietaire FROM Livre"
        cursor.execute(query)
        res = cursor.fetchall()
        conn.close()
        return res
    return []

def recuperer_top_livres():
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT L.titre, ROUND(AVG(A.note), 1) as moyenne 
        FROM Livre L 
        LEFT JOIN Avis A ON L.id_livre = A.id_livre 
        GROUP BY L.id_livre, L.titre
        ORDER BY moyenne DESC 
        LIMIT 5
        """
        cursor.execute(query)
        res = cursor.fetchall()
        conn.close()
        return res
    return []

def recuperer_derniers_avis_complets():
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT U.pseudo, L.titre, A.commentaire, A.note
        FROM Avis A
        JOIN Utilisateur U ON A.id_user = U.id_user
        JOIN Livre L ON A.id_livre = L.id_livre
        ORDER BY A.id_avis DESC LIMIT 5
        """
        cursor.execute(query)
        res = cursor.fetchall()
        conn.close()
        return res
    return []

def recuperer_emprunts_utilisateur(id_user):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT L.titre, E.date_fin 
        FROM Emprunt E
        JOIN Livre L ON E.id_livre = L.id_livre
        WHERE E.id_emprunteur = %s AND E.rendu = 0
        ORDER BY E.date_fin ASC
        """
        cursor.execute(query, (id_user,))
        res = cursor.fetchall()
        conn.close()
        return res
    return []

def rechercher_livres(terme):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        terme_clean = f"%{terme.lower()}%"
        
        query = """
        SELECT L.titre, L.auteur, U.pseudo, AVG(A.note) as moyenne
        FROM Livre L
        JOIN Utilisateur U ON L.id_proprietaire = U.id_user
        LEFT JOIN Avis A ON L.id_livre = A.id_livre
        WHERE LOWER(L.titre) LIKE %s OR LOWER(L.auteur) LIKE %s
        GROUP BY L.id_livre
        """
        cursor.execute(query, (terme_clean, terme_clean))
        res = cursor.fetchall()
        conn.close()
        return res
    return []

def rechercher_livres_disponibles(terme=""):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        terme_clean = f"%{terme.lower()}%"
        query = """
        SELECT id_livre, titre, auteur FROM Livre 
        WHERE id_livre NOT IN (
            SELECT id_livre FROM Emprunt WHERE rendu = 0
        )
        AND (LOWER(titre) LIKE %s OR LOWER(auteur) LIKE %s)
        """
        try:
            cursor.execute(query, (terme_clean, terme_clean))
            res = cursor.fetchall()
            return res
        except Error as e:
            print(f"Erreur SQL détaillée : {e}") 
            return []
        finally:
            conn.close()
    return []

def enregistrer_emprunt(id_user, id_livre, jours):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = """
        INSERT INTO Emprunt (id_livre, id_emprunteur, date_debut, date_fin, rendu) 
        VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL %s DAY), 0)
        """
        try:
            cursor.execute(query, (id_livre, id_user, jours))
            conn.commit()
            return True, "Emprunt enregistré avec succès !"
        except Error as e:
            return False, f"Erreur SQL : {e}"
        finally:
            conn.close()
    return False, "Erreur de connexion"

def modifier_livre(id_livre, nouveau_titre, nouvel_auteur):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE Livre SET titre = %s, auteur = %s WHERE id_livre = %s"
        try:
            cursor.execute(query, (nouveau_titre, nouvel_auteur, id_livre))
            conn.commit()
            return True
        except Error as e:
            print(f"Erreur modif : {e}")
            return False
        finally:
            conn.close()
    return False


# Zone de test rapide
if __name__ == "__main__":
    test_conn = create_connection()
    if test_conn:
        print("Connexion reussie !")
        test_conn.close()
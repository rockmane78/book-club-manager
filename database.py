import mysql.connector
from mysql.connector import Error

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Charge les variables du fichier .env
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
        # Recherche flexible sur le titre ou l'auteur
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
        # On cherche les emprunts non rendus ou la date de fin est depassee
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

# Zone de test rapide
if __name__ == "__main__":
    test_conn = create_connection()
    if test_conn:
        print("Connexion reussie !")
        test_conn.close()
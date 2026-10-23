import time
import sys
import random
from playwright.sync_api import sync_playwright

# Configuration de l'encodage pour la console Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Chemin vers l'exécutable de Brave
BRAVE_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# URL cible
URL = "https://www.mypetition.org/petition/politique/exclure-joris/288374"

# Nombre d'adresses emails aléatoires @gmail.com à générer et traiter
NOMBRE_DE_MAILS = 100

# Sélecteurs des éléments à manipuler
BOUTON_COOKIES_SELECTOR = ".sd-cmp-lJWnC.sd-cmp-M5paA.sd-cmp-cWOb7"  # Bouton Sirdata
BOUTON_1_SELECTOR = "#btn-sign-another-email"  # 1er bouton (cliqué s'il apparaît)
CHAMP_TEXTE_SELECTOR = ".email-input"          # Champ de saisie email
BOUTON_2_SELECTOR = "#registration-no"         # 2ème bouton (option "Non")
BOUTON_3_SELECTOR = "#block-btn-sign"          # 3ème bouton ("Je signe")

# Paramètres d'exécution
HEADLESS = True              # False = Fenêtre Brave visible, True = En arrière-plan
DELAI_ENTRE_ACTIONS = 0.001    # Pause en secondes entre chaque action
DELAI_ENTRE_TOURS = 0.001       # Pause en secondes avant d'ouvrir la prochaine session privée

# ==============================================================================
# GÉNÉRATEUR D'ADRESSES EMAIL ALÉATOIRES @GMAIL.COM
# ==============================================================================

def generer_liste_emails(quantite=100):
    prenoms = [
        "lucas", "thomas", "leo", "hugo", "emma", "lea", "chloe", "manon", "alex", "nathan",
        "maxime", "julie", "camille", "arthur", "sarah", "antoine", "theo", "romain", "paul",
        "louis", "gabriel", "jules", "mathis", "clementine", "clara", "victor", "ines", "oceane"
    ]
    noms = [
        "martin", "bernard", "dubois", "thomas", "robert", "richard", "petit", "durand",
        "leroy", "moreau", "simon", "laurent", "michel", "garcia", "david", "bertrand",
        "roux", "vincent", "fournier", "morel", "girard", "andre", "lefevre", "mercier"
    ]
    
    emails = set()
    while len(emails) < quantite:
        p = random.choice(prenoms)
        n = random.choice(noms)
        num = random.randint(10, 9999)
        sep = random.choice([".", "_", ""])
        emails.add(f"{p}{sep}{n}{num}@gmail.com")
        
    return list(emails)

# ==============================================================================
# SCRIPT D'AUTOMATISATION
# ==============================================================================

def executer_cycle(playwright, numero_cycle, total_cycles, email_a_saisir):
    print(f"\n==========================================")
    print(f"[*] Cycle {numero_cycle}/{total_cycles} | Email : {email_a_saisir}")
    print(f"==========================================")

    # Lancement de Brave
    browser = playwright.chromium.launch(
        executable_path=BRAVE_PATH,
        headless=HEADLESS,
        args=["--incognito"]  # Ouvre une fenêtre privée indépendante
    )

    # Contexte isolé : aucun cookie ni historique conservé
    context = browser.new_context()
    page = context.new_page()

    try:
        # 1. Accès à l'URL
        print(f"[-] Navigation vers : {URL}")
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(DELAI_ENTRE_ACTIONS)

        # 2. Clic sur la modale des cookies (au tout début)
        if BOUTON_COOKIES_SELECTOR:
            try:
                print(f"[-] Recherche de la modale cookies...")
                cookie_loc = page.locator(BOUTON_COOKIES_SELECTOR)
                cookie_loc.first.wait_for(state="visible", timeout=6000)
                cookie_btn = cookie_loc.last if cookie_loc.count() > 1 else cookie_loc.first
                print(f"[-] Clic pour accepter les cookies...")
                cookie_btn.click()
                time.sleep(DELAI_ENTRE_ACTIONS)
            except Exception as e:
                print(f"[-] Pas de modale de cookies détectée.")

        # 3. Clic sur le 1er bouton (s'il apparaît)
        if BOUTON_1_SELECTOR:
            try:
                btn1 = page.locator(BOUTON_1_SELECTOR).first
                if btn1.is_visible(timeout=2000):
                    print(f"[-] Clic sur le 1er bouton ({BOUTON_1_SELECTOR})...")
                    btn1.click()
                    time.sleep(DELAI_ENTRE_ACTIONS)
                else:
                    print(f"[-] 1er bouton non affiché, suite directe.")
            except Exception:
                print(f"[-] 1er bouton non requis ou ignoré.")

        # 4. Remplissage du champ email
        print(f"[-] Saisie de l'email : {email_a_saisir}")
        champ = page.locator(CHAMP_TEXTE_SELECTOR).first
        champ.wait_for(state="visible", timeout=10000)
        champ.fill(email_a_saisir)
        time.sleep(DELAI_ENTRE_ACTIONS)

        # 5. Clic sur le 2ème bouton (ex: #registration-no)
        print(f"[-] Clic sur le 2ème bouton ({BOUTON_2_SELECTOR})...")
        page.locator(BOUTON_2_SELECTOR).first.click(force=True, timeout=10000)
        time.sleep(DELAI_ENTRE_ACTIONS)

        # 6. Clic sur le 3ème bouton (ex: #block-btn-sign)
        print(f"[-] Clic sur le 3ème bouton ({BOUTON_3_SELECTOR})...")
        page.locator(BOUTON_3_SELECTOR).first.click(timeout=10000)
        time.sleep(DELAI_ENTRE_ACTIONS)

        print(f"[✓] Tour {numero_cycle}/{total_cycles} terminé avec succès.")

    except Exception as e:
        print(f"[!] Erreur durant le tour {numero_cycle} : {e}")

    finally:
        # Fermeture de la page, du contexte et du navigateur
        print(f"[-] Fermeture de la fenêtre privée.")
        try:
            context.close()
            browser.close()
        except Exception:
            pass


def main():
    # Génération des 100 adresses emails aléatoires
    liste_emails = generer_liste_emails(NOMBRE_DE_MAILS)

    print("==========================================")
    print(" Lancement de l'automatisation Brave Privé")
    print(f" Nombre d'adresses email @gmail.com générées : {len(liste_emails)}")
    print(" Exemples d'emails générés :", ", ".join(liste_emails[:3]), "...")
    print(" Appuyez sur Ctrl+C pour arrêter le script à tout moment")
    print("==========================================")

    with sync_playwright() as playwright:
        for index, email in enumerate(liste_emails, start=1):
            executer_cycle(playwright, index, len(liste_emails), email)

            if index < len(liste_emails):
                print(f"[-] Attente de {DELAI_ENTRE_TOURS}s avant le prochain tour...")
                time.sleep(DELAI_ENTRE_TOURS)

    print("\n[✓] Tous les cycles ont été exécutés avec succès !")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Script interrompu par l'utilisateur (Ctrl+C).")
        sys.exit(0)

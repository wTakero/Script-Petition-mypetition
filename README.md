# Script d'Automatisation Brave (Navigation Privée)

Ce script utilise **Playwright** pour piloter le navigateur **Brave** en mode navigation privée, effectuer une série d'actions précises, fermer la page et recommencer en boucle.

---

## 📁 Fichiers inclus

- [automation_brave.py](file:///c:/Users/anton/Downloads/Script/automation_brave.py) : Le script Python principal d'automatisation.
- [lancer.bat](file:///c:/Users/anton/Downloads/Script/lancer.bat) : Raccourci pour lancer le script en un clic.
- [test_page.html](file:///c:/Users/anton/Downloads/Script/test_page.html) : Une page web locale pour tester immédiatement le fonctionnement.

---

## 🚀 Comment lancer le script

1. **Option 1** : Double-cliquez sur `lancer.bat`.
2. **Option 2** : Dans un terminal, lancez :
   ```powershell
   python automation_brave.py
   ```
*(Appuyez sur `Ctrl + C` à tout moment dans le terminal pour arrêter le script).*

---

## ⚙️ Personnaliser le script pour votre site

Ouvrez [automation_brave.py](file:///c:/Users/anton/Downloads/Script/automation_brave.py) et modifiez la section **CONFIGURATION** en haut du fichier :

```python
# 1. Votre URL
URL = "https://www.mypetition.org/petition/politique/exclure-joris/288374"

# 2. Nombre d'emails @gmail.com aléatoires à générer et injecter
NOMBRE_DE_MAILS = 100

# 3. Vos sélecteurs
BOUTON_COOKIES_SELECTOR = ".sd-cmp-lJWnC.sd-cmp-M5paA.sd-cmp-cWOb7"  # Bouton 'Tout accepter' (Sirdata)
BOUTON_1_SELECTOR = "#btn-sign-another-email"  # 1er bouton (facultatif / si affiché)
CHAMP_TEXTE_SELECTOR = ".email-input"          # Champ où injecter l'email
BOUTON_2_SELECTOR = "#registration-no"         # 2ème bouton (option "Non")
BOUTON_3_SELECTOR = "#block-btn-sign"          # 3ème bouton ("Je signe")

# 4. Paramètres de boucle et délais
HEADLESS = False          # False = fenêtre Brave visible, True = en arrière-plan
DELAI_ENTRE_ACTIONS = 2.0 # Pause en secondes entre chaque action
DELAI_ENTRE_TOURS = 2.5   # Pause en secondes avant d'ouvrir la prochaine session privée
```

---

## 🔍 Comment trouver les sélecteurs sur votre site ?

1. Ouvrez votre page dans **Brave**.
2. Faites un **clic droit** sur le bouton ou le champ que vous voulez cibler, puis cliquez sur **Inspecter**.
3. Dans la fenêtre d'inspection (Outils de développement) :
   - Faites un **clic droit sur la ligne en surbrillance**.
   - Allez sur **Copier** > **Copier le sélecteur** (ou *Copy selector*).
   - Collez-le directement dans la variable correspondante.
4. *Alternative Playwright très pratique* : Vous pouvez aussi cibler directement par le texte du bouton :
   ```python
   BOUTON_1_SELECTOR = "text='Valider'"
   # ou
   BOUTON_1_SELECTOR = "button:has-text('Confirmer')"
   ```

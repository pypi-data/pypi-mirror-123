from random import randint, choice
import os

global SALARY_VALUE
SALARY_VALUE = 0
global TRANSACTION_VALUE
TRANSACTION_VALUE = 1
global NOT_CONNECTED
NOT_CONNECTED = 0
global CONNECTED
CONNECTED = 1

accounts = []
ids = []
book = []

def clear():
   os.system("clear" if os.name != "nt" else "cls")

def chooseIn(poss=[]):
   poss = [str(i) for i in poss]
   choice = input()
   if choice in poss:
      return choice
   print("Choix impossible")
   if len(poss)<=50:
      print("Vous pouvez uniquement choisir parmi les possibilités suivantes:")
      for possibility in poss:
         print("[*]", possibility)
   return chooseIn(poss)

def chooseInteger():
   choice = input()
   if choice.isdigit():
      return int(choice)
   else:
      return chooseInteger()

def find_accound_by_id(accounts, id_account):
   for account in accounts:
      if account[0] == id_account:
         return account

def create_id(ids):
   new_id = [str(randint(0, 9)) for i in range(10)]
   if new_id not in ids:
      ids.append(new_id)
      return ids, "".join(new_id)
   return create_id(ids)

def create_transaction(book, accounts, debtor_id, receiver_id, money):
   debtor = find_accound_by_id(accounts, debtor_id)
   receiver = find_accound_by_id(accounts, receiver_id)
   debtor[-1] -= int(money)
   receiver[-1] += int(money)
   new_transaction = [TRANSACTION_VALUE, debtor_id, receiver_id, money]
   book.append(new_transaction)
   return accounts, book

def do_transaction(book, accounts, personnal_id):
   print("Vous choisissez de faire une transaction.")
   print("A qui devez vous de l'argent?")
   i = 0
   poss = []
   for account in accounts:
      print('('+ str(i)+ ')', account[1])
      poss.append(str(i))
      i += 1
   choice = chooseIn(poss)
   receiver_account = accounts[int(choice)]
   receiver_id = receiver_account[0]
   poss = range(0, find_accound_by_id(accounts, personnal_id)[-1]+1)
   print("Veuillez chosir le montant à payer: de 0 à", str(find_accound_by_id(accounts, personnal_id)[-1]))
   money = chooseIn(poss)
   accounts, book = create_transaction(book, accounts, personnal_id, receiver_id, money)
   return accounts, book

def create_account(ids, accounts, name, code, money, job):
   ids, id_account = create_id(ids)
   new_account = [id_account, name, code, job, money]
   accounts.append(new_account)
   return accounts, id_account

def do_salary(book, accounts):
   jobs = []
   accounts_by_jobs = {}
   for account in accounts:
      job = account[-2]
      if job in jobs:
         accounts_by_jobs[job].append(account)
      else:
         accounts_by_jobs[job] = []
         accounts_by_jobs[job].append(account)
         jobs.append(job)
   print("Quel métier voulez vous rémunérer?")
   poss = []
   i = 0
   for job in jobs:
      print('('+str(i)+')', job)
      poss.append(i)
      i += 1
   choice = chooseIn(poss)
   print("Veuillez entrer le salaire à envoyer")
   money = chooseInteger()
   job = jobs[int(choice)]
   for account in accounts_by_jobs[job]:
      accounts, book = salary(book, accounts, account[0], money)
   print("Salaire envoyé")
   input()
   return accounts, book

def salary(book, accounts, id_account, money):
   account = find_accound_by_id(accounts, id_account)
   account[-1] += money
   new_transaction = [SALARY_VALUE, id_account, money]
   book.append(new_transaction)
   return accounts, book

def connexion(accounts):
   connected = True
   print("A quel compte voulez-vous vous connecter?: (écrire q pour créer un compte) ")
   i = 0
   poss = []
   for account in accounts:
      print('('+ str(i)+ ')',  account[1])
      poss.append(str(i))
      i += 1
   poss.append("q")
   choice = chooseIn(poss)
   code = ""
   if choice == "q":
      return [NOT_CONNECTED, NOT_CONNECTED]
   else:
      while code != str(accounts[int(choice)][2]):
         code = input("Veuillez entrer le code de connexion ou bien q pour quitter: ")
         if code == "q":
            clear()
            connected, personnal_id = connexion(accounts)
            break
      return [connected, accounts[int(choice)][0]]
      if connected:
         return [CONNECTED, accounts[int(choice)][0]]

def print_account(account):
   print("---------------------------------")
   print("Nom:", account[1])
   print("ID:", account[0])
   print("Métier:", account[-2])
   print("Code", account[2])
   print("Argent:", str(account[-1]))

def account_menu(accounts, personnal_id, book):
   clear()
   account = find_accound_by_id(accounts, personnal_id)
   money = account[-1]
   print(f"Bienvenue sur votre application bancaire")
   print("Vous avez", str(money), "€")
   print("Voici les actions que vous pouvez faire:")
   print("[*] Faire une transaction (0)")
   print("[*] Payer un métier (1)")
   print("[*] Inspecter toutes les transactions (2)")
   print("[*] Regarder les informations de tous les comptes bancaires (3)")
   print("[*] Se deconnecter (q)")
   choice = chooseIn(["0", "1", "q", "2", "3"])
   if choice == "0":
      accounts, book = do_transaction(book, accounts, personnal_id)
      account_menu(accounts, personnal_id, book)
   elif choice == "1":
      accounts, book = do_salary(book, accounts)
      account_menu(accounts, personnal_id, book)
   elif choice == "2":
      for transaction in book:
         print(transaction)
      input()
      account_menu(accounts, personnal_id, book)
   elif choice == "3":
      for account in accounts:
         print_account(account)
      input()
      account_menu(accounts, personnal_id, book)


all_names = ["Paul", "Patrick", "François", "Bob", "Frank", "Rene", "Marie", "Marine", "Esthéban", "Zia", "Julie", "Dolores", "Ducobu"]
all_jobs = ["Professeur", "Etudiant", "Développeur", "Sportif", "Scientifique", "Artiste", "Banquier", "Directeur"]
for i in range(10):
   accounts, id_account = create_account(ids, accounts, choice(all_names), "".join([str(randint(0, 9)) for _ in range(4)]), randint(0, 1000), choice(all_jobs))

run = True
while run:
   clear()
   print("Voulez vous créer un compte (0), vous connecter (1) ou bien fermer l'application (q)?")
   choice = chooseIn(["0", "1", "q"])
   clear()
   if choice == "0":
      name = input("Veuillez entrer un nom pour votre compte: ")
      code = input("Veuillez entrer un code: ")
      job = input("Veuillez entrer votre métier actuel: ")
      accounts, personnal_id = create_account(ids, accounts, name, code, 0, job)
      print("Compté créé!")
      connected = True
      input()
   elif choice == "1":
      connexions_infos = connexion(accounts)
      connected = connexions_infos[0]
      personnal_id = connexions_infos[1]
   else:
      break
   if connected:
      account_menu(accounts, personnal_id, book)
print("Fermeture de l'application...")

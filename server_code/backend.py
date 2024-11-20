import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

# id > name normal aber hier bei 2 egal

@anvil.server.callable
def get_zellen(name):
  zellen = []
# keine zeit mehr
  package = cursor.fetchall()
  for name in package:
    gefaengnisse.append(name[0])
  connection.close()
  return gefaengnisse

@anvil.server.callable
def get_gefaengnisse():
  gefaengnisse = []
  connection = sqlite3.connect('GefaengnissVerwaltungsSystem.db')
  cursor = connection.cursor()

  cursor.execute('''
  SELECT Name FROM Gefaengnis;
  ''')
  package = cursor.fetchall()
  for name in package:
    gefaengnisse.append(name[0])
  connection.close()
  return gefaengnisse

@anvil.server.callable
def get_direktor(name):
  connection = sqlite3.connect('GefaengnissVerwaltungsSystem.db')
  cursor = connection.cursor()
  cursor.execute('SELECT Direktor FROM Gefaengnis WHERE Name = ?', (name,))
  package = cursor.fetchall()
  connection.close()
  return package[0][0]
  

@anvil.server.callable
def get_freie_zellen(name):
  connection = sqlite3.connect('GefaengnissVerwaltungsSystem.db')
  cursor = connection.cursor()
  cursor.execute('SELECT AnzahlFreieZellen FROM Gefaengnis WHERE Name = ?', (name,))
  package = cursor.fetchall()
  connection.close()
  return package[0][0]

@anvil.server.callable
def reset_database():
    connection = sqlite3.connect('GefaengnissVerwaltungsSystem.db')
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS Gefaengnis;')
    cursor.execute('DROP TABLE IF EXISTS Zelle;')
    cursor.execute('DROP TABLE IF EXISTS Haeftling;')
    cursor.execute('DROP TABLE IF EXISTS Verwaltung;')
    connection.commit()
    connection.close()

@anvil.server.callable
def create_database():
    connection = sqlite3.connect('GefaengnissVerwaltungsSystem.db')
    cursor = connection.cursor()

    # Create Gefaengnis table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Gefaengnis(
        GID INTEGER PRIMARY KEY,
        Direktor TEXT,
        Name TEXT,
        AnzahlFreieZellen INTEGER,
        AnzahlBelegteZellen INTEGER
    );
    ''')

    # Create Zelle table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Zelle(
        Zellennummer INTEGER PRIMARY KEY,
        GID INTEGER,
        FOREIGN KEY (GID) REFERENCES Gefaengnis(GID)
    );
    ''')

    # Create Haeftling table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Haeftling(
        Haeftlingsnummer INTEGER PRIMARY KEY,
        Haftdauer INTEGER,
        Zellennummer INTEGER,
        FOREIGN KEY (Zellennummer) REFERENCES Zelle(Zellennummer)
    );
    ''')

    # Create Verwaltung table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Verwaltung(
        VID INTEGER PRIMARY KEY,
        EinzugsDatum DATE,
        AuszugsDatum DATE,
        Haeftlingsnummer INTEGER,
        Zellennummer INTEGER,
        FOREIGN KEY (Haeftlingsnummer) REFERENCES Haeftling(Haeftlingsnummer),
        FOREIGN KEY (Zellennummer) REFERENCES Zelle(Zellennummer)
    );
    ''')

    connection.commit()
    connection.close()

@anvil.server.callable
def fill_database():
  connection = sqlite3.connect('GefaengnissVerwaltungsSystem.db')
  cursor = connection.cursor()

  cursor.execute("INSERT INTO Gefaengnis (Direktor, Name, AnzahlFreieZellen, AnzahlBelegteZellen) VALUES ('Direktor 1', 'Gefängnis 1', 3, 2);")
  cursor.execute("INSERT INTO Gefaengnis (Direktor, Name, AnzahlFreieZellen, AnzahlBelegteZellen) VALUES ('Direktor 2', 'Gefängnis 2', 2, 1);")

  cursor.execute("INSERT INTO Zelle (GID) VALUES (1);")  
  cursor.execute("INSERT INTO Zelle (GID) VALUES (1);")  # Gefängnis 1
  cursor.execute("INSERT INTO Zelle (GID) VALUES (1);")  # Gefängnis 1
  cursor.execute("INSERT INTO Zelle (GID) VALUES (2);")  # Gefängnis 2
  cursor.execute("INSERT INTO Zelle (GID) VALUES (2);")  # Gefängnis 2

  # Insert test data for Haeftlinge
  cursor.execute("INSERT INTO Haeftling (Haeftlingsnummer, Haftdauer, Zellennummer) VALUES (1, 10, 101);")  # Häftling 1 in Zelle 101
  cursor.execute("INSERT INTO Haeftling (Haeftlingsnummer, Haftdauer, Zellennummer) VALUES (2, 12, 103);")  # Häftling 2 in Zelle 103
  cursor.execute("INSERT INTO Haeftling (Haeftlingsnummer, Haftdauer, Zellennummer) VALUES (3, 15, 102);")  # Häftling 3 in Zelle 102
  cursor.execute("INSERT INTO Haeftling (Haeftlingsnummer, Haftdauer, Zellennummer) VALUES (4, 8, 102);")   # Häftling 4 in Zelle 102

  cursor.execute("INSERT INTO Verwaltung (EinzugsDatum, AuszugsDatum, Haeftlingsnummer, Zellennummer) VALUES ('2024-01-01', '2025-01-01', 1, 101);")
  cursor.execute("INSERT INTO Verwaltung (EinzugsDatum, AuszugsDatum, Haeftlingsnummer, Zellennummer) VALUES ('2024-01-01', '2025-01-01', 2, 103);")
  cursor.execute("INSERT INTO Verwaltung (EinzugsDatum, AuszugsDatum, Haeftlingsnummer, Zellennummer) VALUES ('2024-01-01', '2025-01-01', 3, 102);")
  cursor.execute("INSERT INTO Verwaltung (EinzugsDatum, AuszugsDatum, Haeftlingsnummer, Zellennummer) VALUES ('2024-01-01', '2025-01-01', 4, 102);")

  connection.commit()
  connection.close()
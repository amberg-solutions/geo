# Beispielprojekt Geoportal für das Amt für Landwirtschaft und Geodaten

In diesem Beispiel Projekt möchte ich bereits bestehende Kenntnisse aufzeigen, und neue Technologien anwenden, mit denen ich bis dato keine Berührungspunkte hatte.

## Beschreibung

Die App besteht aus einem Python Backend - ein zyklischer Job lädt von der öffentlichen API https://data.gr.ch/api-console/explore/v2.1/ Daten zu Tourismusdestinationen direkt in meine PostgreSQL Datenbank (Azure).
Hier habe ich mich das erste Mal mit postgis auseinandergesetzt, die Extension installiert und gelernt wie ich Geographische Daten (Polygon) in der DB speichere und wieder abrufe.

Das Frontend (HTML, CSS) wurde mithilfe von GPT-5.6 Sol erstellt - das Backend habe ich zu 80-90% selber geschrieben. Beim ein- und auslesen der Geodaten, sowie der Kartenerstellung habe ich mich wiederrum unterstützen lassen. 

Die selbst geschriebene Javscript API, lädt asynchron die geographischen Informationen aus der Datenbank, und rendert sie im Frontend der App. 

## Author
Kai Lanz
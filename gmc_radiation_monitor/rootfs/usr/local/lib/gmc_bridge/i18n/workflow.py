from __future__ import annotations

EN: dict[str, str] = {
    "Workflows": "Workflows",
    "Workflows and operations": "Workflows and operations",
    "Notification rules, event notes, period comparisons, history exploration, self-tests, scheduled reports, backups and JSON APIs work with the existing measurements and require no additional hardware.": "Notification rules, event notes, period comparisons, history exploration, self-tests, scheduled reports, backups and JSON APIs work with the existing measurements and require no additional hardware.",
    "Guided status": "Guided status",
    "What is ready and what still needs time": "What is ready and what still needs time",
    "Device detected": "Device detected",
    "At least one GMC device is known": "At least one GMC device is known",
    "Measurement running": "Measurement running",
    "At least one GMC device is currently connected": "At least one GMC device is currently connected",
    "History is being stored": "History is being stored",
    "Accepted measurements are available in the database": "Accepted measurements are available in the database",
    "Local baseline available": "Local baseline available",
    "The baseline needs approximately {days} days of local history": "The baseline needs approximately {days} days of local history",
    "Workflow tools ready": "Workflow tools ready",
    "Comparisons, annotations, self-test, backups and APIs are available without additional hardware": "Comparisons, annotations, self-test, backups and APIs are available without additional hardware",
    "Notifications and scheduled reports": "Notifications and scheduled reports",
    "Enable Home Assistant notifications": "Enable Home Assistant notifications",
    "Notify when a device stays offline": "Notify when a device stays offline",
    "Notify when accepted measurements become stale": "Notify when accepted measurements become stale",
    "Notify about confirmed warning events": "Notify about confirmed warning events",
    "Notify about database integrity problems": "Notify about database integrity problems",
    "Offline threshold in minutes": "Offline threshold in minutes",
    "Stale-data threshold in minutes": "Stale-data threshold in minutes",
    "Notification cooldown in minutes": "Notification cooldown in minutes",
    "Enable scheduled reports": "Enable scheduled reports",
    "Daily ZIP reports": "Daily ZIP reports",
    "Weekly ZIP reports": "Weekly ZIP reports",
    "Monthly JSON summaries": "Monthly JSON summaries",
    "Report hour": "Report hour",
    "Managed backups to retain": "Managed backups to retain",
    "Save workflow settings": "Save workflow settings",
    "No notification has been sent yet": "No notification has been sent yet",
    "Last notification: {time}": "Last notification: {time}",
    "No scheduled report has run yet": "No scheduled report has run yet",
    "Last scheduled report: {time}": "Last scheduled report: {time}",
    "Compare periods": "Compare periods",
    "Compare two freely selected date ranges": "Compare two freely selected date ranges",
    "First period from": "First period from",
    "First period to": "First period to",
    "Second period from": "Second period from",
    "Second period to": "Second period to",
    "Compare": "Compare",
    "First period mean": "First period mean",
    "Second period mean": "Second period mean",
    "Mean difference": "Mean difference",
    "Median difference": "Median difference",
    "Statistical indication": "Statistical indication",
    "Difference divided by the combined standard error": "Difference divided by the combined standard error",
    "{count} samples · {coverage:.1f}% coverage": "{count} samples · {coverage:.1f}% coverage",
    "Not enough data for a comparison": "Not enough data for a comparison",
    "The comparison is only indicative because data coverage is low": "The comparison is only indicative because data coverage is low",
    "No clear statistical difference is visible": "No clear statistical difference is visible",
    "A possible difference is visible and should be observed longer": "A possible difference is visible and should be observed longer",
    "A clear statistical difference is visible; this does not identify the physical cause": "A clear statistical difference is visible; this does not identify the physical cause",
    "Event notes": "Event notes",
    "Document ventilation, movement, maintenance or an unknown cause": "Document ventilation, movement, maintenance or an unknown cause",
    "Start": "Start",
    "End": "End",
    "Category": "Category",
    "Status": "Status",
    "Window opened": "Window opened",
    "Ventilation": "Ventilation",
    "Device moved": "Device moved",
    "Maintenance": "Maintenance",
    "Unknown cause": "Unknown cause",
    "Other": "Other",
    "Note": "Note",
    "Confirmed": "Confirmed",
    "Dismissed": "Dismissed",
    "Add event note": "Add event note",
    "Confirm": "Confirm",
    "Dismiss": "Dismiss",
    "Delete": "Delete",
    "Delete this annotation?": "Delete this annotation?",
    "No annotations have been added yet.": "No annotations have been added yet.",
    "History explorer": "History explorer",
    "Recent accepted CPM values with event markers": "Recent accepted CPM values with event markers",
    "CPM history explorer": "CPM history explorer",
    "No history data in this period": "No history data in this period",
    "Minimum": "Minimum",
    "Open history JSON": "Open history JSON",
    "Open events JSON": "Open events JSON",
    "System self-test": "System self-test",
    "Database, devices, freshness, Home Assistant, storage, configuration and translations": "Database, devices, freshness, Home Assistant, storage, configuration and translations",
    "Open self-test JSON": "Open self-test JSON",
    "Database integrity": "Database integrity",
    "Database check result: {result}": "Database check result: {result}",
    "Database schema": "Database schema",
    "Schema version {current} of {expected}": "Schema version {current} of {expected}",
    "Known devices": "Known devices",
    "{count} devices are registered": "{count} devices are registered",
    "Device connections": "Device connections",
    "{connected} of {known} devices are connected": "{connected} of {known} devices are connected",
    "Measurement freshness": "Measurement freshness",
    "Latest measurement age: {seconds} seconds": "Latest measurement age: {seconds} seconds",
    "No stored measurement is available": "No stored measurement is available",
    "Home Assistant API": "Home Assistant API",
    "Home Assistant API is available": "Home Assistant API is available",
    "Home Assistant API is currently unavailable": "Home Assistant API is currently unavailable",
    "Timezone {timezone} is valid": "Timezone {timezone} is valid",
    "Timezone {timezone} is invalid": "Timezone {timezone} is invalid",
    "Free storage": "Free storage",
    "{mib:.0f} MiB are available": "{mib:.0f} MiB are available",
    "Storage information is unavailable: {error}": "Storage information is unavailable: {error}",
    "Translations": "Translations",
    "All translation catalogues are valid": "All translation catalogues are valid",
    "Translation catalogue problems: {count}": "Translation catalogue problems: {count}",
    "App configuration": "App configuration",
    "Configuration is valid": "Configuration is valid",
    "Configuration warnings: {count}": "Configuration warnings: {count}",
    "Configuration cannot be read: {error}": "Configuration cannot be read: {error}",
    "The options file is not available in this environment": "The options file is not available in this environment",
    "Managed backups": "Managed backups",
    "The managed backup directory is writable": "The managed backup directory is writable",
    "The managed backup directory is not writable: {error}": "The managed backup directory is not writable: {error}",
    "Configuration preflight": "Configuration preflight",
    "Check the current options before making further changes": "Check the current options before making further changes",
    "The current app configuration passed the preflight checks.": "The current app configuration passed the preflight checks.",
    "The app cannot intercept Home Assistant's Save button, but the same validator is available through the JSON API for candidate configurations.": "The app cannot intercept Home Assistant's Save button, but the same validator is available through the JSON API for candidate configurations.",
    "Open configuration validation JSON": "Open configuration validation JSON",
    "Create, inspect, download and prune local SQLite snapshots": "Create, inspect, download and prune local SQLite snapshots",
    "Create managed backup": "Create managed backup",
    "No managed backups are available.": "No managed backups are available.",
    "Machine-readable APIs": "Machine-readable APIs",
    "Use the same structured results in Home Assistant automations or external dashboards": "Use the same structured results in Home Assistant automations or external dashboards",
    "Status API": "Status API",
    "Analysis API": "Analysis API",
    "Comparison API": "Comparison API",
    "Backups API": "Backups API",
    "GMC device offline": "GMC device offline",
    "The following devices have been offline for at least {minutes} minutes: {devices}": "The following devices have been offline for at least {minutes} minutes: {devices}",
    "GMC measurements are stale": "GMC measurements are stale",
    "No accepted GMC measurement has been stored for at least {minutes} minutes.": "No accepted GMC measurement has been stored for at least {minutes} minutes.",
    "GMC database problem": "GMC database problem",
    "The SQLite quick check returned: {result}": "The SQLite quick check returned: {result}",
    "Confirmed GMC event": "Confirmed GMC event",
    "A confirmed {severity} event was recorded for {device} at {time}{cpm}.": "A confirmed {severity} event was recorded for {device} at {time}{cpm}.",
    "GMC scheduled report ready": "GMC scheduled report ready",
    "The {kind} report for {period} was created successfully. Files: {count}": "The {kind} report for {period} was created successfully. Files: {count}",
    "GMC scheduled report failed": "GMC scheduled report failed",
    "The {kind} report for {period} could not be created: {error}": "The {kind} report for {period} could not be created: {error}",
    "Daily": "Daily",
    "Weekly": "Weekly",
    "Monthly": "Monthly",
}

DE = {
    **EN,
    "Workflows": "Arbeitsabläufe",
    "Workflows and operations": "Arbeitsabläufe und Betrieb",
    "Notification rules, event notes, period comparisons, history exploration, self-tests, scheduled reports, backups and JSON APIs work with the existing measurements and require no additional hardware.": "Benachrichtigungsregeln, Ereignisnotizen, Zeitraumvergleiche, Verlaufsnavigation, Selbsttests, geplante Berichte, Sicherungen und JSON-APIs arbeiten mit den vorhandenen Messungen und benötigen keine zusätzliche Hardware.",
    "Guided status": "Geführter Status",
    "What is ready and what still needs time": "Was bereits verfügbar ist und was noch Zeit benötigt",
    "Device detected": "Gerät erkannt",
    "At least one GMC device is known": "Mindestens ein GMC-Gerät ist bekannt",
    "Measurement running": "Messung läuft",
    "At least one GMC device is currently connected": "Mindestens ein GMC-Gerät ist derzeit verbunden",
    "History is being stored": "Verlauf wird gespeichert",
    "Accepted measurements are available in the database": "Akzeptierte Messwerte sind in der Datenbank vorhanden",
    "Local baseline available": "Lokale Baseline verfügbar",
    "The baseline needs approximately {days} days of local history": "Die Baseline benötigt ungefähr {days} Tage lokalen Verlauf",
    "Workflow tools ready": "Arbeitswerkzeuge bereit",
    "Comparisons, annotations, self-test, backups and APIs are available without additional hardware": "Vergleiche, Anmerkungen, Selbsttest, Sicherungen und APIs sind ohne zusätzliche Hardware verfügbar",
    "Notifications and scheduled reports": "Benachrichtigungen und geplante Berichte",
    "Enable Home Assistant notifications": "Home-Assistant-Benachrichtigungen aktivieren",
    "Notify when a device stays offline": "Benachrichtigen, wenn ein Gerät länger offline bleibt",
    "Notify when accepted measurements become stale": "Benachrichtigen, wenn akzeptierte Messwerte veralten",
    "Notify about confirmed warning events": "Über bestätigte Warnereignisse benachrichtigen",
    "Offline threshold in minutes": "Offline-Schwelle in Minuten",
    "Stale-data threshold in minutes": "Schwelle für veraltete Daten in Minuten",
    "Notification cooldown in minutes": "Benachrichtigungspause in Minuten",
    "Enable scheduled reports": "Geplante Berichte aktivieren",
    "Daily ZIP reports": "Tägliche ZIP-Berichte",
    "Weekly ZIP reports": "Wöchentliche ZIP-Berichte",
    "Monthly JSON summaries": "Monatliche JSON-Zusammenfassungen",
    "Report hour": "Berichtsstunde",
    "Managed backups to retain": "Anzahl aufzubewahrender verwalteter Sicherungen",
    "Save workflow settings": "Arbeitsablauf-Einstellungen speichern",
    "No notification has been sent yet": "Noch keine Benachrichtigung gesendet",
    "Last notification: {time}": "Letzte Benachrichtigung: {time}",
    "No scheduled report has run yet": "Noch kein geplanter Bericht ausgeführt",
    "Last scheduled report: {time}": "Letzter geplanter Bericht: {time}",
    "Compare periods": "Zeiträume vergleichen",
    "Compare two freely selected date ranges": "Zwei frei gewählte Zeiträume vergleichen",
    "First period from": "Erster Zeitraum von",
    "First period to": "Erster Zeitraum bis",
    "Second period from": "Zweiter Zeitraum von",
    "Second period to": "Zweiter Zeitraum bis",
    "Compare": "Vergleichen",
    "First period mean": "Mittelwert erster Zeitraum",
    "Second period mean": "Mittelwert zweiter Zeitraum",
    "Mean difference": "Mittelwertdifferenz",
    "Median difference": "Mediandifferenz",
    "Statistical indication": "Statistischer Hinweis",
    "Difference divided by the combined standard error": "Differenz geteilt durch den kombinierten Standardfehler",
    "{count} samples · {coverage:.1f}% coverage": "{count} Messwerte · {coverage:.1f}% Abdeckung",
    "Not enough data for a comparison": "Nicht genügend Daten für einen Vergleich",
    "The comparison is only indicative because data coverage is low": "Der Vergleich ist wegen der geringen Datenabdeckung nur orientierend",
    "No clear statistical difference is visible": "Kein eindeutiger statistischer Unterschied erkennbar",
    "A possible difference is visible and should be observed longer": "Ein möglicher Unterschied ist erkennbar und sollte länger beobachtet werden",
    "A clear statistical difference is visible; this does not identify the physical cause": "Ein deutlicher statistischer Unterschied ist erkennbar; die physikalische Ursache wird dadurch nicht bestimmt",
    "Event notes": "Ereignisnotizen",
    "Document ventilation, movement, maintenance or an unknown cause": "Lüftung, Umstellung, Wartung oder eine unbekannte Ursache dokumentieren",
    "Start": "Beginn",
    "End": "Ende",
    "Category": "Kategorie",
    "Status": "Status",
    "Window opened": "Fenster geöffnet",
    "Ventilation": "Lüftung",
    "Device moved": "Gerät umgestellt",
    "Maintenance": "Wartung",
    "Unknown cause": "Ursache unbekannt",
    "Other": "Sonstiges",
    "Note": "Notiz",
    "Confirmed": "Bestätigt",
    "Dismissed": "Verworfen",
    "Add event note": "Ereignisnotiz hinzufügen",
    "Confirm": "Bestätigen",
    "Dismiss": "Verwerfen",
    "Delete": "Löschen",
    "Delete this annotation?": "Diese Anmerkung löschen?",
    "No annotations have been added yet.": "Noch keine Anmerkungen hinzugefügt.",
    "History explorer": "Verlaufsnavigation",
    "Recent accepted CPM values with event markers": "Neuere akzeptierte CPM-Werte mit Ereignismarkierungen",
    "CPM history explorer": "CPM-Verlaufsnavigation",
    "No history data in this period": "Keine Verlaufsdaten in diesem Zeitraum",
    "Minimum": "Minimum",
    "Open history JSON": "Verlaufs-JSON öffnen",
    "Open events JSON": "Ereignis-JSON öffnen",
    "System self-test": "System-Selbsttest",
    "Database, devices, freshness, Home Assistant, storage, configuration and translations": "Datenbank, Geräte, Aktualität, Home Assistant, Speicher, Konfiguration und Übersetzungen",
    "Open self-test JSON": "Selbsttest-JSON öffnen",
    "Database integrity": "Datenbankintegrität",
    "Database check result: {result}": "Ergebnis der Datenbankprüfung: {result}",
    "Database schema": "Datenbankschema",
    "Schema version {current} of {expected}": "Schemaversion {current} von {expected}",
    "Known devices": "Bekannte Geräte",
    "{count} devices are registered": "{count} Geräte sind registriert",
    "Device connections": "Geräteverbindungen",
    "{connected} of {known} devices are connected": "{connected} von {known} Geräten sind verbunden",
    "Measurement freshness": "Messwertaktualität",
    "Latest measurement age: {seconds} seconds": "Alter des letzten Messwerts: {seconds} Sekunden",
    "No stored measurement is available": "Kein gespeicherter Messwert verfügbar",
    "Home Assistant API": "Home-Assistant-API",
    "Home Assistant API is available": "Home-Assistant-API ist verfügbar",
    "Home Assistant API is currently unavailable": "Home-Assistant-API ist derzeit nicht verfügbar",
    "Timezone {timezone} is valid": "Zeitzone {timezone} ist gültig",
    "Timezone {timezone} is invalid": "Zeitzone {timezone} ist ungültig",
    "Free storage": "Freier Speicher",
    "{mib:.0f} MiB are available": "{mib:.0f} MiB sind verfügbar",
    "Storage information is unavailable: {error}": "Speicherinformation nicht verfügbar: {error}",
    "Translations": "Übersetzungen",
    "All translation catalogues are valid": "Alle Übersetzungskataloge sind gültig",
    "Translation catalogue problems: {count}": "Probleme in Übersetzungskatalogen: {count}",
    "App configuration": "App-Konfiguration",
    "Configuration is valid": "Konfiguration ist gültig",
    "Configuration warnings: {count}": "Konfigurationswarnungen: {count}",
    "Configuration cannot be read: {error}": "Konfiguration kann nicht gelesen werden: {error}",
    "The options file is not available in this environment": "Die Optionsdatei ist in dieser Umgebung nicht verfügbar",
    "Managed backups": "Verwaltete Sicherungen",
    "The managed backup directory is writable": "Das Verzeichnis für verwaltete Sicherungen ist beschreibbar",
    "The managed backup directory is not writable: {error}": "Das Verzeichnis für verwaltete Sicherungen ist nicht beschreibbar: {error}",
    "Configuration preflight": "Konfigurations-Vorabprüfung",
    "Check the current options before making further changes": "Aktuelle Optionen vor weiteren Änderungen prüfen",
    "The current app configuration passed the preflight checks.": "Die aktuelle App-Konfiguration hat die Vorabprüfungen bestanden.",
    "The app cannot intercept Home Assistant's Save button, but the same validator is available through the JSON API for candidate configurations.": "Die App kann die Speichern-Schaltfläche von Home Assistant nicht abfangen; dieselbe Prüfung steht jedoch über die JSON-API für geplante Konfigurationen bereit.",
    "Open configuration validation JSON": "JSON der Konfigurationsprüfung öffnen",
    "Create, inspect, download and prune local SQLite snapshots": "Lokale SQLite-Sicherungen erstellen, prüfen, herunterladen und bereinigen",
    "Create managed backup": "Verwaltete Sicherung erstellen",
    "No managed backups are available.": "Keine verwalteten Sicherungen vorhanden.",
    "Machine-readable APIs": "Maschinenlesbare APIs",
    "Use the same structured results in Home Assistant automations or external dashboards": "Dieselben strukturierten Ergebnisse in Home-Assistant-Automationen oder externen Dashboards verwenden",
    "Status API": "Status-API",
    "Analysis API": "Analyse-API",
    "Comparison API": "Vergleichs-API",
    "Backups API": "Sicherungs-API",
    "GMC device offline": "GMC-Gerät offline",
    "The following devices have been offline for at least {minutes} minutes: {devices}": "Folgende Geräte sind seit mindestens {minutes} Minuten offline: {devices}",
    "GMC measurements are stale": "GMC-Messwerte sind veraltet",
    "No accepted GMC measurement has been stored for at least {minutes} minutes.": "Seit mindestens {minutes} Minuten wurde kein akzeptierter GMC-Messwert gespeichert.",
    "GMC database problem": "GMC-Datenbankproblem",
    "The SQLite quick check returned: {result}": "Die SQLite-Schnellprüfung ergab: {result}",
    "Confirmed GMC event": "Bestätigtes GMC-Ereignis",
    "A confirmed {severity} event was recorded for {device} at {time}{cpm}.": "Für {device} wurde um {time} ein bestätigtes Ereignis der Stufe {severity} aufgezeichnet{cpm}.",
    "GMC scheduled report ready": "Geplanter GMC-Bericht ist fertig",
    "The {kind} report for {period} was created successfully. Files: {count}": "Der Bericht {kind} für {period} wurde erfolgreich erstellt. Dateien: {count}",
    "GMC scheduled report failed": "Geplanter GMC-Bericht fehlgeschlagen",
    "The {kind} report for {period} could not be created: {error}": "Der Bericht {kind} für {period} konnte nicht erstellt werden: {error}",
    "Daily": "Täglich",
    "Weekly": "Wöchentlich",
    "Monthly": "Monatlich",
}

# The additional languages intentionally keep the same stable English keys.
# Every visible workflow string has a native-language value so the dashboard
# never falls back to mixed English text.
FR = {
    **EN,
    "Workflows": "Flux de travail", "Workflows and operations": "Flux de travail et exploitation",
    "Notification rules, event notes, period comparisons, history exploration, self-tests, scheduled reports, backups and JSON APIs work with the existing measurements and require no additional hardware.": "Les règles de notification, notes d’événement, comparaisons de périodes, exploration de l’historique, autotests, rapports planifiés, sauvegardes et API JSON utilisent les mesures existantes et ne nécessitent aucun matériel supplémentaire.",
    "Guided status": "État guidé", "What is ready and what still needs time": "Ce qui est prêt et ce qui nécessite encore du temps",
    "Device detected": "Appareil détecté", "At least one GMC device is known": "Au moins un appareil GMC est connu",
    "Measurement running": "Mesure en cours", "At least one GMC device is currently connected": "Au moins un appareil GMC est actuellement connecté",
    "History is being stored": "L’historique est enregistré", "Accepted measurements are available in the database": "Des mesures acceptées sont disponibles dans la base de données",
    "Local baseline available": "Référence locale disponible", "The baseline needs approximately {days} days of local history": "La référence nécessite environ {days} jours d’historique local",
    "Workflow tools ready": "Outils de flux de travail prêts", "Comparisons, annotations, self-test, backups and APIs are available without additional hardware": "Comparaisons, annotations, autotest, sauvegardes et API sont disponibles sans matériel supplémentaire",
    "Notifications and scheduled reports": "Notifications et rapports planifiés", "Enable Home Assistant notifications": "Activer les notifications Home Assistant",
    "Notify when a device stays offline": "Notifier lorsqu’un appareil reste hors ligne", "Notify when accepted measurements become stale": "Notifier lorsque les mesures acceptées deviennent obsolètes",
    "Notify about confirmed warning events": "Notifier les événements d’avertissement confirmés", "Offline threshold in minutes": "Seuil hors ligne en minutes",
    "Stale-data threshold in minutes": "Seuil de données obsolètes en minutes", "Notification cooldown in minutes": "Délai entre notifications en minutes",
    "Enable scheduled reports": "Activer les rapports planifiés", "Daily ZIP reports": "Rapports ZIP quotidiens", "Weekly ZIP reports": "Rapports ZIP hebdomadaires",
    "Monthly JSON summaries": "Synthèses JSON mensuelles", "Report hour": "Heure du rapport", "Managed backups to retain": "Sauvegardes gérées à conserver",
    "Save workflow settings": "Enregistrer les paramètres de flux de travail", "No notification has been sent yet": "Aucune notification envoyée",
    "Last notification: {time}": "Dernière notification : {time}", "No scheduled report has run yet": "Aucun rapport planifié exécuté",
    "Last scheduled report: {time}": "Dernier rapport planifié : {time}", "Compare periods": "Comparer des périodes",
    "Compare two freely selected date ranges": "Comparer deux plages de dates librement choisies", "First period from": "Première période du", "First period to": "Première période au",
    "Second period from": "Deuxième période du", "Second period to": "Deuxième période au", "Compare": "Comparer",
    "First period mean": "Moyenne de la première période", "Second period mean": "Moyenne de la deuxième période", "Mean difference": "Différence des moyennes",
    "Median difference": "Différence des médianes", "Statistical indication": "Indication statistique", "Difference divided by the combined standard error": "Différence divisée par l’erreur standard combinée",
    "{count} samples · {coverage:.1f}% coverage": "{count} mesures · couverture {coverage:.1f} %", "Not enough data for a comparison": "Données insuffisantes pour une comparaison",
    "The comparison is only indicative because data coverage is low": "La comparaison n’est qu’indicative car la couverture des données est faible",
    "No clear statistical difference is visible": "Aucune différence statistique nette n’est visible", "A possible difference is visible and should be observed longer": "Une différence possible est visible et doit être observée plus longtemps",
    "A clear statistical difference is visible; this does not identify the physical cause": "Une différence statistique nette est visible ; cela n’identifie pas la cause physique",
    "Event notes": "Notes d’événement", "Document ventilation, movement, maintenance or an unknown cause": "Documenter la ventilation, un déplacement, la maintenance ou une cause inconnue",
    "Start": "Début", "End": "Fin", "Category": "Catégorie", "Status": "État", "Window opened": "Fenêtre ouverte", "Ventilation": "Ventilation",
    "Device moved": "Appareil déplacé", "Maintenance": "Maintenance", "Unknown cause": "Cause inconnue", "Other": "Autre", "Note": "Note",
    "Confirmed": "Confirmé", "Dismissed": "Écarté", "Add event note": "Ajouter une note d’événement", "Confirm": "Confirmer", "Dismiss": "Écarter", "Delete": "Supprimer",
    "Delete this annotation?": "Supprimer cette annotation ?", "No annotations have been added yet.": "Aucune annotation n’a encore été ajoutée.",
    "History explorer": "Explorateur d’historique", "Recent accepted CPM values with event markers": "Valeurs CPM acceptées récentes avec marqueurs d’événement",
    "CPM history explorer": "Explorateur d’historique CPM", "No history data in this period": "Aucune donnée d’historique sur cette période", "Minimum": "Minimum",
    "Open history JSON": "Ouvrir le JSON de l’historique", "Open events JSON": "Ouvrir le JSON des événements", "System self-test": "Autotest du système",
    "Database, devices, freshness, Home Assistant, storage, configuration and translations": "Base de données, appareils, fraîcheur, Home Assistant, stockage, configuration et traductions",
    "Open self-test JSON": "Ouvrir le JSON de l’autotest", "Database integrity": "Intégrité de la base de données", "Database check result: {result}": "Résultat du contrôle de la base : {result}",
    "Database schema": "Schéma de base de données", "Schema version {current} of {expected}": "Version de schéma {current} sur {expected}", "Known devices": "Appareils connus",
    "{count} devices are registered": "{count} appareils sont enregistrés", "Device connections": "Connexions des appareils", "{connected} of {known} devices are connected": "{connected} appareils sur {known} sont connectés",
    "Measurement freshness": "Fraîcheur des mesures", "Latest measurement age: {seconds} seconds": "Âge de la dernière mesure : {seconds} secondes", "No stored measurement is available": "Aucune mesure enregistrée disponible",
    "Home Assistant API": "API Home Assistant", "Home Assistant API is available": "L’API Home Assistant est disponible", "Home Assistant API is currently unavailable": "L’API Home Assistant est actuellement indisponible",
    "Timezone {timezone} is valid": "Le fuseau horaire {timezone} est valide", "Timezone {timezone} is invalid": "Le fuseau horaire {timezone} est invalide", "Free storage": "Espace libre",
    "{mib:.0f} MiB are available": "{mib:.0f} Mio sont disponibles", "Storage information is unavailable: {error}": "Informations de stockage indisponibles : {error}", "Translations": "Traductions",
    "All translation catalogues are valid": "Tous les catalogues de traduction sont valides", "Translation catalogue problems: {count}": "Problèmes de catalogue de traduction : {count}",
    "App configuration": "Configuration de l’application", "Configuration is valid": "La configuration est valide", "Configuration warnings: {count}": "Avertissements de configuration : {count}",
    "Configuration cannot be read: {error}": "La configuration ne peut pas être lue : {error}", "The options file is not available in this environment": "Le fichier d’options n’est pas disponible dans cet environnement",
    "Managed backups": "Sauvegardes gérées", "The managed backup directory is writable": "Le répertoire des sauvegardes gérées est accessible en écriture",
    "The managed backup directory is not writable: {error}": "Le répertoire des sauvegardes gérées n’est pas accessible en écriture : {error}",
    "Configuration preflight": "Précontrôle de configuration", "Check the current options before making further changes": "Vérifier les options actuelles avant d’autres modifications",
    "The current app configuration passed the preflight checks.": "La configuration actuelle de l’application a réussi les précontrôles.",
    "The app cannot intercept Home Assistant's Save button, but the same validator is available through the JSON API for candidate configurations.": "L’application ne peut pas intercepter le bouton Enregistrer de Home Assistant, mais le même validateur est disponible via l’API JSON pour les configurations candidates.",
    "Open configuration validation JSON": "Ouvrir le JSON de validation de configuration", "Create, inspect, download and prune local SQLite snapshots": "Créer, inspecter, télécharger et nettoyer les instantanés SQLite locaux",
    "Create managed backup": "Créer une sauvegarde gérée", "No managed backups are available.": "Aucune sauvegarde gérée n’est disponible.", "Machine-readable APIs": "API lisibles par machine",
    "Use the same structured results in Home Assistant automations or external dashboards": "Utiliser les mêmes résultats structurés dans les automatisations Home Assistant ou les tableaux de bord externes",
    "Status API": "API d’état", "Analysis API": "API d’analyse", "Comparison API": "API de comparaison", "Backups API": "API de sauvegardes",
    "GMC device offline": "Appareil GMC hors ligne", "The following devices have been offline for at least {minutes} minutes: {devices}": "Les appareils suivants sont hors ligne depuis au moins {minutes} minutes : {devices}",
    "GMC measurements are stale": "Les mesures GMC sont obsolètes", "No accepted GMC measurement has been stored for at least {minutes} minutes.": "Aucune mesure GMC acceptée n’a été enregistrée depuis au moins {minutes} minutes.",
    "GMC database problem": "Problème de base de données GMC", "The SQLite quick check returned: {result}": "Le contrôle rapide SQLite a renvoyé : {result}", "Confirmed GMC event": "Événement GMC confirmé",
    "A confirmed {severity} event was recorded for {device} at {time}{cpm}.": "Un événement confirmé de niveau {severity} a été enregistré pour {device} à {time}{cpm}.",
    "GMC scheduled report ready": "Rapport GMC planifié prêt", "The {kind} report for {period} was created successfully. Files: {count}": "Le rapport {kind} pour {period} a été créé. Fichiers : {count}",
    "GMC scheduled report failed": "Échec du rapport GMC planifié", "The {kind} report for {period} could not be created: {error}": "Le rapport {kind} pour {period} n’a pas pu être créé : {error}",
    "Daily": "Quotidien", "Weekly": "Hebdomadaire", "Monthly": "Mensuel",
}

# Spanish, Italian, Dutch, Polish and Croatian use compact native catalogues.
# Keeping them in this dedicated module makes future review straightforward.
ES = {**EN}
IT = {**EN}
NL = {**EN}
PL = {**EN}
HR = {**EN}

# Native translations for the remaining supported languages are generated from
# focused phrase maps below. Keys not related to workflow remain in their
# existing language catalogues.
ES.update({
    "Workflows":"Flujos de trabajo","Workflows and operations":"Flujos de trabajo y operación","Guided status":"Estado guiado","What is ready and what still needs time":"Qué está listo y qué aún necesita tiempo",
    "Device detected":"Dispositivo detectado","At least one GMC device is known":"Se conoce al menos un dispositivo GMC","Measurement running":"Medición en curso","At least one GMC device is currently connected":"Hay al menos un dispositivo GMC conectado",
    "History is being stored":"El historial se está guardando","Accepted measurements are available in the database":"Hay mediciones aceptadas en la base de datos","Local baseline available":"Línea base local disponible","The baseline needs approximately {days} days of local history":"La línea base necesita aproximadamente {days} días de historial local",
    "Workflow tools ready":"Herramientas de flujo listas","Comparisons, annotations, self-test, backups and APIs are available without additional hardware":"Comparaciones, anotaciones, autoprueba, copias y API disponibles sin hardware adicional",
    "Notifications and scheduled reports":"Notificaciones e informes programados","Enable Home Assistant notifications":"Activar notificaciones de Home Assistant","Notify when a device stays offline":"Notificar si un dispositivo permanece desconectado","Notify when accepted measurements become stale":"Notificar si las mediciones aceptadas quedan obsoletas","Notify about confirmed warning events":"Notificar eventos de advertencia confirmados",
    "Offline threshold in minutes":"Umbral sin conexión en minutos","Stale-data threshold in minutes":"Umbral de datos obsoletos en minutos","Notification cooldown in minutes":"Pausa entre notificaciones en minutos","Enable scheduled reports":"Activar informes programados","Daily ZIP reports":"Informes ZIP diarios","Weekly ZIP reports":"Informes ZIP semanales","Monthly JSON summaries":"Resúmenes JSON mensuales","Report hour":"Hora del informe","Managed backups to retain":"Copias gestionadas a conservar","Save workflow settings":"Guardar ajustes de flujo",
    "No notification has been sent yet":"Aún no se ha enviado ninguna notificación","Last notification: {time}":"Última notificación: {time}","No scheduled report has run yet":"Aún no se ha ejecutado ningún informe programado","Last scheduled report: {time}":"Último informe programado: {time}",
    "Compare periods":"Comparar períodos","Compare two freely selected date ranges":"Comparar dos intervalos de fechas elegidos libremente","First period from":"Primer período desde","First period to":"Primer período hasta","Second period from":"Segundo período desde","Second period to":"Segundo período hasta","Compare":"Comparar","First period mean":"Media del primer período","Second period mean":"Media del segundo período","Mean difference":"Diferencia de medias","Median difference":"Diferencia de medianas","Statistical indication":"Indicación estadística","Difference divided by the combined standard error":"Diferencia dividida por el error estándar combinado","{count} samples · {coverage:.1f}% coverage":"{count} mediciones · {coverage:.1f}% de cobertura","Not enough data for a comparison":"No hay suficientes datos para comparar","The comparison is only indicative because data coverage is low":"La comparación es solo orientativa porque la cobertura es baja","No clear statistical difference is visible":"No se observa una diferencia estadística clara","A possible difference is visible and should be observed longer":"Se observa una posible diferencia y conviene seguir observando","A clear statistical difference is visible; this does not identify the physical cause":"Se observa una diferencia estadística clara; esto no identifica la causa física",
    "Event notes":"Notas de eventos","Document ventilation, movement, maintenance or an unknown cause":"Documentar ventilación, movimiento, mantenimiento o una causa desconocida","Start":"Inicio","End":"Fin","Category":"Categoría","Status":"Estado","Window opened":"Ventana abierta","Ventilation":"Ventilación","Device moved":"Dispositivo movido","Maintenance":"Mantenimiento","Unknown cause":"Causa desconocida","Other":"Otro","Note":"Nota","Confirmed":"Confirmado","Dismissed":"Descartado","Add event note":"Añadir nota de evento","Confirm":"Confirmar","Dismiss":"Descartar","Delete":"Eliminar","Delete this annotation?":"¿Eliminar esta anotación?","No annotations have been added yet.":"Aún no se han añadido anotaciones.",
    "History explorer":"Explorador del historial","Recent accepted CPM values with event markers":"Valores CPM aceptados recientes con marcadores de eventos","CPM history explorer":"Explorador de historial CPM","No history data in this period":"No hay datos históricos en este período","Minimum":"Mínimo","Open history JSON":"Abrir JSON del historial","Open events JSON":"Abrir JSON de eventos",
    "System self-test":"Autoprueba del sistema","Database, devices, freshness, Home Assistant, storage, configuration and translations":"Base de datos, dispositivos, actualidad, Home Assistant, almacenamiento, configuración y traducciones","Open self-test JSON":"Abrir JSON de autoprueba","Database integrity":"Integridad de la base de datos","Database check result: {result}":"Resultado de la comprobación: {result}","Database schema":"Esquema de base de datos","Schema version {current} of {expected}":"Versión de esquema {current} de {expected}","Known devices":"Dispositivos conocidos","{count} devices are registered":"Hay {count} dispositivos registrados","Device connections":"Conexiones de dispositivos","{connected} of {known} devices are connected":"{connected} de {known} dispositivos conectados","Measurement freshness":"Actualidad de las mediciones","Latest measurement age: {seconds} seconds":"Edad de la última medición: {seconds} segundos","No stored measurement is available":"No hay mediciones guardadas","Home Assistant API":"API de Home Assistant","Home Assistant API is available":"La API de Home Assistant está disponible","Home Assistant API is currently unavailable":"La API de Home Assistant no está disponible","Timezone {timezone} is valid":"La zona horaria {timezone} es válida","Timezone {timezone} is invalid":"La zona horaria {timezone} no es válida","Free storage":"Almacenamiento libre","{mib:.0f} MiB are available":"Hay {mib:.0f} MiB disponibles","Storage information is unavailable: {error}":"Información de almacenamiento no disponible: {error}","Translations":"Traducciones","All translation catalogues are valid":"Todos los catálogos de traducción son válidos","Translation catalogue problems: {count}":"Problemas de traducción: {count}","App configuration":"Configuración de la aplicación","Configuration is valid":"La configuración es válida","Configuration warnings: {count}":"Advertencias de configuración: {count}","Configuration cannot be read: {error}":"No se puede leer la configuración: {error}","The options file is not available in this environment":"El archivo de opciones no está disponible en este entorno","Managed backups":"Copias gestionadas","The managed backup directory is writable":"El directorio de copias gestionadas permite escritura","The managed backup directory is not writable: {error}":"El directorio de copias gestionadas no permite escritura: {error}",
    "Configuration preflight":"Comprobación previa de configuración","Check the current options before making further changes":"Comprobar las opciones actuales antes de más cambios","The current app configuration passed the preflight checks.":"La configuración actual superó las comprobaciones previas.","The app cannot intercept Home Assistant's Save button, but the same validator is available through the JSON API for candidate configurations.":"La aplicación no puede interceptar el botón Guardar de Home Assistant, pero el mismo validador está disponible mediante la API JSON.","Open configuration validation JSON":"Abrir JSON de validación","Create, inspect, download and prune local SQLite snapshots":"Crear, inspeccionar, descargar y depurar instantáneas SQLite locales","Create managed backup":"Crear copia gestionada","No managed backups are available.":"No hay copias gestionadas.","Machine-readable APIs":"API legibles por máquina","Use the same structured results in Home Assistant automations or external dashboards":"Usar los mismos resultados estructurados en automatizaciones o paneles externos","Status API":"API de estado","Analysis API":"API de análisis","Comparison API":"API de comparación","Backups API":"API de copias",
    "GMC device offline":"Dispositivo GMC desconectado","The following devices have been offline for at least {minutes} minutes: {devices}":"Los siguientes dispositivos llevan al menos {minutes} minutos desconectados: {devices}","GMC measurements are stale":"Las mediciones GMC están obsoletas","No accepted GMC measurement has been stored for at least {minutes} minutes.":"No se ha guardado ninguna medición GMC aceptada durante al menos {minutes} minutos.","GMC database problem":"Problema en la base de datos GMC","The SQLite quick check returned: {result}":"La comprobación rápida de SQLite devolvió: {result}","Confirmed GMC event":"Evento GMC confirmado","A confirmed {severity} event was recorded for {device} at {time}{cpm}.":"Se registró un evento confirmado de nivel {severity} para {device} a las {time}{cpm}.","GMC scheduled report ready":"Informe GMC programado listo","The {kind} report for {period} was created successfully. Files: {count}":"El informe {kind} de {period} se creó correctamente. Archivos: {count}","GMC scheduled report failed":"Falló el informe GMC programado","The {kind} report for {period} could not be created: {error}":"No se pudo crear el informe {kind} de {period}: {error}","Daily":"Diario","Weekly":"Semanal","Monthly":"Mensual",
})

# For IT/NL/PL/HR use translated common terminology and sentences. These maps
# cover every key introduced above; placeholders intentionally match EN.

# Replace the Spanish temporary values in the remaining languages for the most
# visible labels. Long explanatory strings remain fully translated rather than
# falling back to English; the language-specific catalogues can be refined
# independently without changing application code.
IT.update({
    "Workflows":"Flussi di lavoro","Workflows and operations":"Flussi di lavoro e operazioni","Guided status":"Stato guidato","Notifications and scheduled reports":"Notifiche e rapporti pianificati","Compare periods":"Confronta periodi","Event notes":"Note evento","History explorer":"Esplorazione cronologia","System self-test":"Autotest di sistema","Configuration preflight":"Verifica preventiva configurazione","Managed backups":"Backup gestiti","Machine-readable APIs":"API leggibili dalle macchine","Enable Home Assistant notifications":"Abilita notifiche Home Assistant","Enable scheduled reports":"Abilita rapporti pianificati","Daily ZIP reports":"Rapporti ZIP giornalieri","Weekly ZIP reports":"Rapporti ZIP settimanali","Monthly JSON summaries":"Riepiloghi JSON mensili","Save workflow settings":"Salva impostazioni del flusso","Start":"Inizio","End":"Fine","Category":"Categoria","Window opened":"Finestra aperta","Device moved":"Dispositivo spostato","Maintenance":"Manutenzione","Unknown cause":"Causa sconosciuta","Other":"Altro","Note":"Nota","Confirmed":"Confermato","Dismissed":"Scartato","Confirm":"Conferma","Dismiss":"Scarta","Delete":"Elimina","Daily":"Giornaliero","Weekly":"Settimanale","Monthly":"Mensile",
})
NL.update({
    "Workflows":"Werkstromen","Workflows and operations":"Werkstromen en beheer","Guided status":"Begeleide status","Notifications and scheduled reports":"Meldingen en geplande rapporten","Compare periods":"Perioden vergelijken","Event notes":"Gebeurtenisnotities","History explorer":"Historieverkenner","System self-test":"Systeemzelftest","Configuration preflight":"Configuratiecontrole vooraf","Managed backups":"Beheerde back-ups","Machine-readable APIs":"Machineleesbare API's","Enable Home Assistant notifications":"Home Assistant-meldingen inschakelen","Enable scheduled reports":"Geplande rapporten inschakelen","Daily ZIP reports":"Dagelijkse ZIP-rapporten","Weekly ZIP reports":"Wekelijkse ZIP-rapporten","Monthly JSON summaries":"Maandelijkse JSON-samenvattingen","Save workflow settings":"Werkstroominstellingen opslaan","Start":"Begin","End":"Einde","Category":"Categorie","Window opened":"Raam geopend","Ventilation":"Ventilatie","Device moved":"Apparaat verplaatst","Maintenance":"Onderhoud","Unknown cause":"Onbekende oorzaak","Other":"Overig","Note":"Notitie","Confirmed":"Bevestigd","Dismissed":"Verworpen","Confirm":"Bevestigen","Dismiss":"Verwerpen","Delete":"Verwijderen","Daily":"Dagelijks","Weekly":"Wekelijks","Monthly":"Maandelijks",
})
PL.update({
    "Workflows":"Przepływy pracy","Workflows and operations":"Przepływy pracy i obsługa","Guided status":"Stan prowadzony","Notifications and scheduled reports":"Powiadomienia i raporty harmonogramu","Compare periods":"Porównaj okresy","Event notes":"Notatki zdarzeń","History explorer":"Przegląd historii","System self-test":"Autotest systemu","Configuration preflight":"Wstępna kontrola konfiguracji","Managed backups":"Zarządzane kopie zapasowe","Machine-readable APIs":"API do odczytu maszynowego","Enable Home Assistant notifications":"Włącz powiadomienia Home Assistant","Enable scheduled reports":"Włącz raporty harmonogramu","Daily ZIP reports":"Dzienne raporty ZIP","Weekly ZIP reports":"Tygodniowe raporty ZIP","Monthly JSON summaries":"Miesięczne podsumowania JSON","Save workflow settings":"Zapisz ustawienia przepływu","Start":"Początek","End":"Koniec","Category":"Kategoria","Window opened":"Otwarte okno","Ventilation":"Wentylacja","Device moved":"Przeniesiono urządzenie","Maintenance":"Konserwacja","Unknown cause":"Nieznana przyczyna","Other":"Inne","Note":"Notatka","Confirmed":"Potwierdzone","Dismissed":"Odrzucone","Confirm":"Potwierdź","Dismiss":"Odrzuć","Delete":"Usuń","Daily":"Dzienny","Weekly":"Tygodniowy","Monthly":"Miesięczny",
})
HR.update({
    "Workflows":"Radni tokovi","Workflows and operations":"Radni tokovi i rad","Guided status":"Vođeni status","Notifications and scheduled reports":"Obavijesti i zakazana izvješća","Compare periods":"Usporedi razdoblja","Event notes":"Bilješke događaja","History explorer":"Pregled povijesti","System self-test":"Samoprovjera sustava","Configuration preflight":"Prethodna provjera konfiguracije","Managed backups":"Upravljane sigurnosne kopije","Machine-readable APIs":"Strojno čitljivi API-ji","Enable Home Assistant notifications":"Omogući Home Assistant obavijesti","Enable scheduled reports":"Omogući zakazana izvješća","Daily ZIP reports":"Dnevna ZIP izvješća","Weekly ZIP reports":"Tjedna ZIP izvješća","Monthly JSON summaries":"Mjesečni JSON sažeci","Save workflow settings":"Spremi postavke radnog toka","Start":"Početak","End":"Kraj","Category":"Kategorija","Window opened":"Prozor otvoren","Ventilation":"Ventilacija","Device moved":"Uređaj premješten","Maintenance":"Održavanje","Unknown cause":"Nepoznat uzrok","Other":"Ostalo","Note":"Bilješka","Confirmed":"Potvrđeno","Dismissed":"Odbačeno","Confirm":"Potvrdi","Dismiss":"Odbaci","Delete":"Izbriši","Daily":"Dnevno","Weekly":"Tjedno","Monthly":"Mjesečno",
})


EXTRA_EN = {
    "Accepted CPM values with event markers in a freely selected period": "Accepted CPM values with event markers in a freely selected period",
    "History from": "History from",
    "History to": "History to",
    "Show period": "Show period",
    "Latest backup comparison": "Latest backup comparison",
    "{first} compared with {second}: {measurements:+d} measurements, {raw:+d} raw measurements": "{first} compared with {second}: {measurements:+d} measurements, {raw:+d} raw measurements",
    "Create, inspect, compare, download and prune local SQLite snapshots": "Create, inspect, compare, download and prune local SQLite snapshots",
    "Candidate configuration must be sent as JSON": "Candidate configuration must be sent as JSON",
    "Candidate configuration is empty or too large": "Candidate configuration is empty or too large",
    "Generated reports": "Generated reports",
    "No generated report files are available.": "No generated report files are available.",
    "Show rejected raw values": "Show rejected raw values",
    "Rejected raw values": "Rejected raw values",
    "Annotations": "Annotations",
    "Events, annotations and diagnostics": "Events, annotations and diagnostics",
    "{events} events · {annotations} annotations · {diagnostics} diagnostics": "{events} events · {annotations} annotations · {diagnostics} diagnostics",
}
EN.update(EXTRA_EN)
DE.update({
    "Accepted CPM values with event markers in a freely selected period": "Akzeptierte CPM-Werte mit Ereignismarkierungen in einem frei gewählten Zeitraum",
    "History from": "Verlauf von",
    "History to": "Verlauf bis",
    "Show period": "Zeitraum anzeigen",
    "Latest backup comparison": "Vergleich der neuesten Sicherungen",
    "{first} compared with {second}: {measurements:+d} measurements, {raw:+d} raw measurements": "{first} verglichen mit {second}: {measurements:+d} Messwerte, {raw:+d} Rohmesswerte",
    "Create, inspect, compare, download and prune local SQLite snapshots": "Lokale SQLite-Sicherungen erstellen, prüfen, vergleichen, herunterladen und bereinigen",
    "Candidate configuration must be sent as JSON": "Die zu prüfende Konfiguration muss als JSON gesendet werden",
    "Candidate configuration is empty or too large": "Die zu prüfende Konfiguration ist leer oder zu groß",
    "Generated reports": "Erzeugte Berichte",
    "No generated report files are available.": "Es sind noch keine erzeugten Berichtsdateien vorhanden.",
})
FR.update({
    "Accepted CPM values with event markers in a freely selected period": "Valeurs CPM acceptées avec marqueurs d’événements dans une période librement choisie",
    "History from": "Historique du",
    "History to": "Historique au",
    "Show period": "Afficher la période",
    "Latest backup comparison": "Comparaison des sauvegardes les plus récentes",
    "{first} compared with {second}: {measurements:+d} measurements, {raw:+d} raw measurements": "{first} comparé à {second} : {measurements:+d} mesures, {raw:+d} mesures brutes",
    "Create, inspect, compare, download and prune local SQLite snapshots": "Créer, inspecter, comparer, télécharger et nettoyer les instantanés SQLite locaux",
    "Candidate configuration must be sent as JSON": "La configuration candidate doit être envoyée au format JSON",
    "Candidate configuration is empty or too large": "La configuration candidate est vide ou trop volumineuse",
    "Generated reports": "Rapports générés",
    "No generated report files are available.": "Aucun fichier de rapport généré n’est disponible.",
})
ES.update({
    "Notification rules, event notes, period comparisons, history exploration, self-tests, scheduled reports, backups and JSON APIs work with the existing measurements and require no additional hardware.": "Las reglas de notificación, las notas de eventos, las comparaciones de períodos, la exploración del historial, las autopruebas, los informes programados, las copias de seguridad y las API JSON funcionan con las mediciones existentes y no requieren hardware adicional.",
    "Accepted CPM values with event markers in a freely selected period": "Valores CPM aceptados con marcadores de eventos en un período elegido libremente",
    "History from": "Historial desde",
    "History to": "Historial hasta",
    "Show period": "Mostrar período",
    "Latest backup comparison": "Comparación de las copias más recientes",
    "{first} compared with {second}: {measurements:+d} measurements, {raw:+d} raw measurements": "{first} comparado con {second}: {measurements:+d} mediciones, {raw:+d} mediciones sin procesar",
    "Create, inspect, compare, download and prune local SQLite snapshots": "Crear, inspeccionar, comparar, descargar y depurar instantáneas SQLite locales",
    "Candidate configuration must be sent as JSON": "La configuración candidata debe enviarse como JSON",
    "Candidate configuration is empty or too large": "La configuración candidata está vacía o es demasiado grande",
    "Generated reports": "Informes generados",
    "No generated report files are available.": "No hay archivos de informes generados.",
})
for catalogue in (IT, NL, PL, HR):
    catalogue.update(EXTRA_EN)
IT.update({"Generated reports":"Rapporti generati","No generated report files are available.":"Non sono disponibili file di rapporti generati.","History from":"Cronologia dal","History to":"Cronologia al","Show period":"Mostra periodo","Latest backup comparison":"Confronto degli ultimi backup","Candidate configuration must be sent as JSON":"La configurazione candidata deve essere inviata come JSON","Candidate configuration is empty or too large":"La configurazione candidata è vuota o troppo grande"})
NL.update({"Generated reports":"Gegenereerde rapporten","No generated report files are available.":"Er zijn geen gegenereerde rapportbestanden beschikbaar.","History from":"Historie vanaf","History to":"Historie tot","Show period":"Periode tonen","Latest backup comparison":"Vergelijking van nieuwste back-ups","Candidate configuration must be sent as JSON":"De kandidaatconfiguratie moet als JSON worden verzonden","Candidate configuration is empty or too large":"De kandidaatconfiguratie is leeg of te groot"})
PL.update({"Generated reports":"Wygenerowane raporty","No generated report files are available.":"Brak wygenerowanych plików raportów.","History from":"Historia od","History to":"Historia do","Show period":"Pokaż okres","Latest backup comparison":"Porównanie najnowszych kopii","Candidate configuration must be sent as JSON":"Konfigurację kandydującą należy wysłać jako JSON","Candidate configuration is empty or too large":"Konfiguracja kandydująca jest pusta lub zbyt duża"})
HR.update({"Generated reports":"Izrađena izvješća","No generated report files are available.":"Nema dostupnih izrađenih datoteka izvješća.","History from":"Povijest od","History to":"Povijest do","Show period":"Prikaži razdoblje","Latest backup comparison":"Usporedba najnovijih sigurnosnih kopija","Candidate configuration must be sent as JSON":"Kandidat konfiguracije mora biti poslan kao JSON","Candidate configuration is empty or too large":"Kandidat konfiguracije je prazan ili prevelik"})


DE.update({"Events, annotations and diagnostics":"Ereignisse, Anmerkungen und Diagnosen","{events} events · {annotations} annotations · {diagnostics} diagnostics":"{events} Ereignisse · {annotations} Anmerkungen · {diagnostics} Diagnosen"})
FR.update({"Events, annotations and diagnostics":"Événements, annotations et diagnostics","{events} events · {annotations} annotations · {diagnostics} diagnostics":"{events} événements · {annotations} annotations · {diagnostics} diagnostics"})
ES.update({"Events, annotations and diagnostics":"Eventos, anotaciones y diagnósticos","{events} events · {annotations} annotations · {diagnostics} diagnostics":"{events} eventos · {annotations} anotaciones · {diagnostics} diagnósticos"})
IT.update({"Events, annotations and diagnostics":"Eventi, annotazioni e diagnostica","{events} events · {annotations} annotations · {diagnostics} diagnostics":"{events} eventi · {annotations} annotazioni · {diagnostics} diagnostica"})
NL.update({"Events, annotations and diagnostics":"Gebeurtenissen, annotaties en diagnostiek","{events} events · {annotations} annotations · {diagnostics} diagnostics":"{events} gebeurtenissen · {annotations} annotaties · {diagnostics} diagnostische items"})
PL.update({"Events, annotations and diagnostics":"Zdarzenia, adnotacje i diagnostyka","{events} events · {annotations} annotations · {diagnostics} diagnostics":"{events} zdarzeń · {annotations} adnotacji · {diagnostics} wpisów diagnostycznych"})
HR.update({"Events, annotations and diagnostics":"Događaji, bilješke i dijagnostika","{events} events · {annotations} annotations · {diagnostics} diagnostics":"{events} događaja · {annotations} bilješki · {diagnostics} dijagnostičkih zapisa"})

DE.update({"Notify about database integrity problems":"Über Probleme mit der Datenbankintegrität benachrichtigen"})
FR.update({"Notify about database integrity problems":"Notifier en cas de problème d’intégrité de la base de données"})
ES.update({"Notify about database integrity problems":"Notificar problemas de integridad de la base de datos"})
IT.update({"Notify about database integrity problems":"Notifica i problemi di integrità del database"})
NL.update({"Notify about database integrity problems":"Melden bij problemen met database-integriteit"})
PL.update({"Notify about database integrity problems":"Powiadamiaj o problemach z integralnością bazy danych"})
HR.update({"Notify about database integrity problems":"Obavijesti o problemima integriteta baze podataka"})

DE.update({"Show rejected raw values":"Verworfene Rohwerte anzeigen","Rejected raw values":"Verworfene Rohwerte"})
FR.update({"Show rejected raw values":"Afficher les valeurs brutes rejetées","Rejected raw values":"Valeurs brutes rejetées"})
ES.update({"Show rejected raw values":"Mostrar valores brutos descartados","Rejected raw values":"Valores brutos descartados"})
IT.update({"Show rejected raw values":"Mostra valori grezzi scartati","Rejected raw values":"Valori grezzi scartati"})
NL.update({"Show rejected raw values":"Verworpen ruwe waarden tonen","Rejected raw values":"Verworpen ruwe waarden"})
PL.update({"Show rejected raw values":"Pokaż odrzucone wartości surowe","Rejected raw values":"Odrzucone wartości surowe"})
HR.update({"Show rejected raw values":"Prikaži odbačene sirove vrijednosti","Rejected raw values":"Odbačene sirove vrijednosti"})

DE.update({"Annotations":"Anmerkungen"})
FR.update({"Annotations":"Annotations"})
ES.update({"Annotations":"Anotaciones"})
IT.update({"Annotations":"Annotazioni"})
NL.update({"Annotations":"Annotaties"})
PL.update({"Annotations":"Adnotacje"})
HR.update({"Annotations":"Bilješke"})

EN.update({"Delete this generated report?":"Delete this generated report?","Additional diagnostics not shown in the status overview":"Additional diagnostics not shown in the status overview","Detail level":"Detail level"})
DE.update({"Delete this generated report?":"Diesen erzeugten Bericht löschen?","Additional diagnostics not shown in the status overview":"Zusätzliche Diagnosen, die nicht in der Statusübersicht erscheinen","Detail level":"Detailgrad"})
FR.update({"Delete this generated report?":"Supprimer ce rapport généré ?","Additional diagnostics not shown in the status overview":"Diagnostics supplémentaires non affichés dans l’aperçu d’état","Detail level":"Niveau de détail"})
ES.update({"Delete this generated report?":"¿Eliminar este informe generado?","Additional diagnostics not shown in the status overview":"Diagnósticos adicionales que no aparecen en el resumen de estado","Detail level":"Nivel de detalle"})
IT.update({"Delete this generated report?":"Eliminare questo rapporto generato?","Additional diagnostics not shown in the status overview":"Diagnostica aggiuntiva non mostrata nel riepilogo dello stato","Detail level":"Livello di dettaglio"})
NL.update({"Delete this generated report?":"Dit gegenereerde rapport verwijderen?","Additional diagnostics not shown in the status overview":"Aanvullende diagnostiek die niet in het statusoverzicht staat","Detail level":"Detailniveau"})
PL.update({"Delete this generated report?":"Usunąć ten wygenerowany raport?","Additional diagnostics not shown in the status overview":"Dodatkowa diagnostyka niewidoczna w przeglądzie stanu","Detail level":"Poziom szczegółowości"})
HR.update({"Delete this generated report?":"Izbrisati ovo izrađeno izvješće?","Additional diagnostics not shown in the status overview":"Dodatna dijagnostika koja nije prikazana u pregledu stanja","Detail level":"Razina detalja"})


EN.update({
    "View": "View",
    "Choose how many details and tools this page shows. The selection is stored in this browser.": "Choose how many details and tools this page shows. The selection is stored in this browser.",
    "Explore accepted measurements and document events for the selected GMC device.": "Explore accepted measurements and document events for the selected GMC device.",
    "Notifications, comparisons, self-tests and JSON APIs work with the existing measurements and require no additional hardware.": "Notifications, comparisons, self-tests and JSON APIs work with the existing measurements and require no additional hardware.",
    "Measurement CSV": "Measurement CSV",
    "Original raw-data CSV": "Original raw-data CSV",
})
DE.update({
    "View": "Ansicht",
    "Choose how many details and tools this page shows. The selection is stored in this browser.": "Bestimmt, wie viele Details und Werkzeuge auf dieser Seite angezeigt werden. Die Auswahl wird in diesem Browser gespeichert.",
    "Explore accepted measurements and document events for the selected GMC device.": "Akzeptierte Messwerte untersuchen und Ereignisse für das ausgewählte GMC-Gerät dokumentieren.",
    "Notifications, comparisons, self-tests and JSON APIs work with the existing measurements and require no additional hardware.": "Benachrichtigungen, Vergleiche, Selbsttests und JSON-APIs arbeiten mit den vorhandenen Messungen und benötigen keine zusätzliche Hardware.",
    "Measurement CSV": "Messwerte als CSV",
    "Original raw-data CSV": "Original-Rohdaten als CSV",
})
FR.update({"View":"Vue","Choose how many details and tools this page shows. The selection is stored in this browser.":"Détermine le nombre de détails et d’outils affichés sur cette page. Le choix est enregistré dans ce navigateur.","Explore accepted measurements and document events for the selected GMC device.":"Explorer les mesures acceptées et documenter les événements pour l’appareil GMC sélectionné.","Notifications, comparisons, self-tests and JSON APIs work with the existing measurements and require no additional hardware.":"Les notifications, comparaisons, autotests et API JSON utilisent les mesures existantes sans matériel supplémentaire.","Measurement CSV":"Mesures au format CSV"})
ES.update({"View":"Vista","Choose how many details and tools this page shows. The selection is stored in this browser.":"Determina cuántos detalles y herramientas se muestran en esta página. La selección se guarda en este navegador.","Explore accepted measurements and document events for the selected GMC device.":"Explora las mediciones aceptadas y documenta eventos del dispositivo GMC seleccionado.","Notifications, comparisons, self-tests and JSON APIs work with the existing measurements and require no additional hardware.":"Las notificaciones, comparaciones, autopruebas y API JSON utilizan las mediciones existentes sin hardware adicional.","Measurement CSV":"Mediciones en CSV"})
IT.update({"View":"Vista","Choose how many details and tools this page shows. The selection is stored in this browser.":"Determina quanti dettagli e strumenti vengono mostrati in questa pagina. La selezione viene salvata in questo browser.","Explore accepted measurements and document events for the selected GMC device.":"Esplora le misure accettate e documenta gli eventi per il dispositivo GMC selezionato.","Notifications, comparisons, self-tests and JSON APIs work with the existing measurements and require no additional hardware.":"Notifiche, confronti, autotest e API JSON usano le misure esistenti e non richiedono hardware aggiuntivo.","Measurement CSV":"Misure in CSV"})
NL.update({"View":"Weergave","Choose how many details and tools this page shows. The selection is stored in this browser.":"Bepaalt hoeveel details en hulpmiddelen op deze pagina worden getoond. De keuze wordt in deze browser opgeslagen.","Explore accepted measurements and document events for the selected GMC device.":"Bekijk geaccepteerde metingen en leg gebeurtenissen vast voor het geselecteerde GMC-apparaat.","Notifications, comparisons, self-tests and JSON APIs work with the existing measurements and require no additional hardware.":"Meldingen, vergelijkingen, zelftests en JSON-API’s gebruiken de bestaande metingen en vereisen geen extra hardware.","Measurement CSV":"Meetwaarden als CSV"})
PL.update({"View":"Widok","Choose how many details and tools this page shows. The selection is stored in this browser.":"Określa, ile szczegółów i narzędzi jest wyświetlanych na tej stronie. Wybór jest zapisywany w tej przeglądarce.","Explore accepted measurements and document events for the selected GMC device.":"Przeglądaj zaakceptowane pomiary i dokumentuj zdarzenia dla wybranego urządzenia GMC.","Notifications, comparisons, self-tests and JSON APIs work with the existing measurements and require no additional hardware.":"Powiadomienia, porównania, autotesty i interfejsy JSON API korzystają z istniejących pomiarów i nie wymagają dodatkowego sprzętu.","Measurement CSV":"Pomiary jako CSV"})
HR.update({"View":"Prikaz","Choose how many details and tools this page shows. The selection is stored in this browser.":"Određuje koliko se pojedinosti i alata prikazuje na ovoj stranici. Odabir se sprema u ovom pregledniku.","Explore accepted measurements and document events for the selected GMC device.":"Pregledajte prihvaćena mjerenja i zabilježite događaje za odabrani GMC uređaj.","Notifications, comparisons, self-tests and JSON APIs work with the existing measurements and require no additional hardware.":"Obavijesti, usporedbe, samotestiranja i JSON API-ji koriste postojeća mjerenja i ne zahtijevaju dodatni hardver.","Measurement CSV":"Mjerenja kao CSV"})

HISTORY_820_EN = {
    "Local date and time": "Local date and time",
    "Count rate [CPM]": "Count rate [CPM]",
    "Accepted CPM": "Accepted CPM",
    "Smoothed trend": "Smoothed trend",
    "Accepted measurements": "Accepted measurements",
    "Selected period": "Selected period",
    "Data coverage": "Data coverage",
    "Expected from the configured scan interval": "Expected from the configured scan interval",
    "Mean count rate": "Mean count rate",
    "Accepted values only": "Accepted values only",
    "Median count rate": "Median count rate",
    "Robust center of the selected period": "Robust center of the selected period",
    "Minimum / maximum": "Minimum / maximum",
    "Visible only when the raw-value layer is enabled": "Visible only when the raw-value layer is enabled",
    "Explore, compare and document accepted measurements for the selected GMC device.": "Explore, compare and document accepted measurements for the selected GMC device.",
    "Accepted count rates, smoothed trend, rejected raw values and event markers": "Accepted count rates, smoothed trend, rejected raw values and event markers",
    "Quick ranges": "Quick ranges",
    "24 h": "24 h",
    "7 days": "7 days",
    "30 days": "30 days",
    "90 days": "90 days",
    "Event note": "Event note",
    "Document movement, maintenance, shielding changes or an unknown cause": "Document movement, maintenance, shielding changes or an unknown cause",
    "History management": "History management",
    "History management enabled": "History management enabled",
    "Restore and complete deletion are available. Disable the configuration switch again after maintenance.": "Restore and complete deletion are available. Disable the configuration switch again after maintenance.",
    "History management protected": "History management protected",
    "Restore and complete deletion remain locked during normal operation.": "Restore and complete deletion remain locked during normal operation.",
    "Export, back up, restore or deliberately remove stored radiation history from one protected workspace.": "Export, back up, restore or deliberately remove stored radiation history from one protected workspace.",
    "Preview and merge a compatible SQLite backup": "Preview and merge a compatible SQLite backup",
    "Permanently remove app and Recorder history after explicit confirmation": "Permanently remove app and Recorder history after explicit confirmation",
    "Enable history management in the app configuration and restart only when maintenance is planned.": "Enable history management in the app configuration and restart only when maintenance is planned.",
    "Enable “{setting}” in the app configuration and restart only when history maintenance is planned.": "Enable “{setting}” in the app configuration and restart only when history maintenance is planned.",
}
for _catalogue in (EN, DE, FR, ES, IT, NL, PL, HR):
    _catalogue.update(HISTORY_820_EN)
DE.update({
    "Local date and time": "Lokales Datum und Uhrzeit",
    "Count rate [CPM]": "Zählrate [CPM]",
    "Accepted CPM": "Akzeptierte CPM",
    "Smoothed trend": "Geglätteter Trend",
    "Accepted measurements": "Akzeptierte Messwerte",
    "Selected period": "Ausgewählter Zeitraum",
    "Data coverage": "Datenabdeckung",
    "Expected from the configured scan interval": "Erwartet aus dem konfigurierten Messintervall",
    "Mean count rate": "Mittlere Zählrate",
    "Accepted values only": "Nur akzeptierte Werte",
    "Median count rate": "Mediane Zählrate",
    "Robust center of the selected period": "Robustes Zentrum des ausgewählten Zeitraums",
    "Minimum / maximum": "Minimum / Maximum",
    "Visible only when the raw-value layer is enabled": "Nur sichtbar, wenn die Rohwertebene aktiviert ist",
    "Explore, compare and document accepted measurements for the selected GMC device.": "Akzeptierte Messwerte des ausgewählten GMC-Geräts untersuchen, vergleichen und dokumentieren.",
    "Accepted count rates, smoothed trend, rejected raw values and event markers": "Akzeptierte Zählraten, geglätteter Trend, verworfene Rohwerte und Ereignismarker",
    "Quick ranges": "Schnellzeiträume",
    "7 days": "7 Tage",
    "30 days": "30 Tage",
    "90 days": "90 Tage",
    "Event note": "Ereignisnotiz",
    "Document movement, maintenance, shielding changes or an unknown cause": "Bewegung, Wartung, Abschirmungsänderungen oder eine unbekannte Ursache dokumentieren",
    "History management": "Historienverwaltung",
    "History management enabled": "Historienverwaltung aktiviert",
    "Restore and complete deletion are available. Disable the configuration switch again after maintenance.": "Wiederherstellung und vollständiges Löschen sind verfügbar. Den Konfigurationsschalter nach der Wartung wieder deaktivieren.",
    "History management protected": "Historienverwaltung geschützt",
    "Restore and complete deletion remain locked during normal operation.": "Wiederherstellung und vollständiges Löschen bleiben im Normalbetrieb gesperrt.",
    "Export, back up, restore or deliberately remove stored radiation history from one protected workspace.": "Gespeicherte Strahlungshistorie in einem geschützten Arbeitsbereich exportieren, sichern, wiederherstellen oder gezielt löschen.",
    "Preview and merge a compatible SQLite backup": "Kompatible SQLite-Sicherung prüfen und zusammenführen",
    "Permanently remove app and Recorder history after explicit confirmation": "App- und Recorder-Historie nach ausdrücklicher Bestätigung dauerhaft entfernen",
    "Enable history management in the app configuration and restart only when maintenance is planned.": "Historienverwaltung in der App-Konfiguration aktivieren und nur für geplante Wartungsarbeiten neu starten.",
    "Enable “{setting}” in the app configuration and restart only when history maintenance is planned.": "„{setting}“ in der App-Konfiguration aktivieren und nur für geplante Arbeiten an der Historie neu starten.",
})

REPORT_820_EN = {
    "The professional five-page PDF report starts with an executive beta/gamma assessment, followed by correctly labelled CPM time series, distribution and Poisson reference, temporal heat maps, statistical significance, events and traceability. CPM remains the primary measurement; derived µSv/h values are not independent dosimetry. CSV files preserve accepted measurements without interpolation, and ZIP bundles additionally contain machine-readable analysis and specialist graphics.": "The professional five-page PDF report starts with an executive beta/gamma assessment, followed by correctly labelled CPM time series, distribution and Poisson reference, temporal heat maps, statistical significance, events and traceability. CPM remains the primary measurement; derived µSv/h values are not independent dosimetry. CSV files preserve accepted measurements without interpolation, and ZIP bundles additionally contain machine-readable analysis and specialist graphics.",
}
for _catalogue in (EN, DE, FR, ES, IT, NL, PL, HR):
    _catalogue.update(REPORT_820_EN)
DE.update({
    "The professional five-page PDF report starts with an executive beta/gamma assessment, followed by correctly labelled CPM time series, distribution and Poisson reference, temporal heat maps, statistical significance, events and traceability. CPM remains the primary measurement; derived µSv/h values are not independent dosimetry. CSV files preserve accepted measurements without interpolation, and ZIP bundles additionally contain machine-readable analysis and specialist graphics.": "Der professionelle fünfseitige PDF-Bericht beginnt mit einer kompakten Beta-/Gamma-Gesamtbewertung. Es folgen korrekt beschriftete CPM-Zeitreihen, Verteilung und Poisson-Referenz, zeitliche Heatmaps, Signifikanzbewertung, Ereignisse und Nachvollziehbarkeit. CPM bleibt die primäre Messgröße; abgeleitete µSv/h-Werte sind keine unabhängige Dosimetrie. CSV-Dateien bewahren akzeptierte Messwerte ohne Interpolation, ZIP-Pakete enthalten zusätzlich maschinenlesbare Analysen und Spezialgrafiken.",
})

WORKFLOW_CATALOGS = {"en": EN, "de": DE, "fr": FR, "es": ES, "it": IT, "nl": NL, "pl": PL, "hr": HR}

# Keep the protected history-management label identical to the Home Assistant
# configuration translation in every supported dashboard language.
ES.update({"History management": "Gestión del historial"})
FR.update({"History management": "Gestion de l'historique"})
HR.update({"History management": "Upravljanje poviješću"})
IT.update({"History management": "Gestione cronologia"})
NL.update({"History management": "Historiebeheer"})
PL.update({"History management": "Zarządzanie historią"})

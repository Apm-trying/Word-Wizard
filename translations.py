# All UI text lives here, keyed by language code.
# app.py should never contain a hardcoded English or Norwegian string directly —
# that's what makes adding a 3rd language later just "add a new dict entry"
# instead of hunting through app.py for stray text.

TRANSLATIONS = {
    "no": {
        "app_title": "🧙 Word Wizard",
        "app_subtitle": "Lær avansert — ett ord hver 12. time.",
        "topic_step_title": "Velg et tema",
        "topics": {
            "all": "Alle temaer",
            "politics": "Politikk",
            "economy": "Økonomi",
            "health": "Helse",
            "technology": "Teknologi",
        },
        "start_button": "Start læring →",
        "settings_button": "⚙️ Innstillinger",
        "topic_caption": "Tema: {topic}",
        "know_prompt": "Vet du hva dette ordet betyr?",
        "yes_button": "✅ Ja, jeg kan dette",
        "no_button": "❌ Nei, vis meg",
        "definition_label": "Definisjon",
        "example_label": "Eksempler",
        "known_success": "Bra jobbet! Dette ordet er markert som kjent.",
        "skip_button": "➡️ Hopp til nytt ord",
        "locked_message": "Kom tilbake om 12 timer for et nytt ord! Bruk tiden nå til å faktisk ta ordet i bruk.",
        "countdown_format": "{h}t {m}m igjen",
        "all_learned": "🎉 Du har lært alle ordene i dette temaet! Legg til flere i words.json, eller velg et annet tema i Innstillinger.",
    },
    "en": {
        "app_title": "🧙 Word Wizard",
        "app_subtitle": "Learn advanced — one word every 12 hours.",
        "topic_step_title": "Choose a topic",
        "topics": {
            "all": "All topics",
            "politics": "Politics",
            "economy": "Economy",
            "health": "Health",
            "technology": "Technology",
        },
        "start_button": "Start learning →",
        "settings_button": "⚙️ Settings",
        "topic_caption": "Topic: {topic}",
        "know_prompt": "Do you know what this word means?",
        "yes_button": "✅ Yes, I know this",
        "no_button": "❌ No, show me",
        "definition_label": "Definition",
        "example_label": "Examples",
        "known_success": "Nice work! This word is marked as known.",
        "skip_button": "➡️ Skip to a new word",
        "locked_message": "Come back in 12 hours for a new word! Spend your time now actually using this word.",
        "countdown_format": "{h}h {m}m left",
        "all_learned": "🎉 You've learned every word in this topic! Add more to words.json, or pick a different topic in Settings.",
    },
}


def t(language):
    """Returns the translation dict for the given language code."""
    return TRANSLATIONS[language]

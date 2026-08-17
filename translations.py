# All UI text lives here, keyed by language code.
# app.py should never contain a hardcoded English or Norwegian string directly —
# that's what makes adding a 3rd language later just "add a new dict entry"
# instead of hunting through app.py for stray text.

TRANSLATIONS = {
    "no": {
        "app_title": "🧙 Word Wizard",
        "app_subtitle": "Lær avansert — ett ord hver 12. time.",
        "topic_step_title": "Velg temaer",
        "topic_required_warning": "Vennligst velg minst ett tema.",
        "topics": {
            "politics": "Politikk",
            "economy": "Økonomi",
            "health": "Helse",
            "technology": "Teknologi",
        },
        "titles": {
            "beginner": "Nybegynner",
            "novice": "Lærling",
            "magician": "Magiker",
            "archmage": "Erkemagiker",
            "wizard": "Trollmann",
            "wizard_king": "Trollmannkonge",
        },
        "level_prefix": "Nivå",
        "start_button": "Start læring →",
        "settings_button": "⚙️ Innstillinger",
        "know_prompt": "Vet du hva dette ordet betyr?",
        "quiz_prompt": "Hvilken definisjon er riktig?",
        "quiz_wrong": "Ikke helt riktig denne gangen.",
        "yes_button": "✅ Ja, jeg kan dette",
        "no_button": "❌ Nei, vis meg",
        "definition_label": "Definisjon",
        "example_label": "Eksempler",
        "locked_message": "Kom tilbake om 12 timer for et nytt ord! Bruk tiden nå til å faktisk ta ordet i bruk.",
        "countdown_format": "{h}t {m}m igjen",
        "correct_heading": "Riktig! 🎉",
        "xp_gained_template": "+{xp} XP",
        "continue_button": "Fortsett →",
        "all_learned": "🎉 Du har lært alle ordene i dette temaet! Legg til flere i words.json, eller velg et annet tema i Innstillinger.",
    },
    "en": {
        "app_title": "🧙 Word Wizard",
        "app_subtitle": "Learn advanced — one word every 12 hours.",
        "topic_step_title": "Choose topics",
        "topic_required_warning": "Please select at least one topic.",
        "topics": {
            "politics": "Politics",
            "economy": "Economy",
            "health": "Health",
            "technology": "Technology",
        },
        "titles": {
            "beginner": "Beginner",
            "novice": "Novice",
            "magician": "Magician",
            "archmage": "Archmage",
            "wizard": "Wizard",
            "wizard_king": "Wizard King",
        },
        "level_prefix": "Level",
        "start_button": "Start learning →",
        "settings_button": "⚙️ Settings",
        "know_prompt": "Do you know what this word means?",
        "quiz_prompt": "Which definition is correct?",
        "quiz_wrong": "Not quite this time.",
        "yes_button": "✅ Yes, I know this",
        "no_button": "❌ No, show me",
        "definition_label": "Definition",
        "example_label": "Examples",
        "locked_message": "Come back in 12 hours for a new word! Spend your time now actually using this word.",
        "countdown_format": "{h}h {m}m left",
        "correct_heading": "Correct! 🎉",
        "xp_gained_template": "+{xp} XP",
        "continue_button": "Continue →",
        "all_learned": "🎉 You've learned every word in this topic! Add more to words.json, or pick a different topic in Settings.",
    },
}


def t(language):
    """Returns the translation dict for the given language code."""
    return TRANSLATIONS[language]

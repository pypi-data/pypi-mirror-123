lan = {
    "Arabic": 2,
    "Bengali": 54,
    "Brazillian Portuguese": 4,
    "Chinese BG code": 7,
    "Danish": 10,
    "Dutch": 11,
    "English": 13,
    "Farsi Persian": 46,
    "Finnish": 17,
    "French": 18,
    "German": 19,
    "Greek": 21,
    "Hebrew": 22,
    "Indonesian": 44,
    "Italian": 26,
    "Korean": 28,
    "Malay": 50,
    "Norwegian": 30,
    "Portuguese": 32,
    "Romanian": 33,
    "Spanish": 38,
    "Swedish": 39,
    "Thai": 40,
    "Turkish": 41,
    "Vietnamese": 45,
    "Albanian": 1,
    "Armenian": 73,
    "Azerbaijani": 55,
    "Basque": 74,
    "Belarusian": 68,
    "Bosnian": 60,
    "Bulgarian": 5,
    "Bulgarian English": 6,
    "Burmese": 61,
    "Cambodian Khmer": 79,
    "Catalan": 49,
    "Croatian": 8,
    "Czech": 9,
    "Dutch English": 12,
    "English German": 15,
    "Esperanto": 47,
    "Estonian": 16,
    "Georgian": 62,
    "Greenlandic": 57,
    "Hindi": 51,
    "Hungarian": 23,
    "Hungarian English": 24,
    "Icelandic": 25,
    "Japanese": 27,
    "Kannada": 78,
    "Kinyarwanda": 81,
    "Kurdish": 52,
    "Latvian": 29,
    "Lithuanian": 43,
    "Macedonian": 48,
    "Malayalam": 64,
    "Manipuri": 65,
    "Mongolian": 72,
    "Nepali": 80,
    "Pashto": 67,
    "Polish": 31,
    "Punjabi": 66,
    "Russian": 34,
    "Serbian": 35,
    "Sinhala": 58,
    "Slovak": 36,
    "Slovenian": 37,
    "Somali": 70,
    "Sundanese": 76,
    "Swahili": 75,
    "Tagalog": 53,
    "Tamil": 59,
    "Telugu": 63,
    "Ukrainian": 56,
    "Urdu": 42,
    "Yoruba": 71}


class Language:
    def __init__(self, term):
        self._name = ""
        self._code = 0
        find_res = list(filter(lambda x: term.lower().strip() == x.lower().strip(), lan.keys()))

        if len(find_res) == 0:
            find_res = list(filter(lambda x: term.lower().strip() in x.lower().strip(), lan.keys()))

        if len(find_res) == 0:
            self._name = "English"
            self._code = lan.get(self._name)
        else:
            self._name = find_res.pop()
            self._code = lan.get(self._name)

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code


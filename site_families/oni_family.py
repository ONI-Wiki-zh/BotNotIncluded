from pywikibot import family


class Family(family.Family):
    name = 'oni'
    langs = {
        'en': 'oxygennotincluded.wiki.gg',
        'zh': 'oxygennotincluded.wiki.gg',
        'ja': 'oxygennotincluded.fandom.com',
        'pt-br': 'oxygennotincluded.fandom.com',
        'ru': 'oxygen-not-included.fandom.com',
        'th': 'oxygennotincluded.fandom.com',
    }

    def scriptpath(self, code):
        return {
            'en': '',
            'zh': '/zh',
            'ja': '/ja',
            'pt-br': '/pt-br',
            'ru': '/ru',
            'th': '/th',
        }[code]

    def protocol(self, code):
        return 'https'

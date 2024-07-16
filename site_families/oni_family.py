from pywikibot import family


class Family(family.Family):
    name = 'oni'
    langs = {
        'en': 'oxygennotincluded.wiki.gg',
        'zh': 'oxygennotincluded.wiki.gg',
        'ja': 'oxygennotincluded.wiki.gg',
        'pt-br': 'oxygennotincluded.wiki.gg',
        'ru': 'oxygen-not-included.wiki.gg',
        'th': 'oxygennotincluded.wiki.gg',
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
        return 'HTTPS'

from pywikibot import family


class Family(family.Family):
    name = 'oni'
    langs = {
        'en': 'oxygennotincluded.fandom.com',
        'zh': 'oxygennotincluded.fandom.com',
    }

    def scriptpath(self, code):
        return {
            'en': '',
            'zh': '/zh',
        }[code]

    def protocol(self, code):
        return 'HTTPS'

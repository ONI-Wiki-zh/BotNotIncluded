from pywikibot import family


class Family(family.Family):
    name = 'feheroes'
    langs = {
        'en': 'feheroes.fandom.com',
    }

    def scriptpath(self, code):
        return {
            'en': '',
        }[code]

    def protocol(self, code):
        return 'HTTPS'

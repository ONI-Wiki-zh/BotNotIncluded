from pywikibot import family


class Family(family.Family):
    name = 'pogo'
    langs = {
        'en': 'pokemongo.fandom.com',
    }

    def scriptpath(self, code):
        return {
            'en': '',
        }[code]

    def protocol(self, code):
        return 'HTTPS'

from pywikibot import family


class Family(family.Family):
    name = 're0'
    langs = {
        'en': 'rezero.fandom.com',
        'zh': 'rezero.fandom.com',
    }

    def scriptpath(self, code):
        return {
            'en': '',
            'zh': '/zh',
        }[code]

    def protocol(self, code):
        return 'HTTPS'

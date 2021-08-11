from pywikibot import family


class Family(family.Family):
    name = 'boni'
    langs = {
        'zh': 'wiki.biligame.com',
    }

    def scriptpath(self, code):
        return {
            'zh': '/oni',
        }[code]

    def protocol(self, code):
        return 'HTTPS'

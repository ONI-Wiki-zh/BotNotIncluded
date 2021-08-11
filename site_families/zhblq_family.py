from pywikibot import family


class Family(family.Family):
    name = 'zhblq'
    langs = {
        'zh': 'zhpolandball.miraheze.org',
    }

    def scriptpath(self, code):
        return {
            'zh': '/w',
        }[code]

    def protocol(self, code):
        return 'HTTPS'

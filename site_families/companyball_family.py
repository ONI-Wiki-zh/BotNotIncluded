from pywikibot import family


class Family(family.Family):
    name = 'companyball'
    langs = {
        'zh': 'companyball.fandom.com',
    }

    def scriptpath(self, code):
        return {
            'zh': '/zh',
        }[code]

    def protocol(self, code):
        return 'HTTPS'

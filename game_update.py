import utils
logger = utils.getLogger("Game update CI")


def main():
    comment = input("Current game vertion: ")

    logger.info('Parse translation files')
    import parse_po
    parse_po.main()

    logger.info('Generating worldgen data')
    import worlds
    worlds.main()

    logger.info('Generating elements data')
    import elements
    elements.main()

    # TODO: use game dir
    logger.info('Generating personalities data')
    import textAsset.personalities
    textAsset.personalities.main()

    logger.info('Generating codex data')
    import get_codex
    get_codex.main()

    logger.info('Uploading generated data')
    import bot
    bot.update_data(comment=comment)

    logger.info('Updating language convertion tables')
    import t_conversion
    t_conversion.update()


if __name__ == '__main__':
    main()

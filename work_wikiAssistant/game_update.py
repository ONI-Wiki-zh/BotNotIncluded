import utils
logger = utils.getLogger("Game update CI")


def main():
    comment = input("Current game vertion: ")

    logger.info('Parse translation files')
    from work_extractGame import parse_po
    parse_po.main()

    logger.info('Generating worldgen data')
    from work_extractGame import worlds
    worlds.main()

    logger.info('Generating elements data')
    from work_extractGame import elements
    elements.main()

    # TODO: use game dir
    logger.info('Generating personalities data')
    import work_extractGame.personalities
    work_extractGame.personalities.main()

    logger.info('Generating codex data')
    from work_extractGame import get_codex
    get_codex.main()

    logger.info('Uploading generated data')
    from work_wikiAssistant import bot
    bot.update_data(comment=comment)

    logger.info('Updating language conversion tables')
    import t_conversion
    t_conversion.update()


if __name__ == '__main__':
    main()

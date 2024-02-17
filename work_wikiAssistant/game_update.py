import utils
logger = utils.getLogger("Game update CI")


def main():
    comment = input("Current game vertion: ")

    from work_extractGame import game_extract
    game_extract.main()

    logger.info('Uploading generated data')
    from work_wikiAssistant import bot
    bot.update_data(comment=comment)

    logger.info('Updating language conversion tables')
    import t_conversion
    t_conversion.update()


if __name__ == '__main__':
    main()

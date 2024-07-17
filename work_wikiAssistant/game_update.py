import utils
logger = utils.getLogger("Game update CI")


def main():
    comment = input("Current game vertion: ")

    from work_extractGame import game_extract
    game_extract.main()

    # 更新wiki数据模块
    logger.info('Uploading generated data')
    from work_wikiAssistant import bot
    bot.update_data(comment=comment)

    # 更新wiki译名表
    logger.info('Updating language conversion tables')
    import t_conversion
    t_conversion.update()

    logger.info('Update Wiki End')
    pass


if __name__ == '__main__':
    main()

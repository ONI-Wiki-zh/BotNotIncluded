import utils
logger = utils.getLogger("Game update CI")


def main():
    # 处理po翻译文件
    logger.info('Parse translation files')
    from work_extractGame import parse_po
    parse_po.main()

    # 处理世界生成
    logger.info('Generating worldgen data')
    from work_extractGame import worlds
    worlds.main()

    # 处理元素数据
    logger.info('Generating elements data')
    from work_extractGame import elements
    elements.main()

    # TODO: use game dir
    # 处理复制人数据
    logger.info('Generating personalities data')
    import work_extractGame.personalities
    work_extractGame.personalities.main()

    # 处理codex数据
    logger.info('Generating codex data')
    from work_extractGame import get_codex
    get_codex.main()


if __name__ == '__main__':
    """提取游戏数据"""
    main()

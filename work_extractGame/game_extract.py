"""提取游戏数据"""
import utils
from work_extractGame import t_building, t_critter, t_disease, t_equipment, t_food, t_geyser, t_items, \
    t_MaterialModifier, t_plant, t_room, t_sickness, t_skill, t_tech, parse_entity, t_personalities, \
    t_comet, t_artifact, t_artifactPOI, t_gameplaySeasons, t_gravitasEntity, t_harvestablePOI, t_meteorShower, \
    t_spaceDestinationTypes
import constant

logger = utils.getLogger("Game update CI")


def main():
    """提取游戏数据"""
    # 处理世界生成
    logger.info('Generating worldgen data')
    from work_extractGame import worlds
    worlds.main()

    # 处理元素数据
    logger.info('Generating elements data')
    from work_extractGame import elements
    elements.main()

    # 处理实体数据
    logger.info('Generating entity data')
    t_building.convert_data_2_lua(constant.EntityType.Building.value)
    t_critter.convert_data_2_lua(constant.EntityType.Critter.value)
    t_disease.convert_data_2_lua(constant.EntityType.Disease.value)
    t_equipment.convert_data_2_lua(constant.EntityType.Equipment.value)
    t_food.convert_data_2_lua(constant.EntityType.Food.value)
    t_geyser.convert_data_2_lua(constant.EntityType.Geyser.value)
    t_items.convert_data_2_lua(constant.EntityType.Item.value)
    t_MaterialModifier.convert_data_2_lua(constant.EntityType.MaterialModifier.value)
    t_personalities.convert_data_2_lua(constant.EntityType.Personalities.value)
    t_plant.convert_data_2_lua(constant.EntityType.Plant.value)
    t_room.convert_data_2_lua(constant.EntityType.RoomType.value)
    t_sickness.convert_data_2_lua(constant.EntityType.Sickness.value)
    t_skill.convert_data_2_lua(constant.EntityType.Skill.value)
    t_tech.convert_data_2_lua(constant.EntityType.Tech.value)
    t_comet.convert_data_2_lua(constant.EntityType.Comet.value)
    t_artifact.convert_data_2_lua(constant.EntityType.Artifact.value)
    t_artifactPOI.convert_data_2_lua(constant.EntityType.ArtifactPOI.value)
    t_gameplaySeasons.convert_data_2_lua(constant.EntityType.GameplaySeason.value)
    t_gravitasEntity.convert_data_2_lua(constant.EntityType.GravitasEntity.value)
    t_harvestablePOI.convert_data_2_lua(constant.EntityType.HarvestablePOI.value)
    t_meteorShower.convert_data_2_lua(constant.EntityType.MeteorShower.value)
    t_spaceDestinationTypes.convert_data_2_lua(constant.EntityType.SpaceDestinationType.value)


    # 处理codex数据
    logger.info('Generating codex data')
    from work_extractGame import get_codex
    get_codex.main()

    # 实体id与po译名对应表
    logger.info('Parse translation EntityId')
    parse_entity.convert_data_2_lua()

    # 处理po翻译文件
    logger.info('Parse translation files')
    from work_extractGame import parse_po
    parse_po.main()

    logger.info('game_extract End')
    pass


if __name__ == '__main__':
    main()

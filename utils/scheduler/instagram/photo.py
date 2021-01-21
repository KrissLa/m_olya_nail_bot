from loguru import logger

from data.config import INSTAGRAM_ID, INSTAGRAM_KEY
from loader import instagram_bot, db


async def get_recent_images():
    picture_urls = []
    last_medias = instagram_bot.get_last_user_medias(INSTAGRAM_ID, count=10)
    # for l in last_medias:
    #     llm = instagram_bot.get_media_info(l)
    #     logger.info(llm[0]['caption'])
    # logger.info(len(last_medias))
    for n in range(len(last_medias)):
        logger.info(n)
        try:
            comment = instagram_bot.get_media_comments(last_medias[n])[0]
            # logger.info(instagram_bot.get_media_comments(last_medias[n]))
        except IndexError:
            comment = None

        if not comment or INSTAGRAM_KEY not in comment['text']:
            comment = instagram_bot.get_media_info(last_medias[n])[0]['caption']
        logger.info(comment)
        if not comment:
            continue
        if INSTAGRAM_KEY in comment['text']:
            media_info = instagram_bot.get_media_info(last_medias[n])[0]
            if "image_versions2" in media_info.keys():
                url = media_info['image_versions2']['candidates'][0]['url']
                picture_urls.append(url)
            elif "carousel_media" in media_info.keys():
                for e, element in enumerate(media_info["carousel_media"]):
                    if element['image_versions2']["candidates"][0]["width"] != 360:
                        url = element['image_versions2']["candidates"][0]["url"]
                        picture_urls.append(url)
    logger.info(picture_urls[:5])
    return picture_urls[:5]


async def add_new_photo():
    """Добавляем последние фото из instagram в базу данных"""
    recent_images = await get_recent_images()
    recent_images.reverse()
    logger.info(recent_images)
    for ph in recent_images:
        result = await db.add_resent_photo(ph)
        if "success" not in result.keys():
            logger.info("Новая фотография успешно добавлена")






    # logger.info(media_info['image_versions2'])
    # logger.info(media_info['image_versions2']['candidates'][0]['url'])



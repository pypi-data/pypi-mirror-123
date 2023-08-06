import sys
from loguru import logger
from typing import Optional


def set_logger(
    format: Optional[str] = None,
    level: str = "INFO",
    colorize: bool = True,
    diagnose: bool = True,
    catch: bool = True,
    use_file: bool = False,
    file_path: Optional[str] = "./log/log.log",
    file_format: Optional[str] = None,
    file_rotation: str = "00:00",
    file_retention: str = "3 days",
    file_diagnose: bool = True,
    file_catch: bool = True,
    file_level: str = "INFO",
) -> logger:
    """是对loguru的logger进行的二次封装,大概是因为平时的logger不太适合自己,索性造了一个,是一个很可爱的logger呢。
    总之就是这个样子啦！配色什么的都是精心调整过的样子,
    话说回来我拿着别人的轮子来造自己的轮子真的没问题吗，看上去很容易被骂呢。
    嘛，那种事情怎么样都好啦。(笑)

    Args:
        format (Optional[str], optional): loguru的format格式,默认为:`"<g>{time:YYYY-MM-DD HH:mm:ss}</g> | <m>{module}:{function}</m> | <lvl>{level}</lvl> | <lvl>{message}</lvl>"`. Defaults to None.
        level (str, optional): loguru的level级别. Defaults to "INFO".
        colorize (bool), optional): 是否上色(日志会有颜色). Defaults to True.
        diagnose (bool, optional): 是否跟踪诊断原因. Defaults to True.
        catch (bool, optional): logger是否可以catch,使用`@logger.catch`捕获报错信息. Defaults to True.
        use_file (bool, optional): 是否将日志输出到文件. Defaults to False.
        file_path (Optional[str], optional): 文件的路径. Defaults to "./log/log.log".
        file_format (Optional[str], optional): 日志文件使用的格式,要求符合loguru的format,默认同上. Defaults to None.
        file_rotation (str, optional): 什么时候更换为新日志记录. Defaults to "00:00".
        file_retention (str, optional): 日志保留的时间. Defaults to "3 days".
        file_diagnose (bool, optional): 是否跟踪诊断原因. Defaults to True.
        file_catch (bool, optional): logger是否可以catch然后输出至日志,使用方法同上. Defaults to True.
        file_level (str, optional): 日志文件的level. Defaults to "INFO".

    Returns:
        logger: 二次封装后的logger,是自己日常常用的风格
    """
    logger.remove()

    logger.add(
        sys.stderr,
        format=format
        if format
        else "<g>{time:YYYY-MM-DD HH:mm:ss}</g> | <m>{module}:{function}</m> | <lvl>{level}</lvl> | <lvl>{message}</lvl>",
        level=level,
        diagnose=diagnose,
        catch=catch,
        colorize=colorize,
    )
    if use_file:
        logger.add(
            file_path,
            format=file_format
            if file_format
            else "<g>{time:YYYY-MM-DD HH:mm:ss}</g> | <m>{module}:{function}</m> | <lvl>{level}</lvl> | <lvl>{message}</lvl>",
            rotation=file_rotation,
            retention=file_retention,
            diagnose=file_diagnose,
            catch=file_catch,
            level=file_level,
        )

    return logger


logger = set_logger()

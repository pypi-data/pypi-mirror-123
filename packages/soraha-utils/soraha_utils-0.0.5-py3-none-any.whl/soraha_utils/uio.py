import ujson
import aiofiles
from uuid import uuid4
from typing import Any, AnyStr, Optional, Union, IO

from .uiexcep import *
from .uitry import retry
from .uilog import logger
from .uiclient import sync_uiclient, async_uiclient


class uio:
    """请不用理会这个

    Returns:
        ?return什么啊: 啊这
    """

    @staticmethod
    def sync_dump(obj: Any, fp: Optional[IO[AnyStr]]) -> None:
        """同步下的json_dump,单独提出来是因为ensure_ascii跟indent太烦了！

        Args:
            obj (Any): json格式文本
            fp (Optional[IO[AnyStr]]): 同步下的fileIO
        """
        return ujson.dump(obj, fp, indent=4, ensure_ascii=False)

    @staticmethod
    async def async_dump(obj: Any, fp: Optional[IO[AnyStr]]):
        """异步下的json_dump,单独提出来是因为ensure_ascii跟indent太烦了！

        Args:
            obj (Any): json格式文本
            fp (Optional[IO[AnyStr]]): asyncfiles下的fileIO
        """
        return ujson.dump(obj, fp, indent=4, ensure_ascii=False)


class sync_uio(uio):
    def __init__(self) -> None:
        """emmmmm"""
        super().__init__()

    @retry(logger=logger)
    def save_file(
        self,
        type: Optional[str],
        fp: Optional[IO[AnyStr]] = None,
        obj: Any = None,
        open_type: str = "w",
        encoding: Optional[str] = "utf-8",
        save_path: str = "./res/",
        save_name: str = str(uuid4())[-12:],
        file_extension: str = None,
        url: Optional[str] = None,
        proxy: Optional[dict] = None,
        timeout: Optional[Union[tuple, int]] = None,
        request_headers: Optional[dict] = None,
        other_headers: Optional[str] = None,
        request_json: Optional[Any] = None,
        request_params: Optional[dict] = None,
        request_data: Optional[dict] = None,
    ) -> list[bool, Optional[str]]:
        """保存文件的方法,提供了以下几种情况的保存:
        1.提供url,保存请求的json或是图片到默认路径`./res/随机id.[json|png]`或给予的路径或是fileIO
        2.提供obj,保存到提供的路径或是默认或是fileIO
        3.提供dict,保存json到提供路径或是fileIO
        4.提供obj及后缀名,写入到提供路径或是fileIO
        除此之外(例如需要post什么的)请自己动手丰衣足食！羽衣已经累坏了

        Args:
            type (Optional[str], optional): ["json"|"url_json"|"image"|"url_image"|"other"].
            fp (Optional[IO[AnyStr]], optional): fileIO,有需要保存到特定文件时提供,或者提供路径+文件名+文件后缀. Defaults to None.
            obj (Any, optional): 任意需要保存的东西[json|dict|text|Any]. Defaults to None.
            open_type (str, optional): open文件的方法,一般不用理会. Defaults to "w".
            encoding (Optional[str], optional): open文件时的encoding,一般不用改. Defaults to "utf-8".
            save_path (str, optional): 保存的路径. Defaults to "./res/".
            save_name (str, optional): 保存的文件名. Defaults to str(uuid4())[-12:].
            file_extension (str, optional): 如果type=="other",传入文件后缀,否则为空后缀. Defaults to None.
            url (Optional[str], optional): 需要请求url获取数据时,传入url. Defaults to None.
            proxy (Optional[dict], optional): url存在时有效,requests接受的代理. Defaults to None.
            timeout (Optional[Union[tuple, int]], optional): url存在时有效,requests接受的timeout. Defaults to None.
            request_headers (Optional[dict], optional): url存在时有效,默认为中文的windows电脑,传入cookie请使用request_cookies. Defaults to None.
            other_headers (Optional[str]): url存在时有效,传入任意headers的键值对,请求时会加进去. Defaults to None.
            request_json (Optional[AnyStr]): url存在时有效,post的json. Defaults to None.
            request_params (Optional[dict], optional): url存在时有效,请求的params. Defaults to None.
            request_data (Optional[dict], optional): url存在时有效,请求的data. Defaults to None.
        Returns:
            list[bool,Optional[str]]: [成功或失败,保存的文件路径(传入fileIO或出错时返回为None)]
        """
        try:
            if type.lower() == "json":
                file_extension = ".json"
                if fp:
                    self.sync_dump(obj, fp)
                    return [True, None]
                else:
                    with open(
                        save_path + save_name + file_extension,
                        open_type,
                        encoding=encoding,
                    ) as f:
                        self.sync_dump(obj, f)
                        return [True, save_path + save_name + file_extension]
            elif type.lower() == "image":
                file_extension = ".png"
                open_type = "wb"
                encoding = None
                if fp:
                    fp.write(obj)
                    return [True, None]
                else:
                    with open(
                        save_path + save_name + file_extension,
                        open_type,
                        encoding=encoding,
                    ) as f:
                        f.write(obj)
                        return [True, save_path + save_name + file_extension]
            elif type.lower() == "url_image" or "url_json":
                save_type = "image" if type.lower() == "url_image" else "json"
                with sync_uiclient(
                    proxy,
                    timeout,
                    request_headers,
                    other_headers,
                    request_json,
                    request_params,
                    request_data,
                ) as client:
                    res = client.uiget(url)
                if save_type == "json":
                    if fp:
                        self.sync_dump(res.json(), fp)
                        return [True, None]
                    else:
                        file_extension = ".json"
                        open_type = "w"
                        with open(
                            save_path + save_name + file_extension,
                            open_type,
                            encoding=encoding,
                        ) as f:
                            self.sync_dump(res.json(), f)
                            return [True, save_path + save_name + file_extension]
                else:
                    if fp:
                        fp.write(res.content)
                        return [True, None]
                    else:
                        file_extension = ".png"
                        open_type = "wb"
                        with open(
                            save_path + save_name + file_extension, open_type
                        ) as f:
                            f.write(res.content)
                            return [True, save_path + save_name + file_extension]
            elif type.lower() == "other":
                if fp:
                    fp.write(obj)
                    return [True, None]
                else:
                    with open(
                        save_path + save_name + file_extension,
                        open_type,
                        encoding=encoding,
                    ) as f:
                        f.write(obj)
                        return [True, save_path + save_name + file_extension]
            else:
                raise Uio_MethodNotDefinded
        except Uio_MethodNotDefinded:
            raise
        except Exception as e:
            logger.warning(f"文件保存失败!捕获到错误:{e}")


class async_uio(uio):
    def __init__(self) -> None:
        super().__init__()

    @retry(logger=logger)
    async def save_file(
        self,
        type: Optional[str],
        fp: Optional[IO[AnyStr]] = None,
        obj: Any = None,
        open_type: str = "w",
        encoding: Optional[str] = "utf-8",
        save_path: str = "./res/",
        save_name: str = str(uuid4())[-12:],
        file_extension: str = None,
        url: Optional[str] = None,
        proxy: Optional[dict] = None,
        timeout: Optional[Union[tuple, int]] = None,
        request_headers: Optional[dict] = None,
        other_headers: Optional[str] = None,
        request_json: Optional[AnyStr] = None,
        request_params: Optional[dict] = None,
        request_data: Optional[dict] = None,
    ) -> list[bool, Optional[str]]:
        """保存文件的异步方法,提供了以下几种情况的保存:
        1.提供url,保存请求的json或是图片到默认路径`./res/随机id.[json|png]`或给予的路径或是fileIO
        2.提供obj,保存到提供的路径或是默认或是fileIO
        3.提供dict,保存json到提供路径或是fileIO
        4.提供obj及后缀名,写入到提供路径或是fileIO
        除此之外(例如需要post什么的)请自己动手丰衣足食！羽衣已经累坏了
        Args:
            type (Optional[str], optional): ["json"|"url_json"|"image"|"url_image"|"other"]
            fp (Optional[IO[AnyStr]], optional): fileIO,有需要保存到特定文件时提供,或者提供路径+文件名+文件后缀. Defaults to None.
            obj (Any, optional): 任意需要保存的东西[json|dict|text|Any]. Defaults to None.
            open_type (str, optional): open文件的方法,一般不用理会. Defaults to "w".
            encoding (Optional[str], optional): open文件时的encoding,一般不用改. Defaults to "utf-8".
            save_path (str, optional): 保存的路径. Defaults to "./res/".
            save_name (str, optional): 保存的文件名. Defaults to str(uuid4())[-12:].
            file_extension (str, optional): 如果type=="other",传入文件后缀,否则为空后缀. Defaults to None.
            url (Optional[str], optional): 需要请求url获取数据时,传入url. Defaults to None.
            proxy (Optional[dict], optional): url存在时有效,requests接受的代理. Defaults to None.
            timeout (Optional[Union[tuple, int]], optional): url存在时有效,requests接受的timeout. Defaults to None.
            request_headers (Optional[dict], optional): url存在时有效,默认为中文的windows电脑,传入cookie请使用request_cookies. Defaults to None.
            other_headers (Optional[str]): url存在时有效,传入任意headers的键值对,请求时会加进去. Defaults to None.
            request_json (Optional[AnyStr]): url存在时有效,post的json. Defaults to None.
            request_params (Optional[dict], optional): url存在时有效,请求的params. Defaults to None.
            request_data (Optional[dict], optional): url存在时有效,请求的data. Defaults to None.
        Returns:
            list[bool,Optional[str]]: [成功或失败,保存的文件路径(传入fileIO或出错时返回为None)]
        """
        try:
            if type.lower() == "json":
                file_extension = ".json"
                if fp:
                    await self.async_dump(obj, fp)
                    return [True, None]
                else:
                    async with aiofiles.open(
                        save_path + save_name + file_extension,
                        open_type,
                        encoding=encoding,
                    ) as f:
                        await self.async_dump(obj, f)
                        return [True, save_path + save_name + file_extension]
            elif type.lower() == "image":
                file_extension = ".png"
                open_type = "wb"
                encoding = None
                if fp:
                    await fp.write(obj)
                    return [True, None]
                else:
                    async with aiofiles.open(
                        save_path + save_name + file_extension,
                        open_type,
                        encoding=encoding,
                    ) as f:
                        await f.write(obj)
                        return [True, save_path + save_name + file_extension]
            elif type.lower() == "url_image" or "url_json":
                save_type = "image" if type.lower() == "url_image" else "json"
                async with async_uiclient(
                    proxy,
                    timeout,
                    request_headers,
                    other_headers,
                    request_json,
                    request_params,
                    request_data,
                ) as client:
                    res = await client.uiget(url)
                if save_type == "json":
                    if fp:
                        await self.async_dump(res.json(), fp)
                        return [True, None]
                    else:
                        file_extension = ".json"
                        open_type = "w"
                        async with aiofiles.open(
                            save_path + save_name + file_extension,
                            open_type,
                            encoding=encoding,
                        ) as f:
                            await self.async_dump(res.json(), f)
                            return [True, save_path + save_name + file_extension]
                else:
                    if fp:
                        await fp.write(res.content)
                        return [True, None]
                    else:
                        file_extension = ".png"
                        open_type = "wb"
                        async with aiofiles.open(
                            save_path + save_name + file_extension, open_type
                        ) as f:
                            await f.write(res.content)
                            return [True, save_path + save_name + file_extension]
            elif type.lower() == "other":
                if fp:
                    await fp.write(obj)
                    return [True, None]
                else:
                    async with aiofiles.open(
                        save_path + save_name + file_extension,
                        open_type,
                        encoding=encoding,
                    ) as f:
                        await f.write(obj)
                        return [True, save_path + save_name + file_extension]
            else:
                raise Uio_MethodNotDefinded
        except Uio_MethodNotDefinded:
            raise
        except Exception as e:
            logger.warning(f"文件保存失败!捕获到错误:{e}")
            raise

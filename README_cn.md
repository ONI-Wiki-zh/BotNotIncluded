[English](README.md) | 简体中文

# BotNotIncluded

此项目用于为 [zh ONI wiki](https://oxygennotincluded.wiki.gg/zh) 使用Pywikibot和一些脚本（另包含其他wiki的实用工具）。

- 确保使用 **Python 3.7+** 运行，因为使用了一些新功能。（例如，字典的插入顺序保存特性）

本项目包含多个工具集，存放于根目录下的不同package中，分别为：

- 缺氧中文wiki巡查机器人
- 游戏数据提取
- 缺氧中文wiki工具
- 其他wiki工具

## 全局配置

打开`constant.py`，检查以下参数的配置

| 名称           | 说明 (Notes)           | 默认值                                                       |
| -------------- | ---------------------- | ------------------------------------------------------------ |
| `BNI_ONI_ROOT` | 缺氧游戏安装目录       | `C:\Program Files (x86)\Steam\steamapps\common\OxygenNotIncluded` |
| `BNI_PO_HANT`  | 繁体中文po翻译文件位置 | `C:\Users\%USERNAME%\Documents\Klei\OxygenNotIncluded\mods\Steam\2906930548\strings.po` |

在**控制台**运行以下代码，安装项目依赖。

```sh
python -m venv venv --clear # create virtual environment (recommended)
source venv/bin/activate # activate virtual environment
pip3 install -r requirements.txt # install dependencies
```

如果需要执行与wiki站点交互的脚本，需要进行一些配置。

打开`site_families`目录，在对应的wiki站点配置文件中，修改`langs`下的网址为你需要访问的wiki站点。

```
langs = {
    'en': 'xxx.wiki.com',
    'zh': 'xxx.wiki.com',
}
```

打开根目录下的`user-config.py`文件，修改`usernames`为你的wiki机器人用户名。详细参考文档[Manual:Pywikibot/user-config.py](https://www.mediawiki.org/wiki/Manual:Pywikibot/user-config.py)。

```
usernames['oni']['zh'] = "xxxBot"
usernames['oni']['en'] = "xxxBot"
```

在根目录下创建一个`user-password.py`文件，配置你的机器人密码。详细参考文档[Manual:Pywikibot/BotPasswords](https://www.mediawiki.org/wiki/Manual:Pywikibot/BotPasswords)。

```python
from pywikibot.login import BotPassword

("zh", "oni", "<your_user_name>", BotPassword("<your_bot_name>", "<your_bot_password>"))
```

**注意：请不要将`user-password.py`文件上传至Github或泄漏给他人。**



## 工具集1：缺氧中文wiki巡查机器人

> 代码集合在目录`work_githubAction`。该代码托管至Github Action运行。

### 功能

- 读取部分游戏数据，转化为 Lua 格式后上传至站内模块
- 读取站内图片并备份至OneDrive 中
- 比对中、英文站点，记录潜在的过时页面和有误的跨语言链接
- 修正站内文案格式



## 工具集2：游戏数据提取

> 代码集合在目录`work_extractGame`。

### 配置

打开`constant.py`，检查以下参数的配置

| 名称                         | 说明 (Notes)                     | 默认值                                                       |
| ---------------------------- | -------------------------------- | ------------------------------------------------------------ |
| `PATH_EXTRACT_DIR`           | OniExtract数据导出的路径         | `C:\Users\%USERNAME%\Documents\Klei\OxygenNotIncluded\export\database\` |
| `PATH_EXTRACT_DIR_BASE_ONLY` | OniExtract数据导出的路径(仅本体) | `C:\Users\%USERNAME%\Documents\Klei\OxygenNotIncluded\export\database_base\` |
| `PATH_PO_STRINGS_DIR`        | 游戏官方po翻译文件目录           | `C:\Program Files (x86)\Steam\steamapps\common\OxygenNotIncluded\OxygenNotIncluded_Data\StreamingAssets\strings\` |

### 运行

在控制台输入以下命令进入python命令行工具

```sh
python
```

进入python命令行后，逐行输入以下代码，执行脚本

```python
from work_extractGame import game_extract
game_extract.main()
exit()
```



## 工具集3：缺氧中文wiki工具

> 代码集合在目录`work_wikiAssistant`。

### 功能

- `game_update.py` 更新wiki站点的数据模块（Module:Data）。
- `bot_add_footer.py` 批量添加页脚。

### 运行

#### game_update.py

在控制台输入以下命令进入python命令行工具

```sh
python
```

进入python命令行后，逐行输入以下代码，执行脚本

```python
from work_wikiAssistant import game_update
game_update.main()
exit()
```



## 工具集4：其他wiki工具

> 代码集合在目录`work_otherWiki`。

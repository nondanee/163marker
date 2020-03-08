# 163 Marker

为歌曲添加 `163 key(Don't modify)` 标记

让非网易云客户端下载的音频文件能被客户端识别，正常匹配歌词和查看评论

## Dependency

```
$ pip install requests mutagen pycryptodome
```

## Install
```
$ pip install git+https://github.com/nondanee/163marker.git
```

## Usage

### Execute

```
$ 163marker -h # 等同于 "python 163marker/main.py -h" 和 "python -m 163marker.main -h"
usage: 163marker [-h] file [uri] [id]

positional arguments:
  file        audio file path (MP3/FLAC)
  uri         meta data source (URL/PATH)
  id          specific song id

optional arguments:
  -h, --help  show this help message and exit
```

- `file` 文件路径 (支持 MP3 和 FLAC 格式)

- `uri` 用户动态 / 专辑 / 歌曲链接 (客户端内分享，复制链接) 或文件路径 (拷贝标记)

- `id` 强制填充歌曲 ID (可选)

### Import

```python
import importlib # 因包名为数字开头无法直接 import
marker = importlib.import_module('163marker')
```

```python
marker.extract(file_path) # 从文件读取标记内容

marker.parse(resource_uri) # 从链接或文件地址获得元数据

marker.mark(file_path, song_meta, song_id) # 由元数据生成标记并写入文件
```

> 注: 对于已经 "消失" 的曲目 (无歌曲链接)
>
>  1. 若曾分享单曲到动态，可从用户的动态中提取信息
>
>  2. 若曲目消失而专辑未下架，可用专辑信息重建数据，再填充歌曲 ID
>
>  3. 若曾下载过相同专辑的其他歌曲，可拷贝已有文件的标记，再填充歌曲 ID
>
>      2/3 情况下默认同专辑歌手一致，歌名将从 ID3 tag `title` 中读取，请预先设置

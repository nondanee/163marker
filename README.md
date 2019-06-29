# 163 Marker

通过用户动态分享历史数据为已经 "消失" 的歌曲构造 `163 key(Don't modify)` 标记

让非网易云客户端下载的音频文件能被客户端识别，正常匹配歌词和查看评论

## Dependency

```
$ pip install -r requirements.txt
```

## Usage

```
$ python main.py (file) (url) [id]
```

- `file` 文件路径 (支持 MP3 和 FLAC 格式)

- `url` 用户动态链接 / 专辑链接 (客户端内分享，复制链接)

- `id` 强制填充歌曲 id (可选)
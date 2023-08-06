# user-avatars

rock-avatars

```
pytest --cov=rock_avatars/
```

```
python setup.py sdist build
```

```
twine upload dist/*
```

文件目录结构

```
tree ./data
./data
├── background.png
├── cloth
│   └── cloth.png
├── eye
│   └── eyes.png
├── hair
│   ├── hair.png
│   └── hair2.png
├── horn
│   └── horn.png
└── mouth
    ├── mouth.png
    └── mouth2.png

5 directories, 8 files
```

用法

```
import rock_avatars as rf

avatar = rf.Avatar(
    "./data",
    "background.png",
    [
        "mouth",
        "horn",
        "hair",
        "eye",
        "cloth",
    ],
)
avatar.generate()
```

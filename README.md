# 📝 Description

> Fastest Tibia PixelBot developed in python to get unlocked fps.

_Read this in other languages: [English](README.md), [Brazilian Portuguese](README.pt-BR.md)._

This BOT works locating image around the screen and applies cache to avoid image redetection and thus avoid excessive cpu/gpu usage.

This BOT is all based on matrix calculation, also applies parallelism and also pre-processing, as it is the only way to have maximum performance(nanoseconds/microseconds).

This BOT also uses data structure, arrays, path finding, among other important things to have smart decisions and gameplay.

This BOT walks by keyboard and make human mouse movimentation.

I created this BOT to learn python, to stream on twitch, to make friends, to apply my knowledgments in deep learning, path finding, matrix, etc.

I'm not going to sell subscription to this BOT, but it will work on "global" and you can use it, it's at your own risk.

This BOT ins't ready yet, this BOT still under construction.

Be free to use any function to create your custom BOT or wait for the release of v0.

# 🤖 BearSharp

Due to personal commitments that demand my attention, I'm temporarily pausing the development of the bot project for Tibia. However, I'm happy to share that my friend has a fantastic project called BearSharp which offers excellent features and is continually updated. While my project is down, I encourage you to check out BearSharp's exceptional work. I'm sure you'll find everything you need and more there.

Here is the BearSharp discord link: https://discord.gg/rqm9E3EGBr

Thank you for your understanding and I continue to look forward to resuming my work as soon as possible.

# 🗺️ Features

Only available for knight/paladin

| Features                  | Done               |
| ------------------------- | ------------------ |
| Alerts                    | :x:                |
| Auto amulet               | :heavy_check_mark: |
| Auto login                | :x:                |
| Auto ring                 | :heavy_check_mark: |
| Auto server save          | :x:                |
| Cavebot                   | :heavy_check_mark: |
| Combo Spells              | :heavy_check_mark: |
| Drop flasks               | :heavy_check_mark: |
| Deposit gold              | :heavy_check_mark: |
| Deposit non stacked items | :heavy_check_mark: |
| Deposit stacked items     | :heavy_check_mark: |
| Fish                      | :x:                |
| Food eater                | :heavy_check_mark: |
| Healing                   | :heavy_check_mark: |
| Smart Targeting           | :heavy_check_mark: |
| Refill                    | :heavy_check_mark: |
| Quick loot                | :heavy_check_mark: |
| Sell flasks               | :x:                |
| Sell items                | :x:                |
| Train                     | :x:                |

# ⚽ Goals

- Detect every necessary information in the client in (milli/macro/nano)seconds
- Control every pixel of the mouse to make human movements
- Use convolutionals neural networks to detect relevant stuffs like blockable objects, dropped loots, etc
- Use recurrent neural networks to use natural language processing to chat with others players
- Make party gameplay

# 🧰 Installation

## Tibia client options

Before installing the python packages, PyTibia requires that the Tibia client has some necessary settings for it to work correctly. Please leave the options exactly as in the next images:

![Controls](/docs/assets/images/controls.png)
![General Hotkeys](/docs/assets/images/generalHotkeys.png)
![Action Bar Hotkeys](/docs/assets/images/actionBarHotkeys.png)
![Custom hotkeys](/docs/assets/images/customHotkeys.png)
![Interface](/docs/assets/images/interface.png)
![HUD](/docs/assets/images/hud.png)
![Console](/docs/assets/images/console.png)
![Game Window](/docs/assets/images/gameWindow.png)
![Action Bars](/docs/assets/images/actionBars.png)
![Graphics](/docs/assets/images/graphics.png)
![Effects](/docs/assets/images/effects.png)
![Misc](/docs/assets/images/misc.png)
![Gameplay](/docs/assets/images/gameplay.png)

In the Tibia client, open the skills panel, the battle list, and set the gameWindow to the highest resolution, exactly like in the picture below:

![Client](/docs/assets/images/client.png)

For now PyTibia's hotkeys are not configurable, it is necessary to leave it exactly like table below:

| Hotkey | Item                            |
| ------ | ------------------------------- |
| 1      | Health Potion                   |
| 2      | Mana Potion                     |
| 3      | Health food                     |
| 4      | Mana food                       |
| 5      | Light healing(exura ico)        |
| 6      | Critical healing(exura med ico) |
| 7      | utura                           |
| 8      | utura gran                      |
| 9      | exana kor                       |
| 0      | exana pox                       |
| f1     | exori                           |
| f2     | exori gran                      |
| f3     | exori ico                       |
| f4     | exori hur                       |
| f5     | exori mas                       |
| f6     | exori min                       |
| f7     | utamo tempo                     |
| f8     | utito tempo                     |
| f9     | ring                            |
| f10    | amulet                          |
| f11    | tank ring                       |
| f12    | main ring                       |
| u      | tank amulet                     |
| i      | main amulet                     |
| o      | rope                            |
| p      | shovel                          |
| f      | food                            |

![Default Hotkeys](/docs/assets/images/defaultHotkeys.png)

## Prerequisites

- [`Python`](https://www.python.org/downloads/release/python-3117) 3.11.7
- [`Poetry`](https://python-poetry.org/docs/#installation) >=1.8.2

Install packages before continue

```bash
poetry install
```

# ⌨ Development

## ⚙ Running the app

```bash
poetry run python main.py
```

## 🧪 Running tests

```bash
# unit tests
poetry run python -m pytest

# unit tests with code coverage
poetry run python -m pytest --cov=src
```

# ✅ TODO

- Add logout waypoint
- Add alert when editing specific label already being used
- Avoid inserting duplicate labels on waypoints
- Translate README for Spanish language
- Add api docs
- Add apidocs(github pages) deploy on CI
- Add mypy
- Add mypy to CI
- Add unit tests to CI
- Add screenshot adapter on linux

# 👷 Authors

- [**lucasmonstro**](http://github.com/lucasmonstro)([**linkedin**](https://www.linkedin.com/in/lucasmonstro/)) - Owner & Developer
- [**augustocrmattos**](http://github.com/augustocrmattos)([**linkedin**](https://www.linkedin.com/in/augustocrmattos/)) - Developer
- [**GuizinhoYT**](http://github.com/GuizinhoYT)([**linkedin**](https://www.linkedin.com/in/guilherme-gra%C3%A7a-3953231a2/)) - Tester
- [**lelec0**](https://github.com/lelec0)([**linkedin**](https://www.linkedin.com/in/max-miranda/)) - Tibia mentor
- [**evitarafadiga**](http://github.com/evitarafadiga)([**linkedin**](https://www.linkedin.com/in/lazvsantos/)) - Software Architect

See also the list of [contributors](../../graphs/contributors) who participated
in this project.

If you want to become a contributor, send a message to my [**linkedin**](https://www.linkedin.com/in/lucasmonstro/).

# ❤️ Development inspiration

A special thanks to [**Murilo Chianfa**](https://github.com/MuriloChianfa), the owner of [**TibiaAuto12**](https://github.com/MuriloChianfa/TibiaAuto12). I started this bot especially to overcome [**TibiaAuto12**](https://github.com/MuriloChianfa/TibiaAuto12) slowdowns.

You can check the bot development at [https://twitch.tv/lucasmonstrocs](https://twitch.tv/lucasmonstrocs).

# 📝 License

Copyright © 2023 [**lucasmonstro**](https://github.com/lucasmonstro)  
This project is [MIT](https://opensource.org/licenses/MIT) licensed

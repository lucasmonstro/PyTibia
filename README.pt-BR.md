# 📝 Descrição

> O PyTibia é o Tibia PixelBot mais rápido do mercado, desenvolvido em python para atingir unlocked fps.

_Leia também em outras línguas: [Inglês](README.md), [Português Brasileiro](README.pt-BR.md)._

O BOT trabalha localizando imagens por toda a tela e aplica o cache para ignorar a relocalização de imagens estáticas que já foram capturadas, evitando o uso excessivo de CPU/GPU.

O BOT é baseado em cálculo matricial, paralelismo, pré-processamento e cacheamento. Foi a maneira que eu encontrei para obter a performance(em nanosegundos/microsegundos) necessária e responder em tempo útil em relação ao Tibia.

O BOT utiliza estrutura de dados, vetores, _pathfinding_, etc. e outras funcionalidades importantes para tomada de decisões inteligentes durante a _gameplay_.

O BOT anda pelo teclado e faz movimentação humana através do mouse.

Eu, Lucas, criei essa orquestra de funcionalidades para aprender a linguagem de programação python, fazer _lives_ na Twitch, amigos, enquanto aplico meus conhecimentos de _deep learning_, o já mencionado _pathfinding_, matrizes e mais.

Não, eu **não** pretendo vender uma assinatura para o seu uso, porém ele funcionará no "global" e você muito provavelmente poderá usá-lo, sob sua total responsabilidade.

O BOT não está finalizado e passa por constantes mudanças.

Sinta-se livre para utilizar de qualquer função, criar sua própria versão ou aguardar o lançamento de uma versão inicial.

# 🤖 BearSharp

Devido a compromissos pessoais que demandam minha atenção, estou temporariamente pausando o desenvolvimento do projeto do bot para o Tibia. No entanto, estou feliz em compartilhar que meu amigo tem um projeto fantástico chamado BearSharp, que oferece recursos excelentes e é continuamente atualizado. Enquanto meu projeto estiver inativo, encorajo vocês a conferirem o trabalho excepcional do BearSharp. Tenho certeza de que vocês encontrarão tudo o que precisam e mais lá.

Aqui está o link do discord do BearSharp: https://discord.gg/rqm9E3EGBr

Agradeço pela compreensão e continuo ansioso para retomar meu trabalho assim que possível.

# 🗺️ Recursos

Apenas disponível para knight/palaldin

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

# ⚽ Metas

- Detecção de qualquer informação necessária no cliente em (mili/macro/nano) segundos.
- Controle total sob os píxeis do mouse para a movimentação humanizada.
- Utilizar computação visional para detectar objetos que bloqueiam o caminho do char.
- Utilizar processamento de linguagem natural para falar com outros jogadores.
- Party gameplay.

# 🧰 Instalação

## Opções do Tibia client

Antes de instalar os pacotes do pythons, o PyTibia requer uma configuração necessária para funcionar corretamente com o Tibia client. Por favor, deixa as opções exatamente como nas imagens abaixo:

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

No Tibia client, deixa o painel de skills aberto, a battle list, e deixa a game window na maior resolução, exatamente como na imagem abaixo:

![Client](/docs/assets/images/client.png)

Por enquanto as hotkeys no PyTibia não são configuráveis, é necessário deixar exatamente como a tabela abaixo:

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

## Pré-requisitos

- [`Python`](https://www.python.org/downloads/release/python-3117) 3.11.7
- [`Poetry`](https://python-poetry.org/docs/#installation) >=1.8.2

Antes de continuar instale os seguintes pacotes:

```bash
poetry install
```

# ⌨ Desenvolvimento

## ⚙ Executando a aplicação

```bash
poetry run python main.py
```

## 🧪 Testes de execução

```bash
# testes unitários
poetry run python -m pytest

# testes unitários com cobertura de teste
poetry run python -m pytest --cov=src
```

# ✅ TODO

- Adicionar waypoint de logout
- Adicionar alerta ao editar label de waypoint que já está sendo usada
- Evitar inserir labes duplicados em waypoints
- Traduzir o README para a língua espanhola
- Adicionar api docs
- Adicionar deploy da apidocs(github pages) no CI
- Adicionar mypy
- Adicionar mypy na CI
- Adicionar testes unitários na CI
- Adicionar adaptador de screenshot no linux

# 👷 Autores

- [**lucasmonstro**](http://github.com/lucasmonstro)([**linkedin**](https://www.linkedin.com/in/lucasmonstro/)) - Criador & Desenvolvedor
- [**augustocrmattos**](http://github.com/augustocrmattos)([**linkedin**](https://www.linkedin.com/in/augustocrmattos/)) - Desenvolvedor
- [**GuizinhoYT**](http://github.com/GuizinhoYT)([**linkedin**](https://www.linkedin.com/in/guilherme-gra%C3%A7a-3953231a2/)) - Tester
- [**lelec0**](https://github.com/lelec0)([**linkedin**](https://www.linkedin.com/in/max-miranda/)) - Tibia mentor
- [**evitarafadiga**](http://github.com/evitarafadiga)([**linkedin**](https://www.linkedin.com/in/lazvsantos/)) - Arquiteto de Software

Veja também a lista de [contribuidores](../../graphs/contributors) participantes deste projeto.

Gostaria de fazer parte da equipe? Me contate no [**linkedin**](https://www.linkedin.com/in/lucasmonstro/).

# ❤️ Inspiração

Agradecimentos especiais ao [**Murilo Chianfa**](https://github.com/MuriloChianfa), responsável pelo [**TibiaAuto12**](https://github.com/MuriloChianfa/TibiaAuto12). Eu iniciei o bot para resolver problemas que não foram resolvidos no [**TibiaAuto12**](https://github.com/MuriloChianfa/TibiaAuto12).

Você pode acompanhar o desenvolvimento do bot na minha stream [https://twitch.tv/lucasmonstrocs](https://twitch.tv/lucasmonstrocs).

## 📝 Licença

Copyright © 2023 [**lucasmonstro**](https://github.com/lucasmonstro)  
Este projeto contém a licença [MIT](https://opensource.org/licenses/MIT).

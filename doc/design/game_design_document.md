# Game design document: Project OMG

## Introduction

Project OMG is a 2D top-down, multiplayer, match-based game where players
engage in real-time combat with intelligent bots in interactive environments.
Players will create characters with unique skills and experience synergy between
different abilities to defeat their opponents. The game focuses on strategic
combat, team coordination, and dynamic interactions within the game world.

## Game overview

### Game concept

Project OMG combines strategic depth with fast-paced action in a multiplayer
setting. Players will create characters with distinct classes and abilities,
participating in matches where skill synergy plays a crucial role. The
environment is interactive, with destructible objects that can influence
gameplay. Matches are short, with no progression save, ensuring each game is a
fresh experience.

### Genre

2D top-down, multiplayer, match-based combat.

### Platform

The game will be developed for PC initially, with potential expansion to include
controller support and mobile platforms in the future.

### Target audience

The game is aimed at players aged 12 and above who enjoy fast action-based
combat and multiplayer games, targeting both casual gamers and competitive
players looking for an engaging experience with a mix of PvP (Player vs Player)
and PvE (Player vs Environment) elements.

## Gameplay mechanics

### Core mechanics

- **Match-based gameplay**: Each game session is independent, with no
  progression save. Players engage in short, intense matches.
- **Character creation**: Players can create characters, choosing from various
  classes and skills.
- **Skill synergy**: Combining different skills (e.g., fire + poison) can create
  unique effects and strategies.
- **PvPvE**: Players compete against each other and AI-controlled bots, adding
  an extra layer of challenge.
- **Interactive environment**: The game world includes destructible objects and
  other interactable elements that players can use to their advantage.

### Game flow

1. **Matchmaking**: Players join a lobby and are matched with others.

2. **Character selection**: Players choose or create their characters, selecting
   their class and skills.
3. **Gameplay**: Players engage in combat, using their skills strategically to
   defeat opponents and interact with the environment.
4. **End-game**: Statistics are displayed at the end of each match, showing
   player performance and other metrics.

### Controls

- **Keyboard and mouse**: Primary control method for PC.
- **Optional controller support**: Future updates may include support for game controllers.

## Game world

### Setting and theme

Project OMG is set in a fantastical world with various themed arenas. Each
arena offers unique challenges and opportunities for interaction.

### Levels and environments

The game features multiple arenas, each with destructible objects and
interactive elements that can be used strategically during matches.

## Characters

### Player characters

- **Classes**: Various classes with unique skills and abilities.
- **Skills**: Each class has a set of skills that can be combined for synergy effects.

### Non-player characters (NPCs)

- **Bots**: Intelligent AI-controlled bots that players will compete against in
  addition to other players.

## Story

The game is match-based with no overarching story progression. Each match is a
standalone experience focusing on the core gameplay mechanics and interactions.

## User interface (UI)

### Main menu

- **Lobby**: Join or create a match, view statistics, and manage character settings.

### In-game HUD

- **Health and mana Bars**: Display the player's current health and mana.
- **Skill cooldowns**: Show the cooldown status of the player's skills.
- **Match timer**: Indicates the remaining time in the match.

### Other interfaces

- **End-game statistics**: Detailed statistics displayed at the end of each match.

## Technical specifications

### Software architecture

A monolithic architecture will be used for simplicity, ensuring all components
are integrated into a single codebase.

### Technology stack

- **Programming language**: Python
- **Game engine**: Pygame or a similar Python-based game engine
- **Networking**: WebSockets for real-time communication
- **Database**: TBD

### Performance requirements

- **Frame rate**: Targeting 60 FPS for smooth gameplay.
- **Latency**: Low-latency communication to ensure real-time interactions.

## Art and sound

### Art style

A stylized 2D art style with vibrant colors and detailed environments.

### Sound design

- **Sound effects**: Dynamic and responsive sound effects for skills and
  environment interactions.
- **Music**: Engaging background music that enhances the game’s atmosphere.

## Development plan

### Milestones

1. **Prototype development**: Basic gameplay mechanics and networking.
2. **Alpha version**: Core features, character creation, and matchmaking.
3. **Beta version**: Full feature set, including interactive environments and
   intelligent bots.
4. **Release candidate**: Polishing, optimization, and final testing.
5. **Launch**: Official game release.

### Team roles

- **Software lead**: Responsible for gameplay mechanics and overall game design.
- **Programmers**: Develop the game’s codebase and implement features.
- **Artists**: Create the visual and audio assets, including sound effects and
  music for the game.

## Appendix

Any additional information or references.

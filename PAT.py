"""The Behavior of this code depends on the resolution of the screen that you run it on."""

import numpy
from numpy.random import mtrand
import pygame
from configReader import ConfigReader, ConfigContainer
from src.pat_io import LogWriter
from screens import Background, StartScreen, InstrScreen, PauseScreen, HUD, FinalScreen
from objects import Player, Enemy, Coin
from datetime import date, datetime, time
import sys
from pygame import mixer
from exe import EXE
import time

seed = 0


class PAT:
    """This class contains code that wraps the individual components of the game.
    Most of the code handles the setup and flow from between levels. The game is
    organized by PAT->level->round->agents (player+ai) or PAT->level->questions.
    """

    def __init__(self):
        """PAT is responsible for initiallizing core pygame information and configuration
        variables.
        """

        pygame.init()
        global coin_sound
        path = EXE.resource_path("sounds/coin_sound.mp3")
        coin_sound = pygame.mixer.Sound(path)

        numpy.random.seed(seed)

        self.presetName = "block1"

        self.info = dict()

        self.displayInfo = pygame.display.Info()
        # get resolution of the current display
        self.res = (1920, 1080)
        # initialize game clock
        self.clock = pygame.time.Clock()

        self.time = datetime.now().strftime("%H_%M_%S")

        self.background = Background(self.res)

        self.countdownBackgroundsList = [
            Background(self.res, image="countdown_3.png", isBackground=True),
            Background(self.res, image="countdown_2.png", isBackground=True),
            Background(self.res, image="countdown_1.png", isBackground=True),
            Background(self.res, image="start.png", isBackground=True),
        ]

        # startscreen is responsible for letting the player select which configuration
        # the code is defined in the background.py file
        self.startScreen = StartScreen(self.background)

        while not self.startScreen.finished:
            self.startScreen.mainLoop()
        self.participantID = self.startScreen.name

        # organize levels based on chosen configuration
        self.parseStructure(self.startScreen.chosenStruct)

        print("levels: ", self.levels)

        self.totalRounds = 24  # changed to constant with current study design

        # initiallize logwriter class to track participant responses and inputs
        self.logWriter = LogWriter(self.presetName, self.participantID, self.time, seed)

        instructions = InstrScreen(self.res)

        while not instructions.proceed:
            instructions.mainLoop()

    def parseStructure(self, structName="structure1"):
        """
        It takes a structure name, parses the structure file, and then adds levels to a list.

        Args:
          structName: the name of the structure to parse. Defaults to structure1
        """

        self.mainConfig = ConfigReader.parseToDict("structure")
        self.structure = self.mainConfig[structName]
        self.blocks = self.mainConfig["blocks"]
        self.levels = []
        # loop through the structure and add levels
        for blockType in self.structure:
            block = self.blocks[blockType]["layout"]
            for b in block:
                level = b[0]
                freq = int(b[1])
                for i in range(freq):
                    self.levels.append(level)
        # # DEBUG: Uncomment this to shorten the experiment to a single round for dev purposes
        # self.levels = [self.levels[0]]

    def main_loop(self):
        """
        The main_loop function is called from the main function. It loops through the levels in
        the levels list and calls the main_loop function from the Level class.

        The Level class has a main_loop function that loops through the questions in the level or
        runs a game round with the corresponding manipulation.
        """
        levelnum = 1
        roundsCompleted = 0

        for currLevel in range(len(self.levels)):
            # print(f"The current level is {self.levels[currLevel]}")
            level = Level(
                self,
                self.time,
                self.participantID,
                self.presetName,
                currLevel,
                self.levels,
                self.countdownBackgroundsList,
                roundsCompleted,
                self.totalRounds,
            )

            level.main_loop()
            if "questions" in level.config:
                # questions will occur after, so -1 is "safe"
                self.info[f"questions {levelnum - 1}"] = level.info
                levelnum += 1
            else:
                self.info[f"level {levelnum}"] = level.info
                levelnum += 1
            roundsCompleted = level.prevRoundsCompleted
            # print("writing log")
            self.logWriter.writeLog(self.info)

        final = FinalScreen(self.background)
        final.mainLoop()  # screen will exit pygame when done


class Level:
    def __init__(
        self,
        Pat,
        timestamp,
        patientName,
        presetName,
        level,
        levelList,
        countdownList,
        roundsCompleted,
        totalRounds,
    ):
        """
        It initializes the level, and if it's not a questions level, it initializes the
        groups, coins, and rounds.

        Args:
          Pat: the patient object
          timestamp: the time the game was started
          patientName: the name of the patient
          presetName: the name of the preset file
          level: the current level
          levelList: a list of the levels in the game
        """

        self.Pat = Pat
        self.levelList = levelList
        self.levelNum = level
        self.levels = len(levelList)
        self.config = ConfigReader.parseToDict(f"{levelList[level]}", "levelconfigs")
        self.background = Pat.background
        self.res = Pat.res
        self.pauseFlag = True

        self.countdownList = countdownList
        self.prevRoundsCompleted = roundsCompleted
        self.totalRounds = totalRounds

        self.logWriter = LogWriter(presetName, patientName, timestamp, seed)
        # TODO: MAC issue with write permissions causes game to crash
        self.logWriter.writeSeed()

        self.info = dict()
        # will only be set if it is a 'questions' level

        # not a questions block
        if "questions" not in self.config:
            self.aGroup = pygame.sprite.Group()
            self.eGroup = pygame.sprite.Group()
            self.cGroup = pygame.sprite.Group()

            self.initGroups()
            # keep track of total coins
            self.pCoins = 0
            self.e1Coins = 0
            self.e2Coins = 0
            self.e3Coins = 0

            self.rounds = int(self.config["rounds"])
            self.currRound = 0

    def initGroups(self):
        """
        This function creates the player and three enemies, and adds them to their respective
        groups and starting positions
        """
        self.player = Player(
            self.background,
            self.aGroup,
            (self.res[0] // 4, self.res[1] // 4),
            self.config["playerVel"],
            "p1.png",
        )

        # TODO: change the temporary spawn points of enemies, and change sprite
        self.enemy1 = Enemy(
            "player2",
            self.background,
            self.aGroup,
            self.cGroup,
            (3 * self.res[0] // 4, self.res[1] // 4),
            self.config["enemy1Vel"],
            "p2.png",
        )
        self.enemy2 = Enemy(
            "player3",
            self.background,
            self.aGroup,
            self.cGroup,
            (self.res[0] // 4, 3 * self.res[1] // 4),
            self.config["enemy2Vel"],
            "p3.png",
        )
        self.enemy3 = Enemy(
            "player4",
            self.background,
            self.aGroup,
            self.cGroup,
            (3 * self.res[0] // 4, 3 * self.res[1] // 4),
            self.config["enemy3Vel"],
            "p4.png",
        )

        self.eGroup.add(self.enemy1)
        self.eGroup.add(self.enemy2)
        self.eGroup.add(self.enemy3)

    def returnInfo(self):
        return self.info

    def main_loop(self):
        """
        The function is called when the player presses the spacebar to start the level.

        The function first checks if there are any questions to be asked at the beginning of
        the level. If there are, it creates a PauseScreen object and runs the updateLoop()
        function until the player presses the spacebar to continue.

        If there are no questions, the function runs the main_loop() function of the Round
        class for the number of rounds specified in the config file.

        After each round, the function creates a PauseScreen until the player presses
        the spacebar to continue.

        The function then resets the Round object and starts the next round.

        The function ends when all the rounds are completed.
        """

        # blit questions here if a question block
        if "questions" in self.config:
            levelStartPause = PauseScreen(
                self.levelNum, self.levels, 0, 0, self.background, self.config
            )
            while levelStartPause.paused:
                levelStartPause.updateLoop()
            # record what answers were chosen

            answersDict = dict()
            answersDict["level"] = self.levelNum
            questions = levelStartPause.returnQuestionText()
            answers = levelStartPause.returnAnswerText()

            for i in range(len(questions)):
                answersDict[questions[i]] = answers[i]

            # self.logWriter.writeLevelQA(answersDict)
            self.info = answersDict
        else:
            for currRound in range(self.rounds):
                round = Round(
                    self.Pat, self.levelNum, currRound, self.config, self.totalRounds
                )
                self.countdown(round.agentGroup, round.coinGroup)
                round.updateAgentVelocity()

                while round.inProgress:
                    round.main_loop()

                self.pCoins += round.player.coins
                self.e1Coins += round.enemy1.coins
                self.e2Coins += round.enemy2.coins
                self.e3Coins += round.enemy3.coins
                self.prevRoundsCompleted += 1

                # blit the round completed here
                pauseScreen = PauseScreen(
                    self.levelNum,
                    self.levels,
                    self.prevRoundsCompleted,
                    self.totalRounds,
                    self.background,
                    round.config,
                    round.agentGroup,
                    1,
                )

                while pauseScreen.paused:
                    pauseScreen.updateLoop()

                # save round info
                self.info[f"level {self.levelNum} round {self.currRound}"] = round.info
                self.currRound += 1
                round.reset()

    def countdown(self, agents, coins):
        """
        Blits a countdown screen. Duration is roughly 3 seconds (on my end)
        """
        for curr in self.countdownList:
            prev_time = pygame.time.get_ticks()
            while True:
                curr.draw()
                agents.draw(self.background.screen)
                coins.draw(self.background.screen)
                pygame.display.flip()
                pygame.display.update()
                pygame.event.get()
                if pygame.time.get_ticks() - prev_time > 1000:
                    break

    def reset(self):
        """
        It clears the sprite groups
        """

        pygame.sprite.Group.empty(self.aGroup)
        pygame.sprite.Group.empty(self.eGroup)
        pygame.sprite.Group.empty(self.cGroup)


class Round:
    def __init__(self, Pat, levelNum, roundNum, config, totalRounds):
        """
        It initializes the game

        Args:
          Pat: the main game class
          levelNum: the level number
          roundNum: the current round number
          config: a dictionary of parameters for the level
        """

        # print(f"starting level {levelNum}, round {roundNum}")
        self.coinsLeft = config["numberOfCoins"]
        self.inProgress = True
        self.background = Pat.background
        self.res = Pat.res

        self.config = config
        self.totalRounds = totalRounds

        # ticks in milliseconds
        self.prev_time = pygame.time.get_ticks()
        self.time = 0
        # add time prev and time passed param
        # add calculation/update before player input and pass time
        self.info = dict()
        self.info["level"] = levelNum
        self.info["round"] = roundNum

        self.agentGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        self.coinGroup = pygame.sprite.Group()

        # Pass background and player into HUD
        self.HUD = HUD(self.background, self.agentGroup)
        self.initGroups()

        # set mean acoording to biases:
        meanCoor = (self.res[0] / 2, self.res[1] / 2)

        if config["playerBias"] > 0:
            # print("playerBias detected")

            dx = meanCoor[0] - self.player.x
            dy = meanCoor[1] - self.player.y
            meanCoor = (
                (meanCoor[0] - config["playerBias"] * dx),
                (meanCoor[1] - config["playerBias"] * dy),
            )

        if config["enemy1Bias"] > 0:
            # print("e1 bias")
            dx = meanCoor[0] - self.enemy1.x
            dy = meanCoor[1] - self.enemy1.y
            meanCoor = (
                (meanCoor[0] - config["enemy1Bias"] * dx),
                (meanCoor[1] - config["enemy1Bias"] * dy),
            )

        if config["enemy2Bias"] > 0:
            # print("e2 bias")
            dx = meanCoor[0] - self.enemy2.x
            dy = meanCoor[1] - self.enemy2.y
            meanCoor = (
                (meanCoor[0] - config["enemy2Bias"] * dx),
                (meanCoor[1] - config["enemy2Bias"] * dy),
            )
        if config["enemy3Bias"] > 0:
            # print("e3 bias")
            dx = meanCoor[0] - self.enemy3.x
            dy = meanCoor[1] - self.enemy3.y
            meanCoor = (
                (meanCoor[0] - config["enemy3Bias"] * dx),
                (meanCoor[1] - config["enemy3Bias"] * dy),
            )

        for i in range(int(config["numberOfCoins"])):
            spawnCoord = numpy.random.normal(
                meanCoor[0], self.res[0] / 8
            ), numpy.random.normal(meanCoor[1], self.res[1] / 8)
            while (
                spawnCoord[0] < 100
                or spawnCoord[0] > self.res[0] - 100
                or spawnCoord[1] < 100
                or spawnCoord[1] > self.res[1] - 100
            ):
                spawnCoord = numpy.random.normal(
                    meanCoor[0], self.res[0] / 4
                ), numpy.random.normal(meanCoor[1], self.res[1] / 6)
            coin = Coin(self.coinGroup, self.background, spawnCoord)

        self.info["coin_coordinates"] = [
            [coin.x, coin.y] for coin in self.coinGroup.sprites()
        ]

        for e in self.enemyGroup:
            e.coinObj = e.getNearestCoinCoord(self.coinGroup)
            # print(f"initial objective set to {e.coinObj}")

    def initGroups(self):
        # why is this here twice?
        self.player = Player(
            self.background,
            self.agentGroup,
            (self.res[0] // 8, self.res[1] // 8),
            self.config["playerVel"],
            "p1.png",
            seed,
        )

        # TODO: change the temporary spawn points of enemies, and change sprite
        self.enemy1 = Enemy(
            "Player 2",
            self.background,
            self.agentGroup,
            self.coinGroup,
            (7 * self.res[0] // 8, self.res[1] // 8),
            self.config["enemy1Vel"],
            "p2.png",
            seed,
        )

        self.enemy2 = Enemy(
            "Player 3",
            self.background,
            self.agentGroup,
            self.coinGroup,
            (self.res[0] // 8, 7 * self.res[1] // 8),
            self.config["enemy2Vel"],
            "p3.png",
            seed,
        )

        self.enemy3 = Enemy(
            "Player 4",
            self.background,
            self.agentGroup,
            self.coinGroup,
            (7 * self.res[0] // 8, 7 * self.res[1] // 8),
            self.config["enemy3Vel"],
            "p4.png",
            seed,
        )

        self.enemyGroup.add(self.enemy1)
        self.enemyGroup.add(self.enemy2)
        self.enemyGroup.add(self.enemy3)

    def updateAgentVelocity(self):
        self.player.update_velocity()
        self.enemy1.update_velocity()
        self.enemy2.update_velocity()
        self.enemy3.update_velocity()

    # main loop will check what
    def main_loop(self):

        keys = pygame.key.get_pressed()

        self._update_time()
        self._handle_input(keys)
        self._process_game_logic(keys)
        self._draw()

    def _update_time(self):
        """
        It gets the time passed since the last time the function was called and stores it in
        the variable time_passed
        """
        self.time_passed = pygame.time.get_ticks() - self.prev_time
        self.prev_time = pygame.time.get_ticks()

    def _handle_input(self, keys):
        """
        The player object is passed the keys that are pressed and the time passed since the
        last frame

        Args:
          keys: a list of keys that are currently being pressed
        """

        # player moves with WASD
        self.player.getInput(keys, self.time_passed)

    def _process_game_logic(self, keys):
        # print(self.time)
        """
        The function is called every frame and it checks for collisions between the agents and
        the coins, updates the agents' coin count, and updates the timer

        Args:
          keys: a list of keys that are currently being pressed
        """

        events = pygame.event.get()

        # collisions
        collectFlag = pygame.sprite.groupcollide(
            self.agentGroup, self.coinGroup, False, True
        )
        coins_collected = {}
        # allows us to access and update selected agent coin count
        for agent, coin_list in collectFlag.items():
            if not agent in self.enemyGroup:
                pygame.mixer.Sound.play(coin_sound)

            coins_collected[agent.name] = [
                (coin.x, coin.y) for coin in coin_list if isinstance(coin, Coin)
            ]
            agent.coins += 1
            self.coinsLeft -= 1

        if len(collectFlag) > 0:
            # reupdate the coin objectives
            for e in self.enemyGroup:
                e.setCoinObjective(self.coinGroup)

        for e in self.enemyGroup:
            if self.coinsLeft > 0 and self.time > 10:
                e.optimalMove()

        if self.coinsLeft <= 0 or len(self.coinGroup) == 0:
            print("finished level")
            self.inProgress = False

        for event in events:
            # if event.type == pygame.QUIT:
            #    pygame.quit()
            #    exit()
            if (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):  # Quitting out of fullScreen
                pygame.quit()
                exit()

        # TODO fix time stuff
        self.time += self.time_passed
        # Clock updates
        self.HUD.updateTimer(self.time_passed)
        self.updateInfo(keys, coins_collected)

    def _draw(self):
        """
        _draw() draws the background, the HUD, and the sprites to the screen
        """

        self.background.draw()

        # sprite groups are great because they allow you
        # to draw all sprites of the group at the same time
        self.agentGroup.draw(self.background.screen)
        self.coinGroup.draw(self.background.screen)
        self.HUD.drawHUD()

        pygame.display.flip()
        pygame.display.update()

    def updateInfo(self, keys, coins_collected):
        """
        This function updates the info dictionary with the current time, the number of coins
        left, the number of coins each player has, the keys pressed, and the position of each
        player.

        Args:
          keys: the keys that are pressed
        """

        keysPressedStr = ""

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            keysPressedStr += "up "
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            keysPressedStr += "down "

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            keysPressedStr += "left "
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            keysPressedStr += "right "

        info = dict()
        info["tick"] = str(self.time)
        info["coins left"] = str(self.coinsLeft)
        info["player coins"] = str(self.player.coins)
        info["collected coins"] = coins_collected
        info["keys pressed"] = keysPressedStr
        info["e1 coins"] = str(self.enemy1.coins)
        info["e2 coins"] = str(self.enemy2.coins)
        info["e3 coins"] = str(self.enemy3.coins)
        info["player position"] = str((self.player.x, self.player.y))
        info["enemy1 position"] = str((self.enemy1.x, self.enemy1.y))
        info["enemy2 position"] = str((self.enemy2.x, self.enemy2.y))
        info["enemy3 position"] = str((self.enemy3.x, self.enemy3.y))
        self.info[str(self.time)] = info

    def reset(self):
        pygame.sprite.Group.empty(self.agentGroup)
        pygame.sprite.Group.empty(self.enemyGroup)
        pygame.sprite.Group.empty(self.coinGroup)


if __name__ == "__main__":
    pat = PAT()
    pat.main_loop()

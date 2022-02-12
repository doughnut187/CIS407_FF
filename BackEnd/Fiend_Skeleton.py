"""
Author(s): Niklaas Cotta
Date created: 11/6/21
Team WAHP, CIS422 FA21
Desc:
"""

from time import *
import sys

"""
TODO:
1)
"""

bestiary = {"01": "Baby",
            "02": "Juvenile",
            "03": "Normal",
            "04": "Mature",
            "05": "Magnificent",
            "06": "Geriatric",
            "07": "Ascended"}


def delay_print(s, delay):
    """
    Params:
        s (str) -- string to be printed
        delay (number) -- how much delay for each character
    Desc: Prints out one character at a time
          https://stackoverflow.com/questions/9246076/how-to-print-one-character-at-a-time-on-one-line
    """
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        sleep(delay)


def testFiend():
    """
    Desc: A test for the Fiend() class. tests addition of experience, leveling up, and changing form
          Prints out initial and final stats for comparison
    """
    myFiend = Fiend()
    myFiend.printinfo()
    for i in range(5):
        sleep(0.5)
        print(f"\nStep: {i+1}")
        myFiend.updateXP(50)
    myFiend.printinfo()
    # myFiend.seppuku()


class Level:
    def __init__(self, value=1, xpCap=3, xpPoints=0):
        """
        Params:
            value -- the actual level of the monster
            xpCap -- the amount of xp needed to levelup (dynamic)
            xpPoints -- the amount of xp the monster currently has
        Desc: Creation of Level class, includes associated attributes value, xpCap, xpPoints
        """
        self.value = value
        self.xpCap = xpCap
        self.xp = xpPoints

    def __str__(self):
        """
        Desc: Simply returns a string formatted level value
        """
        return str(self.value)

    def incrementXP(self, value):
        """
        Params:
            value (int) -- the amount of experience you want to be added to the fiend
        Desc: (NOTE: only for positive increases, currently does not handle negative numbers).
              First adds all the experience. Loops while level-up can still occur. If the xpCap is reached,
              it calls levelUp() to increase the level, and the xpCap is then reset. Returns how much the monster's
              level increase by.
        """
        done = False
        oldLevel = self.value

        print(f"EXP increased by {value} points!")
        self.xp += value

        while not done:
            prevLevel = self.value

            if self.xp >= self.xpCap:  # levelup
                self.levelUp()
                print(f"LEVELED UP TO LEVEL {str(self.value)}!!!")

            if self.value == prevLevel:
                done = True

            sleep(0.25)

        return self.value - oldLevel  # how much you leveled up

    def levelUp(self):
        """
        Desc: setter that increases the level, keeps track of experience, and then resets the xpCap with xpCap()
        """
        self.value += 1
        self.xp -= self.xpCap
        self.resetCap()

    def resetCap(self):
        """
        Desc: setter that resets the xpCap. Called on level-up. Calculation is from fast-leveling pokemon from the game
        series, Pokemon.
        """
        self.xpCap = ((4 * self.value ** 3) // 5)


class Fiend:
    def __init__(self, nickname="Lil Klokov", species="Kettlehell", species_id="KM01", level=1):
        """
        Params:
            nickname (str) -- the nickname the user wants to give the monster
            species (str) -- the colloquial name of the species
            species_id (str) -- the species_id for backend. Form is as follows:
                                1st/2nd char -- monster species abbreviation
                                3rd/4th char -- what form the monster is in in number form
            level (level obj) -- level object associated with monster. Defaults to level 1
        """
        self.nickname = nickname
        self.species = species
        self.id = species_id
        self.level = Level(level)

    def dance(self):
        """
        Desc: Test method to tell the monster to do something
        """
        print(f"{self.nickname} does a little dance and looks very cute doing it")

    def tellLevel(self):
        """
        Desc: getter method for obtaining the level of the monster
        """
        return self.level.value

    def updateXP(self, value):
        """
        Params:
            value (int) -- the amount of experience you want to be added to the fiend
        Desc: method wrapper for incrementXP from level class. incrementXP() handles adding xp, leveling up, and
        resetting the cap. Then handles the evolution of the monster. On level-up, checks if monster is ready to
        evolve (currently set to every 5th level). If it is, updates the monster's form with transform()
        """
        leveled = self.level.incrementXP(value)
        evolveLevel = 5
        toEvolve = self.level.value % evolveLevel
        if toEvolve == 0 and leveled > 0:
            self.transform()

    def transform(self):
        """
        Desc: generic handler for changing a monsters form. Currently only associated with evolution, but can be
        adapted to change species as well. First updates the form portion (second half) of the species_id by
        incrementing by 1. Then it returns the new species ID. The species here does not change, only the form.
        """
        print(f"{self.nickname} is evolving!!!")
        for _ in range(3):
            sleep(0.5)
            print("  .  ")

        newFormInt = int(self.id[3]) + 1
        self.id = self.id[0:3] + str(newFormInt) + self.id[4:]  # dont ask me
        print(f"{self.species} grew into it's {bestiary[self.id[2:]]} form!!!")

        return self.species

    def seppuku(self):
        """
        Desc: the monster kills (deletes) itself. For cleanup purposes
        """
        delay_print("私は名誉をもって人生を送ってきました。 私は何も後悔していない...\n", 0.15)
        sleep(1)
        delay_print("死  DEATH  死\n", 0.25)
        sleep(1)
        del self

    def printinfo(self):
        """
        Desc: Prints out several attributes of the fiend. Mostly for testing purposes
        """
        print("==========================================")
        print(f"Name:     {self.nickname}")
        print(f"Species:  {self.species} ({bestiary[self.id[2:]]})")
        print(f"Level:    {str(self.level.value)} (xp: {str(self.level.xp)}/{str(self.level.xpCap)})")
        print("==========================================\n")


if __name__ == '__main__':
    testFiend()

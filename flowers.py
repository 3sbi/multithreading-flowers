from threading import Thread, Lock
from time import sleep
import random


class bcolors:
    RED = '\033[31m'
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class Gardener:
    id: int

    def __init__(self, id):
        self.id = id


mutex_gardeners = Lock()
mutex_flowers = Lock()
mutex_print_to_cli = Lock()
days: int = 0
days_total: int = 0
indexes_for_gardeners: list[int] = []
flowers: list[int] = []
work_is_done: bool = True


def getInput():
    value = input()
    while not value.isnumeric():
        value = input("Input must be a positive number, enter again: ")
    return int(value)


def gardenerWork(gardener: Gardener):
    global days
    global indexes_for_gardeners
    while (days):
        sleep(2)
        if len(indexes_for_gardeners) >= 2:
            with mutex_gardeners:
                index: int = indexes_for_gardeners[0]
                with mutex_print_to_cli:
                    id: int = gardener.id
                    print(
                        bcolors.GREEN+"Gardener #{} waters flower #{}".format(id, index+1)+bcolors.ENDC)
                flowers[index] = 0
                indexes_for_gardeners.remove(index)
                sleep(1)
            continue
        with mutex_gardeners:
            if len(indexes_for_gardeners) != 0:
                index: int = indexes_for_gardeners[0]
                with mutex_print_to_cli:
                    id: int = gardener.id
                    print(
                        bcolors.GREEN+"Gardener #{} waters flower #{}".format(id, index+1)+bcolors.ENDC)
                flowers[index] = 0
                indexes_for_gardeners.pop(0)
                sleep(1)


def flowersWilting():
    global days
    global flowers
    global indexes_for_gardeners
    global work_is_done
    global days_total
    while (days):
        day_number = days_total-days+1
        if work_is_done:
            print(bcolors.BOLD+"day #{}".format(day_number)+bcolors.ENDC)
            work_is_done = False
            flowers_len = len(flowers)
            indexes_of_flowers_to_wilt = random.sample(
                range(0, flowers_len), random.randint(1, flowers_len))
            print("today" + bcolors.BOLD+" {} ".format(len(indexes_of_flowers_to_wilt))+bcolors.ENDC +
                  "flowers will wilt")
            for index in indexes_of_flowers_to_wilt:
                sleep(1)
                with mutex_flowers:
                    flowers[index] = 1
                    with mutex_print_to_cli:
                        print(bcolors.YELLOW +
                              "flower #{} is wilting".format(index+1)+bcolors.ENDC)
                    indexes_for_gardeners.append(index)
        if len(indexes_for_gardeners) == 0:
            days = days - 1
            work_is_done = True
            print(bcolors.BOLD+"end of day #{}".format(day_number) +
                  bcolors.ENDC, end="\n\n")


def main():
    global days
    global days_total
    global flowers
    print("Enter number of days:", end=" ")
    days = getInput()
    days_total = days
    print("Enter number of flowers:", end=" ")
    number_of_flowers: int = getInput()
    gardener1 = Gardener(1)
    gardener2 = Gardener(2)
    flowers = [0]*number_of_flowers
    flowersThread = Thread(target=flowersWilting)
    gardener1Thread = Thread(target=gardenerWork, args=(gardener1,))
    gardener2Thread = Thread(target=gardenerWork, args=(gardener2,))
    flowersThread.start()
    gardener1Thread.start()
    gardener2Thread.start()
    flowersThread.join()
    gardener1Thread.join()
    gardener2Thread.join()
    print(bcolors.BOLD + bcolors.GREEN +
          "All flowers are watered and happy =)"+bcolors.ENDC+bcolors.ENDC)


if __name__ == "__main__":
    main()

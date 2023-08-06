import argparse
import os
import random as ro
import sys

from requests import get

__version__ = "1.1.1"


def checkip():
    url = 'https://checkip.amazonaws.com/'
    response = get(url).text
    print(f'Public IP Address: {response}')


def cow_bull(n_sample, n_digits):
    guess_n = input("enter a number you guess: ").zfill(n_digits)
    if 'answer' in guess_n:
        print("""
        >>>>> 
           Do you really want to give up?
                Don't Give Up!!
                I know you Can do it!
                                           <<<<<<
        """)
        yn = (input("y/n : ").lower()).strip()
        if ('yes' == yn) or ('y' == yn):
            return 'answer'
        else:
            guess_n = input("enter a number you guess: ").zfill(n_digits)
    guess_n_list = list(str(guess_n))
    if len(guess_n_list) != len(set(guess_n_list)):
        print("Duplicates are not allowed!")
        return -1
    if len(guess_n) != n_digits:
        print(f"Only {n_digits} digits are allowed!")
        return -1
    cow = 0
    bull = 0
    for i in guess_n_list:
        if int(i) in n_sample:
            cow += 1

    for i in range(n_digits):
        if n_sample[i] == int(guess_n_list[i]):
            bull += 1
            cow -= 1

    print("Cow : {0},Bull : {1}".format(cow, bull))
    return int(guess_n)


def play():
    print(r"""
            ##############--->>> Rules: <<---################
            #   Note:                                       #
            #       Bulls = correct code, correct position. #
            #       Cows = correct code, wrong position.    #
            #################################################
            """)

    try:
        n_digits = int(input("how many digits number you need? "))
        if n_digits >= 10:
            raise Exception("Up to 10-digits number are allowed!")
        if not type(n_digits) is int:
            raise TypeError("Only integers are allowed")
        if n_digits < 0:
            raise Exception("Sorry, no numbers below zero")
        n_sample = ro.sample(range(10), n_digits)
        # print(n_sample)
        ans_list = map(str, n_sample)
        answer = ''.join(ans_list)
        ans = cow_bull(n_sample, n_digits)
        count = 1
        while ans != int(answer):
            ans = cow_bull(n_sample, n_digits)
            count += 1
            if "answer" == ans:
                print(r"""
                        |---------------------------------------|
                                        YOU LOST!                 
                            * Answer is "{}"
                            * Number of attempts are {}
                            * Because you used cheat code!!       
                        |---------------------------------------|   
                                """.format(answer, count))
                sys.exit(0)

        print(r"""
                        |-------------------------------|
                                    YOU WON!                 
                          * Answer is "{}"
                          * Number of attempts are {}       
                        |-------------------------------|   
                        """.format(answer, count))
    except Exception as e:
        print("Error : ", e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version", help="show program version", action="store_true")
    parser.add_argument("-n", "--name", help="output Hello Name! or Hello World!", nargs='*',
                        type=str, )
    parser.add_argument("-ip", "--checkip", help="This will check public IP address of system", action="store_true")
    parser.add_argument("-g", "--playgame", help="You can play Bulls and Cows game", action="store_true")

    # Read arguments from the command line
    args = parser.parse_args()

    # Check for --version or -V
    if args.name:
        print(f'Hello {str(" ".join(args.name)).title()}!')
    # Check for --name or -n
    elif args.version:
        print(f"Version-{__version__}")
    # Check for --checkip or -ip
    elif args.checkip:
        checkip()
    # Check for --playgame or -g
    elif args.playgame:
        os.system('cls||clear')  # Clearing the terminal screen
        play()
    else:
        print("Hello World Py!")


if __name__ == "__main__":
    main()

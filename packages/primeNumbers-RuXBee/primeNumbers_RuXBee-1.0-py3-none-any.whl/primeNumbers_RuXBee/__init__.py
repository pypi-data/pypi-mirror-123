"""
numerosPrimos
=====

Provides
  1. Subroutine that has a "n" number for parameter, and 
  returns a list of prime numbers samaller than parameter.
  2. Subroutine that asks for a number and returns a list of 
  prime number smaller.
"""


def returns_list_prime_numbers(n):
    print("PARAMETER:", n)
    list_result = [2]
    if n > 1:
        for i in range(2, n+1):
            result = False
            for x in range(2,i):
                #print(i,x)
                if i%x != 0:
                    #print(i)
                    result = True
                    break
                else:
                    result = False
                    break
            if result == True:
                list_result.append(i)
        print(f"PRIMES LIST: {list_result}")
    else:
        print("Enter number bigger than 1")


def ask_user_for_a_number_and_returns_list_prime_numbers():
    n = int(input("Enter a Integer Number:"))
    print("NUMBER:", n)
    if n > 1:
        list_result = [2]
        for i in range(2, n+1):
            result = False
            for x in range(2,i):
                #print(i,x)
                if i%x != 0:
                    #print(i)
                    result = True
                    break
                else:
                    result = False
                    break
            if result == True:
                list_result.append(i)
        print(f"PRIMES LIST: {list_result}")
    else:
        print("Enter number bigger than 1")

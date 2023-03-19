# this project checks if your password has been hacked before and then shows your how many times your passowrd has been hacked

import requests  # allows us to make a request i.e like a browser
import hashlib  # bulit-in module that allows you to perform hashing
import sys


def request_api_data(query_char):  # function requests the 5 keys of our password

    # this API uses something called hashing , we gave the first 5 keys of our password
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)

    if res.status_code != 200:  # response[400] is bad , response[200] is good
        raise RuntimeError(
            f"Error fetching: {res.status_code} check the API and try again")
    return res


def get_password_leaks_count(hashes, hash_to_check):

    hashes = (line.split(':') for line in hashes.text.splitlines())

    for hash, count in hashes:
        if hash == hash_to_check:
            return count
    return 0


# check if our password exits in API response
def pwned_api_check(password):

    # we encode the password with `utf-8` and pass is through a hexdigets with reutrns a hexidecimal passowrd which we make uppercase
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    # store the 5 first characters , then rest of the characters
    first_5_char, tail = sha1password[:5], sha1password[5:]

    response = request_api_data(first_5_char)

    # get a response of all passowrds that match our first 5 characters
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(
                f"{password} was found {count} times .... you should probabaly change your password, lol")

        else:
            print(f"The password: {password} , was not found, carry on")

    return "dOnE !"


if __name__ == "__main__":
    # allows us to check an ulmited amount of passowrs
    sys.exit(main(sys.argv[1:]))

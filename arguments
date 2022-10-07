# Do not modify these lines
__winc_id__ = "7b9401ad7f544be2a23321292dd61cb6"
__human_name__ = "arguments"

# Add your code after this line
from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from unicodedata import name


def main():
    print(greet())
    print(force())
    print(pull())


def greet(name, greeting="Hello, <name>!"):
    return greeting.replace("<name>", name)


def force(mass, body="earth"):
    gravity = {
        "sun": 274.0,
        "jupiter": 24.9,
        "neptune": 11.2,
        "saturn": 10.4,
        "earth": 9.8,
        "uranus": 8.9,
        "venus": 8.9,
        "mars": 3.7,
        "mercury": 3.7,
        "moon": 1.6,
        "pluto": 0.6,
    }
    force = mass * gravity[body]
    return force


def pull(m1, m2, d):
    gravitational_constant = 6.674 * 10**-11
    pull = gravitational_constant * ((m1 * m2) / d**2)
    return pull


if __name__ == "__main__":
    main()

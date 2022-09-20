from environment import Environment


def main():
    env = Environment()
    while True:
        env.simulate_generation()


if __name__ == "__main__":
    main()

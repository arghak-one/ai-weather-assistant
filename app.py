from agent import ask_weather_ai

def main():

    print("🌤 AI Weather Assistant")
    print("Type 'exit' to quit\n")

    while True:

        user_input = input("Ask about weather: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        result = ask_weather_ai(user_input)

        print("\nResult:")
        print(result)
        print()


if __name__ == "__main__":
    main()
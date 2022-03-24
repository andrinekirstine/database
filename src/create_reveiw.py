import argparse
if __name__ == "__main__":
  parser = argparse.ArgumentParser("Coffe Review Creator")
  parser.add_argument("--username", help="The username under which the review is stored")
  parser.add_argument("--coffee-name", help="Name of coffee")
  arguments = parser.parse_args()

  # Nå har arguments masse data som du kan bruke slik:
  print(arguments.username)
  print(arguments.coffee_name)

  
import argparse
if __name__ == "__main__":
  parser = argparse.ArgumentParser("Kaffesmaking Creator")
  parser.add_argument("--brukernavn", help="Brukernavnet det blir lagret under")
  parser.add_argument("--kaffenavn", help="Navnet på kaffen")
  parser.add_argument("--poeng", help="Poeng på kaffesmaken")
  parser.add_argument("--brenneri", help="Navnet på brenneriet")
  parser.add_argument("--smaksnotat", help="Notater om kaffen")

  arguments = parser.parse_args()

  # Nå har arguments masse data som du kan bruke slik:
  print(arguments.brukernavn)
  print(arguments.kaffenavn)
  print(arguments.poeng)
  print(arguments.brenneri)
  print(arguments.smaksnotat)

  
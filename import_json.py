import json
import logging
import database

logging.basicConfig(
    filename="gamesync.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def import_games():
    try:
        with open("games.json", "r", encoding="utf-8") as file:
            games = json.load(file)

        if not isinstance(games, list):
            raise ValueError("JSON file must contain a list of games")

        database.init_db()

        imported = 0
        skipped = 0

        for game in games:
            if not isinstance(game, dict):
                raise ValueError("Each game must be a JSON object")

            if not game.get("title") or not game.get("genre"):
                raise ValueError("Each game needs a title and genre")

            if database.add_game("games_a", game):
                imported += 1
                logging.info("Imported game: %s", game["title"])
            else:
                skipped += 1
                logging.warning(
                    "Game already exists: %s", game["title"]
                )

        print(
            f"Import completed. Added: {imported}, skipped: {skipped}"
        )

    except (OSError, json.JSONDecodeError, ValueError) as error:
        logging.error("Import failed: %s", error)
        print(f"Import failed: {error}")

    except Exception as error:
        logging.error("Unexpected import error: %s", error)
        print(f"Import failed. Check gamesync.log: {error}")

if __name__ == "__main__":
    import_games()
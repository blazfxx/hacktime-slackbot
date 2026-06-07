import os
import random
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from tictactoe import TicTacToe, format_board
import requests

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])

active_games: dict[str, TicTacToe] = {}


@app.command("/3t")
def tictactoe(ack, respond, command):
    ack()
    channel = command["channel_id"]
    text = command.get("text", "").strip().lower()
    parts = text.split()
    action = parts[0] if parts else ""

    if action == "start":
        active_games[channel] = TicTacToe()
        respond(
            "TicTacToe game started. You are the Xs\n"
            "For you to move, do /3t move <and anything between 1-9>\n\n"
            + format_board(active_games[channel].board)
        )
        return

    if action == "move":
        if channel not in active_games:
            respond("No games rn. Start one with /3t start")
            return

        game = active_games[channel]

        if len(parts) < 2 or not parts[1].isdigit():
            respond("Do: '/3t move <1-9>'")
            return

        pos = int(parts[1]) - 1
        if pos < 0 or pos > 8:
            respond("Position has to be between 1 and 9")
            return

        ok, err = game.player_move(pos)
        if not ok:
            respond(f"Invalid move: {err}")
            return

        board_str = format_board(game.board)

        if game.check_winner("X"):
            respond(f"You won!\n\n{board_str}")
            del active_games[channel]
            return

        if game.is_draw():
            respond(f"It is a draw\n\n{board_str}")
            del active_games[channel]
            return

        bot_pos = game.bot_move()
        board_str = format_board(game.board)

        if game.check_winner("O"):
            respond(f"Bot won... oops :(\n\n{board_str}")
            del active_games[channel]
            return

        if game.is_draw():
            respond(f"It is a draw\n\n{board_str}")
            del active_games[channel]
            return

        respond(f"You moved, bot played {bot_pos + 1}.\n\n{board_str}")
        return

    if action == "quit":
        if channel in active_games:
            del active_games[channel]
            respond("Game quit")
        else:
            respond("No active game")
        return

    respond("Unknown command. Try:\n• `/3t start`\n• `/3t move <1-9>`\n• `/3t quit`")




CHOICES = ["rock", "paper", "scissors"]
EMOJI = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}


@app.command("/blaze-rps")
def rps(ack, respond, command):
    ack()
    user_choice = command.get("text", "").strip().lower()
    if user_choice not in CHOICES:
        respond("Usage: `/blaze-rps rock|paper|scissors`")
        return
    bot_choice = random.choice(CHOICES)
    u, b = EMOJI[user_choice], EMOJI[bot_choice]
    if user_choice == bot_choice:
        result = "It is a tie!"
    elif BEATS[user_choice] == bot_choice:
        result = "You win!"
    else:
        result = "You lost..."
    respond(f"You: {u} *{user_choice.capitalize()}*  vs  Bot: {b} *{bot_choice.capitalize()}*\n{result}")

@app.command("/blaze-flip")
def flip(ack, body, logger, respond):
    ack()
    logger.info(body)
    result = random.choice(["Heads 🪙", "Tails 🪙"])
    respond(f"*Coin flip:* {result}")



@app.command("/blaze-ask")
def blaze_ask(ack, respond, command):
    ack()
    question = command.get("text", "").strip()
    if not question:
        respond("Do: '/blaze-ask <whatever>'")
        return
    try:
        response = requests.post(
            f"{os.environ['AI_BASE_URL']}/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ['AI_API_KEY']}",
                "Content-Type": "application/json",
            },
            json={
                "model": os.environ["AI_MODEL"],
                "messages": [{"role": "user", "content": question}],
                "max_tokens": 1024,
            }
        )
        print("Status:", response.status_code)
        print("Raw response:", response.text)
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        respond(f"*You: {question}*\n\n*gemma-3n-e2b-it:*\n{answer}")
    except Exception as e:
        respond(f"Error: {e}")
        print("Exception:", e)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    print("Bot is running!")
    handler.start()
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Stan gry
hidden_word = "python"
max_attempts = 5
attempts_left = max_attempts
guessed_letters = []

@app.get("/start")
async def start_game():
    global hidden_word, attempts_left, guessed_letters
    hidden_word = "python"  # Możesz dostosować słowo
    attempts_left = max_attempts
    guessed_letters = []
    return {"message": "Gra rozpoczęta! Odgadnij ukryte słowo."}

@app.post("/guess")
async def make_guess(letter: str):
    global attempts_left, guessed_letters

    if attempts_left <= 0:
        raise HTTPException(status_code=400, detail="Gra już się skończyła.")

    if len(letter) != 1 or not letter.isalpha():
        raise HTTPException(status_code=400, detail="Podaj pojedynczą literę.")

    letter = letter.lower()

    if letter in guessed_letters:
        raise HTTPException(status_code=400, detail=f"Litera '{letter}' została już odgadnięta.")

    guessed_letters.append(letter)

    if letter not in hidden_word:
        attempts_left -= 1

    game_result = get_game_result()
    return {
        "attempts_left": attempts_left,
        "guessed_letters": guessed_letters,
        "game_result": game_result,
    }

def get_game_result():
    global hidden_word, guessed_letters, attempts_left
    if set(guessed_letters) >= set(hidden_word):
        return "Wygrana! Odgadłeś słowo."
    elif attempts_left <= 0:
        return f"Przegrana! Ukryte słowo to: {hidden_word}"
    else:
        return "Trwa gra."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

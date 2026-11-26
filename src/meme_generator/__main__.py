import os

import uvicorn


def main() -> None:
    uvicorn.run(
        "meme_generator.app:app",
        host=os.environ.get("MEME_HOST", "127.0.0.1"),
        port=int(os.environ.get("MEME_PORT", "8000")),
    )


if __name__ == "__main__":
    main()

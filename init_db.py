from db import engine, Post

Post.metadata.create_all(engine)

if __name__ == "__main__":
    Post.metadata.create_all(engine)
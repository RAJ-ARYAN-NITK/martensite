from db import engine, Base
import models.driver  # noqa - ensures models are registered
import models.order   # noqa

def init():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done! Tables created in Supabase ✅")

if __name__ == "__main__":
    init()
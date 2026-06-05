from db import engine, Base
import models.driver  
import models.order   

def init():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done! Tables created in Supabase ")

if __name__ == "__main__":
    init()

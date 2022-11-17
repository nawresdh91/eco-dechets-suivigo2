import pickle
from pathlib import Path

import streamlit_authenticator as stauth

from database import Database

names = ["Scoty Loumbou"]
usernames = ["scoty.loumbou@eco-dechets.fr"]
passwords = ["password"]

hashed_passwords = stauth.Hasher(passwords).generate()
print(hashed_passwords)

# save the credentials
for (name, username, hashed_password) in zip(names, usernames, hashed_passwords):
    db = Database()
    db.insert_user(password=hashed_password, email=username, name=name)


file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)

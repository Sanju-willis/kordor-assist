# 📄 .gitignore rules (explained)
scripts/                      # Ignore 'scripts' folder in root
.scripts/                     # Ignore hidden '.scripts' folder
scripts                       # Ignore any file/folder named 'scripts' (anywhere)
git log --oneline             # List commits
git checkout <commit_hash>    # Checkout that commit temporarily

# start up
source .venv/Scripts/activate
uvicorn src.main:app --reload

# add dependencies to requirement txt
pip list --not-required --format=freeze > requirements.txt


# Dependencies 
1. pip install -e .


PYTHONPATH=. python scripts/insert_conversation.py
PYTHONPATH=./ python scripts/view_checkpoints.py


# emogies  
  
main - 🚀
app - 📋

route - 1️⃣🔀
controller - 2️⃣🕹️
service - 3️⃣🔧
database - 4️⃣🗄️

home 🏠
nodes - 🚦🧩
agents - 🤖
tools - 🛠️
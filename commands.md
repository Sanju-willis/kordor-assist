# start up
poetry run dev
poetry run uvicorn app.main:app --reload

# Git Bash / CMD
poetry run python -m app.main



poetry run uvicorn app.main:app --reload --no-access-log --log-level warning

PYTHONPATH=. python scripts/insert_conversation.py
PYTHONPATH=./ python scripts/view_checkpoints.py
$ python scripts/show_checkpoint_columns.py
poetry run python scripts/view_checkpoints.py



# Dependencies 
1. pip install -e .
2. pip list --not-required --format=freeze > requirements.txt



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

# settings. VS code 
1. settings.json
2. **/.gitignore - exclude



# 📄 .gitignore rules (explained)
scripts/                      # Ignore 'scripts' folder in root
.scripts/                     # Ignore hidden '.scripts' folder
scripts                       # Ignore any file/folder named 'scripts' (anywhere)
git log --oneline             # List commits
git checkout <commit_hash>    # Checkout that commit temporarily

# Old Start up pip
source .venv/Scripts/activate
uvicorn src.main:app --reload
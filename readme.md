# SIH Python Backend

Backend Server written using fastapi. Deployed on Render.
Make sure you dont push the code in master branch!

## Getting Started

Contributors need to install Python & Git before they can run your API.
1. Clone the Repository.
```bash
git clone https://github.com/adityaiiitr/sih-python-backend.git
```
2. Move inside working directory.
```bash
cd sih-python-backend
```
3. Setup Python Virtual Environment (Windows setup).
```bash
python -m venv myvenv
```
4. Activate Virtual Environment.
```bash
myvenv\Scripts\activate
```

5. Install Python Libraries.
```bash
pip install -r requirements.txt
```
6. Run local server.
```bash
uvicorn main:app --reload --port 3000
```

Server is up and running on [localhost:3000](localhost:3000)

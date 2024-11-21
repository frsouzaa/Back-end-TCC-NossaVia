from dotenv import load_dotenv
from src.jobs.curtidas import run as run_curtidas
from src.jobs.pontuacao import run as run_pontuacao

load_dotenv()

run_curtidas()
run_pontuacao()

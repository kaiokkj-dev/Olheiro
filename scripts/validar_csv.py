"""Valida a planilha candidaturas.csv do Olheiro.

Uso:
    python scripts/validar_csv.py candidaturas.csv

Sai com código 1 se encontrar erro. Avisos (ex.: status antigos) não falham.
Só usa a biblioteca padrão do Python.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

COLUNAS = [
    "data", "empresa", "vaga", "plataforma", "link", "modelo", "local", "bolsa",
    "nota", "status", "motivo", "proxima_etapa", "prazo", "observacoes",
]
STATUS = {
    "candidatada", "aguardando_voce", "precisa_voce", "descartada",
    "teste", "entrevista", "aprovada", "reprovada", "encerrada",
}
# Nomes usados em versões antigas (com o nome da pessoa no status).
STATUS_ANTIGOS = re.compile(r"^(aguardando|precisa)_\w+$")
DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validar(caminho: Path) -> tuple[list[str], list[str]]:
    erros: list[str] = []
    avisos: list[str] = []
    with caminho.open(encoding="utf-8", newline="") as f:
        leitor = csv.reader(f)
        try:
            cabecalho = next(leitor)
        except StopIteration:
            return ["arquivo vazio"], []
        if [c.strip().lstrip("﻿") for c in cabecalho] != COLUNAS:
            erros.append(f"cabeçalho diferente do esperado: {','.join(COLUNAS)}")
            return erros, avisos

        links: dict[str, int] = {}
        for n, linha in enumerate(leitor, start=2):
            if not any(c.strip() for c in linha):
                continue
            if len(linha) != len(COLUNAS):
                erros.append(f"linha {n}: {len(linha)} colunas (esperado {len(COLUNAS)}); falta aspas num campo com vírgula?")
                continue
            r = dict(zip(COLUNAS, linha))

            if not DATA.match(r["data"]):
                erros.append(f"linha {n}: data '{r['data']}' fora do formato AAAA-MM-DD")
            if not r["empresa"].strip():
                erros.append(f"linha {n}: empresa vazia")

            status = r["status"].strip()
            if status not in STATUS:
                if STATUS_ANTIGOS.match(status):
                    avisos.append(f"linha {n}: status antigo '{status}' (use aguardando_voce / precisa_voce)")
                else:
                    erros.append(f"linha {n}: status '{status}' desconhecido")

            nota = r["nota"].strip()
            if nota:
                if not nota.isdigit() or not 0 <= int(nota) <= 100:
                    erros.append(f"linha {n}: nota '{nota}' deve ser um número de 0 a 100")
                elif status == "descartada" and int(nota) >= 60:
                    avisos.append(f"linha {n}: descartada com nota {nota} (>= 60); o motivo explica?")

            if status in {"descartada", "precisa_voce"} and not r["motivo"].strip():
                erros.append(f"linha {n}: status '{status}' sem motivo")

            link = r["link"].strip()
            if link:
                if not link.startswith(("http://", "https://")):
                    erros.append(f"linha {n}: link não começa com http(s)://")
                elif link in links:
                    avisos.append(f"linha {n}: mesmo link da linha {links[link]} (vaga repetida?)")
                else:
                    links[link] = n

            prazo = r["prazo"].strip()
            if prazo and re.match(r"^\d{4}-", prazo) and not DATA.match(prazo[:10]):
                erros.append(f"linha {n}: prazo '{prazo}' parece data mas não está em AAAA-MM-DD")
    return erros, avisos


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    caminho = Path(sys.argv[1])
    if not caminho.is_file():
        print(f"arquivo não encontrado: {caminho}")
        return 2
    erros, avisos = validar(caminho)
    for a in avisos:
        print(f"aviso: {a}")
    for e in erros:
        print(f"ERRO: {e}")
    print(f"{caminho.name}: {len(erros)} erro(s), {len(avisos)} aviso(s)")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())

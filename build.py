"""
build.py — Le a planilha Excel e gera data.json para o dashboard.

Uso: python build.py
Isso e chamado automaticamente por atualizar_dashboard.bat.
Tambem roda no GitHub Actions quando voce sobe a planilha.
"""
import json
import os
import sys
from datetime import datetime, date

try:
    import openpyxl
except ImportError:
    print("ERRO: biblioteca openpyxl nao instalada.")
    print("Rode uma vez: py -m pip install openpyxl")
    sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(HERE, "Financeiro - FEIRA DE MERCADO.xlsx")
OUT_PATH = os.path.join(HERE, "data.json")


def cell(ws, coord):
    v = ws[coord].value
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    return v


def to_num(v, default=0):
    if v is None:
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def build():
    if not os.path.exists(XLSX_PATH):
        print(f"ERRO: nao achei a planilha em {XLSX_PATH}")
        sys.exit(1)

    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)

    # ===== Parametros =====
    ws = wb["Parâmetros"]
    parametros = {
        "data_base": cell(ws, "C6"),
        "data_evento_1": cell(ws, "C7"),
        "data_evento_2": cell(ws, "C8"),
        "margem_seguranca": to_num(cell(ws, "C11")),
        "saldo_inicial": to_num(cell(ws, "C12")),
        "pct_pago_contratacao": to_num(cell(ws, "C13")),
        "ejs": [cell(ws, "C18"), cell(ws, "C19")],
    }

    # Tabela de pacotes (linhas 23..27)
    pacotes = []
    for r in range(23, 28):
        nome = cell(ws, f"B{r}")
        if not nome:
            continue
        pacotes.append({
            "nome": nome,
            "preco_tabela": to_num(cell(ws, f"C{r}")),
            "preco_minimo": to_num(cell(ws, f"D{r}")),
            "cotas_totais": int(to_num(cell(ws, f"E{r}"))),
            "custo_estande": to_num(cell(ws, f"F{r}")),
            "margem_unitaria": to_num(cell(ws, f"G{r}")),
            "faturamento_maximo": to_num(cell(ws, f"H{r}")),
        })
    parametros["pacotes"] = pacotes

    # ===== Vendas =====
    ws = wb["Vendas"]
    vendas = []
    r = 5
    while True:
        empresa = cell(ws, f"C{r}")
        if not empresa:
            r += 1
            if r > 50:
                break
            continue
        ej = cell(ws, f"B{r}")
        if not ej:
            r += 1
            continue
        vendas.append({
            "ej": ej,
            "empresa": empresa,
            "pacote": cell(ws, f"D{r}"),
            "preco_tabela": to_num(cell(ws, f"E{r}")),
            "status": cell(ws, f"F{r}"),
            "valor_contratado": to_num(cell(ws, f"H{r}")),
            "custo_estande": to_num(cell(ws, f"I{r}")),
            "margem": to_num(cell(ws, f"J{r}")),
            "p1_data": cell(ws, f"K{r}"),
            "p1_valor": to_num(cell(ws, f"L{r}")),
            "p2_data": cell(ws, f"M{r}"),
            "p2_valor": to_num(cell(ws, f"N{r}")),
            "p3_data": cell(ws, f"O{r}"),
            "p3_valor": to_num(cell(ws, f"P{r}")),
            "soma_parcelas": to_num(cell(ws, f"Q{r}")),
            "ok": cell(ws, f"R{r}"),
        })
        r += 1
        if r > 50:
            break

    # ===== Gastos Previstos - totais por categoria =====
    ws = wb["Gastos Previstos"]
    meses = ["Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    cols = ["D", "E", "F", "G", "H", "I"]

    gastos_previstos = {
        "fixos_dtrip": {
            "total": to_num(cell(ws, "C22")),
            "por_mes": {m: to_num(cell(ws, f"{c}22")) for m, c in zip(meses, cols)},
        },
        "variaveis_estandes": {
            "total": to_num(cell(ws, "C29")),
            "por_mes": {m: to_num(cell(ws, f"{c}29")) for m, c in zip(meses, cols)},
        },
        "outros": {
            "total": to_num(cell(ws, "C48")),
            "por_mes": {m: to_num(cell(ws, f"{c}48")) for m, c in zip(meses, cols)},
        },
        "total_evento": {
            "total": to_num(cell(ws, "C50")),
            "por_mes": {m: to_num(cell(ws, f"{c}50")) for m, c in zip(meses, cols)},
        },
    }

    # Detalhe de gastos previstos (para transparencia)
    detalhe_previstos = []
    for r in range(5, 50):
        desc = cell(ws, f"B{r}")
        total = cell(ws, f"C{r}")
        if not desc or total is None:
            continue
        d = str(desc).strip()
        if not d or d.startswith("TOTAL") or d.startswith("GASTOS ") or d == "OUTROS GASTOS":
            continue
        detalhe_previstos.append({
            "descricao": d,
            "total": to_num(total),
        })

    # ===== Gastos Realizados =====
    ws = wb["Gastos Realizados"]
    gastos_realizados = []
    for r in range(5, 40):
        desc = cell(ws, f"C{r}")
        if not desc:
            continue
        gastos_realizados.append({
            "categoria": cell(ws, f"B{r}"),
            "descricao": desc,
            "status": cell(ws, f"D{r}"),
            "margem_seg": cell(ws, f"E{r}"),
            "valor_previsto": to_num(cell(ws, f"F{r}")),
            "n_parcelas": to_num(cell(ws, f"G{r}")),
            "pago_pj": to_num(cell(ws, f"H{r}")),
            "pago_eesc": to_num(cell(ws, f"J{r}")),
            "total_pago": to_num(cell(ws, f"L{r}")),
            "pct_pago": to_num(cell(ws, f"M{r}")),
            "ok": cell(ws, f"N{r}"),
        })
    total_pago = to_num(cell(ws, "L33"))

    # ===== Fluxo de Caixa =====
    # Nesta aba as colunas Jul-Dez ficam em C-H (não D-I como em Gastos Previstos)
    ws = wb["Fluxo de Caixa"]
    cols_fluxo = ["C", "D", "E", "F", "G", "H"]
    fluxo = {
        "meses": meses,
        "entradas_pj": [to_num(cell(ws, f"{c}6")) for c in cols_fluxo],
        "entradas_eesc": [to_num(cell(ws, f"{c}7")) for c in cols_fluxo],
        "total_entradas": [to_num(cell(ws, f"{c}8")) for c in cols_fluxo],
        "saidas_fixos": [to_num(cell(ws, f"{c}11")) for c in cols_fluxo],
        "saidas_estandes": [to_num(cell(ws, f"{c}12")) for c in cols_fluxo],
        "saidas_outros": [to_num(cell(ws, f"{c}13")) for c in cols_fluxo],
        "total_saidas": [to_num(cell(ws, f"{c}14")) for c in cols_fluxo],
        "resultado_mes": [to_num(cell(ws, f"{c}16")) for c in cols_fluxo],
        "saldo_acumulado": [to_num(cell(ws, f"{c}17")) for c in cols_fluxo],
    }

    # ===== KPIs prontos (agregados) =====
    faturamento_fechado = sum(v["valor_contratado"] for v in vendas if v["status"] == "Fechado")
    custo_estandes_fechados = sum(v["custo_estande"] for v in vendas if v["status"] == "Fechado")
    margem_fechada = sum(v["margem"] for v in vendas if v["status"] == "Fechado")
    cotas_vendidas = sum(1 for v in vendas if v["status"] == "Fechado")
    cotas_totais = sum(p["cotas_totais"] for p in pacotes)

    gastos_fixos_independentes = (
        gastos_previstos["fixos_dtrip"]["total"]
        + gastos_previstos["outros"]["total"]
    )
    gasto_total_previsto = gastos_previstos["total_evento"]["total"]
    resultado_hoje = faturamento_fechado - gasto_total_previsto
    equilibrio_pct = (
        faturamento_fechado / gasto_total_previsto if gasto_total_previsto else 0
    )
    caixa_pior_mes = min(fluxo["saldo_acumulado"]) if fluxo["saldo_acumulado"] else 0

    # Faturamento por EJ
    fat_por_ej = {}
    for v in vendas:
        if v["status"] == "Fechado":
            fat_por_ej[v["ej"]] = fat_por_ej.get(v["ej"], 0) + v["valor_contratado"]

    # Vendas por pacote
    vendas_por_pacote = {}
    for p in pacotes:
        vendas_por_pacote[p["nome"]] = {
            "fechados": 0,
            "faturamento": 0.0,
            "cotas_totais": p["cotas_totais"],
            "preco_tabela": p["preco_tabela"],
            "custo_estande": p["custo_estande"],
            "margem_unitaria": p["margem_unitaria"],
        }
    for v in vendas:
        if v["status"] == "Fechado" and v["pacote"] in vendas_por_pacote:
            vendas_por_pacote[v["pacote"]]["fechados"] += 1
            vendas_por_pacote[v["pacote"]]["faturamento"] += v["valor_contratado"]

    kpis = {
        "faturamento_fechado": faturamento_fechado,
        "custo_estandes_fechados": custo_estandes_fechados,
        "margem_fechada": margem_fechada,
        "cotas_vendidas": cotas_vendidas,
        "cotas_totais": cotas_totais,
        "gasto_total_previsto": gasto_total_previsto,
        "gastos_fixos_independentes": gastos_fixos_independentes,
        "resultado_hoje": resultado_hoje,
        "equilibrio_pct": equilibrio_pct,
        "total_pago_realizado": total_pago,
        "caixa_pior_mes": caixa_pior_mes,
        "faturamento_maximo_tabela": sum(p["faturamento_maximo"] for p in pacotes),
    }

    # ===== Monta o JSON final =====
    data = {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "parametros": parametros,
        "kpis": kpis,
        "vendas": vendas,
        "vendas_por_pacote": vendas_por_pacote,
        "faturamento_por_ej": fat_por_ej,
        "gastos_previstos": gastos_previstos,
        "detalhe_previstos": detalhe_previstos,
        "gastos_realizados": gastos_realizados,
        "fluxo_caixa": fluxo,
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

    print(f"OK. Gerado: {OUT_PATH}")
    print(f"  Faturamento fechado: R$ {faturamento_fechado:,.2f}")
    print(f"  Cotas vendidas:      {cotas_vendidas} / {cotas_totais}")
    print(f"  Resultado hoje:      R$ {resultado_hoje:,.2f}")
    print(f"  Equilibrio:          {equilibrio_pct*100:.1f}%")


if __name__ == "__main__":
    build()

@echo off
REM ================================================================
REM  Feira de Mercado - Atualizador do Dashboard
REM  Duplo clique para regerar data.json a partir da planilha
REM ================================================================
cd /d "%~dp0"
title Atualizar Dashboard - Feira de Mercado

echo.
echo   ==========================================
echo   Atualizando o dashboard da Feira de Mercado
echo   ==========================================
echo.

REM Verifica se Python esta instalado
where py >nul 2>&1
if errorlevel 1 (
    echo   [ERRO] Python nao encontrado no computador.
    echo.
    echo   Baixe e instale em: https://www.python.org/downloads/
    echo   IMPORTANTE: marque a opcao "Add Python to PATH" na instalacao.
    echo.
    pause
    exit /b 1
)

REM Instala openpyxl (silencioso, so na primeira vez)
py -m pip install --quiet openpyxl 2>nul

REM Roda o build
py -X utf8 build.py
if errorlevel 1 (
    echo.
    echo   [ERRO] Falha ao gerar o dashboard. Veja a mensagem acima.
    pause
    exit /b 1
)

echo.
echo   [OK] Dashboard atualizado com sucesso!
echo.
echo   Proximos passos:
echo   1. Abra o arquivo index.html no navegador para ver localmente
echo      (recomendado: clique com botao direito ^> Abrir com ^> Chrome/Edge)
echo   2. Ou envie os arquivos atualizados (data.json, planilha) para o GitHub
echo.

REM Abre o dashboard automaticamente via servidor local (para o fetch de data.json funcionar)
echo   Iniciando servidor local em http://localhost:8765 ...
echo   (Feche esta janela quando terminar de usar o dashboard)
echo.
start "" http://localhost:8765/
py -m http.server 8765

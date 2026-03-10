#!/bin/bash
# Render Start Script
# Este script é executado pelo Render antes de iniciar a aplicação

set -e

echo "🚀 Iniciando aplicação Passos Mágicos - API de Risco de Evasão"
echo "=============================================================="

# Verificar se modelo existe
if [ ! -f "app/model/model.joblib" ]; then
    echo "⚠️  AVISO: Modelo não encontrado em app/model/model.joblib"
    echo "    Certifique-se de que os arquivos do modelo foram incluídos no deploy"
fi

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p app/logs
mkdir -p app/model
mkdir -p backups

# Verificar variáveis de ambiente
echo "🔍 Verificando configuração..."
echo "   Environment: ${ENVIRONMENT:-development}"
echo "   Model Version: ${MODEL_VERSION:-unknown}"
echo "   Python Version: $(python --version)"
echo "   Port: ${PORT:-8000}"

# Listar arquivos do modelo
echo ""
echo "📦 Arquivos do modelo disponíveis:"
ls -lh app/model/ || echo "   Nenhum arquivo encontrado"

echo ""
echo "✅ Configuração concluída"
echo "🌐 Iniciando servidor..."
echo "=============================================================="

# Render executará o startCommand definido no render.yaml

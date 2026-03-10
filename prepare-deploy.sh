#!/bin/bash

# Script de Deploy no Render
# Prepara o projeto para deployment no Render

set -e

echo "🚀 Preparando projeto para deploy no Render..."
echo "================================================"

# 1. Verificar se Git está inicializado
if [ ! -d ".git" ]; then
    echo "📦 Inicializando repositório Git..."
    git init
    git branch -M main
else
    echo "✅ Repositório Git já inicializado"
fi

# 2. Verificar se modelo existe
if [ ! -f "app/model/model.joblib" ]; then
    echo ""
    echo "⚠️  ATENÇÃO: Modelo não encontrado!"
    echo "    Execute primeiro: python src/train.py"
    echo ""
    read -p "Deseja continuar mesmo assim? (y/N): " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        echo "❌ Deploy cancelado"
        exit 1
    fi
else
    echo "✅ Modelo encontrado: app/model/model.joblib"
    
    # Verificar tamanho do modelo
    model_size=$(stat -f%z "app/model/model.joblib" 2>/dev/null || stat -c%s "app/model/model.joblib" 2>/dev/null || echo "0")
    model_size_mb=$((model_size / 1024 / 1024))
    
    echo "   Tamanho: ${model_size_mb}MB"
    
    if [ $model_size_mb -gt 100 ]; then
        echo "   ⚠️  Modelo grande (>100MB) - considere usar Git LFS"
        echo "   Instale Git LFS: https://git-lfs.github.com"
        echo ""
        read -p "   Configurar Git LFS agora? (y/N): " setup_lfs
        if [[ $setup_lfs =~ ^[Yy]$ ]]; then
            git lfs install
            git lfs track "*.joblib"
            git add .gitattributes
            echo "   ✅ Git LFS configurado"
        fi
    fi
fi

# 3. Verificar arquivos essenciais
echo ""
echo "🔍 Verificando arquivos essenciais..."

required_files=(
    "requirements.txt"
    "render.yaml"
    "app/main.py"
    "app/routes.py"
    "src/preprocessing.py"
    "src/feature_engineering.py"
    "src/utils.py"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file - FALTANDO!"
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo ""
    echo "❌ Arquivos essenciais faltando. Corrija antes de fazer deploy."
    exit 1
fi

# 4. Verificar dependências
echo ""
echo "📦 Verificando dependências..."
if command -v pip &> /dev/null; then
    echo "   Gerando requirements.txt atualizado..."
    pip freeze > requirements.txt.new
    echo "   ✅ requirements.txt.new gerado"
    echo "   Revise e substitua requirements.txt se necessário"
else
    echo "   ⚠️  pip não encontrado - pule este passo"
fi

# 5. Testar localmente (opcional)
echo ""
read -p "🧪 Testar API localmente antes do deploy? (Y/n): " run_tests
if [[ ! $run_tests =~ ^[Nn]$ ]]; then
    echo "   Executando testes..."
    if command -v pytest &> /dev/null; then
        pytest tests/ -v --tb=short -k "not test_api" || echo "   ⚠️  Alguns testes falharam"
    else
        echo "   ⚠️  pytest não instalado - pulando testes"
    fi
fi

# 6. Commit
echo ""
echo "📝 Preparando commit..."
git add .
git status

echo ""
read -p "💾 Fazer commit das alterações? (Y/n): " do_commit
if [[ ! $do_commit =~ ^[Nn]$ ]]; then
    read -p "   Mensagem do commit: " commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Deploy: API v3.0 - Risco de Evasão"
    fi
    
    git commit -m "$commit_msg"
    echo "   ✅ Commit realizado"
fi

# 7. Instruções finais
echo ""
echo "================================================"
echo "✅ Preparação concluída!"
echo "================================================"
echo ""
echo "📋 Próximos passos:"
echo ""
echo "1️⃣  Criar repositório no GitHub:"
echo "   https://github.com/new"
echo ""
echo "2️⃣  Adicionar remote (substitua SEU_USUARIO):"
echo "   git remote add origin https://github.com/SEU_USUARIO/passos-magicos-evasao-api.git"
echo ""
echo "3️⃣  Push para GitHub:"
echo "   git push -u origin main"
echo ""
echo "4️⃣  Deploy no Render:"
echo "   - Acesse: https://dashboard.render.com"
echo "   - New → Web Service"
echo "   - Connect GitHub repository"
echo "   - Render lerá automaticamente render.yaml"
echo ""
echo "📚 Documentação completa:"
echo "   docs_contexto/DEPLOY_RENDER.md"
echo ""
echo "🌐 URL da API após deploy:"
echo "   https://passos-magicos-evasao-api.onrender.com"
echo ""
echo "================================================"

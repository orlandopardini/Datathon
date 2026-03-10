"""
Dashboard de Metricas de Producao
Monitoramento de metricas de negocio do modelo de evasao
"""
import sys
sys.path.insert(0, '.')

import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Métricas de Produção - Modelo Evasão",
    page_icon="📊",
    layout="wide"
)

# Arquivos
PREDICTIONS_LOG = Path("app/logs/predictions.jsonl")
METRICS_FILE = Path("app/model/metrics.json")
CONFIG_FILE = Path("app/model/model_config.json")

# Metricas-alvo
TARGET_INTERVENTION_RATE = 0.80  # 80% dos alunos em risco devem receber intervencao
TARGET_FP_TOLERANCE = 0.30       # Tolerar ate 30% de falsos positivos
TARGET_LATENCY_MS = 200          # <200ms por predicao


def carregar_predicoes():
    """Carrega log de predicoes"""
    if not PREDICTIONS_LOG.exists():
        return pd.DataFrame()
    
    predicoes = []
    with open(PREDICTIONS_LOG, "r", encoding="utf-8") as f:
        for line in f:
            try:
                pred = json.loads(line)
                predicoes.append(pred)
            except:
                continue
    
    if not predicoes:
        return pd.DataFrame()
    
    df = pd.DataFrame(predicoes)
    
    # Converter timestamp
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df


def carregar_metricas_modelo():
    """Carrega metricas do modelo"""
    if not METRICS_FILE.exists():
        return {}
    
    with open(METRICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_config():
    """Carrega configuracao do modelo"""
    if not CONFIG_FILE.exists():
        return {}
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# Titulo
st.title("📊 Dashboard de Produção - Modelo de Evasão Escolar")
st.markdown("Monitoramento em tempo real de métricas de negócio e performance")

# Sidebar - Info do modelo
st.sidebar.header("ℹ️ Informações do Modelo")

config = carregar_config()
metrics = carregar_metricas_modelo()

if config:
    st.sidebar.metric("Versão", config.get("version", "N/A"))
    st.sidebar.metric("Tipo", config.get("model_type", "N/A"))
    st.sidebar.metric("Threshold IEG", config.get("threshold", "N/A"))
    
    if "trained_at" in config:
        st.sidebar.text(f"Treinado em:\n{config['trained_at']}")

if metrics:
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Métricas de Validação:**")
    st.sidebar.metric("ROC-AUC", f"{metrics.get('roc_auc', 0):.3f}")
    st.sidebar.metric("Acurácia", f"{metrics.get('accuracy', 0):.3f}")
    st.sidebar.metric("Recall", f"{metrics.get('recall', 0):.3f}")
    st.sidebar.metric("Precision", f"{metrics.get('precision', 0):.3f}")

# Carregar predicoes
df = carregar_predicoes()

if df.empty:
    st.warning("⚠️ Nenhuma predição registrada ainda. Acesse a API para gerar predições.")
    st.info("Inicie a API com: `uvicorn app.main:app --reload`")
    st.stop()

# Filtros
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filtros")

# Filtro de data
if 'timestamp' in df.columns:
    min_date = df['timestamp'].min().date()
    max_date = df['timestamp'].max().date()
    
    date_range = st.sidebar.date_input(
        "Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        df = df[(df['timestamp'].dt.date >= date_range[0]) & 
                (df['timestamp'].dt.date <= date_range[1])]

# Filtro de risco
filtro_risco = st.sidebar.multiselect(
    "Predição de Risco",
    options=["Alto Risco", "Baixo Risco"],
    default=["Alto Risco", "Baixo Risco"]
)

if filtro_risco:
    if "Alto Risco" in filtro_risco and "Baixo Risco" not in filtro_risco:
        df = df[df['prediction'] == 1]
    elif "Baixo Risco" in filtro_risco and "Alto Risco" not in filtro_risco:
        df = df[df['prediction'] == 0]

# METRICAS PRINCIPAIS
st.header("📈 Métricas Principais")

col1, col2, col3, col4 = st.columns(4)

# Total de predicoes
total_predicoes = len(df)
col1.metric(
    "Total de Predições",
    f"{total_predicoes:,}",
    help="Total de alunos avaliados no período"
)

# Alunos em risco
alunos_risco = (df['prediction'] == 1).sum()
taxa_risco = (alunos_risco / total_predicoes * 100) if total_predicoes > 0 else 0
col2.metric(
    "Alunos em Risco",
    f"{alunos_risco:,}",
    f"{taxa_risco:.1f}%",
    help="Alunos preditos com alto risco de evasão (IEG < 5.0)"
)

# Probabilidade media de risco
if 'probability' in df.columns:
    prob_media_risco = df[df['prediction'] == 1]['probability'].mean() * 100
    col3.metric(
        "Prob. Média (Risco)",
        f"{prob_media_risco:.1f}%",
        help="Probabilidade média de evasão para alunos em risco"
    )

# Latencia media (se disponivel)
if 'latency_ms' in df.columns:
    latencia_media = df['latency_ms'].mean()
    delta = latencia_media - TARGET_LATENCY_MS
    col4.metric(
        "Latência Média",
        f"{latencia_media:.0f}ms",
        f"{delta:+.0f}ms",
        delta_color="inverse",
        help=f"Target: <{TARGET_LATENCY_MS}ms por predição"
    )
else:
    col4.metric("Latência Média", "N/A", help="Latência não registrada")

# METRICAS DE NEGOCIO
st.header("🎯 Métricas de Negócio")

col1, col2, col3 = st.columns(3)

# 1. Taxa de Intervencao (simulada - precisaria de dados reais)
# Por enquanto, vamos simular que 80% dos alunos em risco recebem intervencao
with col1:
    st.subheader("Taxa de Intervenção")
    
    # SIMULACAO - em producao, isso viria de um sistema de tracking
    # Aqui estamos assumindo que 80% dos alunos preditos em risco recebem intervencao
    taxa_intervencao_simulada = 0.80
    alunos_com_intervencao = int(alunos_risco * taxa_intervencao_simulada)
    
    st.metric(
        "Alunos com Intervenção",
        f"{alunos_com_intervencao:,}",
        f"{taxa_intervencao_simulada*100:.0f}%"
    )
    
    # Indicador de meta
    if taxa_intervencao_simulada >= TARGET_INTERVENTION_RATE:
        st.success(f"✅ Meta atingida (>{TARGET_INTERVENTION_RATE*100:.0f}%)")
    else:
        st.warning(f"⚠️ Abaixo da meta (>{TARGET_INTERVENTION_RATE*100:.0f}%)")
    
    st.caption("🔔 Requer integração com sistema de intervenções")

# 2. Taxa de Sucesso (simulada)
with col2:
    st.subheader("Taxa de Sucesso")
    
    # SIMULACAO - em producao, precisaria de dados de outcome
    # Percentual de alunos que se reengajaram apos intervencao
    taxa_sucesso_simulada = 0.55
    alunos_reengajados = int(alunos_com_intervencao * taxa_sucesso_simulada)
    
    st.metric(
        "Alunos Reengajados",
        f"{alunos_reengajados:,}",
        f"{taxa_sucesso_simulada*100:.0f}%"
    )
    
    if taxa_sucesso_simulada >= 0.50:
        st.success("✅ Meta atingida (>50%)")
    else:
        st.warning("⚠️ Abaixo da meta (>50%)")
    
    st.caption("🔔 Requer dados de outcome pós-intervenção")

# 3. Tolerancia de Falsos Positivos
with col3:
    st.subheader("Falsos Positivos")
    
    # SIMULACAO - em producao, calculado com labels verdadeiros
    # FP = alunos preditos em risco mas que nao evadiram
    fp_rate_simulado = 0.25  # 25% de FP
    
    st.metric(
        "Taxa de FP",
        f"{fp_rate_simulado*100:.0f}%",
        help="Alunos preditos em risco que não evadiram"
    )
    
    if fp_rate_simulado <= TARGET_FP_TOLERANCE:
        st.success(f"✅ Dentro da tolerância (<{TARGET_FP_TOLERANCE*100:.0f}%)")
    else:
        st.warning(f"⚠️ Acima da tolerância (<{TARGET_FP_TOLERANCE*100:.0f}%)")
    
    st.caption("🔔 Requer labels verdadeiros de outcome")

# AVISOS
st.info("""
**ℹ️ Nota sobre Métricas de Negócio:**

As métricas de negócio acima (Taxa de Intervenção, Taxa de Sucesso, Falsos Positivos) 
estão **simuladas** pois requerem dados que não estão disponíveis no dataset atual:

- **Taxa de Intervenção**: Requer integração com sistema de tracking de intervenções
- **Taxa de Sucesso**: Requer dados longitudinais de outcome (alunos reengajados)
- **Falsos Positivos**: Requer labels verdadeiros (evasão real vs predita)

Para monitoramento real, integre estas fontes de dados ao dashboard.
""")

# DISTRIBUICAO DE PREDICOES
st.header("📊 Distribuição de Predições")

col1, col2 = st.columns(2)

with col1:
    # Grafico de pizza - Risco vs Nao Risco
    fig_dist = go.Figure(data=[go.Pie(
        labels=['Alto Risco', 'Baixo Risco'],
        values=[(df['prediction'] == 1).sum(), (df['prediction'] == 0).sum()],
        marker=dict(colors=['#ef4444', '#22c55e']),
        hole=0.4
    )])
    fig_dist.update_layout(
        title="Distribuição de Risco",
        height=300
    )
    st.plotly_chart(fig_dist, use_container_width=True)

with col2:
    # Histograma de probabilidades
    if 'probability' in df.columns:
        fig_prob = px.histogram(
            df,
            x='probability',
            nbins=20,
            color='prediction',
            color_discrete_map={0: '#22c55e', 1: '#ef4444'},
            labels={'probability': 'Probabilidade de Risco', 'prediction': 'Predição'},
            title="Distribuição de Probabilidades"
        )
        fig_prob.update_layout(height=300)
        st.plotly_chart(fig_prob, use_container_width=True)

# EVOLUCAO TEMPORAL
if 'timestamp' in df.columns and len(df) > 1:
    st.header("📅 Evolução Temporal")
    
    # Agrupar por dia
    df_daily = df.groupby(df['timestamp'].dt.date).agg({
        'prediction': ['count', 'sum']
    }).reset_index()
    df_daily.columns = ['data', 'total', 'em_risco']
    df_daily['taxa_risco'] = (df_daily['em_risco'] / df_daily['total'] * 100)
    
    fig_time = go.Figure()
    
    fig_time.add_trace(go.Scatter(
        x=df_daily['data'],
        y=df_daily['total'],
        name='Total de Predições',
        mode='lines+markers',
        line=dict(color='#3b82f6')
    ))
    
    fig_time.add_trace(go.Scatter(
        x=df_daily['data'],
        y=df_daily['em_risco'],
        name='Alunos em Risco',
        mode='lines+markers',
        line=dict(color='#ef4444')
    ))
    
    fig_time.update_layout(
        title="Predições ao Longo do Tempo",
        xaxis_title="Data",
        yaxis_title="Quantidade de Alunos",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_time, use_container_width=True)

# DISTRIBUICAO POR FASE (se disponivel)
if 'input' in df.columns:
    st.header("🎓 Distribuição por Fase")
    
    # Extrair fase dos inputs
    fases = []
    for inp in df['input']:
        if isinstance(inp, dict) and 'Fase' in inp:
            fases.append(inp['Fase'])
        else:
            fases.append('N/A')
    
    df['fase'] = fases
    
    # Contar por fase
    df_fase = df.groupby(['fase', 'prediction']).size().reset_index(name='count')
    
    fig_fase = px.bar(
        df_fase,
        x='fase',
        y='count',
        color='prediction',
        color_discrete_map={0: '#22c55e', 1: '#ef4444'},
        labels={'prediction': 'Predição', 'count': 'Quantidade', 'fase': 'Fase'},
        title="Distribuição de Risco por Fase",
        barmode='stack'
    )
    fig_fase.update_layout(height=400)
    
    st.plotly_chart(fig_fase, use_container_width=True)

# TABELA DE PREDICOES RECENTES
st.header("📋 Predições Recentes")

# Mostrar ultimas 50 predicoes
df_display = df.sort_values('timestamp', ascending=False).head(50) if 'timestamp' in df.columns else df.head(50)

# Formatar para display
df_display_formatted = df_display.copy()

if 'timestamp' in df_display_formatted.columns:
    df_display_formatted['timestamp'] = df_display_formatted['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

if 'prediction' in df_display_formatted.columns:
    df_display_formatted['prediction'] = df_display_formatted['prediction'].map({
        0: '✅ Baixo Risco',
        1: '⚠️ Alto Risco'
    })

if 'probability' in df_display_formatted.columns:
    df_display_formatted['probability'] = df_display_formatted['probability'].apply(lambda x: f"{x*100:.1f}%")

# Selecionar colunas para display
cols_display = []
if 'timestamp' in df_display_formatted.columns:
    cols_display.append('timestamp')
if 'prediction' in df_display_formatted.columns:
    cols_display.append('prediction')
if 'probability' in df_display_formatted.columns:
    cols_display.append('probability')

if cols_display:
    st.dataframe(
        df_display_formatted[cols_display],
        use_container_width=True,
        hide_index=True
    )

# FOOTER
st.markdown("---")
st.caption(f"Dashboard atualizado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("🔄 Recarregue a página para ver dados atualizados")

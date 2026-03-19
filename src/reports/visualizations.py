import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Colores neutros y limpios
FINTECH_COLORS = ['#2563EB', '#60A5FA', '#93C5FD', '#BFDBFE', '#DBEAFE', '#1E3A8A']

def plot_transacciones_por_tipo(df: pd.DataFrame):
    """Dibuja un gráfico pastel minimalista de transacciones por tipo."""
    if df.empty:
        return None
        
    fig = px.pie(df, values='monto_total', names='tipo_transaccion', 
                 hole=0.5,
                 color_discrete_sequence=FINTECH_COLORS)
                 
    fig.update_layout(
        margin=dict(t=20, b=20, l=0, r=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        font=dict(color='#1F2937')
    )
    # Quitar bordes de los pedazos
    fig.update_traces(marker=dict(line=dict(color='#FFFFFF', width=2)))
    return fig

def plot_alertas_severidad(df: pd.DataFrame):
    """Crea un gráfico de barras minimalista para alertas."""
    if df.empty:
        return None
        
    # Colores sobrios para severidad (evitando rojos puros/chillones)
    color_map = {
        'Critica': '#991B1B', # Rojo muy oscuro y sobrio
        'Alta': '#B45309',    # Naranja oscuro
        'Media': '#D97706',   # Ambar oscuro
        'Baja': '#3B82F6'     # Azul claro
    }
    
    fig = px.bar(df, x='cantidad', y='severidad', orientation='h',
                 color='severidad', color_discrete_map=color_map)
                 
    fig.update_layout(
        showlegend=False, 
        margin=dict(t=20, b=20, l=0, r=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#E5E7EB', title='Cantidad', color='#6B7280'),
        yaxis=dict(showgrid=False, title='', color='#1F2937'),
        font=dict(color='#1F2937')
    )
    return fig

def format_currency(value):
    return f"${value:,.2f}"

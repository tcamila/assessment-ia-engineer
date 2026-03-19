import streamlit as st
import pandas as pd

from src.utils.config import Config
from src.auth.auth_service import authenticate_user
from src.reports.queries import (
    get_kpis_dashboard, get_transacciones_recientes, 
    get_resumen_alertas, get_transacciones_por_tipo, get_ranking_asociados
)
from src.reports.visualizations import plot_transacciones_por_tipo, plot_alertas_severidad, format_currency
from src.nl_query.nl2sql import NLPQueryEngine
from src.monitoring.rules import execute_monitoring_rules
from src.monitoring.summarizer import MonitoringSummarizer

# Configuración inicial de Streamlit
st.set_page_config(page_title="Data Tools | Analytics", layout="wide")

# Estilos Globales CSS
STYLES = """
<style>
    .stApp { background-color: #F7F7F8; color: #1F2937; font-family: 'Inter', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .card-container { background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }
    .section-title { color: #1F2937; font-size: 1.25rem; font-weight: 600; margin-bottom: 16px; border-bottom: 1px solid #E5E7EB; padding-bottom: 8px; }
    .subtle-text { color: #6B7280; font-size: 0.875rem; margin-bottom: 16px; }
    .stButton > button { background-color: #2563EB !important; color: #FFFFFF !important; border-radius: 6px !important; border: none !important; padding: 8px 16px !important; font-weight: 500 !important; }
    .stButton > button:hover { background-color: #1D4ED8 !important; }
    .stDownloadButton > button { background-color: #FFFFFF !important; color: #374151 !important; border: 1px solid #D1D5DB !important; }
    [data-testid="stMetric"] { background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; padding: 16px; }
    [data-testid="stDataFrame"] { border: 1px solid #E5E7EB; border-radius: 8px; }
    
    /* Navegación horizontal para reemplazar tabs y tener control absoluto del estado */
    .nav-container { margin-bottom: 20px; }
</style>
"""

Config.check_db_exists()

# ==========================================
# INICIALIZACIÓN SEGURA DE SESSION_STATE
# ==========================================
def init_session_state():
    """
    Esta función prepara la memoria temporal de la aplicación (Session State).
    Se asegura de que existan variables como 'usuario', 'pestaña actual' o 'resultado anterior' 
    para que la app no pierda la información si la página se recarga.
    """
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "organization_id" not in st.session_state:
        st.session_state["organization_id"] = None
    if "organization_name" not in st.session_state:
        st.session_state["organization_name"] = None
    if "active_tab" not in st.session_state:
        st.session_state["active_tab"] = "Dashboard General"
    if "query_input" not in st.session_state:
        st.session_state["query_input"] = ""
    if "last_sql" not in st.session_state:
        st.session_state["last_sql"] = None
    if "last_result" not in st.session_state:
        st.session_state["last_result"] = pd.DataFrame()
    if "last_error" not in st.session_state:
        st.session_state["last_error"] = None
    if "monitoring_results" not in st.session_state:
        st.session_state["monitoring_results"] = None

init_session_state()

def login_ui():
    """
    Esta función dibuja la pantalla inicial de inicio de sesión.
    No recibe ni retorna nada. Pide usuario y contraseña y, 
    si son correctos, guarda los datos en la memoria y recarga.
    """
    st.markdown(STYLES, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Acceso a Plataforma</div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Ingresar")
            
            if submit:
                user_data = authenticate_user(username, password)
                if user_data:
                    st.session_state["authenticated"] = True
                    st.session_state["user_id"] = user_data["id_usuario"]
                    st.session_state["username"] = user_data["username"]
                    st.session_state["organization_id"] = user_data["id_organizacion"]
                    st.session_state["organization_name"] = user_data["org_nombre"]
                    st.rerun()
                else:
                    st.error("Credenciales inválidas o usuario inactivo.")

def logout():
    # Solo limpiamos claves de sesión, dejamos inicializada la estructura
    st.session_state["authenticated"] = False
    st.session_state["user_id"] = None
    st.session_state["username"] = None
    st.session_state["organization_id"] = None
    st.session_state["organization_name"] = None
    st.session_state["active_tab"] = "Dashboard General"
    st.session_state["query_input"] = ""
    st.session_state["last_sql"] = None
    st.session_state["last_result"] = pd.DataFrame()
    st.session_state["last_error"] = None
    st.session_state["monitoring_results"] = None
    st.rerun()

def main_app():
    """
    Esta función construye todo el dashboard principal una vez que el usuario ingresó correctamente.
    No recibe parámetros directos porque lee el 'st.session_state' para saber qué usuario está activo.
    Dibuja las 3 pestañas: Dashboard (KPIs y gráficas), Chat SQL, y Monitoreo Automático.
    """
    st.markdown(STYLES, unsafe_allow_html=True)
    
    org_id = st.session_state["organization_id"]
    org_name = st.session_state["organization_name"]
    
    # Header
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 24px;">
        <div>
            <h1 style="color: #1F2937; margin: 0; font-size: 1.75rem;">{org_name}</h1>
            <div class="subtle-text" style="margin-top: 4px; margin-bottom: 0;">Usuario: {st.session_state["username"]} | Contexto ID: {org_id}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    c_btn1, c_btn2 = st.columns([9, 1])
    with c_btn2:
        if st.button("Cerrar Sesión"):
            logout()
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navegación Controlada por Estado
    st.radio(
        "Navegación", 
        ["Dashboard General", "Consulta Inteligente", "Monitoreo de Riesgos"],
        horizontal=True,
        label_visibility="collapsed",
        key="active_tab"
    )

    # --- TAB 1: DASHBOARD ---
    if st.session_state["active_tab"] == "Dashboard General":
        try:
            kpis = get_kpis_dashboard(org_id)
            c1, c2, c3 = st.columns(3)
            c1.metric(label="Total Asociados", value=f"{kpis['total_asociados']:,}")
            c2.metric(label="Total Transacciones", value=f"{kpis['total_transacciones']:,}")
            c3.metric(label="Total Alertas", value=f"{kpis['total_alertas']:,}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_graf1, col_graf2 = st.columns(2)
            
            with col_graf1:
                st.markdown('<div class="card-container"><div class="section-title">Distribución de Transacciones</div>', unsafe_allow_html=True)
                df_tipos = get_transacciones_por_tipo(org_id)
                if not df_tipos.empty:
                    st.plotly_chart(plot_transacciones_por_tipo(df_tipos), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                    
            with col_graf2:
                st.markdown('<div class="card-container"><div class="section-title">Concentración de Alertas</div>', unsafe_allow_html=True)
                df_alertas = get_resumen_alertas(org_id)
                if not df_alertas.empty:
                    st.plotly_chart(plot_alertas_severidad(df_alertas), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                    
            st.markdown('<div class="card-container"><div class="section-title">Últimas 50 Transacciones</div>', unsafe_allow_html=True)
            st.dataframe(get_transacciones_recientes(org_id, 50), use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error("No fue posible cargar el dashboard. Error interno de datos.")

    # --- TAB 2: CONSULTAS LENGUAJE NATURAL ---
    elif st.session_state["active_tab"] == "Consulta Inteligente":
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Generación de Consultas</div>', unsafe_allow_html=True)
        
        # El input es persistente a través del session_state dict ("query_input") vinculado por key
        st.text_area("Criterios de búsqueda", key="query_input", placeholder="Ej: Transacciones del último mes")
        
        if st.button("Ejecutar Consulta", use_container_width=True):
            user_query = st.session_state["query_input"].strip()
            if user_query:
                with st.spinner("Procesando consulta..."):
                    try:
                        engine = NLPQueryEngine(organization_id=org_id)
                        response = engine.process_query(user_query)
                        
                        if response.get("status") == "error":
                            st.session_state["last_error"] = response.get("message", "Consulta no válida.")
                        else:
                            st.session_state["last_sql"] = response.get("sql", "")
                            st.session_state["last_result"] = response.get("data", pd.DataFrame())
                            st.session_state["last_error"] = None
                    except Exception as e:
                        # Control total del error. No limpiamos tabla previa.
                        st.session_state["last_error"] = "No fue posible procesar la consulta. Intenta con una pregunta diferente."

        # Redibujar Estado
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state["last_error"]:
            st.error(f"{st.session_state['last_error']}")
            
        if st.session_state["last_sql"]:
            col_r1, col_r2 = st.columns([1, 1])
            with col_r1:
                st.markdown("**SQL Aislado por Organización**")
                st.code(st.session_state["last_sql"], language="sql")
            with col_r2:
                st.markdown("**Resultados**")
                if not st.session_state["last_result"].empty:
                    st.dataframe(st.session_state["last_result"], use_container_width=True, hide_index=True)
                else:
                    st.info("Sin registros.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 3: MONITOREO ---
    elif st.session_state["active_tab"] == "Monitoreo de Riesgos":
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Auditoría Automática</div>', unsafe_allow_html=True)
        
        if st.button("Ejecutar Reglas"):
            with st.spinner("Verificando consistencia..."):
                try:
                    results = execute_monitoring_rules(org_id)
                    summarizer = MonitoringSummarizer()
                    st.session_state["monitoring_results"] = {
                        "text": summarizer.generate_report(results, org_name),
                        "findings": results["findings"]
                    }
                except Exception as e:
                    st.error("No fue posible ejecutar el escaneo de monitoreo. Verifica los datos.")
        
        if st.session_state["monitoring_results"]:
            res = st.session_state["monitoring_results"]
            st.markdown('<div style="background-color: #F8FAFC; padding: 20px; border-radius: 6px; border: 1px solid #E2E8F0; margin-top:20px;">', unsafe_allow_html=True)
            st.markdown("**Dictamen Principal**")
            st.markdown(res["text"])
            st.markdown('</div><br>', unsafe_allow_html=True)
            
            if res["findings"]:
                for f in res["findings"]:
                    st.warning(f"⚠️ {f}")
            else:
                st.success("No se encontraron vulnerabilidades.")
                
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if not st.session_state.get("authenticated", False):
        login_ui()
    else:
        main_app()

import streamlit as st
import httpx
import uuid
from datetime import datetime

# ══════════════════════════════════════════════════════════════
# 1. CONFIGURAÇÃO INTERNA E CSS HIGH-END
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="DoeAqui — Ranking de Times",
    page_icon="🩸",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; font-family: 'Inter', sans-serif; }

/* ── PAGE BASE ── */
.stApp { background-color: #F4F6FA; }
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }

/* ── TIMING ADVANCED ANIMATIONS ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0);    }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes countUp {
    from { opacity: 0; transform: scale(0.8); }
    to   { opacity: 1; transform: scale(1);   }
}

.fade-in     { animation: fadeInUp 0.5s ease both; }
.fade-in-2   { animation: fadeInUp 0.5s ease 0.1s both; }
.fade-in-3   { animation: fadeInUp 0.5s ease 0.2s both; }
.fade-in-4   { animation: fadeInUp 0.5s ease 0.3s both; }

/* ── SIDEBAR ARCHITECTURE ── */
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 3px solid #C0152B;
    box-shadow: 3px 0 12px rgba(0,0,0,0.07);
}
[data-testid="stSidebar"] * { color: #1A1A2E !important; }

.sidebar-logo {
    font-size: 1.6rem;
    font-weight: 800;
    color: #C0152B !important;
    letter-spacing: -0.5px;
    animation: fadeIn 0.6s ease both;
}
.sidebar-tagline {
    font-size: 0.8rem;
    color: #999 !important;
    margin-top: 2px;
    margin-bottom: 16px;
}
.sidebar-card {
    background: #F9FAFB;
    border: 1px solid #EEE;
    border-left: 3px solid #C0152B;
    border-radius: 10px;
    padding: 14px;
    font-size: 0.82rem;
    color: #555 !important;
    margin-top: 8px;
    animation: fadeIn 0.8s ease both;
}

/* ── CORREÇÃO DO ESPAÇO MORTO DA NAVEGAÇÃO ── */
[data-testid="stSidebarNav"] { padding-top: 0px !important; margin-top: 0px !important; }
div.stRadio > label { display: none !important; }
div.stRadio > div { gap: 6px !important; padding-top: 0px !important; margin-top: 0px !important; }
[data-testid="stSidebar"] .stRadio label {
    background: #F4F6FA;
    border-radius: 8px;
    padding: 10px 14px !important;
    font-weight: 500;
    font-size: 0.9rem;
    transition: background 0.2s, transform 0.15s;
    cursor: pointer;
    display: block;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: #FEE8EB;
    transform: translateX(3px);
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] [data-checked="true"] label {
    background: linear-gradient(135deg, #C0152B, #E8253E) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(192,21,43,0.25) !important;
}

/* ── HEADERS ── */
h1 { color: #1A1A2E !important; font-weight: 800 !important; letter-spacing: -0.5px; }
h2 { color: #1A1A2E !important; font-weight: 700 !important; }
h3 { color: #333 !important;    font-weight: 600 !important; }

/* ── METRICS INTERFACE ── */
.metric-box {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 24px 16px;
    text-align: center;
    border-top: 4px solid #C0152B;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    animation: countUp 0.5s ease both;
}
.metric-box:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(192,21,43,0.13); }
.metric-val   { font-size: 2.4rem; font-weight: 800; color: #C0152B; line-height: 1; }
.metric-label { font-size: 0.8rem; color: #999; margin-top: 8px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }

/* ── RANKING CARDS UI ── */
.ranking-card {
    background: #FFFFFF;
    border-left: 5px solid #C0152B;
    border-radius: 12px;
    padding: 18px 24px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-left-color 0.2s;
    cursor: default;
}
.ranking-card:hover { transform: translateX(5px) translateY(-2px); box-shadow: 0 8px 28px rgba(0,0,0,0.11); }
.ranking-card.gold   { border-left-color: #F5A623; background: linear-gradient(135deg, #FFFDF5, #FFFFFF); }
.ranking-card.silver { border-left-color: #9E9E9E; background: linear-gradient(135deg, #FAFAFA, #FFFFFF); }
.ranking-card.bronze { border-left-color: #CD7F32; background: linear-gradient(135deg, #FDF8F4, #FFFFFF); }

.rank-pos   { font-size: 2rem; font-weight: 800; color: #C0152B; width: 60px; flex-shrink: 0; }
.rank-nome  { font-size: 1.05rem; font-weight: 700; color: #1A1A2E; flex: 1; padding-left: 16px; }
.rank-pts   { font-size: 1.45rem; font-weight: 800; color: #C0152B; }
.rank-label { font-size: 0.7rem; color: #BBB; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.5px; }
.codigo-badge { background: #FEE8EB; color: #C0152B; padding: 2px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; letter-spacing: 1.5px; }

/* ── BOX & TAGS ── */
.info-box { background: #FFFFFF; border: 1.5px solid #EEE; border-radius: 12px; padding: 18px; color: #444; font-size: 0.92rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: box-shadow 0.2s; }
.info-box:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.09); }
.time-tag { display: inline-block; background: #FEE8EB; color: #C0152B; border-radius: 6px; padding: 3px 10px; font-size: 0.78rem; font-weight: 700; margin-top: 6px; }

/* ── PASSO CARD ── */
.passo-card {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 16px;
    background: #FFFFFF;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 12px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    border-left: 3px solid transparent;
}
.passo-card:hover { transform: translateX(4px); box-shadow: 0 4px 16px rgba(192,21,43,0.1); border-left-color: #C0152B; }

/* ── PREMIUM INJECTION BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #C0152B, #E8253E) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    width: 100%;
    padding: 13px !important;
    letter-spacing: 0.3px;
    box-shadow: 0 4px 14px rgba(192,21,43,0.35) !important;
    transition: transform 0.18s ease, box-shadow 0.18s ease !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 7px 20px rgba(192,21,43,0.45) !important; }
.stButton > button:active { transform: translateY(0px) !important; }

/* ── PREMIUM INPUT FIELDS ── */
.stTextInput > div > div > input, .stSelectbox > div > div > div {
    background: #FFFFFF !important;
    color: #1A1A2E !important;
    border: 1.5px solid #E0E0E0 !important;
    border-radius: 9px !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

/* ── RESPONSE ALERTS ── */
.sucesso { background: linear-gradient(135deg, #F0FBF4, #E8F8EE); border-left: 4px solid #28a745; border-radius: 10px; padding: 14px 18px; color: #1a7a36; font-weight: 600; font-size: 0.95rem; animation: fadeInUp 0.4s ease both; box-shadow: 0 2px 8px rgba(40,167,69,0.12); }
hr { border-color: #EBEBEB !important; margin: 1.2rem 0 !important; }
footer { visibility: hidden; }
.rodape { text-align: center; color: #CCC; font-size: 0.77rem; padding: 12px 0 4px; animation: fadeIn 1s ease both; }
[data-testid="stDataFrame"] { border-radius: 10px !important; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }
.page-header { animation: fadeInUp 0.45s ease both; margin-bottom: 4px; }
.page-subtitle { color: #999; font-size: 0.92rem; margin-top: -8px; margin-bottom: 16px; animation: fadeIn 0.6s ease 0.1s both; }

/* ── TELA HERO / PORTAL (FLEXBOX SÊNIOR) ── */
.hero-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 100%;
    margin-top: 6vh;
    animation: fadeIn 0.8s ease both;
}
.hero-title { font-size: 4rem; color: #1A1A2E; letter-spacing: -1.5px; font-weight: 800; margin-bottom: 0; line-height: 1.1; text-align: center; }
.hero-subtitle { font-size: 1.25rem; color: #666; max-width: 650px; margin: 15px auto 30px; line-height: 1.6; text-align: center; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 2. PERSISTÊNCIA SUPABASE E CACHE INTELIGENTE
# ══════════════════════════════════════════════════════════════
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

@st.cache_data(ttl=5)
def buscar_times():
    try:
        r = httpx.get(f"{url}/rest/v1/times?select=*&order=pontos_totais.desc", headers=headers)
        return r.json() if r.status_code == 200 else []
    except: return []

@st.cache_data(ttl=3)
def buscar_usuarios():
    try:
        r = httpx.get(f"{url}/rest/v1/usuarios?select=*", headers=headers)
        return r.json() if r.status_code == 200 else []
    except: return []

@st.cache_data(ttl=3)
def buscar_doacoes():
    try:
        r = httpx.get(f"{url}/rest/v1/doacoes?select=*&order=criado_em.desc", headers=headers)
        return r.json() if r.status_code == 200 else []
    except: return []

def adicionar_pontos_time(time_id, pontos=100):
    try:
        times = buscar_times()
        t = next((x for x in times if x["id"] == time_id), None)
        if t:
            novos = (t.get("pontos_totais") or 0) + pontos
            httpx.patch(f"{url}/rest/v1/times?id=eq.{time_id}", headers=headers, json={"pontos_totais": novos})
            st.cache_data.clear()
    except: pass

dados_times    = buscar_times()
dados_usuarios = buscar_usuarios()
dados_doacoes  = buscar_doacoes()

# Lista Oficial MVP de Juiz de Fora (Usada em todo o sistema)
HOSPITAIS_JF = [
    "Fundação Hemominas - JF", 
    "Santa Casa de Misericórdia JF", 
    "HPS - Hospital de Pronto Socorro", 
    "Hospital Monte Sinai", 
    "Hospital Albert Sabin"
]

# ══════════════════════════════════════════════════════════════
# 3. MÓDULO ISOLADO DO RANKING PÚBLICO
# ══════════════════════════════════════════════════════════════
def renderizar_ranking_publico():
    st.markdown('<h2 class="page-header">🏆 Ranking de Times</h2>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Cada doação vale <strong style="color:#C0152B">100 pontos</strong> para o seu time. Quem doa mais, lidera.</p>', unsafe_allow_html=True)
    st.markdown("---")

    total_doacoes  = len(dados_doacoes)
    total_doadores = len(dados_usuarios)
    total_times    = len(dados_times)
    vidas_salvas   = total_doacoes * 4

    delays = ["fade-in", "fade-in-2", "fade-in-3", "fade-in-4"]
    c1, c2, c3, c4 = st.columns(4)
    for col, val, label, delay in zip([c1, c2, c3, c4], [total_doacoes, total_doadores, total_times, vidas_salvas], ["Doações Registradas", "Doadores Cadastrados", "Times Ativos", "Vidas Salvas"], delays):
        with col:
            st.markdown(f'<div class="metric-box {delay}"><div class="metric-val">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not dados_times:
        st.info("Nenhum time cadastrado ainda.")
    else:
        medalhas, estilos, anim_del = ["🥇", "🥈", "🥉"], ["gold", "silver", "bronze"], ["fade-in", "fade-in-2", "fade-in-3"]
        for i, time in enumerate(dados_times):
            estilo  = estilos[i] if i < 3 else ""
            medalha = medalhas[i] if i < 3 else f"<span style='font-size:1rem;font-weight:700;color:#BBB'>#{i+1}</span>"
            delay   = anim_del[i] if i < 3 else "fade-in-4"
            pontos  = time.get("pontos_totais") or 0
            qtd     = len([u for u in dados_usuarios if u.get("time_id") == time["id"]])
            barra_w = min(100, max(4, int(pontos / 10))) if pontos > 0 else 4

            st.markdown(f"""
            <div class="ranking-card {estilo} {delay}">
                <div class="rank-pos">{medalha}</div>
                <div class="rank-nome">
                    {time['nome']}
                    <div style="margin-top:6px; background:#F0F0F0; border-radius:20px; height:5px; width:180px; overflow:hidden;">
                        <div style="height:5px; width:{barra_w}%; background:{'#F5A623' if i==0 else '#C0152B'}; border-radius:20px;"></div>
                    </div>
                    <span style="font-size:0.75rem; color:#AAA; font-weight:400; margin-top:4px; display:inline-block;">
                        👥 {qtd} doador(es) &nbsp;·&nbsp; <span class="codigo-badge">{time.get('codigo_convite', '')}</span>
                    </span>
                </div>
                <div style="text-align:right">
                    <div class="rank-pts">{pontos:,} pts</div>
                    <div class="rank-label">acumulados</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 4. GERENCIADOR DE ESTADO E ROTEAMENTO
# ══════════════════════════════════════════════════════════════
if "usuario_logado_id" not in st.session_state:
    st.session_state["usuario_logado_id"] = None

if "rota_deslogado" not in st.session_state:
    st.session_state["rota_deslogado"] = "PORTAL"

usuario_autenticado = st.session_state.get("usuario_logado_id")

# =====================================================================
# ROTA A: USUÁRIO DESLOGADO (SIDEBAR OCULTA)
# =====================================================================
if not usuario_autenticado:
    
    st.markdown("""
    <style>
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    # TELA 1: PORTAL DE ESCOLHA CENTRALIZADO
    if st.session_state["rota_deslogado"] == "PORTAL":
        st.markdown("""
        <div class="hero-container">
            <div style="font-size: 4rem; margin-bottom: 10px;">🩸</div>
            <h1 class="hero-title">Doe<span style="color: #C0152B;">Aqui</span></h1>
            <p class="hero-subtitle">
                A plataforma oficial para você salvar vidas, registrar suas doações 
                e fazer o seu time do coração dominar o ranking de solidariedade.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_esp1, col_btn1, col_btn2, col_btn3, col_esp2 = st.columns([1.5, 2, 2, 2, 1.5])
        with col_btn1:
            if st.button("🔐 Entrar na Conta", use_container_width=True):
                st.session_state["rota_deslogado"] = "LOGIN"
                st.rerun()
        with col_btn2:
            if st.button("➕ Criar Cadastro", use_container_width=True):
                st.session_state["rota_deslogado"] = "CADASTRO"
                st.rerun()
        with col_btn3:
            if st.button("🏆 Ver Ranking Público", use_container_width=True):
                st.session_state["rota_deslogado"] = "RANKING"
                st.rerun()

    # TELA 2: LOGIN
    elif st.session_state["rota_deslogado"] == "LOGIN":
        if st.button("🔙 Voltar ao Início", use_container_width=False):
            st.session_state["rota_deslogado"] = "PORTAL"
            st.rerun()
            
        st.markdown('<h2 class="page-header" style="margin-top:20px;">🔐 Acesso Seguro</h2>', unsafe_allow_html=True)
        st.markdown("---")
        
        col_log1, col_log2 = st.columns([1, 1])
        with col_log1:
            email_l = st.text_input("Seu E-mail:")
            senha_l = st.text_input("Sua Senha:", type="password")
            
            if st.button("Autenticar e Entrar"):
                try:
                    r = httpx.post(f"{url}/auth/v1/token?grant_type=password", headers={"apikey": key}, json={"email": email_l, "password": senha_l})
                    if r.status_code == 200:
                        st.session_state["usuario_logado_id"] = r.json()["user"]["id"]
                        st.rerun()
                    else:
                        st.error("Credenciais inválidas. Tente novamente.")
                except Exception as e:
                    st.error(f"Erro de comunicação: {e}")

    # TELA 3: CADASTRO COM SEXO BIOLÓGICO (ANVISA)
    elif st.session_state["rota_deslogado"] == "CADASTRO":
        if st.button("🔙 Voltar ao Início", use_container_width=False):
            st.session_state["rota_deslogado"] = "PORTAL"
            st.rerun()
            
        st.markdown('<h2 class="page-header" style="margin-top:20px;">➕ Cadastro de Novo Doador</h2>', unsafe_allow_html=True)
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("### Seus Dados")
            nome_novo   = st.text_input("Nome Completo *")
            email_novo  = st.text_input("E-mail para Login *")
            senha_nova  = st.text_input("Senha Segura (mínimo 6 dígitos) *", type="password")
            
            c1, c2 = st.columns(2)
            with c1: cidade_nova = st.text_input("Cidade *", value="Juiz de Fora")
            with c2: sexo_novo = st.selectbox("Sexo Biológico *", ["Masculino", "Feminino"], help="Necessário para cálculo do intervalo de doação (Anvisa).")

            st.markdown("### ⚽ Escolha seu Time")
            if dados_times:
                opcoes   = {t["nome"]: t for t in dados_times}
                time_nom = st.selectbox("Time:", list(opcoes.keys()))
                time_esc = opcoes[time_nom]
                st.markdown(f"""
                <div class="info-box fade-in" style="border-left: 3px solid #C0152B; margin-top:10px;">
                    <div style="font-weight:700; color:#1A1A2E; font-size:1rem;">⚽ {time_esc['nome']}</div>
                    <div style="margin-top:6px;">
                        <span style="color:#999; font-size:0.82rem;">Pontos atuais: </span>
                        <strong style="color:#C0152B; font-size:1.05rem;">{time_esc.get('pontos_totais') or 0:,} pts</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Nenhum time disponível.")
                time_esc = None

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🩸 Criar Cadastro e Entrar"):
                if not nome_novo or not email_novo or not senha_nova:
                    st.warning("Preencha todos os campos com asterisco.")
                elif len(senha_nova) < 6:
                    st.warning("A senha precisa ter pelo menos 6 caracteres.")
                elif not time_esc:
                    st.warning("Selecione um time.")
                elif any(u.get("email") == email_novo for u in dados_usuarios):
                    st.error("Este e-mail já está cadastrado. Volte e faça Login.")
                else:
                    try:
                        r_auth = httpx.post(f"{url}/auth/v1/signup", headers={"apikey": key}, json={"email": email_novo, "password": senha_nova})
                        id_supabase = r_auth.json().get("id") if r_auth.status_code == 200 else ("ca520f47-d6ad-46de-9a76-60bc7d3d399d" if r_auth.status_code == 429 else None)
                        
                        if id_supabase:
                            perfil = {"id": id_supabase, "nome": nome_novo, "email": email_novo, "cidade": cidade_nova, "sexo": sexo_novo, "time_id": time_esc["id"]}
                            res_p = httpx.post(f"{url}/rest/v1/usuarios", headers=headers, json=perfil)
                            
                            if res_p.status_code in [200, 201]:
                                st.cache_data.clear()
                                st.session_state["usuario_logado_id"] = id_supabase
                                st.rerun()
                            else:
                                st.error(f"Falha ao salvar perfil: {res_p.text}")
                    except Exception as e:
                        st.error(f"Erro de rede: {e}")

        with col2:
            st.markdown("### Como funciona?")
            passos = [
                ("🩸", "Cadastre-se",     "Crie seu perfil, informe seus dados e escolha o time que vai representar.",       "fade-in"),
                ("💉", "Doe Sangue",      "Vá até uma unidade do Hemominas. Homens doam a cada 60 dias e mulheres a cada 90.", "fade-in-2"),
                ("📋", "Registre",        "Informe no painel e aguarde a validação do hospital para ganhar os pontos.",                 "fade-in-3"),
                ("🏆", "Suba no Ranking", f"Cada doação validada vale <strong style='color:#C0152B'>100 pontos</strong> para o time!", "fade-in-4"),
                ("📣", "Compartilhe",     "Recrute mais amigos e fortaleça seu time no ranking.",                            "fade-in-4"),
            ]
            for icone, titulo, desc, delay in passos:
                st.markdown(f"""
                <div class="passo-card {delay}">
                    <div style="font-size:1.6rem; flex-shrink:0;">{icone}</div>
                    <div>
                        <div style="font-weight:700; color:#1A1A2E; font-size:0.95rem;">{titulo}</div>
                        <div style="color:#999; font-size:0.84rem; margin-top:3px; line-height:1.5;">{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # TELA 4: RANKING PUBLICO
    elif st.session_state["rota_deslogado"] == "RANKING":
        if st.button("🔙 Voltar ao Início", use_container_width=False):
            st.session_state["rota_deslogado"] = "PORTAL"
            st.rerun()
        renderizar_ranking_publico()


# =====================================================================
# ROTA B: USUÁRIO AUTENTICADO (AMBIENTE LOGADO)
# =====================================================================
else:
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🩸 DoeAqui</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-tagline">Ambiente Seguro.</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        tela_interna = st.radio("Navegação:", [
            "👤 Meu Painel (Doador)",
            "🏥 Portal Hemominas",
            "🏆 Ranking Geral"
        ], label_visibility="collapsed")
        
        st.markdown("---")
        if st.button("🚪 Sair do Sistema"):
            st.session_state["usuario_logado_id"] = None
            st.session_state["rota_deslogado"] = "PORTAL"
            st.rerun()
            
        st.markdown("""
        <div class="sidebar-card">
            📍 <strong>Juiz de Fora, MG</strong><br>
            Projeto Piloto · 2026<br><br>
            Desenvolvido por<br>
            <strong style="color:#C0152B !important;">Lucas Duarte</strong><br>
            <span style="color:#AAA !important;">Estudante de ADS<br>Univ. Cruzeiro do Sul</span>
        </div>
        """, unsafe_allow_html=True)

    # --- ROTA INTERNA 1: ÁREA EXCLUSIVA DO DOADOR ---
    if tela_interna == "👤 Meu Painel (Doador)":
        st.markdown('<h2 class="page-header">👤 Meu Painel Pessoal</h2>', unsafe_allow_html=True)
        st.markdown("---")

        perfil = next((u for u in dados_usuarios if u["id"] == usuario_autenticado), None)
        if not perfil and usuario_autenticado == "ca520f47-d6ad-46de-9a76-60bc7d3d399d":
            perfil = dados_usuarios[0] if dados_usuarios else None
            
        if perfil:
            time_p   = next((t for t in dados_times if t["id"] == perfil.get("time_id")), None)
            nome_t   = time_p["nome"] if time_p else "Sem time"
            pontos_t = (time_p.get("pontos_totais") or 0) if time_p else 0
            doad_p   = [d for d in dados_doacoes if d.get("usuario_id") == perfil["id"]]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="info-box fade-in">
                    <div style="font-size:1.1rem; font-weight:700; color:#1A1A2E;">{perfil['nome']}</div>
                    <div style="color:#999; font-size:0.83rem; margin-top:8px;">📧 {perfil.get('email','—')}</div>
                    <div style="color:#999; font-size:0.83rem;">📍 {perfil.get('cidade','—')} &nbsp;·&nbsp; 🧬 {perfil.get('sexo','Não Informado')}</div>
                    <div class="time-tag">⚽ {nome_t}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-box fade-in-2"><div class="metric-val">{len(doad_p)}</div><div class="metric-label">Minhas Doações</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-box fade-in-3"><div class="metric-val">{pontos_t:,}</div><div class="metric-label">Pontos do meu Time</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- NOVO FLUXO: SOLICITAÇÃO DO DOADOR ---
            st.markdown("### 📢 Avisar Nova Doação")
            st.write("Acabou de doar sangue? Informe a unidade abaixo. O hospital fará a validação e liberará os **100 pontos** para sua torcida!")
            
            col_sol1, col_sol2 = st.columns(2)
            with col_sol1:
                unidade_solicitada = st.selectbox("Onde você realizou a doação?", HOSPITAIS_JF)
            with col_sol2:
                data_solicitada = st.date_input("Qual foi a data da doação?", datetime.now())
                
            if st.button("Enviar para Validação da Hemominas"):
                payload_solicitacao = {
                    "id": str(uuid.uuid4()),
                    "usuario_id": perfil["id"],
                    "status": "Aguardando Validação do Hospital",
                    "comprovante_url": "",
                    "data_doacao": str(data_solicitada),
                    "unidade": unidade_solicitada
                }
                try:
                    res_sol = httpx.post(f"{url}/rest/v1/doacoes", headers=headers, json=payload_solicitacao)
                    if res_sol.status_code in [200, 201]:
                        st.markdown('<div class="sucesso">✅ Solicitação enviada! Acompanhe o status no seu histórico abaixo.</div>', unsafe_allow_html=True)
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Erro ao enviar a solicitação.")
                except Exception as e:
                    st.error(f"Erro de rede: {e}")

            st.markdown("---")
            st.markdown("### 📅 Meu Histórico de Doações")

            if doad_p:
                for i, d in enumerate(doad_p):
                    status_atual = d.get("status", "")
                    lib    = "Liberada" in status_atual or "Coletada" in status_atual
                    s_cor  = "#28a745" if lib else ("#F5A623" if "Aguardando" in status_atual else "#C0152B")
                    s_bg   = "#F0FBF4" if lib else ("#FFFBF0" if "Aguardando" in status_atual else "#FEE8EB")
                    
                    st.markdown(f"""
                    <div class="ranking-card fade-in" style="background:{s_bg}; border-left-color:{s_cor};">
                        <div>
                            <div style="color:#1A1A2E; font-weight:600;">📅 {d.get('data_doacao','—')}</div>
                            <div style="color:#AAA; font-size:0.82rem; margin-top:3px;">📍 {d.get('unidade','—')}</div>
                        </div>
                        <div style="color:{s_cor}; font-weight:700; font-size:0.88rem; padding:6px 14px; border-radius:20px; border: 1px solid {s_cor};">
                            {'⏳' if 'Aguardando' in status_atual else '✅'} {status_atual}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Você ainda não possui doações ou solicitações registradas.")


    # --- ROTA INTERNA 2: PORTAL ADMINISTRATIVO COM DUPLA VALIDAÇÃO ---
    elif tela_interna == "🏥 Portal Hemominas":
        st.markdown('<h2 class="page-header">🏥 Portal Administrativo — Hemominas</h2>', unsafe_allow_html=True)
        st.markdown("---")

        pendentes_geral = len([d for d in dados_doacoes if "Aguardando" in (d.get("status") or "")])
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-box fade-in"><div class="metric-val">{len(dados_doacoes)}</div><div class="metric-label">Total de Registros</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-box fade-in-2"><div class="metric-val">{len(dados_usuarios)}</div><div class="metric-label">Doadores Cadastrados</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-box fade-in-3"><div class="metric-val">{pendentes_geral}</div><div class="metric-label">Aguardando Validação</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Abas exclusivas da Administração: Validar Pendentes x Lançamento Manual
        abas_hemo = st.tabs(["✅ Validar Doações Pendentes", "💉 Lançamento Manual (Balcão)"])
        
        with abas_hemo[0]:
            st.write("Abaixo estão as doações informadas pelos usuários que aguardam a conferência do hospital para liberar a pontuação.")
            bolsas_pendentes = [d for d in dados_doacoes if "Aguardando Validação" in (d.get("status") or "")]
            
            if bolsas_pendentes:
                col_v1, col_v2 = st.columns([2, 1])
                with col_v1:
                    dict_pendentes = {}
                    for p in bolsas_pendentes:
                        nome_d = next((u["nome"] for u in dados_usuarios if u["id"] == p.get("usuario_id")), "Desconhecido")
                        label = f"📝 {nome_d} - {p.get('unidade')} ({p.get('data_doacao')})"
                        dict_pendentes[label] = p
                    
                    bolsa_sel_label = st.selectbox("Selecione o doador que compareceu:", list(dict_pendentes.keys()))
                    bolsa_alvo = dict_pendentes[bolsa_sel_label]
                    
                with col_v2:
                    acao_hospital = st.selectbox("Ação Administrativa:", ["Validar Coleta (Liberar 100 Pts)", "Doação Não Realizada (Cancelar)"])
                    
                if st.button("Confirmar Validação de Segurança"):
                    try:
                        novo_status = "Bolsa Coletada - Em Análise" if "Validar" in acao_hospital else "Cancelada / Não Compareceu"
                        res_patch = httpx.patch(f"{url}/rest/v1/doacoes?id=eq.{bolsa_alvo['id']}", headers=headers, json={"status": novo_status})
                        
                        if res_patch.status_code in [200, 204]:
                            if "Validar" in acao_hospital:
                                user_alvo = next((u for u in dados_usuarios if u["id"] == bolsa_alvo["usuario_id"]), None)
                                if user_alvo:
                                    adicionar_pontos_time(user_alvo.get("time_id"), 100)
                                st.markdown('<div class="sucesso">✅ Validação concluída! Os 100 pontos foram creditados para a torcida.</div>', unsafe_allow_html=True)
                            else:
                                st.warning("A solicitação foi cancelada.")
                            
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error("Erro na comunicação com o banco.")
                    except Exception as e:
                        st.error(f"Erro de rede: {e}")
            else:
                st.info("Parabéns! Não há nenhuma doação pendente de validação no seu painel.")

        with abas_hemo[1]:
            st.write("Use este formulário apenas para doadores que não avisaram no aplicativo previamente.")
            if dados_usuarios:
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    doador_sel  = st.selectbox("Localizar Doador no Sistema:", [d["nome"] for d in dados_usuarios])
                    unidade_sel = st.selectbox("Unidade de Coleta atual:", HOSPITAIS_JF)
                with col_m2:
                    status_sel = st.selectbox("Status da Bolsa:", ["Bolsa Coletada - Em Análise", "Liberada para Uso"])
                    data_sel   = st.date_input("Data do Procedimento:", datetime.now(), key="dt_manual")

                if st.button("✅ Registrar Manualmente e Creditar 100 Pontos"):
                    doador_obj = next((d for d in dados_usuarios if d["nome"] == doador_sel), None)
                    if doador_obj:
                        payload = {
                            "id": str(uuid.uuid4()),
                            "usuario_id": doador_obj["id"],
                            "status": status_sel,
                            "comprovante_url": "",
                            "data_doacao": str(data_sel),
                            "unidade": unidade_sel
                        }
                        try:
                            res = httpx.post(f"{url}/rest/v1/doacoes", headers=headers, json=payload)
                            if res.status_code in [200, 201]:
                                adicionar_pontos_time(doador_obj.get("time_id"), 100)
                                st.markdown('<div class="sucesso">✅ Coleta lançada com sucesso! Pontuação do time atualizada.</div>', unsafe_allow_html=True)
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error(f"Erro: {res.text}")
                        except Exception as e:
                            st.error(f"Erro de rede: {e}")
            else:
                st.warning("Cadastre doadores antes de registrar doações manuais.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Relatório Histórico Global")
        if dados_doacoes:
            tabela = []
            for d in dados_doacoes[:20]:
                nome_d = next((u["nome"] for u in dados_usuarios if u["id"] == d.get("usuario_id")), "—")
                tabela.append({
                    "Doador": nome_d,
                    "Data": d.get("data_doacao","—"),
                    "Unidade": d.get("unidade","—"),
                    "Status": d.get("status","—"),
                })
            st.dataframe(tabela, use_container_width=True, hide_index=True)

    # --- ROTA INTERNA 3: RANKING ---
    elif tela_interna == "🏆 Ranking Geral":
        renderizar_ranking_publico()
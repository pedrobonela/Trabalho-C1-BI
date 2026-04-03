from pathlib import Path
import unicodedata

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Dashboard COVID-19 ES",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
CSV_PADRAO = BASE_DIR / "MICRODADOS.csv"
CSV_REDUZIDO = BASE_DIR / "MICRODADOS_reduzido.csv"
COLUNAS_DATA = [
    "DataNotificacao",
    "DataCadastro",
    "DataDiagnostico",
    "DataColeta_RT_PCR",
    "DataColetaTesteRapido",
    "DataColetaSorologia",
    "DataColetaSorologiaIGG",
    "DataEncerramento",
    "DataObito",
]
COLUNAS_SINTOMAS = [
    "Febre",
    "DificuldadeRespiratoria",
    "Tosse",
    "Coriza",
    "DorGarganta",
    "Diarreia",
    "Cefaleia",
]
COLUNAS_COMORBIDADES = [
    "ComorbidadePulmao",
    "ComorbidadeCardio",
    "ComorbidadeRenal",
    "ComorbidadeDiabetes",
    "ComorbidadeTabagismo",
    "ComorbidadeObesidade",
]
COR_FUNDO_FIGURA = "#07111f"
COR_FUNDO_EIXO = "#0f1b2d"
COR_BORDA = "#28435f"
COR_TEXTO = "#e5eefb"
COR_TEXTO_SUAVE = "#8ba3bf"
COR_GRID = "#28435f"
MUNICIPIOS_ES = {
    "afonso claudio",
    "agua doce do norte",
    "aguia branca",
    "alegre",
    "alfredo chaves",
    "alto rio novo",
    "anchieta",
    "apiaca",
    "aracruz",
    "atilio vivacqua",
    "baixo guandu",
    "barra de sao francisco",
    "boa esperanca",
    "bom jesus do norte",
    "brejetuba",
    "cachoeiro de itapemirim",
    "cariacica",
    "castelo",
    "colatina",
    "conceicao da barra",
    "conceicao do castelo",
    "divino de sao lourenco",
    "domingos martins",
    "dores do rio preto",
    "ecoporanga",
    "fundao",
    "governador lindenberg",
    "guacui",
    "guarapari",
    "ibatiba",
    "ibiracu",
    "ibitirama",
    "iconha",
    "irupi",
    "itaguacu",
    "itapemirim",
    "itarana",
    "iuna",
    "jaguare",
    "jeronimo monteiro",
    "joao neiva",
    "laranja da terra",
    "linhares",
    "mantenopolis",
    "marataizes",
    "marechal floriano",
    "marilandia",
    "mimoso do sul",
    "montanha",
    "mucurici",
    "muniz freire",
    "muqui",
    "nova venecia",
    "pancas",
    "pedro canario",
    "pinheiros",
    "piuma",
    "ponto belo",
    "presidente kennedy",
    "rio bananal",
    "rio novo do sul",
    "santa leopoldina",
    "santa maria de jetiba",
    "santa teresa",
    "sao domingos do norte",
    "sao gabriel da palha",
    "sao jose do calcado",
    "sao mateus",
    "sao roque do canaa",
    "serra",
    "sooretama",
    "vargem alta",
    "venda nova do imigrante",
    "viana",
    "vila pavao",
    "vila valerio",
    "vila velha",
    "vitoria",
}


st.markdown(
    """
    <style>
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        .block-container {
            max-width: 1320px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }

        .hero-shell {
            position: relative;
            overflow: hidden;
            border-radius: 28px;
            padding: 2rem 2rem 1.6rem 2rem;
            margin-bottom: 1.4rem;
            background:
                radial-gradient(circle at top left, rgba(56, 189, 248, 0.35), transparent 30%),
                radial-gradient(circle at bottom right, rgba(45, 212, 191, 0.25), transparent 32%),
                linear-gradient(135deg, #0f172a 0%, #111827 48%, #0b1220 100%);
            border: 1px solid rgba(148, 163, 184, 0.18);
            color: white;
            box-shadow: 0 24px 60px rgba(15, 23, 42, 0.34);
        }

        .hero-kicker {
            font-size: 0.88rem;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            font-weight: 700;
            color: #7dd3fc;
            margin-bottom: 0.55rem;
        }

        .hero-title {
            font-size: 2.8rem;
            line-height: 1.05;
            font-weight: 900;
            margin: 0;
            max-width: 760px;
        }

        .hero-subtitle {
            margin-top: 0.9rem;
            max-width: 760px;
            color: #cbd5e1;
            font-size: 1rem;
            line-height: 1.7;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 1rem;
            align-items: end;
        }

        .hero-stats {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
        }

        .hero-stat {
            background: rgba(15, 23, 42, 0.42);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 20px;
            padding: 1rem 1rem 0.9rem 1rem;
            backdrop-filter: blur(6px);
        }

        .hero-stat-label {
            color: #94a3b8;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }

        .hero-stat-value {
            font-size: 1.7rem;
            line-height: 1;
            font-weight: 800;
            color: #f8fafc;
        }

        .hero-stat-value.range {
            font-size: 1.15rem;
            line-height: 1.35;
        }

        .hero-stat-note {
            margin-top: 0.45rem;
            color: #cbd5e1;
            font-size: 0.9rem;
        }

        .panel-card {
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.88), rgba(8, 15, 28, 0.92));
            border: 1px solid rgba(71, 85, 105, 0.42);
            border-radius: 22px;
            padding: 1.05rem 1.15rem;
            margin-bottom: 1rem;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
        }

        .filter-card {
            background: linear-gradient(135deg, #eff6ff 0%, #ecfeff 100%);
            border: 1px solid #cfe5ff;
            border-radius: 22px;
            padding: 1rem 1rem 0.2rem 1rem;
            margin-bottom: 1rem;
        }

        .section-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #0284c7;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }

        .section-title {
            font-size: 1.55rem;
            font-weight: 800;
            color: #e2e8f0;
            margin-bottom: 0.75rem;
        }

        .footer-note {
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(148, 163, 184, 0.25);
            font-size: 0.9rem;
            color: #94a3b8;
        }

        @media (max-width: 980px) {
            .hero-grid {
                grid-template-columns: 1fr;
            }

            .hero-stats {
                grid-template-columns: 1fr;
            }

            .hero-title {
                font-size: 2rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def normalizar_texto(valor: str) -> str:
    return (
        unicodedata.normalize("NFKD", str(valor).strip().lower())
        .encode("ascii", "ignore")
        .decode("utf-8")
    )


def carregar_dados(fonte):
    df_bruto = pd.read_csv(fonte, sep=";", encoding="latin-1", low_memory=False)

    for coluna in COLUNAS_DATA:
        if coluna in df_bruto.columns:
            try:
                df_bruto[coluna] = pd.to_datetime(
                    df_bruto[coluna], errors="coerce", format="mixed"
                )
            except TypeError:
                df_bruto[coluna] = pd.to_datetime(df_bruto[coluna], errors="coerce")

    df_base_es = df_bruto.copy()
    if "Municipio" in df_base_es.columns:
        municipios_comparaveis = (
            df_base_es["Municipio"]
            .fillna("")
            .astype(str)
            .map(normalizar_texto)
        )
        df_base_es = df_base_es[municipios_comparaveis.isin(MUNICIPIOS_ES)].copy()

    return df_bruto, df_base_es


def formatar_numero(valor: int) -> str:
    return f"{int(valor):,}".replace(",", ".")


def coluna_normalizada(df: pd.DataFrame, coluna: str) -> pd.Series:
    return df[coluna].fillna("Nao informado").astype(str).str.strip()


def coluna_comparavel(df: pd.DataFrame, coluna: str) -> pd.Series:
    serie = df[coluna].fillna("").astype(str).str.strip().str.lower()
    return serie.map(normalizar_texto)


def contagem_sim(df: pd.DataFrame, colunas: list[str]) -> pd.Series:
    validas = [coluna for coluna in colunas if coluna in df.columns]
    dados = {
        coluna: (coluna_comparavel(df, coluna) == "sim").sum()
        for coluna in validas
    }
    return pd.Series(dados).sort_values(ascending=False)


def estilizar_eixos(ax, titulo: str):
    ax.set_title(titulo, color=COR_TEXTO, fontsize=14, fontweight="bold", loc="left", pad=14)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_facecolor(COR_FUNDO_EIXO)
    ax.grid(axis="y", linestyle="--", alpha=0.35, color=COR_GRID)
    ax.tick_params(axis="x", colors=COR_TEXTO_SUAVE, labelsize=9)
    ax.tick_params(axis="y", colors=COR_TEXTO_SUAVE, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(COR_BORDA)
        spine.set_alpha(0.7)


def grafico_barra(serie: pd.Series, titulo: str, cor: str, horizontal: bool = False, rotacao: int = 0):
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(COR_FUNDO_FIGURA)
    if horizontal:
        serie.plot(kind="barh", ax=ax, color=cor, edgecolor=cor, width=0.68)
    else:
        serie.plot(kind="bar", ax=ax, color=cor, edgecolor=cor, width=0.68)
    estilizar_eixos(ax, titulo)
    ax.tick_params(axis="x", rotation=rotacao)
    if horizontal:
        ax.grid(axis="x", linestyle="--", alpha=0.35, color=COR_GRID)
        ax.grid(axis="y", visible=False)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def grafico_linha(serie: pd.Series, titulo: str, cor: str):
    fig, ax = plt.subplots(figsize=(10, 4.8))
    fig.patch.set_facecolor(COR_FUNDO_FIGURA)
    x = range(len(serie))
    ax.plot(x, serie.values, color=cor, linewidth=2.6, marker="o", markersize=3.8)
    ax.fill_between(x, serie.values, color=cor, alpha=0.18)
    estilizar_eixos(ax, titulo)
    passo = max(1, len(serie) // 8)
    indices = list(range(0, len(serie), passo))
    if indices[-1] != len(serie) - 1:
        indices.append(len(serie) - 1)
    ax.set_xticks(indices)
    ax.set_xticklabels([serie.index[i] for i in indices], rotation=35, ha="right")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def grafico_pizza(serie: pd.Series, titulo: str):
    fig, ax = plt.subplots(figsize=(6.2, 6.2))
    fig.patch.set_facecolor(COR_FUNDO_FIGURA)
    ax.set_facecolor(COR_FUNDO_EIXO)
    cores = ["#38bdf8", "#22c55e", "#2dd4bf", "#f59e0b", "#8b5cf6", "#fb7185"]
    serie.plot(
        kind="pie",
        ax=ax,
        autopct="%1.1f%%",
        startangle=90,
        colors=cores[: len(serie)],
        textprops={"color": COR_TEXTO, "fontsize": 10, "fontweight": "bold"},
        wedgeprops={"linewidth": 1.2, "edgecolor": COR_FUNDO_EIXO},
        pctdistance=0.75,
    )
    ax.set_title(titulo, color=COR_TEXTO, fontsize=14, fontweight="bold", loc="left", pad=14)
    ax.set_ylabel("")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


fonte_dados = CSV_PADRAO

if not CSV_PADRAO.exists():
    fonte_dados = CSV_REDUZIDO

if not Path(fonte_dados).exists():
    st.error(
        "Nenhum arquivo de dados foi encontrado. O app precisa de `MICRODADOS.csv` "
        "ou `MICRODADOS_reduzido.csv` na pasta do projeto."
    )
    st.stop()

df_bruto, df_base_es = carregar_dados(
    str(fonte_dados) if isinstance(fonte_dados, Path) else fonte_dados
)
total_original = len(df_bruto)
registros_removidos = total_original - len(df_base_es)

data_min = None
data_max = None
if "DataNotificacao" in df_bruto.columns:
    datas_validas = df_bruto["DataNotificacao"].dropna()
    if not datas_validas.empty:
        data_min = datas_validas.min().date()
        data_max = datas_validas.max().date()


st.markdown(
    f"""
    <div class="hero-shell">
        <div class="hero-grid">
            <div>
                <div class="hero-kicker">Dashboard interativo</div>
                <h1 class="hero-title">COVID-19 ES - Painel Analitico dos Microdados</h1>
                <div class="hero-subtitle">
                    Atividade avaliativa da Materia de Bussines Intelligence
                        - Desenvolvido por Pedro Bonela
                </div>
            </div>
            <div class="hero-stats">
                <div class="hero-stat">
                    <div class="hero-stat-label">Base completa</div>
                    <div class="hero-stat-value">{formatar_numero(len(df_base_es))}</div>
                    <div class="hero-stat-note">registros carregados</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-label">Municipios ES</div>
                    <div class="hero-stat-value">{formatar_numero(df_base_es['Municipio'].nunique() if 'Municipio' in df_base_es.columns else 0)}</div>
                    <div class="hero-stat-note">nas visoes territoriais</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-label">Periodo</div>
                    <div class="hero-stat-value range">
                        {f"{data_min.strftime('%d/%m/%Y')} ate {data_max.strftime('%d/%m/%Y')}" if data_min and data_max else "-"}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


op_municipios = sorted(df_base_es["Municipio"].dropna().astype(str).unique().tolist()) if "Municipio" in df_base_es.columns else []
op_classificacao = sorted(df_base_es["Classificacao"].dropna().astype(str).unique().tolist()) if "Classificacao" in df_base_es.columns else []
op_sexo = sorted(df_base_es["Sexo"].dropna().astype(str).unique().tolist()) if "Sexo" in df_base_es.columns else []
op_faixa = sorted(df_base_es["FaixaEtaria"].dropna().astype(str).unique().tolist()) if "FaixaEtaria" in df_base_es.columns else []

municipios_sel = []
classificacao_sel = []
sexo_sel = []
faixa_sel = []
periodo_sel = None

with st.expander("Filtros", expanded=False):
    f1, f2, f3, f4 = st.columns(4)

    municipios_sel = f1.multiselect("Municipio", op_municipios, placeholder="Todos")
    classificacao_sel = f2.multiselect("Classificacao", op_classificacao, placeholder="Todas")
    sexo_sel = f3.multiselect("Sexo", op_sexo, placeholder="Todos")
    faixa_sel = f4.multiselect("Faixa etaria", op_faixa, placeholder="Todas")

    if data_min and data_max:
        periodo_sel = st.date_input(
            "Periodo de notificacao",
            value=(data_min, data_max),
            min_value=data_min,
            max_value=data_max,
        )

df_filtrado_geral = df_bruto.copy()
df_filtrado_municipios = df_base_es.copy()

if classificacao_sel and "Classificacao" in df_filtrado_geral.columns:
    df_filtrado_geral = df_filtrado_geral[coluna_normalizada(df_filtrado_geral, "Classificacao").isin(classificacao_sel)]
    df_filtrado_municipios = df_filtrado_municipios[coluna_normalizada(df_filtrado_municipios, "Classificacao").isin(classificacao_sel)]
if sexo_sel and "Sexo" in df_filtrado_geral.columns:
    df_filtrado_geral = df_filtrado_geral[coluna_normalizada(df_filtrado_geral, "Sexo").isin(sexo_sel)]
    df_filtrado_municipios = df_filtrado_municipios[coluna_normalizada(df_filtrado_municipios, "Sexo").isin(sexo_sel)]
if faixa_sel and "FaixaEtaria" in df_filtrado_geral.columns:
    df_filtrado_geral = df_filtrado_geral[coluna_normalizada(df_filtrado_geral, "FaixaEtaria").isin(faixa_sel)]
    df_filtrado_municipios = df_filtrado_municipios[coluna_normalizada(df_filtrado_municipios, "FaixaEtaria").isin(faixa_sel)]
if (
    periodo_sel
    and len(periodo_sel) == 2
    and "DataNotificacao" in df_filtrado_geral.columns
):
    inicio = pd.to_datetime(periodo_sel[0])
    fim = pd.to_datetime(periodo_sel[1])
    df_filtrado_geral = df_filtrado_geral[df_filtrado_geral["DataNotificacao"].between(inicio, fim)]
    df_filtrado_municipios = df_filtrado_municipios[df_filtrado_municipios["DataNotificacao"].between(inicio, fim)]

if municipios_sel and "Municipio" in df_filtrado_municipios.columns:
    df_filtrado_municipios = df_filtrado_municipios[
        coluna_normalizada(df_filtrado_municipios, "Municipio").isin(municipios_sel)
    ]
    df_filtrado_geral = df_filtrado_municipios.copy()

df_filtrado = df_filtrado_geral.copy()
df_territorial = df_filtrado_municipios.copy()

if df_filtrado.empty:
    st.error("Os filtros aplicados nao retornaram registros. Ajuste a selecao para continuar.")
    st.stop()

total_registros = len(df_filtrado)
confirmados = (
    (coluna_normalizada(df_filtrado, "Classificacao") == "Confirmados").sum()
    if "Classificacao" in df_filtrado.columns
    else 0
)
obitos = (
    (coluna_comparavel(df_filtrado, "Evolucao") == "obito pelo covid-19").sum()
    if "Evolucao" in df_filtrado.columns
    else 0
)
internacoes = (
    (coluna_comparavel(df_filtrado, "FicouInternado") == "sim").sum()
    if "FicouInternado" in df_filtrado.columns
    else 0
)
profissionais_saude = (
    (coluna_comparavel(df_filtrado, "ProfissionalSaude") == "sim").sum()
    if "ProfissionalSaude" in df_filtrado.columns
    else 0
)
letalidade = (obitos / confirmados * 100) if confirmados else 0


tabs = st.tabs(["Visao geral", "Perfil dos casos", "Saude e desfechos", "Exploracao de dados"])

with tabs[0]:
    c1, c2 = st.columns([1.35, 1])

    with c1:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-label">Panorama</div>
                <div class="section-title">Evolucao das notificacoes</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if "DataNotificacao" in df_filtrado.columns:
            serie_tempo = (
                df_filtrado.dropna(subset=["DataNotificacao"])
                .assign(AnoMes=lambda frame: frame["DataNotificacao"].dt.to_period("M").astype(str))
                .groupby("AnoMes")
                .size()
            )
            if not serie_tempo.empty:
                grafico_linha(serie_tempo, "Notificacoes por mes", "#22c55e")

    with c2:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-label">Distribuicao</div>
                <div class="section-title">Classificacao dos casos</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if "Classificacao" in df_filtrado.columns:
            classificacao = coluna_normalizada(df_filtrado, "Classificacao").value_counts().head(8)
            grafico_barra(classificacao, "Classificacao", "#38bdf8", horizontal=True)

    c3, c4 = st.columns([1, 1])
    with c3:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-label">Territorio</div>
                <div class="section-title">Top 10 municipios</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if "Municipio" in df_territorial.columns:
            top_municipios = coluna_normalizada(df_territorial, "Municipio").value_counts().head(10)
            grafico_barra(top_municipios, "Municipios com mais notificacoes", "#0ea5e9", rotacao=35)

    with c4:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-label">Cadencia</div>
                <div class="section-title">Status da notificacao</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if "StatusNotificacao" in df_filtrado.columns:
            status = coluna_normalizada(df_filtrado, "StatusNotificacao").value_counts().head(6)
            grafico_pizza(status, "Status da notificacao")

with tabs[1]:
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-label">Demografia</div>
                <div class="section-title">Distribuicao por sexo</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if "Sexo" in df_filtrado.columns:
            sexo = coluna_normalizada(df_filtrado, "Sexo").value_counts()
            grafico_pizza(sexo, "Sexo")

    with c2:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-label">Demografia</div>
                <div class="section-title">Faixas etarias</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if "FaixaEtaria" in df_filtrado.columns:
            faixa = coluna_normalizada(df_filtrado, "FaixaEtaria").value_counts().sort_index()
            grafico_barra(faixa, "Casos por faixa etaria", "#8b5cf6", rotacao=35)

    c3, c4 = st.columns([1.2, 0.8])
    with c3:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-label">Contexto social</div>
                <div class="section-title">Raca/cor e escolaridade</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if "RacaCor" in df_filtrado.columns:
            raca = coluna_normalizada(df_filtrado, "RacaCor").value_counts().head(8)
            grafico_barra(raca, "Raca/cor", "#f59e0b", horizontal=True)

    with c4:
        if "Escolaridade" in df_filtrado.columns:
            escolaridade = (
                coluna_normalizada(df_filtrado, "Escolaridade")
                .value_counts()
                .head(8)
                .rename_axis("Escolaridade")
                .reset_index(name="Quantidade")
            )
            st.dataframe(escolaridade, use_container_width=True, hide_index=True)

with tabs[2]:
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-label">Sintomas</div>
                <div class="section-title">Ocorrencia dos sintomas</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        sintomas = contagem_sim(df_filtrado, COLUNAS_SINTOMAS)
        if not sintomas.empty:
            grafico_barra(sintomas, "Sintomas mais frequentes", "#14b8a6", horizontal=True)

    with c2:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-label">Comorbidades</div>
                <div class="section-title">Fatores de risco na base</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        comorbidades = contagem_sim(df_filtrado, COLUNAS_COMORBIDADES)
        if not comorbidades.empty:
            grafico_barra(comorbidades, "Comorbidades mais informadas", "#ef4444")

    c3, c4 = st.columns([1.1, 0.9])
    with c3:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-label">Desfecho</div>
                <div class="section-title">Evolucao dos casos nos top municipios</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if "Municipio" in df_territorial.columns and "Evolucao" in df_territorial.columns:
            top5 = coluna_normalizada(df_territorial, "Municipio").value_counts().head(5).index
            base_top = df_territorial[coluna_normalizada(df_territorial, "Municipio").isin(top5)].copy()
            tabela = pd.crosstab(
                coluna_normalizada(base_top, "Municipio"),
                coluna_normalizada(base_top, "Evolucao"),
            )
            st.dataframe(tabela, use_container_width=True)

    with c4:
        st.markdown(
            """
            <div class="panel-card">
                <div class="section-label">Indicadores</div>
                <div class="section-title">Recortes especiais</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        esp1, esp2, esp3 = st.columns(3)
        esp1.metric(
            "Prof. saude",
            formatar_numero(profissionais_saude),
        )
        esp2.metric(
            "Gestantes",
            formatar_numero((coluna_comparavel(df_filtrado, "Gestante") == "sim").sum() if "Gestante" in df_filtrado.columns else 0),
        )
        esp3.metric(
            "Deficiencia",
            formatar_numero((coluna_comparavel(df_filtrado, "PossuiDeficiencia") == "sim").sum() if "PossuiDeficiencia" in df_filtrado.columns else 0),
        )

        indicadores = pd.DataFrame(
            [
                ["Morador de rua", formatar_numero((coluna_comparavel(df_filtrado, "MoradorDeRua") == "sim").sum() if "MoradorDeRua" in df_filtrado.columns else 0)],
                ["Viagem no Brasil", formatar_numero((coluna_comparavel(df_filtrado, "ViagemBrasil") == "sim").sum() if "ViagemBrasil" in df_filtrado.columns else 0)],
                ["Viagem internacional", formatar_numero((coluna_comparavel(df_filtrado, "ViagemInternacional") == "sim").sum() if "ViagemInternacional" in df_filtrado.columns else 0)],
            ],
            columns=["Indicador", "Quantidade"],
        )
        st.dataframe(indicadores, use_container_width=True, hide_index=True)

with tabs[3]:
    st.markdown(
        """
        <div class="panel-card">
            <div class="section-label">Base filtrada</div>
            <div class="section-title">Amostra de dados e estrutura</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1.1, 0.9])
    with c1:
        st.dataframe(df_filtrado.head(200), use_container_width=True)
    with c2:
        tipos = (
            df_filtrado.dtypes.astype(str)
            .rename_axis("Coluna")
            .reset_index(name="Tipo")
        )
        st.dataframe(tipos, use_container_width=True, hide_index=True)

    nulos = (
        df_filtrado.isnull()
        .sum()
        .sort_values(ascending=False)
        .rename_axis("Coluna")
        .reset_index(name="Valores nulos")
    )
    st.dataframe(nulos, use_container_width=True, hide_index=True)


fonte_texto = (
    str(fonte_dados)
    if isinstance(fonte_dados, Path)
    else "arquivo de dados local"
)
st.markdown(
    f"""
    <div class="footer-note">
        Fonte de dados: Painel COVID-19 ES - <a href="https://coronavirus.es.gov.br/painel-covid-19-es" target="_blank">coronavirus.es.gov.br/painel-covid-19-es</a><br>
        Arquivo utilizado no app: {fonte_texto}<br>
        Observacao: a versao publicada usa uma amostra reduzida da base para viabilizar o deploy online.<br>
        Painel desenvolvido a partir do notebook <strong>Atividade_C1_PedroBonela.ipynb</strong>.
    </div>
    """,
    unsafe_allow_html=True,
)

import pandas as pd
import unicodedata

df_genero = pd.read_csv(
    "Dados empreg mulheres.csv",
    sep=";",
     encoding="utf-8-sig")
colunas_id = ["Sigla", "Codigo", "Estado"]
colunas_valor = [c for c in df_genero.columns if c not in colunas_id]
dados_genero = df_genero.melt(
    id_vars=colunas_id,
    value_vars=colunas_valor,
    var_name="variavel",
    value_name="percentual")
dados_genero[["atividade", "ano"]] = (
    dados_genero["variavel"]
    .str.rsplit(" ", n=1, expand=True))
dados_genero["ano"] = dados_genero["ano"].astype(int)
dados_genero= dados_genero.drop(columns="variavel")
dados_genero["percentual"] = (
    dados_genero["percentual"]
    .str.replace(",", ".", regex=False)
    .astype(float))


################## Dados educação ##################
def carregar_prouni(ano):
    return pd.read_csv(
        f"pda-prouni-{ano}.csv",
        sep=";",
        encoding="latin1"
    )
edu_2015 = carregar_prouni(2015)
edu_2016 = carregar_prouni(2016)
edu_2017 = carregar_prouni(2017)
edu_2018 = carregar_prouni(2018)
edu_2019 = carregar_prouni(2019)
edu_2020 = carregar_prouni(2020)

mapa_colunas = {
    "ï»¿ANO_CONCESSAO_BOLSA": "ANO_CONCESSAO_BOLSA",
    "CPF_BENEFICIARIO_BOLSA": "CPF_BENEFICIARIO",
    "SEXO_BENEFICIARIO_BOLSA": "SEXO_BENEFICIARIO",
    "RACA_BENEFICIARIO_BOLSA": "RACA_BENEFICIARIO",
    "DT_NASCIMENTO_BENEFICIARIO": "DATA_NASCIMENTO",
    "REGIAO_BENEFICIARIO_BOLSA": "REGIAO_BENEFICIARIO",
    "SIGLA_UF_BENEFICIARIO_BOLSA": "UF_BENEFICIARIO",
    "MUNICIPIO_BENEFICIARIO_BOLSA": "MUNICIPIO_BENEFICIARIO"}
def padronizar_colunas(df):
    return df.rename(columns=mapa_colunas)

edu_2015 = padronizar_colunas(edu_2015)
edu_2016 = padronizar_colunas(edu_2016)
edu_2017 = padronizar_colunas(edu_2017)
edu_2018 = padronizar_colunas(edu_2018)
edu_2019 = padronizar_colunas(edu_2019)
edu_2020 = padronizar_colunas(edu_2020)
colunas_padrao = edu_2015.columns

edu_2020 = edu_2020[colunas_padrao]
prouni = pd.concat(
    [edu_2015, edu_2016, edu_2017, edu_2018, edu_2019, edu_2020],
    ignore_index=True)
prouni["REGIAO_BENEFICIARIO"] = (
    prouni["REGIAO_BENEFICIARIO"]
    .astype(str)
    .str.strip()
    .str.upper())
prouni = prouni.dropna(subset=["REGIAO_BENEFICIARIO"])
prouni = prouni[prouni["REGIAO_BENEFICIARIO"] != "NAN"]
prouni_agg = (
    prouni
    .groupby([
        "ANO_CONCESSAO_BOLSA",
        "SEXO_BENEFICIARIO",
        "RACA_BENEFICIARIO",
        "REGIAO_BENEFICIARIO",
        "MODALIDADE_ENSINO_BOLSA",
        "NOME_TURNO_CURSO_BOLSA"])
    .size()
    .reset_index(name="quantidade"))
mapa_sexo = {
    "F": "Feminino",
    "M": "Masculino",
    "Feminino": "Feminino",
    "Masculino": "Masculino"}

prouni_agg["SEXO_BENEFICIARIO"] = (
    prouni_agg["SEXO_BENEFICIARIO"]
    .map(mapa_sexo))
prouni_agg["sexo_raca"] = (
    prouni_agg["SEXO_BENEFICIARIO"] + " - " + prouni_agg["RACA_BENEFICIARIO"])
prouni_agg["percentual"] = (
    prouni_agg
    .groupby("ANO_CONCESSAO_BOLSA")["quantidade"]
    .transform(lambda x: 100 * x / x.sum()))

def normalizar_texto(txt):
    if pd.isna(txt):
        return txt
    txt = str(txt).strip()
    txt = unicodedata.normalize("NFKD", txt)
    txt = txt.encode("ascii", "ignore").decode("utf-8")
    return txt.title()
prouni_agg["RACA_BENEFICIARIO"] = prouni_agg["RACA_BENEFICIARIO"].apply(normalizar_texto)
prouni_agg["RACA_BENEFICIARIO"] = prouni_agg["RACA_BENEFICIARIO"].replace({
    "Indagena": "Indigena",
    "Indgena": "Indigena"})
prouni_agg = prouni_agg[prouni_agg["RACA_BENEFICIARIO"] != "Nao Informada"]
mapa_regioes = {
    "NORTE": "Norte",
    "NORDESTE": "Nordeste",
    "SUDESTE": "Sudeste",
    "SUL": "Sul",
    "CENTRO-OESTE": "Centro-Oeste",
    "CENTRO OESTE": "Centro-Oeste"}
prouni_agg["REGIAO_BENEFICIARIO"] = (
    prouni_agg["REGIAO_BENEFICIARIO"]
    .replace(mapa_regioes))
bolsas_por_ano = (
    prouni_agg
    .groupby("ANO_CONCESSAO_BOLSA", as_index=False)["quantidade"]
    .sum()
    .rename(columns={"quantidade": "total_bolsas"}))
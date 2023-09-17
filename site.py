import streamlit as st
import psycopg2
import os
import pandas as pd

#Importando variáveis no render
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_DATABASE = os.environ.get('DB_DATABASE')

# Função para conectar ao PostgreSQL
def conectar_postgresql():
    try:
        # Substitua as informações de conexão com seu próprio host, banco de dados, usuário e senha
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_DATABASE,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

# Função para executar consultas SQL e retornar um DataFrame Pandas
def executar_consulta(conn, query):
    try:
        return pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Erro ao executar consulta: {e}")
        return None

# Título do aplicativo
st.title("Streamlit com PostgreSQL")

# Conectar ao PostgreSQL
conn = conectar_postgresql()

#Buscando informações no banco de dados
if conn:
    st.subheader("Exibindo informações da tabela SINASC_RO")
    query = "select * from bdestudo.public.sinasc_ro;"
    resultado = executar_consulta(conn, query)

    # Exibir os resultados em um DataFrame
    if resultado is not None:
        st.dataframe(resultado)
else:
    st.warning("Não foi possível obter informações do banco de dados.")
    
if conn:
    #Executando a consulta SQL
    consulta_sql = "select * from bdestudo.public.sinasc_ro limit 80;"
    resultado = executar_consulta(conn, consulta_sql)
    if resultado is not None:

    #Criando gráfico de barras
        st.subheader("Gráfico de Barras (limitado a 80 pessoas)")
        coluna_para_grafico = st.selectbox("Selecione o campo abaixo para gerar o gráfico:", resultado.columns)
        if coluna_para_grafico:
            st.bar_chart(resultado[coluna_para_grafico])
else:
    st.warning("Não foi possível obter informações para montar o gráfico de barras")

#
#
# 
   
#Criando um formulário para registrar novos RNs
st.subheader('Use o Form abaixo para registrar um RN(Recém-Nascido) no banco de dados!')
idademae = st.number_input('Idade da Mãe', min_value=0)
sexo = st.selectbox('Sexo do RN', ['Masculino', 'Feminino'])
peso = st.number_input('Peso', min_value=0.0)
idadepai = st.number_input('Idade do Pai', min_value=0)
nome = st.text_input('Nome completo do RN')

#Criando o cursor
cursor = conn.cursor()
#Botão para enviar os dados''
if st.button('Registrar'):
    try:
        # Inserir os dados no PostgreSQL
        cursor.execute(
            "INSERT INTO sinasc_ro (idademae, sexo, peso, idadepai, nome) VALUES (%s, %s, %s, %s, %s)",
            (idademae, sexo, peso, idadepai, nome)
        )
        # Commit da transação
        conn.commit()
        #Mensagem de confirmação
        st.success('Informações registradas no banco dados!')

    except psycopg2.Error as e:
        st.error(f"Erro ao inserir dados: {e}")

#Vamos criar um botão para pesquisar as informações inseridas na etapa anterior, vou criar somente para buscar o parâmetro = nome, pois é mais simples :)
#Título da aplicação
st.subheader('Para pesquisar registro de um RN no banco de dados, preencha o campo abaixo: ')
#Onde vamos informar o campo para pesquisa
termo_pesquisa = st.text_input('Digite o nome completo do recém-nascido (case-sensitive):')

if st.button('Pesquisar'):
    try:
        cursor.execute(
            "SELECT * FROM sinasc_ro WHERE nome = %s",
            (termo_pesquisa,)
        )
        #Buscando resultados
        resultados = cursor.fetchall()
        #Colocando as colunas da tabela de exibição
        colunas = [desc[0] for desc in cursor.description]

        #Exibindo resultados
        if len(resultados) > 0:
            #st.subheader('Resultados da Pesquisa:')
            st.table([colunas] + resultados)
        else:
            st.warning('Nenhuma informação encontrada!')

    except psycopg2.Error as e:
        st.error(f"Erro ao executar a pesquisa: {e}")

#Criando um botão para deletar registros de RN's do banco de dados
# Título da aplicação
st.subheader('Para deletar registro de RN no banco de dados, preencha o campo abaixo:')
#Onde vamos captar o parametro para deletar no banco
termo_delete = st.text_input('Digite o nome completo do recém-nascido, que o registro será deletado! (case-sensitive):')

if st.button('Deletar'):
    try:
        cursor.execute(
            "DELETE FROM sinasc_ro WHERE nome = %s",
            (termo_delete,)
        )
        #Commit da transação
        conn.commit()
        #Mensagem de confirmação
        st.success('Registro deletado do banco de dados, para validar, basta realizar a pesquisa na etapa de busca!')

    except psycopg2.Error as e:
        st.error(f"Erro ao inserir dados: {e}")

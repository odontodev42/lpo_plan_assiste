import pandas as pd
import streamlit as st

st.set_page_config(layout='wide')

st.title('Lista de Procedimentos Odontológicos :file_cabinet:')


try:
        df_tabela = pd.read_csv('tabela_2025_com_valor.csv')
        df_tabela = df_tabela.reset_index()
        df_tabela['CÓDIGO'] = df_tabela['CÓDIGO'].astype(str)
        df_tabela['CÓDIGO'] = df_tabela['CÓDIGO'].str.zfill(8)
        df_tabela['VALOR'] = df_tabela['VALOR'].apply(lambda x: str(x).replace(".", ","))
        df_tabela = df_tabela.drop(columns=['index'])


        # dados da tabela antiga
        dados_ant = pd.read_csv("completo_antigo.csv")
        dados_ant = dados_ant.reset_index()
        # dados_ant = dados_ant.drop(columns=['PROCEDIMENTO'])
        dados_ant['Código'] = dados_ant['Código'].astype(str)
        dados_ant['Código'] = dados_ant['Código'].str.zfill(8)
        dados_ant = dados_ant.rename(columns={"Código": "CÓDIGO"})
        dados_ant['VALOR_ANTERIOR'] = dados_ant['CHO_ANTIGO'].apply(lambda x: round(x * 0.48, 2))
        dados_ant = dados_ant.drop(columns=['index'])
        dados_ant.drop_duplicates(inplace=True)


        # Filtro
        especialidades = df_tabela['ESPECIALIDADE'].unique()

        filtro_especialidade = st.sidebar.multiselect('Selecione a especialidade', especialidades)
        if filtro_especialidade:
            df_tabela = df_tabela[df_tabela['ESPECIALIDADE'].isin(filtro_especialidade)]
            dados_ant = dados_ant[dados_ant['ESPECIALIDADE'].isin(filtro_especialidade)]

        codigos = df_tabela['CÓDIGO'].unique()
        # codigos = df_tabela['CÓDIGO'].unique()



        filtro_codigo = st.sidebar.multiselect('Selecione os códigos', codigos)
        if filtro_codigo:
            df_tabela = df_tabela[df_tabela['CÓDIGO'].isin(filtro_codigo)]
            dados_ant = dados_ant[dados_ant['CÓDIGO'].isin(filtro_codigo)]
  

        st.title("PLAN-ASSISTE 2025")
        st.dataframe(df_tabela)

        st.title("PLAN-ASSISTE 2016")
        st.dataframe(dados_ant)

        merged_data = pd.merge(df_tabela, dados_ant, left_on=['CÓDIGO','ESPECIALIDADE'], right_on=['CÓDIGO','ESPECIALIDADE'], how='outer')
        merged_data['DIFERENCA_CHO'] = merged_data['CHO'] - merged_data['CHO_ANTIGO']
        merged_data['DIFERENCA_VALOR'] = merged_data['DIFERENCA_CHO'].apply(lambda x: round(x * 0.48, 2))
        

        st.title("PLAN-ASSISTE 2025 e 2016")
        st.dataframe(merged_data)

        filtered_data = merged_data[merged_data['DIFERENCA_CHO'] > 0]
        filtered_data_novo = merged_data[(merged_data['ESPECIALIDADE'].notna()) & (merged_data['CHO_ANTIGO'].isna())]
        
        st.title("PLAN-ASSISTE o que teve aumento de 2016 para 2025")
        filtered_data = filtered_data.drop(columns=['level_0'])
        st.dataframe(filtered_data)
        

        filtered_data_novo = filtered_data_novo.drop(columns=['level_0', 'PROCEDIMENTO_2016', 'CHO_ANTIGO', 'VALOR_ANTERIOR', 'DIFERENCA_CHO', 'DIFERENCA_VALOR'])

        st.title("PLAN-ASSISTE o que entou em 2025")
        st.dataframe(filtered_data_novo)


except Exception as e:
    print(f"Erro: {e}")

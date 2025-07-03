# ETL Series Code - Modelos BYD

## Bibliotecas Utilizadas

![Libs utilizadas](/pic/libs.png "Libs utilizadas")

## Preparação
 - Extraia a informação dos modelos do DMS, seguindo o layout do arquivo [Fake Model CSV](data/fake_model.csv) 
   - Para o NBS utilizei a consulta abaixo:
      ```sql
      WITH byd_models as (
          SELECT pm.cod_produto, 
                  pm.cod_modelo, 
                  pm.descricao_modelo, 
                  v.chassi_completo,
                  ROW_NUMBER() OVER (PARTITION BY pm.cod_modelo ORDER BY v.chassi_completo) as rn
            FROM produtos_modelos pm 
                  INNER JOIN produtos p ON (pm.cod_produto = p.cod_produto)
                  INNER JOIN veiculos v ON (v.cod_produto = pm.cod_produto and v.cod_modelo = pm.cod_modelo)
            WHERE p.descricao_produto LIKE 'BYD%'
            )

      SELECT COD_PRODUTO, COD_MODELO, DESCRICAO_MODELO, CHASSI_COMPLETO 
        FROM byd_models m
        WHERE m.rn = 1
        ORDER BY 3
      ```
   - Salve o arquivo com o nome ``models.csv`` na pasta [data](data/).

## Execução
 - Altere o arquivo .env_sample [.env_sample](.env_sample), informe suas credenciais e renomeie o arquivo para ``.env``

 Execute o comando abaixo
   ```bash
   poetry run python src/byd_series_code.py
   ```
 - Ao finalizar a execução será impresso no terminal o DataFrame gerado, junto com o arquivo ``seriesCode_BYD.csv``

## Retorno Terminal

![Retorno do Terminal após execução](/pic/dataframe_print.png "Retorno do Terminal após execução")

## Possíveis problemas

Para alguns chassis a api não retorna a informação, deixando a coluna SERIES_CODE vazia, a solução é buscar por outro chassi do modelo que faltar.

Nas próximas mudanças, podemos ligar diretamente no banco de dados e tratar a questão dos dados que retornam nulos ;)

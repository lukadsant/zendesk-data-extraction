from requester import *
print(f'-Leitura conluida, iniciando a Atualização de dados do modulo {modulo}...')

def bulkinsert(dados,modulo):
    cnxn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = cnxn.cursor()

    if modulo=='groups':
        # Convert list of dictionaries to list of tuples
        group_tuples = [(group['id'], group['name'], group['description']) for group in dados]

        sql = "INSERT INTO zengroups (Id, Name, Description) VALUES (?, ?, ?)"

        cursor.execute("TRUNCATE TABLE zengroups")
        cursor.executemany(sql, group_tuples)
        cnxn.commit()
        cnxn.close()

        # Count the number of inserted records and print a message
        num_records = len(group_tuples)
        print(f"Atualização de dados completa!, {num_records} grupos foram inseridos no banco.")

    elif modulo == 'tickets':
        #"listaDeTipos" com os IDs a serem filtrados
        listaDeTipos=[1500002350461,1900002214785,1900002214805,1500002350501,1500002391482,1500002391542]

        tickets_tuples = []

        for ticket in dados:
            # Filtra a lista custom_fields com base nos IDs em listaDeTipos
            filtered_custom_fields = [field for field in ticket['custom_fields'] if field['id'] in listaDeTipos and field['value'] is not None]
            
            # Verifica se a lista filtrada não está vazia
            if filtered_custom_fields:
                # Adiciona os dados do ticket à lista de tuplas
                tickets_tuples.append(
                    (
                        ticket['id'], ticket['status'], ticket['subject'], ticket['group_id'],
                        ticket['requester_id'], ticket['submitter_id'], ticket['created_at'],
                        ticket['updated_at'], ticket['assignee_id'],
                        ticket['satisfaction_rating']['score'],
                        filtered_custom_fields[0]['value'] # Adiciona a lista filtrada de custom_fields
                    )
                )

        sqlTicket = "INSERT INTO zentickets (Id_Ticket, Status,Assunto,Id_Grupo, Solicitante,Id_Usuario,Criado_Em,Finalizado_Em,Finalizador,Satisfacao, Tipo_Solitacao) VALUES (?, ?, ?, ?, ?, ?,?,?,?,?,?)"
        cursor.execute("TRUNCATE TABLE zentickets")
        cursor.executemany(sqlTicket, tickets_tuples)
        cnxn.commit()
        cnxn.close()

        # Count the number of inserted records and print a message
        num_records = len(tickets_tuples)
        print(f"Atualização de dados completa!, {num_records} tickets foram inseridos no banco.")

    elif modulo == 'users':
        # Convert list of dictionaries to list of tuples
        user_tuples = [(user['id'], user['name'], user['email'], user['default_group_id']) for user in dados]

        sqlInsertUser = "INSERT INTO zenusers (Id, Name, Email, Grupo) VALUES (?, ?, ?, ?)"
        cursor.execute("TRUNCATE TABLE zenusers")
        cursor.executemany(sqlInsertUser, user_tuples)
        cnxn.commit()
        cnxn.close()

        num_records = len(user_tuples)
        print(f"Atualização de dados completa!, {num_records} usuários foram inseridos no banco.")
    else:
        print('por algum motivo você conseguiu usar um modulo que não existe :O')




bulkinsert(listaComDados,modulo)



from main import *
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
        # Convert list of dictionaries to list of tuples
        tickets_tuples = [(
                          ticket['id'], ticket['status'], ticket['subject'], ticket['group_id'], ticket['requester_id'],
                          ticket['submitter_id'], ticket['created_at'], ticket['updated_at'], ticket['assignee_id']) for
                          ticket in dados]

        sqlTicket = "INSERT INTO zentickets (Id, Status,Assunto,Grupo, Solicitante,Atribuido,Criado_Em,Finalizado_Em,finalizado) VALUES (?, ?, ?, ?, ?, ?,?,?,?)"
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



import pandas as pd
from matplotlib import pyplot as plt
import numpy
import seaborn as sns 
import string

df = pd.read_csv("data/respostas_formulario.csv")

columns_tags_index: dict = {
    'date': 0, 
    'consent_policy': 1, 
    'micro_schedule': 2, 
    'professor_info': 3, 
    'classes_info': 4,
    'feedback_question': 5,
    'website_proposal': 6,
    'useful_features': 7
}

# Read headers (colummns)
columns: list = df.columns

# Read each Column
#print(df[columns[0]])

def count_occurrences(arr: list, x: any) -> int:
    count: int = 0
    for item in arr:
        if (item == x):
            count = count + 1
    return count

def get_date_info():
    date_col: int = 0
    dmy = []
    days_count = []
    #print(df[columns[date_col]])
    for d in df[columns[date_col]]:
        dmy.append(d.split(' '))
    
    for day in dmy:
        day = day[0][:2]
        days_count.append(day)
    
    print(days_count)
    # count occurrences in list
    day14 = count_occurrences(days_count, '14')
    day18 = count_occurrences(days_count, '18')
    day19 = count_occurrences(days_count, '19')
    day24 = count_occurrences(days_count, '24') 

def get_info_from_column(column_index: int) -> list:
    new_list: list = []
    info = df[columns[column_index]]
    for i in info:
        # micro schedule
        if column_index == columns_tags_index['micro_schedule']:
            if 'Mais informações sobre o' in i:
                i = i.replace('Mais informações sobre o', '')
                
            if 'Mais informações sobre a' in i:
                i = i.replace('Mais informações sobre a', '')
            
            if i.endswith('disciplina'):
                i = i.replace('Mais informações sobre a', '')

        elif column_index == columns_tags_index['professor_info']:
            if 'Como o professor faz a avaliação (provas/testes/trabalhos/etc)' in i:
                i = i.replace('Como o professor faz a avaliação (provas/testes/trabalhos/etc)', 'professor_avaliação_provas_testes')
                
            if 'Qual o índice de aprovação/reprovação do professor' in i:
                i = i.replace('Qual o índice de aprovação/reprovação do professor', 'indice_aprovação_reprovação_professor')
                
            if 'Quantas vezes o professor lecionou a disciplina que te interessa' in i:
                i = i.replace('Quantas vezes o professor lecionou a disciplina que te interessa', 'qts_vezes_lecionou_disciplina_interessa')
            
            if 'Qual a média de desempenho dos alunos com esse professor' in i:
                i = i.replace('Qual a média de desempenho dos alunos com esse professor', 'media_alunos_desempenho_professor')
                
            if 'Se o professor costuma cobrar presença' in i:
                i = i.replace('Se o professor costuma cobrar presença', 'cobrar_presenca')
                
            if 'Quais disciplinas o professor leciona ou já lecionou' in i:
                i = i.replace('Quais disciplinas o professor leciona ou já lecionou', 'disciplinas_leciona_lecionou')
            
        elif column_index == columns_tags_index['classes_info']:
            if 'Quais professores lecionam ou já lecionaram ela' in i:
                i = i.replace('Quais professores lecionam ou já lecionaram ela', 'professor_leciona_lecionaram')
                
            if 'Qual o índice de aprovação/reprovação da disciplina' in i:
                i = i.replace('Qual o índice de aprovação/reprovação da disciplina', 'indice_aprovacao_reprovacao_disciplina')
                
            if 'Qual a média de desempenho dos alunos da disciplina' in i:
                i = i.replace('Qual a média de desempenho dos alunos da disciplina', 'media_desempenho_disciplina')
        
        # not necessary to put feedback_question
        
        elif column_index == columns_tags_index['useful_features']:
            # ignore trash
            if 'Busca por disciplina' in i:
                i = i.replace('Busca por disciplina', 'busca_disciplina')
                
            if 'Busca por professor' in i:
                i = i.replace('Busca por professor', 'busca_professor')
                
            if 'Filtros por curso' in i:
                i = i.replace('Filtros por curso', 'filtros_curso')
            
            if 'Estatísticas de aprovação/reprovação' in i:
                i = i.replace('Estatísticas de aprovação/reprovação', 'estatisticas_aprov_reprov')
                
            if 'Comentários de outros alunos' in i:
                i = i.replace('Comentários de outros alunos', 'comentarios_alunos')
            
        i = i.translate({ord(c): None for c in string.whitespace})
        new_list.append(i.split(','))
        
        for i in new_list:
            if 'semestre' in i or 'etc.' in i:
                new_list.remove(i)
                
    return new_list
    
    
def get_column_answer_count(col_tag: int) -> dict:
    option1_count = 0; option2_count = 0; option3_count = 0
    option4_count = 0; option5_count = 0; option6_count = 0
    if col_tag == 2:
        dataset_tag_answers = get_info_from_column(columns_tags_index['micro_schedule'])
        for answer in dataset_tag_answers:
            # print(answer, "options_count: ", len(answer))
            for suboptions in answer:
                if 'professor' in suboptions:
                    option1_count = option1_count + 1
                    
                if 'critériodeavaliação' in suboptions:
                    option2_count = option2_count + 1
                    
                if 'disciplina' in suboptions:
                    option3_count = option3_count + 1
            
        return {"professor_count": option1_count, 
                "discipline_count": option2_count, 
                "evaluation_count": option3_count}
    elif col_tag == 3:
        data = get_info_from_column(columns_tags_index['professor_info'])
        for answer in data:
            for suboptions in answer:
                if 'disciplinas_leciona_lecionou' in suboptions:
                    option1_count = option1_count + 1
                    
                if 'qts_vezes_lecionou_disciplina_interessa' in suboptions:
                    option2_count = option2_count + 1
                    
                if 'indice_aprovação_reprovação_professor' in suboptions:
                    option3_count = option3_count + 1
                    
                if 'media_alunos_desempenho_professor' in suboptions:
                    option4_count = option4_count + 1
                    
                if 'cobrar_presenca' in suboptions:
                    option5_count = option5_count + 1
                    
                if 'professor_avaliação_provas_testes' in suboptions:
                    option6_count = option6_count + 1
                        
        return {"disciplinas_leciona_lecionou": option1_count, 
                "qts_vezes_lecionou_disciplina_interessa": option2_count, 
                "indice_aprovação_reprovação_professor": option3_count,
                "media_alunos_desempenho_professor": option4_count,
                "cobrar_presenca": option5_count,
                "professor_avaliação_provas_testes": option6_count}
        
    elif col_tag == 4:
        dataset_tag_answers = get_info_from_column(columns_tags_index['classes_info'])
        for answer in dataset_tag_answers:
            for suboptions in answer:
                if 'professor_leciona_lecionaram' in suboptions:
                    option1_count = option1_count + 1
                    
                if 'indice_aprovacao_reprovacao_disciplina' in suboptions:
                    option2_count = option2_count + 1
                    
                if 'media_desempenho_disciplina' in suboptions:
                    option3_count = option3_count + 1
            
        return {"professor_leciona_lecionaram": option1_count, 
                "indice_aprovacao_reprovacao_disciplina": option2_count, 
                "media_desempenho_disciplina": option3_count}
    
    elif col_tag == 5:
        dataset_tag_answers = get_info_from_column(columns_tags_index['feedback_question'])
        for answer in dataset_tag_answers:
            for suboptions in answer:
                if 'Osprofessoresqueteve' in suboptions:
                    option1_count = option1_count + 1
                    
                elif 'Nenhum' in suboptions:
                    option2_count = option2_count + 1
                    
                elif 'Ambos' in suboptions:
                    option3_count = option3_count + 1
                
                elif 'Asdisciplinasquecursou' in suboptions:
                    option4_count = option4_count + 1
            
        return {"Osprofessoresqueteve": option1_count, 
                "Nenhum": option2_count, 
                "Ambos": option3_count, 
                "Asdisciplinasquecursou": option4_count}
        
    elif col_tag == 6:
        dataset_tag_answers = get_info_from_column(columns_tags_index['website_proposal'])
        for answer in dataset_tag_answers:
            for suboptions in answer:
                if 'Sim' in suboptions:
                    option1_count = option1_count + 1
                    
                elif 'Não' in suboptions:
                    option2_count = option2_count + 1
            
        return {"Sim": option1_count, 
                "Não": option2_count}
        
    elif col_tag == 7:
        dataset_tag_answers = get_info_from_column(columns_tags_index['useful_features'])
        for answer in dataset_tag_answers:
            for suboptions in answer:
                if 'busca_disciplina' in suboptions:
                    option1_count = option1_count + 1
                    
                elif 'busca_professor' in suboptions:
                    option2_count = option2_count + 1
                
                elif 'estatisticas_aprov_reprov' in suboptions:
                    option3_count = option3_count + 1
                
                elif 'comentarios_alunos' in suboptions:
                    option4_count = option4_count + 1
            
        return {"busca_disciplina": option1_count, 
                "busca_professor": option2_count,
                "estatisticas_aprov_reprov": option3_count, 
                "comentarios_alunos": option4_count}
    else:
        print("Erro: index not found")
        return { }
        
#dataset_info_date()
def print_info_count():
    for value in columns_tags_index.values():
        if value != 0 or value != 1:
            for k, v in get_column_answer_count(value).items():
                print(f"{k}: {v}")
            print("------------------------")

print_info_count()
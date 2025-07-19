try:
  resposta_git = requests.get(URL, headers=headers)
  resposta_git.raise_for_status()
except requests.exceptions.HTTPError as err:
  print(err)
  soup = None
else:
  soup = BeautifulSoup(resposta_git.text, 'html.parser')

projeto = soup.find_all('article',class_="Box-row")
top_projetos = []
for projeto in projeto:

# Nome do autor / nome do projeto
  projeto_nome = projeto.find('h2', class_='h3 lh-condensed')
  nome = projeto_nome.get_text().replace('\n', '').replace(' ', '').strip().split('/')
  top_projetos.append(nome[0])
  top_projetos.append(nome[1])

  # Linguagem
  lingua = projeto.find('span', itemprop='programmingLanguage')
  try:
    top_projetos.append(lingua.get_text())
  except AttributeError:
    top_projetos.append(None)

  # Stars Total
  stars_total = projeto.find('a' ,{'href': lambda x: x and 'stargazers' in x})
  top_projetos.append(stars_total.get_text().strip())

  # Forks
  forks = projeto.find('a', {'href': lambda x: x and 'forks' in x})
  top_projetos.append(forks.get_text().strip())

  # Stars Today
  stars_today = projeto.find('span', class_='d-inline-block float-sm-right')
  stars_today = stars_today.get_text().strip().split(' ')
  top_projetos.append(stars_today[0])

  # Today's date
  today = pd.Timestamp.now().date()
  top_projetos.append(today)

  # Salvando a lista top_projetos em um DataFrame e limpando ela
  df_data.loc[len(df_data)] = top_projetos
  top_projetos = []

# Salvando o DataFrame um um arquivo CSV
df_data.to_csv(TRENDING, sep=',',mode='a', index=False, header=False)
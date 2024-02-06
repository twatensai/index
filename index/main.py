import json
from collections import Counter, defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk

# Décommenter les lignes suivantes si ces packages ne sont pas installés
# nltk.download('stopwords')
# nltk.download('punkt')

def tokenize(text):
    stop_words_french = set(stopwords.words('french'))
    tokens = [word.lower() for word in word_tokenize(text) if word.isalnum() and word.lower() not in stop_words_french]
    return tokens

# Initialiser le stemmer
stemmer = SnowballStemmer('french')

# Fonction de tokenization avec stemming
def tokenize_with_stemming(text):
    stop_words_french = set(stopwords.words('french'))
    tokens = [stemmer.stem(word.lower()) for word in word_tokenize(text) if word.isalnum() and word.lower() not in stop_words_french]
    return tokens

def write_index_to_file(index, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(index, file, ensure_ascii=False, indent=2)

# Charger la liste d'URLs depuis le fichier JSON
with open('crawled_urls.json', 'r', encoding='utf-8') as file:
    url_list = json.load(file)

# Initialiser des variables pour les statistiques
num_documents = len(url_list)
num_tokens_global = 0
num_tokens_by_field = Counter()
avg_tokens_per_document = 0
avg_tokens_in_title_per_document = 0
avg_tokens_in_content_per_document = 0

# Initialiser l'index non positionnel et positionnel pour le champ 'title'
non_pos_index_title = defaultdict(list)
pos_index_title = defaultdict(lambda: defaultdict(list))

# Initialiser l'index non positionnel et positionnel pour le champ 'content'
non_pos_index_content = defaultdict(list)
pos_index_content = defaultdict(lambda: defaultdict(list))

# Initialiser l'index non positionnel et positionnel pour le champ 'title'
non_pos_index_title_stemmer = defaultdict(list)
pos_index_title_stemmer = defaultdict(lambda: defaultdict(list))

# Parcourir chaque URL
for url_data in url_list:
    title = url_data.get('title', '')
    content = url_data.get('content','')
    title_tokens = tokenize(title)
    content_tokens = tokenize(content)
    stemmer_title_tokens = tokenize_with_stemming(title)

    # Mise à jour des statistiques
    num_tokens_global += len(title_tokens) + len(content_tokens)
    num_tokens_by_field['title'] += len(title_tokens)
    num_tokens_by_field['content'] += len(content_tokens)
    avg_tokens_per_document += len(title_tokens) + len(content_tokens)
    avg_tokens_in_title_per_document += len(title_tokens)
    avg_tokens_in_content_per_document += len(content_tokens)

    # Construction de l'index non positionnel pour le champ 'title'
    for token in title_tokens:
        non_pos_index_title[token].append(url_data['url'])

    # Construction de l'index positionnel pour le champ 'title'
    for position, token in enumerate(title_tokens):
        pos_index_title[token]['urls'].append(url_data['url'])
        pos_index_title[token]['positions'].append(position)

    # Construction de l'index non positionnel pour le champ 'content'
    for token in content_tokens:
        non_pos_index_content[token].append(url_data['url'])

    # Construction de l'index positionnel pour le champ 'content'
    for position, token in enumerate(title_tokens):
        pos_index_content[token]['urls'].append(url_data['url'])
        pos_index_content[token]['positions'].append(position)

    # Construction de l'index non positionnel pour le champ 'title' avec le stemmer
    for token in stemmer_title_tokens:
        non_pos_index_title_stemmer[token].append(url_data['url'])

    # Construction de l'index positionnel pour le champ 'title' avec le stemmer
    for position, token in enumerate(stemmer_title_tokens):
        pos_index_title_stemmer[token]['urls'].append(url_data['url'])
        pos_index_title_stemmer[token]['positions'].append(position)

# Calcul des moyennes
avg_tokens_per_document /= num_documents
avg_tokens_in_title_per_document /= num_documents
avg_tokens_in_content_per_document /= num_documents

# Création du fichier de statistiques
metadata = {
    'num_documents': num_documents,
    'num_tokens_global': num_tokens_global,
    'num_tokens_by_field': dict(num_tokens_by_field),
    'avg_tokens_per_document': avg_tokens_per_document,
    'avg_tokens_in_title_per_document': avg_tokens_in_title_per_document,
    'avg_tokens_in_content_per_document': avg_tokens_in_content_per_document,
}

with open('metadata.json', 'w') as metadata_file:
    json.dump(metadata, metadata_file, indent=2)

# Création des fichiers de sortie pour le champ 'title'
write_index_to_file(non_pos_index_title, 'title.non_pos_index.json')

pos_index_title_dict = {token: {'urls': data['urls'], 'positions': data['positions']} for token, data in pos_index_title.items()}
write_index_to_file(pos_index_title_dict, 'title.pos_index.json')

# Création des fichiers de sortie pour le champ 'content'
write_index_to_file(non_pos_index_content, 'content.non_pos_index.json')

pos_index_content_dict = {token: {'urls': data['urls'], 'positions': data['positions']} for token, data in pos_index_content.items()}
write_index_to_file(pos_index_content_dict, 'content.pos_index.json')

# Création des fichiers de sortie pour le champ 'title' avec le stemmer
write_index_to_file(non_pos_index_title_stemmer, 'snowball_stemmer.title.non_pos_index.json')

pos_index_title_dict_stemmer = {token: {'urls': data['urls'], 'positions': data['positions']} for token, data in pos_index_title_stemmer.items()}
write_index_to_file(pos_index_title_dict_stemmer, 'snowball_stemmer.title.pos_index.json')

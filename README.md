Скрипт создания таблиц в базе и заливка информации из pkl
=========================================================

Сущности
--------

Имеются журналы и следующие данные о них в формате json:
1. Наименование супердомена (primary domain)
2. Наименование домена (domain)
3. Список поддоменов (subdomain) к которым журнал относится
4. Список статей журнала начиная с 2010 года со следующей информацией:
   * Дата публикации в виде месяц-год (годовые журналы приурочены к январю)
   * Название статьи
   * Индентификатор статьи (Doi)
   * Абстракт статьи
   * Ключевые слова статьи (могут быть null)
   * Биграмы
   * Триграмы

В базу данных не включаются абстракт и ключевые слова - не показательная информация


Схема базы данных
-----------------

### Данная система имеет следующие связи:

* Супердомены, домены и поддомены образуют дерево
* Журнал может относится к нескольким поддоменам, один поддомен содержит несколько журналов
* В одном журнале несколько статей, статья относится только к одному журналу
* В одной статье много словосочетаний, каждое словосочетание может встречаться в разных статьях
* Каждая статья имеет только одну дату выпуска (год и квартал)
* Каждое словосочетание принадлежит либо к типу биграм либо триграм

### Таблицы

#### Супердомены (primary_domains)
1. id smallserial primary key
2. name varchar

#### Домены (domains)
1. id smallserial primary key
2. name varchar
3. primary_id references primary_domains (id)

#### Поддомены (subdomains)
1. id smallserial primary_id primary key
2. name varchar
3. domain_id references domains (id)

#### Журналы (journals)
1. id serial primary key
2. name varchar

#### Таблица связи поддоменов и журналов (subdomains_journals)
1. subdomain_id smallint references subdomains (id)
2. journal_id integer references journals (id)
   primary key (subdomain_id, journal_id)

#### Статьи (articles)
1. id serial primary key
2. name varchar
3. doi varchar
4. pub_year_id smallint references years (id)
5. pub_qarter_id smallint references quarters (id)
6. journal_id integer references journals (id)

#### Года (years)
1. id smallserial primary key
2. year smallint

#### Кварталы
1. id smallserial primary key
2. name varchar(2)

#### Словосочетания (collocations)
1. id serial primary key
2. collocation varchar
3. col_type_id smallint references collocation_types (id)

#### Таблица связи статей и словосочетаний (articles_collocations)
1. article_id references articles (id)
2. collocation_id references collocations (id)
   primary key (article_id collocation_id)

#### Таблица типов словосочетаний
1. id smallserial primary key
2. type varchar

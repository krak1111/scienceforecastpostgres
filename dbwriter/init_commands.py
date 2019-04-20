creating_commands = (
    """
    CREATE TABLE primary_domains(
        id SMALLSERIAL PRIMARY KEY,
        name VARCHAR NOT NULL
    )
    """,
    """
    CREATE TABLE domains(
        id SMALLSERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        primary_id SMALLINT NOT NULL
    )
    """,
    """
    CREATE TABLE subdomains(
        id SMALLSERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        domain_id SMALLINT NOT NULL
    )
    """,
    """
    CREATE TABLE journals(
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL
    )
    """,
    """
    CREATE TABLE subdomains_journals(
        subdomain_id SMALLINT NOT NULL,
        journal_id INTEGER NOT NULL,
        PRIMARY KEY (subdomain_id, journal_id)
    )
    """,
    """
    CREATE TABLE articles(
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        doi VARCHAR NOT NULL,
        pub_year_id SMALLINT NOT NULL,
        pub_quarter_id SMALLINT NOT NULL,
        journal_id INT NOT NULL
    )
    """,
    """
    CREATE TABLE years(
        id SMALLSERIAL PRIMARY KEY,
        year SMALLINT NOT NULL
    )
    """,
    """
    CREATE TABLE quarters(
        id SMALLSERIAL PRIMARY KEY,
        name VARCHAR(2)
    )
    """,
    """
    CREATE TABLE articles_collocations(
        article_id SERIAL NOT NULL,
        collocation_id INTEGER NOT NULL,
        PRIMARY KEY (article_id, collocation_id)
    )
    """,
    """
    CREATE TABLE collocations(
        id SERIAL PRIMARY KEY,
        collocation VARCHAR NOT NULL,
        col_type_id SMALLINT NOT NULL
    )
    """,
    """
    CREATE TABLE collocation_types(
        id SMALLSERIAL PRIMARY KEY,
        type VARCHAR
    )
    """,)


references = (
    """
    ALTER TABLE domains ADD CONSTRAINT primaryfk FOREIGN KEY (primary_id) REFERENCES primary_domains (id) ON DELETE CASCADE
    """,
    """
    ALTER TABLE subdomains ADD CONSTRAINT domainfk FOREIGN KEY (domain_id) REFERENCES domains (id) ON DELETE CASCADE
    """,
    """
    ALTER TABLE subdomains_journals ADD CONSTRAINT subdomainfk FOREIGN KEY (subdomain_id) REFERENCES subdomains (id) ON DELETE CASCADE
    """,
     """
    ALTER TABLE subdomains_journals ADD CONSTRAINT journalnfk FOREIGN KEY (journal_id) REFERENCES journals (id) ON DELETE CASCADE
    """,
    """
    ALTER TABLE articles ADD CONSTRAINT journalfk FOREIGN KEY (journal_id) REFERENCES journals (id) ON DELETE CASCADE
    """,
    """
    ALTER TABLE articles ADD CONSTRAINT yearfk FOREIGN KEY (pub_year_id) REFERENCES years (id) ON DELETE CASCADE
    """,
    """
    ALTER TABLE articles ADD CONSTRAINT quarterfk FOREIGN KEY (pub_quarter_id) REFERENCES quarters (id) ON DELETE CASCADE
    """,
    """
    ALTER TABLE articles_collocations ADD CONSTRAINT articlefk FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE
    """,
    """
    ALTER TABLE articles_collocations ADD CONSTRAINT collocationfk FOREIGN KEY (collocation_id) REFERENCES collocations (id) ON DELETE CASCADE
    """,
    """
    ALTER TABLE collocations ADD CONSTRAINT collocationtypefk FOREIGN KEY (col_type_id) REFERENCES collocation_types (id) ON DELETE CASCADE
    """,)

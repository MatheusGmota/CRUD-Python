DROP TABLE emissoes_carbono CASCADE CONSTRAINTS;

DROP TABLE projetos_sustentaveis CASCADE CONSTRAINTS;

DROP TABLE regioes_sustentaveis CASCADE CONSTRAINTS;

DROP TABLE tipo_fontes CASCADE CONSTRAINTS;

DROP SEQUENCE emissoes_carbono_id_emissao;

DROP SEQUENCE projetos_sustentaveis_id_proje;

DROP SEQUENCE regioes_sustentaveis_id_regiao;

DROP SEQUENCE tipo_fontes_id_tipo_fonte_seq;

CREATE TABLE emissoes_carbono (
    id_emissao    NUMBER NOT NULL,
    id_tipo_fonte NUMBER,
    emissao       NUMBER(12, 2)
);

ALTER TABLE emissoes_carbono ADD CONSTRAINT emissoes_carbono_pk PRIMARY KEY ( id_emissao );

CREATE TABLE projetos_sustentaveis (
    id_projeto    NUMBER NOT NULL,
    descricao     VARCHAR2(255 BYTE),
    custo         NUMBER(*, 0),
    status        VARCHAR2(50 BYTE),
    id_regiao     NUMBER,
    id_tipo_fonte NUMBER
);

ALTER TABLE projetos_sustentaveis ADD CONSTRAINT projetos_sustentaveis_pk PRIMARY KEY ( id_projeto );

CREATE TABLE regioes_sustentaveis (
    id_regiao NUMBER NOT NULL,
    nome      VARCHAR2(50 BYTE)
);

ALTER TABLE regioes_sustentaveis ADD CONSTRAINT regioes_sustentaveis_pk PRIMARY KEY ( id_regiao );

CREATE TABLE tipo_fontes (
    id_tipo_fonte NUMBER NOT NULL,
    nome          VARCHAR2(50 BYTE)
);

ALTER TABLE tipo_fontes ADD CONSTRAINT tipo_fontes_pk PRIMARY KEY ( id_tipo_fonte );

ALTER TABLE projetos_sustentaveis
    ADD CONSTRAINT regioes_sustentaveis_fk FOREIGN KEY ( id_regiao )
        REFERENCES regioes_sustentaveis ( id_regiao );

ALTER TABLE projetos_sustentaveis
    ADD CONSTRAINT tipo_fontes_fk FOREIGN KEY ( id_tipo_fonte )
        REFERENCES tipo_fontes ( id_tipo_fonte );

ALTER TABLE emissoes_carbono
    ADD CONSTRAINT tipo_fontes_fkv2 FOREIGN KEY ( id_tipo_fonte )
        REFERENCES tipo_fontes ( id_tipo_fonte );

CREATE SEQUENCE emissoes_carbono_id_emissao START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER emissoes_carbono_id_emissao BEFORE
    INSERT ON emissoes_carbono
    FOR EACH ROW
    WHEN ( new.id_emissao IS NULL )
BEGIN
    :new.id_emissao := emissoes_carbono_id_emissao.nextval;
END;
/

CREATE SEQUENCE projetos_sustentaveis_id_proje START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER projetos_sustentaveis_id_proje BEFORE
    INSERT ON projetos_sustentaveis
    FOR EACH ROW
    WHEN ( new.id_projeto IS NULL )
BEGIN
    :new.id_projeto := projetos_sustentaveis_id_proje.nextval;
END;
/

CREATE SEQUENCE regioes_sustentaveis_id_regiao START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER regioes_sustentaveis_id_regiao BEFORE
    INSERT ON regioes_sustentaveis
    FOR EACH ROW
    WHEN ( new.id_regiao IS NULL )
BEGIN
    :new.id_regiao := regioes_sustentaveis_id_regiao.nextval;
END;
/

CREATE SEQUENCE tipo_fontes_id_tipo_fonte_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER tipo_fontes_id_tipo_fonte_trg BEFORE
    INSERT ON tipo_fontes
    FOR EACH ROW
    WHEN ( new.id_tipo_fonte IS NULL )
BEGIN
    :new.id_tipo_fonte := tipo_fontes_id_tipo_fonte_seq.nextval;
END;
/
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
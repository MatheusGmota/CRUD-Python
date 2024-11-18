CREATE SEQUENCE tb_eficiencia_setor_id_eficien START WITH 1 NOCACHE ORDER
CREATE OR REPLACE TRIGGER tb_eficiencia_setor_id_eficien BEFORE
    INSERT ON tb_eficiencia_setor
    FOR EACH ROW
    WHEN ( new.id_eficiencia IS NULL )
BEGIN
    :new.id_eficiencia := tb_eficiencia_setor_id_eficien.nextval;
END
CREATE SEQUENCE tb_empresas_id_empresa_seq START WITH 1 NOCACHE ORDER
CREATE OR REPLACE TRIGGER tb_empresas_id_empresa_trg BEFORE
    INSERT ON tb_empresas
    FOR EACH ROW
    WHEN ( new.id_empresa IS NULL )
BEGIN
    :new.id_empresa := tb_empresas_id_empresa_seq.nextval;
END
CREATE SEQUENCE tb_tipo_empresa_id_tipo_seq START WITH 1 NOCACHE ORDER
CREATE OR REPLACE TRIGGER tb_tipo_empresa_id_tipo_trg BEFORE
    INSERT ON tb_tipo_empresa
    FOR EACH ROW
    WHEN ( new.id_tipo IS NULL )
BEGIN
    :new.id_tipo := tb_tipo_empresa_id_tipo_seq.nextval;
END
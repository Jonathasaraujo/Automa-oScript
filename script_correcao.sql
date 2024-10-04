-- Declarar a data atual
DECLARE @data_atual DATE = GETDATE();

-- Inserir o registro faltante para cada idt_oper que tinha saldo ontem e está faltando o tipo_sald = 'JURPREX' hoje
INSERT INTO tbsgc056_sald_oper (idt_oper, dat_sald, indicador_ativ, tipo_sald, vlr_sald)
SELECT 
    a.idt_oper, 
    @data_atual AS dat_sald, 
    a.indicador_ativ, 
    'JURPREX' AS tipo_sald, 
    a.vlr_sald
FROM 
    tbsgc056_sald_oper a
LEFT JOIN 
    tbsgc056_sald_oper b
    ON a.idt_oper = b.idt_oper
    AND b.tipo_sald = 'JURPREX'
    AND b.dat_sald = @data_atual
WHERE 
    a.dat_sald = DATEADD(DAY, -1, @data_atual)   -- Considera apenas os registros do dia anterior
    AND a.tipo_sald = 'JURPREX'                  -- Considera apenas o saldo do tipo 'JURPREX' do dia anterior
    AND b.idt_oper IS NULL;                      -- Garante que ainda não existe o registro de hoje

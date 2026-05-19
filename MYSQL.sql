use calculadora;

CREATE TABLE IF NOT EXISTS historico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    N1 FLOAT NOT NULL,
    Operacao VARCHAR(20) NOT NULL,
    N2 FLOAT NOT NULL,
    Resultado VARCHAR(50) NOT NULL,
    data_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from historico
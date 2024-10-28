INSERT INTO constructal_automate_verification_cases.csg_stiffenedplate
(id, phi, N_ls, N_ts, k, t_1, h_s, t_s, description, plate_id)
VALUES
(5, 0.1000, 2, 2, 6.600, 18.0, 66.0, 10.0, 'Placa P(2,2). LIMA (2016)', 1),
(6, 0.1000, 2, 2, 2.933, 18.0, 44.0, 15.0, 'Placa P(2,2). LIMA (2016)', 1),
(7, 0.1000, 2, 2, 1.650, 18.0, 33.0, 20.0, 'Placa P(2,2). LIMA (2016)', 1),
(8, 0.1000, 2, 2, 1.080, 18.0, 27.0, 25.0, 'Placa P(2,2). LIMA (2016)', 1),
(9, 0.1000, 2, 2, 0.733, 18.0, 22.0, 30.0, 'Placa P(2,2). LIMA (2016))', 1),
(10, 0.1000, 2, 2, 0.543, 18.0, 19.0, 35.0, 'Placa P(2,2). LIMA (2016)', 1),
(11, 0.1000, 2, 2, 0.400, 18.0, 16.0, 40.0, 'Placa P(2,2). LIMA (2016)', 1),
(12, 0.1000, 2, 2, 0.311, 18.0, 14.0, 45.0, 'Placa P(2,2). LIMA (2016)', 1);

INSERT INTO constructal_automate_mcsul_2024_results.csg_stiffenedplate
(id, phi, N_ls, N_ts, k, t_1, h_s, t_s, description, plate_id)
VALUES(2, 0.30, 2, 2, 3.200, 14.00, 80.00, 25.00, 'Convergência de malha. Placa com enrijecedores. LIMA(2016)', 1);
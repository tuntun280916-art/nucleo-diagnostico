--
-- PostgreSQL database dump
--

-- Dumped from database version 17.11
-- Dumped by pg_dump version 17.11

-- Started on 2026-11-23 10:19:04

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 16395)
-- Name: empleado; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.empleado (
    id_empleado integer NOT NULL,
    nombre_comp character varying(50) NOT NULL,
    sexo character(1) NOT NULL,
    direccion character varying(150),
    telefono character varying(20),
    fecha_nac date NOT NULL,
    turno character varying(50),
    salario real,
    contrasena character varying(8)
);


ALTER TABLE public.empleado OWNER TO admin;

--
-- TOC entry 218 (class 1259 OID 16405)
-- Name: medico; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medico (
    id_medico integer NOT NULL,
    nombre_comp character varying(50) NOT NULL,
    direccion character varying(150),
    telefono character varying(20),
    fecha_nac date NOT NULL,
    sexo character(1) NOT NULL,
    especialidad character varying(150) NOT NULL,
    contrasena character varying(8)
);


ALTER TABLE public.medico OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16410)
-- Name: paciente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.paciente (
    id_paciente integer NOT NULL,
    nombre_comp character varying(50) NOT NULL,
    direccion character varying(150),
    telefono character varying(20),
    fecha_nac date NOT NULL,
    sexo character(1) NOT NULL,
    edad integer NOT NULL,
    estatura real
);


ALTER TABLE public.paciente OWNER TO postgres;

--
-- TOC entry 4900 (class 0 OID 16395)
-- Dependencies: 217
-- Data for Name: empleado; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.empleado (id_empleado, nombre_comp, sexo, direccion, telefono, fecha_nac, turno, salario, contrasena) FROM stdin;
2	JANET VALENCIA CARBAJAL	F	HIDALGO 986	3314129537	1987-10-31	VESPERTINO	14999.99	31101987
1	BEATRIZ MEDINA CHICUATE	F	COIMBRA 869	3313669040	1972-02-07	MATUTINO	14500.75	7021972
\.


--
-- TOC entry 4901 (class 0 OID 16405)
-- Dependencies: 218
-- Data for Name: medico; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medico (id_medico, nombre_comp, direccion, telefono, fecha_nac, sexo, especialidad, contrasena) FROM stdin;
1	PAOLA ELIZABETH DIAZ ACEVES	COLINA CENTRAL 200	3329853910	1985-01-29	F	GERIATRIA	7021972
2	CLAUDIA ELIZABETH GOMEZ LOPEZ	MARIANO OTERO 300	3301053911	1985-05-01	F	REUMATOLOGIA	1051985
3	JOSUE FRANCISCO RAMIREZ \nLUGO	TOLEDO 2588	3334903175	1984-03-02	M	GASTROENTEROLOGIA	2031984
4	CHRISTOPHER MENESES ARREOLA	CLUB ORO \n400	3314108419	1984-10-14	M	CARDIOLOGIA	14101984
\.


--
-- TOC entry 4902 (class 0 OID 16410)
-- Dependencies: 219
-- Data for Name: paciente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.paciente (id_paciente, nombre_comp, direccion, telefono, fecha_nac, sexo, edad, estatura) FROM stdin;
1	JOB GODOY GAMBOA	PALMA REAL 7691	3313480524	1967-08-14	M	59	1.77
2	FRANCISCO ELIAS REYNOSO \nPRESA	JUAN DEL CARMEN \n891	3311737312	1980-07-19	M	46	1.83
3	ALAN SANTIAGO CORTES\nGODINEZ	VOLCAN SAN FCO \n8891	3310615592	1988-11-23	M	38	1.83
4	DOLORES MEDINA \nCHICUATE	COIMBRA \n869	3313669039	1968-10-15	F	58	1.73
5	GUADALUPE LUGO \nROJAS	JUAREZ \n3691	3314517285	1936-10-27	F	90	1.55
6	LUZ ROBLES \nJIMENEZ	LITOGRAFIA \n5591	3334530438	1956-08-11	F	69	1.65
\.


--
-- TOC entry 4750 (class 2606 OID 16399)
-- Name: empleado empleado_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.empleado
    ADD CONSTRAINT empleado_pkey PRIMARY KEY (id_empleado);


--
-- TOC entry 4752 (class 2606 OID 16409)
-- Name: medico medico_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medico
    ADD CONSTRAINT medico_pkey PRIMARY KEY (id_medico);


--
-- TOC entry 4754 (class 2606 OID 16414)
-- Name: paciente paciente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paciente
    ADD CONSTRAINT paciente_pkey PRIMARY KEY (id_paciente);


-- Completed on 2026-11-23 10:19:05

--
-- PostgreSQL database dump complete
--



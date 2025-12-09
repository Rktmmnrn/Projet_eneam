--
-- PostgreSQL database dump
--

\restrict Xdw5Pcq79fOwGkM11EpMfshwVnBxI1DFyBGrAc2do9YLiARmne5e73kg5fYbVzP

-- Dumped from database version 15.15 (Debian 15.15-1.pgdg13+1)
-- Dumped by pg_dump version 15.15 (Debian 15.15-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- Name: base_cache_signaling_assets; Type: SEQUENCE; Schema: public; Owner: odoo
--

CREATE SEQUENCE public.base_cache_signaling_assets
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_cache_signaling_assets OWNER TO odoo;

--
-- Name: base_cache_signaling_default; Type: SEQUENCE; Schema: public; Owner: odoo
--

CREATE SEQUENCE public.base_cache_signaling_default
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_cache_signaling_default OWNER TO odoo;

--
-- Name: base_cache_signaling_routing; Type: SEQUENCE; Schema: public; Owner: odoo
--

CREATE SEQUENCE public.base_cache_signaling_routing
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_cache_signaling_routing OWNER TO odoo;

--
-- Name: base_cache_signaling_templates; Type: SEQUENCE; Schema: public; Owner: odoo
--

CREATE SEQUENCE public.base_cache_signaling_templates
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_cache_signaling_templates OWNER TO odoo;

--
-- Name: base_registry_signaling; Type: SEQUENCE; Schema: public; Owner: odoo
--

CREATE SEQUENCE public.base_registry_signaling
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_registry_signaling OWNER TO odoo;

--
-- Name: base_cache_signaling_assets; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.base_cache_signaling_assets', 33, true);


--
-- Name: base_cache_signaling_default; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.base_cache_signaling_default', 33, true);


--
-- Name: base_cache_signaling_routing; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.base_cache_signaling_routing', 33, true);


--
-- Name: base_cache_signaling_templates; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.base_cache_signaling_templates', 33, true);


--
-- Name: base_registry_signaling; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.base_registry_signaling', 33, true);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\unrestrict Xdw5Pcq79fOwGkM11EpMfshwVnBxI1DFyBGrAc2do9YLiARmne5e73kg5fYbVzP


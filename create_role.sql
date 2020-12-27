CREATE OR REPLACE FUNCTION public.create_role(IN role_name text)
    RETURNS void
    LANGUAGE 'plpgsql'
    VOLATILE
    PARALLEL UNSAFE
    COST 100
AS $BODY$
BEGIN
EXECUTE format('CREATE ROLE %s', role_name);
EXECUTE format('GRANT %s TO trifacta', role_name);
END;
$BODY$;

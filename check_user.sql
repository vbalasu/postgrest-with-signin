CREATE OR REPLACE FUNCTION public.check_user()
    RETURNS void
    LANGUAGE 'plpgsql'
    VOLATILE
    PARALLEL UNSAFE
    COST 100
AS $BODY$
BEGIN
  IF current_user = 'evil_user' THEN
    RAISE EXCEPTION 'No, you are evil'
      USING HINT = 'Stop being so evil and maybe you can log in';
  END IF;
END
$BODY$;

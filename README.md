# postgrest-with-signin

This is a running configuration that implements Google One Tap for sign in, and uses these credentials to access a Postgres database via a PostgREST api.

Included in this project are the following files:

1. `postgrest.conf` configuration file that sets up a postgrest server listening to the `main` database at https://postgres.amer.trifacta.net/api
2. `supervisord.conf` configuration file that starts up `postgrest` and the `db_access` service
3. `onetap.html` that allows a user to sign in using Google One Tap. See [this bitbucket project](https://bitbucket.org/vbalasu/onetap/src/master/) and [this page](https://postgres.amer.trifacta.net/onetap.html)
4. `db_access.py` that powers the `db_access` service running on the server. This performs a couple of useful functions:
   - [/swap](https://postgres.amer.trifacta.net/db_access/swap) provides a Postgrest JWT token in exchange for a Google id_token
   - [/create_role](https://postgres.amer.trifacta.net/db_access/create_role) sets up a new role in the database for the user (`sub`) in the Google id_token
5. SQL scripts for `check_user` and `create_role`

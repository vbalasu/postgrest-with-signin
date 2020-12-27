export DB_TOKEN=$(curl "http://127.0.0.1:5000/swap?token=$TOKEN")
curl "http://127.0.0.1:5000/create_role?token=$TOKEN"

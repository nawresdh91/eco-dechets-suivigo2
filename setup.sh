mkdir -p .streamlit
echo "\
[general]\n\
email = \"{scoty.loumbou@eco-dechets.fr}\"\n\
" > .streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > .streamlit/config.toml
test -f .streamlit/secrets.toml || touch .streamlit/secrets.toml
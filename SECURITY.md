# Segurança

## O que nunca vai para o repositório

Este repositório é público. Não versione:

- `.streamlit/secrets.toml` (já está no `.gitignore`; versione só `secrets.toml.example`);
- credenciais do Xano CLI (`~/.xano/credentials.yaml`) e tokens de API;
- senhas de usuários, inclusive de teste.

Credenciais da equipe ficam no gerenciador de senhas, não no Git.

## Como o app protege os dados

- Senhas são guardadas pelo Xano com hash (campo `password`); o app nunca as armazena.
- Toda rota de dados exige `Authorization: Bearer <token>` (JWT de 24 h) e filtra por `user_id`.

## Reportar um problema

Encontrou uma falha de segurança? Não abra uma issue pública: fale diretamente com o mantenedor (@simaquee no GitHub).

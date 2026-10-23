# Primeiros passos

## 1. Backend no Xano

1. Crie uma conta em <https://xano.com> (o plano gratuito serve) e um workspace.
2. Autentique o Xano CLI (requer Node.js):
   ```powershell
   npm install -g @xano/cli
   xano auth
   xano profile me
   ```
3. Confira as mudanças sem aplicar nada e só depois publique:
   ```powershell
   xano workspace push -d ./src/xano --dry-run
   xano workspace push -d ./src/xano
   ```
   Se o dry-run listar *Destructive Operations*, pare e revise antes de publicar.
4. No Xano, abra **API > OrbitFin** e copie a **Base URL**: `https://x8ki-letl-twmt.n7.xano.io/api:orbitfingm`.
   O grupo usa o canonical `orbitfingm` porque a instância gratuita é compartilhada e `api:orbitfin` já pertence ao projeto original.

> A tabela `user` é compartilhada com a API *authentication* do Quick Start do Xano no mesmo workspace. Mantenha em `src/xano/table/user.xs` os campos `role` e `password_reset`; sem eles o push os apaga.

## 2. Frontend

Rode a partir da raiz do projeto (o Streamlit procura `.streamlit/` no diretório atual):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .streamlit\secrets.toml.example .streamlit\secrets.toml   # cole a Base URL do Xano
streamlit run src/app.py
```

Acesse <http://localhost:8501>. Sem `secrets.toml` configurado, o app mostra como configurá-lo.

## 3. Testes

```powershell
pytest                                                                                 # sem rede
python scripts/teste_integracao.py https://x8ki-letl-twmt.n7.xano.io/api:orbitfingm   # contra o Xano real
```

O teste de integração cria um usuário descartável (`teste-…@orbitfin.test`); apague-o em Xano > Database > user.

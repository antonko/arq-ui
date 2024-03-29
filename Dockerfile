FROM node:20 as frontend-builder

RUN corepack enable && yarn set version berry

WORKDIR /app/frontend

COPY ./frontend/package.json ./frontend/yarn.lock ./
COPY ./frontend/.yarn ./.yarn
COPY ./frontend/.yarnrc.yml ./

RUN yarn install

COPY ./frontend .

ENV NODE_ENV=production

RUN yarn build --mode production

FROM python:3.11-slim as backend-builder

RUN pip install pdm

WORKDIR /app

COPY ./backend/pyproject.toml ./backend/pdm.lock ./

RUN pdm install --prod

COPY ./backend/src ./src
COPY --from=frontend-builder /app/frontend/dist ./src/static

WORKDIR /app/src

EXPOSE 8000

ENTRYPOINT ["pdm", "run", "uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]

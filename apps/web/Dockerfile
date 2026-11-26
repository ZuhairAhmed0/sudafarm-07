FROM node:22-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME/bin:$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app

# 1. Keep only the files that "web" needs
FROM base AS pruner
RUN pnpm add -g turbo
COPY . .
RUN turbo prune web --docker

# 2. Install and build
FROM base AS builder
COPY --from=pruner /app/out/json/ .
RUN pnpm install --frozen-lockfile
COPY --from=pruner /app/out/full/ .
RUN pnpm turbo run build --filter=web

# 3. Serve with nginx
FROM nginx:alpine
ENV BACKEND_URL="https://sudafarm.onrender.com"
COPY apps/web/nginx.conf /etc/nginx/conf.d/default.conf
COPY apps/web/nginx.conf.template /etc/nginx/templates/default.conf.template
COPY apps/web/docker-entrypoint.sh /docker-entrypoint.d/40-render-backend.sh
RUN sed -i 's/\r$//' /docker-entrypoint.d/40-render-backend.sh && chmod +x /docker-entrypoint.d/40-render-backend.sh
COPY --from=builder /app/apps/web/dist /usr/share/nginx/html
EXPOSE 80
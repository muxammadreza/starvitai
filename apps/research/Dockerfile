FROM node:22-alpine
WORKDIR /app
RUN npm install -g pnpm@10.26.0
ENV CI=true
COPY . .
RUN pnpm install
RUN pnpm turbo run build --filter=@starvit/research...
CMD ["pnpm", "--filter", "@starvit/research", "start"]

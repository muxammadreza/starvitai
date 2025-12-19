FROM node:18-alpine
WORKDIR /app
RUN npm install -g pnpm
COPY . .
RUN pnpm install
RUN pnpm --filter @starvit/research build
CMD ["pnpm", "--filter", "@starvit/research", "start"]

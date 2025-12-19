FROM node:25-alpine
WORKDIR /app
RUN npm install -g pnpm
COPY . .
RUN pnpm install
RUN pnpm --filter @starvit/clinician build
CMD ["pnpm", "--filter", "@starvit/clinician", "start"]

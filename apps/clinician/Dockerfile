FROM node:22-alpine
WORKDIR /app
RUN npm install -g pnpm
ENV CI=true
COPY . .
RUN pnpm install
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
RUN pnpm turbo run build --filter=@starvit/clinician...
CMD ["pnpm", "--filter", "@starvit/clinician", "start"]

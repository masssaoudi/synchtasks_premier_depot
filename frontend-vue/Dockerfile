# Frontend Dockerfile (Vue.js) - Production Ready
FROM node:20-alpine as builder

WORKDIR /app

# Copier les fichiers de dépendances et node_modules
COPY package*.json ./
COPY node_modules ./node_modules

# Réinstaller esbuild pour Linux (résout les problèmes de plateforme)
RUN npm rebuild esbuild

# Copier le code source
COPY . .

# Build de l'application
RUN npm run build

# Stage de production avec nginx
FROM nginx:alpine

# Copier les fichiers buildés
COPY --from=builder /app/dist /usr/share/nginx/html

# Copier la configuration nginx personnalisée
COPY nginx.conf /etc/nginx/nginx.conf

# Exposer le port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"] 
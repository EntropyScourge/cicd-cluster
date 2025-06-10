# Use the official PostgreSQL image from Docker Hub
FROM postgres:15

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=adminpassword
ENV POSTGRES_DB=postgresdb

# Expose the default PostgreSQL port
EXPOSE 5432

# Add any custom initialization scripts (optional)
COPY seed.sql /docker-entrypoint-initdb.d/

# Default command to run PostgreSQL
CMD ["postgres"]
# Use the official PostgreSQL image from Docker Hub
FROM postgres

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=postgres

# Expose the default PostgreSQL port
EXPOSE 5432

# Add any custom initialization scripts (optional)
COPY seed.sql /docker-entrypoint-initdb.d/

# Default command to run PostgreSQL
CMD ["postgres"]
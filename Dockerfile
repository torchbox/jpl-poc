FROM python:3.8

ENV PYTHONUNBUFFERED 1

# APT dependencies
RUN apt-get update && apt-get install -y \
  postgresql-client

# Install Node.js 12.x
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
  apt-get install -y nodejs=12\*

RUN pip install poetry
RUN npm install -g yarn gulp-cli

# Node dependencies
RUN mkdir -p /node_cache/jpl-poc
RUN mkdir -p /app/node_modules
WORKDIR /node_cache/jpl-poc
COPY package.json yarn.lock ./
RUN yarn install

# Python dependencies
WORKDIR /app
COPY wagtail-2.9a0.tar.gz ./
ADD pyproject.toml poetry.lock ./
RUN poetry install

# Copy project files
COPY . /app
RUN rm -rf /app/node_modules && \
  ln -s /node_cache/jpl-poc/node_modules /app/node_modules

# Compile front-end
RUN gulp build --prod

# Load shortcuts
RUN cat bin/shortcuts >> /root/.bashrc

RUN poetry run python manage.py collectstatic --noinput
EXPOSE 8000

CMD ["bin/run_prod"]

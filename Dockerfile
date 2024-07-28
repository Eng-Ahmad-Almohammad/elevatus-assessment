# Python version
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements/base.txt /code/
RUN pip install --no-cache-dir --upgrade -r base.txt
EXPOSE 8000

# Copy project
COPY . /code/

RUN chmod +x /code/entrypoint.sh

ENTRYPOINT [ "/code/entrypoint.sh" ]
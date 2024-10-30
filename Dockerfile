FROM python:3.11
WORKDIR /workdir
COPY . .
RUN pip install --upgrade pip && pip install \
    black \
    flake8 \
    mutmut==2.* \
    mypy \
    pylint \
    pytest \
    pytest-cov

RUN make install

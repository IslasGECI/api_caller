FROM python:3.11
WORKDIR /workdir
COPY . .
RUN pip install --upgrade pip && pip install \
    black \
    flake8 \
    geci_test_tools \
    mutmut==2.* \
    mypy \
    pillow \
    pylint \
    pytest \
    pytest-cov

RUN make install

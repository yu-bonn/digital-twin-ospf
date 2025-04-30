FROM debian:bullseye

RUN apt-get update && apt-get install -y \
  build-essential \
  autoconf \
  automake \
  libtool \
  git \
  python3 \
  python3-pip \
  snmp \
  libsnmp-dev \
  vim \
  && apt-get clean

# 作業ディレクトリ
WORKDIR /app

# 必要なソースをコピー（simroutingのみ）
COPY ./src /app/src

# Pythonライブラリ
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# src/以下はMacからのマウントに任せるのでCOPYしない
CMD ["bash"]

with import <nixpkgs> {};

let
  heroku-cli = 1;

in stdenv.mkDerivation rec {
  name = "env";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [
    gcc
    libffi
    python36
    openssl
    postgresql
    pkgconfig
  ];
}

class SolanaInitTemplates:

    def __init__(self, project_name, programs_list):

        self.TYPESCRIPT_TEMPLATE = """

/* 
TypeScript hello world template.
*/

async function main() {
  console.log('Hello, World!');
}


main().then(
    () => process.exit(),
    err => {
      console.error(err);
      process.exit(-1);
    },
  );

"""

        self.DOCKERFILE_TEMPLATE = """
FROM frolvlad/alpine-glibc

RUN apk update && apk upgrade -a &&\
    apk add --update bash build-base wget curl nodejs npm eudev-dev &&\
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y -q &&\
    mv root/.cargo $PWD/.cargo &&\
    wget -o solana-release.tar.bz2 https://github.com/solana-labs/solana/releases/download/v1.10.6/solana-release-x86_64-unknown-linux-gnu.tar.bz2 &&\
    tar jxf solana-release-x86_64-unknown-linux-gnu.tar.bz2

ENV PATH=$PWD/.cargo/bin:$PWD/solana-release/bin:$PATH

RUN solana-keygen new --no-bip39-passphrase &&\
    solana config set --keypair /root/.config/solana/id.json &&\
    solana config set --url http://api.devnet.solana.com &&\
    solana airdrop 2

COPY src src
COPY package.json package.json

RUN npm run build &&\
    npm run deploy

ENTRYPOINT npm run start
"""

        self.README_TEMPLATE = f"""# {project_name}

"""
        self.PACKAGE_JSON_TEMPLATE = f"""
{
    "name": "{project_name}",
    "version": "0.0.1",
    "scripts": {
        "start": "ts-node src/client/main.ts",
        "clean": "npm run clean:program",
        "build:program": "cargo build-bpf --manifest-path=./src/program/Cargo.toml --bpf-out-dir=dist/program",
        "clean:program": "cargo clean --manifest-path=./src/program/Cargo.toml && rm -rf ./dist",
        "test:program": "cargo test-bpf --manifest-path=./src/program/Cargo.toml"
    },
    "dependencies": {
        "@solana/web3.js": "^1.37.1",
        "mz": "^2.7.0"
    },
    "devDependencies": {
        "@tsconfig/recommended": "^1.0.1",
        "@types/mz": "^2.7.2",
        "ts-node": "^10.0.0",
        "typescript": "^4.0.5"
    },
    "engines": {
        "node": ">=14.0.0"
    }
}
"""
        program_bash_array = "("
        for program in programs_list:
            program_bash_array += program + " "
        program_bash_array = program_bash_array[:-1] +  ")"
        self.CICD_SH_TEMPLATE = f"""
#! /bin/bash

SOLANA_PROGRAMS={program_bash_array}""" + """

case $1 in
    "reset")
        rm -rf ./node_modules
        for x in $(solana program show --programs | awk 'RP==0 {print $1}'); do 
            if [[ $x != "Program" ]]; 
            then 
                solana program close $x;
            fi
        done
        rm -rf dist/program
        ;;
    "clean")
        rm -rf ./node_modules
        for program in "${SOLANA_PROGRAMS[@]}"; do
            cargo clean --manifest-path=./src/$program/Cargo.toml
        done;;
    "build")
        for program in "${SOLANA_PROGRAMS[@]}"; do
            cargo build-bpf --manifest-path=./src/$program/Cargo.toml --bpf-out-dir=./dist/program
        done;;
    "deploy")
        for program in "${SOLANA_PROGRAMS[@]}"; do
            cargo build-bpf --manifest-path=./src/$program/Cargo.toml --bpf-out-dir=./dist/program
            solana program deploy dist/program/$program.so
        done;;
    "example")
        npm install
        ts-node ./src/example/hotel.ts
        ;;
    "reset-and-build")
        rm -rf ./node_modules
        for x in $(solana program show --programs | awk 'RP==0 {print $1}'); do 
            if [[ $x != "Program" ]]; 
            then 
                solana program close $x; 
            fi
        done
        rm -rf dist/program
        for program in "${SOLANA_PROGRAMS[@]}"; do
            cargo clean --manifest-path=./src/$program/Cargo.toml
            cargo build-bpf --manifest-path=./src/$program/Cargo.toml --bpf-out-dir=./dist/program
            solana program deploy dist/program/$program.so
        done
        npm install
        solana program show --programs
        ;;
esac
"""
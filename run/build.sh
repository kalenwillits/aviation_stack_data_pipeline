if [[ -z "$APP" ]]; then
    echo "Missing APP environment variable" 1>&2
    exit 1
fi

cd ./src/$APP/;
./build.sh

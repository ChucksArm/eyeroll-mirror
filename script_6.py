import zipfile, pathlib
base = pathlib.Path('output')
zip_path = base/'eyeroll_tenderloin_bundle_v6_deploy.zip'
files = [
    base/'eyeroll-mirror'/'tenderloin-mirror-static.html',
    base/'eyeroll-mirror'/'latest-frames.json',
    base/'eyeroll-mirror'/'archive-index.json',
    base/'eyeroll-recorder'/'package.json',
    base/'eyeroll-recorder'/'recorder.js',
    base/'eyeroll-recorder'/'README.md',
    base/'eyeroll-recorder'/'DEPLOY.md',
    base/'eyeroll-recorder'/'setup-macbook-intel.sh',
    base/'eyeroll-recorder'/'ecosystem.config.js',
    base/'eyeroll-recorder'/'scripts'/'build-archives.js',
    base/'eyeroll-recorder'/'scripts'/'build-index.js',
    base/'eyeroll-recorder'/'scripts'/'build-latest-frames.js',
    base/'eyeroll-recorder'/'scripts'/'refresh-all.sh',
    base/'eyeroll-recorder'/'.github'/'workflows'/'deploy.yml',
    base/'eyeroll-recorder'/'deploy'/'nginx-eyeroll.conf',
    base/'eyeroll-recorder'/'deploy'/'lightsail-bootstrap.sh',
]
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for f in files:
        if f.exists():
            z.write(f, arcname=f.relative_to(base))
print(zip_path, zip_path.stat().st_size)
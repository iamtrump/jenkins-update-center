# jenkuc — Jenkins update center
Simple Jenkins update center implementation.

## Limitations
* Supported Jenkins >= 1.432 ([info](https://github.com/jenkinsci/jenkins/blob/62f66f899c95ccdfdc7a5d3346240988b42a9aad/core/src/main/java/jenkins/util/JSONSignatureValidator.java#L101))

## Installation
```
pip install git+https://github.com/iamtrump/jenkins-update-center
```

## Steps to create local mirror of Jenkins update center:
1. Generate self-signed certificate:
```
openssl genrsa -out update-center.key 2048
openssl req -new -x509 -days 1825 -key update-center.key -outform der -out update-center.der
```
2. Rsync `plugins` and `war` dirs into your www root directory:
```
rsync -avz --delete rsync://rsync.osuosl.org/jenkins/plugins/ /srv/www/jenkins/plugins
rsync -avz --delete rsync://rsync.osuosl.org/jenkins/war/ /srv/www/jenkins/war
```
3. Download original `update-center.json`:
```
rsync rsync://rsync.osuosl.org/jenkins/updates/current/update-center.json /tmp/update-center.json.original
```
4. Run the following python code:
```
import jenkuc
import json

original_update_center_json = "/tmp/update-center.json.original"
www_root = "/srv/www/jenkins"
www_url = "http://jenkins.local"
private_key = "update-center.key"
public_key = "update-center.der"

# Load origignal update center
with open(original_update_center_json, "r") as fd:
  original = json.loads(fd.read().replace("updateCenter.post(\n", "").replace("\n);", ""))

uc = jenkuc.JenkinsUpdateCenter()
uc.load_private(private_key)
uc.load_public(public_key)
uc.plugins=json.loads(json.dumps(original["plugins"]).replace("http://updates.jenkins-ci.org/download/plugins/", www_url+"/plugins/"))
uc.warnings=original["warnings"]
uc.core=json.loads(json.dumps(original["core"]).replace("http://updates.jenkins-ci.org/download/war/", www_url+"/war/"))
with open(www_root+"/update-center.json", "w") as fd:
  uc.out(fd)
```
5. Put `update-center.der` into `${JENKINS_HOME}/update-center-rootCAs` folder.
6. Go to `Jenkins → Manage Jenkins → Manage Plugins → Advanced → Update Site` and submit URL to your `update-center.json`.

#!/usr/bin/env python
import json
import base64
import binascii
from Crypto.Hash import SHA512, SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class JenkinsUpdateCenter:
  def __init__(self):
    self.updateCenterVersion = "1"
    self.core = None
    self.warnings = None
    self.plugins = None
    self.id = "default"
    self.connectionCheckUrl = None
    self._private_key = None
    self._cert = [None]

  def _sha1_digest(self, body):
    digest = base64.b64encode(SHA.new(body).digest()).decode("utf-8")
    return digest

  def _sha512_digest(self, body):
    digest = binascii.hexlify(SHA512.new(body).digest()).decode("utf-8")
    return digest

  def _sign(self, body, algo = "SHA-1"):
    signer = PKCS1_v1_5.new(self._private_key)
    if algo == "SHA-1":
      digest = SHA.new()
    else:
      digest = SHA512.new()
    digest.update(body)
    try:
      signature = signer.sign(digest)
    except Exception as err:
      raise Exception("Could not make sign. "+str(err))
    return signature

  def _sha1_signature(self, body):
    signature = base64.b64encode(self._sign(body, "SHA-1")).decode("utf-8")
    return signature

  def _sha512_signature(self, body):
    signature = binascii.hexlify(self._sign(body, "SHA-512")).decode("utf-8")
    return signature

  def load_private(self, key_path):
    try:
      with open(key_path, "r") as fd:
        self._private_key = RSA.importKey(fd.read())
    except Exception as err:
      raise Exception("Could not load private key "+key_path+". "+str(err))

  def load_public(self, key_path):
    try:
      with open(key_path, "rb") as fd:
        self._cert = base64.b64encode(fd.read()).decode("utf-8")
    except Exception as err:
      raise Exception("Could not load public key "+key_path+". "+str(err))

  def out(self, fd):
    output = {}
    output["updateCenterVersion"] = self.updateCenterVersion
    if self.core is not None:
      output["core"] = self.core
    if self.warnings is not None:
      output["warnings"] = self.warnings
    if self.plugins is not None:
      output["plugins"] = self.plugins
    output["id"] = self.id
    if self.connectionCheckUrl is not None:
      output["connectionCheckUrl"] = self.connectionCheckUrl
    payload = (json.dumps(output, separators=(",", ":"), sort_keys=True, ensure_ascii=False).encode("utf-8"))
    output["signature"] = {"certificates":[self._cert]}
    output["signature"]["correct_digest"] = self._sha1_digest(payload)
    output["signature"]["correct_digest512"] = self._sha512_digest(payload)
    output["signature"]["correct_signature"] = self._sha1_signature(payload)
    output["signature"]["correct_signature512"] = self._sha512_signature(payload)
    try:
      fd.write("updateCenter.post(\n"+json.dumps(output, separators=(",", ":"), sort_keys=True)+"\n);")
    except Exception as err:
      raise Exception("Could not write output. "+str(err))

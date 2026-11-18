# DeepTutor for Railway: the official image, pinned by version and digest,
# plus a small first-boot script that turns on login and sets the port.
FROM ghcr.io/hkuds/deeptutor:1.7.3@sha256:dff6d6ef37bcb433e67addb2cc6fd06e9b504f6acfe66e91a1162c1b0d1ee801

COPY railway/railway-setup.py /opt/railway/railway-setup.py
COPY --chmod=0755 railway/start.sh /opt/railway/start.sh

EXPOSE 3782

ENTRYPOINT ["/opt/railway/start.sh"]

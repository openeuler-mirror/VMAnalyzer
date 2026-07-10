#!/usr/bin/env python3
"""Certificate manager for TLS/SSL certificate lifecycle."""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import time
import hashlib
import threading

class CertStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    PENDING = "pending"
    RENEWING = "renewing"

@dataclass
class Certificate:
    common_name: str
    serial_number: str
    issuer: str
    not_before: float
    not_after: float
    fingerprint: str = ""
    status: CertStatus = CertStatus.ACTIVE
    san: List[str] = field(default_factory=list)
    key_algorithm: str = "RSA-2048"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        return time.time() > self.not_after

    def is_expiring_soon(self, days: int = 30) -> bool:
        return time.time() + (days * 86400) > self.not_after

    def days_until_expiry(self) -> float:
        return (self.not_after - time.time()) / 86400

    def to_dict(self) -> Dict[str, Any]:
        return {
            "common_name": self.common_name,
            "serial_number": self.serial_number,
            "issuer": self.issuer,
            "not_before": self.not_before,
            "not_after": self.not_after,
            "fingerprint": self.fingerprint,
            "status": self.status.value,
            "san": self.san,
            "key_algorithm": self.key_algorithm,
        }

class CertificateManager:
    def __init__(self, renewal_threshold_days: int = 30):
        self._certs: Dict[str, Certificate] = {}
        self._renewal_threshold = renewal_threshold_days
        self._lock = threading.Lock()
        self._renewal_callbacks: List = []
        self._stats = {"issued": 0, "renewed": 0, "revoked": 0, "expired": 0}
        self._ca_cert: Optional[Certificate] = None

    def set_ca_certificate(self, cert: Certificate) -> None:
        self._ca_cert = cert

    def issue_certificate(self, common_name: str, issuer: str = "self-signed",
                          validity_days: int = 365, san: Optional[List[str]] = None,
                          key_algorithm: str = "RSA-2048") -> Certificate:
        now = time.time()
        serial = hashlib.sha256(f"{common_name}{now}".encode()).hexdigest()[:16]
        fingerprint = hashlib.sha256(f"{common_name}{serial}{issuer}".encode()).hexdigest()
        cert = Certificate(
            common_name=common_name,
            serial_number=serial,
            issuer=issuer,
            not_before=now,
            not_after=now + (validity_days * 86400),
            fingerprint=fingerprint,
            san=san or [],
            key_algorithm=key_algorithm,
        )
        with self._lock:
            self._certs[serial] = cert
            self._stats["issued"] += 1
        return cert

    def get_certificate(self, serial: str) -> Optional[Certificate]:
        with self._lock:
            return self._certs.get(serial)

    def find_by_common_name(self, cn: str) -> List[Certificate]:
        with self._lock:
            return [c for c in self._certs.values() if c.common_name == cn]

    def find_by_sAN(self, hostname: str) -> Optional[Certificate]:
        with self._lock:
            for cert in self._certs.values():
                if hostname in cert.san or cert.common_name == hostname:
                    if cert.status == CertStatus.ACTIVE and not cert.is_expired():
                        return cert
        return None

    def revoke_certificate(self, serial: str) -> bool:
        with self._lock:
            cert = self._certs.get(serial)
            if cert and cert.status == CertStatus.ACTIVE:
                cert.status = CertStatus.REVOKED
                self._stats["revoked"] += 1
                return True
            return False

    def renew_certificate(self, serial: str, validity_days: int = 365) -> Optional[Certificate]:
        with self._lock:
            old_cert = self._certs.get(serial)
            if not old_cert:
                return None
            old_cert.status = CertStatus.RENEWING
        new_cert = self.issue_certificate(
            old_cert.common_name, old_cert.issuer,
            validity_days, old_cert.san, old_cert.key_algorithm
        )
        with self._lock:
            old_cert.status = CertStatus.EXPIRED
            self._stats["renewed"] += 1
        for callback in self._renewal_callbacks:
            try:
                callback(old_cert, new_cert)
            except Exception:
                pass
        return new_cert

    def check_expirations(self) -> List[Certificate]:
        expiring = []
        with self._lock:
            for cert in self._certs.values():
                if cert.is_expired() and cert.status == CertStatus.ACTIVE:
                    cert.status = CertStatus.EXPIRED
                    self._stats["expired"] += 1
                elif cert.is_expiring_soon(self._renewal_threshold) and \
                     cert.status == CertStatus.ACTIVE:
                    expiring.append(cert)
        return expiring

    def add_renewal_callback(self, callback) -> None:
        self._renewal_callbacks.append(callback)

    def list_certificates(self, status: Optional[CertStatus] = None) -> List[Certificate]:
        with self._lock:
            if status:
                return [c for c in self._certs.values() if c.status == status]
            return list(self._certs.values())

    def delete_certificate(self, serial: str) -> bool:
        with self._lock:
            if serial in self._certs:
                del self._certs[serial]
                return True
            return False

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    @property
    def cert_count(self) -> int:
        with self._lock:
            return len(self._certs)

    def get_expiring_certs(self, days: int = 30) -> List[Certificate]:
        with self._lock:
            return [c for c in self._certs.values()
                   if c.is_expiring_soon(days) and c.status == CertStatus.ACTIVE]

    def export_certificates(self) -> List[Dict]:
        with self._lock:
            return [c.to_dict() for c in self._certs.values()]

    def set_renewal_threshold(self, days: int) -> None:
        self._renewal_threshold = days

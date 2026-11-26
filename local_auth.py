from collections import deque
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import blake2s, pbkdf2_hmac
from hmac import compare_digest
import re
from secrets import token_bytes
from threading import Lock
from time import monotonic


HASH_ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 600_000
MAX_PASSWORD_LENGTH = 256
TOTAL_SESSION_SECONDS = 8 * 60 * 60
IDLE_SESSION_SECONDS = 30 * 60
ROLES = {"admin", "consulta", "consulta_academica"}
HASH_PATTERN = re.compile(rf"{HASH_ALGORITHM}[$]{ITERATIONS}[$]([0-9a-f]{{32}})[$]([0-9a-f]{{64}})")


def normalize_username(username):
    username = username.strip().lower()
    return username if re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,63}", username) else ""


def password_digest(password, salt):
    return pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)


def hash_password(password):
    if not 16 <= len(password) <= MAX_PASSWORD_LENGTH:
        raise ValueError("La contraseña debe tener entre 16 y 256 caracteres.")
    salt = token_bytes(16)
    digest = password_digest(password, salt)
    return "$".join((HASH_ALGORITHM, str(ITERATIONS), salt.hex(), digest.hex()))


@dataclass(frozen=True)
class Account:
    name: str
    role: str
    salt: bytes
    digest: bytes

    @property
    def revision(self):
        return self.role, self.salt, self.digest


def read_accounts(config):
    accounts = {}
    if not isinstance(config, Mapping):
        return accounts
    for username, settings in config.items():
        normalized = normalize_username(username)
        if normalized != username or not normalized or not isinstance(settings, Mapping):
            continue
        role = settings.get("rol")
        name = settings.get("nombre")
        encoded = settings.get("hash_contrasena")
        match = HASH_PATTERN.fullmatch(encoded) if isinstance(encoded, str) else None
        if isinstance(role, str) and role in ROLES and isinstance(name, str) and name.strip() and match:
            salt, digest = (bytes.fromhex(value) for value in match.groups())
            accounts[username] = Account(name.strip(), role, salt, digest)
    return accounts


def verify_password(password, account):
    if not password or len(password) > MAX_PASSWORD_LENGTH:
        return False
    # Realiza el mismo trabajo para usuarios inexistentes sin guardar sus intentos por nombre.
    salt = account.salt if account else bytes(16)
    expected = account.digest if account else bytes(32)
    return compare_digest(password_digest(password, salt), expected) and account is not None


class AttemptLimiter:
    def __init__(self, clock=monotonic):
        self.clock = clock
        self.lock = Lock()
        self.recent = deque()
        self.bucket_key = token_bytes(16)
        self.buckets = [deque() for _ in range(256)]

    def bucket(self, username):
        # Un conjunto fijo evita que nombres inventados hagan crecer la memoria.
        index = blake2s(username.encode("ascii"), key=self.bucket_key, digest_size=1).digest()[0]
        return self.buckets[index]

    @staticmethod
    def discard_expired(timestamps, cutoff):
        while timestamps and timestamps[0] <= cutoff:
            timestamps.popleft()

    def reserve(self, username):
        with self.lock:
            now = self.clock()
            self.discard_expired(self.recent, now - 60)
            if len(self.recent) >= 40:
                return False

            attempts = self.bucket(username)
            self.discard_expired(attempts, now - 300)
            if len(attempts) >= 8:
                return False
            attempts.append(now)
            self.recent.append(now)
            return True

    def reset_account(self, username):
        with self.lock:
            self.bucket(username).clear()


login_attempts = AttemptLimiter()


def current_account(session, accounts, now):
    if session is None:
        return None
    username, revision, started, last_activity = session
    account = accounts.get(username)
    if (account is None or account.revision != revision
            or now - started >= TOTAL_SESSION_SECONDS
            or now - last_activity >= IDLE_SESSION_SECONDS):
        return None
    return account

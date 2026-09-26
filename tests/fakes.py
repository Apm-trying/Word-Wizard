"""Lightweight in-memory stand-in for the Supabase client, used by the tests
in this folder so they never make a real network call. Mimics just the
chained-call shape learner.py actually uses:
    client.table("progress").select("data").eq("nickname", n).execute()
    client.table("progress").upsert({...}).execute()
    client.table("progress").delete().eq("nickname", n).execute()
"""


class _Result:
    def __init__(self, data):
        self.data = data


class _Query:
    def __init__(self, store, op, payload=None):
        self.store = store
        self.op = op
        self.payload = payload
        self._nickname_filter = None

    def select(self, *_args, **_kwargs):
        return self

    def eq(self, _column, value):
        self._nickname_filter = value
        return self

    def execute(self):
        if self.op == "select":
            row = self.store.rows.get(self._nickname_filter)
            self.store.select_calls += 1
            return _Result([row] if row else [])
        if self.op == "upsert":
            nickname = self.payload["nickname"]
            self.store.rows[nickname] = self.payload
            self.store.upsert_calls += 1
            return _Result([self.payload])
        if self.op == "delete":
            self.store.rows.pop(self._nickname_filter, None)
            return _Result([])
        raise AssertionError(f"unexpected op {self.op}")


class _Table:
    def __init__(self, store):
        self.store = store

    def select(self, *args, **kwargs):
        return _Query(self.store, "select")

    def upsert(self, payload):
        return _Query(self.store, "upsert", payload)

    def delete(self):
        return _Query(self.store, "delete")


class FakeSupabaseClient:
    """Call-counting fake. rows: nickname -> {"nickname":, "data": {...}}."""

    def __init__(self):
        self.rows = {}
        self.select_calls = 0
        self.upsert_calls = 0

    def table(self, _name):
        return _Table(self)

    def seed(self, nickname, data):
        self.rows[nickname] = {"nickname": nickname, "data": data}

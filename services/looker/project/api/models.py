from project import db


def get_attrs(dx_looker):
    attrs = []
    for attr in dir(dx_looker):
        if not callable(getattr(dx_looker, attr)) and not attr.startswith("__"):
            attrs.append(attr)
    return attrs


# potentially change name to reflect the specificity of the columns
class DXLooker(db.Model):
    __tablename__ = "dx_looker"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    email_send_month = db.Column(db.DateTime, nullable=False)

    net = db.Column(db.BigInteger)
    csharp = db.Column(db.BigInteger)
    django = db.Column(db.BigInteger)
    go = db.Column(db.BigInteger)
    java = db.Column(db.BigInteger)
    nodejs = db.Column(db.BigInteger)
    perl = db.Column(db.BigInteger)
    php = db.Column(db.BigInteger)
    prolific = db.Column(db.BigInteger)
    python = db.Column(db.BigInteger)
    ruby = db.Column(db.BigInteger)
    scala = db.Column(db.BigInteger)
    swift = db.Column(db.BigInteger)

    def to_json(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def set_tablename(self, name: str):
        self.__tablename__ = name

    def __repr__(self):
        str_list = []
        for attr, value in self.to_json().items():
            str_list.append("{}={}".format(attr, value))
        return "{}({})".format(self.__class__.__name__, ",".join(str_list))


class SendsByLibrary(db.Model):
    __tablename__ = "sends_by_library"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    email_send_month = db.Column(db.DateTime, nullable=False)

    net = db.Column(db.BigInteger)
    csharp = db.Column(db.BigInteger)
    django = db.Column(db.BigInteger)
    go = db.Column(db.BigInteger)
    java = db.Column(db.BigInteger)
    nodejs = db.Column(db.BigInteger)
    perl = db.Column(db.BigInteger)
    php = db.Column(db.BigInteger)
    prolific = db.Column(db.BigInteger)
    python = db.Column(db.BigInteger)
    ruby = db.Column(db.BigInteger)
    scala = db.Column(db.BigInteger)
    swift = db.Column(db.BigInteger)

    def to_json(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def set_tablename(self, name: str):
        self.__tablename__ = name

    def __repr__(self):
        str_list = []
        for attr, value in self.to_json().items():
            str_list.append("{}={}".format(attr, value))
        return "{}({})".format(self.__class__.__name__, ",".join(str_list))


class InvoicingByLibrary(db.Model):
    __tablename__ = "invoicing_by_library"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    email_send_month = db.Column(db.DateTime, nullable=False)

    net = db.Column(db.BigInteger)
    csharp = db.Column(db.BigInteger)
    django = db.Column(db.BigInteger)
    go = db.Column(db.BigInteger)
    java = db.Column(db.BigInteger)
    nodejs = db.Column(db.BigInteger)
    perl = db.Column(db.BigInteger)
    php = db.Column(db.BigInteger)
    prolific = db.Column(db.BigInteger)
    python = db.Column(db.BigInteger)
    ruby = db.Column(db.BigInteger)
    scala = db.Column(db.BigInteger)
    swift = db.Column(db.BigInteger)

    def to_json(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def set_tablename(self, name: str):
        self.__tablename__ = name

    def __repr__(self):
        str_list = []
        for attr, value in self.to_json().items():
            str_list.append("{}={}".format(attr, value))
        return "{}({})".format(self.__class__.__name__, ",".join(str_list))

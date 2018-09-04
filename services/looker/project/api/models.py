from project import db


def get_attrs(dx_looker):
    attrs = []
    for attr in dir(dx_looker):
        if not callable(getattr(dx_looker, attr)) and not attr.startswith("__"):
            attrs.append(attr)
    return attrs


class DXLooker(db.Model):
    __tablename__ = "dx_looker"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    email_send_month = db.Column(db.DateTime, nullable=False)

    net = db.Column(db.Integer)
    csharp = db.Column(db.Integer)
    django = db.Column(db.Integer)
    go = db.Column(db.Integer)
    java = db.Column(db.Integer)
    nodejs = db.Column(db.Integer)
    perl = db.Column(db.Integer)
    php = db.Column(db.Integer)
    prolific = db.Column(db.Integer)
    python = db.Column(db.Integer)
    ruby = db.Column(db.Integer)
    scala = db.Column(db.Integer)
    swift = db.Column(db.Integer)

    def to_json(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def set_tablename(self, name: str):
        self.__tablename__ = name

    def __repr__(self):
        str_list = []
        for attr, value in self.to_json().items():
            str_list.append("{}={}".format(attr, value))
        return "{}({})".format(self.__class__.__name__, ",".join(str_list))


class SendsByLibrary(DXLooker):
    __tablename__ = "4404_mail_sends_by_library_language"


class InvoicingByLibrary(DXLooker):
    __tablename__ = "4405_invoicing_by_library_language"

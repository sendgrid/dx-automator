from project import db

class AddUpdateDelete():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

class Hacktoberfest(db.Model, AddUpdateDelete):
    __tablename__ = 'hacktoberfest'

    id = db.Column(db.Integer, primary_key=True)
    swag_id = db.Column(db.Integer, db.ForeignKey('swag.id'))
    time_logged = db.Column(db.DateTime(timezone=True), unique=False)
    total_points = db.Column(db.Integer)
    hacktoberfest_swag_sent = db.Column(db.Integer) # year
    hacktoberfest_approved = db.Column(db.Boolean, unique=False, default=False)
    email_address = db.Column(db.String(255), unique=False)
    sendgrid_employee = db.Column(db.Boolean)
    sendgrid_customer = db.Column(db.Boolean)
    swag = db.relationship("Swag")

class GitHubContributions(db.Model, AddUpdateDelete):
    __tablename__ = 'githubcontributions'

    id = db.Column(db.Integer, primary_key=True)
    swag_id = db.Column(db.Integer, db.ForeignKey('swag.id'))
    time_logged = db.Column(db.DateTime(timezone=True), unique=False)
    github_url = db.Column(db.Text, unique=False)
    point_value = db.Column(db.Integer)
    swag = db.relationship("Swag")

class Log(db.Model, AddUpdateDelete):
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True)
    time_logged = db.Column(db.DateTime(timezone=True), unique=True)
    action = db.Column(db.String(255), unique=False)
    delta = db.Column(db.Text, unique=False)
    error = db.Column(db.Text, unique=False)
    affected_systems = db.Column(db.String(255), unique=False)

    def __init__(self,
                 time_logged=None,
                 action=None,
                 delta=None,
                 error=None,
                 affected_systems=None):
        self.time_logged = time_logged
        self.action = action
        self.delta = delta
        self.error = error
        self.affected_systems = affected_systems

    def add_log_entry(self,
                      time_logged,
                      action,
                      delta,
                      error,
                      affected_systems):
        self.time_logged = time_logged
        self.action = action
        self.delta = delta
        self.error = error
        self.affected_systems = affected_systems
        self.add(self)

    def __repr__(self):
        """Return a machine-readable representation of this Log object.
        Only trouble is, a log entry has an ID property which is determined
        on creation.  Reporting it here means this isn't executable to make a
        new log entry.
        """
        return ("{classname}("
                "id={id!r}, "
                "time_logged={time_logged!r}, "
                "action={action!r}, "
                "delta={delta!r}, "
                "error={error!r}, "
                "affected_systems={affected_systems!r})").format(
                    classname=self.__class__.__name__,
                    id=self.id,
                    time_logged=self.time_logged,
                    action=self.action,
                    delta=self.delta,
                    error=self.error,
                    affected_systems=self.affected_systems)


class Swag(db.Model, AddUpdateDelete):
    __tablename__ = 'swag'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), unique=False)
    full_name = db.Column(db.String(255), unique=False)
    github_username = db.Column(db.String(255), unique=True)
    attention = db.Column(db.String(255), unique=False)
    # TODO: Use Phone Number Type: http://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.phone_number
    phone_number = db.Column(db.String(30), unique=False)
    link_to_github_issue = db.Column(db.String(255), unique=False)
    t_shirt_size = db.Column(db.String(10), unique=False)
    notes = db.Column(db.Text, unique=False)
    twitter_handle = db.Column(db.String(100), unique=False)
    address = db.Column(db.String(255), unique=False)
    address_2 = db.Column(db.String(255), unique=False)
    city = db.Column(db.String(255), unique=False)
    country = db.Column(db.String(255), unique=False)
    state = db.Column(db.String(100), unique=False)
    zip_code = db.Column(db.String(100), unique=False)
    address_type = db.Column(db.String(100), unique=False)
    verified = db.Column(db.Boolean)
    sendgrid_contact = db.Column(db.String(255), unique=False)
    date_sent = db.Column(db.DateTime(timezone=True), unique=False)
    what_we_sent = db.Column(db.Text, unique=False)
    followed_up = db.Column(db.DateTime(timezone=True), unique=False)
    email_address = db.Column(db.String(255), unique=False)
    hacktoberfest = db.relationship("Hacktoberfest")
    hacktoberfest_t_shirt_size = db.Column(db.String(10), unique=False)
    githubcontributions = db.relationship("GitHubContributions")
    is_gridder = db.Column(db.Boolean)

    def __init__(self,
                 form_submission_time=None,
                 full_name=None,
                 github_username=None,
                 attention=None,
                 phone_number=None,
                 link_to_github_issue=None,
                 t_shirt_size=None,
                 notes=None,
                 twitter_handle=None,
                 address=None,
                 address_2=None,
                 city=None,
                 country=None,
                 state=None,
                 zip_code=None,
                 address_type=None,
                 verified=None,
                 sendgrid_contact=None,
                 date_sent=None,
                 what_we_sent=None,
                 followed_up=None,
                 email_address=None,
                 is_gridder=None):
        vars(self).update(locals())
        del self.self  # self gets added, since it's an arg too
        self.timestamp = vars(self).pop('form_submission_time')  # rename

    def add_swag_entry(self):
        self.add(self)
